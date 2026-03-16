import dearpygui.dearpygui as dpg
from app.db.db_crypto import DBConn
import re
import os.path as path
from app.gui.file_dialog.fdialog import FileDialog

cntx=dpg.create_context()

class GUI():
    def __init__(self):
        
        self.db = None
        self.dbPath = None
        self.dbPass = None
        self.selectedList = []

        with dpg.window(tag="devList", label="List of available devices") as devList:
            with dpg.menu_bar():
                
                with dpg.menu(label="DB files"):
                    #dpg.add_menu_item(label="Device DB", callback=dbfd.show_file_dialog, user_data="device")
                    dpg.add_menu_item(label="Device DB", callback=self.dbFilePopup, user_data={"txt":"device"})
                    dpg.add_menu_item(label="Command DB")

            
            with dpg.group(horizontal=True):
                dpg.add_button(label="Add device", tag="AddButton")
                dpg.add_button(label="Remove selected devices", tag="DelButton")
                #dpg.add_button(label="Add device", tag="AddButton", callback=self.openAdd)
                #dpg.add_button(label="Remove selected devices", tag="DelButton", callback=self.delDev)
        
        dpg.create_viewport(title='Micoto', width=1200, height=1000)
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.set_primary_window(devList, True)
        dpg.start_dearpygui()
        dpg.destroy_context()

    def dbFilePopup(self, sender, app_data, user_data):
        fd=FileDialog(callback=lambda x: (dpg.configure_item("Choose file", default_value=x[0])), show_dir_size=False, modal=True, allow_drag=False, default_path="..", multi_selection=False, file_filter=".db")
        fd.show_file_dialog()
        with dpg.window(label=user_data["txt"]+" db file select", tag="FilePopup"):
            with dpg.table(header_row=False):
                dpg.add_table_column()
                dpg.add_table_column()
                with dpg.table_row():
                    dpg.add_text(" "+user_data["txt"]+" db file")
                    dpg.add_input_text(tag="Choose file", readonly=True)
                with dpg.table_row():
                    dpg.add_text(" "+user_data+" db file")
                    dpg.add_input_text(tag="DBPassword", password=True)

    def printDirs(self, selected_files):
        for file in selected_files:
            dpg.configure_item("Choose file", default_value=file)


if __name__ == "__main__":
    gui=GUI()
    
