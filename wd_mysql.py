from wd_config import Config
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
    def update_query(self,text):
        cur = self.connect.cursor()
        try:
            cur.execute(text)
            self.connect.commit()
        except:
            print(sys.exc_info())
            self.connect.rollback()
    def clear_table(self,table_name):
        sql = 'TRUNCATE TABLE %s'%(table_name)
        self.update_query(sql)
    def insert_race_info(self,id,mask,side,name):
        sql = 'INSERT INTO races(race_id,mask,side,name) VALUES ("%d","%d","%s","%s")'%(id,mask,side,name)
        self.update_query(sql)
    def insert_class_info(self,id,mask,powerType,name):
        sql = 'INSERT INTO classes(class_id,mask,powerType,name) VALUES ("%d","%d","%s","%s")'%(id,mask,powerType,name)
        self.update_query(sql)
    def insert_member_info(self,character,rank):
        sql = 'INSERT INTO guild_members(name,realm,class,race,gender,level,achievementPoints,thumbnail,rank,published,isMember)\
            VALUES ("%s","%s","%d","%d","%d","%d","%d","%s","%d","%d","%d")'%(character['name'],character['realm'],character['class'],character['race'],\
            character['gender'],character['level'],character['achievementPoints'],character['thumbnail'],rank,0,1)
        print(sql)
        self.update_query(sql)
    def insert_item_loot(self,type,character,timestamp,itemId,context,**other):
        sql = 'INSERT INTO item_loot(type,character_name,timestamp,itemId,context,posted) VALUES ("%s","%s","%d","%d","%s","%d")'%(type,character,timestamp,itemId,context,0)
        self.update_query(sql)

    def insert_guild_achievement(self,type,character,timestamp,context,achievement,**other):
        sql = 'INSERT INTO guild_achievement(character_name,timestamp,context,achievement_id,title,description,icon,posted)\
           VALUES ("%s","%d","%s","%d","%s","%s","%s","%d")'%(character,timestamp,context,achievement['id'],achievement['title'],
           achievement['description'],achievement['icon'],0)
        self.update_query(sql)

    def insert_player_achievement(self,type,character,timestamp,context,achievement,**other):
        sql = 'INSERT INTO player_achievement(character_name,timestamp,context,achievement_id,title,description,icon,posted)\
           VALUES ("%s","%d","%s","%d","%s","%s","%s","%d")'%(character,timestamp,context,achievement['id'],achievement['title'],
           achievement['description'],achievement['icon'],0)
        self.update_query(sql)

    def mark_as_posted(self,list_ids):
        format_strings = ','.join(['%s'] * len(list_ids))
        sql = "UPDATE news SET posted = 1 WHERE news_id IN (%s)" % (format_strings, tuple(list_ids))
        self.update_query(sql)
    
