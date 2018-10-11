from wd_mysql import MySqlOperations

class MysqlObjects():
    def __init__(self,mysql):
        self.mysql = mysql
    def clear_table(self,table_name):
        sql = 'TRUNCATE TABLE %s'%(table_name)
        self.mysql.update_query(sql,())

