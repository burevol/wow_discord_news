# -*- coding: utf-8 -*-

import traceback

from wd_config import Config
from wd_generators import WowData
from wd_messages import ItemLootMessage, GuildAchievementMessage, PlayerAchievementMessage
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import wd_alchemy


class MainClass(object):
    def __init__(self, cf_name):
        self.cf = Config(cf_name)
        self.wow_data = WowData(self.cf)
        db_engine = create_engine(
            'mysql://%s:%s@%s/%s?charset=utf8' % (self.cf.dbuser, self.cf.dbpasswd, self.cf.dbhost, self.cf.db))
        Session = sessionmaker(bind=db_engine)
        self.session = Session()

    def add_item_loot(self,news):
        if not (self.session.query(wd_alchemy.CItemLoot).filter_by(character_name=news['character']).filter_by(
                timestamp=news['timestamp']).first()):
            if not (self.session.query(wd_alchemy.CItem).filter_by(id=news['itemId']).first()):
                newitem = wd_alchemy.CItem(**self.wow_data.get_item(news['itemId']))
                self.session.add(newitem)
            if not (self.session.query(wd_alchemy.CMember).filter_by(name=news['character']).first()):
                data_member = self.wow_data.get_character(news['character'])
                newmember = wd_alchemy.CMember(**data_member, class_id=data_member['class'])
                self.session.add(newmember)
            newloot = wd_alchemy.CItemLoot(**news)
            self.session.add(newloot)

    def add_guild_achievement(self,news):
        if not (
                self.session.query(wd_alchemy.CMemberAchievement).filter_by(character_name=news['character']).filter_by(
                    timestamp=news['timestamp']).filter_by(achievement_id=news['achievement']['id']).first()):
            if not (self.session.query(wd_alchemy.CMember).filter_by(name=news['character']).first()):
                data_member = self.wow_data.get_character(news['character'])
                newmember = wd_alchemy.CMember(**data_member, class_id=data_member['class'])
                self.session.add(newmember)
            new_achievement = wd_alchemy.CMemberAchievement(**news)
            self.session.add(new_achievement)
    def add_player_achievement(self,news):
        if not (
                self.session.query(wd_alchemy.CGuildAchievement).filter_by(character_name=news['character']).filter_by(
                    timestamp=news['timestamp']).filter_by(achievement_id=news['achievement']['id']).first()):
            if not (self.session.query(wd_alchemy.CMember).filter_by(name=news['character']).first()):
                data_member = self.wow_data.get_character(news['character'])
                newmember = wd_alchemy.CMember(**data_member, class_id=data_member['class'])
                self.session.add(newmember)
            new_achievement = wd_alchemy.CGuildAchievement(**news)
            self.session.add(new_achievement)

    def get_data(self):

        for news in self.wow_data.get_guild_news():
            if news['type'] == 'itemLoot':
                self.add_item_loot(news)
            elif news['type'] == 'playerAchievement':
                self.add_guild_achievement(news)
            elif news['type'] == 'guildAchievement':
                self.add_player_achievement(news)
        self.session.commit()

    def process_news(self):

        self.get_data()

        item_news = self.session.query(wd_alchemy.CItemLoot).filter_by(posted=0).all()
        for news in item_news:
            post = ItemLootMessage(self.cf, news)
            try:
                post.post_message()
            except:
                print('Ошибка отправки сообщения в Discord', traceback.format_exc())
            else:
                news.posted = 1

        player_news = self.session.query(wd_alchemy.CMemberAchievement).filter_by(posted=0).all()
        for news in player_news:
            post = PlayerAchievementMessage(self.cf, news)
            try:
                post.post_message()
            except:
                print('Ошибка отправки сообщения в Discord', traceback.format_exc())
            else:
                news.posted = 1

        guild_news = self.session.query(wd_alchemy.CGuildAchievement).filter_by(posted=0).all()
        for news in guild_news:
            post = GuildAchievementMessage(self.cf, news)
            try:
                post.post_message()
            except:
                print('Ошибка отправки сообщения в Discord', traceback.format_exc())
            else:
                news.posted = 1

        self.session.commit()
        self.session.close()
