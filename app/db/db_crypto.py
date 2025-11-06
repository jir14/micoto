import sqlite3, os
from ..api.apiros import ApiRos as apiros
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

class DBConn:
    def __init__(self, dbFile, masterPass):
        try:
            con = sqlite3.connect(dbFile)
            cur = con.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS devices(id INTEGER PRIMARY KEY AUTOINCREMENT, devHost VARCHAR(255), devIp VARCHAR(255), devUser VARCHAR(255), devPass VARCHAR(255), devIv VARCHAR(255))")
            self.masterPass = masterPass.encode().ljust(32)[:32]
            self.con = con
            self.cur = cur
        except:
            return False      

    def encrypt(self, text):
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES256(self.masterPass), modes.CBC(iv))
        encryptor = cipher.encryptor()
        return encryptor.update(text) + encryptor.finalize(), iv

    def decrypt(self, ciphertext, iv):
        decryptor = Cipher(algorithms.AES256(self.masterPass), modes.CBC(iv)).decryptor()
        return decryptor.update(ciphertext) + decryptor.finalize()

    def insert(self, devIp, devUser, devPass):
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

    def selectAll(self, decrypt=True):
        res = []
        for row in self.query("SELECT * FROM devices"):
            row = list(row)
            if decrypt:
                row[5] = self.decrypt(row[4], row[5]).strip()
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