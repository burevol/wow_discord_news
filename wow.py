import requests
from wowmysql import *
from wow_discord import *


guild_name = "ххсекира перунахх"
guild_realm = "borean-tundra"

info = get_data(guild_name, guild_realm, 'news')

maximum_timestamp = get_maximum_timestamp()

for news in info['news']:
    if news['timestamp'] > maximum_timestamp:
        if news['type'] == "itemLoot":
            insert_news(news['timestamp'],news['type'],news['character'],news['itemId'],'','')
        elif news['type'] == "playerAchievement":
            insert_news(news['timestamp'],news['type'],news['character'],0,news['achievement']['description'],news['achievement']['icon'])
        elif news['type'] == "itemPurchase":
            insert_news(news['timestamp'],news['type'],news['character'],news['itemId'],'','')
        elif news['type'] == "itemCraft":
            insert_news(news['timestamp'],news['type'],news['character'],news['itemId'],'','')
        elif news['type'] == "guildAchievement":
            insert_news(news['timestamp'],news['type'],news['character'],0,news['achievement']['description'],news['achievement']['icon'])
post_new_messages()




