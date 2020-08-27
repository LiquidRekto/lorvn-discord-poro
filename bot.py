import discord
import os
import card_identify
import card_image
import db_getter
import report_bot
import kaomoji_handler
import permissions
import utilities


from lor_deckcodes import LoRDeck
from discord.ext import commands

inAdmin = os.environ['ADMIN']

def getUserDiscordProperty(src, method, value):
    print(value)
    if (method == "by_name"):
        out = src.server.get_member()
        return out.id
    if (method == "by_id"):
        out_id = discord.utils.get(src.get_all_members(), id=int(value))
        return out_id.name

def authorIsAdmin(msg):
    identified = False
    for role in msg.author.roles:
        if (role.name == "admin") or (role.name == inAdmin) or (role.name == "SupremeMaster"):
            identified = True
            return True
    if identified == False:
        return False

def isSupremeMaster(msg):
    identified = False
    for role in msg.author.roles:
        if (role.name == "SupremeMaster"):
            identified = True
            return True
    if identified == False:
        return False

def checkEligibility(msg):
    identified = False
    if len(msg.author.roles) > 0:
        for role in msg.author.roles:
            print(role.name, permissions.checkPermissionOf(role.name))
            if (permissions.checkPermissionOf(role.name) is True):
                identified = True
                return True
                break
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

def regionEmote(reg, cli):
    switcher = {
        'Bilgewater':'704619522665086999',
        'Demacia':'704619523117940737',
        'Freljord':'704619523009019915',
        'Noxus':'704619523239706655',
        'Ionia':'704619522706898996',
        'PiltoverZaun':'704619522715418737',
        'ShadowIsles':'704619523172597860'
    }
    defined = False
    target = None
    out = switcher[reg]
    for emote in cli.emojis:
        print((emote.id, out))
        if (str(emote.id) == out):
            target = str(emote)
            defined = True
            break
    if defined:
        return target
    else:
        return ""


def cardParser(code):
    src = str(code)
    amount = src[0]
    cardCode = src[2:]
    card_set = cardCode[:2]
    card_region = cardCode[2:-3]
    return {"amount":amount, "cardCode":cardCode, "region":card_region, "set":card_set}

#def regionChunkCompiler(cards):

