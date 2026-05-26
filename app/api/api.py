
class Api():
    def __init__(self, device=""):
        """Initialises Api object"""
        self.apiros=device.getApiros()
        """Creates ROS API connection for device object"""

    def printDir(self, dirID, id=None, bID=None):
        """Calls `print` command in defined directory"""
        sentence = []
        first = True
        keys = []
        values = []
        ids = []
        path = self.db.printDirPath(dirID, bID)
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
        return keys, values, ids
    
    def getDirTableData(self, id="", spacer=",", pathDef="", begin=False):
        """Gets table data from device if available"""
        answer=[]
        path=""
        if begin:
            path=spacer
        path+=pathDef
        for re in self.apiros.talk([path+spacer+"print"]):
            ans=dict()
            if re[0]=="!trap":
                ans["error"]=re[1]["=message"]
                return ans
            if re[0]=="!re":
                for k, v in re[1].items():
                    ans[k.replace("=","")]=v
                answer.append(ans)
        return answer


    def getDir(self, id="", spacer=",", pathDef="", begin=False):
        """Calls `print` command in defined directory + help"""
        sentence = []
        keys = []
        values = []
        help=[]
        path=""
        error=False
        if begin:
            path=spacer
        path+=pathDef
        sentence.append(path+spacer+"print")
        for re in self.apiros.talk(sentence):
            if re[0]=="!trap":
                return keys, values, [], re[1]
            if re[0]=="!re":
                for k in re[1].keys():
                    k = k.replace("=","")
                    if k not in keys:
                        k = k.replace("=","")
                        keys.append(k)
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
        return keys, values, help, error


    def getArgs(self, cmd="", pathDef=""):
        """Returns available arguments of the command"""
        sentence=[]
        argVals=dict()
        path=pathDef+","+cmd
        sentence.append("/console/inspect")
        sentence.append("=request=child")
        sentence.append("=path="+path)
        for re in self.apiros.talk(sentence):
            if re[0]=="!re":
                if re[1]["=type"]!="child":
                    continue
                arg=re[1]["=name"]
                argVals[arg]=self.getCompletions(path=path, arg=arg)
        help=self.getSyntax(path=path)
        return argVals, help


    def getCompletions(self, path="", arg=""):
        """Returns available completetions of the command"""
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
        """Returns syntax of the command"""
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

    def checkValues(self, argVals="", pathDef=""):
        """Tries to apply changes, returns error messages"""
        sentence=[]
        answer=dict()
        sentence.append(pathDef)
        for arg, val in argVals.items():
            sentence.append("="+arg+"="+str(val))
        for re in self.apiros.talk(sentence):
            if re[0]=="!re":
                continue
            elif re[0]=="!trap":
                answer["message"]=re[1]["=message"].replace("=", "")
        return answer
    
    def getDevName(self):
        """Returns device identity"""
        for re in self.apiros.talk(["/system/identity/print"]):
            if re[0]=="!re":
                return re[1]["=name"]
        return