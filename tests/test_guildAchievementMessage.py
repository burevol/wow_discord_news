from unittest import TestCase
from wd_config import Config
from wd_messages import GuildAchievementMessage


class TestMember:
    def __init__(self):
        self.thumbnail = "testpicture.jpg"
        self.gender = 0

class TestGuildAchievement:
    def __init__(self):
        self.character_name = "Test"
        self.title = "Title"
        self.member_obj = TestMember()


class TestGuildAchievementMessage(TestCase):
    def setUp(self):
        self.cf = Config("wowdiscord.conf.debug")
        self.loot = TestGuildAchievement()
        self.message = GuildAchievementMessage(self.cf, self.loot)

    def test_post_message(self):
        self.message.post_message()

    def test_str(self):
        self.assertEqual(str(self.message), "Гильдия заслужила достижение Title")
