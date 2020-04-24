import discord
import os

from twisted_fate import Deck

client = discord.Client()

@client.event
async def on_message(message):
    if message.author.bot:
        return
    else:
        await message.channel.send("WowWowWow!")

client.run(os.environ['DISCORD_TOKEN'])
