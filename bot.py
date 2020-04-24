import discord
import os

from twisted_fate import Deck

client = discord.Client()

@client.event
async def on_message(message):
    if message.author.bot:
        return
    else:
        if "uwu" in message.content.lower():
            await message.channel.send("UwU")

client.run(os.environ['DISCORD_TOKEN'])
