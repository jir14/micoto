import dearpygui.dearpygui as dpg
from db import Database
import api as API

db = Database("penis.db")
#db = Database("db.db")
api = API.Api("10.255.255.255", "admin", "testpass", db)
dpg.create_context()

def addDirTable(user_data):
    itemName=str(user_data["dirId"])+"table"
    if dpg.does_item_exist(itemName):
        dpg.delete_item(itemName)
    keys, values, ids, help = api.getDir(user_data["dirId"], spacer="/", begin=True)
    a=0
    with dpg.table(tag=itemName, parent=str(user_data["dirId"])+"group", header_row=True, policy=dpg.mvTable_SizingFixedFit, hideable=True):
        for key in keys:
            dpg.add_table_column(label=key)
        for vals in values:
            user_data["id"]=vals[0]
            vals[0]=a
            a+=1
            with dpg.table_row():
                for value in vals:
                    dpg.add_selectable(label=value, span_columns=True, user_data=user_data)
    return

def onClose(sender, app_data, user_data):
    user_data["pos"]-=120
    addDirTable(user_data=user_data)
    dpg.delete_item(user_data["tag"])
    return

def addToArgVals(sender, app_data, user_data):
    arg=user_data[1]
    user_data=user_data[0]
    user_data[user_data["tag"]][arg]=app_data
    return

def apply(sender, app_data, user_data):
    cmdID=user_data["cmd"]
    argVals=user_data[user_data["tag"]]
    check=api.checkValues(cmdID=cmdID, argVals=argVals)
    #print(check)
    if "message" in check:
        dpg.set_value(item=user_data["tag"]+str(cmdID)+"message", value=list(check.values())[0])
    else:
        dpg.set_value(item=user_data["tag"]+str(cmdID)+"message", value="ok")
        addDirTable(user_data=user_data)
        dpg.delete_item(user_data["tag"])
    if "id" in check:
        print(check["id"])
    return

def openArgs(sender, app_data, user_data):
    lbl = "new "+str(db.getDirName(user_data["dirId"]))
    uTag = str(dpg.generate_uuid())
    user_data=user_data.copy()
    user_data["tag"]=uTag
    user_data[uTag]=dict()
    with dpg.window(label=lbl, tag=uTag, autosize=True, on_close=onClose, user_data=user_data):
        user_data["pos"] = user_data["pos"]+120
        dpg.set_item_pos(uTag,[user_data["pos"],0])
        all, help = api.getArgs(user_data["cmd"])
        args=all.keys()
        vals=all.values()
        with dpg.group(horizontal=True, parent=uTag):
            with dpg.group(horizontal=False):
                with dpg.table(header_row=False, policy=dpg.mvTable_SizingFixedFit, width=500):
                    dpg.add_table_column()
                    dpg.add_table_column(width_stretch=True)
                    for arg, val in zip(args, vals):
                        with dpg.table_row():
                            dpg.add_text(arg, tag=uTag+str(user_data["cmd"])+arg)
                            with dpg.tooltip(parent=uTag+str(user_data["cmd"])+arg):
                                if len(help[arg])>1:
                                    dpg.add_text(help[arg])
                                else:
                                    dpg.add_text("You are on your own bro")
                            if len(val)>0:
                                dpg.add_combo(tag=uTag+str(user_data["cmd"])+arg+"text", items=val, callback=addToArgVals, user_data=(user_data, arg))
                            else:
                                dpg.add_input_text(tag=uTag+str(user_data["cmd"])+arg+"text", width=200, callback=addToArgVals, user_data=(user_data, arg))
                
                    with dpg.table_row():
                        dpg.add_text("test:")
                        dpg.add_text(default_value="fill in the required fields", tag=uTag+str(user_data["cmd"])+"message", wrap=150)
           
            with dpg.group(horizontal=False):
                dpg.add_button(label="apply", callback=apply, user_data=user_data)
                dpg.add_button(label="cancel", callback=lambda: dpg.delete_item(uTag))
    return

def openCmds(sender, app_data, user_data):
    lbl = db.getDirName(user_data["dirId"])
    uTag = dpg.generate_uuid()
    with dpg.window(label=lbl, tag=uTag, autosize=True, on_close=onClose, user_data=user_data):
        user_data["pos"] = user_data["pos"]+120
        dpg.set_item_pos(uTag,[user_data["pos"],0])
        keys, values, ids, help = api.getDir(user_data["dirId"], id=user_data["id"])
        with dpg.group(horizontal=True, parent=uTag):
            with dpg.group(horizontal=False):
                for key in keys:
                    dpg.add_text(key)
                    with dpg.tooltip(parent=str(user_data["id"])+key):
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
    lbl = db.getDirName(user_data["dirId"])
    if dpg.does_item_exist(lbl):
        dpg.focus_item(lbl)
        return
    user_data["tag"]=lbl
    with dpg.window(label=lbl, tag=lbl, autosize=True, on_close=onClose, user_data=user_data):
        user_data["pos"] = user_data["pos"]+120
        dpg.set_item_pos(lbl ,[user_data["pos"],0])
        with dpg.group(horizontal=True, parent=lbl):
            with dpg.group(horizontal=False):
                recs = db.getDirDirsIDs(user_data["dirId"])
                help = api.getSyntax(db.printDirPath(user_data["dirId"], spacer=","))
                if len(recs)!=0:
                    for rec in recs:
                        lbl=db.getDirName(rec)
                        usr_data=user_data.copy()
                        usr_data["dirId"]=rec
                        dpg.add_button(label=lbl, user_data=usr_data, callback=openDirWindow, tag=str(user_data["dirId"])+lbl)
                        with dpg.tooltip(parent=str(user_data["dirId"])+lbl):
                            if len(help[lbl])>1:
                                dpg.add_text(help[lbl])
                            else:
                                dpg.add_text("You are on your own bro")
                dpg.add_text("")
            with dpg.group(horizontal=False):
                keys, values, ids, help = api.getDir(user_data["dirId"], spacer="/", begin=True)
                for cmd in db.getDirCmdsIDs(user_data["dirId"]):
                    usr_data=user_data.copy()
                    usr_data["cmd"]=cmd
                    dpg.add_button(label=db.getCmdName(cmd), callback=openArgs, user_data=usr_data)
            with dpg.group(tag=str(user_data["dirId"])+"group", horizontal=False):
                addDirTable(user_data=user_data)
                dpg.add_text("")
    return


with dpg.window(tag="Main",label="Main"):
    with dpg.group(horizontal=False, parent="Main", tag="Menu", width=100):
        with dpg.table(header_row=False):
            dpg.add_table_column()
            for dirId in db.getDirsWithoutParent():
                with dpg.table_row():
                    user_data={"pos":0, "dirId":dirId}
                    #dpg.add_button(label=db.getDirName(dirId), user_data=user_data, callback=openDirWindow)
                    dpg.add_selectable(label=db.getDirName(dirId), user_data=user_data, callback=openDirWindow)


dpg.create_viewport(title='Micoto', width=1500, height=1000)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.show_item_registry()
dpg.set_primary_window("Main", True)
dpg.start_dearpygui()
dpg.destroy_context()