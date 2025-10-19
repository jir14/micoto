import sqlite3

class Database:
    def __init__(self, dbFile):
        try:
            con = sqlite3.connect(dbFile)
            cur = con.cursor()
            self.con = con
            self.cur = cur
            cur.execute("CREATE TABLE IF NOT EXISTS routes(id INTEGER PRIMARY KEY AUTOINCREMENT, route VARCHAR(255))")
            cur.execute("CREATE TABLE IF NOT EXISTS options(id INTEGER PRIMARY KEY AUTOINCREMENT, routeId INTEGER, option VARCHAR(255), UNIQUE(routeId, option) ON CONFLICT REPLACE, FOREIGN KEY (routeId) REFERENCES routes(id) ON UPDATE CASCADE ON DELETE CASCADE)")
        except:
            print("Connection to DB failed")   
    
    def filterWords(self, word):
        self.cur.execute("SELECT id FROM forbidden_words WHERE word=?", (word,)) 
        if len(self.cur.fetchall()) == 0:
            return False
        else:
            return True
        
    def filterOptions(self, opt):
        self.cur.execute("SELECT id FROM forbidden_commands WHERE command=?", (opt,))
        if len(self.cur.fetchall()) == 0:
            return False
        else:
            return True
        
    def insertRoutes(self, route):
        if self.cur.execute("INSERT INTO routes (route) VALUES (?)", (route,)):
            self.con.commit()
            print(route)
            return True
        return False
    
    def clearTable(self, tableName):
        if self.cur.execute(f"DELETE FROM {tableName}"):
            self.con.commit()
            return True
        return False

    def insertOptions(self, route, options):
        #self.cur.execute("SELECT id FROM routes WHERE route=?", (route,))
        #self.cur.execute(f"SELECT id FROM routes WHERE route={route}")
        id = self.cur.fetchone()[0]
        for opt in options:
            self.cur.execute("INSERT INTO options (routeId, option) VALUES (?, ?)", (id,opt,))
            self.con.commit()
        return True