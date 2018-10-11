from wd_mysql import MySqlOperations
from wd_mysqlobjects import MysqlObjects

class Races(MysqlObjects):
     def __init(self,mysql):
        super().__init__(mysql)
     def clear_table(self):
        super().clear_table('races')
     def get_dict_from_result(self,result):
        return {'id':result[0],'mask':result[1],'side':result[2],'name':result[3]}
     def __len__(self):
        sql = 'SELECT COUNT(*) FROM races'
        return self.mysql.execute_query(sql,())[0]
     def __getitem__(self,id):
        if type(id) is int:
            sql = "SELECT * FROM races WHERE race_id = %s"
            result = self.mysql.execute_query(sql,(id,))
            if result:
                return get_dict_from_result(result)
            else:
                raise IndexError
        elif type(id) is str:
            sql = "SELECT * FROM races WHERE name = %s"
            result = self.mysql.execute_query(sql,(id,))
            if result:
                return get_dict_from_result(result)
            else:
                raise KeyError
        else:
            raise TypeError

     def __setitem__(self,id,data):
        if type(id) is int:
            try:
                self.__getitem__(id)
            except IndexError:
                sql = 'INSERT INTO races(race_id,mask,side,name) VALUES (%s,%s,%s,%s)'
                self.mysql.update_query(sql,(id,data['mask'],data['side'],data['name']))
            except TypeError:
                raise TypeError
            else:
                sql = 'UPDATE races SET mask = %s, side = %s, name = %s WHERE race_id = %s'
                self.mysql.update_query(sql,(data['mask'],data['side'],data['name'],data['id']))
        elif type(id) is str:
            try:
                self.__getitem__(id)
            except KeyError:
                sql = 'INSERT INTO races(race_id,mask,side,name) VALUES (%s,%s,%s,%s)'
                sql.mysql.update_query(sql,id,data['mask'],data['side'],data['name'])
            except TypeError:
                raise TypeError
            else:
                sql = 'UPDATE races SET race_id = %s, mask = %s, side = %s WHERE name = %s'
                self.mysql.update_query(sql,(data['id'],data['mask'],data['side'],data['name'],data['name']))
        else:
            print('неверное значение id')
            raise TypeError



