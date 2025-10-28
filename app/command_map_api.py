import app.apiros as API
import db as DB

class Api():
    def __init__(self, ip, username, password):
        self.sk = API.open_socket(ip, 8729, True)
        #self.sk = API.open_socket(ip, 8728, False)
        self.api = API.ApiRos(self.sk)
        self.api.login(username, password)

    def filter(self, output):
        filtered = []
        for re in output:
             if re[0] == '!re':
                if re[1]["=type"] == "self":
                     continue
                filtered.append(re[1])
        return filtered

    def requestAll(self, *args):
        path = ""
        for arg in args:
            path = path+","+arg
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
    
    def getPath(self, dir):
        path = dir
        while dir:
            dir = self.db.getDirParentName(dir)
            if dir:
                path = dir+","+path
        return path
    
    def requestOne(self, re, type):
        answer = []
        for r in re:
            if r["=node-type"] == type:
                answer.append(r["=name"])
        return answer

    def requestSome(self, path, type):
        sentence = []
        sentence.append("/console/inspect")
        sentence.append("=request=child")
        sentence.append("=path="+path)
        out = self.api.talk(sentence)
        out = self.filter(out)
        return self.requestOne(out, type)

def main():
    api = API.Api("10.255.255.255", "admin", "testpass")
    db = DB.Database("db.db")

    dirs, opts, args = api.requestAll()
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
        dirs = db.getLevelDirs(a-1)
        for dir in dirs:
            path = api.getPath(dir)
            print(path)
            dirss, cmdss, argss = api.requestAll(path)
            db.insertDirs(dirss, a, dir)
            db.insertCommands(dir, cmdss)
            dirID = db.getDirID(dir)
            for cmdd in cmdss:
                argss = api.requestSome(path+","+cmdd, "arg")
                db.insertArgs(cmdd, argss, dirID)
        a=a+1
        

if __name__ == '__main__':
	main()