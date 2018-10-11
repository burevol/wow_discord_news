from wd_wowdiscord import WowDiscord
from wd_mysql import MySqlOperations
from wd_mysqlobjects import MysqlObjects
from wd_mysqlobjects_races import Races
from wd_mysqlobjects_classes import Classes
from wd_mysqlobjects_members import Members

if __name__ == '__main__':
    wd = WowDiscord()
    with MySqlOperations(wd.cf) as mysql:
        #classes = Classes(mysql)
        #classes.clear_table()
        #print(len(classes))
        #for classe in wd.get_classes():
        #    classes[classe['id']] = classe
        #    print(classe)
        #print(len(classes))
        cmembers = Members(mysql)
        cmembers.clear_table()
        members = wd.get_guild_members()
        for member in members:
             print(member['character']['name'])
             try:
                 item = cmembers[member['character']['name']]
             except KeyError:
                 cmembers[member['character']['name']] = member
             

        #races = Races(mysql)
        #races.clear_table()
        #print(len(races))

        #for race in wd.get_races():
        #    races[race['id']] = race
        #print(len(races))
        #print(races['Орк'])
        #print(races[28])
        #print(races['Гномэ'])
