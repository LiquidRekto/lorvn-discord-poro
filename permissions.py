import os
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cur = conn.cursor()

rolelist = {}

cur.execute('SELECT * FROM permissions;')
dat = cur.fetchall()
for chunk in dat:
    rolelist[chunk[0]] = chunk[1]

def checkPermissionOf(role):
    if role in rolelist:
        if (rolelist[role] is True):
            return True
        else:
            return False