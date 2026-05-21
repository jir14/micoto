import db.db as DB
import device as device

class middleware():
    def __init__(self, cmdDbFile="", devices=dict()):
        self.db=DB.Database(dbFile=cmdDbFile)
        self.devList=[]
        for devIp, params in devices.items():
            for username, password in params.items():
                self.devList.append(device.Device(devIp, username, password.decode()))    
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
        return self.devList[0].api.getSyntax(path=self.printDirPath(dirId=dirID, spacer=","),)
    
    def getDirCmds(self, dirId=""):
        return self.db.getDirCmds(dirID=dirId)
    
    def getDirTableData(self, dirId="", id="", spacer="", begin=False):
        resDict=dict()
        pathDef=self.printDirPath(dirId=dirId, spacer=spacer)
        for dev in self.devList:
            ip=dev.getDevIp()
            resDict[ip]= dev.api.getDirTableData(id=id, spacer=spacer, begin=begin, pathDef=pathDef)
            if "error" in resDict[ip]:
                resDict[ip]=False
            continue
        return resDict

    def getCommon(self, keyVal=""):
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
        out = dict()
        for ip, vals in keyVal.items():
            out[ip]=[]
            for val in vals:
                if ".id" in val:
                    out[ip].append(val[".id"])
        return out


    def getDir(self, dirId="", id="", spacer="", begin=False):
        resDict=dict()
        pathDef=self.printDirPath(dirId=dirId, spacer=spacer)
        for dev in self.devList:
            resDict[dev.getDevIp()]=dev.api.getDirTableData(id=id, spacer=spacer, begin=begin, pathDef=pathDef)
            if bool(resDict[dev.getDevIp()]):
                continue
            resDict[dev.getDevIp()]=False
        return resDict
    
    def getArgs(self, dirId="", cmd="", spacer=","):
        return self.devList[0].api.getArgs(cmd, pathDef=self.printDirPath(dirId=dirId, spacer=spacer))
    
    def checkValues(self, argVals="", dirId="", cmdName="", spacer="/"):
        pathDef=spacer+self.printDirPath(dirId=dirId, spacer=spacer)+spacer+cmdName
        for dev in self.devList:
            msg = dev.api.checkValues(argVals=argVals, pathDef=pathDef)
            if msg and "message" in msg:
                msg["ip"]=dev.getDevIp()
                return msg
        return True
    
    def getIpDevices(self):
        lst=[]
        for dev in self.devList:
            lst.append(dev.getDevIp())
        return lst
    
    def applyToDevices(self, argVals="", dirId="", cmdName="", spacer="/", selected=False):
        pathDef=spacer+self.printDirPath(dirId=dirId, spacer=spacer)+spacer+cmdName
        if selected:
            msgs=dict()
            for devIp, ids in selected.items():
                for r in self.devList:
                    if r.getDevIp()==devIp:
                        dev=r
                        break
                argVals=argVals.copy()
                if "interface" not in argVals.keys():
                    argVals["numbers"]=",".join(ids)
                msg = dev.api.checkValues(argVals=argVals, pathDef=pathDef)
                if msg and "message" in msg:
                    msgs[devIp]=msg["message"]
                else:
                    msgs[devIp]="ok"
        return msgs
