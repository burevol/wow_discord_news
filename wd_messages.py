class NewsMessages():
    pass

class ItemLootMessage(NewsMessages):
    def __init__(self, datalist):
        self.id = datalist[0]
        self.type = datalist[1]
        self.character_name = datalist[2]
        self.timestamp = datalist[3]
        self.itemId = datalist[4]
        self.context = datalist[5]
        self.posted = datalist[6]
    def __str__(self):
        return '%s получил %d'%(self.character_name,self.itemId)

class PlayerAchievementMessage(NewsMessages):
    def __init__(self,datalist):
        self.id = datalist[0]
        self.character_name = datalist[1]
        self.timestamp = datalist[2]
        self.context = datalist[3]
        self.achievement_id = datalist[4]
        self.title = datalist[5]
        self.description = datalist[6]
        self.icon = datalist[7]
        self.posted = datalist[8]
    def __str__(self):
        return '%s заслужил достижение %s'%(self.character_name,self.title)

class GuildAchievementMessage(NewsMessages):
    def __init__(self,datalist):
        self.id = datalist[0]
        self.character_name = datalist[1]
        self.timestamp = datalist[2]
        self.context = datalist[3]
        self.achievement_id = datalist[4]
        self.title = datalist[5]
        self.description = datalist[6]
        self.icon = datalist[7]
        self.posted = datalist[8]
    def __str__(self):
        print(self.character_name,self.title) 
        return 'Гильдия заслужила достижение %s'%(self.title)
      

