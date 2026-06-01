from api.apiros import *
from db.db import Database
import sys, ast

class ApiCommands():
    def __init__(self, ip, username, password, database):
        """Initialises ApiCommands object"""
        self.sk = open_socket(ip, 8729, True)
        """Opens socket"""
        self.api = ApiRos(self.sk)
        """Sets ApiRos"""
        self.api.login(username, password)
        """Performes ApiRos login"""
        self.db = database
        """Sets command database file"""

    def filter(self, output):
        """Filters output"""
        filtered = []
        for re in output:
             if re[0] == '!re':
                if re[1]["=type"] == "self":
                     continue
                filtered.append(re[1])
        return filtered

    def requestOne(self, re, type):
        """Helper - filters defined record type"""
        answer = []
        for r in re:
            if r["=node-type"] == type:
                answer.append(r["=name"])
        return answer

    def requestSome(self, path="", type=""):
        """Returns `child` items"""
        sentence = []
        sentence.append("/console/inspect")
        sentence.append("=request=child")
        sentence.append("=path="+path)
        out = self.api.talk(sentence)
        out = self.filter(out)
        return self.requestOne(out, type)
    
    def dirLoop(self, higherID=""):
        """Helper - loops through directories"""
        path=self.db.getDirPath(higherID)
        self.addCmds(path=path, dirID=higherID)
        dirs=self.requestSome(path=path, type="dir")+self.requestSome(path=path, type="path")
        for dir in dirs:
            id=self.db.insertDir(dir, higherID)
            self.dirLoop(id)
        return
    
    def addCmds(self, path="", dirID=""):
        """Adds available commands to database (add, set, remove, etc...)"""
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
        """Starts scan"""
        dirs=self.requestSome(type="dir")+self.requestSome(type="path")
        for dir in dirs:
            id=self.db.insertDir(dir, higherID=False)
            self.dirLoop(id)
        return

def main(dbFile="default-commands.db", devIp="", device=""):
    """Main"""
    db = Database(dbFile, create=True)
    """Sets command database object"""
    dev = ast.literal_eval(device)
    """Type conversion (string &rarr dictionary)"""
    api = ApiCommands(devIp, list(dev.keys())[0], list(dev.values())[0].decode(), db)
    """Sets ApiCommands object"""
    api.scan()
    """Runs command scan"""


if __name__ == '__main__':
	main(sys.argv[1], sys.argv[2], sys.argv[3])