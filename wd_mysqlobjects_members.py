from wd_mysql import MySqlOperations
from wd_mysqlobjects import MysqlObjects

class Members(MysqlObjects):
     def __init(self,mysql):
        super().__init__(mysql)
     def clear_table(self):
        super().clear_table('guild_members')
     def get_dict_from_result(self,result):
        return {'member_id':result[0],'name':result[1],'realm':result[2],'class':result[3],\
                       'race':result[4],'gender':result[5],'level':result[6],\
                       'achievementPoints':result[7],'thumbnail':result[8],'rank':result[9],\
                       'posted':result[9],'isMember':result[10],'is_check':result[11]}
     def __len__(self):
        sql = 'SELECT COUNT(*) FROM guild_members'
        return self.mysql.execute_query(sql,())[0]
     def __getitem__(self,id):
        if type(id) is str:
            sql = "SELECT * FROM guild_members WHERE name = %s"
            result = self.mysql.execute_query(sql,(id,))
            if result:
                return self.get_dict_from_result(result)
            else:
                raise KeyError
        else:
            raise TypeError

     def __setitem__(self,id,data):
        if type(id) is str:
            try:
                self.__getitem__(id)
            except KeyError:
                sql = 'INSERT INTO guild_members(name,realm,class,race,gender,level,\
                       achievementPoints,thumbnail,rank,isMember,posted,is_check) VALUES \
                       (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                self.mysql.update_query(sql,(data['character']['name'], \
                        data['character']['realm'],data['character']['class'], \
                        data['character']['race'],data['character']['gender'], \
                        data['character']['level'],data['character']['achievementPoints'], \
                        data['character']['thumbnail'],data['rank'],1,0,1))
            except TypeError:
                raise TypeError
            else:
                sql = 'UPDATE guild_members SET name = %s, realm = %s, class = %s, race = %s, \
                       gender = %s, level = %s, achievementPoints = %s, thumbnail = %s, \
                       rank = %s, isMember = %s, is_check = 1 WHERE name = %s'
                self.mysql.update_query(sql,(data['character']['name'],data['character']['realm'], \
                       data['character']['class'],data['character']['race'], \
                       data['character']['gender'],data['character']['level'], \
                       data['character']['achievementPoints'],data['character']['thumbnail'], \
                       data['rank'],1,id))
        else:
            print('неверное значение id')
            raise TypeError



