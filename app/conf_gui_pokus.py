import copy
import dearpygui.dearpygui as dpg
import middleware as middle
import ast as ast
import sys
from EditThemePlugin import EditThemePlugin
import window as wnd

class conf_gui():
    def __init__(self, cmdDbPath="" , devs=""):
        dpg.create_context()

        dpg.show_item_registry()

        """with dpg.font_registry():
            default_font=dpg.add_font("./themes/Roboto.ttf", 15*2)
            dpg.set_global_font_scale(0.5)
        dpg.bind_font(default_font)"""

        devices=ast.literal_eval(devs)        
        self.middle=middle.middleware(cmdDbFile=cmdDbPath, devices=devices)
        with dpg.window(label="Main") as MainWindow:
            with dpg.menu_bar():
                with dpg.menu(label="Theme"):
                    EditThemePlugin()
                    dpg.add_menu_item(label="Fonts", callback=lambda: dpg.show_font_manager())
            with dpg.group(horizontal=False, parent=MainWindow, tag="Menu", width=100, height=dpg.get_item_height(MainWindow)):
                with dpg.table(header_row=False):
                    dpg.add_table_column()
                    for dirId in self.middle.getDirsWithoutParent():
                        with dpg.table_row():
                            user_data={"pos":0, "dirId":dirId}       
                            dpg.add_button(label=self.middle.getDirName(dirId), user_data=user_data, callback=self.openDirWindow)
        name=", ".join(list(devices.keys()))

        dpg.create_viewport(title='Micoto - configure '+name, width=1500, height=1000)
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.set_primary_window(MainWindow, True)
        dpg.start_dearpygui()
        dpg.destroy_context()

    def openDirWindow(self, sender, app_data, user_data):
        win = wnd.window(dirId=user_data["dirId"], pos=user_data["pos"], lbl=self.middle.printDirPath(user_data["dirId"], spacer="/"))
        if dpg.does_item_exist(win.getLbl()):
            dpg.focus_item(win.getLbl())
            return
        with dpg.window(label=win.getLbl(), tag=win.getLbl(), width=1000, autosize=True, on_close=self.onClose, user_data=win, no_resize=False):
            win.setPos(win.getPos()+120)
            dpg.set_item_pos(win.getLbl(), [win.getPos(), win.getPos()/2])
            tableData = self.middle.getDirTableData(win.getDirId(), spacer="/", begin=True)
            dirs=self.middle.getDirDirsIDs(win.getDirId())
            if not all(value == False for value in tableData.values()):
                help = self.middle.getSyntax(win.getDirId())
                with dpg.tab_bar():
                    with dpg.tab(label=self.middle.getDirName(win.getDirId()), tag=str(win.getDirId())+str(win.getLbl())):
                        with dpg.group(horizontal=True, tag=str(win.getDirId())+str(win.getLbl())+"group", parent=str(win.getDirId())+str(win.getLbl())):
                            self.addCommands(win=win)
                        self.addDirTable(user_data=win)
                    if dirs:
                        for dir in dirs:
                            wn = copy.deepcopy(win)
                            wn.setDirId(dir)
                            wn.setLbl(self.middle.printDirPath(dir, spacer="/"))
                            dirName=self.middle.getDirName(dir)
                            with dpg.tab(label=dirName, tag=str(wn.getDirId())+str(wn.getLbl()), no_tooltip=True):
                                with dpg.group(horizontal=True, tag=str(wn.getDirId())+str(wn.getLbl())+"group", parent=str(wn.getDirId())+str(wn.getLbl())):
                                    self.addCommands(win=wn)
                                self.addDirTable(user_data=wn)

                            with dpg.tooltip(parent=str(wn.getDirId())+str(wn.getLbl())):
                                if len(help[dirName])>1:
                                    dpg.add_text(help[dirName])
            else:
                recs = self.middle.getDirDirsIDs(win.getDirId())
                if recs:
                    with dpg.group(horizontal=False):
                        help = self.middle.getSyntax(win.getDirId())
                        for rec in recs:
                            lbl=self.middle.getDirName(rec)
                            dpg.add_button(label=lbl, tag=str(rec)+lbl, callback=self.openDirWindow, user_data={"pos":win.getPos(), "dirId":rec})
                            with dpg.tooltip(parent=str(rec)+lbl):
                                if len(help[lbl])>1:
                                    dpg.add_text(help[lbl])
                                else:
                                    dpg.add_text("You are on your own bro")

                with dpg.group(horizontal=True, parent=lbl):
                    cmds = self.middle.getDirCmds(win.getDirId())
                    if cmds:
                        for key, val in cmds.items():
                            wn = copy.deepcopy(win)
                            wn.setCmd(key)
                            if val:
                                match key:
                                    #case "add":
                                    #    dpg.add_button(label=key, callback=lambda: print("pes"), user_data=wn)
                                    case _:
                                        dpg.add_button(label=key, callback=self.openCmds, user_data=wn)
                        with dpg.group(tag=str(win.getDirId())+"group"+win.getLbl(), horizontal=False, parent=lbl):
                            self.addDirTable(user_data=win)
                dpg.add_text("")
        return
    
    def openCmds(self, sender, app_data, user_data):
        oldWin = user_data
        path = self.middle.printDirPath(oldWin.getDirId(), spacer="/")
        cmd = str(dpg.get_item_label(sender))
        lbl = path+"/"+cmd
        if dpg.does_item_exist(lbl):
            dpg.focus_item(lbl)
            return
        win = wnd.window(dirId=oldWin.getDirId(), selected=oldWin.getSelected(), lbl=path, pos=oldWin.getPos(), cmd=cmd)
        win.clearArgVals()
        with dpg.window(label=lbl, tag=lbl, autosize=True, on_close=self.onClose, user_data=win):
            win.setPos(win.getPos()+120)
            dpg.set_item_pos(lbl,[win.getPos(),win.getPos()/2])
            all, help = self.middle.getArgs(dirId=win.getDirId(), cmd=cmd)
            with dpg.group(horizontal=True, parent=lbl):
                with dpg.group(horizontal=False):
                    with dpg.table(header_row=False, policy=dpg.mvTable_SizingFixedFit, width=500):
                        dpg.add_table_column()
                        dpg.add_table_column(width_stretch=True)
                        for arg, val in all.items():
                            with dpg.table_row():
                                dpg.add_text(arg, tag=lbl+cmd+arg)
                                with dpg.tooltip(parent=lbl+cmd+arg):
                                    if len(help[arg])>1:
                                        dpg.add_text(help[arg])
                                    else:
                                        dpg.add_text("You are on your own bro")
                                if arg=="numbers":
                                    if len(win.getSelected())!=0:                   
                                        dpg.add_input_text(tag=lbl+cmd+arg+"text", width=200, callback=self.addToArgVals, user_data=(win, arg))
                                        dpg.set_value(lbl+cmd+arg+"text", win.getSelected())
                                        dpg.configure_item(lbl+cmd+arg+"text", readonly=True)
                                        continue
                                    dpg.add_combo(tag=lbl+cmd+arg+"numbers", items=val, callback=self.applyChange, user_data=win)
                                    continue

                                if len(val)>0:
                                    dpg.add_combo(tag=lbl+cmd+arg+"text", items=val, callback=self.addToArgVals, user_data=(win, arg))
                                else:
                                    dpg.add_input_text(tag=lbl+cmd+arg+"text", width=200, callback=self.addToArgVals, user_data=(win, arg))

                        match str(dpg.get_item_label(sender)):
                            case "add":
                                with dpg.table_row():
                                    dpg.add_text("apply to:")
                                    with dpg.group(horizontal=False):
                                        for devIp in self.middle.getIpDevices():
                                            #win.getSelected[devIp]=None
                                            dpg.add_checkbox(label=devIp, default_value=False, callback=self.applyChange, user_data=win)
                                            #dpg.add_checkbox(label=devIp, default_value=False, callback=self.checkboxChecker, user_data=win)
                                            #dpg.add_checkbox(label=devIp, default_value=True, callback=lambda btn: win.setSelected.pop(dpg.get_item_label(btn)) if (dpg.get_item_label(btn) in win.setSelected) else win.setSelected.update({dpg.get_item_label(btn):None}))
                            case _:
                                if len(win.getSelected())==0:
                                    with dpg.table_row():
                                        dpg.add_text("apply to:")
                                        devs=self.middle.getIpDevices()
                                        dpg.add_combo(items=devs, default_value=devs[0], tag=lbl+cmd+arg+"device", callback=self.applyChange, user_data=win)
                                        #dpg.add_combo(items=devs, default_value=devs[0], tag=lbl+cmd+arg+"device", callback=lambda ip: win.setSelected(dpg.get_value(lbl+cmd+arg+"text")))

                        with dpg.table_row():
                            dpg.add_text("test:")
                            dpg.add_text(default_value="fill in the required fields", tag=lbl+cmd+"message", wrap=150)
            
                with dpg.group(horizontal=False):
                    dpg.add_button(label="apply", callback=self.apply, user_data=win)
                    dpg.add_button(label="cancel", callback=self.onClose, user_data=win)
        return

    def addDirTable(self, user_data):
        win=user_data
        dirName=win.getLbl()
        itemName=str(win.getDirId())+"table"+dirName
        if dpg.does_item_exist(itemName):
            dpg.delete_item(itemName)
        if dpg.does_alias_exist(str(str(win.getDirId())+"group"+win.getLbl())):
            dpg.delete_item(str(str(win.getDirId())+"group"+win.getLbl()))
        devKeyVal=self.middle.getDirTableData(win.getDirId(), spacer="/", begin=True)
        win.clearSelected()
        if not all(value == False for value in devKeyVal.values()):
            stateList={"invalid":"I", "dynamic":"D", "slave":"S", "disabled":"X", "dhcp":"d", "active":"A", "inactive":"I", "connect":"C","static":"S", "rip":"r", "bgp":"b", "o":"ospf", "v":"vpn"}
            with dpg.group(tag=str(str(win.getDirId())+"group"+win.getLbl()), horizontal=False, parent=str(win.getDirId())+str(win.getLbl())):
                with dpg.table(tag=itemName, header_row=False, parent=str(win.getDirId())+"group"+dirName):
                    dpg.add_table_column(label=" ")
                    commons = self.middle.getCommon(devKeyVal)
                    with dpg.table_row():
                        with dpg.collapsing_header(label="common", tag="common,"+str(win.getDirId()), default_open=True):
                            with dpg.table(header_row=True, policy=dpg.mvTable_SizingFixedFit):
                                dpg.add_table_column(label=" ", no_hide=True)
                                for ip, devs in commons.items():
                                    with dpg.table_row():
                                        dpg.add_selectable(label=ip, tag=ip+","+str(win.getDirId()), span_columns=True,  callback=win.setSelected, user_data=self.middle.commonFiltered(commons[ip]), default_value=False)
                                        with dpg.tooltip(parent=ip+","+str(win.getDirId())):
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
                                                                    dpg.add_selectable(label="", tag="common"+","+devIp+","+str(win.getDirId())+",states,"+row[".id"])
                                                                for key, value in row.items():
                                                                    if key==".id":
                                                                        dpg.add_selectable(label=value, span_columns=True)
                                                                        continue
                                                                    if key in stateList and value=="true":
                                                                        state+=stateList[key]
                                                                        continue
                                                                    dpg.add_selectable(label=value)
                                                            if inRowKeys:
                                                                dpg.configure_item("common"+","+devIp+","+str(win.getDirId())+",states,"+row[".id"], label=state)
                    for ip in devKeyVal.keys():
                        device=devKeyVal[ip]
                        if not device:
                            return
                        with dpg.table_row():
                            with dpg.collapsing_header(label=ip, tag=ip+","+str(win.getDirId())):
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
                                                dpg.add_selectable(label="", tag=ip+","+str(win.getDirId())+",states,"+row[".id"])
                                            else:
                                                dpg.add_selectable(label="")
                                            for key, value in row.items():
                                                if key==".id":
                                                    dpg.add_selectable(label=value, span_columns=True, callback=win.setSelected, user_data={ip:[value]})
                                                    continue
                                                if key in stateList and value=="true":
                                                    state+=stateList[key]
                                                    continue
                                                dpg.add_selectable(label=value)
                                        if inRowKeys:
                                            dpg.configure_item(ip+","+str(win.getDirId())+",states,"+row[".id"], label=state)
        return

    def addCommands(self, win):
        if dpg.does_item_exist(str(win.getDirId())+str(win.getLbl())+"group"):
            dpg.delete_item(str(win.getDirId())+str(win.getLbl())+"group")
            with dpg.group(horizontal=True, tag=str(win.getDirId())+str(win.getLbl())+"group", parent=str(win.getDirId())+str(win.getLbl())):
                cmds = self.middle.getDirCmds(win.getDirId())
                if cmds:
                    for key, val in cmds.items():
                        if val:
                            dpg.add_button(label=key, callback=self.openCmds, user_data=win)
        return

    def apply(self, sender, app_data, user_data):
        cmdName=user_data.getCmd()
        argVals=user_data.getArgVals()
        check=self.middle.applyToDevices(dirId=user_data.getDirId(), cmdName=cmdName, argVals=argVals, selected=user_data.getSelected())
        txt=str()
        for ip, mess in check.items():
            txt+=str(ip)+": "+str(mess)+"\n"
        dpg.set_value(item=str(user_data.getLbl()+"/"+user_data.getCmd())+cmdName+"message", value=txt)
        if all(value =="ok" for value in check.values()):
            user_data.setPos(user_data.getPos()-120)
            dpg.set_value(item=str(user_data.getLbl()+"/"+user_data.getCmd())+cmdName+"message", value="ok")
            self.onClose(sender=self,app_data=app_data,user_data=user_data)

    def onClose(self, sender, app_data, user_data):
        self.addCommands(win=user_data)
        self.addDirTable(user_data=user_data)
        dpg.delete_item(user_data.getLbl()+"/"+user_data.getCmd() if user_data.getCmd() else user_data.getLbl())
        return

    def addToArgVals(self, sender, app_data, user_data):
        arg=user_data[1]
        win=user_data[0]
        win.setArgVals({arg:dpg.get_value(sender)})
        return
    
    def applyChange(self, sender, app_data, win):
        if not isinstance(app_data, bool):
            win.clearSelected()
            ip = dpg.get_value(str(win.getLbl()+"/"+win.getCmd()+win.getCmd()+"numbers"+"device"))
        else:
            ip = dpg.get_item_label(sender)
        if dpg.does_item_exist(str(win.getLbl()+"/"+win.getCmd()+win.getCmd()+"interface"+"text")):
            number = dpg.get_value(str(win.getLbl()+"/"+win.getCmd()+win.getCmd()+"interface"+"text"))
        else:
            number = dpg.get_value(str(win.getLbl()+"/"+win.getCmd()+win.getCmd()+"numbers"+"numbers"))
        win.setSelected(ipId={ip:[number]})
        return
    
    """def checkboxChecker(self, sender, app_data, win):
        if dpg.does_item_exist(str(win.getLbl()+"/"+win.getCmd()+win.getCmd()+"numbers"+"device")):
            dpg.delete_item(str(win.getLbl()+"/"+win.getCmd()+win.getCmd()+"numbers"+"device"))
        dpg.add_text(show=False, default_value=dpg.get_item_label(sender), tag=str(win.getLbl()+"/"+win.getCmd()+win.getCmd()+"numbers"+"device"), parent=sender)
        self.applyChange(sender=sender, app_data=app_data, win=win)
        return"""

if __name__ == "__main__":
    conf_gui(sys.argv[1], sys.argv[2])
