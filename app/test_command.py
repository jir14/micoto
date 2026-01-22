import apiros as API
import db as DB

class Api():
    def __init__(self, ip, username, password, database):
        self.sk = API.open_socket(ip, 8729, True)
        #self.sk = API.open_socket(ip, 8728, False)
        self.api = API.ApiRos(self.sk)
        self.api.login(username, password)
        self.db = database

    def filter(self, output):
        filtered = []
        for re in output:
             if re[0] == '!re':
                if re[1]["=type"] == "self":
                     continue
                filtered.append(re[1])
        return filtered

    def requestAll(self, path=""):
        sentence = []
        paths = []
        dirs = []
        cmds = []
        args = [] 
        sentence.append("/console/inspect")
        sentence.append("=request=child")
        sentence.append("=path="+path)
        out = self.api.talk(sentence)
        out = self.filter(out)
        paths = self.requestOne(out, "path")
        dirs = self.requestOne(out, "dir")
        cmds = self.requestOne(out, "cmd")
        args = self.requestOne(out, "arg")
        for path in paths:
            dirs.append(path)
        return dirs, cmds, args
    
    def getPath(self, dirId):
        path=str(self.db.getDirName(dirId))
        dirId=self.db.getDirParentID(dirId)
        while dirId:
            path=str(self.db.getDirName(dirId))+","+path
            dirId=self.db.getDirParentID(dirId)
        return path

    def requestOne(self, re, type):
        answer = []
        for r in re:
            if r["=node-type"] == type:
                answer.append(r["=name"])
        return answer

    def requestSome(self, path="", type=""):
        sentence = []
        sentence.append("/console/inspect")
        sentence.append("=request=child")
        sentence.append("=path="+path)
        out = self.api.talk(sentence)
        out = self.filter(out)
        return self.requestOne(out, type)
    
    def dirLoop(self, higherID=""):
        path=self.getPath(higherID)
        dirs=self.requestSome(path=path, type="dir")+self.requestSome(path=path, type="path")
        for dir in dirs:
            id=self.db.insertDir(dir, higherID)
            print(path+","+dir)
            self.addCmds(path=path+","+dir, dirID=id)
            self.dirLoop(id)
        return
    
    def addCmds(self, path="", dirID=""):
        cmds=self.requestSome(path=path, type="cmd")
        cmds=self.filterCmds(cmds)
        for cmd in cmds:
            self.db.insertCmds(dirID, cmd)
        return
    
    def scan(self):
        dirs=self.requestSome(type="dir")+self.requestSome(type="path")
        for dir in dirs:
            id=self.db.insertDir(dir, higherID=False)
            self.addCmds(dirID=id)
            self.dirLoop(id)
        return
    
    def filterCmds(self, cmds):
        out=[]
        for cmd in cmds:
            out.append(self.db.filterCmds(cmd))
        return out

def main():
    
    db = DB.Database("db.db")
    api = Api("10.255.255.255", "admin", "testpass", db)

    api.scan()


    


    """dirs, opts, args = api.requestAll()
    db.insertDirs(dirs, 0, None, False)
    cmds = []
    for var in cmds:
        if db.filterOptions(var):
            continue
        cmds.append(var)

    db.insertCommands("", cmds)
    for cmd in cmds:
        args = api.requestSome(cmd, "arg")
        db.insertArgs(cmd, args)

    for dir in dirs:
        path = api.getPath(dir)
        print(path)
        dirss, cmdss, argss = api.requestAll(path)
        db.insertDirs(dirss, 1, dir)
        db.insertCommands(dir, cmdss)
        for cmdd in cmdss:
            argss = api.requestSome(path+cmdd, "arg")
            db.insertArgs(cmdd, argss)

    a=2
    while a<10:
        dirs, bids = db.getLevelDirs(a-1, True)
        for dir, bid in zip(dirs, bids):
            path = api.getPath(dir, bid)
            print(path)
            dirss, cmdss, argss = api.requestAll(path)
            db.insertDirs(dirss, a, dir)
            db.insertCommands(dir, cmdss)
            dirID = db.getDirID(dir, bid=bid)
            for cmdd in cmdss:
                argss = api.requestSome(path+","+cmdd, "arg")
                db.insertArgs(cmdd, argss, dirID)
        a=a+1
        """
        

if __name__ == '__main__':
	main()