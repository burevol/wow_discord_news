from unittest import TestCase
from wd_config import Config
from wd_messages import PlayerAchievementMessage


class TestMember:
    def __init__(self):
        self.thumbnail = "testpicture.jpg"
        self.gender = 0

class TestPlayerAchievement:
    def __init__(self):
        self.character_name = "Test"
        self.title = "Title"
        self.member_obj = TestMember()


class TestPlayerAchievementMessage(TestCase):
    def setUp(self):
        self.cf = Config("wowdiscord.conf.debug")
        self.loot = TestPlayerAchievement()
        self.message = PlayerAchievementMessage(self.cf, self.loot)

    def test_post_message(self):
        self.message.post_message()

    def test_str(self):
        self.assertEqual(str(self.message),"Test заслужил достижение Title")
        self.loot.member_obj.gender = 1
        self.message1 = PlayerAchievementMessage(self.cf, self.loot)
        self.assertEqual(str(self.message1), "Test заслужила достижение Title")
