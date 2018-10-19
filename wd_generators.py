import requests


class WowData():
    def __init__(self, cf):
        self.cf = cf
        self.token = None
        if cf.auth_mode == 'oauth2':
            path_oauth = 'https://us.battle.net/oauth/token?grant_type=client_credentials' \
                         '&client_id=%s&client_secret=%s' % (cf.client_id,cf.client_secret)

            request_oauth = requests.get(path_oauth)
            request_oauth.raise_for_status()
            request_json_oauth = request_oauth.json()
            self.cf.wow_api_key = request_json_oauth['access_token']
            self.auth_string = 'access_token'
            self.host = 'https://eu.api.blizzard.com'
        else:
            self.auth_string = "apikey"
            self.host = 'https://eu.api.battle.net'

    @staticmethod
    def get_data_json(path):
        '''Выполняет запрос по заданному пути'''
        try:
            request = requests.get(path)
            request.raise_for_status()
            request_json = request.json()
        except requests.exceptions.RequestException as error:
            print('Ошибка получения данных json')
            request_json = []
        return request_json

    def get_character(self, char_name):
        '''Возвращает JSON с описанием запрошенного персонажа'''
        path = '%s/wow/character/%s/%s?&locale=%s&%s=%s' % (
            self.host, self.cf.guild_realm, char_name, self.cf.local, self.auth_string, self.cf.wow_api_key)
        request_json = self.get_data_json(path)
        return request_json

    def get_item(self, item_id):
        '''Возвращает JSON с описанием запрошенного итема'''
        path = '%s/wow/item/%s?&locale=%s&%s=%s' % (
            self.host, item_id, self.cf.local, self.auth_string, self.cf.wow_api_key)
        request_json = self.get_data_json(path)
        return request_json

    def get_guild_news(self):
        '''Функция-генератор, возвращающая гильдейские новости'''
        path = '%s/wow/guild/%s/%s?fields=news&locale=%s&%s=%s' % (
            self.host, self.cf.guild_realm, self.cf.guild_name, self.cf.local, self.auth_string, self.cf.wow_api_key)
        request_json = self.get_data_json(path)

        for member in request_json['news']:
            yield member

    def get_races(self):
        '''Функция-генератор, возвращающая расы персонажей'''
        path = '%s/wow/data/character/races?locale=%s&%s=%s' % (
            self.host, self.cf.local, self.auth_string, self.cf.wow_api_key)
        request_json = self.get_data_json(path)

        for race in request_json['races']:
            yield race

    def get_classes(self):
        '''Функция - генератор, возвращающая классы персонажей'''
        path = '%s/wow/data/character/classes?locale=%s&%s=%s' % (
            self.host, self.cf.local, self.auth_string, self.cf.wow_api_key)
        request_json = self.get_data_json(path)

        for w_class in request_json['classes']:
            yield w_class

    def get_guild_members(self):
        '''Функция-генератор, возвращающая персонажей гильдии'''
        path = '%s/wow/guild/%s/%s?fields=members&locale=%s&%s=%s' % (
            self.host, self.cf.guild_realm, self.cf.guild_name, self.cf.local, self.auth_string, self.cf.wow_api_key)
        request_json = self.get_data_json(path)
        try:
            for member in request_json['members']:
                yield member
        except TypeError:
            print("Не удалось прочитать формат данных", request_json)
