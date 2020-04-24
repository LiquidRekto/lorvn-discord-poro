import discord
import os

from twisted_fate import Deck

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
        elif "!deck" in message.content.lower():
            await message.channel.send("Hiện tại chức năng tra Deck không khả dụng. Tui sẽ đem đến cho mấy bro sớm nhất có thể! OwO")
        elif (message.content.startsWith("!")):
            await message.channel.send(message.author + " AWAITING FUNCTION")

client.run(os.environ['DISCORD_TOKEN'])
