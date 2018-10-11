from wd_mysql import MySqlOperations
from wd_mysqlobjects import MysqlObjects

class Classes(MysqlObjects):
     def __init(self,mysql):
        super().__init__(mysql)
     def clear_table(self):
        super().clear_table('classes')
     def __len__(self):
        sql = 'SELECT COUNT(*) FROM classes'
        return self.mysql.execute_query(sql,())[0]
     def __getitem__(self,id):
        if type(id) is int:
            sql = "SELECT * FROM classes WHERE class_id = %s"
            result = self.mysql.execute_query(sql,(id,))
            if result:
                return {'id':result[0],'mask':result[1],'powerType':result[2],'name':result[3]}
            else:
                raise IndexError
        elif type(id) is str:
            sql = "SELECT * FROM classes WHERE name = %s"
            result = self.mysql.execute_query(sql,(id,))
            if result:
                return {'id':result[0],'mask':result[1],'powerType':result[2],'name':result[3]}
            else:
                raise KeyError
        else:
            raise TypeError

     def __setitem__(self,id,data):
        if type(id) is int:
            try:
                self.__getitem__(id)
            except IndexError:
                sql = 'INSERT INTO classes(class_id,mask,powerType,name) VALUES (%s,%s,%s,%s)'
                self.mysql.update_query(sql,(id,data['mask'],data['powerType'],data['name']))
            except TypeError:
                raise TypeError
            else:
                sql = 'UPDATE classes SET mask = %s, powerType = %s, name = %s WHERE class_id = %s'
                self.mysql.update_query(sql,(data['mask'],data['powerType'],data['name'],data['id']))
        elif type(id) is str:
            try:
                self.__getitem__(id)
            except KeyError:
                sql = 'INSERT INTO classes(class_id,mask,powerType,name) VALUES (%s,%s,%s,%s)'
                sql.mysql.update_query(sql,id,data['mask'],data['powerType'],data['name'])
            except TypeError:
                raise TypeError
            else:
                sql = 'UPDATE classes SET class_id = %s, mask = %s, powerType = %s WHERE name = %s'
                self.mysql.update_query(sql,(data['id'],data['mask'],data['powerType'],data['name'],data['name']))
        else:
            print('неверное значение id')
            raise TypeError



