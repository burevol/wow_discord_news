import requests
from discord_hooks import Webhook
from wowmysql import get_new_messages_from_db
from wowmysql import get_item_info
from wowmysql import set_item_info
from wowmysql import mark_as_posted
from wowmysql import get_item_icon
from wowmysql import get_achievement_icon

discord_webhook_url = 'https://discordapp.com/api/webhooks/455653836619513857/ERE1MrqNg0bHz5VM7t-0hkXg1BvgXKDLX__PzP8TxbEe0EDxB4p36M11xA9yjFlQ3Vic'
wow_api_key = "cefjrjeny5778yyhg5s2cv6tet65hffd"
locale = "ru_RU"


def post_message(message, image = None, url = None):
    if image == None:
        msg = Webhook(discord_webhook_url,msg = message)
        msg.post()
    else:
        embed = Webhook(discord_webhook_url, msg=message) # NOTE: the `msg` kwarg is a normal message.
        #embed.set_thumbnail(image)
        if url != None:
           embed.set_title(title=message, url=url)
        embed.set_image(image)
        embed.post()

        #embed.set_footer(text=str,icon=url,ts=True) # NOTE: You can input `True` (current time) or an int timestamp.

        #data = {"content":message,"embeds":[{"image":{"url": image }}]}
        #print( data)
    #requests.post(discord_webhook_url, data = data)

def get_item(item_id):
    name = get_item_info(item_id)
    if name == '':
        path = 'https://eu.api.battle.net/wow/item/%s?locale=%s&apikey=%s' % (item_id,locale,wow_api_key)
        try:
            request = requests.get(path)
            request.raise_for_status()
            request_json = request.json()
        except requests.exceptions.RequestException as error:
            request_json = ''
        set_item_info(item_id,request_json['name'],request_json['icon'])
        return request_json['name']
    else:
        return name

def get_item_url(item_id):
    icon = get_item_icon(item_id)
    return  "https://render-eu.worldofwarcraft.com/icons/56/"+icon+".jpg"

def get_item_description_url(item_id):
    return "http://eu.battle.net/wow/ru/item/"+str(item_id)


def get_data(guild, realm, field):

    path = 'https://eu.api.battle.net/wow/guild/%s/%s?fields=%s&locale=%s&apikey=%s' % (
        realm, guild, field, locale, wow_api_key)

    try:
        request = requests.get(path)
        # Make sure the request doesn't error.
        request.raise_for_status()
        request_json = request.json()

    except requests.exceptions.RequestException as error:
       # If there's an issue or a character doesn't exist, return an empty string.
       request_json = ''

    return request_json

def get_achievement_url(achievment):
    icon = get_achievement_icon(achievment)
    return  "http://media.blizzard.com/wow/icons/36/"+icon+".jpg"
        

def post_new_messages():
    list_ids = []
    messages = get_new_messages_from_db()
    for message in messages:
        list_ids.append(message[0])
        if message[2] == 'itemLoot':
            item = get_item(message[4])
            url = get_item_url(message[4])
            description_url = get_item_description_url(message[4])
            post_message('%s получил %s'% (message[5],item),url,description_url)
        elif message[2] == 'itemCraft':
            item = get_item(message[4])
            url = get_item_url(message[4])
            description_url = get_item_description_url(message[4])
            post_message('%s скрафтил %s'% (message[5],item),url,description_url)
        elif message[2] == 'itemPurchase':
            item = get_item(message[4])
            url = get_item_url(message[4])
            description_url = get_item_description_url(message[4])
            post_message('%s прикупил %s'% (message[5],item),url,description_url)
        elif message[2] == 'playerAchievement':
            url = get_achievement_url(message[3])
            post_message('%s заслужил достижение %s'%(message[5],message[3]),url)
        elif message[2] == 'guildAchievement':
            url = get_achievement_url(message[3])
            post_message('%s приности гильдии достижение %s'%(message[5],message[3]),url)
    if len(list_ids) != 0:
        mark_as_posted(list_ids)




