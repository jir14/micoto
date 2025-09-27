import sqlite3, base64, api
from cryptography.fernet import Fernet

class DBConn:
    def __init__(self, dbFile, masterPass):
        try:
            con = sqlite3.connect(dbFile)
            cur = con.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS devices(id INTEGER PRIMARY KEY AUTOINCREMENT, devName VARCHAR(255), devHost VARCHAR(255), devIp VARCHAR(255), devUser VARCHAR(255), devPass VARCHAR(255))")
            self.masterPass = masterPass.encode().ljust(32)[:32]
            self.con = con
            self.cur = cur
        except:
            print("Connection to DB failed")        

    def dbInsert(self, devName, devIp, devUser, devPass):
        #devHost
        try:
            apiros = api.ApiRos(api.open_socket(devIp, 8729, True))
            if not apiros.login(devUser, devPass):
                devHost = devName
            apiros.writeWord("/system/identity/print")
            apiros.writeWord("")
            res = apiros.readSentence()
            devHost = res[1].split("=")[2]
        except:
            print("cannot connect to device")
            devHost = devName

        #password encryption
        f = Fernet(base64.urlsafe_b64encode(self.masterPass))
        ciphertext = f.encrypt(devPass.encode())

        #db insert
        self.cur.execute("INSERT INTO devices (devName, devHost, devIp, devUser, devPass) VALUES (?, ?, ?, ?, ?)", (devName, devHost, devIp, devUser, ciphertext))
        self.con.commit()

    def dbSelect(self):
        res = self.cur.execute("SELECT * FROM devices")
        for row in res.fetchall():
            row = list(row)
            f = Fernet(base64.urlsafe_b64encode(self.masterPass))
            row[5] = f.decrypt(row[5])
        return row

    def dbQuery(self, query):
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