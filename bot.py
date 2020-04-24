import discord
import os

from twisted_fate import Deck
from discord.ext import commands

def deckCompiler(deckcode):
    target = Deck.decode(deckcode)
    print(target.cards)

client = discord.Client()

@client.event
async def on_message(message):
    if message.author.bot:
        return
    else:
        if "uwu" in message.content.lower():
            await message.channel.send("UwU")
        if message.content.startswith('!deck'):
            ctx = message.content.split()
            deckCompiler(ctx[1:])
            await message.channel.send('Deck decoded!')
        

        

client.run(os.environ['DISCORD_TOKEN'])
