import traceback
from webhook import DiscordWebhook, DiscordEmbed

class NewsMessages():
    def get_item_image(self,item_id):
        '''Возвращает URL изображения предмета'''
        return "https://render-eu.worldofwarcraft.com/icons/56/%s.jpg"%(self.items[item_id]['id'])

    def get_item_url(self,item_id):
        '''Возвращает URL описания предмета'''
        return "http://eu.battle.net/wow/ru/item/"+str(item_id) 

    def post_message(self, message, avatar = None, author = None, image = None, url = None):
        '''Отправляет сообщение в Discord'''
        webhook = DiscordWebhook(self.cf.discord_webhook)
        embed = DiscordEmbed()
        embed.title = message
        embed.set_image(url = image)
        embed.set_url(url)
        embed.color = 242424
        embed.set_author(name=author, url=None, icon_url=avatar)
        embed.set_footer(text='Отправлено:')
        embed.set_timestamp()
        webhook.add_embed(embed)

        webhook.execute() 

class ItemLootMessage(NewsMessages):
    def __init__(self, datalist):
        self.id = datalist[0]
        self.type = datalist[1]
        self.character_name = datalist[2]
        self.timestamp = datalist[3]
        self.itemId = datalist[4]
        self.context = datalist[5]
        self.posted = datalist[6]
    def __str__(self):
        return '%s получил %d'%(self.character_name,self.itemId)
    def post_message(self):
        try:
            gender = wdobject.get_member_info(self.character_name)['gender']
            avatar = wdobject.get_avatar(self.character_name)
        except KeyError:
            gender = 0
            avatar = None

        if gender == 0:
            message = '%s получил %s'%(self.character_name,wdobject.get_item_description(self.itemId)['name'])
        else:
            message = '%s получила %s'%(self.character_name,wdobject.get_item_description(self.itemId)['name'])
        image = self.get_item_image(self.itemId)
        url = self.get_item_url(self.itemId)
        answer= {"author":self.character_name,"message":message,"avatar":avatar,"image":image,"url":url}
        super().post_message(**answer)
    def get_mark_query(self):
        return 'UPDATE item_loot SET posted = 1 WHERE id = "%d"' % (self.id)

class PlayerAchievementMessage(NewsMessages):
    def __init__(self,datalist):
        self.id = datalist[0]
        self.character_name = datalist[1]
        self.timestamp = datalist[2]
        self.context = datalist[3]
        self.achievement_id = datalist[4]
        self.title = datalist[5]
        self.description = datalist[6]
        self.icon = datalist[7]
        self.posted = datalist[8]
    def __str__(self):
        return '%s заслужил достижение %s'%(self.character_name,self.title)
    def post_message(self):
        try:
            avatar = wdobject.get_avatar(self.character_name)
        except KeyError:
            avatar = None
        message = '%s заслужил достижение %s'%(self.character_name,self.title)
        answer= {"message":message,"avatar":avatar,'image':avatar}
        super().post_message(**answer)
    def get_mark_query(self):
        return 'UPDATE player_achievement SET posted = 1 WHERE id = "%d"' % (self.id)

class GuildAchievementMessage(NewsMessages):
    def __init__(self,datalist):
        self.id = datalist[0]
        self.character_name = datalist[1]
        self.timestamp = datalist[2]
        self.context = datalist[3]
        self.achievement_id = datalist[4]
        self.title = datalist[5]
        self.description = datalist[6]
        self.icon = datalist[7]
        self.posted = datalist[8]
    def __str__(self):
        print(self.character_name,self.title) 
        return 'Гильдия заслужила достижение %s'%(self.title)
    def post_message(self):
        try:
             avatar = wdobject.get_avatar(self.character_name)
        except KeyError:
             avatar = None 
        message = 'Гильдия заслужила достижение %s'%(self.title)
        answer= {"message":message,"avatar":avatar}
        super().post_message(**answer)
    def get_mark_query(self):
        return  'UPDATE guild_achievement SET posted = 1 WHERE id = "%d"' % (self.id)
class GuildInviteMessage(NewsMessages):
    def __init__(self,datalist):
        self.id = datalist[0]
        self.character_name = datalist[1]
        self.gender = datalist[5]
        self.isMember = datalist[11]
    def __str__(self):
        if self.isMember == 1:
            if self.gender == 0:
                return "%s присоединился к гильдии"%(self.character_name)
            else:
                return '%s присоединилась к гильдии'%(self.character_name)
        else:
            if self.gender == 0:
                return "%s покинул гильдию"%(self.character_name)
            else:
                return '%s покинула гильдию'%(self.character_name)
    def get_news_string(self,wdobject):
        try:
            avatar = wdobject.get_avatar(self.character_name)
        except KeyError:
            avatar = None
        if self.isMember == 1:
            if self.gender == 0:
                message = "%s присоединился к гильдии"%(self.character_name)
            else:
                message =  '%s присоединилась к гильдии'%(self.character_name)
        else:
            if self.gender == 0:
                message =  "%s покинул гильдию"%(self.character_name)
            else:
                message =  '%s покинула гильдию'%(self.character_name)
        answer = {'message':message,'avatar':avatar,'image':avatar}
        return answer
    def get_mark_query(self):
        return 'UPDATE guild_members  SET posted = 1 WHERE member_id = "%d"' % (self.id)


