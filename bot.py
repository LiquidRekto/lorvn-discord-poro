import discord
import os
import card_identify
import card_image
import db_getter
import report_bot


from lor_deckcodes import LoRDeck
from discord.ext import commands

inAdmin = os.environ['ADMIN']

def authorIsAdmin(msg):
    identified = False
    for role in msg.author.roles:
        if (role.name == "admin") or (role.name == inAdmin):
            identified = True
            return True
    if identified == False:
        return False
        


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
    card_list = list(target)
    for card in card_list:
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
                await message.channel.send(f"{message.author.mention} Hổng có gì để xem hết... Bạn vui lòng đưa mình code ạ!")
            else:
                for code in ctx[1:]:
                    await message.channel.send('Mã Deck dã được giải rồi! Yay~')
                    await message.channel.send(embed = deckCompiler(code))  
        if message.content.startswith('!wallet'):
            ctx = message.content.split()
            if (len(ctx) < 2):
                wallet_check = db_getter.checkWalletInfo(str(message.author))
                if (wallet_check == 'non-exist'):
                    await message.channel.send(f"{message.author.mention} Bạn chưa có ví!")
                else:
                    msg = "\n *Thông tin ví:* \n ID của ví: **{}** \n Số Snax hiện có: **{}**".format(wallet_check["id"],wallet_check["snax"])                   
                    await message.channel.send(f"{message.author.mention} %s" % msg)
            else:
                for status in ctx[1:]:
                    if status == 'create':
                        wallet = db_getter.addUserEconomyData(str(message.author), 0)
                        if wallet == 'duplicated':
                            await message.channel.send(f"{message.author.mention} Bạn đã tạo ví rồi! Vui lòng nhập **!wallet** để xem thông tin về ví của bạn hoặc **!wallet help** để biết thêm một số lệnh khác!")
                        else:
                            await message.channel.send(f"{message.author.mention} Bạn đã tạo ví mới! ID của ví bạn là: {wallet['id']}")
                    if status == 'destroy':
                        await message.channel.send(f"{message.author.mention} Hiện tại bạn không thể xoá ví!")
                    if status == 'snax':
                        snax = db_getter.getSnaxInfo(str(message.author))
                        if (snax == 'non-exist'):
                            msg = "Ví của bạn đâu? Tui không thể check được snax nếu bạn không có ví! ;(( \n Tạo ví mới ngay bằng cách nhập **!wallet create**"
                            await message.channel.send(f"{message.author.mention} %s" % msg)
                        else:
                            await message.channel.send(f"{message.author.mention} Bạn hiện tại đang có: **%s Snax!**" % snax["snax"])
                    if status == 'help':
                        msg = "\n*Các lệnh liên quan đến* ***!wallet*** \n **(để không)** - Xem thông tin ví \n **create** - Tạo ví mới \n **snax** - Xem thông tin snax hiện có \n **destroy** - Xoá ví hiện tại đang sử dụng"
                        await message.channel.send(f"{message.author.mention} %s" % msg) 
        if message.content.startswith('!card'):
            ctx = message.content.split()
            if (len(ctx) < 2):
                await message.channel.send(f"{message.author.mention} Hổng có gì để xem hết... Bạn vui lòng đưa mình tên thẻ ạ!")
            else:
                card_name = ""
                for code in ctx[1:]:
                    card_name += code
                image_link = (card_image.image_urls[card_name])['CardArt']
                e = discord.Embed()
                e.set_image(url=image_link)
                await message.channel.send(f"{message.author.mention} Tìm được thẻ rồi nha~ OwO")
                await message.channel.send(embed = e)
        # Check neu do la admin (thuc hien chuc nang duoi)    
        if authorIsAdmin(message):
            if message.content.startswith("&clear"):
                con = message.content.split()
                msg = []
                lists = await message.channel.history(limit=int(con[1])+1).flatten()
                for x in lists:
                    msg.append(x)
                await message.channel.delete_messages(msg)
                await message.channel.send(f"{message.author.mention} Bạn đã xoá %s tin nhắn!" % con[1])
                # Check vi

            if message.content.startswith('&ban'):
                print('ban')

            if message.content.startswith('&mute'):
                print('mute')

            if message.content.startswith('&slowmode'):
                print('slow')
            


                            
            if message.content.startswith('&reward'):
                REQUIRED_LENGTH = 3
                contents = ['base','<user>','<amount>']
                ctx = message.content.split()
                if (len(ctx) < 3):
                    missers = ""
                    TRACK = len(ctx)
                    missing_contents = []
                    for num in contents:
                        if contents.index(num) > (TRACK - 1):
                            missing_contents.append(num)
                    for miss in missing_contents:
                        missers += "{} ".format(miss)
                    msg = "\nLệnh thưởng đã bị huỷ! \nLí do: Thiếu {}".format(missers)
                    await message.channel.send(f"{message.author.mention} %s" % msg)
                else:
                    content = db_getter.awardUser(ctx[1],ctx[2])
                    if content == 'user-not-exist':
                        msg = "\nLệnh thưởng đã bị huỷ! \nLí do: Người được thưởng không tồn tại hoặc chưa tạo ví!"
                        await message.channel.send(f"{message.author.mention} %s" % msg)
                    elif content == 'exceeded-number':
                        msg = "\nLệnh thưởng đã bị huỷ! \nLí do: Số snax mà bạn nhập vượt quá số ký tự quy định!"
                        await message.channel.send(f"{message.author.mention} %s" % msg)
                    elif content == 'negative-number':
                        msg = "\nLệnh thưởng đã bị huỷ! \nLí do: Số snax bạn nhập vào là số âm!"
                        await message.channel.send(f"{message.author.mention} %s" % msg)
                    else:
                        await message.channel.send(f"{message.author.mention} Chuyển thưởng thành công!")
            
            if message.content.startswith('&fine'):
                REQUIRED_LENGTH = 3
                contents = ['base','<user>','<amount>']
                ctx = message.content.split()
                if (len(ctx) < 3):
                    missers = ""
                    TRACK = len(ctx)
                    missing_contents = []
                    for num in contents:
                        if contents.index(num) > (TRACK - 1):
                            missing_contents.append(num)
                    for miss in missing_contents:
                        missers += "{} ".format(miss)
                    msg = "\nLệnh phạt đã bị huỷ! \nLí do: Thiếu {}".format(missers)
                    await message.channel.send(f"{message.author.mention} %s" % msg)
                else:
                    content = db_getter.fineUser(ctx[1],ctx[2])
                    if content == 'user-not-exist':
                        msg = "\nLệnh phạt đã bị huỷ! \nLí do: Người bị phạt không tồn tại hoặc chưa tạo ví!"
                        await message.channel.send(f"{message.author.mention} %s" % msg)
                    elif content == 'exceeded-number':
                        msg = "\nLệnh phạt đã bị huỷ! \nLí do: Số snax mà bạn nhập vượt quá số ký tự quy định!"
                        await message.channel.send(f"{message.author.mention} %s" % msg)
                    elif content == 'negative-number':
                        msg = "\nLệnh phạt đã bị huỷ! \nLí do: Số snax bạn nhập vào là số âm!"
                        await message.channel.send(f"{message.author.mention} %s" % msg)
                    else:
                        await message.channel.send(f"{message.author.mention} Phạt người chơi thành công!")

                

                

#@bot.command()
#async def test (ctx):
#print(ctx.message.member.)
        

        

client.run(os.environ['DISCORD_TOKEN'])
