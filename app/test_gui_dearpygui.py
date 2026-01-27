import dearpygui.dearpygui as dpg
from db import Database
import api as API

db = Database("db.db")
api = API.Api("10.255.255.255", "admin", "testpass", db)
dpg.create_context()

def requiredFields(sender, app_data, user_data):
    cmdID=user_data[0][2]
    error=api.checkValue(cmdID=cmdID, value=app_data, arg=user_data[1])
    if error:
        dpg.set_value(item=str(cmdID)+"message", value=list(error.values())[0])
    else:
        dpg.set_value(item=str(cmdID)+"message", value="ok")
    return

def apply(sender, app_data, user_data):

    return

def openArgs(sender, app_data, user_data):
    lbl = "new "+str(db.getDirName(user_data[1]))
    uTag = dpg.generate_uuid()
    with dpg.window(label=lbl, tag=uTag, autosize=True, on_close=lambda: dpg.delete_item(uTag)):
        pos = user_data[0]+120
        dpg.set_item_pos(uTag,[pos,0])
        args, vals, help = api.getArgs(user_data[2])
        with dpg.group(horizontal=True, parent=uTag):
            with dpg.group(horizontal=False):
                with dpg.table(header_row=False, policy=dpg.mvTable_SizingFixedFit, width=500):
                    dpg.add_table_column()
                    dpg.add_table_column(width_stretch=True)
                    for arg, val, hlp in zip(args, vals, help):
                        with dpg.table_row():
                            dpg.add_text(arg, tag=str(user_data[2])+arg)
                            with dpg.tooltip(parent=str(user_data[2])+arg):
                                if len(hlp)>1:
                                    dpg.add_text(hlp)
                                else:
                                    dpg.add_text("You are on your own bro")
                            if len(val)>0:
                                dpg.add_combo(tag=str(user_data[2])+arg+"text", items=val, callback=requiredFields, user_data=(user_data, arg))
                            else:
                                dpg.add_input_text(tag=str(user_data[2])+arg+"text", width=200, callback=requiredFields, user_data=(user_data, arg))
                
                    with dpg.table_row():
                        dpg.add_text("test:")
                        dpg.add_text(default_value="ok", tag=str(user_data[2])+"message", wrap=150)
           
            with dpg.group(horizontal=False):
                dpg.add_button(label="apply")
                dpg.add_button(label="cancel", callback=lambda: dpg.delete_item(uTag))
    return

def openCmds(sender, app_data, user_data):
    lbl = db.getDirName(user_data[1])
    uTag = dpg.generate_uuid()
    with dpg.window(label=lbl, tag=uTag, autosize=True, on_close=lambda: dpg.delete_item(uTag)):
        pos = user_data[0]+120
        dpg.set_item_pos(uTag,[pos,0])
        keys, values, ids, help = api.getDir(user_data[1], id=user_data[2])
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
    lbl = db.getDirName(user_data[1])
    uTag = dpg.generate_uuid()
    with dpg.window(label=lbl, tag=uTag, autosize=True, on_close=lambda: dpg.delete_item(uTag)):
        pos = user_data[0]+120
        dpg.set_item_pos(uTag,[pos,0])
        with dpg.group(horizontal=True, parent=uTag):
            with dpg.group(horizontal=False):
                recs = db.getDirDirsIDs(user_data[1])
                help = api.getSyntax(db.printDirPath(user_data[1], spacer=","))
                if len(recs)!=0:
                    for rec in recs:
                        lbl=db.getDirName(rec)
                        dpg.add_button(label=lbl, user_data=(pos, rec), callback=openDirWindow, tag=str(user_data[1])+lbl)
                        with dpg.tooltip(parent=str(user_data[1])+lbl):
                            if len(help[lbl])>1:
                                dpg.add_text(help[lbl])
                            else:
                                dpg.add_text("You are on your own bro")
                dpg.add_text("")
            with dpg.group(horizontal=False):
                keys, values, ids, help = api.getDir(user_data[1])
                for cmd in db.getDirCmdsIDs(user_data[1]):
                    dpg.add_button(label=db.getCmdName(cmd)[0], callback=openArgs, user_data=(pos, user_data[1], cmd))
            with dpg.group(horizontal=False):
                with dpg.table(header_row=True, policy=dpg.mvTable_SizingFixedFit, hideable=True):
                    for key in keys:
                        dpg.add_table_column(label=key)
                    for vals, id in zip(values, ids):
                        with dpg.table_row():
                            for value in vals:
                                dpg.add_selectable(label=value, span_columns=True, user_data=(pos, user_data[1], id))
                dpg.add_text("")
    return


with dpg.window(tag="Main",label="Main"):
    with dpg.group(horizontal=False, parent="Main", tag="Menu"):
        for id in db.getDirsWithoutParent():
            dpg.add_button(label=db.getDirName(id), user_data=(0, id), callback=openDirWindow)


dpg.create_viewport(title='Micoto', width=1500, height=1000)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.show_item_registry()
dpg.set_primary_window("Main", True)
dpg.start_dearpygui()
dpg.destroy_context()