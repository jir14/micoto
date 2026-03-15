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
            cur.execute('CREATE TABLE IF NOT EXISTS "cmds" ("id" INTEGER NOT NULL UNIQUE, "add_cmd" INTEGER NOT NULL DEFAULT 0, "set_cmd" INTEGER NOT NULL DEFAULT 0, "remove_cmd" INTEGER NOT NULL DEFAULT 0, "enable_cmd" INTEGER NOT NULL DEFAULT 0, "disable_cmd" INTEGER NOT NULL DEFAULT 0, "comment_cmd" INTEGER NOT NULL DEFAULT 0, "dir_id" INTEGER NOT NULL, UNIQUE("dir_id"), PRIMARY KEY("id" AUTOINCREMENT), FOREIGN KEY("dir_id") REFERENCES "dirs"("dir") ON DELETE CASCADE)')
            #cur.execute('CREATE TABLE IF NOT EXISTS "cmds" ("id" INTEGER NOT NULL UNIQUE, "cmd" TEXT NOT NULL, "dir_id" INTEGER NOT NULL, UNIQUE("cmd","dir_id") ON CONFLICT IGNORE, PRIMARY KEY("id" AUTOINCREMENT), FOREIGN KEY("dir_id") REFERENCES "dirs"("dir") ON DELETE CASCADE)')
            #cur.execute('CREATE TABLE IF NOT EXISTS "args" ("id" INTEGER NOT NULL UNIQUE, "arg" TEXT NOT NULL, "cmd_id" INTEGER NOT NULL, UNIQUE("arg","cmd_id") ON CONFLICT IGNORE, PRIMARY KEY("id" AUTOINCREMENT), FOREIGN KEY("cmd_id") REFERENCES "cmds"("id") ON DELETE CASCADE)')
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

    """def insertCmd(self, dirId, cmd):
        if self.cur.execute("SELECT id FROM dirs WHERE id=?", (dirId,)):
            id = self.cur.fetchone()[0]
            self.cur.execute("INSERT INTO cmds (cmd, dir_id) VALUES (?, ?)", (cmd,id,))
            self.con.commit()
            return self.cur.lastrowid
        return False"""
    
    def insertCmd(self, dirId, vals):
        if self.cur.execute("SELECT id FROM dirs WHERE id=?", (dirId,)):
            id = self.cur.fetchone()[0]
            self.cur.execute("INSERT INTO cmds ('add_cmd', 'set_cmd', 'remove_cmd', 'enable_cmd', 'disable_cmd', 'comment_cmd', dir_id) VALUES (?, ?, ?, ?, ?, ?, ?)", (vals["add"],vals["set"],vals["remove"],vals["enable"],vals["disable"],vals["comment"],id,))
            self.con.commit()
            return self.cur.lastrowid
        return False
    
    def getDirName(self, dirID):
        sql = "SELECT dir FROM dirs WHERE id=?"
        return self.getOne(sql, [dirID])

    def getDirParentID(self, dir, bid=None):
        sql = "SELECT higherID FROM dirs WHERE"
        params = [dir]
        if isinstance(dir, int):
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
        if self.cur.execute("SELECT add_cmd, set_cmd, remove_cmd, enable_cmd, disable_cmd, comment_cmd FROM cmds WHERE dir_id=?", (dirID,)):
            res=self.cur.fetchone()
            if res:
                return {"add":res[0], "set":res[1], "remove":res[2], "enable":res[3], "disable":res[4], "comment":res[5]}
        return False

    def getCmdID(self, dirID):
        sql = "SELECT id FROM cmds WHERE dir_id=?"
        params = [dirID]
        return self.getOne(sql, params)
    
    def getOne(self, sql, params):
        if self.cur.execute(sql, params):
            res = self.cur.fetchone()
            if res:
                return res[0]
        return False
    
    def printDirPath(self, dirID, spacer="/"):
        path=self.getDirName(dirID)
        while dirID:
            dirID = self.getDirParentID(dirID)
            if dirID:
                path = self.getDirName(dirID)+spacer+path
        return path

    def getDirDirsIDs(self, dirID):
        if self.cur.execute("SELECT id FROM dirs WHERE higherID=?", (dirID,)):
            res = []
            for re in self.cur.fetchall():
                res.append(re[0])
            if len(res)>0:
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
        """if self.cur.execute("SELECT cmd FROM cmds WHERE id=?", (cmdID,)):
            res = self.cur.fetchone()
            return res[0]"""
        return False
    
    def getDirsWithoutParent(self):
        if self.cur.execute("SELECT id FROM dirs WHERE higherID IS NULL"):
            res = []
            for re in self.cur.fetchall():
                res.append(re[0])
            return res
        return False
    
    def getCmdParentID(self, cmdID):
        if self.cur.execute("SELECT dir_id FROM cmds WHERE id=?", (cmdID,)):
            res = self.cur.fetchone()
            if res:
                return res[0]
        return False
    
    def getDirPath(self, dirID):
        path=self.getDirName(dirID=dirID)
        parDirID=self.getDirParentID(dir=dirID)
        while parDirID:
            path=str(self.getDirName(parDirID))+","+path
            parDirID=self.getDirParentID(parDirID)
        return path

    def getCmdPath(self, cmdID):
        path=""
        cmdName=self.getCmdName(cmdID=cmdID)
        parID=self.getCmdParentID(cmdID=cmdID)
        path=self.getDirPath(dirID=parID)+"/"+cmdName
        return path
    
    def getDirPathIDs(self, dirID):
        path=list()
        path.append(dirID)
        parent=self.getDirParentID(dir=dirID)
        while parent:
            path.append(parent)
            parent=self.getDirParentID(dir=parent)     
        return path
    
    def getCmdPathIDs(self, cmdID):
        dirID=self.getCmdParentID(cmdID=cmdID)
        path=self.getDirPathIDs(dirID=dirID)
        path.append(cmdID)
        return path
    
    def dbCopy(self, cmdIDs="", dirIDs="", path=""):
        self.cur.execute("ATTACH DATABASE ? AS 'COPY'", (path,))
        for dirID, value in dirIDs.items():
            if value:
                self.cur.execute("INSERT INTO COPY.dirs SELECT * FROM dirs WHERE id=?", (dirID,))
        for dirID in cmdIDs:
            vals={"add": 0, "set":0, "remove":0, "enable":0, "disable":0, "comment":0}
            for key, val in cmdIDs[dirID].items():
                vals[key]=val
            self.cur.execute("INSERT INTO COPY.cmds ('add_cmd', 'set_cmd', 'remove_cmd', 'enable_cmd', 'disable_cmd', 'comment_cmd', dir_id) VALUES (?, ?, ?, ?, ?, ?, ?)", (vals["add"],vals["set"],vals["remove"],vals["enable"],vals["disable"],vals["comment"],dirID,))
        self.con.commit()
        self.cur.execute("DETACH DATABASE 'COPY'")
        return