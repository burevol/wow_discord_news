# -*- coding: utf-8 -*-
import configparser
import traceback


class Config():
    def __init__(self, configfile=None):
        try:
            config = configparser.ConfigParser()
            if configfile is not None:
                print("Читаем файл", configfile)
                config.read(configfile, encoding="utf-8-sig")
            else:
                print('Читаем wowdiscord')
                config.read('wowdiscord.conf', encoding="utf-8-sig")
            self.read_parameters(config)
        except:
            print('Не удалось прочитать конфигурационный файл', traceback.format_exc())

    def read_parameters(self, config):
        try:
            self.dbhost = config['Config']['DBHOST']
            self.dbuser = config['Config']['DBUSER']
            self.dbpasswd = config['Config']['DBPASSWD']
            self.db = config['Config']['DB']
            self.guild_name = config['Config']['GUILD_NAME']
            self.guild_realm = config['Config']['GUILD_REALM']
            self.discord_webhook = config['Config']['DISCORD_WEBHOOK']
            self.wow_api_key = config['Config']['WOW_API_KEY']
            self.local = config['Config']['LOCAL']
        except:
            print("Не удалось прочитать один из параметров конфигурационного файла")
