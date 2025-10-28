import sqlite3, base64, os
import app.apiros as apiros
from Crypto.Cipher import AES

class DBConn:
    def __init__(self, dbFile, masterPass):
        try:
            con = sqlite3.connect(dbFile)
            cur = con.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS devices(id INTEGER PRIMARY KEY AUTOINCREMENT, devName VARCHAR(255), devHost VARCHAR(255), devIp VARCHAR(255), devUser VARCHAR(255), devPass VARCHAR(255), devNonce)")
            self.masterPass = masterPass.encode().ljust(32)[:32]
            self.con = con
            self.cur = cur
        except:
            print("Connection to DB failed")        

    def encrypt(self, text):
        cipher = AES.new(text, AES.MODE_EAX)
        nonce = cipher.nonce
        return cipher.encrypt(text), nonce


    def decrypt(self, ciphertext, nonce):
        cipher = AES.new(self.masterPass, AES.MODE_EAX, nonce=nonce)
        return cipher.decrypt(ciphertext)

    def insert(self, devName, devIp, devUser, devPass):
        #devHost
        identity = apiros.ApiRos.getResponse(devIp, devUser, devPass, "/system/identity/print")
        if identity:
            devHost = identity["name"]
        else:
            devHost = devName
        #db insert
        ciphertext, nonce = self.encrypt(self.masterPass)
        self.cur.execute("INSERT INTO devices (devName, devHost, devIp, devUser, devPass, devNonce) VALUES (?, ?, ?, ?, ?, ?)", (devName, devHost, devIp, devUser, ciphertext, nonce))
        self.con.commit()

    def selectAll(self, decrypt=True):
        res = []
        for row in self.query("SELECT * FROM devices"):
            row = list(row)
            if decrypt:
                row[5] = self.decrypt(row[5], row[6]).strip()
            res.append(row)
        return res

    def select(self, query, decrypt=True):
        ans = self.query(query)
        for row in self.query(query):
            row = list(row)
        return ans

    def query(self, query):
        res = self.cur.execute(query)
        return res.fetchall()



"""

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

"""