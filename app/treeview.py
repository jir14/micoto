import dearpygui.dearpygui as dpg
from db import Database
import app.api_old as API
import os

dpg.create_context()

class Treeview:
    def __init__(self, dbName):
        self.db = Database(dbName)
        self.dirsToDB=dict()
        self.cmdsToDB=dict()
        with dpg.window(tag="Menu", label="Menu", width=500):
            dpg.add_button(label="Save as", callback=self.createDBWindow)
            dpg.show_item_registry()
            for dirID in self.db.getDirsWithoutParent():
                with dpg.group(horizontal=True, tag="sectionTag"+str(dirID), parent="Menu"):
                    dirName = self.db.getDirName(dirID)
                    if dirName=="":
                        continue
                    dpg.add_checkbox(tag="check"+dirName, parent="sectionTag"+str(dirID), callback=self.dirCallback, user_data=dirID)
                    with dpg.group(horizontal=False, parent="sectionTag"+str(dirID), tag="sectionHorizontalTag"+str(dirID)):
                        dpg.add_collapsing_header(tag="dir"+str(dirID), label=dirName, parent="sectionHorizontalTag"+str(dirID))
                        self.loop(dirID) 
    
    def createDBlists(self, sender, appdata, userdata):
        dirsCopy=self.dirsToDB.copy()
        for key, val in dirsCopy.items():
            if val:
                if key=="":
                    continue
                for rec in self.db.getDirPathIDs(key):
                    self.dirsToDB[rec]=True
        return

    def createDBWindow(self, sender, appdata, userdata):
        with dpg.file_dialog(directory_selector=False, modal=True, callback=self.fileSelect, show=True, id="file_dialog_id", width=700 , height=400, cancel_callback=lambda: dpg.delete_item("file_dialog_id")):
            dpg.add_file_extension("", color=(150, 255, 150, 255))
            dpg.add_file_extension(".db", color=(255, 0, 255, 255), custom_text="[DB file]")
        return

    def fileSelect(self, sender, app_data, user_data):
        filePath=app_data["file_path_name"]
        if os.path.exists(filePath):
            try:
                os.remove(filePath)
            except Exception as e:
                with dpg.window(width=500):
                    dpg.add_text("Error writing DB file")
                    dpg.add_text(e, wrap=450)
                    dpg.delete_item("file_dialog_id")
                return
        Database(filePath)
        self.createDBlists(sender, app_data, user_data)
        self.db.dbCopy(cmdIDs=self.cmdsToDB, dirIDs=self.dirsToDB, path=filePath)
        dpg.delete_item(item="file_dialog_id")
        return

    def cmdCallback(self, sender, appdata, userdata):
        value=dpg.get_value(sender)
        self.dirRootLoop(dirId=userdata, value=value)
        if userdata not in self.cmdsToDB.keys():
            self.cmdsToDB[userdata] = {dpg.get_item_label(sender): value}
            return
        self.cmdsToDB[userdata][dpg.get_item_label(sender)]=value
        return

    def dirCallback(self, sender, appdata, userdata):
        value=dpg.get_value(sender)
        cmds = dpg.get_item_children("cmd"+str(userdata))[1]
        if len(cmds)>0:
            for item in cmds:
                if userdata not in self.cmdsToDB.keys():
                    self.cmdsToDB[userdata]={}
                self.cmdsToDB[userdata][dpg.get_item_label(item=item)] = value
                dpg.set_value(item, value)
        recs = dpg.get_item_children("rec"+str(userdata))[1]
        if len(recs)>0:
            for item in recs:
                self.dirsToDB[int(dpg.get_item_alias(item+1)[5:])]=value
                dpg.set_value(item+1, value)
                self.dirCallback(sender=item+1, appdata=appdata, userdata=dpg.get_item_user_data(item+1))
        self.dirRootLoop(dirId=userdata, value=value)
        return

    def dirRootLoop(self, dirId="", value=""):
        par=int(dirId)
        while par:
            self.dirsToDB[par]=value
            par=self.db.getDirParentID(par)
        return
    
    def loop(self, dirID):
        dirid=str(dirID)
        with dpg.group(horizontal=False, parent="dir"+dirid, tag="group"+dirid):
            cmds = self.db.getDirCmds(dirID)
            with dpg.group(horizontal=True, parent="group"+dirid, tag="cmd"+dirid):
                if len(cmds)>0:
                    for key, val in cmds.items():
                        if val:
                            dpg.add_checkbox(label=key, tag="checkCmd"+dirid+str(key), parent="cmd"+dirid, callback=self.cmdCallback, user_data=dirid)

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

tree=Treeview("db.db")

dpg.create_viewport(title='Micoto', width=1500, height=1000)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Menu", True)
dpg.start_dearpygui()
dpg.destroy_context()