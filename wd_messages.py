from abc import ABCMeta, abstractmethod

from discord_webhook.webhook import DiscordWebhook, DiscordEmbed


class NewsMessages(metaclass=ABCMeta):
    def __init__(self, cf):
        self.cf = cf

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def post_message(self):
        pass

    @staticmethod
    def get_item_image(item_id):
        """Возвращает URL изображения предмета"""
        return "https://render-eu.worldofwarcraft.com/icons/56/%s.jpg" % item_id

    @staticmethod
    def get_avatar_url(avatar):
        return 'https://render-eu.worldofwarcraft.com/character/' + avatar

    @staticmethod
    def get_item_url(item_id):
        """Возвращает URL описания предмета"""
        return "http://eu.battle.net/wow/ru/item/" + str(item_id)

    def send_message(self, message, avatar=None, author=None, image=None, url=None):
        """Отправляет сообщение в Discord"""
        if not self.cf.debug:
            web_hook = DiscordWebhook(self.cf.discord_webhook)
            embed = DiscordEmbed()
            embed.title = message
            embed.set_image(url=image)
            embed.set_url(url)
            embed.color = 242424
            embed.set_author(name=author, url=None, icon_url=avatar)
            embed.set_footer(text='Отправлено:')
            embed.set_timestamp()
            web_hook.add_embed(embed)
            web_hook.execute()
        else:
            print(message)


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
        if self.gender == 0:
            return '%s получил %s' % (self.character_name, self.item_name)
        else:
            return '%s получила %s' % (self.character_name, self.item_name)

    def post_message(self):
        answer = {"author": self.character_name, "message": str(self), "avatar": self.avatar, "image": self.image,
                  "url": self.url}
        self.send_message(**answer)


class PlayerAchievementMessage(NewsMessages):
    def __init__(self, cf, achievement):
        super().__init__(cf)
        self.character_name = achievement.character_name
        self.title = achievement.title
        self.avatar = self.get_avatar_url(achievement.member_obj.thumbnail)
        self.gender = achievement.member_obj.gender

    def __str__(self):
        if self.gender == 0:
            return '%s заслужил достижение %s' % (self.character_name, self.title)
        else:
            return '%s заслужила достижение %s' % (self.character_name, self.title)

    def post_message(self):
        answer = {"message": str(self), "avatar": self.avatar, 'image': self.avatar}
        self.send_message(**answer)


class GuildAchievementMessage(NewsMessages):
    def __init__(self, cf, achievement):
        super().__init__(cf)
        self.character_name = achievement.character_name
        self.title = achievement.title
        self.avatar = self.get_avatar_url(achievement.member_obj.thumbnail)

    def __str__(self):
        return 'Гильдия заслужила достижение %s' % self.title

    def post_message(self):
        answer = {"message": str(self), "avatar": self.avatar, 'image': self.avatar}
        self.send_message(**answer)


class GuildInviteMessage(NewsMessages):
    def __init__(self, cf, datalist):
        super().__init__(cf)
        self.character_name = datalist.character_name
        self.gender = datalist.member_obj.gender
        self.isMember = datalist.member_obj.isMember
        self.avatar = self.get_avatar_url(datalist.member_obj.thumbnail)

    def __str__(self):
        if self.isMember == 1:
            if self.gender == 0:
                return "%s присоединился к гильдии" % self.character_name
            else:
                return '%s присоединилась к гильдии' % self.character_name
        else:
            if self.gender == 0:
                return "%s покинул гильдию" % self.character_name
            else:
                return '%s покинула гильдию' % self.character_name

    def post_message(self):
        answer = {'message': str(self), 'avatar': self.avatar, 'image': self.avatar}
        self.send_message(**answer)
