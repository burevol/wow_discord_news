import configparser

class Config():
    def __init__(self):
        try:
            config = configparser.ConfigParser()
            config.read('wowdiscord.conf')
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
            print('Не удалось прочитать конфигурационный файл. Убедитесь в его наличии в папке программы и его правильной структуре.')

