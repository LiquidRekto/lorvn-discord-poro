import os
import math
import random
import psycopg2
import utilities

DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cur = conn.cursor()

def getKeys():
    board = {}
    cur.execute("SELECT * FROM bot_config")
    dat = cur.fetchall()
    for chunk in dat:
        key = chunk[0]
        val = chunk[1]
        board[key] = val
    return board


def addUserEconomyData(discord_id, amount):
    cur.execute("SELECT discord_id FROM economy WHERE discord_id = '%s'" % discord_id)
    check = cur.fetchone()
    if (check == None):
        cur.execute("SELECT id_num FROM id_get")
        results = cur.fetchone()
        wallet_id = results[0]
        command = (
            "INSERT INTO economy (wallet_id, discord_id, snax, steal_cd, steal_count)"
            "VALUES (%s, %s, %s, %s, %s)"
        )
        data = (wallet_id, discord_id, amount, utilities.getCurrentDatetime(), 0)
        cur.execute("UPDATE id_get SET id_num=%s",(wallet_id+1,))
        cur.execute(command,data)
        conn.commit()
        return {"wallet_id":wallet_id }
    else:
        return 'duplicated'

def addUserEconomyDataNew(discord_id, amount):
    cur.execute("SELECT discord_id FROM economy_new WHERE discord_id = '%s'" % discord_id)
    check = cur.fetchone()
    if (check == None):
        cur.execute("SELECT id_num FROM id_get")
        results = cur.fetchone()
        wallet_id = results[0]
        command = (
            "INSERT INTO economy_new (wallet_id, discord_id, snax)"
            "VALUES (%s, %s, %s)"
        )
        data = (wallet_id, discord_id, amount)
        cur.execute("UPDATE id_get SET id_num=%s",(wallet_id+1,))
        cur.execute(command,data)
        conn.commit()
        return {"wallet_id":wallet_id }
    else:
        return 'duplicated'


def awardUser(discord_id, amount):
    if discord_id is not None:
        cur.execute("SELECT discord_id FROM economy WHERE discord_id = '%s'" % discord_id)
        discord = (cur.fetchone())[0]
        key_str = getKeys()
        LIMIT = int(key_str["SNAX_DIGIT_LIMIT"])
        cur.execute("SELECT discord_id FROM economy WHERE discord_id = '%s'" % discord_id)
        user = cur.fetchone()
        if (user == None):
            return "user-not-exist"
        elif (len(amount) > LIMIT):
            return "exceeded-number"
        elif (amount[0] == '-'):
            return "negative-number"
        else:
            cur.execute("SELECT snax FROM economy WHERE discord_id = '%s'" % discord_id)
            currentAmnt = cur.fetchone()
            newAmnt = currentAmnt[0] + int(amount)
            cur.execute("UPDATE economy SET snax = %s WHERE discord_id = '%s'" % (newAmnt, discord_id))
            conn.commit()
            return {"user":discord, "snax":amount}
    else:
        return "input-error"

def fineUser(discord_id, amount):
    if discord_id is not None:
        cur.execute("SELECT discord_id FROM economy WHERE discord_id = '%s'" % discord_id)
        discord = (cur.fetchone())[0]
        key_str = getKeys()
        LIMIT = int(key_str["SNAX_DIGIT_LIMIT"])
        cur.execute("SELECT discord_id FROM economy WHERE discord_id = '%s'" % discord_id)
        user = cur.fetchone()
        if (user == None):
            return "user-not-exist"
        elif (len(amount) > LIMIT):
            return "exceeded-number"
        elif (amount[0] == '-'):
            return "negative-number"
        else:
            cur.execute("SELECT snax FROM economy WHERE discord_id = '%s'" % discord_id)
            currentAmnt = cur.fetchone()
            newAmnt = currentAmnt[0] - int(amount)
            cur.execute("UPDATE economy SET snax = %s WHERE discord_id = '%s'" % (newAmnt, discord_id))
            conn.commit()
            return {"user":discord, "snax":amount}
    else:
        return "input-error"

