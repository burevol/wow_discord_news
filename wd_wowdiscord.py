# -*- coding: utf-8 -*-

import traceback

from wd_config import Config
from wd_generators import WowData
from wd_messages import ItemLootMessage, GuildAchievementMessage, PlayerAchievementMessage
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import wd_alchemy

def get_data(cf,session):
    wow_data = WowData(cf)

    for news in wow_data.get_guild_news():
        if news['type'] == 'itemLoot':
            if not (session.query(wd_alchemy.CItemLoot).filter_by(character_name=news['character']).filter_by(
                    timestamp=news['timestamp']).first()):
                if not (session.query(wd_alchemy.CItem).filter_by(id=news['itemId']).first()):
                    newitem = wd_alchemy.CItem(**wow_data.get_item(news['itemId']))
                    session.add(newitem)
                if not (session.query(wd_alchemy.CMember).filter_by(name=news['character']).first()):
                    data_member = wow_data.get_character(news['character'])
                    newmember = wd_alchemy.CMember(**data_member, class_id=data_member['class'])
                    session.add(newmember)
                newloot = wd_alchemy.CItemLoot(**news)
                session.add(newloot)
        elif news['type'] == 'playerAchievement':
            if not (session.query(wd_alchemy.CMemberAchievement).filter_by(character_name=news['character']).filter_by(
                    timestamp=news['timestamp']).filter_by(achievement_id=news['achievement']['id']).first()):
                if not (session.query(wd_alchemy.CMember).filter_by(name=news['character']).first()):
                    data_member = wow_data.get_character(news['character'])
                    newmember = wd_alchemy.CMember(**data_member, class_id=data_member['class'])
                    session.add(newmember)
                new_achievement = wd_alchemy.CMemberAchievement(**news)
                session.add(new_achievement)
        elif news['type'] == 'guildAchievement':
            if not (session.query(wd_alchemy.CGuildAchievement).filter_by(character_name=news['character']).filter_by(
                    timestamp=news['timestamp']).filter_by(achievement_id=news['achievement']['id']).first()):
                if not (session.query(wd_alchemy.CMember).filter_by(name=news['character']).first()):
                    data_member = wow_data.get_character(news['character'])
                    newmember = wd_alchemy.CMember(**data_member, class_id=data_member['class'])
                    session.add(newmember)
                new_achievement = wd_alchemy.CGuildAchievement(**news)
                session.add(new_achievement)
    session.commit()


def process_news(cf_name):
    cf = Config(cf_name)

    db_engine = create_engine('mysql://%s:%s@%s/%s?charset=utf8'%(cf.dbuser,cf.dbpasswd,cf.dbhost,cf.db))

    Session = sessionmaker(bind=db_engine)
    session = Session()

    get_data(cf, session)

    item_news = session.query(wd_alchemy.CItemLoot).filter_by(posted = 0).all()
    for news in item_news:
        post = ItemLootMessage(cf, news)
        try:
            post.post_message()
        except:
            print('Ошибка отправки сообщения в Discord', traceback.format_exc())
        else:
            news.posted = 1

    player_news = session.query(wd_alchemy.CMemberAchievement).filter_by(posted = 0).all()
    for news in player_news:
        post = PlayerAchievementMessage(cf, news)
        try:
            post.post_message()
        except:
            print('Ошибка отправки сообщения в Discord', traceback.format_exc())
        else:
            news.posted = 1

    guild_news = session.query(wd_alchemy.CGuildAchievement).filter_by(posted = 0).all()
    for news in guild_news:
        post = GuildAchievementMessage(cf, news)
        try:
            post.post_message()
        except:
            print('Ошибка отправки сообщения в Discord', traceback.format_exc())
        else:
            news.posted = 1

    session.commit()
    session.close()
