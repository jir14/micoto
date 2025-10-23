import sqlite3

class Database:
    def __init__(self, dbFile):
        try:
            con = sqlite3.connect(dbFile)
            cur = con.cursor()
            self.con = con
            self.cur = cur
            cur.execute('CREATE TABLE IF NOT EXISTS "dirs" ("id" INTEGER NOT NULL UNIQUE, "higherID" INTEGER, "dir" TEXT UNIQUE ON CONFLICT IGNORE, "level" INTEGER NOT NULL, PRIMARY KEY("id" AUTOINCREMENT))')
            cur.execute('INSERT INTO dirs (dir, level) VALUES ("", 0)')
            cur.execute('CREATE TABLE IF NOT EXISTS "cmds" ("id" INTEGER NOT NULL UNIQUE, "cmd" TEXT NOT NULL, "dir_id" INTEGER NOT NULL, UNIQUE("cmd","dir_id") ON CONFLICT IGNORE, PRIMARY KEY("id" AUTOINCREMENT), FOREIGN KEY("dir_id") REFERENCES "dirs"("dir") ON DELETE CASCADE)')
            cur.execute('CREATE TABLE IF NOT EXISTS "args" ("id" INTEGER NOT NULL UNIQUE, "cmd_id" INTEGER NOT NULL, "arg" TEXT NOT NULL, UNIQUE("arg","cmd_id") ON CONFLICT IGNORE, PRIMARY KEY("id" AUTOINCREMENT), FOREIGN KEY("cmd_id") REFERENCES "cmds"("id") ON DELETE CASCADE)')
        except:
            print("Connection to DB failed")   
    
    def filterOptions(self, opt):
        self.cur.execute("SELECT id FROM forbidden_commands WHERE command=?", (opt,))
        if len(self.cur.fetchall()) == 0:
            return False
        else:
            return True

    def insertDirs(self, dirs, level, higherID=""):  
        for dir in dirs:
            if higherID == "":
                higherID=self.getDirParentID(dir)
            if self.cur.execute("INSERT INTO dirs (dir, level, higherID) VALUES (?, ?, ?)", (dir,level,higherID,)):
                self.con.commit()
                continue
            return False
        return True
    

    def insertCommands(self, dir, cmds):
        if self.cur.execute("SELECT id FROM dirs WHERE dir=?", (dir,)):
            id = self.cur.fetchone()[0]
            for cmd in cmds:
                self.cur.execute("INSERT INTO cmds (cmd, dir_id) VALUES (?, ?)", (cmd,id,))
                self.con.commit()
            return True
        return False

    def insertArgs(self, cmd, args):
        if self.cur.execute("SELECT id FROM cmds WHERE cmd=?", (cmd,)):
            id = self.cur.fetchone()[0]
            for arg in args:
                self.cur.execute("INSERT INTO args (arg, cmd_id) VALUES (?, ?)", (arg,id,))
                self.con.commit()
            return True
        return False
    
    def getLevelDirs(self, level):
        if self.cur.execute("SELECT dir FROM dirs WHERE level=?", (level,)):
            return self.cur.fetchall()
        return False
    
    def getLevelCmds(self, dir_id):
        if self.cur.execute("SELECT cmd FROM cmds WHERE dir_id=?", (dir_id,)):
            return self.cur.fetchall()
        return False
    
    def getDirID(self, dir):
        if self.cur.execute("SELECT id FROM dirs WHERE dir=?", (dir,)):
            res = self.cur.fetchone()
            if res:
                return res[0]
        return False
    
    def getDirName(self, dirID):
        if self.cur.execute("SELECT dir FROM dirs WHERE id=?", (dirID,)):
            res = self.cur.fetchone()
            if res:
                return res[0]
        return False
    
    def getDirParentID(self, dir):
        if self.cur.execute("SELECT higherID FROM dirs WHERE dir=?", (dir,)):
            res = self.cur.fetchone()
            if res:
                return res[0]
        return False
    
    def getDirParentName(self, dir):
        perID = self.getDirParentID(dir)
        if perID:
            return self.getDirName(perID)
        return False