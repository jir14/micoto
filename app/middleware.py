import apiros as apiros
import db as DB
import api_old as api_old

class middleware():
    def __init__(self, cmdDbFile="", devList=""):
        #self.db=DB.Database(dbFile=cmdDbFile)
        #self.api=api.api()
        self.db=DB.Database("db.db")
        self.api=api_old.Api(ip="10.255.255.255", username="admin", password="testpass")
        self.devs=devList
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
        keys, values, ids, help = self.api.getDir(dirID=dirId, id=id, spacer=spacer, begin=begin, pathDef=self.printDirPath(dirId=dirId, spacer=spacer))
        print(keys)
        if keys:
            return keys, values, ids, help
        return False, False, False, False