from unittest import TestCase
from wd_messages import NewsMessages
from wd_config import Config


class TestNewsMessages(TestCase):
    def setUp(self):
        self.cf = Config("wowdiscord.conf.debug")
        NewsMessages.__abstractmethods__ = frozenset()
        self.nm = NewsMessages(self.cf)

    def test_get_item_image(self):
        result = self.nm.get_item_image( 11234)
        self.assertEqual(result,"https://render-eu.worldofwarcraft.com/icons/56/11234.jpg")
        result = self.nm.get_item_image( "11234")
        self.assertEqual(result, "https://render-eu.worldofwarcraft.com/icons/56/11234.jpg")

    def test_get_avatar_url(self):
        result = self.nm.get_avatar_url( "test_avatar.jpg")
        self.assertEqual(result,'https://render-eu.worldofwarcraft.com/character/test_avatar.jpg')
        self.assertRaises(TypeError, self.nm.get_avatar_url, 112)

    def test_get_item_url(self):
        result = self.nm.get_item_url( 11234)
        self.assertEqual(result, "http://eu.battle.net/wow/ru/item/11234")
        result = self.nm.get_item_url("11234")
        self.assertEqual(result, "http://eu.battle.net/wow/ru/item/11234")

