import sqlite3
import sys
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

con = sqlite3.connect("test.db")

cur = con.cursor()

cur.execute("CREATE TABLE devices(id INTEGER PRIMARY KEY AUTOINCREMENT, devName, devHost, devIp, devPass)")

masterPass = sys.argv[1]
devName = sys.argv[2]
devHost = sys.argv[3]
devIp = sys.argv[4]
devPass = sys.argv[5]

while len(masterPass)<16:
    masterPass+="0"

masterPass = bytes(masterPass, encoding='utf-8')

cipher = AES.new(masterPass, AES.MODE_EAX)
ciphertext, tag = cipher.encrypt_and_digest(devPass)

params = [devName, devHost, devIp, ciphertext]

cur.execute("""
    INSERT INTO devices VALUES
        ('?', '?', '?', '?')
""", params)

res = cur.execute("SELECT * FROM devices")

print(res.fetchone())