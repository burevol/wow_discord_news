from wd_wowdiscord import WowDiscord
from wd_mysql import MySqlOperations
from wd_mysqlobjects import MysqlObjects
from wd_mysqlobjects_races import Races
from wd_mysqlobjects_classes import Classes

if __name__ == '__main__':
    wd = WowDiscord()
    with MySqlOperations(wd.cf) as mysql:
        classes = Classes(mysql)
        classes.clear_table()
        print(len(classes))
        for classe in wd.get_classes():
            classes[classe['id']] = classe
            print(classe)
        print(len(classes))
        

        #races = Races(mysql)
        #races.clear_table()
        #print(len(races))

        #for race in wd.get_races():
        #    races[race['id']] = race
        #print(len(races))
        #print(races['Орк'])
        #print(races[28])
        #print(races['Гномэ'])