import discord
import os

from twisted_fate import Deck

client = discord.Client()

@client.event
async def on_message(message):
    if message.author.bot:
        return
    else:
        if "UwU" in message.content.lower():
            await message.channel.send("UwU")
        else:
            await message.channel.send("Wazzup {message.author}!")

client.run(os.environ['DISCORD_TOKEN'])
