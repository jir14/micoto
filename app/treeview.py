import dearpygui.dearpygui as dpg
from db import Database
import api as API

db = Database("db.db")
api = API.Api("10.255.255.255", "admin", "testpass", db)
dpg.create_context()

def loop(dirID):
    dirid=str(dirID)
    with dpg.group(horizontal=False, parent="dir"+str(dirID), tag="group"+dirid):
        cmds = db.getDirCmds(dirID)
        if len(cmds)>0:
            with dpg.group(horizontal=True, parent="dir"+str(dirID), tag="cmd"+dirid):
                dpg.add_text(dirID)
                for cmd in db.getDirCmds(dirID):
                    if cmd=="":
                        continue
                    dpg.add_checkbox(label=cmd, parent="cmd"+dirid)

        recs = db.getDirDirsIDs(dirID)
        if len(recs)>0:
            with dpg.group(horizontal=False, parent="group"+dirid, tag="rec"+dirid):
                for rec in recs:
                    dirName=db.getDirName(rec)
                    dpg.add_tree_node(tag="dir"+str(rec), label=str(rec)+" "+str(dirID)+" "+dirName, parent="rec"+dirid, selectable=True)
                    loop(rec)
    return

with dpg.window(tag="Menu", label="Menu", width=500):
    dpg.add_text("pes")
    with dpg.group(tag="mainTag", parent="Menu"):
        for dirID in db.getLevelDirsIDs(0):
            dirName = db.getDirName(dirID)
            if dirName=="":
                continue
            dpg.add_tree_node(tag="dir"+str(dirID), label=dirName, parent="mainTag", selectable=True)
            loop(dirID)    

dpg.create_viewport(title='Micoto', width=1500, height=1000)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Menu", True)
dpg.start_dearpygui()
dpg.destroy_context()