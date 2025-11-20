import dearpygui.dearpygui as dpg
from app.db.db_crypto import DBConn
import re as re
import os.path as path

dpg.create_context()

class GUI:
    def __init__(self):
        self.db = None
        self.dbPath = None
        self.dbPass = None
        self.selectedList = []

        with dpg.window(tag="welcome", label="Welcome to Micoto", width=400) as welcome:
            with dpg.group(horizontal=False):
                with dpg.group():
                    dpg.add_text("Mikoto")
                with dpg.group(horizontal=True):
                    dpg.add_button(tag="DBPath", label="Choose DB file", callback=lambda: dpg.show_item("file_dialog_id"))
                    dpg.add_button(tag="DBDir", label="Create new DB file", callback=lambda: dpg.show_item("directory_dialog_id"))
                    dpg.add_text("none", tag="DBFile")
                dpg.add_input_text(tag="DBName", label="DB file name", show=False)  
                dpg.add_input_text(tag="DBPassword", label="DB password", password=True)
                dpg.add_button(tag="DBDecrypt", label="Decrypt DB", callback=self.decrypt)

        with dpg.file_dialog(directory_selector=False, show=False, tag="file_dialog_id", width=500, height=400, callback=fileSelect):
            dpg.configure_item("DBName", enabled=False)
            dpg.add_file_extension(".db", tag="file", color=(255, 255, 0, 255), custom_text="[DB file]")
            dpg.add_file_extension(".*")

        with dpg.file_dialog(directory_selector=True, show=False, tag="directory_dialog_id", width=500, height=400, callback=directorySelect):
            dpg.configure_item("DBName", enabled=True)
            dpg.add_file_extension(".db", tag="folder", color=(255, 255, 0, 255), custom_text="[DB file]")


    def decrypt(self):
        dpg.configure_item("welcome", show=False)
        dpg.configure_item("AddButton", show=True)
        dpg.configure_item("DelButton", show=True)
        db_pass = dpg.get_value("DBPassword")
        db_path = dpg.get_value("DBFile")
        db_name = dpg.get_value("DBName")
        if db_pass and db_path:
            if ""!=db_name:
                if re.match(r".*\.db$", db_name):
                    self.dbPath = path.join(db_path, db_name)
                else:
                    self.dbPath = path.join(db_path, db_name+".db")
            else:
                self.dbPath = db_path
            self.dbPass = db_pass
            self.db = DBConn(self.dbPath, db_pass)
            self.drawTable()    
    
    def drawTable(self):
        with dpg.table(header_row=True, policy=dpg.mvTable_SizingFixedFit, parent="devList", tag="devTable"):
            dpg.add_table_column(label="Name")
            dpg.add_table_column(label="IP") 
            for rec in self.db.selectAll():
                with dpg.table_row():
                    dpg.add_text(rec[1])
                    dpg.add_selectable(label=rec[2], span_columns=True, callback=self.selected)

    def delDev(self):
        for devIp in self.selectedList:
            self.db.remove(devIp)
        dpg.delete_item("devTable")
        self.drawTable()
    
    def selected(self, app_data):
        devIpAddr = dpg.get_item_label(app_data)
        if devIpAddr in self.selectedList:
            self.selectedList.remove(devIpAddr)
        else:
            self.selectedList.append(devIpAddr)
                    
    def openAdd(self, sender, app_data, user_data):
        with dpg.window(label="Add device", width=400, tag="AddWindow", on_close=lambda: dpg.delete_item("AddWindow")):
            with dpg.group():
                ipItem = dpg.add_input_text(label="Device IP", tag="DevIP", callback=self.ipValidation)
                dpg.add_input_text(label="Device Username", tag="DevUser")
                dpg.add_input_text(label="Device password", tag="DevPass", password=True)
            with dpg.group(horizontal=True):
                dpg.add_button(label="Add", tag="Add", callback=self.add, user_data=user_data, enabled=False)
                dpg.add_text("Trying to add device...", tag="Adding", show=False)
            dpg.bind_item_theme(ipItem, ipTheme)

    def ipValidation(self):
        if re.match(r"^(((?!25?[6-9])[12]\d|[1-9])?\d\.?\b){4}$", dpg.get_value("DevIP")):
            dpg.bind_item_theme("DevIP", ipThemeCorrect)
            dpg.configure_item("Add", enabled=True)
        else:
            dpg.bind_item_theme("DevIP", ipTheme)
            dpg.configure_item("Add", enabled=False)


    def add(self, sender, app_data, user_data):
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

def fileSelect(sender, app_data, user_data):
    for s in app_data["selections"].values():
        dpg.set_value("DBFile", s)
    dpg.configure_item("DBName", show=False)

def directorySelect(sender, app_data, user_data):
    dpg.set_value("DBFile", app_data["file_path_name"])
    dpg.configure_item("DBName", show=True)

with dpg.window(tag="devList", label="List of available devices") as devList:
    gui = GUI()
    with dpg.group(horizontal=True):
        dpg.add_button(label="Add device", tag="AddButton", show=False, callback=gui.openAdd, user_data=gui)
        dpg.add_button(label="Remove selected devices", tag="DelButton", show=False, callback=gui.delDev, user_data=gui)

with dpg.theme() as ipThemeCorrect:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (0, 0, 0), category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 0, category=dpg.mvThemeCat_Core)

with dpg.theme() as ipTheme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (200, 0, 0), category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 0, category=dpg.mvThemeCat_Core)

dpg.create_viewport(title='Micoto', width=700, height=500)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window(devList, True)
dpg.start_dearpygui()
dpg.destroy_context()
