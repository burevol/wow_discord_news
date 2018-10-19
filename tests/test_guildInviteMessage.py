from unittest import TestCase
from wd_config import Config
from wd_messages import GuildInviteMessage

class TestMember:
    def __init__(self):
        self.thumbnail = "testpicture.jpg"
        self.gender = 0
        self.isMember = 1

class TestGuildInvite:
    def __init__(self):
        self.character_name = "Test"
        self.title = "Title"
        self.member_obj = TestMember()


class TestGuildInviteMessage(TestCase):
    def setUp(self):
        self.cf = Config("wowdiscord.conf.debug")
        self.loot = TestGuildInvite()
        self.message = GuildInviteMessage(self.cf, self.loot)

    def test_post_message(self):
        self.message.post_message()

    def test_str(self):
        self.assertEqual(str(self.message), "Test присоединился к гильдии")
        self.loot.member_obj.gender = 1
        self.message = GuildInviteMessage(self.cf, self.loot)
        self.assertEqual(str(self.message), "Test присоединилась к гильдии")
        self.loot.member_obj.isMember = 0
        self.message = GuildInviteMessage(self.cf, self.loot)
        self.assertEqual(str(self.message), "Test покинула гильдию")
        self.loot.member_obj.gender = 0
        self.message = GuildInviteMessage(self.cf, self.loot)
        self.assertEqual(str(self.message), "Test покинул гильдию")
