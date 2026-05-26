import sqlite3

class Database:
    def __init__(self, dbFile, create=False):
        """Initialises command database object"""
        try:
            self.con = sqlite3.connect(dbFile, check_same_thread=False)
            self.cur = self.con.cursor()
            if create:
                self.cur.execute('CREATE TABLE IF NOT EXISTS "dirs" ("id" INTEGER NOT NULL UNIQUE, "higherID" INTEGER, "dir" TEXT, UNIQUE("dir","higherID") ON CONFLICT IGNORE, PRIMARY KEY("id" AUTOINCREMENT))')
                self.cur.execute('CREATE TABLE IF NOT EXISTS "cmds" ("id" INTEGER NOT NULL UNIQUE, "add_cmd" INTEGER NOT NULL DEFAULT 0, "set_cmd" INTEGER NOT NULL DEFAULT 0, "remove_cmd" INTEGER NOT NULL DEFAULT 0, "enable_cmd" INTEGER NOT NULL DEFAULT 0, "disable_cmd" INTEGER NOT NULL DEFAULT 0, "comment_cmd" INTEGER NOT NULL DEFAULT 0, "dir_id" INTEGER NOT NULL, UNIQUE("dir_id"), PRIMARY KEY("id" AUTOINCREMENT), FOREIGN KEY("dir_id") REFERENCES "dirs"("dir") ON DELETE CASCADE)')
            self.checkCmdFile()
        except:
            pass
            #print("Connection to DB failed")

    def checkCmdFile(self):
        """Check if right database file chosen (existance of `dirs` and `cmds` table)"""
        try:
            self.cur.execute("SELECT * FROM dirs").fetchall()
            self.cur.execute("SELECT * FROM cmds").fetchall()
        except sqlite3.OperationalError as e:
            return e
    
    def insertDir(self, dir, higherID=True):
        """Inserts dir in database"""
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
        """Loops through dir list, calls `insertDir` function"""
        for dir in dirs:
            self.insertDir(dir, higherID)
        return True
    
    def insertCommands(self, dir, cmds):
        """Insert commands to database"""
        if self.cur.execute("SELECT id FROM dirs WHERE dir=?", (dir,)):
            id = self.cur.fetchone()[0]
            for cmd in cmds:
                self.cur.execute("INSERT INTO cmds (cmd, dir_id) VALUES (?, ?)", (cmd,id,))
                self.con.commit()
            return True
        return False
    
    def insertCmd(self, dirId, vals):
        """Insert available commands to database (add, set, remove, etc...)"""
        if self.cur.execute("SELECT id FROM dirs WHERE id=?", (dirId,)):
            id = self.cur.fetchone()[0]
            self.cur.execute("INSERT INTO cmds ('add_cmd', 'set_cmd', 'remove_cmd', 'enable_cmd', 'disable_cmd', 'comment_cmd', dir_id) VALUES (?, ?, ?, ?, ?, ?, ?)", (vals["add"],vals["set"],vals["remove"],vals["enable"],vals["disable"],vals["comment"],id,))
            self.con.commit()
            return self.cur.lastrowid
        return False
    
    def getDirName(self, dirID):
        """Returns directory name from dirId"""
        sql = "SELECT dir FROM dirs WHERE id=?"
        return self.getOne(sql, [dirID])

    def getDirParentID(self, dir, bid=None):
        """Returns parent directory"""
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
        """Returns name of parent directory"""
        if bid:
            perID = self.getDirParentID(dir, bid)
        else:
            perID = self.getDirParentID(dir)
        if perID:
            return self.getDirName(perID)
        return False
    
    def getDirCmds(self, dirID):
        """Returns all available commands in certain directory"""
        if self.cur.execute("SELECT add_cmd, set_cmd, remove_cmd, enable_cmd, disable_cmd, comment_cmd FROM cmds WHERE dir_id=?", (dirID,)):
            res=self.cur.fetchone()
            if res:
                return {"add":res[0], "set":res[1], "remove":res[2], "enable":res[3], "disable":res[4], "comment":res[5]}
        return False

    def getCmdID(self, dirID):
        """Returns command id"""
        sql = "SELECT id FROM cmds WHERE dir_id=?"
        params = [dirID]
        return self.getOne(sql, params)
    
    def getOne(self, sql, params):
        """Helper function - returns one result"""
        if self.cur.execute(sql, params):
            res = self.cur.fetchone()
            if res:
                return res[0]
        return False
    
    def printDirPath(self, dirID, spacer="/"):
        """Returns whole command path separated by defined spacer"""
        path=self.getDirName(dirID)
        while dirID:
            dirID = self.getDirParentID(dirID)
            if dirID:
                path = self.getDirName(dirID)+spacer+path
        return path

    def getDirDirsIDs(self, dirID):
        """Returns ids of subdirectory"""
        if self.cur.execute("SELECT id FROM dirs WHERE higherID=?", (dirID,)):
            res = []
            for re in self.cur.fetchall():
                res.append(re[0])
            if len(res)>0:
                return res
        return False
    
    def getDirCmdsIDs(self, dirID):
        """Returns directory command ids"""
        if self.cur.execute("SELECT id FROM cmds WHERE dir_id=?", (dirID,)):
            res = []
            for re in self.cur.fetchall():
                res.append(re[0])
            return res
        return False
    
    def getDirsWithoutParent(self):
        """Returns dirs without parents (root dirs)"""
        if self.cur.execute("SELECT id FROM dirs WHERE higherID IS NULL"):
            res = []
            for re in self.cur.fetchall():
                res.append(re[0])
            return res
        return False
    
    def getCmdParentID(self, cmdID):
        """Returns parent dir id"""
        if self.cur.execute("SELECT dir_id FROM cmds WHERE id=?", (cmdID,)):
            res = self.cur.fetchone()
            if res:
                return res[0]
        return False
    
    def getDirPath(self, dirID):
        """Creates complete dir path, used only in backend"""
        path=self.getDirName(dirID=dirID)
        parDirID=self.getDirParentID(dir=dirID)
        while parDirID:
            path=str(self.getDirName(parDirID))+","+path
            parDirID=self.getDirParentID(parDirID)
        return path

    def getCmdPath(self, cmdID):
        """Creates complete command path"""
        path=""
        cmdName=self.getCmdName(cmdID=cmdID)
        parID=self.getCmdParentID(cmdID=cmdID)
        path=self.getDirPath(dirID=parID)+"/"+cmdName
        return path
    
    def getDirPathIDs(self, dirID):
        """Returns list of dir path ids"""
        path=list()
        path.append(dirID)
        parent=self.getDirParentID(dir=dirID)
        while parent:
            path.append(parent)
            parent=self.getDirParentID(dir=parent)     
        return path
    
    def getCmdPathIDs(self, cmdID):
        """Returns list of command path ids"""
        dirID=self.getCmdParentID(cmdID=cmdID)
        path=self.getDirPathIDs(dirID=dirID)
        path.append(cmdID)
        return path
    
    def dbCopy(self, cmdIDs="", dirIDs="", path=""):
        """Copies database entries"""
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