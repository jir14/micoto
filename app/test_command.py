import apiros as API
import db as DB

class ApiCommands():
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
        path=self.db.getDirPath(higherID)
        self.addCmds(path=path, dirID=higherID)
        dirs=self.requestSome(path=path, type="dir")+self.requestSome(path=path, type="path")
        for dir in dirs:
            id=self.db.insertDir(dir, higherID)
            print(path+","+dir)
            self.dirLoop(id)
        return
    
    def addCmds(self, path="", dirID=""):
        cmds=self.requestSome(path=path, type="cmd")
        vals={"add": 0, "set":0, "remove":0, "enable":0, "disable":0, "comment":0}
        for cmd in cmds:
            match cmd:
                case "add":
                    vals["add"]=1
                case "set":
                    vals["set"]=1
                case "remove":
                    vals["remove"]=1
                case "enable":
                    vals["enable"]=1
                case "disable":
                    vals["disable"]=1
                case "comment":
                    vals["comment"]=1
        self.db.insertCmd(dirID, vals)
        return
    
    def scan(self):
        dirs=self.requestSome(type="dir")+self.requestSome(type="path")
        for dir in dirs:
            id=self.db.insertDir(dir, higherID=False)
            self.dirLoop(id)
        return

def main():
    
    db = DB.Database("db.db")
    api = ApiCommands("10.255.255.255", "admin", "testpass", db)

    api.scan()


if __name__ == '__main__':
	main()