import apiros as API

class Api():
    def __init__(self, ip, username, password, db=None):
        self.sk = API.open_socket(ip, 8729, True)
        #self.sk = API.open_socket(ip, 8728, False)
        self.apiros = API.ApiRos(self.sk)
        self.apiros.login(username, password)
        self.db = db

    def getDir(self, dirID="", id="", spacer=",", begin=False, pathDef=""):
        sentence = []
        first = True
        keys = []
        values = []
        ids = []
        if begin:
            path=spacer
        path+=pathDef
        sentence.append(path+spacer+"print")
        for re in self.apiros.talk(sentence):
            if re[0]=="!re":
                #print(re[1])
                if first:
                    for k in re[1].keys():
                        k = k.replace("=","")
                        keys.append(k)
                    first = False
                vals = []
                for rec in re[1].values():
                    vals.append(rec)
                values.append(vals)
        if id:
            val = values[ids.index(id)]
            values = []
            values.append(val)
            ids = [id]
        help=self.getSyntax(path=path)
        return keys, values, ids, help

    def getArgs(self, dirID="", cmd=""):
        sentence=[]
        argVals=dict()
        dir = self.db.printDirPath(dirID, spacer=",")
        path=dir+","+cmd
        sentence.append("/console/inspect")
        sentence.append("=request=child")
        sentence.append("=path="+path)
        for re in self.apiros.talk(sentence):
            if re[0]=="!re":
                if re[1]["=type"]!="child":
                    continue
                arg=re[1]["=name"]
                argVals[arg]=self.getCompletetions(path=path, arg=arg)
        help=self.getSyntax(path=path)
        return argVals, help


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
        for re in self.apiros.talk(sentence):
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
        for re in self.apiros.talk(sentence):
            if re[0]=="!re":
                if re[1]["=symbol-type"]=="explanation":
                    symbol=re[1]["=symbol"]
                    symbol=symbol.replace("<", "").replace(">", "")
                    answer[symbol]=re[1]["=text"]
        return answer

    def checkValues(self, dirID="", cmdName="", argVals="", spacer="/"):
        sentence=[]
        answer=dict()
        dir = self.db.printDirPath(dirID, spacer=spacer)
        path=spacer+dir+spacer+cmdName
        sentence.append(path)
        for arg, val in argVals.items():
            sentence.append("="+arg+"="+str(val))
        for re in self.apiros.talk(sentence):
            #print(re)
            if re[0]=="!re":
                continue
            elif re[0]=="!trap":
                answer["message"]=re[1]["=message"].replace("=", "")
        return answer