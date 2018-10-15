# WoW -> Discord news


![GitHub last commit](https://img.shields.io/github/last-commit/google/skia.svg)
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/burevol/wow_discord_news/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/burevol/wow_discord_news/?branch=master)  
A small project to forward the news of the WoW guild to Discord  
A project still in development

### Requirements
* [discord-webhook 0.2.0](https://pypi.org/project/discord-webhook/ )
* [SQLAlchemy](https://www.sqlalchemy.org/)  

### Configuration file format  
```
[Config]
DBHOST = <IP address of MySQL server>
DBUSER = <user of MySQL database>
DBPASSWD =  <password>
DB =  <MySQL databas ename>
GUILD_NAME = <WoW guild name>
GUILD_REALM = <guild realm name e.g. borean-tundra>
DISCORD_WEBHOOK =  <Discord webhook URL>
WOW_API_KEY = <WoW API key (only for AUTH_MODE api_key)> 
LOCAL = <locale for WoW API quieries>
CLIENT_ID = <client id (only for oauth2)>
CLIENT_SECRET= <client secret (only for AUTH_MODE oauth2)>
AUTH_MODE = <api_key or oauth2>
```


### Usage  

```# python3 wow.py [-c path_to_config (default: ./wowdiscord.conf)]```


###Authors   

Alexandex Mavimov - [burevol](https://github.com/burevol)

