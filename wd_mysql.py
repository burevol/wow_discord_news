import traceback
from wd_config import Config
from wd_messages import NewsMessages,ItemLootMessage,GuildAchievementMessage,PlayerAchievementMessage,GuildInviteMessage

import MySQLdb
import sys

class MySqlOperations():
    def __init__(self,config):
        self.dbhost = config.dbhost
        self.dbuser = config.dbuser
        self.dbpasswd = config.dbpasswd
        self.db = config.db
        self.connect =  MySQLdb.connect(host = self.dbhost, user = self.dbuser, passwd = self.dbpasswd, db = self.db, use_unicode = True, charset = 'utf8')
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        print('Connection to MySql closed!')
        self.connect.close()
    def update_query(self,text,params = None):
        cur = self.connect.cursor()
        try:
            cur.execute(text,params)
            self.connect.commit()
        except:
            print("Ошибка выполнения запроса на запись",text,params,traceback.format_exc())
            self.connect.rollback()
    def execute_query(self,text,params):
        try:
            cur = self.connect.cursor()
            row_count = cur.execute(text,params)
        except:
            print("Ошибка выполнения запроса на чтение",text,params,traceback.format_exc())
        if row_count == 0:
            return None
        else:
            return cur.fetchone()
    def execute_query_all(self,text):
        cur = self.connect.cursor()
        cur.execute(text)
        return cur.fetchall()

##    def clear_table(self,table_name):
##        sql = 'TRUNCATE TABLE %s'
##        self.update_query(sql,(table_name,))
##    def insert_race_info(self,id,mask,side,name):
##        sql = 'INSERT INTO races(race_id,mask,side,name) VALUES (%d,%d,%s,%s)'
##        self.update_query(sql,(id,mask,side,name))
##    def insert_class_info(self,id,mask,powerType,name):
##        sql = 'INSERT INTO classes(class_id,mask,powerType,name) VALUES (%d,%d,%s,%s)'
##        self.update_query(sql,(id,mask,powerType,name))
##    def insert_member_info(self,character,rank):
##        sql = 'SELECT * FROM guild_members WHERE (name = %s) AND (realm = %s)'
##        seek = self.execute_query(sql,(character['name'],character['realm']))
##        if seek == None:
##            sql = 'INSERT INTO guild_members(name,realm,class,race,gender,level,achievementPoints,thumbnail,rank,posted,isMember,is_check)\
##                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
##            self.update_query(sql,(character['name'],character['realm'],character['class'],\
##                character['race'],character['gender'],character['level'],character['achievementPoints'],character['thumbnail'],\
##                rank,0,1,1) )
##        else:
##            sql = 'UPDATE guild_members SET isMember = "1" WHERE member_id = %s'
##            self.update_query(sql, (seek[0],)) 
##            sql = 'UPDATE guild_members SET is_check = "1" WHERE member_id = %s'
##            self.update_query(sql, (seek[0],))

##    def get_member_avatar(self,character):
##        sql = 'SELECT thumbnail FROM guild_members WHERE name = %s'
##        avatar =  self.execute_query(sql,(character,))
##        if avatar == None:
##            return None
##        else:
##            return avatar[0] 
##
##    def get_member_info(self,character):
##        sql = 'SELECT * FROM guild_members WHERE name = %s'
##        return self.execute_query(sql,(character,))

    def insert_item_loot(self,type,character,timestamp,itemId,context,**other):
        sql = 'INSERT INTO item_loot(type,character_name,timestamp,itemId,context,posted) VALUES (%s,%s,%s,%s,%s,%s)'
        self.update_query(sql, (type,character,timestamp,itemId,context,0))

    def insert_guild_achievement(self,type,character,timestamp,context,achievement,**other):
        sql = 'INSERT INTO guild_achievement(character_name,timestamp,context,achievement_id,title,description,icon,posted)\
           VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'
        self.update_query(sql,(character,timestamp,context,achievement['id'],achievement['title'],
           achievement['description'],achievement['icon'],0) )

    def insert_player_achievement(self,type,character,timestamp,context,achievement,**other):
        sql = 'INSERT INTO player_achievement(character_name,timestamp,context,achievement_id,title,description,icon,posted)\
           VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'
        self.update_query(sql, (character,timestamp,context,achievement['id'],achievement['title'],
           achievement['description'],achievement['icon'],0))

##    def insert_item_info(self,id,description,name,icon,itemLevel,**other):
##        sql = 'INSERT INTO items2(id,description,name,icon,itemLevel) VALUES (%s,%s,%s,%s,%s)'
##        self.update_query(sql, (id,description,name,icon,itemLevel))
##
##    def get_item_info(self,item_id):
##        sql = "SELECT * FROM items2 WHERE id = %s"
##        result = self.execute_query(sql,(item_id,))
##        return result

    def get_maximum_timestamp(self):
        sql = 'SELECT MAX(timestamp) AS timestamp FROM   (SELECT MAX(timestamp) AS timestamp FROM item_loot UNION SELECT \
                MAX(timestamp) FROM guild_achievement UNION SELECT MAX(timestamp) FROM player_achievement) AS t'
        return self.execute_query(sql,())[0] 

#    def mark_as_posted(self,list_ids):
#        format_strings = ','.join(['%s'] * len(list_ids))
#        sql = "UPDATE news SET posted = 1 WHERE news_id IN (%s)" % (format_strings, tuple(list_ids))
#        self.update_query(sql)
    def mark_posted(self,news):
        sql = news.get_mark_query()
        self.update_query(sql)

    #def mark_posted_item_loot(self,id):
    #    sql = 'UPDATE item_loot SET posted = 1 WHERE id = "%d"' % (id)
    #    self.update_query(sql)
    #def mark_posted_guild_achievement(self,id):
    #    sql = 'UPDATE guild_achievement SET posted = 1 WHERE id = "%d"' % (id)
    #    self.update_query(sql)
    #def mark_posted_player_achievement(self,id):
    #    sql = 'UPDATE player_achievement SET posted = 1 WHERE id = "%d"' % (id)
    #    self.update_query(sql)
    def get_unposted_news(self):
        sql = "SELECT * FROM item_loot WHERE posted = '0'"
        rows = self.execute_query_all(sql)
        newslist = []
        for row in rows:
            newslist.append(ItemLootMessage(row))
        sql = "SELECT * FROM player_achievement WHERE posted = '0'"
        rows = self.execute_query_all(sql)
        for row in rows:
            newslist.append(PlayerAchievementMessage(row))
        sql = "SELECT * FROM guild_achievement WHERE posted = '0'"
        rows = self.execute_query_all(sql)
        for row in rows:
            newslist.append(GuildAchievementMessage(row))
        sql = 'SELECT * FROM guild_members WHERE posted = "0"'
        rows = self.execute_query_all(sql)
        for row in rows:
            newslist.append(GuildInviteMessage(row))
        return newslist

    def reset_guild_flag(self):
        sql = 'UPDATE guild_members SET is_check = "0"'
        self.update_query(sql)

    def check_guild_members(self):
        sql = 'SELECT * FROM guild_members WHERE (is_check = "0") and (isMember = "1")'
        rows = self.execute_query_all(sql)
        for row in rows:
            sql = 'UPDATE guild_members SET posted = "0" WHERE member_id = %s'
            self.update_query(sql,(row[0],))
            sql = 'UPDATE guild_members SET isMember = "0" WHERE member_id = %s'
            self.update_query(sql,(row[0],))
