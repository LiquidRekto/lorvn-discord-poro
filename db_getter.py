import os
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cur = conn.cursor()

def addUserEconomyData(discord, amount):
    cur.execute("SELECT id_num FROM id_get")
    results = cur.fetchone()
    id = results[0]
    command = (
        "INSERT INTO economy (id, discord, snax)"
        "VALUES (%s, %s, %s)"
    )
    data = (id, discord, amount)
    cur.execute("UPDATE id_get SET id_num=%s",(id+1,))
    cur.execute(command,data)
    conn.commit()
    return {"id":id }