import discord
import os
import card_identify
import db_getter


from lor_deckcodes import LoRDeck, CardCodeAndCount
from discord.ext import commands


# commands:
#   !deck <deckcode> <locale>, !wallet <(status, buy, pass, balance)>, !report <user> <reason>
#   !sharedeck <deckcode> <locale>
# 
# admin commands: 
#   $kick <user> <reason>, $mute <user> <time> <reason>, $slowmode <channel> <cooldown>
#   $announcement <description>, $warn <user> <reason>, $ban <user> <time> <reason>

def AdminRestriction(msg, userRole):
    output = {"isAdmin":False, "extra_msg":""}
    if msg.channel.author.mention == discord.Permissions.administrator:
        output["isAdmin"] = True
    return output

def generateEmbed(deckData, deckCode):
    embed=discord.Embed(title="**Thông tin Deck**", description=f"Deck Code: {deckCode}", color=0xd34e05)
    embed.add_field(name="Chi tiết", value=deckData, inline=False)
    embed.set_footer(text="Deck hay thiệt!")
    return embed

def cardParser(code):
    src = str(code)
    amount = src[0]
    cardCode = src[2:]
    return {"amount":amount, "cardCode":cardCode}

def deckCompiler(deckcode):
    outputmsg = ">>> "
    data = card_identify.cards_data
    target = LoRDeck.from_deckcode(deckcode)
    for card in target.cards:
        subject = cardParser(card)
        chunkInfo = f"**{subject['amount']} lá **- {(data[subject['cardCode']])['Name']}"
        print(chunkInfo)
        outputmsg += f"{chunkInfo}\n"
    return generateEmbed(outputmsg, deckcode)


bot = commands.Bot(command_prefix='%')
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
                print(code)
                if (code == "" or code is None):
                    await message.channel.send('Hổng có gì để xem hết... Bạn vui lòng đưa mình code ạ!')
                else:
                    await message.channel.send('Mã Deck dã được giải rồi! Yay~')
                    await message.channel.send(embed = deckCompiler(code))
        if message.content.startswith('!wallet'):
            wallet = db_getter.addUserEconomyData(message.author, 0)
            await message.channel.send(f"{message.author.mention} Bạn đã tạo ví mới! ID của ví bạn là: {wallet['id']}")
        if "admin" in [y.name.lower() for y in message.author.roles]:
            if message.content.startswith('$clear'):
                print(str(message.author.roles))
                print(str(message.channel))
            
                

#@bot.command()
#async def test (ctx):
#print(ctx.message.member.)
        

        

client.run(os.environ['DISCORD_TOKEN'])
