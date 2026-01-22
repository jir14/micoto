import dearpygui.dearpygui as dpg
from db import Database
import api as API

db = Database("db.db")
api = API.Api("10.255.255.255", "admin", "testpass", db)
dpg.create_context()

def cmdCallback(sender, appdata, userdata, value):
    
    return

def dirCallback(sender, appdata, userdata):
    value=dpg.get_value(sender)
    cmds = dpg.get_item_children("cmd"+str(userdata))[1]
    if len(cmds)>0:
        for item in cmds:
            dpg.set_value(item, value)
    recs = dpg.get_item_children("rec"+str(userdata))[1]
    if len(recs)>0:
        for item in recs:
            dpg.set_value(item+1, value)
            dirCallback(sender=item+1, appdata=appdata, userdata=dpg.get_item_user_data(item+1))
    return

def loop(dirID):
    dirid=str(dirID)
    with dpg.group(horizontal=False, parent="dir"+dirid, tag="group"+dirid):
        cmds = db.getDirCmds(dirID)
        with dpg.group(horizontal=True, parent="group"+dirid, tag="cmd"+dirid):
            if len(cmds)>0:
                for cmd in db.getDirCmdsIDs(dirID):
                    cmdName=db.getCmdName(cmd)[0]
                    if cmd=="":
                        continue
                    dpg.add_checkbox(label=cmdName, parent="cmd"+dirid, callback=cmdCallback, user_data=cmd)

        recs = db.getDirDirsIDs(dirID)
        with dpg.group(horizontal=False, parent="group"+dirid, tag="rec"+dirid):
            if len(recs)>0:
                for rec in recs:
                    dirName=db.getDirName(rec)
                    with dpg.group(horizontal=True, parent="rec"+dirid, tag="rec"+dirid+dirName):
                        dpg.add_checkbox(parent="rec"+dirid+dirName, callback=dirCallback, user_data=rec)
                        dpg.add_tree_node(tag="dir"+str(rec), label=dirName, parent="rec"+dirid+dirName)
                    loop(rec)
    return

with dpg.window(tag="Menu", label="Menu", width=500):
    dpg.add_text("pes")
    #dpg.show_item_registry()
    with dpg.group(tag="mainTag", parent="Menu"):
        for dirID in db.getDirsWithoutParent():
            with dpg.group(horizontal=True, tag="sectionTag"+str(dirID), parent="Menu"):
                dirName = db.getDirName(dirID)
                if dirName=="":
                    continue
                dpg.add_checkbox(parent="sectionTag"+str(dirID), callback=dirCallback, user_data=dirID)
                with dpg.group(horizontal=False, parent="sectionTag"+str(dirID), tag="sectionHorizontalTag"+str(dirID)):
                    dpg.add_collapsing_header(tag="dir"+str(dirID), label=dirName, parent="sectionHorizontalTag"+str(dirID))
                    loop(dirID)    

dpg.create_viewport(title='Micoto', width=1500, height=1000)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Menu", True)
dpg.start_dearpygui()
dpg.destroy_context()