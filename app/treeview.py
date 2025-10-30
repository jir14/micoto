import dearpygui.dearpygui as dpg
from db import Database
import api as API

db = Database("db.db")
api = API.Api("10.255.255.255", "admin", "testpass", db)
dpg.create_context()

with dpg.window(tag="Menu",label="Menu"):
    for rec in db.getLevelDirs(0):
        if rec =="":
            continue
        dpg.add_tree_node(tag=db.getDirID(rec), label=rec)
    dirID=1
    while dirID<10:
        recs, bids = db.getLevelDirs(dirID, True)
        for rec, bid in zip(recs, bids):
            if rec =="":
                continue
            dpg.add_tree_node(tag=db.getDirID(rec, bid), label=rec, parent=db.getDirParentID(rec, bid))
        dirID+=1

dpg.create_viewport(title='Micoto', width=1500, height=1000)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Menu", True)
dpg.start_dearpygui()
dpg.destroy_context()