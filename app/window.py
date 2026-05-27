class window():
    def __init__(self, dirId="", selected="", pos=0, lbl="", cmd="", argVals=dict(), tableData=False):
        """Initialises window object"""
        self.dirId = dirId
        """Sets dirId"""
        self.selected = selected
        """Sets list of selected items"""
        self.pos = pos
        """Sets position coordinates"""
        self.lbl = lbl
        """Sets window label"""
        self.cmd = cmd
        """Sets used command"""
        self.argVals = argVals
        """Sets `argument : value` dictionary"""
        self.tableData = tableData
        """Sets table data"""
    
    def getDirId(self):
        """Returns dirId"""
        return self.dirId
    
    def setDirId(self, dirId):
        """Sets dirId"""
        self.dirId=dirId
        return True
    
    def getPos(self):
        """Returns position"""
        return self.pos
    
    def setPos(self, pos):
        """Sets position"""
        self.pos=pos
        return True
    
    def getLbl(self):
        """Returns window label"""
        return self.lbl
    
    def setLbl(self, lbl=""):
        """Sets window label"""
        self.lbl=lbl
        return True
    
    def getCmd(self):
        """Returns command"""
        return self.cmd
    
    def setCmd(self, cmd=""):
        """Sets command"""
        self.cmd=cmd
        return True
    
    def getTableData(self):
        """Returns table data"""
        return self.tableData
    
    def setTableData(self, tableData):
        """Sets table data"""
        self.tableData = tableData
        return True
    
    def getArgVals(self):
        """Returns `argument : value` dictionary"""
        return self.argVals
    
    def setArgVals(self, argVal):
        """Sets `argument : value` dictionary"""
        for arg, val in argVal.items():
            self.argVals[arg]=val
        return True

    def clearArgVals(self):
        """Clears `argument : value` dictionary (sets to empty)"""
        self.argVals = dict()
        return True
    
    def getSelected(self):
        """Returns `selected` dictionary"""
        return self.selected
    
    def setSelected(self, sender="", app_data="", ipId=dict()):
        """Adds/removes to/from `selected` dictionary"""
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
    
    def clearSelected(self):
        """Clears `selected` dictionary (sets to empdy)"""
        self.selected=dict()
        return True