import apiros as apiros
import db as DB
import api as api
import api_old as api_old
import device as device

class middleware():
    def __init__(self, cmdDbFile="", devList=""):
        #self.db=DB.Database(dbFile=cmdDbFile)
        #self.api=api.api()
        #self.devs=devList
        self.db=DB.Database("db.db")
        #self.api=api_old.Api(ip="10.255.255.255", username="admin", password="testpass")
        dev=device.device("BC-TEST","10.255.255.255","admin","testpass")
        self.api=api.Api({"10.255.255.255" : dev})
        pass

    def getDirsWithoutParent(self):
        return self.db.getDirsWithoutParent()
    
    def getDirName(self, dirId=""):
        return self.db.getDirName(dirID=dirId)
    
    def getDirDirsIDs(self, dirId=""):
        return self.db.getDirDirsIDs(dirID=dirId)
    
    def printDirPath(self, dirId="", spacer=""):
        return self.db.printDirPath(dirID=dirId, spacer=spacer)
    
    def getSyntax(self, dirID=""):
        return self.api.getSyntax(path=self.printDirPath(dirId=dirID, spacer=","),)
    
    def getDirCmds(self, dirId=""):
        return self.db.getDirCmds(dirID=dirId)
    
    def getDir(self, dirId="", id="", spacer="", begin=False):
        keys, values, help = self.api.getDir(id=id, spacer=spacer, begin=begin, pathDef=self.printDirPath(dirId=dirId, spacer=spacer))
        if keys:
            return keys, values, help
        return False, False, False
    
    def getArgs(self, dirId="", cmd="", spacer=","):
        return self.api.getArgs(cmd, pathDef=self.printDirPath(dirId=dirId, spacer=spacer))
    
    def checkValues(self, argVals="", dirId="", cmdName="", spacer="/"):
        return self.api.checkValues(argVals=argVals, pathDef=spacer+self.printDirPath(dirId=dirId, spacer=spacer)+spacer+cmdName)