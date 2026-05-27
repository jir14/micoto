from db.db import Database
from device import Device

class middleware():
    def __init__(self, cmdDbFile="", devices=dict()):
        """Initialises middleware object"""
        self.db=Database(dbFile=cmdDbFile)
        """Sets command database"""
        self.devList=[]
        """Sets empty list of devices"""
        for devIp, params in devices.items():
            for username, password in params.items():
                self.devList.append(Device(devIp, username, password.decode()))
                """Device initialization"""    
        pass

    def getDirsWithoutParent(self):
        """Calls `db.getDirsWithoutParent`"""
        return self.db.getDirsWithoutParent()
    
    def getDirName(self, dirId=""):
        """Calls `db.getDirName`"""
        return self.db.getDirName(dirID=dirId)
    
    def getDirDirsIDs(self, dirId=""):
        """Calls `db.getDirDirsIDs`"""
        return self.db.getDirDirsIDs(dirID=dirId)
    
    def printDirPath(self, dirId="", spacer=""):
        """Calls `db.printDirPath`"""
        return self.db.printDirPath(dirID=dirId, spacer=spacer)
    
    def getDirCmds(self, dirId=""):
        """Calls `db.getDirCmds`"""
        return self.db.getDirCmds(dirID=dirId)
    
    def getSyntax(self, dirID=""):
        """Calls `api.getSyntax` on first device"""
        try:
            return self.devList[0].api.getSyntax(path=self.printDirPath(dirId=dirID, spacer=","),)
        except:
            raise
        
    def getDirTableData(self, dirId="", id="", spacer="", begin=False):
        """Returns table data"""
        resDict=dict()
        pathDef=self.printDirPath(dirId=dirId, spacer=spacer)
        for dev in self.devList:
            ip=dev.getDevIp()
            try:
                resDict[ip]= dev.api.getDirTableData(id=id, spacer=spacer, begin=begin, pathDef=pathDef)
            except:
                raise
            if "error" in resDict[ip]:
                resDict[ip]=False
            continue
        return resDict

    def getCommon(self, keyVal=""):
        """Returns common items of at least 2 devices"""
        comKeyVal=dict()
        testDev=dict()
        first, second=True, True
        for devIp, devData in keyVal.items():
            if not devData:
                continue
            if first:
                for row in devData:
                    key=(list(row.keys())[1])
                    if row[key] not in testDev.keys():
                        testDev[row[key]]={devIp:[]}
                    testDev[row[key]][devIp].append(row)
                first=False
                continue
            if second:
                for row in devData:
                    if row[key] in testDev.keys():
                        if row[key] not in comKeyVal.keys():
                            comKeyVal[row[key]]=testDev[row[key]]
                            comKeyVal[row[key]][devIp]=[]
                        comKeyVal[row[key]][devIp].append(row)
                second=False
                continue
            for row in devData:
                if row[key] in comKeyVal.keys():
                    if devIp not in comKeyVal[row[key]]:
                        comKeyVal[row[key]][devIp]=[]
                    comKeyVal[row[key]][devIp].append(row)
        return comKeyVal

    def commonFiltered(self, keyVal=""):
        """Returns filtered output of common items `{devIP : [common items]}`"""
        out = dict()
        for ip, vals in keyVal.items():
            out[ip]=[]
            for val in vals:
                if ".id" in val:
                    out[ip].append(val[".id"])
        return out
    
    def getArgs(self, dirId="", cmd="", spacer=","):
        """Calls `api.getArgs` on first device"""
        try:
            return self.devList[0].api.getArgs(cmd, pathDef=self.printDirPath(dirId=dirId, spacer=spacer))
        except:
            raise
    
    def getIpDevices(self):
        """Returns list of IPs"""
        lst=[]
        for dev in self.devList:
            lst.append(dev.getDevIp())
        return lst
    
    def applyToDevices(self, argVals="", dirId="", cmdName="", spacer="/", selected=False):
        """Checkes values and applies changes"""
        pathDef=spacer+self.printDirPath(dirId=dirId, spacer=spacer)+spacer+cmdName
        msgs=dict()
        for devIp, ids in selected.items():
            for r in self.devList:
                if r.getDevIp()==devIp:
                    dev=r
                    break
            argVals=argVals.copy()
            if "interface" not in argVals.keys():
                argVals["numbers"]=",".join(ids)
            try:
                msg = dev.api.checkValues(argVals=argVals, pathDef=pathDef)
            except:
                raise
            if msg and "message" in msg:
                msgs[devIp]=msg["message"]
            else:
                msgs[devIp]="ok"
        return msgs
