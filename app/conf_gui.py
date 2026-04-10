import dearpygui.dearpygui as dpg
import middleware as middle
import ast as ast
import sys
import os.path as paths
from EditThemePlugin import EditThemePlugin

class conf_gui():
    def __init__(self, cmdDbPath="" , devs=""):
        dpg.create_context()

        with dpg.font_registry():
            #default_font=dpg.add_font("../themes/OpenSans.ttf", 15*2)
            default_font=dpg.add_font("./themes/Roboto.ttf", 15*2)
            dpg.set_global_font_scale(0.5)
        dpg.bind_font(default_font)

        devices=ast.literal_eval(devs)        
        self.middle=middle.middleware(cmdDbFile=cmdDbPath, devices=devices)
        with dpg.window(label="Main") as MainWindow:
            
            #EditThemePlugin()
            
            with dpg.group(horizontal=False, parent=MainWindow, tag="Menu", width=100, height=dpg.get_item_height(MainWindow)):
                with dpg.table(header_row=False):
                    dpg.add_table_column()
                    for dirId in self.middle.getDirsWithoutParent():
                        with dpg.table_row():
                            user_data={"pos":0, "dirId":dirId}       
                            dpg.add_button(label=self.middle.getDirName(dirId), user_data=user_data, callback=self.openDirWindow)
        name=", ".join(list(devices.keys()))
        
        with dpg.theme() as GlobalTheme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 10, 10)
                dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 10, 2)
                dpg.add_theme_style(dpg.mvStyleVar_CellPadding, 4, 2)
                dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 10, 4)
                dpg.add_theme_style(dpg.mvStyleVar_ItemInnerSpacing, 10, 2)
                dpg.add_theme_style(dpg.mvStyleVar_GrabMinSize, 20)
                dpg.add_theme_style(dpg.mvStyleVar_WindowBorderSize, 1)
                dpg.add_theme_style(dpg.mvStyleVar_PopupBorderSize, 1)
                dpg.add_theme_style(dpg.mvStyleVar_FrameBorderSize, 0.5)
                dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 12)
                dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 12)
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 12)
                dpg.add_theme_style(dpg.mvStyleVar_PopupRounding, 12)
                dpg.add_theme_style(dpg.mvStyleVar_ScrollbarRounding, 12)
                dpg.add_theme_style(dpg.mvStyleVar_GrabRounding, 12)
                dpg.add_theme_style(dpg.mvStyleVar_TabRounding, 12)
                dpg.add_theme_style(dpg.mvStyleVar_WindowTitleAlign, 0.5, 0.5)
                dpg.add_theme_style(dpg.mvStyleVar_TableAngledHeadersTextAlign, 0.5, 0.5)
                dpg.add_theme_style(dpg.mvStyleVar_ButtonTextAlign, 0.5, 0.5)

        dpg.bind_theme(GlobalTheme)
        
        dpg.show_style_editor()
        

        dpg.create_viewport(title='Micoto - configure '+name, width=1500, height=1000)
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.show_item_registry()
        dpg.set_primary_window(MainWindow, True)
        dpg.start_dearpygui()
        dpg.destroy_context()

    def openDirWindow(self, sender, app_data, user_data):
        lbl = self.middle.printDirPath(user_data["dirId"], spacer="/")
        if dpg.does_item_exist(lbl):
            dpg.focus_item(lbl)
            return
        user_data["tag"]=lbl
        user_data["selected"]=dict()
        with dpg.window(label=lbl, tag=lbl, width=1000, autosize=True, on_close=self.onClose, user_data=user_data, no_resize=False):
            user_data["pos"] = user_data["pos"]+120
            dpg.set_item_pos(lbl ,[user_data["pos"],0])
            data=self.middle.getDirTableData(user_data["dirId"], spacer="/", begin=True)
            recs=self.middle.getDirDirsIDs(user_data["dirId"])
            if not all(value == False for value in data.values()):
                with dpg.group(horizontal=True):
                    help = self.middle.getSyntax(user_data["dirId"])
                    with dpg.tab_bar():
                        with dpg.tab(label=self.middle.getDirName(user_data["dirId"]), tag=str(user_data["dirId"])+lbl):
                            with dpg.group(horizontal=False, parent=str(user_data["dirId"])+lbl):
                                with dpg.group(horizontal=True):
                                    cmds = self.middle.getDirCmds(user_data["dirId"])
                                    if cmds:
                                        for key, val in cmds.items():
                                            usr_data=user_data.copy()
                                            usr_data["cmd"]=key
                                            if val:
                                                dpg.add_button(label=key, callback=self.openCmds, user_data=usr_data)
                                with dpg.group(tag=str(usr_data["dirId"])+"group"+usr_data["tag"], horizontal=False, parent=str(usr_data["dirId"])+lbl):
                                    self.addDirTable(user_data=usr_data)
                        if recs:
                            for rec in recs:
                                lbl=self.middle.printDirPath(rec, spacer="/")
                                dirName=self.middle.getDirName(rec)
                                usr_data=user_data.copy()
                                usr_data["tag"]=lbl
                                usr_data["dirId"]=rec
                                with dpg.tab(label=dirName, tag=str(usr_data["dirId"])+lbl, no_tooltip=True):
                                    with dpg.group(horizontal=False, parent=str(usr_data["dirId"])+lbl):
                                        with dpg.group(horizontal=True):
                                            cmds = self.middle.getDirCmds(usr_data["dirId"])
                                            if cmds:
                                                for key, val in cmds.items():
                                                    usr_data["cmd"]=key
                                                    if val:
                                                        dpg.add_button(label=key, callback=self.openCmds, user_data=usr_data)
                                        with dpg.group(tag=str(usr_data["dirId"])+"group"+usr_data["tag"], horizontal=False, parent=str(usr_data["dirId"])+lbl):
                                            self.addDirTable(user_data=usr_data)

                                with dpg.tooltip(parent=str(usr_data["dirId"])+lbl):
                                    if len(help[dirName])>1:
                                        dpg.add_text(help[dirName])
                        
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
                                match key:
                                    case "add":
                                        dpg.add_button(label=key, callback=self.addWindow, user_data=usr_data)
                                    case _:
                                        dpg.add_button(label=key, callback=self.openCmds, user_data=usr_data)
                        with dpg.group(tag=str(user_data["dirId"])+"group"+user_data["tag"], horizontal=False, parent=lbl):
                            self.addDirTable(user_data=user_data)
                dpg.add_text("")
        return

    def openCmds(self, sender, app_data, user_data):
        lbl = self.middle.printDirPath(user_data["dirId"], spacer="/")+"/"+str(dpg.get_item_label(sender))
        if dpg.does_item_exist(lbl):
            dpg.focus_item(lbl)
            return
        user_data["tag"]=lbl
        user_data[lbl]=dict()
        user_data[lbl]["argVals"]=dict()
        selected=user_data["selected"]
        with dpg.window(label=lbl, tag=lbl, autosize=True, on_close=self.onClose, user_data=user_data):
            user_data["pos"] = user_data["pos"]+120
            dpg.set_item_pos(lbl,[user_data["pos"],0])
            all, help = self.middle.getArgs(dirId=user_data["dirId"], cmd=user_data["cmd"])
            args=all.keys()
            vals=all.values()
            with dpg.group(horizontal=True, parent=lbl):
                with dpg.group(horizontal=False):
                    with dpg.table(header_row=False, policy=dpg.mvTable_SizingFixedFit, width=500):
                        dpg.add_table_column()
                        dpg.add_table_column(width_stretch=True)
                        for arg, val in zip(args, vals):
                            with dpg.table_row():
                                dpg.add_text(arg, tag=lbl+str(user_data["cmd"])+arg)
                                with dpg.tooltip(parent=lbl+str(user_data["cmd"])+arg):
                                    if len(help[arg])>1:
                                        dpg.add_text(help[arg])
                                    else:
                                        dpg.add_text("You are on your own bro")
                                if arg=="numbers" and len(selected)>0:
                                        dpg.add_input_text(tag=lbl+str(user_data["cmd"])+arg+"text", width=200, callback=self.addToArgVals, user_data=(user_data, arg))
                                        dpg.set_value(lbl+str(user_data["cmd"])+arg+"text", selected)
                                        dpg.configure_item(lbl+str(user_data["cmd"])+arg+"text", readonly=True)
                                        continue
                                if len(val)>0:
                                    dpg.add_combo(tag=lbl+str(user_data["cmd"])+arg+"text", items=val, callback=self.addToArgVals, user_data=(user_data, arg))
                                else:
                                    dpg.add_input_text(tag=lbl+str(user_data["cmd"])+arg+"text", width=200, callback=self.addToArgVals, user_data=(user_data, arg))

                        match str(dpg.get_item_label(sender)):
                            case "add":
                                with dpg.table_row():
                                    dpg.add_text("apply to:")
                                    with dpg.group(horizontal=False):
                                        for devIp in self.middle.getIpDevices():
                                            selected[devIp]=None
                                            dpg.add_checkbox(label=devIp, default_value=True, callback=lambda btn: selected.pop(dpg.get_item_label(btn)) if (dpg.get_item_label(btn) in selected) else selected.update({dpg.get_item_label(btn):None}))

                            case _:
                                if len(user_data["selected"])==0:
                                    with dpg.table_row():
                                        dpg.add_text("apply to:")
                                        devs=self.middle.getIpDevices()
                                        dpg.add_combo(items=devs, default_value=devs[0], tag=lbl+str(user_data["cmd"])+arg+"device")

                        with dpg.table_row():
                            dpg.add_text("test:")
                            dpg.add_text(default_value="fill in the required fields", tag=lbl+str(user_data["cmd"])+"message", wrap=150)
            
                with dpg.group(horizontal=False):
                    dpg.add_button(label="apply", callback=self.apply, user_data=user_data)
                    dpg.add_button(label="cancel", callback=self.onClose, user_data=user_data)
        return

    def addDirTable(self, user_data):
        dirName=self.middle.printDirPath(user_data["dirId"], spacer="/")
        itemName=str(user_data["dirId"])+"table"+dirName
        if dpg.does_item_exist(itemName):
            dpg.delete_item(itemName)
        devKeyVal=self.middle.getDirTableData(user_data["dirId"], spacer="/", begin=True)
        user_data["selected"]=dict()
        if not all(value == False for value in devKeyVal.values()):
            stateList={"invalid":"I", "dynamic":"D", "slave":"S", "disabled":"X", "dhcp":"d", "active":"A", "inactive":"I", "connect":"C","static":"S", "rip":"r", "bgp":"b", "o":"ospf", "v":"vpn"}
            with dpg.table(tag=itemName, header_row=False, parent=str(user_data["dirId"])+"group"+dirName):
                dpg.add_table_column(label=" ")
                commons = self.middle.getCommon(devKeyVal)
                with dpg.table_row():
                    with dpg.collapsing_header(label="common", tag="common,"+str(user_data["dirId"]), default_open=True):
                        with dpg.table(header_row=True, policy=dpg.mvTable_SizingFixedFit):
                            dpg.add_table_column(label=" ", no_hide=True)
                            for ip, devs in commons.items():
                                with dpg.table_row():
                                    dpg.add_selectable(label=ip, tag=ip+","+str(user_data["dirId"]), user_data=[user_data, commons[ip]], span_columns=True, callback=self.tableCallback)
                                    with dpg.tooltip(parent=ip+","+str(user_data["dirId"])):
                                        for devIp, dev in devs.items():
                                            with dpg.collapsing_header(label=devIp, default_open=True, bullet=True):
                                                with dpg.table(policy=dpg.mvTable_SizingFixedFit):
                                                    dpg.add_table_column(label="")
                                                    for k in dev[0].keys():
                                                            if k in stateList:
                                                                continue
                                                            dpg.add_table_column(label=k)
                                                    for row in dev:
                                                        inRowKeys=".id" in row.keys()
                                                        with dpg.table_row():
                                                            state=str()
                                                            if inRowKeys:
                                                                dpg.add_selectable(label="", tag="common"+","+devIp+","+str(user_data["dirId"])+",states,"+row[".id"])
                                                            for key, value in row.items():
                                                                if key==".id":
                                                                    dpg.add_selectable(label=value, span_columns=True, callback=self.tableCallback, user_data=[user_data, {ip:[{".id":value}]}])
                                                                    continue
                                                                if key in stateList and value=="true":
                                                                    state+=stateList[key]
                                                                    continue
                                                                dpg.add_selectable(label=value)
                                                        if inRowKeys:
                                                            dpg.configure_item("common"+","+devIp+","+str(user_data["dirId"])+",states,"+row[".id"], label=state)
                for ip in devKeyVal.keys():
                    device=devKeyVal[ip]
                    if not device:
                        return
                    with dpg.table_row():
                        with dpg.collapsing_header(label=ip, tag=ip+","+str(user_data["dirId"])):
                            with dpg.table(header_row=True, policy=dpg.mvTable_SizingFixedFit, hideable=True):
                                dpg.add_table_column(label="", no_hide=True)
                                for k in device[0].keys():
                                    if k in stateList:
                                        continue
                                    dpg.add_table_column(label=k, width_stretch=True)
                                for row in device:
                                    inRowKeys=".id" in row.keys()
                                    with dpg.table_row():
                                        state=str()
                                        if inRowKeys:
                                            dpg.add_selectable(label="", tag=ip+","+str(user_data["dirId"])+",states,"+row[".id"])
                                        else:
                                            dpg.add_selectable(label="")
                                        for key, value in row.items():
                                            if key==".id":
                                                dpg.add_selectable(label=value, span_columns=True, callback=self.tableCallback, user_data=[user_data, {ip:[{".id":value}]}])
                                                continue
                                            if key in stateList and value=="true":
                                                state+=stateList[key]
                                                continue
                                            dpg.add_selectable(label=value)
                                    if inRowKeys:
                                        dpg.configure_item(ip+","+str(user_data["dirId"])+",states,"+row[".id"], label=state)
        return

    def apply(self, sender, app_data, user_data):
        cmdName=user_data["cmd"]
        argVals=user_data[user_data["tag"]]["argVals"]
        if list(user_data["selected"].values())[0] is None:
            selected=user_data["selected"].copy()
        else:
            selected=ast.literal_eval(dpg.get_value(user_data["tag"]+str(user_data["cmd"])+"numbers"+"text"))
        check=self.middle.applyToDevices(dirId=user_data["dirId"], cmdName=cmdName, argVals=argVals, selected=selected)
        txt=str()
        for ip, mess in check.items():
            txt+=str(ip)+": "+str(mess)+"\n"
        dpg.set_value(item=str(user_data["tag"])+cmdName+"message", value=txt)
        if all(value =="ok" for value in check.values()):
            dpg.set_value(item=str(user_data["tag"])+cmdName+"message", value="ok")
            self.onClose(sender=self,app_data=app_data,user_data=user_data)

    def onClose(self, sender, app_data, user_data):
        user_data["pos"]-=120
        self.addDirTable(user_data=user_data)
        dpg.delete_item(user_data["tag"])
        return

    def addToArgVals(self, sender, app_data, user_data):
        arg=user_data[1]
        user_data=user_data[0]
        user_data[user_data["tag"]]["argVals"][arg]=app_data
        return

    def tableCallback(self, sender, app_data, user_data):
        first=True
        selected=user_data[0]["selected"]
        for rec in user_data:
            if first:
                first=False
                continue
            for devIp in rec.keys():
                for v in rec[devIp]:
                    if devIp not in selected:
                        selected[devIp]=[]
                    if dpg.get_value(sender):
                        if v[".id"] not in selected[devIp]:
                            selected[devIp].append(v[".id"])
                    else:
                        if v[".id"] in selected[devIp]:
                            selected[devIp].remove(v[".id"])
                if len(selected[devIp])==0:
                    selected.pop(devIp)
        user_data=user_data[0]
        #print(user_data["selected"])
        return

if __name__ == "__main__":
    conf_gui(sys.argv[1], sys.argv[2])
