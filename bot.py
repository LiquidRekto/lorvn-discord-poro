import discord
import os

from twisted_fate import Deck

client = discord.Client()

@client.event
async def on_ready():
    print("Bot is ready!")

client.run('NzAzMDgwNDY1MTUzNzg1ODU2.XqJkTA.9ONX0zHzGKSiF91aYvhT7Pju9gc')