def deckCompiler(deckcode):
    outputmsg = f">>> "
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
         #tao emoji
        if kaomoji_handler.isAnEmote(message.content):
            await message.channel.send(kaomoji_handler.HandleKaomoji())
        if message.content.startswith('!requestfeature') or message.content.startswith('!rf'):

            ctx = message.content.split()
            if (len(ctx) < 2):
                await message.channel.send(f"{message.author.mention} Tui không thể góp ý hộ bạn nếu như nội dung đóng góp để trống! :v")
            else:
                try:
                    question = ""
                    for question_chunk in ctx[1:]:
                        question += question_chunk
                        if (ctx[1:].index(question_chunk) < len(ctx[1:]) - 1):
                            question += " "
                    me = discord.utils.get(client.get_all_members(), id=670673783002103811)
                    await me.send(f"Người dùng tên **{message.author}** đã hỏi:\n*{question}*")
                    await message.channel.send(f"{message.author.mention} Gửi đóng góp thành công!")
                except Exception as e:
                    print(str(e))
                    await message.channel.send(f"{message.author.mention} Đóng góp thất bại! XIn hãy thử lại!")

            #tao deck
        if message.content.startswith('!deck'):
            ctx = message.content.split()
            if (len(ctx) < 2):
                await message.channel.send(f"{message.author.mention} Hổng có gì để xem hết... Bạn vui lòng đưa mình code ạ!")
            else:
                for code in ctx[1:]:
                    try:
                        await message.channel.send(embed = deckCompiler(code))
                    except Exception as e:
                        print(e)
                        await message.channel.send(f"{message.author.mention} Hình như Code bạn cung cấp có vấn đề... bạn thử sửa lại code xem \n┐(︶▽︶)┌")
                    else:
                        await message.channel.send(f"{message.author.mention} Mã Deck dã được giải rồi! Yay~")

         # Kiểm tra ví
        if message.content.startswith('!poke'):
            await message.channel.send("Nào...BUỒN!")
        if message.content.startswith('!steal'):
            ctx = message.content.split()
            if len(ctx) > 1:
                if (len(message.mentions) > 0):
                    result = db_getter.stealSnax(message.author.id,message.mentions[0].id,message.mentions[0].status is 'online')
                    if (result == 'non-exist'):
                        await message.channel.send(f"{message.author.mention} Người dùng mà bạn muốn cướp snax không tồn tại hoặc chưa có ví!")
                    elif (result == 'no-snax'):
                        await message.channel.send(f"{message.author.mention} Hmm người đó rỗng túi rồi, thôi chọn người khác đi :>")
                    elif (result == 'unlucky'):
                        await message.channel.send(f"{message.author.mention} Úi, trượt rồi! Chúc bạn may mắn lần sau!")
                    else:
                        await message.channel.send(f"{message.author.mention} Bạn đã cướp thành công **%s Snax** từ **%s**!" % (result, message.mentions[0].name))
                else:
                    await message.channel.send(f"{message.author.mention} Phép màu sẽ không thành hiện thực nếu bạn không **Mention**! UwU")
            else:
                await message.channel.send(f"{message.author.mention} Bạn hem thể cướp được gì nếu bạn chỉ hô thôi mà không thực hiện :>")
        if message.content.startswith('!shop') and checkEligibility(message) is True:
            funcs = db_getter.getShopFunctionsList()
            embed_storage = []
            for func in funcs:
                embed=discord.Embed(title=f"**{func['shop_func']}**", description=f"{func['func_desc']}" ,color=0x5a3030)
                embed.add_field(name=f"Giá", value=f"{func['price']} Snax", inline=True)
                embed.add_field(name=f"Thời lượng sử dụng", value=f"{func['dur']}", inline=True)
                embed_storage.append(embed)
            await message.channel.send(f"{message.author.mention}\nChào mừng bạn đến với cửa hàng Poro!\nHiện tại tui đang có bán một số mặt hàng sau, bạn tham khảo nhé!\n\n")
            for em in embed_storage:
                await message.channel.send(embed=em)
        if message.content.startswith('!wallet') and checkEligibility(message) is True:
            ctx = message.content.split()
            if (len(ctx) < 2):
                try:
                    wallet_check = db_getter.checkWalletInfoSelf(str(message.author.id))
                    if (wallet_check == 'non-exist'):
                        await message.channel.send(f"{message.author.mention} Bạn chưa có ví!")
                    else:
                        msg = "\n *Thông tin ví:* \n ID của ví: **{}** \n Số Snax hiện có: **{}**".format(wallet_check["wallet_id"],wallet_check["snax"])
                        await message.channel.send(f"{message.author.mention} %s" % msg)
                except Exception as e:
                    print(e)
                    await message.channel.send(f"{message.author.mention} Có trục trặc trong xử lý lệnh. Xin bạn thử lại!")

            else:
                for status in ctx[1:]:
                    if status == 'create': # Tạo ví
                       # try:

                       # except:
                       #     await message.channel.send(f"{message.author.mention} Có trục trặc trong xử lý lệnh. Xin bạn thử lại!")
                        wallet = db_getter.addUserEconomyData(str(message.author.id), 0)
                        if wallet == 'duplicated':
                            await message.channel.send(f"{message.author.mention} Bạn đã tạo ví rồi! Vui lòng nhập **!wallet** để xem thông tin về ví của bạn hoặc **!wallet help** để biết thêm một số lệnh khác!")
                        else:
                            await message.channel.send(f"{message.author.mention} Bạn đã tạo ví mới! ID của ví bạn là: {wallet['wallet_id']}")

                    if status == 'destroy':
                        await message.channel.send(f"{message.author.mention} Hiện tại bạn không thể xoá ví!")
                    if status == 'snax': #Kiểm tra snax
                        try:
                            snax = db_getter.getSnaxInfo(str(message.author.id))
                        except:
                            await message.channel.send(f"{message.author.mention} Có trục trặc trong xử lý lệnh. Xin bạn thử lại!")
                        if (snax == 'non-exist'):
                            msg = "Ví của bạn đâu? Tui không thể check được snax nếu bạn không có ví! ;(( \n Tạo ví mới ngay bằng cách nhập **!wallet create**"
                            await message.channel.send(f"{message.author.mention} %s" % msg)
                        else:
                            await message.channel.send(f"{message.author.mention} Bạn hiện tại đang có: **%s Snax!**" % snax["snax"])
                    if status == 'help':
                        msg = "\n*Các lệnh liên quan đến* ***!wallet*** \n **(để không)** - Xem thông tin ví \n **create** - Tạo ví mới \n **snax** - Xem thông tin snax hiện có \n **destroy** - Xoá ví hiện tại đang sử dụng \n **peek <discord name>** - Xem thông tin ví của người khác"
                        await message.channel.send(f"{message.author.mention} %s" % msg)
                    if status == 'peek':
                        if len(ctx) < 3:
                            msg = "Úi! Tui hông thể kiểm tra ví của người đó nếu bạn chưa cung cấp thông tin!"
                            await message.channel.send(f"{message.author.mention} %s" % msg)
                        else:
                            username = ""
                            for chunk in ctx[2:]:
                                username += chunk
                                if (ctx[2:].index(chunk) < len(ctx[2:]) - 1):
                                    username += " "
                            try:
                                wallet_check = db_getter.checkWalletInfoSelf(message.mentions[0].id)
                                if wallet_check == "non-exist":
                                    await message.channel.send(f"{message.author.mention} Chủ sở hữu của ví mà bạn cần truy vấn không tồn tại!")
                                else:
                                    msg = "\n *Thông tin ví của {}:* \n ID của ví: **{}** \n Số Snax hiện có: **{}**".format(message.mentions[0].name,wallet_check["wallet_id"],wallet_check["snax"])
                                    await message.channel.send(f"{message.author.mention} %s" % msg)
                            except Exception as e:
                                print(e)
                                await message.channel.send(f"{message.author.mention} Có trục trặc trong xử lý lệnh. Xin bạn thử lại!")


        if message.content.startswith('!card') or message.content.startswith('!cardart'):
            image_link = None
            ctx = message.content.split()
            if (len(ctx) < 2):
                await message.channel.send(f"{message.author.mention} Hổng có gì để xem hết... Bạn vui lòng đưa mình tên thẻ ạ!")
            else:
                card_name = ""
                for code in ctx[1:]:
                    if code != "lvlup":
                        card_name += code
                    if (ctx[1:].index(code) < len(ctx[1:]) - 1):
                        card_name += " "
                if card_name[len(card_name) - 1] == " ":
                    card_name = card_name[:-1]
                if len(card_image.image_urls[card_name]) > 1:

                    for tar in card_image.image_urls[card_name]:
                        if 'isLevelledUp' in tar:
                            if ctx[len(ctx) - 1] == "lvlup":
                                if tar['isLevelledUp'] is True:
                                    if ctx[0] == '!card':
                                        image_link = tar['CardArt']
                                    else:
                                        image_link = tar['FullArt']
                                    break
                            else:
                                if tar['isLevelledUp'] is False:
                                    if ctx[0] == '!card':
                                        image_link = tar['CardArt']
                                    else:
                                        image_link = tar['FullArt']
                                    break
                else:
                    if ctx[0] == "!card":
                        image_link = ((card_image.image_urls[card_name])[0])['CardArt']
                    else:
                        image_link = ((card_image.image_urls[card_name])[0])['FullArt']
                print(image_link)
                e = discord.Embed()
                e.set_image(url=image_link)
                fig = ""
                if ctx[0] == "!card":
                    fig = "thẻ"
                else:
                    fig = "art"
                await message.channel.send(f"{message.author.mention} Tìm được {fig} rồi nha~ OwO")
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
                contents = ['base','<mention>','<amount>']
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
                    content = db_getter.awardUser(message.mentions[0].id,ctx[2])
                    if content == 'user-not-exist':
                        msg = "\nLệnh thưởng đã bị huỷ! \nLí do: Người được thưởng không tồn tại hoặc chưa tạo ví!"
                        await message.channel.send(f"{message.author.mention} %s" % msg)
                    elif content == 'exceeded-number':
                        msg = "\nLệnh thưởng đã bị huỷ! \nLí do: Số snax mà bạn nhập vượt quá số ký tự quy định!"
                        await message.channel.send(f"{message.author.mention} %s" % msg)
                    elif content == 'negative-number':
                        msg = "\nLệnh thưởng đã bị huỷ! \nLí do: Số snax bạn nhập vào là số âm!"
                        await message.channel.send(f"{message.author.mention} %s" % msg)
                    elif content == 'input-error':
                        msg = "\nLệnh thưởng đã bị huỷ! \nLí do: Lỗi nhập liệu!"
                        await message.channel.send(f"{message.author.mention} %s" % msg)
                    else:
                        await message.channel.send(f"{message.author.mention} Chuyển thưởng thành công!")

            if message.content.startswith('&fine'):
                REQUIRED_LENGTH = 3
                contents = ['base','<mention>','<amount>']
                ctx = message.content.split()
                if (len(ctx) < REQUIRED_LENGTH):
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
                    content = db_getter.fineUser(message.mentions[0].id,ctx[2])
                    if content == 'user-not-exist':
                        msg = "\nLệnh phạt đã bị huỷ! \nLí do: Người bị phạt không tồn tại hoặc chưa tạo ví!"
                        await message.channel.send(f"{message.author.mention} %s" % msg)
                    elif content == 'exceeded-number':
                        msg = "\nLệnh phạt đã bị huỷ! \nLí do: Số snax mà bạn nhập vượt quá số ký tự quy định!"
                        await message.channel.send(f"{message.author.mention} %s" % msg)
                    elif content == 'negative-number':
                        msg = "\nLệnh phạt đã bị huỷ! \nLí do: Số snax bạn nhập vào là số âm!"
                        await message.channel.send(f"{message.author.mention} %s" % msg)
                    elif content == 'input-error':
                        msg = "\nLệnh thưởng đã bị huỷ! \nLí do: Lỗi nhập liệu!"
                        await message.channel.send(f"{message.author.mention} %s" % msg)
                    else:
                        await message.channel.send(f"{message.author.mention} Phạt người chơi thành công!")

            if message.content.startswith('&peekwallet'):
                print()

            if message.content.startswith('&shopmng'):
                ctx = message.content.split()
                if len(ctx) > 1:
                    status = ctx[1]
                    if status == "add":

                        REQUIRED_LENGTH = 4
                        contents = ['<shop function>','<shop description>','<price>','<duration>']
                        shop_ctx = (utilities.getMergedStringChunks(ctx[2:])).split('<->')
                        if len(shop_ctx) < REQUIRED_LENGTH:
                            missers = ""
                            TRACK = len(shop_ctx)
                            missing_contents = []
                            for num in contents:
                                if contents.index(num) > (TRACK - 1):
                                    missing_contents.append(num)
                            for miss in missing_contents:
                                missers += "{} ".format(miss)
                            msg = "\nTạo mặt hàng mới không thành công! \nLí do: Thiếu {}".format(missers)
                            await message.channel.send(f"{message.author.mention} %s" % msg)
                        else:
                            result = db_getter.addShopFunction(shop_ctx[0],shop_ctx[1],shop_ctx[2],shop_ctx[3])
                            if (result == 'success'):
                                await message.channel.send(f"{message.author.mention} Khởi tạo mặt hàng thành công! Đã thêm vào kệ hàng!")
                            elif (result == 'duplicated'):
                                msg = "\nTạo mặt hàng mới không thành công! \nLí do: Đã tồn tại mặt hàng cùng tên"
                                await message.channel.send(f"{message.author.mention} Khởi tạo mặt hàng thành công! Đã thêm vào kệ hàng!")

                    if status == "remove":
                        print()

        if isSupremeMaster(message):
            if message.content.startswith('%testvalhax'):
                target = client.get_guild(748007473050419362)
                tar = discord.utils.get(client.guilds, id=695461977438421004)
                print(tar)






#@bot.command()
#async def test (ctx):
#print(ctx.message.member.)




client.run(os.environ['DISCORD_TOKEN'])
