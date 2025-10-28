import dearpygui.dearpygui as dpg
from db import Database
import api as API

db = Database("db.db")
api = API.Api("10.255.255.255", "admin", "testpass", db)
dpg.create_context()

def openCmdWindow(user_data):
    lbl = db.getDirName(user_data)
    cmds = db.getDirCmds(user_data)
    with dpg.window(label=lbl, tag="window", width=500):
        with dpg.group(horizontal=True):
            with dpg.group(horizontal=False):
                           #width=(dpg.get_item_width("window")-100)
                with dpg.table(header_row=True, policy=dpg.mvTable_SizingFixedFit, hideable=True, resizable=False, width=(dpg.get_item_width("window")-100)):
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

            with dpg.group(horizontal=False, width=100):
                for cmd in cmds:
                    dpg.add_button(label=cmd)
            
    return

def openDirWindow(sender, app_data, user_data):
    dirs = db.getDirDirs(user_data)
    lbl = db.getDirName(user_data)
    if not dirs:
        openCmdWindow(user_data)
        return
    with dpg.window(label=lbl):
        for rec in dirs:
            if rec =="":
                continue
            dpg.add_button(label=rec, user_data=db.getDirID(rec), callback=openDirWindow)

with dpg.window(tag="Menu",label="Menu"):
    for rec in db.getLevelDirs(0):
        if rec =="":
            continue
        dpg.add_button(label=rec, user_data=db.getDirID(rec), callback=openDirWindow)

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