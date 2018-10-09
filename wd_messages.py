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
    def get_news_string(self,wdobject):
        char = wdobject.get_member_info(self.character_name)
        gender = char[5]
        avatar = wdobject.get_avatar(self.character_name)
        if gender == 0:
            message = '%s получил %s'%(self.character_name,wdobject.get_item_description(self.itemId)[2])
        else:
            message = '%s получила %s'%(self.character_name,wdobject.get_item_description(self.itemId)[2])
        image = wdobject.get_item_image(self.itemId)
        url = wdobject.get_item_url(self.itemId)
        answer= {"author":self.character_name,"message":message,"avatar":avatar,"image":image,"url":url}
        return answer
    def get_mark_query(self):
        return 'UPDATE item_loot SET posted = 1 WHERE id = "%d"' % (self.id)

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
    def get_news_string(self,wdobject):
        avatar = wdobject.get_avatar(self.character_name)
        message = '%s заслужил достижение %s'%(self.character_name,self.title)
        answer= {"message":message,"avatar":avatar}
        return answer
    def get_mark_query(self):
        return 'UPDATE player_achievement SET posted = 1 WHERE id = "%d"' % (self.id)
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
    def get_news_string(self,wdobject):
        avatar = wdobject.get_avatar(self.character_name)
        message = 'Гильдия заслужила достижение %s'%(self.title)
        answer= {"message":message,"avatar":avatar}
        return answer
    def get_mark_query(self):
        return  'UPDATE guild_achievement SET posted = 1 WHERE id = "%d"' % (self.id)
class GuildInviteMessage(NewsMessages):
    def __init__(self,datalist):
        self.id = datalist[0]
        self.character_name = datalist[1]
        self.gender = datalist[5]
        self.isMember = datalist[11]
    def __str__(self):
        if self.isMember == 1:
            if self.gender == 0:
                return "%s присоединился к гильдии"%(self.character_name)
            else:
                return '%s присоединилась к гильдии'%(self.character_name)
        else:
            if self.gender == 0:
                return "%s покинул гильдию"%(self.character_name)
            else:
                return '%s покинула гильдию'%(self.character_name)
    def get_news_string(self,wdobject):
        avatar = wdobject.get_avatar(self.character_name)
        if self.isMember == 1:
            if self.gender == 0:
                message = "%s присоединился к гильдии"%(self.character_name)
            else:
                message =  '%s присоединилась к гильдии'%(self.character_name)
        else:
            if self.gender == 0:
                message =  "%s покинул гильдию"%(self.character_name)
            else:
                message =  '%s покинула гильдию'%(self.character_name)
        answer = {'message':message,'avatar':avatar}
        return answer
    def get_mark_query(self):
        return 'UPDATE guild_members  SET posted = 1 WHERE id = "%d"' % (self.id)


