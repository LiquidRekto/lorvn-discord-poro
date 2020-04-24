import discord
import os

from twisted_fate import Deck
from discord.ext import commands

def deckCompiler():
    print("Hi!")

client = discord.Client()

@client.event
async def on_message(message):
    if message.author.bot:
        return
    else:
        if "uwu" in message.content.lower():
            await message.channel.send("UwU")
        if "!deck" in message.content.lower():
            await message.channel.send("Hiện tại chức năng tra Deck không khả dụng. Tui sẽ đem đến cho mấy bro sớm nhất có thể! OwO")
        if message.content[0] == "!":
            await message.channel.send("COMMAND INITIALIZED")
        

        

client.run(os.environ['DISCORD_TOKEN'])
