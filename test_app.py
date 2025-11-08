import dearpygui.dearpygui as dpg
from app.db.db_crypto import DBConn
import re

dpg.create_context()

class GUI:
    def __init__(self):
        self.db = None
        self.dbPath = None
        self.dbPass = None
        with dpg.file_dialog(directory_selector=False, show=False, tag="file_dialog_id", width=500, height=400, callback=fileSelect):
            dpg.add_file_extension(".db", tag="file", color=(255, 255, 0, 255), custom_text="[DB file]")
            dpg.add_file_extension(".*")

        with dpg.window(tag="welcome", label="Welcome to Micoto", width=400) as welcome:
            with dpg.group(horizontal=False):
                with dpg.group():
                    dpg.add_text("Mikoto")
                with dpg.group(horizontal=True):
                    dpg.add_button(tag="DBPath", label="DB file", callback=lambda: dpg.show_item("file_dialog_id"))
                    dpg.add_text("none", tag="DBFile")
                dpg.add_input_text(tag="DBPassword", label="DB password", password=True)
                dpg.add_button(tag="DBDecrypt", label="Decrypt DB", callback=self.decrypt)

    def decrypt(self):
        dpg.configure_item("welcome", show=False)
        dpg.configure_item("AddButton", show=True)
        db_pass = dpg.get_value("DBPassword")
        db_path = dpg.get_value("DBFile")
        if db_pass and db_path:
            self.dbPass = db_pass
            self.dbPath = db_path
            self.db = DBConn(db_path, db_pass)
            self.drawTable()
        
    def drawTable(self):
        with dpg.table(header_row=True, policy=dpg.mvTable_SizingFixedFit, parent="devList", tag="devTable"):
            dpg.add_table_column(label="Name")
            dpg.add_table_column(label="IP") 
            for rec in self.db.selectAll():
                with dpg.table_row():
                    dpg.add_text(rec[1])
                    dpg.add_text(rec[2])
                    
def openAdd(sender, app_data, user_data):
    with dpg.window(label="Add device", width=400, tag="AddWindow"):
        with dpg.group():
            ipItem = dpg.add_input_text(label="Device IP", tag="DevIP", callback=ipValidation)
            dpg.add_input_text(label="Device Username", tag="DevUser")
            dpg.add_input_text(label="Device password", tag="DevPass", password=True)
        dpg.add_button(label="Add", tag="Add", callback=add, user_data=user_data, enabled=False)
        dpg.bind_item_theme(ipItem, ipTheme)
    

def fileSelect(sender, app_data, user_data):
    for s in app_data["selections"].values():
        dpg.set_value("DBFile", s)

def ipValidation():
    if re.match(r"^(((?!25?[6-9])[12]\d|[1-9])?\d\.?\b){4}$", dpg.get_value("DevIP")):
        dpg.bind_item_theme("DevIP", ipThemeCorrect)
        dpg.configure_item("DevIP", enabled=True)
    else:
        dpg.bind_item_theme("DevIP", ipTheme)


def add(sender, app_data, user_data):
    dpg.configure_item("Add", enabled=False)
    user_data.db.insert(dpg.get_value("DevIP"), dpg.get_value("DevUser"), dpg.get_value("DevPass"))
    dpg.delete_item("devTable")
    user_data.drawTable()
    dpg.delete_item("AddWindow") 


with dpg.window(tag="devList", label="List of available devices") as devList:
    gui = GUI()
    dpg.add_button(label="Add device", tag="AddButton", show=False, callback=openAdd, user_data=gui)
    

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
