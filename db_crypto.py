import sqlite3
import sys
from cryptography.fernet import Fernet
import base64

masterPass = sys.argv[1]
devName = sys.argv[2]
devHost = sys.argv[3]
devIp = sys.argv[4]
devUser = sys.argv[5]
devPass = sys.argv[6]

#encryption
f = Fernet(base64.urlsafe_b64encode(masterPass.encode().ljust(32)[:32]))
ciphertext = f.encrypt(devPass.encode())

con = sqlite3.connect("test.db")

cur = con.cursor()

cur.execute("CREATE TABLE devices(id INTEGER PRIMARY KEY AUTOINCREMENT, devName VARCHAR(255), devHost VARCHAR(255), devIp, devUser, devPass VARCHAR(255))")

cur.execute("INSERT INTO devices (devName, devHost, devIp, devUser, devPass) VALUES (?, ?, ?, ?, ?)", (devName, devHost, devIp, devUser, ciphertext))

res = cur.execute("SELECT * FROM devices")

print(res.fetchone())

#decryption
res = cur.execute("SELECT * FROM devices")
for row in res.fetchall():
    f = Fernet(base64.urlsafe_b64encode(masterPass.encode().ljust(32)[:32]))
    print(f.decrypt(row[5]))
