from unittest import TestCase
from wd_config import Config


class TestConfig(TestCase):
    def test_constructor(self):
        self.assertRaises(IOError, Config, "dowdiscord.conf")
        #self.assertRaises(KeyError,Config,"wowdiscord.conf.debug")
        cf = Config("wowdiscord.conf.debug")

        self.assertTrue(cf.dbhost, "Не найден параметр dbhost")
        self.assertTrue(cf.dbuser, "Не найден параметр dbuser")
        self.assertTrue(cf.dbpasswd, "Не найден параметр dbpasswd")
        self.assertTrue(cf.db, "Не найден параметр db")
        self.assertTrue(cf.guild_name, "Не найден параметр guild_name")
        self.assertTrue(cf.guild_realm, "Не найден параметр guild_realm")
        self.assertTrue(cf.discord_webhook, "Не найден параметр discord_webhook")
        self.assertTrue(cf.local, "Не найден параметр local")
        self.assertIn(cf.auth_mode, ("api_key", 'oauth2'), "Неверный параметр auth_mode")

        self.assertIn(cf.debug, (True, False), "Неверный параметр debug")

        if cf.auth_mode == 'api_key':
            self.assertTrue(cf.wow_api_key, "Не найден параметр wow_api_key")
        elif cf.auth_mode == 'oauth2':
            self.assertTrue(cf.client_id, "Не найден параметр client_id")
            self.assertTrue(cf.client_secret, "Не найден параметр secret")
