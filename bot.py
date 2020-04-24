import discord
import os
import card_identify

from lor_deckcodes import LoRDeck, CardCodeAndCount
from discord.ext import commands

def cardParser(code):
    amount = code[0]
    cardCode = code[2:]
    return { "amount":amount, "code":cardCode}

def deckCompiler(deckcode):
    data = card_identify.cards_data
    target = LoRDeck.from_deckcode(deckcode)
    for card in target.cards:
        subject = cardParser(card)
        print(f"{data[subject.code].Name}:{subject.amount} lá")

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
