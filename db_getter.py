import os
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


def addUserEconomyData(discord, amount):
    cur.execute("SELECT discord_id FROM economy WHERE discord_id = '%s'" % discord_id)
    check = cur.fetchone()
    if (check == None):
        cur.execute("SELECT id_num FROM id_get")
        results = cur.fetchone()
        wallet_id = results[0]
        command = (
            "INSERT INTO economy (wallet_id, discord_id, snax)"
            "VALUES (%s, %s, %s)"
        )
        data = (wallet_id, discord_id, amount)
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
    if id.isdigit():
        cur.execute("SELECT discord_id FROM economy WHERE discord_id = '%s'" % id)
        discord = (cur.fetchone())[0]
        key_str = getKeys()
        LIMIT = int(key_str["SNAX_DIGIT_LIMIT"])
        cur.execute("SELECT discord_id FROM economy WHERE discord_id = '%s'" % id)
        user = cur.fetchone()
        if (user == None):
            return "user-not-exist"
        elif (len(amount) > LIMIT):
            return "exceeded-number"
        elif (amount[0] == '-'):
            return "negative-number"
        else:
            cur.execute("SELECT snax FROM economy WHERE discord_id = '%s'" % id)
            currentAmnt = cur.fetchone()
            newAmnt = currentAmnt[0] + int(amount)
            cur.execute("UPDATE economy SET snax = %s WHERE discord_id = '%s'" % (newAmnt, id))
            conn.commit()
            return {"user":discord, "snax":amount}
    else:
        return "input-error"

def fineUser(discord_id, amount):
    if id.isdigit():
        cur.execute("SELECT discord_id FROM economy WHERE discord_id = '%s'" % id)
        discord = (cur.fetchone())[0]
        key_str = getKeys()
        LIMIT = int(key_str["SNAX_DIGIT_LIMIT"])
        cur.execute("SELECT discord_id FROM economy WHERE discord_id = '%s'" % id)
        user = cur.fetchone()
        if (user == None):
            return "user-not-exist"
        elif (len(amount) > LIMIT):
            return "exceeded-number"
        elif (amount[0] == '-'):
            return "negative-number"
        else:
            cur.execute("SELECT snax FROM economy WHERE discord_id = '%s'" % id)
            currentAmnt = cur.fetchone()
            newAmnt = currentAmnt[0] - int(amount)
            cur.execute("UPDATE economy SET snax = %s WHERE discord_id = '%s'" % (newAmnt, id))
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
        return {"id":check[0], "snax":check[2], "discord":discord}

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