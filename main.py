import json
import requests

import discord

url = 'http://127.0.0.1:3000'

client = discord.Client()


@client.event
async def on_message(msg):
    log({'type': 'msgsent', 'channelid': msg.channel.id, 'authorid': msg.author.id, 'message': msg.content, 'messageid': msg.id})


with open('config.json') as json_file:
    data = json.load(json_file)


def log(obj):
    requests.post(url, json.dumps(obj).encode('utf-8'))


client.run(data['token'], bot=False)
