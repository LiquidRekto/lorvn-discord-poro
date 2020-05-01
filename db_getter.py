import os
import psycopg2

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
    cur.execute("SELECT discord FROM economy WHERE discord = '%s'" % discord)
    check = cur.fetchone()
    if check == None:
        cur.execute("SELECT id_num FROM id_get")
        results = cur.fetchone()
        id = results[0]
        command = (
            "INSERT INTO economy (discord, id, snax)"
            "VALUES (%s, %s, %s)"
        )
        data = (discord, id, amount)
        cur.execute("UPDATE id_get SET id_num=%s",(id+1,))
        cur.execute(command,data)
        conn.commit()
        return {"id":id }
    else:
        return 'duplicated'
        

def awardUser(int, amount):
    cur.execute("SELECT discord FROM economy WHERE id = '%s'" % id)
    discord = (cur.fetchone())[0]
    key_str = getKeys()
    LIMIT = int(key_str["SNAX_DIGIT_LIMIT"])
    cur.execute("SELECT discord FROM economy WHERE id = '%s'" % id)
    user = cur.fetchone()
    if (user == None):
        return "user-not-exist"
    elif (len(amount) > LIMIT):
        return "exceeded-number"
    elif (amount[0] == '-'):
        return "negative-number"
    else:
        cur.execute("SELECT snax FROM economy WHERE id = '%s'" % id)
        currentAmnt = cur.fetchone()
        newAmnt = currentAmnt[0] + int(amount)
        cur.execute("UPDATE economy SET snax = %s WHERE id = '%s'" % (newAmnt, id))
        conn.commit()
        return {"user":discord, "snax":amount}

def fineUser(id, amount):
    cur.execute("SELECT discord FROM economy WHERE id = '%s'" % id)
    discord = (cur.fetchone())[0]
    key_str = getKeys()
    LIMIT = int(key_str["SNAX_DIGIT_LIMIT"])
    cur.execute("SELECT id FROM economy WHERE id = '%s'" % id)
    user = cur.fetchone()
    if (user == None):
        return "user-not-exist"
    elif (len(amount) > LIMIT):
        return "exceeded-number"
    elif (amount[0] == '-'):
        return "negative-number"
    else:
        cur.execute("SELECT snax FROM economy WHERE id = '%s'" % id)
        currentAmnt = cur.fetchone()
        newAmnt = currentAmnt[0] - int(amount)
        cur.execute("UPDATE economy SET snax = %s WHERE id = '%s'" % (newAmnt, id))
        conn.commit()
        
        return {"user":discord, "snax":amount}

def checkWalletInfoSelf(discord): #self
    cur.execute("SELECT * FROM economy WHERE discord = '%s'" % (discord))
    check = cur.fetchone()
    if (check == None):
        return 'non-exist'
    else:
        return {"id":check[0], "snax":check[2], "discord":discord}

def checkWalletInfoById(id):
    cur.execute("SELECT * FROM economy WHERE id = '%s'" % (id))
    check = cur.fetchone()
    if (check == None):
        return 'non-exist'
    else:
        return { "discord":check[1], "snax":check[2] }

def getSnaxInfo(discord): # self
    
    cur.execute("SELECT snax FROM economy WHERE discord = '%s'" % (discord))
    check = cur.fetchone()
    if (check == None):
        return 'non-exist'
    else:
        return {"snax": check[0]}