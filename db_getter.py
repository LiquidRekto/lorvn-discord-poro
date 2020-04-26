import os
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cur = conn.cursor()

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

def awardUser(discord, amount):
    cur.execute("SELECT discord FROM economy WHERE discord = '%s'" % discord)
    user = (cur.fetchone())[0]
    if (user == None):
        return "user-not-exist"
    else:
        cur.execute("SELECT snax FROM economy WHERE discord = '%s'" % discord)
        currentAmnt = cur.fetchone()
        newAmnt = currentAmnt[0] + int(amount)
        cur.execute("UPDATE economy SET snax = %s WHERE discord = '%s'" % (discord, newAmnt))
        conn.commit()
        return {"user":discord, "snax":amount}

def fineUser(discord, amount):
    print()

def checkWalletInfo(discord):
    cur.execute("SELECT * FROM economy WHERE discord = '%s'" % (discord))
    check = cur.fetchone()
    if (check == None):
        return 'non-exist'
    else:
        return {"id":check[1], "snax":check[2]}

def getSnaxInfo(discord):
    cur.execute("SELECT snax FROM economy WHERE discord = '%s'" % (discord))
    check = cur.fetchone()
    if (check == None):
        return 'non-exist'
    else:
        return {"snax": check[0]}