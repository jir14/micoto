import dearpygui.dearpygui as dpg
from db import Database
import api as API

db = Database("db.db")
api = API.Api("10.255.255.255", "admin", "testpass", db)
dpg.create_context()

def selectedRow(sender, app_data, user_data):
    lbl = db.getDirName(user_data[1])
    uTag = dpg.generate_uuid()
    with dpg.window(label=lbl, tag=uTag, autosize=True):
        with dpg.group(horizontal=False): 
            with dpg.group(horizontal=False):
                with dpg.table(header_row=True, policy=dpg.mvTable_SizingFixedFit, hideable=True):
                    keys, values, ids = api.printDir(user_data[1], user_data[2], bID=user_data[0])
                    for key in keys:
                        dpg.add_table_column(label=key)
                    for vals, id in zip(values, ids):
                        with dpg.table_row():
                            for value in vals:
                                dpg.add_input_text(default_value=value)
                                #dpg.add_selectable(label=value, span_columns=True, user_data=(user_data, id))
    return

def openDirWindow(sender, app_data, user_data):
    lbl = db.getDirName(user_data[1])
    uTag = dpg.generate_uuid()
    with dpg.window(label=lbl, tag=uTag):
        dpg.set_item_pos(uTag,[120,0])
        with dpg.group(horizontal=True):
            with dpg.group(horizontal=False):
                dpg.add_text("Dirs")
                dirs = db.getDirDirs(user_data[1], user_data[0])
                for rec in dirs:
                    if rec =="":
                        continue
                    dpg.add_button(label=rec, user_data=(user_data[0], db.getDirID(rec)), callback=openDirWindow)
            with dpg.group(horizontal=False):
                with dpg.table(header_row=True, policy=dpg.mvTable_SizingFixedFit, hideable=True):
                    if user_data[0] == user_data[1]:
                        keys, values, ids = api.printDir(user_data[1])
                    else:
                        keys, values, ids = api.printDir(user_data[1], bID=user_data[0])
                    for key in keys:
                        dpg.add_table_column(label=key)
                    for vals, id in zip(values, ids):
                        with dpg.table_row():
                            for value in vals:
                                dpg.add_selectable(label=value, span_columns=True, callback=selectedRow, user_data=(user_data[0], user_data[1], id))
    return

with dpg.window(tag="Menu",label="Menu"):
    for rec in db.getLevelDirs(0):
        if rec =="":
            continue
        dpg.add_button(label=rec, user_data=(db.getDirID(rec), 0), callback=openDirWindow)

dpg.create_viewport(title='Micoto', width=1500, height=1000)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Menu", True)
dpg.start_dearpygui()
dpg.destroy_context()






"""dpg.create_context()

def callback(sender, app_data, user_data):
    print("Sender: ", sender)
    print("App Data: ", app_data)

with dpg.file_dialog(directory_selector=False, show=False, callback=callback, id="file_dialog_id", width=700 ,height=400):
    dpg.add_file_extension(".*")
    dpg.add_file_extension(".db", color=(255, 0, 255, 255), custom_text="[DB file]")

with dpg.window(label="DB file select", width=400, height=300):
    dpg.add_button(label="File Selector", callback=lambda: dpg.show_item("file_dialog_id"))

dpg.create_viewport(title='Micoto', width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()

        with dpg.table(header_row=True, policy=dpg.mvTable_SizingFixedFit):
            first = True
            for re in api.printDir(user_data):
                if re[0]=="!re":
                    if first:
                        for k in re[1].keys():
                            k = k.replace("=","")
                            if k == ".id":
                                continue
                            dpg.add_table_column(label=k)
                        first = False
                    with dpg.table_row():
                        for rec in re[1].values():
                            if "*" in rec:
                                continue
                            dpg.add_text(rec)

                            """
"""
                    first = True
                    for re in api.printDir(user_data):
                        if re[0]=="!re":
                            if first:
                                for k in re[1].keys():
                                    k = k.replace("=","")
                                    if k == ".id":
                                        continue
                                    dpg.add_table_column(label=k)
                                first = False
                            with dpg.table_row():
                                item_id = 0
                                for rec in re[1].values():
                                    print(rec)
                                    if "*" in rec:
                                        item_id = rec.replace("*","")
                                        continue
                                    dpg.add_selectable(label=rec, span_columns=True, callback=openArgWindow, user_data=(user_data, cmds, item_id, re))"""

"""def changeValue(sender, app_data, user_data):
    with dpg.window():
        dpg.add_text()
    return

def openArgWindow(sender, app_data, user_data):
    lbl = db.getDirName(user_data[1])
    cmds = db.getDirCmds(user_data[1])
    uTag = dpg.generate_uuid()
    with dpg.window(label=lbl, tag=uTag, autosize=True):
        with dpg.group(horizontal=False): 
            with dpg.group(horizontal=False):
                with dpg.table(header_row=True, policy=dpg.mvTable_SizingFixedFit, hideable=True):
                    keys, values, ids = api.printDir(user_data[1], user_data[0])
                    for key in keys:
                        dpg.add_table_column(label=key)
                    for vals, id in zip(values, ids):
                        with dpg.table_row():
                            for value in vals:
                                dpg.add_selectable(label=value, span_columns=True, callback=changeValue, user_data=(user_data, id))
            with dpg.group(horizontal=True):
                for cmd in cmds:
                    dpg.add_button(label=cmd) 

def openCmdWindow(user_data):
    lbl = db.getDirName(user_data[1])
    cmds = db.getDirCmds(user_data[1])
    uTag = dpg.generate_uuid()
    with dpg.window(label=lbl, width=500, tag=uTag):
        dpg.set_item_pos(uTag, [240, 0])
        with dpg.group(horizontal=True):
            with dpg.group(horizontal=False, width=100):
                for cmd in cmds:
                    dpg.add_button(label=cmd) 
            with dpg.group(horizontal=False):
                           #width=(dpg.get_item_width("window")-100)
                with dpg.table(header_row=True, policy=dpg.mvTable_SizingFixedFit, hideable=True):
                    keys, values, ids = api.printDir(user_data[1], bID=user_data[0])
                    for key in keys:
                        dpg.add_table_column(label=key)
                    for vals, id in zip(values, ids):
                        with dpg.table_row():
                            for value in vals:
                                dpg.add_selectable(label=value, span_columns=True, callback=openArgWindow, user_data=(user_data[0], user_data, id)) 



def openDirWindow(sender, app_data, user_data):
    dirs = db.getDirDirs(user_data[1], user_data[0])
    lbl = db.getDirName(user_data[1])
    uTag = dpg.generate_uuid()
    if not dirs:
        openCmdWindow(user_data)
        return
    with dpg.window(label=lbl, tag=uTag):
        dpg.set_item_pos(uTag, [120, 0])
        for rec in dirs:
            if rec =="":
                continue
            dpg.add_button(label=rec, user_data=(user_data[0], db.getDirID(rec)), callback=openDirWindow)

        with dpg.group(horizontal=False):
                           #width=(dpg.get_item_width("window")-100)
                with dpg.table(header_row=True, policy=dpg.mvTable_SizingFixedFit, hideable=True):
                    keys, values, ids = api.printDir(user_data[1], user_data[0])
                    for key in keys:
                        dpg.add_table_column(label=key)
                    for vals, id in zip(values, ids):
                        with dpg.table_row():
                            for value in vals:
                                dpg.add_selectable(label=value, span_columns=True, callback=openArgWindow, user_data=(user_data, id)) """