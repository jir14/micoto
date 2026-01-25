import dearpygui.dearpygui as dpg
from db import Database
import api as API

db = Database("db.db")
api = API.Api("10.255.255.255", "admin", "testpass", db)
dpg.create_context()

def apply(sender, app_data, user_data):

    return

def openArgs(sender, app_data, user_data):
    lbl = "new "+str(db.getDirName(user_data[0]))
    uTag = dpg.generate_uuid()
    with dpg.window(label=lbl, tag=uTag, autosize=True, on_close=lambda: dpg.delete_item(uTag)):
        pos = user_data[1]+120
        dpg.set_item_pos(uTag,[pos,0])
        args, vals, help = api.getArgs(user_data[2])
        with dpg.group(horizontal=True, parent=uTag):
            with dpg.group(horizontal=False):
                for arg in args:
                    dpg.add_text(arg, tag=str(user_data[2])+arg)
                    with dpg.tooltip(parent=str(user_data[2])+arg):
                        if len(help[arg])>1:
                            dpg.add_text(help[arg])
                        else:
                            dpg.add_text("You are on your own bro")
            with dpg.group(horizontal=False):
                for val in vals:
                    if len(val)>0:
                        dpg.add_combo(items=val)
                    else:
                        dpg.add_input_text()
            with dpg.group(horizontal=False):
                dpg.add_button(label="apply")
                dpg.add_button(label="cancel", callback=lambda: dpg.delete_item(uTag))
    return

def openCmds(sender, app_data, user_data):
    lbl = db.getDirName(user_data[0])
    uTag = dpg.generate_uuid()
    with dpg.window(label=lbl, tag=uTag, autosize=True, on_close=lambda: dpg.delete_item(uTag)):
        pos = user_data[1]+120
        dpg.set_item_pos(uTag,[pos,0])
        keys, values, ids, help = api.getDir(user_data[0], id=user_data[2])
        with dpg.group(horizontal=True, parent=uTag):
            with dpg.group(horizontal=False):
                for key in keys:
                    dpg.add_text(key)
                    with dpg.tooltip(parent=str(user_data[2])+key):
                        if len(help[key])>1:
                            dpg.add_text(help[key])
                        else:
                            dpg.add_text("You are on your own bro")
            with dpg.group(horizontal=False):
                for vals, id in zip(values, ids):
                    for value in vals:
                        dpg.add_input_text(default_value=value)
            dpg.add_text("")

def openDirWindow(sender, app_data, user_data):
    lbl = db.getDirName(user_data[0])
    uTag = dpg.generate_uuid()
    with dpg.window(label=lbl, tag=uTag, autosize=True, on_close=lambda: dpg.delete_item(uTag)):
        pos = user_data[1]+120
        dpg.set_item_pos(uTag,[pos,0])
        with dpg.group(horizontal=True, parent=uTag):
            with dpg.group(horizontal=False):
                recs = db.getDirDirsIDs(user_data[0])
                help = api.getSyntax(db.printDirPath(user_data[0], spacer=","))
                if len(recs)!=0:
                    for rec in recs:
                        lbl=db.getDirName(rec)
                        dpg.add_button(label=lbl, user_data=(rec, pos), callback=openDirWindow, tag=str(user_data[0])+lbl)
                        with dpg.tooltip(parent=str(user_data[0])+lbl):
                            if len(help[lbl])>1:
                                dpg.add_text(help[lbl])
                            else:
                                dpg.add_text("You are on your own bro")
                dpg.add_text("")
            with dpg.group(horizontal=False):
                keys, values, ids, help = api.getDir(user_data[0])
                for cmd in db.getDirCmdsIDs(user_data[0]):
                    dpg.add_button(label=db.getCmdName(cmd)[0], callback=openArgs, user_data=(user_data[0], pos, cmd))
            with dpg.group(horizontal=False):
                with dpg.table(header_row=True, policy=dpg.mvTable_SizingFixedFit, hideable=True):
                    for key in keys:
                        dpg.add_table_column(label=key)
                    for vals, id in zip(values, ids):
                        with dpg.table_row():
                            for value in vals:
                                dpg.add_selectable(label=value, span_columns=True, user_data=(user_data[0], pos, id))
                dpg.add_text("")
    return


with dpg.window(tag="Main",label="Main"):
    with dpg.group(horizontal=False, parent="Main", tag="Menu"):
        for id in db.getDirsWithoutParent():
            dpg.add_button(label=db.getDirName(id), user_data=(id, 0), callback=openDirWindow)


dpg.create_viewport(title='Micoto', width=1500, height=1000)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.show_item_registry()
dpg.set_primary_window("Main", True)
dpg.start_dearpygui()
dpg.destroy_context()