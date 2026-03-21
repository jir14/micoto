import dearpygui.dearpygui as dpg
from app.db.db_crypto import DBConn
import re
import os
from app.gui.file_dialog.fdialog import FileDialog
import subprocess

cntx=dpg.create_context()

class GUI():
    def __init__(self):
        
        self.db = None
        self.devDbPath = None
        self.devDbPass = None
        self.cmdDbPath = None
        self.selectedList = []

        with dpg.window(tag="devList", label="List of available devices", on_close=lambda: print("close")) as devList:
            with dpg.menu_bar():
                with dpg.menu(label="DB files"):
                    dfd=FileDialog(tag="dfd", callback=self.setDevDbPath, show_dir_size=False, modal=True, allow_drag=False, default_path="..", multi_selection=False, file_filter=".db")
                    dpg.add_menu_item(label="Device DB file", callback=dfd.show_file_dialog)
                    dpg.add_menu_item(label="Device DB password", callback=self.setDevDbPassWindow)
                    cfd=FileDialog(callback=self.setCmdDb, show_dir_size=False, modal=True, allow_drag=False, default_path="..", multi_selection=False, file_filter=".db")
                    dpg.add_menu_item(label="Command DB", callback=cfd.show_file_dialog)
                    dpg.add_menu_item(label="decrypt", callback=self.decrypt)
                with dpg.menu(label="Admin"):
                    cndd=FileDialog(tag="cndd", callback=self.createNewDevDbFile, show_dir_size=False, dirs_only=True, modal=True, allow_drag=False, default_path="..", multi_selection=False)
                    dpg.add_menu_item(label="Create new device db", callback=cndd.show_file_dialog)
                    dpg.add_menu_item(label="New device to db", callback=self.openDeviceAddWindow)

            with dpg.group(horizontal=True):
                dpg.add_button(label="connect", tag="ConnectButton", callback=self.connect)
                dpg.add_button(label="log", tag="LogButton")
                #dpg.add_button(label="Add device", tag="AddButton", callback=self.openAdd)
                #dpg.add_button(label="Remove selected devices", tag="DelButton", callback=self.delDev)
        
        dpg.create_viewport(title='Micoto', width=1200, height=1000)
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.set_primary_window(devList, True)
        dpg.start_dearpygui()
        dpg.destroy_context()

    def setDevDbFile(self, sender, app_data, user_data):
        self.setDevDbPath([os.path.join(user_data, dpg.get_value("fileName")+".db")])
        self.setDevDbPass()
        self.decrypt()

    def setDevDbPath(self, path):
        self.devDbPath=path[0]
    
    def setDevDbPass(self):
        self.devDbPass=dpg.get_value("DBPassword")
        dpg.delete_item("dbPassPopup")
    
    def setCmdDb(self, path):
        self.cmdDbPath=path[0]

    def centerItem(self, tag):
        Main_width=dpg.get_item_width("devList")
        Main_heigh=dpg.get_item_height("devList")
        Window_width=dpg.get_item_width(tag)
        Window_height=dpg.get_item_height(tag)
        dpg.set_item_pos(tag, [int(Main_width/2-Window_width/2), int(Main_heigh/2-Window_height/2)])

    def openDeviceAddWindow(self, sender, app_data, user_data):
        with dpg.window(label="Add device", width=400, tag="AddWindow", on_close=lambda: dpg.delete_item("AddWindow")) as addWindow:
            with dpg.group():
                ipItem = dpg.add_input_text(label="Device IP", tag="DevIP", callback=self.ipValidation)
                dpg.add_input_text(label="Device Username", tag="DevUser")
                dpg.add_input_text(label="Device password", tag="DevPass", password=True)
            with dpg.group(horizontal=True):
                dpg.add_button(label="Add", tag="Add", callback=self.addDeviceToDb, user_data=user_data, enabled=False)
                dpg.add_text("Trying to add device...", tag="Adding", show=False)
            dpg.bind_item_theme(ipItem, self.ipTheme)
        self.centerItem(addWindow)

    def setDevDbPassWindow(self):
        with dpg.window(label="Device DB password", tag="dbPassPopup", modal=True, autosize=True) as window:
            with dpg.table(header_row=False):
                dpg.add_table_column()
                dpg.add_table_column()
                with dpg.table_row():
                    dpg.add_text("device db file")
                    dpg.add_input_text(tag="devDbPath", readonly=True, default_value=self.devDbPath)
                with dpg.table_row():
                    dpg.add_text("device DB password")
                    dpg.add_input_text(tag="DBPassword", password=True)
            dpg.add_button(label="apply", callback=self.setDevDbPass)
        dpg.render_dearpygui_frame()
        self.centerItem(window)

    def createNewDevDbFile(self, dir):
        with dpg.window(label="Choose file name", tag="NewDbFileName") as wnd:
            with dpg.table(header_row=False):
                dpg.add_table_column()
                dpg.add_table_column()
                with dpg.table_row():
                    dpg.add_text("file name")
                    dpg.add_input_text(tag="fileName")
                with dpg.table_row():
                    dpg.add_text("device DB password")
                    dpg.add_input_text(tag="DBPassword", password=True)  
                with dpg.table_row():
                    dpg.add_text()
                    dpg.add_button(label="create", callback=self.setDevDbFile, user_data=dir[0])
        self.centerItem(wnd)

    def addDeviceToDb(self):
        dpg.configure_item("Add", enabled=False)
        dpg.configure_item("Adding", show=True)
        if self.db.insert(dpg.get_value("DevIP"), dpg.get_value("DevUser"), dpg.get_value("DevPass")):
            dpg.delete_item("devTable")
            self.drawTable()
            dpg.delete_item("AddWindow")
        else:
            with dpg.window(label="Error", tag="Error", modal=True, no_close=True) as modal_id:
                dpg.add_text("Device with same IP already exists!")
                dpg.add_button(label="Ok", width=75, user_data=(modal_id, True), callback=lambda: dpg.delete_item("Error"))
                dpg.configure_item("Adding", show=False)

    def decrypt(self):
        if self.devDbPath and self.devDbPass:
            if dpg.does_item_exist("NewDbFileName"):
                dpg.delete_item("NewDbFileName")
            self.db = DBConn(self.devDbPath, self.devDbPass)
            self.drawTable()

    def drawTable(self):
        with dpg.table(header_row=True, policy=dpg.mvTable_SizingFixedFit, parent="devList", tag="devTable"):
            dpg.add_table_column(label="Name")
            dpg.add_table_column(label="IP") 
            for rec in self.db.selectAll():
                with dpg.table_row():
                    dpg.add_text(rec[1])
                    dpg.add_selectable(label=rec[2], span_columns=True, callback=self.selected)

    def selected(self, app_data):
        devIpAddr = dpg.get_item_label(app_data)

        if devIpAddr in self.selectedList:
            self.selectedList.remove(devIpAddr)
        else:
            self.selectedList.append(devIpAddr)

    def ipValidation(self):
        if re.match(r"^(((?!25?[6-9])[12]\d|[1-9])?\d\.?\b){4}$", dpg.get_value("DevIP")):
            dpg.bind_item_theme("DevIP", self.ipThemeCorrect)
            dpg.configure_item("Add", enabled=True)
        else:
            dpg.bind_item_theme("DevIP", self.ipTheme)
            dpg.configure_item("Add", enabled=False)

    def connect(self):
        if (self.devDbPath or self.devDbPass or self.cmdDbPath) is None:
            return
        conList=dict()
        for devIp in self.selectedList:
            conList[devIp]=self.db.selectDevUserAndPass(devIp)
        
        subprocess.run(["python3", os.path.dirname(os.path.realpath(__file__))+"/app/conf_gui.py", str(self.cmdDbPath), str(conList)])
        return

    with dpg.theme() as ipThemeCorrect:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (0, 0, 0), category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 0, category=dpg.mvThemeCat_Core)

    with dpg.theme() as ipTheme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (200, 0, 0), category=dpg.mvThemeCat_Core)
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 0, category=dpg.mvThemeCat_Core)



if __name__ == "__main__":
    gui=GUI()
    
