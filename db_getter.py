import os
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cur = conn.cursor()

def addUserEconomyData():
    cur.execute("SELECT id_num FROM id_get")
    results cur.fetchone()
    return results
    #cur.execute("INSERT INTO economy VALUES(%s %s %s)",
    #(id, discord, currency))