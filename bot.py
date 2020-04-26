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
        if "uwu" in message.content.lower(): #Tra loi UwU
            await message.channel.send("UwU")
            #tao deck
        if message.content.startswith('!deck'):
            ctx = message.content.split()
            if (len(ctx) < 2):
                await message.channel.send('Hổng có gì để xem hết... Bạn vui lòng đưa mình code ạ!')
            else:
                for code in ctx[1:]:
                    await message.channel.send('Mã Deck dã được giải rồi! Yay~')
                    await message.channel.send(embed = deckCompiler(code))   
        # Check neu do la admin (thuc hien chuc nang duoi)    
        if "admin" in [y.name.lower() for y in message.author.roles]:
            if message.content.startswith('$clear'):
                print(str(message.author.roles))
                print(str(message.channel))
                # Check vi
            if message.content.startswith('!wallet'):
                ctx = message.content.split()
                if (len(ctx) < 2):
                    wallet_check = db_getter.checkWalletInfo(str(message.author))
                    if (wallet_check == 'non-exist'):
                        await message.channel.send(f"{message.author.mention} Bạn chưa có ví!")
                    else:
                        msg = """\n Thông tin ví: \n
                        ID của ví: {} \n
                        Số Snax hiện có: {}
                        """.format(wallet_check["id"],wallet_check["snax"])
                        await message.channel.send(f"{message.author.mention} %s" % msg)
                else:
                    for status in ctx[1:]:
                        if status == 'create':
                            wallet = db_getter.addUserEconomyData(str(message.author), 0)
                            if wallet == 'duplicated':
                                await message.channel.send(f"{message.author.mention} Bạn đã tạo ví rồi! Vui lòng nhập !wallet để xem thông tin về ví của bạn hoặc !wallet help để biết thêm một số lệnh khác!")
                            else:
                                await message.channel.send(f"{message.author.mention} Bạn đã tạo ví mới! ID của ví bạn là: {wallet['id']}")
                        if status == 'destroy':
                            await message.channel.send(f"{message.author.mention} Hiện tại bạn không thể xoá ví!")
                        if status == 'snax':
                            snax = db_getter.getSnaxInfo(str(message.author))
                            if (snax == 'non-exist'):
                                msg = """Ví của bạn đâu? Tui không thể check được snax nếu bạn không có ví! ;(( \n
                                Tạo ví mới ngay bằng cách nhập !wallet create
                                """
                                await message.channel.send(f"{message.author.mention} %s" % msg)
                            else:
                                await message.channel.send(f"{message.author.mention} Bạn hiện tại đang có: **%s Snax!**" % snax["snax"])

                            
            if message.content.startswith('$reward'):
                ctx = message.content.split()
                

                

#@bot.command()
#async def test (ctx):
#print(ctx.message.member.)
        

        

client.run(os.environ['DISCORD_TOKEN'])
