import dearpygui.dearpygui as dpg
from db import Database
import api as API

db = Database("db.db")
api = API.Api("10.255.255.255", "admin", "testpass", db)
dpg.create_context()

def loop(user_data):
    recs = db.getDirDirs(user_data)
    if recs:
        for rec in recs:
            dirID=db.getDirID(rec, higherID=user_data)
            dpg.add_tree_node(tag=dirID, label=rec, parent=user_data)
            loop(dirID)
    return

with dpg.window(tag="Menu",label="Menu"):
    for rec in db.getLevelDirs(0):
        if rec =="":
            continue
        dirID=db.getDirID(rec)
        dpg.add_tree_node(tag=dirID, label=rec)
        loop(user_data=dirID)

dpg.create_viewport(title='Micoto', width=1500, height=1000)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Menu", True)
dpg.start_dearpygui()
dpg.destroy_context()