import dearpygui.dearpygui as dpg
from db import Database
import api as API

dpg.create_context()

class Treeview:
    def __init__(self, dbName, ipAddress, username, password):
        self.db = Database(dbName)
        self.api = API.Api(ipAddress, username, password, self.db)
        self.dirsToDB=dict()
        self.cmdsToDB=dict()
        with dpg.window(tag="Menu", label="Menu", width=500):
            dpg.add_button(label="Save as", callback=self.createDB)
            dpg.show_item_registry()
            with dpg.group(tag="mainTag", parent="Menu"):
                for dirID in self.db.getDirsWithoutParent():
                    with dpg.group(horizontal=True, tag="sectionTag"+str(dirID), parent="Menu"):
                        dirName = self.db.getDirName(dirID)
                        if dirName=="":
                            continue
                        dpg.add_checkbox(parent="sectionTag"+str(dirID), callback=self.dirCallback, user_data=dirID)
                        with dpg.group(horizontal=False, parent="sectionTag"+str(dirID), tag="sectionHorizontalTag"+str(dirID)):
                            dpg.add_collapsing_header(tag="dir"+str(dirID), label=dirName, parent="sectionHorizontalTag"+str(dirID))
                            self.loop(dirID) 
    
    def createDB(self, sender, appdata, userdata):
        print(self.dirsToDB)
        print(self.cmdsToDB)
        for key, val in zip(self.dirsToDB.keys(), self.dirsToDB.values()):
            if val:
                print(self.db.getDirPathIDs(key))
        for key, val in zip(self.cmdsToDB.keys(), self.cmdsToDB.values()):
            if val:
                print(self.db.getCmdPathIDs(key))
        return

    def cmdCallback(self, sender, appdata, userdata):
        value=dpg.get_value(sender)
        if userdata not in self.cmdsToDB.keys():
            self.cmdsToDB[userdata] = True
            return
        self.cmdsToDB[userdata]=value
        return

    def dirCallback(self, sender, appdata, userdata):
        value=dpg.get_value(sender)
        cmds = dpg.get_item_children("cmd"+str(userdata))[1]
        if len(cmds)>0:
            for item in cmds:
                self.cmdsToDB[dpg.get_item_alias(item)]=value
                dpg.set_value(item, value)
        recs = dpg.get_item_children("rec"+str(userdata))[1]
        self.dirsToDB[dpg.get_item_alias(sender)[5:]]=value
        if len(recs)>0:
            for item in recs:
                dpg.set_value(item+1, value)
                self.dirsToDB[dpg.get_item_alias(item+1)[5:]]=value
                self.dirCallback(sender=item+1, appdata=appdata, userdata=dpg.get_item_user_data(item+1))
        return

    def loop(self, dirID):
        dirid=str(dirID)
        with dpg.group(horizontal=False, parent="dir"+dirid, tag="group"+dirid):
            cmds = self.db.getDirCmds(dirID)
            with dpg.group(horizontal=True, parent="group"+dirid, tag="cmd"+dirid):
                if len(cmds)>0:
                    for cmd in self.db.getDirCmdsIDs(dirID):
                        cmdName=self.db.getCmdName(cmd)
                        if cmd=="":
                            continue
                        dpg.add_checkbox(label=cmdName, tag=str(cmd), parent="cmd"+dirid, callback=self.cmdCallback, user_data=cmd)

            recs = self.db.getDirDirsIDs(dirID)
            with dpg.group(horizontal=False, parent="group"+dirid, tag="rec"+dirid):
                if len(recs)>0:
                    for rec in recs:
                        dirName=self.db.getDirName(rec)
                        with dpg.group(horizontal=True, parent="rec"+dirid, tag="rec"+dirid+dirName):
                            dpg.add_checkbox(tag="check"+str(rec), parent="rec"+dirid+dirName, callback=self.dirCallback, user_data=rec)
                            dpg.add_tree_node(tag="dir"+str(rec), label=dirName, parent="rec"+dirid+dirName)
                        self.loop(rec)
        return

tree=Treeview("db.db", "10.255.255.255", "admin", "testpass")

dpg.create_viewport(title='Micoto', width=1500, height=1000)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Menu", True)
dpg.start_dearpygui()
dpg.destroy_context()