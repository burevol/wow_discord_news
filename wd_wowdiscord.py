import traceback
import requests

from wd_config import Config
from wd_mysql import MySqlOperations

from wd_mysqlobjects_items import Items
from wd_mysqlobjects_members import Members
from wd_mysqlobjects_races import Races
from wd_mysqlobjects_classes import Classes

class WowDiscord():
    def __init__(self,configfile = None):
        if configfile != None:
            self.cf = Config(configfile)
        else:
            self.cf = Config()
        self.mysql = None

    def get_data_json(self,path):
        try:
            request = requests.get(path)
            request.raise_for_status()
            request_json = request.json()
        except requests.exceptions.RequestException as error:
            print('Ошибка получения данных json') 
            request_json = []
        return request_json

    def get_guild_news(self):
        path = 'https://eu.api.battle.net/wow/guild/%s/%s?fields=news&locale=%s&apikey=%s' % (
           self.cf.guild_realm, self.cf.guild_name, self.cf.local,self.cf.wow_api_key)
        request_json = self.get_data_json(path)

        for member in request_json['news']:
            yield member

    def get_guild_members(self):
        '''Функция-генератор, возвращающая персонажей гильдии'''
        path = 'https://eu.api.battle.net/wow/guild/%s/%s?fields=members&locale=%s&apikey=%s'%(self.cf.guild_realm,self.cf.guild_name,self.cf.local,self.cf.wow_api_key)
        request_json = self.get_data_json(path)

        for member in request_json['members']:
            yield member

    def get_races(self):
        '''Функция-генератор, возвращающая расы персонажей'''
        path = 'https://eu.api.battle.net/wow/data/character/races?locale=%s&apikey=%s'%(self.cf.local,self.cf.wow_api_key)
        request_json = self.get_data_json(path)

        for race in request_json['races']:
            yield race

    def get_classes(self):
        '''Функция - генератор, возвращающая классы персонажей'''
        path = 'https://eu.api.battle.net/wow/data/character/classes?locale=%s&apikey=%s'%(self.cf.local,self.cf.wow_api_key)
        request_json = self.get_data_json(path)

        for w_class in request_json['classes']:
            yield w_class

   # def get_item_description(self,item_id):
   #     items = Items(self.mysql)
   #     try:
   #        item = items[item_id]
   #     except IndexError:
   #         path = 'https://eu.api.battle.net/wow/item/%d?locale=%s&apikey=%s'%(item_id,self.cf.local,self.cf.wow_api_key)
   #         request_json = self.get_data_json(path)
   #         items[item_id] = request_json
   #         return items[item_id]
   #     else:
   #        return item

    def get_avatar(self,character):
        '''Возвращает ссылку на аватар персонажа'''
        try:
            field = self.members[character]['thumbnail']
        except KeyError:
             return None
        else:
             return  'https://render-eu.worldofwarcraft.com/character/'+field

    def get_member_info(self, character):
        '''Возвращает словарь с данными персонажа'''
        return self.members[character]

    

    

    def update_guild_members(self):
        self.mysql.reset_guild_flag()
        for member in self.get_guild_members():
            self.members[member['character']['name']] = member
        self.mysql.check_guild_members()

    def read_news(self):
        
        with MySqlOperations(self.cf) as mysql:
            self.mysql = mysql
            news_types = {'itemLoot':mysql.insert_item_loot,'playerAchievement':
              mysql.insert_player_achievement,'guildAchievement':
              mysql.insert_guild_achievement}
            self.items = Items(mysql)
            self.members = Members(mysql)

            self.update_guild_members()

            max_timestamp = mysql.get_maximum_timestamp()
            if max_timestamp == None:
                max_timestamp = 0;
            for news in self.get_guild_news():
                if news['timestamp'] > max_timestamp:
                    try:
                        news_types[news['type']](**news)
                    except KeyError:
                        pass #Добавить код логирования неопознанных строк

                    #if news['type'] == 'itemLoot':
                    #    mysql.insert_item_loot(**news)
                    #elif news['type'] == 'playerAchievement':
                    #    mysql.insert_player_achievement(**news)
                    #elif news['type'] == 'guildAchievement':
                    #    mysql.insert_guild_achievement(**news)
                    #else:
                    #    pass #Добавить код логирования неопознанных строк
            for news in mysql.get_unposted_news():
                try:
                    #print(news.get_news_string(self))
                    #self.post_message(**news.get_news_string(self))
                    news.post_message()
                except:
                    print('Ошибка отправки сообщения в Discord',traceback.format_exc())
                else:
                    mysql.mark_posted(news)
