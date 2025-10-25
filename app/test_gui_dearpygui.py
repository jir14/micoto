import dearpygui.dearpygui as dpg
from db import Database

db = Database("db.db")

dpg.create_context()

def openCmdWindow(user_data):
    lbl = db.getDirName(user_data)   
    with dpg.window(label=lbl, width=300, height=500):
        dpg.add_text("state data/options")
    return

def openDirWindow(sender, app_data, user_data):
    dirs = db.getDirDirs(user_data)
    lbl = db.getDirName(user_data)
    if not dirs:
        openCmdWindow(user_data)
        return
    with dpg.window(label=lbl, width=300, height=500):
        for rec in dirs:
            if rec =="":
                continue
            dpg.add_button(label=rec[0], user_data=db.getDirID(rec[0]), callback=openDirWindow)

with dpg.window(tag="Menu",label="Menu", width=200, height=500):
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
dpg.destroy_context()"""