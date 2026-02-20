import dearpygui.dearpygui as dpg
import middleware as middle

dpg.create_context()

class conf_gui():
    def __init__(self):
        self.middle=middle.middleware()
        with dpg.window(tag="Main",label="Main"):
            with dpg.group(horizontal=False, parent="Main", tag="Menu", width=100):
                with dpg.table(header_row=False):
                    dpg.add_table_column()
                    for dirId in self.middle.getDirsWithoutParent():
                        with dpg.table_row():
                            user_data={"pos":0, "dirId":dirId}
                            #dpg.add_selectable(label=self.middle.getDirName(dirId), user_data=user_data, callback=self.openDirWindow)       
                            dpg.add_button(label=self.middle.getDirName(dirId), user_data=user_data, callback=self.openDirWindow)
        pass

    def openDirWindow(self, sender, app_data, user_data):
        lbl = self.middle.getDirName(user_data["dirId"])
        if dpg.does_item_exist(lbl):
            dpg.focus_item(lbl)
            return
        user_data["tag"]=lbl
        with dpg.window(label=lbl, tag=lbl, autosize=True, on_close=lambda: dpg.delete_item(lbl), user_data=user_data):
            user_data["pos"] = user_data["pos"]+120
            dpg.set_item_pos(lbl ,[user_data["pos"],0])
            keys, values, help = self.middle.getDir(user_data["dirId"], spacer="/", begin=True)
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
                                                dpg.add_button(label=key, user_data=usr_data)
                                                #dpg.add_button(label=key, callback=self.openArgs, user_data=usr_data)
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
                                                #usr_data=user_data.copy()
                                                usr_data["cmd"]=key
                                                if val:
                                                    dpg.add_button(label=key, user_data=usr_data)
                                                    #dpg.add_button(label=key, callback=self.openArgs, user_data=usr_data)
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
                            #usr_data=user_data.copy()
                            user_data["cmd"]=key
                            if val:
                                dpg.add_button(label=key, user_data=user_data)

                with dpg.group(tag=str(user_data["dirId"])+"group"+lbl, horizontal=False, parent=lbl):
                    self.addDirTable(user_data=user_data, lbl=lbl)
                dpg.add_text("")
        return

    def addDirTable(self, user_data, lbl=""):
        itemName=str(user_data["dirId"])+"table"+lbl
        if dpg.does_item_exist(itemName):
            dpg.delete_item(itemName)
        keys, values, help = self.middle.getDir(user_data["dirId"], spacer="/", begin=True)
        if keys:
            with dpg.table(tag=itemName, parent=str(user_data["dirId"])+"group"+lbl, header_row=True, policy=dpg.mvTable_SizingFixedFit, hideable=True):
                for key in keys:
                    dpg.add_table_column(label=key)
                for vals in values:
                    print(vals)
                    user_data["id"]=vals[0]
                    with dpg.table_row():
                        for value in vals:
                            """if "*" in value:
                                dpg.add_selectable(tag=str(value), label=value, span_columns=True, user_data=user_data, callback=self.addDevToList)
                                continue"""
                            dpg.add_selectable(label=value, span_columns=True, user_data=user_data, callback=self.addDevToList)
                return True
        return False

    def onClose(self, sender, app_data, user_data):
        user_data["pos"]-=120
        self.addDirTable(user_data=user_data)
        dpg.delete_item(user_data["tag"])
        return
    
    def addDevToList(self, sender, app_data, user_data):
        print(sender)
        print(app_data)
        print(dpg.get_item_label(sender))
        #user_data["selected"].append()
        return

test=conf_gui()



dpg.create_viewport(title='Micoto', width=1500, height=1000)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.show_item_registry()
dpg.set_primary_window("Main", True)
dpg.start_dearpygui()
dpg.destroy_context()