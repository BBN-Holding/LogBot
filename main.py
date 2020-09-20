import json
import time
import discord
from pymongo import MongoClient

with open('config.json') as json_file:
    data = json.load(json_file)

mongoclient = MongoClient(data['uri'])
db = mongoclient.discordlog
print(db)


class EventClient(discord.Client):
    async def on_message(self, msg):
        db.sentmsgs.insert_one(
            {'type': 'msgsent', 'guildid': msg.guild.id, 'channelid': msg.channel.id, 'user': msg.author.id,
             'message': msg.content,
             'messageid': msg.id, 'time': time.time()}
        )

    async def on_typing(self, channel, user, when):
        db.starttyping.insert_one(
            {'type': 'starttyping', 'guildid': channel.guild.id, 'channelid': channel.id, 'user': user.id,
             'time': when}
        )

    async def on_message_delete(self, msg):
        db.delmsgs.insert_one(
            {'type': 'msgdel', 'guildid': msg.guild.id, 'channelid': msg.channel.id, 'user': msg.author.id,
             'message': msg.content,
             'messageid': msg.id, 'time': time.time()}
        )

    async def on_message_edit(self, before, after):
        db.editmsgs.insert_one(
            {'type': 'msgedit', 'guildid': before.guild.id, 'channelid': before.channel.id,
             'user': before.author.id, 'oldmessage': before.content, 'newmessage': after.content,
             'messageid': before.id, 'time': time.time()}
        )

    async def on_reaction_add(self, reaction, user):
        db.reacadd.insert_one(
            {'type': 'reacadd', 'guildid': reaction.message.guild.id, 'channelid': reaction.message.channel.id,
             'user': user.id, 'message': reaction.message.content,
             'messageid': reaction.message.id, 'reaction': str(reaction.emoji), 'count': reaction.count,
             'time': time.time()}
        )

    async def on_reaction_remove(self, reaction, user):
        db.reacrem.insert_one(
            {'type': 'reacrem', 'guildid': reaction.message.guild.id, 'channelid': reaction.message.channel.id,
             'user': user.id, 'message': reaction.message.content,
             'messageid': reaction.message.id, 'reaction': str(reaction.emoji), 'count': reaction.count,
             'time': time.time()}
        )

    async def on_reaction_clear(self, message):
        db.reacclear.insert_one(
            {'type': 'reacclear', 'guildid': message.guild.id, 'channelid': message.channel.id,
             'message': message.content, 'messageid': message.id, 'time': time.time()}
        )

    async def on_reaction_clear_emoji(self, reaction):
        db.reacspecclear.insert_one(
            {'type': 'reacspecclear', 'guildid': reaction.message.guild.id, 'channelid': reaction.message.channel.id,
             'message': reaction.message.content, 'messageid': reaction.message.id, 'reaction': str(reaction.emoji),
             'count': reaction.count, 'time': time.time()}
        )

    async def on_guild_channel_delete(self, channel):
        db.chdel.insert_one(
            {'type': 'chdel', 'guildid': channel.guild.id, 'channelid': channel.id, 'time': time.time()}
        )

    async def on_guild_channel_create(self, channel):
        db.chcre.insert_one(
            {'type': 'chcre', 'guildid': channel.guild.id, 'channelid': channel.id, 'time': time.time()}
        )

    async def on_member_join(self, member):
        db.memjoin.insert_one(
            {'type': 'memjoin', 'guildid': member.guild.id, 'user': member.id, 'time': time.time()}
        )

    async def on_member_remove(self, member):
        db.memleav.insert_one(
            {'type': 'memleav', 'guildid': member.guild.id, 'user': member.id, 'time': time.time()}
        )


for token in data['tokens']:
    EventClient().run(token, bot=False)
