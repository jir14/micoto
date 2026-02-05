import dearpygui.dearpygui as dpg

dpg.create_context()

def selectables(sender, app_data, user_data):
    test=("alza", "czc", "datard")
    dpg.add_listbox(items=test, parent="Selectable Tables")

with dpg.window(tag="Selectable Tables"):
    with dpg.table(header_row=False):
        dpg.add_table_column()
        with dpg.table_row():
            dpg.add_selectable(label="Pes", callback=selectables)

dpg.create_viewport(width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()