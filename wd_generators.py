import requests


class WowData():
    def __init__(self, cf):
        self.cf = cf

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
        path = 'https://eu.api.battle.net/wow/character/%s/%s?&locale=%s&apikey=%s' % (
            self.cf.guild_realm, char_name, self.cf.local, self.cf.wow_api_key)
        request_json = self.get_data_json(path)
        return request_json

    def get_item(self, item_id):
        '''Возвращает JSON с описанием запрошенного итема'''
        path = 'https://eu.api.battle.net/wow/item/%s?&locale=%s&apikey=%s' % (
            item_id, self.cf.local, self.cf.wow_api_key)
        request_json = self.get_data_json(path)
        return request_json

    def get_guild_news(self):
        '''Функция-генератор, возвращающая гильдейские новости'''
        path = 'https://eu.api.battle.net/wow/guild/%s/%s?fields=news&locale=%s&apikey=%s' % (
            self.cf.guild_realm, self.cf.guild_name, self.cf.local, self.cf.wow_api_key)
        request_json = self.get_data_json(path)

        for member in request_json['news']:
            yield member

    def get_races(self):
        '''Функция-генератор, возвращающая расы персонажей'''
        path = 'https://eu.api.battle.net/wow/data/character/races?locale=%s&apikey=%s' % (
            self.cf.local, self.cf.wow_api_key)
        request_json = self.get_data_json(path)

        for race in request_json['races']:
            yield race

    def get_classes(self):
        '''Функция - генератор, возвращающая классы персонажей'''
        path = 'https://eu.api.battle.net/wow/data/character/classes?locale=%s&apikey=%s' % (
            self.cf.local, self.cf.wow_api_key)
        request_json = self.get_data_json(path)

        for w_class in request_json['classes']:
            yield w_class

    def get_guild_members(self):
        '''Функция-генератор, возвращающая персонажей гильдии'''
        path = 'https://eu.api.battle.net/wow/guild/%s/%s?fields=members&locale=%s&apikey=%s' % (
            self.cf.guild_realm, self.cf.guild_name, self.cf.local, self.cf.wow_api_key)
        request_json = self.get_data_json(path)
        try:
            for member in request_json['members']:
                yield member
        except TypeError:
            print("Не удалось прочитать формат данных", request_json)
