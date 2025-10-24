import api as API
import db as DB

class Api():
    def __init__(self, ip, username, password):
        self.sk = API.open_socket(ip, 8729, True)
        #self.sk = API.open_socket(ip, 8728, False)
        self.api = API.ApiRos(self.sk)
        self.api.login(username, password)
        self.db = DB.Database("db.db")

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
    api = Api("10.255.255.255", "admin", "testpass")
    db = api.db

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
        



"""


    


    for dir in dirs:   
        dirss, cmdss, argss = api.requestAll(dir)
        db.insertDirs(dirss, 1, db.getDirID(dir))
        db.insertCommands(dir, cmdss)
        for cmdd in cmdss:
            argss = api.requestSome(cmdd, "arg")
            db.insertArgs(cmdd, argss)

    dirs = dirss

    a = 1
    for lvl in db.getLevelDirs(a-1):
        if lvl[0] == "":
            continue
        db.insertDirs(api.requestSome(lvl[0], "dir"), a)

    print("PATHS")
    for path in paths:
        v = api.requestSome(path, "path")
        if len(v)==0:
            continue
        db.insertDirs(v)
    print("DIRS")
    for dir in dirs:
        v = api.requestSome(dir, "dir")
        if len(v)==0:
            continue
        db.insertDirs(v, 0)
    print("CMD")
    for cmd in cmds:
        v = api.requestSome(cmd, "cmd")
        if len(v)==0:
            continue
        print(v)
        db.insertCommands(v)
    print("ARG")
    for arg in args:
        v = api.requestSome(arg, "arg")
        if len(v)==0:
            continue
        print(v)
        db.insertArgs(v)

    #PATH
    paths, dirs, cmds, args = api.requestAll()
    rpaths = []
    rdirs = []
    rcmds = []
    rargs = []
    for path in paths:
        rpaths.append(api.requestSome(path, "path"))
    for dir in dirs:
        rdirs.append(api.requestSome(dir, "dir"))
    for cmd in cmds:
        rcmds.append(api.requestSome(cmd, "cmd"))
    for arg in args:
        rargs.append(api.requestSome(arg, "arg"))
    dir = [rpaths, rdirs, rcmds, rargs]
    if len(cmds)>0:
        db.insert


    paths, dirs, cmds, args = api.requestAll()
    for var in paths:
        print(var.upper())
        vars = api.requestAll(var)
        print("PATH")
        for path in vars[0]:
            print(path)
        print("DIR")
        for dir in vars[1]:
            print(dir)
        print("CMD")
        for cmd in vars[2]:
            print(cmd)
        print("ARG")
        for arg in vars[3]:
            print(arg)




    print("PATHS")
    for var in paths:
        print(var)

    print("DIRS")
    for var in dirs:
        print(var.upper())
        vars = api.requestSome(var, "dir")
        while len(vars)>0:
             for varr in vars:
                print(var+"/"+varr)
                vars = api.requestSome(varr, "dir")
                for cmd in api.requestSome(varr, "cmd"):
                    print(var+"/"+varr+"/"+cmd)
                    for arg in api.requestSome(cmd, "arg"):
                        print(var+"/"+varr+"/"+cmd+" "+arg)
"""

    #for cmd in cmds:
    #    sentence = []
    #    sentence.append("/console/inspect")
    #    sentence.append("=request=child")
    #    sentence.append("=path="+cmd)
    #    out = api.api.talk(sentence)
    #    out = api.filter(out)
    #    args = api.requestArgs(out)
    #    print(cmd, args)

    #api.api.writeSentence(sentence)
    #print(api.apiRead())

if __name__ == '__main__':
	main()