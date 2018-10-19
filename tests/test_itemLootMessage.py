from unittest import TestCase
from wd_config import Config
from wd_messages import ItemLootMessage


class TestMember:
    def __init__(self):
        self.thumbnail = "testpicture.jpg"
        self.gender = 0


class TestItem:
    def __init__(self):
        self.name = "hammer"
        self.icon = "icon.jpg"


class TestItemLoot:

    def __init__(self):
        self.itemId = 12345
        self.character_name = "Test"
        self.member_obj = TestMember()
        self.item_obj = TestItem()


class TestItemLootMessage(TestCase):
    def setUp(self):
        self.cf = Config("wowdiscord.conf.debug")
        self.loot = TestItemLoot()
        self.message = ItemLootMessage(self.cf, self.loot)

    def test_post_message(self):
        self.message.post_message()

    def test_str(self):
        self.assertEqual(str(self.message),"Test получил hammer")
        self.loot.member_obj.gender = 1
        self.message1 = ItemLootMessage(self.cf, self.loot)
        self.assertEqual(str(self.message1), "Test получила hammer")