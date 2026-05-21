import dearpygui.dearpygui as dpg

class window():
    def __init__(self, dirId="", selected="", pos=0, lbl="", cmd="", argVals=dict()):
        self.dirId = dirId
        self.selected = selected
        self.pos = pos
        self.lbl = lbl
        self.cmd = cmd
        self.argVals = argVals
    
    def getDirId(self):
        return self.dirId
    
    def setDirId(self, dirId):
        self.dirId=dirId
        return True
    
    def getPos(self):
        return self.pos
    
    def setPos(self, pos):
        self.pos=pos
        return True
    
    def getLbl(self):
        return self.lbl
    
    def setLbl(self, lbl=""):
        self.lbl=lbl
        return True
    
    def getCmd(self):
        return self.cmd
    
    def setCmd(self, cmd=""):
        self.cmd=cmd
        return True
    
    def getArgVals(self):
        return self.argVals
    
    def setArgVals(self, argVal):
        for arg, val in argVal.items():
            self.argVals[arg]=val
        return True
    
    def getSelected(self):
        return self.selected
    
    def setSelected(self, sender, app_data, ipId):
        for ip, ids in ipId.items():
            self.selected.keys()
            if ip not in self.selected.keys():
                self.selected[ip]=[]
                for id in ids:
                    self.selected[ip].append(id)
            else:
                for id in ids:
                    if id in self.selected[ip]:
                        self.selected[ip].remove(id)
                        if len(self.selected[ip])==0:
                            del self.selected[ip]
                    else:
                        self.selected[ip].append(id)
        print(self.selected)
    
    def clearSelected(self):
        self.selected=dict()
        return True