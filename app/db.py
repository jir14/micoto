import sqlite3

class Database:
    def __init__(self, dbFile):
        try:
            con = sqlite3.connect(dbFile, check_same_thread=False)
            cur = con.cursor()
            self.con = con
            self.cur = cur
            cur.execute('CREATE TABLE IF NOT EXISTS "dirs" ("id" INTEGER NOT NULL UNIQUE, "higherID" INTEGER, "dir" TEXT, UNIQUE("dir","higherID") ON CONFLICT IGNORE, PRIMARY KEY("id" AUTOINCREMENT))')
            #cur.execute('INSERT INTO dirs (dir) VALUES ("")')
            cur.execute('CREATE TABLE IF NOT EXISTS "cmds" ("id" INTEGER NOT NULL UNIQUE, "cmd" TEXT NOT NULL, "dir_id" INTEGER NOT NULL, UNIQUE("cmd","dir_id") ON CONFLICT IGNORE, PRIMARY KEY("id" AUTOINCREMENT), FOREIGN KEY("dir_id") REFERENCES "dirs"("dir") ON DELETE CASCADE)')
            cur.execute('CREATE TABLE IF NOT EXISTS "args" ("id" INTEGER NOT NULL UNIQUE, "arg" TEXT NOT NULL, "cmd_id" INTEGER NOT NULL, UNIQUE("arg","cmd_id") ON CONFLICT IGNORE, PRIMARY KEY("id" AUTOINCREMENT), FOREIGN KEY("cmd_id") REFERENCES "cmds"("id") ON DELETE CASCADE)')
        except:
            print("Connection to DB failed")   
    
    def filterOptions(self, opt):
        self.cur.execute("SELECT id FROM forbidden_commands WHERE command=?", (opt,))
        if len(self.cur.fetchall()) == 0:
            return False
        else:
            return True
    
    def insertDir(self, dir, higherID=True):
        if higherID:
            if self.cur.execute("INSERT INTO dirs (dir, higherID) VALUES (?, ?)", (dir,higherID,)):
                self.con.commit()
                return self.cur.lastrowid
        else:
            if self.cur.execute("INSERT INTO dirs (dir) VALUES (?)", (dir,)):
                self.con.commit()
                return self.cur.lastrowid
        return False

    def insertDirs(self, dirs, higherID=True):  
        for dir in dirs:
            self.insertDir(dir, higherID)
        return True
    
    def insertCommands(self, dir, cmds):
        if self.cur.execute("SELECT id FROM dirs WHERE dir=?", (dir,)):
            id = self.cur.fetchone()[0]
            for cmd in cmds:
                self.cur.execute("INSERT INTO cmds (cmd, dir_id) VALUES (?, ?)", (cmd,id,))
                self.con.commit()
            return True
        return False

    def insertCmd(self, dirId, cmd):
        if self.cur.execute("SELECT id FROM dirs WHERE id=?", (dirId,)):
            id = self.cur.fetchone()[0]
            self.cur.execute("INSERT INTO cmds (cmd, dir_id) VALUES (?, ?)", (cmd,id,))
            self.con.commit()
            return self.cur.lastrowid
        return False


    def insertArgs(self, cmd, args, dirID=None):
        sql = "SELECT id FROM cmds WHERE cmd=?"
        params = [cmd]
        if dirID:
            sql = sql+" AND dir_id=?"
            params.append(dirID)
        id = self.getOne(sql, params)
        if id:
            for arg in args:
                if self.cur.execute("INSERT INTO args (arg, cmd_id) VALUES (?, ?)", (arg,id,)):
                    self.con.commit()
                    continue
            return True
        return False
    
    def getLevelDirs(self, level, bid=None):
        if bid:
            self.cur.execute("SELECT dir, bid FROM dirs WHERE level=?", (level,))
            res = []
            bid = []
            for re in self.cur.fetchall():
                res.append(re[0])
                bid.append(re[1])
            return res, bid
        else:
            self.cur.execute("SELECT dir FROM dirs WHERE level=?", (level,))
            res = []
            for re in self.cur.fetchall():
                res.append(re[0])
            return res
    
    def getLevelCmds(self, dir_id):
        if self.cur.execute("SELECT cmd FROM cmds WHERE dir_id=?", (dir_id,)):
            res = []
            for re in self.cur.fetchall():
                res.append(re[0])
            return res
        return False
    
    def getDirID(self, dir, bid=None, lvl=None, higherID=None):
        sql = "SELECT id FROM dirs WHERE dir=?"
        params = [dir]
        if bid:
            sql = sql+" AND bid=?"
            params.append(bid)
        if lvl:
            sql = sql+" AND level=?"
            params.append(lvl)
        if higherID:
            sql = sql+" AND higherID=?"
            params.append(higherID)
        return self.getOne(sql, params)
    
    def getDirName(self, dirID, bid=None):
        sql = "SELECT dir FROM dirs WHERE id=?"
        params = [dirID]
        if bid:
            sql = sql+" AND bid=?"
            params.append(bid)
        return self.getOne(sql, params)

    def getDirParentID(self, dir, bid=None):
        sql = "SELECT higherID FROM dirs WHERE"
        params = [dir]
        if type(dir) is int:
            sql = sql+" id=?"
        else:
            sql = sql+" dir=?"
        if bid:
            sql = sql+" AND bid=?"
            params.append(bid)
        return self.getOne(sql, params)
    
    def getDirParentName(self, dir, bid=None):
        if bid:
            perID = self.getDirParentID(dir, bid)
        else:
            perID = self.getDirParentID(dir)
        if perID:
            return self.getDirName(perID)
        return False
    
    def getDirCmds(self, dirID):
        if self.cur.execute("SELECT cmd FROM cmds WHERE dir_id=?", (dirID,)):
            res = []
            for re in self.cur.fetchall():
                res.append(re[0])
            return res
        return False
        
    def getDirDirs(self, dirID, bid=None):
        sql = "SELECT dir FROM dirs WHERE higherID=?"
        params = [dirID]
        if bid:
            sql = sql+" AND bid=?"
            params.append(bid)
        if self.cur.execute(sql, params):
            res = []
            for re in self.cur.fetchall():
                res.append(re[0])
            return res
        return False
            
    def getCmdArgs(self, cmdID):
        if self.cur.execute("SELECT arg FROM args WHERE cmd_id=?", (cmdID,)):
            res = []
            for re in self.cur.fetchall():
                res.append(re[0])
            return res
        return False

    def getCmdID(self, dirID):
        sql = "SELECT id FROM cmds WHERE dir_id=?"
        params = [dirID]
        return self.getOne(sql, params)
    
    def getDirLevel(self, dirID):
        if self.cur.execute("SELECT level FROM dirs WHERE id=?", (dirID,)):
            res = self.cur.fetchone()
            if res:
                return res[0]
        return False
    
    def getBaseID(self, parDirID):
        bid=parDirID
        while parDirID:
            parDirID = self.getDirParentID(parDirID)
            if parDirID:
                bid = parDirID
        return bid
    
    def getOne(self, sql, params):
        if self.cur.execute(sql, params):
            res = self.cur.fetchone()
            if res:
                return res[0]
        return False
    
    def printDirPath(self, dirID, bID=None):
        parDir = self.getDirName(dirID, bID)
        if parDir:
            path = parDir
        else:
            return
        while dirID:
            dirID = self.getDirParentID(dirID)
            if dirID:
                path = self.getDirName(dirID)+"/"+path
            else:
                break
        return "/"+path
    
    def getDirAddArgs(self, dirID):
        cmdID = self.getCmdID(dirID)
        return self.getCmdArgs(cmdID)

    def getDirDirsIDs(self, dirID):
        if self.cur.execute("SELECT id FROM dirs WHERE higherID=?", (dirID,)):
            res = []
            for re in self.cur.fetchall():
                res.append(re[0])
            return res
        return False
    
    def getLevelDirsIDs(self, level):
        if self.cur.execute("SELECT id FROM dirs WHERE level=?", (level,)):
            res = []
            for re in self.cur.fetchall():
                res.append(re[0])
            return res
        return False
    
    def getDirCmdsIDs(self, dirID):
        if self.cur.execute("SELECT id FROM cmds WHERE dir_id=?", (dirID,)):
            res = []
            for re in self.cur.fetchall():
                res.append(re[0])
            return res
        return False
    
    def getCmdName(self, cmdID):
        if self.cur.execute("SELECT cmd FROM cmds WHERE id=?", (cmdID,)):
            res = self.cur.fetchone()
            return res
        return False
    
    def getDirsWithoutParent(self):
        if self.cur.execute("SELECT id FROM dirs WHERE higherID IS NULL"):
            res = []
            for re in self.cur.fetchall():
                res.append(re[0])
            return res
        return False