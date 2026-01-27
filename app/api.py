import apiros as API

class Api():
    def __init__(self, ip, username, password, db=None):
        self.sk = API.open_socket(ip, 8729, True)
        #self.sk = API.open_socket(ip, 8728, False)
        self.api = API.ApiRos(self.sk)
        self.api.login(username, password)
        self.db = db

    def getDir(self, dirID="", id=""):
        sentence = []
        first = True
        keys = []
        values = []
        ids = []
        path = self.db.printDirPath(dirID)
        if not path:
            return keys, values, ids
        sentence.append(path+"/print")
        for re in self.api.talk(sentence):
            if re[0]=="!re":
                if first:
                    for k in re[1].keys():
                        k = k.replace("=","")
                        if k == ".id":
                            continue
                        keys.append(k)
                    first = False
                vals = []
                for rec in re[1].values():
                    if "*" in rec:
                        ids.append(rec.replace("*",""))
                        continue
                    vals.append(rec)
                values.append(vals)
        if id:
            val = values[ids.index(id)]
            values = []
            values.append(val)
            ids = [id]
        help=self.getSyntax(path=path)
        return keys, values, ids, help

    def getArgs(self, cmdID=""):
        sentence=[]
        args = []
        values = []
        cmd = self.db.getCmdName(cmdID)[0]
        dirID = self.db.getCmdParentID(cmdID)
        dir = self.db.printDirPath(dirID, spacer=",")
        path=dir+","+cmd
        sentence.append("/console/inspect")
        sentence.append("=request=child")
        sentence.append("=path="+path)
        for re in self.api.talk(sentence):
            if re[0]=="!re":
                vals = []
                if re[1]["=type"]!="child":
                    continue
                args.append(re[1]["=name"])
        for arg in args:
            values.append(self.getCompletetions(path=path, arg=arg))
        help=self.getSyntax(path=path)
        return args, values, help

    def getCompletetions(self, path="", arg=""):
        sentence=[]
        answer=[]
        if arg!="":
            path=path+","+arg
        else:
            path=path
        sentence.append("/console/inspect")
        sentence.append("=request=completion")
        sentence.append("=path="+path)
        for re in self.api.talk(sentence):
            if re[0]=="!re":
                if re[1]["=show"]=="false":
                    continue
                answer.append(re[1]["=completion"])
        return answer
    
    def getSyntax(self, path="", arg=""):
        sentence=[]
        answer=dict()
        if arg!="":
            path=path+","+arg
        else:
            path=path
        sentence.append("/console/inspect")
        sentence.append("=request=syntax")
        sentence.append("=path="+path)
        for re in self.api.talk(sentence):
            if re[0]=="!re":
                if re[1]["=symbol-type"]=="explanation":
                    symbol=re[1]["=symbol"]
                    symbol=symbol.replace("<", "").replace(">", "")
                    answer[symbol]=re[1]["=text"]
        return answer

    def checkValue(self, cmdID="", value="", arg=""):
        sentence=[]
        answer=dict()
        cmd = self.db.getCmdName(cmdID)[0]
        dirID = self.db.getCmdParentID(cmdID)
        dir = self.db.printDirPath(dirID, spacer="/")
        path=dir+"/"+cmd
        sentence.append(path)
        sentence.append("="+arg+"="+str(value))
        sentence.append("=disabled=yes")
        for re in self.api.talk(sentence):
            print(re)
            if re[0]=="!re":
                continue
                #print(re[1])
            if re[0]=="!trap":
                mess=re[1]["=message"]
                mess=mess.replace("=", "")
                answer[mess[0]]=mess
        return answer