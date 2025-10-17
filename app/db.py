import sqlite3

class Database:
    def __init__(self, dbFile):
        try:
            con = sqlite3.connect(dbFile)
            cur = con.cursor()
            self.con = con
            self.cur = cur
        except:
            print("Connection to DB failed")   
    
    def filter(self, word):
        self.cur.execute("SELECT id FROM forbidden_words WHERE word=?", (word,)) 
        if len(self.cur.fetchall()) == 0:
            return False
        else:
            return True