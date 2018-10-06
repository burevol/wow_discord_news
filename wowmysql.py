import MySQLdb

DBHOST =  '192.168.88.4'
DBUSER = 'wow_api'
DBPASSWD =  '^6N9AodseNl|*7ulqCI6'
DB =  'wow_database'


def insert_news(timestamp,type,character,item_id,achievement,achievement_icon):
    db = MySQLdb.connect(host = DBHOST,
                     user = DBUSER,
                     passwd = DBPASSWD,
                     db = DB, use_unicode=True, charset="utf8")

    cur = db.cursor()

    sql = "INSERT INTO news(timestamp,type,character_name,achievement,item_id) VALUES ('%d','%s','%s','%s','%d')"%(timestamp,type,character,achievement,item_id)
    try:
        cur.execute(sql)
        db.commit()
    except:
        db.rollback()

    db.close()
    if achievement != '':
        icon = get_achievement_icon(achievement)
        if icon == '':
            set_achievement_icon(achievement,achievement_icon)

def get_achievement_icon(achievment):
    db = MySQLdb.connect(host = DBHOST,
                     user = DBUSER,
                     passwd = DBPASSWD,
                     db = DB, use_unicode=True, charset="utf8")
    cur = db.cursor()
    sql = "SELECT icon FROM achievments WHERE achievment = '%s'"%(achievment)
    row_count = cur.execute(sql)
    db.close()
    if row_count == 0:
        return ''
    else:
        row = cur.fetchone()
        return row[0]

def set_achievement_icon(achievment, icon):
    db = MySQLdb.connect(host = DBHOST,
                     user = DBUSER,
                     passwd = DBPASSWD,
                     db = DB, use_unicode=True, charset="utf8")
    cur = db.cursor()
    sql = "INSERT INTO achievments(achievment,icon) VALUES('%s','%s')"%(achievment,icon)
    try:
        cur.execute(sql)
        db.commit()
    except:
        db.rollback()
    db.close()



def get_maximum_timestamp():
    db = MySQLdb.connect(host = DBHOST,
                     user = DBUSER,
                     passwd = DBPASSWD,
                     db = DB)

    cur = db.cursor()
    sql = "SELECT MAX(timestamp) AS timestamp FROM news"
    row_count = cur.execute(sql)
    row = cur.fetchone()
    db.close()
    if row[0] == None:
        return 0
    else:
        return row[0]

def set_item_info(itemId,item_name,icon):
    db = MySQLdb.connect(host = DBHOST,
                     user = DBUSER,
                     passwd = DBPASSWD,
                     db = DB, use_unicode=True, charset="utf8")
    cur = db.cursor()
    print (item_name)
    sql = 'INSERT INTO items(item_id,item_name,icon) VALUES ("%d","%s","%s")'%(itemId,item_name,icon)
    try:
        cur.execute(sql)
        db.commit()
    except:
        db.rollback()
    db.close()

def get_item_info(itemId):
    db = MySQLdb.connect(host = DBHOST,
                     user = DBUSER,
                     passwd = DBPASSWD,
                     db = DB, use_unicode=True, charset="utf8")


    sql = "SELECT item_name FROM items WHERE item_id = '%d'"%(itemId)
    cur = db.cursor()
    row_count = cur.execute(sql)
    row = cur.fetchone()
    db.close()
    if row_count == 0:
        return ''
    else:
        return row[0]


def get_item_icon(itemId):
    db = MySQLdb.connect(host = DBHOST,
                     user = DBUSER,
                     passwd = DBPASSWD,
                     db = DB, use_unicode=True, charset="utf8")


    sql = "SELECT icon FROM items WHERE item_id = '%d'"%(itemId)
    cur = db.cursor()
    row_count = cur.execute(sql)
    row = cur.fetchone()
    db.close()
    if row_count == 0:
        return ''
    else:
        return row[0]


def get_new_messages_from_db():
    db = MySQLdb.connect(host = DBHOST,
                     user = DBUSER,
                     passwd = DBPASSWD,
                     db = DB, use_unicode=True, charset="utf8")
    sql = "SELECT * FROM news WHERE posted = '0'"
    cur =db.cursor()
    cur.execute(sql)
    db.close()
    return cur.fetchall()

def mark_as_posted(list_ids):
    db = MySQLdb.connect(host = DBHOST,
                     user = DBUSER,
                     passwd = DBPASSWD,
                     db = DB, use_unicode=True, charset="utf8")

    format_strings = ','.join(['%s'] * len(list_ids))
    cur =db.cursor()
    cur.execute("UPDATE news SET posted = 1 WHERE news_id IN (%s)" % format_strings,
                tuple(list_ids))
    db.commit()
    db.close()

#get_maximum_timestamp()

#insert_news(12312331,'obtain',12345,54412)
