import traceback
import requests

from wd_config import Config
from wd_mysql import MySqlOperations
from json_generators import JSON_Generators

from wd_mysqlobjects_items import Items
from wd_mysqlobjects_members import Members
from wd_mysqlobjects_races import Races
from wd_mysqlobjects_classes import Classes


class WowDiscord():
    def __init__(self, configfile=None):
        if configfile != None:
            self.cf = Config(configfile)
        else:
            self.cf = Config()
        self.mysql = None
        self.json = JSON_Generators(self.cf)

    def update_guild_members(self):
        self.mysql.reset_guild_flag()
        for member in self.json.get_guild_members():
            self.members[member['character']['name']] = member
        self.mysql.check_guild_members()
    def get_guild_news(self):

    def read_news(self):

        with MySqlOperations(self.cf) as mysql:
            self.mysql = mysql
            news_types = {'itemLoot': mysql.insert_item_loot, 'playerAchievement':
                mysql.insert_player_achievement, 'guildAchievement':
                              mysql.insert_guild_achievement}
            self.items = Items(mysql)
            self.members = Members(mysql)

            self.update_guild_members()

            max_timestamp = mysql.get_maximum_timestamp()
            if max_timestamp == None:
                max_timestamp = 0;
            for news in self.json.get_guild_news():
                if news['timestamp'] > max_timestamp:
                    try:
                        news_types[news['type']](**news)
                    except KeyError:
                        pass #Добавить код логирования неопознанных строк
                    if news['type'] == 'itemLoot':
                        item = self.get_item_description(news['itemId'])

            for news in mysql.get_unposted_news():
                try:
                    #print(news.get_news_string(self))
                    #self.post_message(**news.get_news_string(self))
                    news.post_message()
                except:
                    print('Ошибка отправки сообщения в Discord',traceback.format_exc())
                else:
                    mysql.mark_posted(news)
