import dearpygui.dearpygui as dpg
import os, sys
from db.db import Database
from EditThemePlugin import EditThemePlugin

class Treeview:
    def __init__(self, dbName):
        """Initialises tree view window object"""
        self.db = Database(dbName)
        """Sets command database object"""
        self.dirsToDB=dict()
        """Sets list of dirs to be added to new database file"""
        self.cmdsToDB=dict()
        """Sets list of commands to be added to new database file"""

        self.dbTest()
        """Calls `dbTest` function"""

        dpg.create_context()
        with dpg.window(tag="Menu", label="Menu", width=500):
            with dpg.menu_bar():
                with dpg.menu(label="Theme"):
                    EditThemePlugin()
                    dpg.add_menu_item(label="Fonts", callback=lambda: dpg.show_font_manager())
            dpg.add_button(label="Save as", callback=self.createDBWindow)
            for dirID in self.db.getDirsWithoutParent():
                with dpg.group(horizontal=True, tag="sectionTag"+str(dirID), parent="Menu"):
                    dirName = self.db.getDirName(dirID)
                    if dirName=="":
                        continue
                    dpg.add_checkbox(tag="check"+dirName, parent="sectionTag"+str(dirID), callback=self.dirCallback, user_data=dirID)
                    with dpg.group(horizontal=False, parent="sectionTag"+str(dirID), tag="sectionHorizontalTag"+str(dirID)):
                        dpg.add_collapsing_header(tag="dir"+str(dirID), label=dirName, parent="sectionHorizontalTag"+str(dirID))
                        self.loop(dirID) 
        
        dpg.create_viewport(title='Micoto', width=1500, height=1000)
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.set_primary_window("Menu", True)
        dpg.start_dearpygui()
        dpg.destroy_context()
    
    def dbTest(self):
        """Calls `db.checkCmdFile` function"""
        e = self.db.checkCmdFile()
        if e!=True:
            return

    def createDBlists(self, sender, appdata, userdata):
        """Copies selected items to new database"""
        dirsCopy=self.dirsToDB.copy()
        for key, val in dirsCopy.items():
            if val:
                if key=="":
                    continue
                for rec in self.db.getDirPathIDs(key):
                    self.dirsToDB[rec]=True
        return

    def createDBWindow(self, sender, appdata, userdata):
        """Opens new database file dialog"""
        with dpg.file_dialog(directory_selector=False, modal=True, callback=self.fileSelect, show=True, id="file_dialog_id", width=700 , height=400, cancel_callback=lambda: dpg.delete_item("file_dialog_id")):
            dpg.add_file_extension("", color=(150, 255, 150, 255))
            dpg.add_file_extension(".db", color=(255, 0, 255, 255), custom_text="[DB file]")
        return

    def fileSelect(self, sender, app_data, user_data):
        """Processes db file (checks and file creation)"""
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
        Database(filePath, create=True)
        self.createDBlists(sender, app_data, user_data)
        self.db.dbCopy(cmdIDs=self.cmdsToDB, dirIDs=self.dirsToDB, path=filePath)
        dpg.delete_item(item="file_dialog_id")
        return

    def cmdCallback(self, sender, appdata, userdata):
        """Helper - tracking selected commands"""
        value=dpg.get_value(sender)
        self.dirRootLoop(dirId=userdata, value=value)
        if userdata not in self.cmdsToDB.keys():
            self.cmdsToDB[userdata] = {dpg.get_item_label(sender): value}
            return
        self.cmdsToDB[userdata][dpg.get_item_label(sender)]=value
        return

    def dirCallback(self, sender, appdata, userdata):
        """Helper - tracking selected dirs"""
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
        """Helper - loops through selected subdirs (root)"""
        par=int(dirId)
        while par:
            self.dirsToDB[par]=value
            par=self.db.getDirParentID(par)
        return
    
    def loop(self, dirID):
        """Helper - loops through selected subdirs"""
        dirid=str(dirID)
        with dpg.group(horizontal=False, parent="dir"+dirid, tag="group"+dirid):
            cmds = self.db.getDirCmds(dirID)
            with dpg.group(horizontal=True, parent="group"+dirid, tag="cmd"+dirid):
                if cmds:
                    for key, val in cmds.items():
                        if val:
                            dpg.add_checkbox(label=key, tag="checkCmd"+dirid+str(key), parent="cmd"+dirid, callback=self.cmdCallback, user_data=dirid)

            recs = self.db.getDirDirsIDs(dirID)
            with dpg.group(horizontal=False, parent="group"+dirid, tag="rec"+dirid):
                if recs:
                    for rec in recs:
                        dirName=self.db.getDirName(rec)
                        with dpg.group(horizontal=True, parent="rec"+dirid, tag="rec"+dirid+dirName):
                            dpg.add_checkbox(tag="check"+str(rec), parent="rec"+dirid+dirName, callback=self.dirCallback, user_data=rec)
                            dpg.add_tree_node(tag="dir"+str(rec), label=dirName, parent="rec"+dirid+dirName)
                        self.loop(rec)
        return



if __name__ == "__main__":
    tree=Treeview(sys.argv[1])
    
