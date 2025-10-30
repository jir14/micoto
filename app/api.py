import apiros as API

class Api():
    def __init__(self, ip, username, password, db=None):
        self.sk = API.open_socket(ip, 8729, True)
        #self.sk = API.open_socket(ip, 8728, False)
        self.api = API.ApiRos(self.sk)
        self.api.login(username, password)
        self.db = db

    def printDir(self, dirID, id=None, bID=None):
        sentence = []
        sentence.append(self.db.printDirPath(dirID, bID)+"/print")
        first = True
        keys = []
        values = []
        ids = []
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
    
    def getAvailableInterfaces(self):
        sentence = []
        sentence.append("/interface/print")
        first = True
        keys = []
        values = []
        ids = []
        print(self.api.talk(sentence))