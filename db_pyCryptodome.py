import sqlite3
import sys
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

masterPass = sys.argv[1]
devName = sys.argv[2]
devHost = sys.argv[3]
devIp = sys.argv[4]
devUser = sys.argv[5]
devPass = sys.argv[6]

while len(masterPass)<16:
    masterPass+="0"

masterPass = masterPass.encode()

#encryption
cipher = AES.new(masterPass, AES.MODE_CTR, nonce=None)
ciphertext = cipher.encrypt(devPass.encode())
#nonce = cipher.nonce

print(masterPass, ciphertext)

con = sqlite3.connect("test.db")

cur = con.cursor()

cur.execute("CREATE TABLE devices(id INTEGER PRIMARY KEY AUTOINCREMENT, devName VARCHAR(255), devHost VARCHAR(255), devIp, devUser, devPass VARCHAR(255))")

cur.execute("INSERT INTO devices (devName, devHost, devIp, devUser, devPass) VALUES (?, ?, ?, ?, ?)", (devName, devHost, devIp, devUser, ciphertext))

res = cur.execute("SELECT * FROM devices")

print(res.fetchone())

#decryption
res = cur.execute("SELECT * FROM devices")
for row in res.fetchall():
    cipher = AES.new(masterPass, AES.MODE_CTR, nonce=None)
    print(cipher, row[5])
    message = cipher.decrypt(row[5])
    print("Password:", message)
