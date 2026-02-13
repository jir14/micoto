import dearpygui.dearpygui as dpg

dpg.create_context()

with dpg.window(label="Tutorial"):
    with dpg.tab_bar():
        with dpg.tab(label="les"):
            dpg.add_text("pes")
        with dpg.tab(label="ves"):
            dpg.add_text("mez")

dpg.create_viewport(title='Custom Title', width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()