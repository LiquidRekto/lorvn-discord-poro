import discord
import os
import card_identify

from lor_deckcodes import LoRDeck, CardCodeAndCount
from discord.ext import commands



def generateEmbed(deckData):
    embed=discord.Embed(title="Thông tin Deck", description="Deck Code", color=0xd34e05)
    embed.add_field(name=deckData, value="", inline=False)
    embed.set_footer(text="Deck hay thiệt!")
    return embed

def cardParser(code):
    src = str(code)
    amount = src[0]
    cardCode = src[2:]
    return {"amount":amount, "cardCode":cardCode}

def deckCompiler(deckcode):
    outputmsg = ">>>"
    data = card_identify.cards_data
    target = LoRDeck.from_deckcode(deckcode)
    for card in target.cards:
        subject = cardParser(card)
        chunkInfo = f"{(data[subject['cardCode']])['Name']}:{subject['amount']} lá"
        print(chunkInfo)
        outputmsg += f"{chunkInfo}\n"
    return generateEmbed(outputmsg)


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
                    await message.channel.send('Mã Deck dã được giải!')
                    await message.channel.send(embed = deckCompiler(code))
        

        

client.run(os.environ['DISCORD_TOKEN'])
