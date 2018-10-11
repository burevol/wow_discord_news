from wd_mysql import MySqlOperations
from wd_mysqlobjects import MysqlObjects

class Items(MysqlObjects):
     def __init(self,mysql):
        super().__init__(mysql)
     def clear_table(self):
        super().clear_table('items2')
     def get_dict_from_result(self,result):
        return {'id':result[0],'description':result[1],'name':result[2],'icon':result[3],'itemLevel':result[4]}
     def __len__(self):
        sql = 'SELECT COUNT(*) FROM items2'
        return self.mysql.execute_query(sql,())[0]
     def __getitem__(self,id):
        if type(id) is int:
            sql = "SELECT * FROM items2 WHERE id = %s"
            result = self.mysql.execute_query(sql,(id,))
            if result:
                return self.get_dict_from_result(result)
            else:
                raise IndexError
        elif type(id) is str:
            sql = "SELECT * FROM items2 WHERE name = %s"
            result = self.mysql.execute_query(sql,(id,))
            if result:
                return self.get_dict_from_result(result)
            else:
                raise KeyError
        else:
            raise TypeError

     def __setitem__(self,id,data):
        if type(id) is int:
            try:
                self.__getitem__(id)
            except IndexError:
                sql = 'INSERT INTO items2(id,description,name,icon,itemLevel) VALUES (%s,%s,%s,%s,%s)'
                self.mysql.update_query(sql,(id,data['description'],data['name'],data['icon'],data['itemLevel']))
            except TypeError:
                raise TypeError
            else:
                sql = 'UPDATE items2 SET description = %s, name = %s, icon = %s, itemLevel = %s WHERE id = %s'
                self.mysql.update_query(sql,(data['description'],data['name'],data['icon'],data['itemLevel'],data['id']))
        elif type(id) is str:
            try:
                self.__getitem__(id)
            except KeyError:
                sql = 'INSERT INTO items2(id,description,name,icon,itemLevel) VALUES (%s,%s,%s,%s,%s)'
                sql.mysql.update_query(sql,id,data['description'],data['name'],data['icon'],data['itemLevel'])
            except TypeError:
                raise TypeError
            else:
                sql = 'UPDATE items2 SET id = %s, description = %s, icon = %s,itemLevel = %s WHERE name = %s'
                self.mysql.update_query(sql,(data['id'],data['description'],data['icon'],data['itemLevel'],data['name']))
        else:
            print('неверное значение id')
            raise TypeError



