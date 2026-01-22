import dearpygui.dearpygui as dpg
from db import Database
import api as API

db = Database("db.db")
api = API.Api("10.255.255.255", "admin", "testpass", db)
dpg.create_context()

def openAdd(sender, app_data, user_data):
    lbl = "new "+str(db.getDirName(user_data[0]))
    uTag = dpg.generate_uuid()
    with dpg.window(label=lbl, tag=uTag, width=400):
        pos = user_data[1]+120
        dpg.set_item_pos(uTag,[pos,0])
        args = db.getDirAddArgs(user_data[0])
        for arg in args:
            dpg.add_text(arg)
    return

def openCmds(sender, app_data, user_data):
    lbl = db.getDirName(user_data[0])
    uTag = dpg.generate_uuid()
    with dpg.window(label=lbl, tag=uTag, autosize=True):
        pos = user_data[1]+120
        dpg.set_item_pos(uTag,[pos,0])
        keys, values, ids = api.printDir(user_data[0], id=user_data[2])
        with dpg.group(horizontal=True):
            with dpg.group(horizontal=False):
                for key in keys:
                    dpg.add_text(key)
            with dpg.group(horizontal=False):
                for vals, id in zip(values, ids):
                    for value in vals:
                        dpg.add_input_text(default_value=value)
            dpg.add_text("")

def openDirWindow(sender, app_data, user_data):
    lbl = db.getDirName(user_data[0])
    uTag = dpg.generate_uuid()
    with dpg.window(label=lbl, tag=uTag, width=400, horizontal_scrollbar=True):
        pos = user_data[1]+120
        dpg.set_item_pos(uTag,[pos,0])
        with dpg.group(horizontal=True):
            dpg.add_text("")
            with dpg.group(horizontal=False):
                recs = db.getDirDirs(user_data[0])
                if len(recs)!=0:
                    for rec in recs:
                        dirID=db.getDirID(rec, higherID=user_data[0])
                        dpg.add_button(label=rec, user_data=(dirID, pos), callback=openDirWindow)
            dpg.add_text("")
            with dpg.group(horizontal=False):
                keys, values, ids = api.printDir(user_data[0])
                if len(values)!=0:
                    dpg.add_button(label="add", callback=openAdd, user_data=(user_data[0], pos))
                with dpg.table(header_row=True, policy=dpg.mvTable_SizingFixedFit, hideable=True):
                    keys, values, ids = api.printDir(user_data[0])
                    for key in keys:
                        dpg.add_table_column(label=key)
                    for vals, id in zip(values, ids):
                        with dpg.table_row():
                            for value in vals:
                                dpg.add_selectable(label=value, span_columns=True, callback=openCmds, user_data=(user_data[0], pos, id))

with dpg.window(tag="Menu",label="Menu"):
    for rec in db.getDirsWithoutParent():
        if rec =="":
            continue
        dpg.add_button(label=rec, user_data=(db.getDirID(rec), 0), callback=openDirWindow)

dpg.create_viewport(title='Micoto', width=1500, height=1000)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Menu", True)
dpg.start_dearpygui()
dpg.destroy_context()