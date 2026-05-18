import sqlite3, os
from ..api.apiros import ApiRos as apiros
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

class DBConn:
    def __init__(self, dbFile, masterPass, createFile=False):
        try:
            con = sqlite3.connect(dbFile)
            cur = con.cursor()
            print(createFile)
            if createFile:
                cur.execute("CREATE TABLE IF NOT EXISTS devices(id INTEGER PRIMARY KEY AUTOINCREMENT, devHost VARCHAR(255), devIp VARCHAR(255), devUser VARCHAR(255), devPass VARCHAR(255), devIv VARCHAR(255))")
            self.masterPass = masterPass.encode().ljust(32)[:32]
            self.con = con
            self.cur = cur
        except:
            print()     

    def checkDevFile(self):
        try:
            self.cur.execute("SELECT * FROM devices").fetchall()
        except sqlite3.OperationalError as e:
            return e
        else:
            return True

    def encrypt(self, text):
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES256(self.masterPass), modes.CBC(iv))
        encryptor = cipher.encryptor()
        return encryptor.update(text) + encryptor.finalize(), iv

    def decrypt(self, ciphertext, iv):
        decryptor = Cipher(algorithms.AES256(self.masterPass), modes.CBC(iv)).decryptor()
        return decryptor.update(ciphertext) + decryptor.finalize()

    def insert(self, devIp, devUser, devPass):
        if self.checkExistance(devIp):
            return False
        #devHost
        identity = apiros.getResponse(devIp, devUser, devPass, "/system/identity/print")
        if identity:
            devHost = identity["name"]
        else:
            devHost = ""
        #db insert
        devCipher, devIv = self.encrypt(devPass.encode().ljust(32)[:32])
        self.cur.execute("INSERT INTO devices (devHost, devIp, devUser, devPass, devIv) VALUES (?, ?, ?, ?, ?)", (devHost, devIp, devUser, devCipher, devIv))
        self.con.commit()
        return True

    def selectAll(self, decrypt=True):
        res = []
        for row in self.query("SELECT * FROM devices"):
            row = list(row)
            if decrypt:
                row[5] = self.decrypt(row[4], row[5]).strip()
            res.append(row)
        return res

    def selectDevUserAndPass(self, devIp):
        self.cur.execute("SELECT devUser, devPass, devIv FROM devices WHERE devIp=?", (devIp,))
        self.con.commit()
        row=list(self.cur.fetchone())
        return {row[0]:self.decrypt(row[1], row[2]).strip()}

    def select(self, query, decrypt=True):
        ans = self.query(query)
        for row in self.query(query):
            row = list(row)
        return ans

    def query(self, query):
        res = self.cur.execute(query)
        return res.fetchall()
    
    def remove(self, devIp):
        if self.cur.execute("DELETE FROM devices WHERE devIP=?", (devIp,)):
            self.con.commit()
            return True
        return False
    
    def checkExistance(self, devIp):
        res = self.cur.execute("SELECT devIp FROM devices WHERE devIP=?", (devIp,))
        if len(res.fetchall()) > 0:
            return True
        return False