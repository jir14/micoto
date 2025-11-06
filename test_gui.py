import dearpygui.dearpygui as dpg

dpg.create_context()

dpg.create_viewport()

with dpg.window(show=False) as main_window:

    dpg.add_text('This is the main window!')

def login():

    dpg.configure_item(main_window, show=True)

    dpg.set_primary_window(main_window, True)

    dpg.configure_item(login_window, show=False)

with dpg.window() as login_window:

    dpg.add_button(label='Login', callback=login)

dpg.set_primary_window(login_window, True)

dpg.setup_dearpygui()

dpg.show_viewport()

dpg.start_dearpygui()

dpg.destroy_context() 