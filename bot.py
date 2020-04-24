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
            for code in ctx[1:]:
                if (code == "" or code is None):
                    await message.channel.send('Hổng có gì để xem hết... Bạn vui lòng đưa mình code ạ!')
                else:
                    deckCompiler(code)
                    await message.channel.send('Mã Deck dã được giải!')
        

        

client.run(os.environ['DISCORD_TOKEN'])
