# -*- coding: utf-8 -*-
from configparser import ConfigParser
import traceback


class Config(object):
    def __init__(self, configfile=None):
        config = ConfigParser()
        if configfile is None:
            configfile = 'wowdiscord.conf'
        with open(configfile) as f:
            config.read( configfile, encoding="utf-8-sig")
            #   try:
        self.dbhost = config['Config']['DBHOST']
        self.dbuser = config['Config']['DBUSER']
        self.dbpasswd = config['Config']['DBPASSWD']
        self.db = config['Config']['DB']
        self.guild_name = config['Config']['GUILD_NAME']
        self.guild_realm = config['Config']['GUILD_REALM']
        self.discord_webhook = config['Config']['DISCORD_WEBHOOK']
        self.local = config['Config']['LOCAL']
        self.auth_mode = config['Config']['AUTH_MODE']

        if config['Config']['DEBUG'] == "On":
            self.debug = True
        else:
            self.debug = False

        if self.auth_mode == 'api_key':
            self.wow_api_key = config['Config']['WOW_API_KEY']
        elif self.auth_mode == 'oauth2':
            self.client_id = config['Config']['CLIENT_ID']
            self.client_secret = config['Config']['CLIENT_SECRET']
        # except KeyError:
        #     print('Не удалось прочитать конфигурационный файл', traceback.format_exc())
        # except:
        #     print('Неопознанная ошибка при чтении файла', traceback.format_exc())
