from wd_config import Config


class JSON_Generators():
    def __init__(self, cf):
        self.cf = cf

    def get_data_json(self, path):
        try:
            request = requests.get(path)
            request.raise_for_status()
            request_json = request.json()
        except requests.exceptions.RequestException as error:
            print('Ошибка получения данных json')
            request_json = []
        return request_json

    def get_guild_news(self):
        path = 'https://eu.api.battle.net/wow/guild/%s/%s?fields=news&locale=%s&apikey=%s' % (
            self.cf.guild_realm, self.cf.guild_name, self.cf.local, self.cf.wow_api_key)
        request_json = self.get_data_json(path)

        for member in request_json['news']:
            yield member

    def get_guild_members(self):
        '''Функция-генератор, возвращающая персонажей гильдии'''
        path = 'https://eu.api.battle.net/wow/guild/%s/%s?fields=members&locale=%s&apikey=%s' % (
            self.cf.guild_realm, self.cf.guild_name, self.cf.local, self.cf.wow_api_key)
        request_json = self.get_data_json(path)

        for member in request_json['members']:
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

    def get_item(self, item_id):
        path = 'https://eu.api.battle.net/wow/item/%s?locale=%s&apikey=%s' % (
        item_id, self.cf.local, self.cf.wow_api_key)
        request_json = self.get_data_json(path)
        return request_json