def checkWalletInfoSelf(discord_id): #self
    cur.execute("SELECT * FROM economy WHERE discord_id = '%s'" % (discord_id))
    check = cur.fetchone()
    if (check == None):
        return 'non-exist'
    else:
        return {"wallet_id":check[0], "snax":check[2], "discord":discord_id}

def checkWalletInfoById(id):
    cur.execute("SELECT * FROM economy WHERE discord_id = '%s'" % (id))
    check = cur.fetchone()
    if (check == None):
        return 'non-exist'
    else:
        return { "discord_id":check[1], "snax":check[2] }

def getSnaxInfo(discord): # self

    cur.execute("SELECT snax FROM economy WHERE discord_id = '%s'" % (discord))
    check = cur.fetchone()
    if (check == None):
        return 'non-exist'
    else:
        return {"snax": check[0]}

def getShopFunctionsList(): # UNDER CONSTRCUTION
    cur.execute("SELECT * FROM poro_shop")
    shop_funcs = cur.fetchall()
    func_list = []
    for func in shop_funcs:
        print(func)
        func_list.append({"shop_func":func[0], "func_desc":func[1], "price":func[2], "dur":func[3]})
    return func_list

def addShopFunction(shop_func, func_desc, price, dur): # UNDER CONSTRCUTION
    cur.execute("SELECT * FROM poro_shop WHERE shop_function = '%s'" % (shop_func))
    check = cur.fetchone()
    if (check != None):
        return 'duplicated'
    else:
        command = (
            "INSERT INTO poro_shop (shop_function, shop_function_desc, price, duration)"
            "VALUES (%s, %s, %s, %s)"
        )
        data = (shop_func, func_desc, price, dur)
        cur.execute(command,data)
        conn.commit()
        return 'success'


def removeShopFunction(shop_func, func_desc, price, dur): # UNDER CONSTRCUTION
    print('LUL')

def alterShopFunction(shop_func, sector): # UNDER CONSTRCUTION
    print('LUL')

def resetSteal():
    cur.execute("UPDATE economy SET steal_count = '0'")
    conn.commit()

def stealSnax(selfWallet, targetWallet, isOnline):
    cur.execute("SELECT steal_cd FROM economy WHERE discord_id = '%s'" % (selfWallet))
    cooldownFinished = utilities.dateTimeIsExpired(cur.fetchone()[0])
    cur.execute("SELECT steal_count FROM economy WHERE discord_id = '%s'" % (selfWallet))
    stealCount = cur.fetchone()[0]


    if (cooldownFinished is True):
        if (stealCount < 10):
            times = 1
            if (isOnline is True):
                times = 2
            cur.execute("SELECT snax FROM economy WHERE discord_id = '%s'" % (selfWallet))
            check = cur.fetchone()
            cur.execute("SELECT snax FROM economy WHERE discord_id = '%s'" % (targetWallet))
            check_2 = cur.fetchone()
            if (check_2 == None):
                return 'non-exist'
            else:
                selfSnax = check[0]
                targetSnax = check_2[0]
                if (targetSnax > 0):
                    number = random.randint(1,10)
                    print(number)
                    if (number == 2 or number == 5 or number == 8):
                        difference = times * math.floor(math.log(targetSnax,math.e))
                        selfSnax += difference
                        targetSnax -= difference

                        cur.execute("UPDATE economy SET snax = %s WHERE discord_id = '%s'" % (selfSnax, selfWallet))
                        cur.execute("UPDATE economy SET snax = %s WHERE discord_id = '%s'" % (targetSnax, targetWallet))
                        conn.commit()

                        return str(difference)
                    else:
                        return 'unlucky'
                else:
                    return 'no-snax'
                new_cd = utilities.dateTimeAddTime(utilities.getCurrentDatetime(),0,0,1,0)
                cur.execute("UPDATE economy SET steal_cd = %s WHERE discord_id = '%s'" % (new_cd, selfWallet))
                cur.execute("UPDATE economy SET steal_count = %s WHERE discord_id = '%s'" % (stealCount+1, selfWallet))
                conn.commit()
        else:
            return 'limit-reached'
    else:
        return 'cooldowned'



