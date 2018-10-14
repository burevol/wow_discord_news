from webhook import DiscordWebhook, DiscordEmbed

class NewsMessages():
    def __init__(self, cf):
        self.cf = cf

    def get_item_image(self,item_id):
        '''Возвращает URL изображения предмета'''
        return "https://render-eu.worldofwarcraft.com/icons/56/%s.jpg"%(item_id)

    def get_avatar_url(self,avatar):
        return  'https://render-eu.worldofwarcraft.com/character/'+avatar

    def get_item_url(self,item_id):
        '''Возвращает URL описания предмета'''
        return "http://eu.battle.net/wow/ru/item/"+str(item_id)

    def post_message(self, message, avatar = None, author = None, image = None, url = None):
        '''Отправляет сообщение в Discord'''
        #print("message: %s, avatar: %s, author: %s, image: %s, url: %s"%(message,avatar,author,image,url))

        webhook = DiscordWebhook(self.cf.discord_webhook)
        embed = DiscordEmbed()
        embed.title = message
        embed.set_image(url=image)
        embed.set_url(url)
        embed.color = 242424
        embed.set_author(name=author, url=None, icon_url=avatar)
        embed.set_footer(text='Отправлено:')
        embed.set_timestamp()
        webhook.add_embed(embed)

        webhook.execute()

class ItemLootMessage(NewsMessages):
    def __init__(self, cf, loot):
        super().__init__(cf)
        self.character_name = loot.character_name
        self.itemId = loot.itemId
        self.avatar = self.get_avatar_url(loot.member_obj.thumbnail)
        self.item_name = loot.item_obj.name
        self.gender = loot.member_obj.gender
        self.image = self.get_item_image(loot.item_obj.icon)
        self.url = self.get_item_url(loot.itemId)

    def __str__(self):
        return '%s получил %d'%(self.character_name,self.itemId)

    def post_message(self):
        if not self.gender:
            message = '%s получил %s'%(self.character_name,self.item_name)
        else:
            message = '%s получила %s'%(self.character_name,self.item_name)
        answer= {"author":self.character_name,"message":message,"avatar":self.avatar,"image":self.image,"url":self.url}
        super().post_message(**answer)

class PlayerAchievementMessage(NewsMessages):
    def __init__(self,cf,achievement):
        super().__init__(cf)
        self.character_name = achievement.character_name
        self.title = achievement.title
        self.avatar = self.get_avatar_url(achievement.member_obj.thumbnail)
    def __str__(self):
        return '%s заслужил достижение %s'%(self.character_name,self.title)

    def post_message(self):
        message = '%s заслужил достижение %s'%(self.character_name,self.title)
        answer= {"message":message,"avatar":self.avatar,'image':self.avatar}
        super().post_message(**answer)

class GuildAchievementMessage(NewsMessages):
    def __init__(self,cf,achievement):
        super().__init__(cf)
        self.character_name = achievement.character_name
        self.title = achievement.title
        self.avatar = self.get_avatar_url(achievement.member_obj.thumbnail)

    def __str__(self):
        print(self.character_name,self.title) 
        return 'Гильдия заслужила достижение %s'%(self.title)

    def post_message(self):
        message = 'Гильдия заслужила достижение %s'%(self.title)
        answer= {"message":message,"avatar":self.avatar,'image':self.avatar}
        super().post_message(**answer)

class GuildInviteMessage(NewsMessages):
    def __init__(self,cf,datalist):
        super().__init__(cf)
        self.id = datalist[0]
        self.character_name = datalist[1]
        self.gender = datalist[5]
        self.isMember = datalist[11]
        self.avatar = datalist[8]
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
    def post_message(self):
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
        avatar_url = self.get_avatar_url(self.avatar)
        answer = {'message':message,'avatar':avatar_url,'image':avatar_url}
        super().post_message(**answer)
