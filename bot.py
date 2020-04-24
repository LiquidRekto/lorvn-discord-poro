import discord
import os

from twisted_fate import Deck

client = discord.Client()

@client.event
async def on_ready():
    print("Bot is ready!")

client.run(os.environ(['DISCORD_TOKEN']))
