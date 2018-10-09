import requests
from webhook import DiscordWebhook, DiscordEmbed
from wd_config import Config
from wd_mysql import MySqlOperations

class WowDiscord():
    def __init__(self):
        self.cf = Config()
        self.mysql = None

    def get_data_json(self,path):
        try:
            request = requests.get(path)
            request.raise_for_status()
            request_json = request.json()
        except requests.exceptions.RequestException as error:
            request_json = []
        return request_json

    def get_guild_news(self):
        path = 'https://eu.api.battle.net/wow/guild/%s/%s?fields=news&locale=%s&apikey=%s' % (
           self.cf.guild_realm, self.cf.guild_name, self.cf.local,self.cf.wow_api_key)
        request_json = self.get_data_json(path)

        for member in request_json['news']:
            yield member

    def get_guild_members(self):
        path = 'https://eu.api.battle.net/wow/guild/%s/%s?fields=members&locale=%s&apikey=%s'%(self.cf.guild_realm,self.cf.guild_name,self.cf.local,self.cf.wow_api_key)
        request_json = self.get_data_json(path)

        for member in request_json['members']:
            yield member

    def get_races(self):
        path = 'https://eu.api.battle.net/wow/data/character/races?locale=%s&apikey=%s'%(self.cf.local,self.cf.wow_api_key)
        request_json = self.get_data_json(path)

        for race in request_json['races']:
            yield race

    def get_classes(self):
        path = 'https://eu.api.battle.net/wow/data/character/classes?locale=%s&apikey=%s'%(self.cf.local,self.cf.wow_api_key)
        request_json = self.get_data_json(path)

        for w_class in request_json['classes']:
            yield w_class

    def get_item_description(self,item_id):
        descr = self.mysql.get_item_info(item_id)
        if descr == None:
            path = 'https://eu.api.battle.net/wow/item/%d?locale=%s&apikey=%s'%(item_id,self.cf.local,self.cf.wow_api_key)
            request_json = self.get_data_json(path)
            self.mysql.insert_item_info(**request_json)
            return self.get_item_description(item_id)
        else:
            return descr
    def get_avatar(self,character):
        field = self.mysql.get_member_avatar(character)
        path = 'https://render-eu.worldofwarcraft.com/character/'+field
        return path

    def get_member_info(self, character):
        return self.mysql.get_member_info(character)

    def get_item_image(self,item_id):
        return "https://render-eu.worldofwarcraft.com/icons/56/%s.jpg"%(self.get_item_description(item_id)[3])

    def get_item_url(self,item_id):
       return "http://eu.battle.net/wow/ru/item/"+str(item_id)

    def post_message(self,message, avatar = None, author = None, image = None, url = None):
        webhook = DiscordWebhook(self.cf.discord_webhook)
        embed = DiscordEmbed()
        embed.title = message
        embed.set_image(url = image)
        #embed.description = message
        embed.set_url(url)
        embed.color = 242424
        embed.set_author(name=author, url=None, icon_url=avatar)
        embed.set_footer(text='Отправлено:')
        embed.set_timestamp()

        # create embed object for webhook
        #embed = DiscordEmbed(title='Your Title', description='Lorem ipsum dolor sit', color=242424)

        # add embed object to webhook
        webhook.add_embed(embed)

        webhook.execute()
        

        #if image == None:
        #    msg = Webhook(self.cf.discord_webhook,msg = message)
        #    msg.post()
        #else:
        #    embed = Webhook(self.cf.discord_webhook, msg=message) # NOTE: the `msg` kwarg is a normal message.
            
            #embed.set_thumbnail(image)
        #    if url != None:
        #        embed.set_title(title=message, url=url)
        #    embed.set_image(image)
        #    embed.post()

        #embed.set_footer(text=str,icon=url,ts=True) # NOTE: You can input `True` (current time) or an int timestamp.

        #data = {"content":message,"embeds":[{"image":{"url": image }}]}
        #print( data)
    #requests.post(discord_webhook_url, data = data)

    def read_news(self):
        with MySqlOperations(self.cf) as mysql:
            self.mysql = mysql
            max_timestamp = mysql.get_maximum_timestamp()
            for news in self.get_guild_news():
                if news['timestamp'] > max_timestamp:
                    if news['type'] == 'itemLoot':
                        mysql.insert_item_loot(**news)
                    elif news['type'] == 'playerAchievement':
                        mysql.insert_player_achievement(**news)
                    elif news['type'] == 'guildAchievement':
                        mysql.insert_guild_achievement(**news)
                    else:
                        pass #Добавить код логирования неопознанных строк
            for news in mysql.get_unposted_news():
                try:
                    print(news)
                    #self.post_message(**news.get_news_string(self))
                except:
                    print('Ошибка отправки сообщения в Discord')
                else:
                    mysql.mark_posted(news)


#             pass
#news.mark_posted()
#       print(mysql.get_maximum_timestamp())
#    mysql.clear_table('races')
#    mysql.clear_table('classes')
#    for race in get_races(cf):

#        print(race)
#        mysql.insert_race_info(**race)
#    for w_class in get_classes(cf):
#        print(w_class)
#        mysql.insert_class_info(**w_class)
#    for member in get_guild_members(cf):
#        mysql.insert_member_info(**member)
#    mysql.clear_table('item_loot')
#    mysql.clear_table('guild_achievement')
#    mysql.clear_table('player_achievement')