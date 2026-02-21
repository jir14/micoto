import dearpygui.dearpygui as dpg
import middleware as middle

dpg.create_context()

class conf_gui():
    def __init__(self):
        self.middle=middle.middleware()
        with dpg.window(tag="Main",label="Main"):
            with dpg.group(horizontal=False, parent="Main", tag="Menu", width=100, height=dpg.get_item_height("Main")):
                with dpg.table(header_row=False):
                    dpg.add_table_column()
                    for dirId in self.middle.getDirsWithoutParent():
                        with dpg.table_row():
                            user_data={"pos":0, "dirId":dirId}       
                            dpg.add_button(label=self.middle.getDirName(dirId), user_data=user_data, callback=self.openDirWindow)
        pass

    def openDirWindow(self, sender, app_data, user_data):
        lbl = self.middle.getDirName(user_data["dirId"])
        if dpg.does_item_exist(lbl):
            dpg.focus_item(lbl)
            return
        user_data["tag"]=lbl
        with dpg.window(label=lbl, tag=lbl, width=1000, autosize=True, on_close=self.onClose, user_data=user_data):
            user_data["pos"] = user_data["pos"]+120
            dpg.set_item_pos(lbl ,[user_data["pos"],0])
            keys, values, help, error = self.middle.getDir(user_data["dirId"], spacer="/", begin=True)
            recs = self.middle.getDirDirsIDs(user_data["dirId"])
            if keys and recs:
                with dpg.group(horizontal=True):
                    help = self.middle.getSyntax(user_data["dirId"])
                    with dpg.tab_bar():
                        usr_data=user_data.copy()
                        usr_data["dirId"]=user_data["dirId"]
                        with dpg.tab(label=lbl, user_data=usr_data, tag=str(user_data["dirId"])+lbl):
                            with dpg.group(horizontal=False, parent=str(user_data["dirId"])+lbl):
                                with dpg.group(horizontal=True):
                                    cmds = self.middle.getDirCmds(user_data["dirId"])
                                    if cmds:
                                        for key, val in cmds.items():
                                            usr_data=user_data.copy()
                                            usr_data["cmd"]=key
                                            if val:
                                                dpg.add_button(label=key, callback=self.openCmds, user_data=usr_data)
                                with dpg.group(tag=str(user_data["dirId"])+"group"+lbl, horizontal=False, parent=str(user_data["dirId"])+lbl):
                                    self.addDirTable(user_data=usr_data, lbl=lbl)
                            
                        for rec in recs:
                            lbl=self.middle.getDirName(rec)
                            usr_data=user_data.copy()
                            usr_data["dirId"]=rec
                            with dpg.tab(label=lbl, user_data=usr_data, tag=str(usr_data["dirId"])+lbl, no_tooltip=True):
                                with dpg.group(horizontal=False, parent=str(usr_data["dirId"])+lbl):
                                    with dpg.group(horizontal=True):
                                        cmds = self.middle.getDirCmds(usr_data["dirId"])
                                        if cmds:
                                            for key, val in cmds.items():
                                                usr_data["cmd"]=key
                                                if val:
                                                    dpg.add_button(label=key, callback=self.openCmds, user_data=usr_data)
                                    with dpg.group(tag=str(usr_data["dirId"])+"group"+lbl, horizontal=False, parent=str(usr_data["dirId"])+lbl):
                                        self.addDirTable(user_data=usr_data)

                            with dpg.tooltip(parent=str(usr_data["dirId"])+lbl):
                                if len(help[lbl])>1:
                                    dpg.add_text(help[lbl])
                        
            else:
                recs = self.middle.getDirDirsIDs(user_data["dirId"])
                if recs:
                    with dpg.group(horizontal=False):
                        help = self.middle.getSyntax(user_data["dirId"])
                        for rec in recs:
                            lbl=self.middle.getDirName(rec)
                            usr_data=user_data.copy()
                            usr_data["dirId"]=rec
                            dpg.add_button(label=lbl, user_data=usr_data, callback=self.openDirWindow, tag=str(user_data["dirId"])+lbl)
                            with dpg.tooltip(parent=str(user_data["dirId"])+lbl):
                                if len(help[lbl])>1:
                                    dpg.add_text(help[lbl])
                                else:
                                    dpg.add_text("You are on your own bro")

                with dpg.group(horizontal=True, parent=lbl):
                    cmds = self.middle.getDirCmds(user_data["dirId"])
                    if cmds:
                        for key, val in cmds.items():
                            usr_data=user_data.copy()
                            usr_data["cmd"]=key
                            if val:
                                dpg.add_button(label=key, callback=self.openCmds, user_data=usr_data)
                        with dpg.group(tag=str(user_data["dirId"])+"group"+lbl, horizontal=False, parent=lbl):
                            self.addDirTable(user_data=user_data, lbl=lbl)
                dpg.add_text("")
        return
    
    def openCmds(self, sender, app_data, user_data):
        lbl = "new "+self.middle.getDirName(user_data["dirId"])
        uTag = dpg.generate_uuid()
        usr_data=user_data.copy()
        usr_data["selected"]=[]

        if dpg.does_item_exist(str(user_data["dirId"])+"table"+str(user_data["tag"])):
            table=dpg.get_item_children(str(user_data["dirId"])+"table"+str(user_data["tag"]))[1]
            for r in table:
                if dpg.get_value(dpg.get_item_children(r)[1][0]):
                    usr_data["selected"].append(dpg.get_item_label(dpg.get_item_children(r)[1][0]))

        usr_data["tag"]=uTag
        usr_data[uTag]=dict()
        with dpg.window(label=lbl, tag=uTag, autosize=True, on_close=self.onClose, user_data=usr_data):
            usr_data["pos"] = usr_data["pos"]+120
            dpg.set_item_pos(uTag,[usr_data["pos"],0])
            all, help = self.middle.getArgs(dirId=usr_data["dirId"], cmd=usr_data["cmd"])
            args=all.keys()
            vals=all.values()
            with dpg.group(horizontal=True, parent=uTag):
                with dpg.group(horizontal=False):
                    with dpg.table(header_row=False, policy=dpg.mvTable_SizingFixedFit, width=500):
                        dpg.add_table_column()
                        dpg.add_table_column(width_stretch=True)
                        for arg, val in zip(args, vals):
                            with dpg.table_row():
                                dpg.add_text(arg, tag=str(uTag)+str(usr_data["cmd"])+arg)
                                with dpg.tooltip(parent=str(uTag)+str(usr_data["cmd"])+arg):
                                    if len(help[arg])>1:
                                        dpg.add_text(help[arg])
                                    else:
                                        dpg.add_text("You are on your own bro")
                                if len(val)>0:
                                    dpg.add_combo(tag=str(uTag)+str(usr_data["cmd"])+arg+"text", items=val, callback=self.addToArgVals, user_data=(usr_data, arg))
                                else:
                                    dpg.add_input_text(tag=str(uTag)+str(usr_data["cmd"])+arg+"text", width=200, callback=self.addToArgVals, user_data=(usr_data, arg))
                                if arg=="numbers" and len(usr_data["selected"])>0:
                                    dpg.configure_item(str(uTag)+str(usr_data["cmd"])+arg+"text", default_value=','.join(usr_data["selected"]))
                                    usr_data[uTag]["numbers"]=dpg.get_value(str(uTag)+str(usr_data["cmd"])+arg+"text")
                    
                        with dpg.table_row():
                            dpg.add_text("test:")
                            dpg.add_text(default_value="fill in the required fields", tag=str(uTag)+str(usr_data["cmd"])+"message", wrap=150)
            
                with dpg.group(horizontal=False):
                    dpg.add_button(label="apply", callback=self.apply, user_data=usr_data)
                    dpg.add_button(label="cancel", callback=self.onClose, user_data=usr_data)
        return

    def addDirTable(self, user_data, lbl=""):
        itemName=str(user_data["dirId"])+"table"+lbl
        if dpg.does_item_exist(itemName):
            dpg.delete_item(itemName)
        keys, values, help, error = self.middle.getDir(user_data["dirId"], spacer="/", begin=True)
        if error:
            dpg.add_text(error, tag=itemName, parent=str(user_data["dirId"])+"group"+lbl)
            return False
        if keys:
            with dpg.table(tag=itemName, parent=str(user_data["dirId"])+"group"+lbl, header_row=True, policy=dpg.mvTable_SizingFixedFit, hideable=True):
                for key in keys:
                    dpg.add_table_column(label=key)
                for vals in values:
                    with dpg.table_row():
                        for value in vals:
                            if "*" in value:
                                dpg.add_selectable(label=value, span_columns=True)
                                continue
                            dpg.add_selectable(label=value, span_columns=True)
            return True
        return False

    def apply(self, sender, app_data, user_data):
        cmdName=user_data["cmd"]
        argVals=user_data[user_data["tag"]]
        check=self.middle.checkValues(dirId=user_data["dirId"], cmdName=cmdName, argVals=argVals)
        if "message" in check:
            dpg.set_value(item=str(user_data["tag"])+cmdName+"message", value=list(check.values())[0])
        else:
            dpg.set_value(item=str(user_data["tag"])+cmdName+"message", value="ok")
            self.onClose(sender=self,app_data=app_data,user_data=user_data)
            argVals["numbers"]=[]
        return

    def onClose(self, sender, app_data, user_data):
        user_data["pos"]-=120
        self.addDirTable(user_data=user_data, lbl=self.middle.getDirName(user_data["dirId"]))
        dpg.delete_item(user_data["tag"])
        return

    def addToArgVals(self, sender, app_data, user_data):
        arg=user_data[1]
        user_data=user_data[0]
        user_data[user_data["tag"]][arg]=app_data
        return

test=conf_gui()



dpg.create_viewport(title='Micoto', width=1500, height=1000)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.show_item_registry()
dpg.set_primary_window("Main", True)
dpg.start_dearpygui()
dpg.destroy_context()