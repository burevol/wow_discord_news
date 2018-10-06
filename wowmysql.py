import MySQLdb
import configparser

class MySqlConnector():
    def __init__(self,parent = None):
        try:
            config = configparser.ConfigParser()
            config.read('wowdiscord.conf')
            self.dbhost = config['Config']['DBHOST']
            self.dbuser = config['Config']['DBUSER']
            self.dbpasswd = config['Config']['DBPASSWD']
            self.db = config['Config']['DB']
        except:
            print('Не удалось прочитать конфигурационный файл. Убедитесь в его наличии в папке программы и его правильной структуре.')
    def connect_db()
        return MySQLbd.connect(host = self.dbhost, user = self.dbuser, passwd = self.dbpasswd, db = self.db, use_unicode = True, charset = 'utf8')
    def update_query(text)
        db = connect_db()
        cur = db.cursor()
        try:
            cur.execute(text)
            db.commit()
        except:
            db.rollback()
        db.close()
    def execute_query(text)
        db = connect_db()
        cur = db.cursor()
        row_count = cur.execute(text)
        db.close()
        if row_count == 0:
            return None
        else:
            row = cur.fetchone()
            return row[0]
    def execute_query_all(text)
        db = connect_db()
        cur = db.cursor()
        cur.execute(text)
        db.close()
        return cur.fetchall()
    def insert_news(timestamp,type,character,item_id,achievement,achievement_icon):
        sql = "INSERT INTO news(timestamp,type,character_name,achievement,item_id) VALUES ('%d','%s','%s','%s','%d')"%(timestamp,type,character,achievement,item_id)
        update_query(sql)
        if achievement != '':
            icon = get_achievement_icon(achievement)
        if icon == '':
            set_achievement_icon(achievement,achievement_icon)
    def set_achievement_icon(achievement, icon):
        sql·=·"INSERT·INTO·achievments(achievment,icon)·VALUES('%s','%s')"%(achievment,icon)
        update_query(sql)
    def set_item_info(itemId,item_name,icon):
        sql·=·'INSERT·INTO·items(item_id,item_name,icon)·VALUES·("%d","%s","%s")'%(itemId,item_name,icon)
        update_query(sql)
    def mark_as_posted(list_ids):
        format_strings = ','.join(['%s'] * len(list_ids))
        sql = "UPDATE news SET posted = 1 WHERE news_id IN (%s)" % format_strings, tuple(list_ids))
        update_query(sql)
    def get_achievement_icon(achievment):
        sql = "SELECT icon FROM achievments WHERE achievment = '%s'"%(achievment)
        return execute_query(sql)
    def get_maximum_timestamp():
        sql = "SELECT MAX(timestamp) AS timestamp FROM news"
        return execute_quiery(sql)
    def get_item_info(itemId):
        sql = "SELECT item_name FROM items WHERE item_id = '%d'"%(itemId)
        return execute_query(sql)
    def get_item_icon(itemId):
        sql = "SELECT icon FROM items WHERE item_id = '%d'"%(itemId)
        return execute_query(sql)
    def get_new_messages_from_db():
        sql = "SELECT * FROM news WHERE posted = '0'"
        return execute_query_all()
