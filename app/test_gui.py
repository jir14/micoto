import dearpygui.dearpygui as dpg

dpg.create_context()

with dpg.window(label="about", width=400, height=400):
    with dpg.group(horizontal=True):
        for a in range(1, 9):
            dpg.add_checkbox(label=a)
    with dpg.group(horizontal=False):
        for a in range(1, 9):
            dpg.add_checkbox(label=a)

# print children
print(dpg.get_item_children(dpg.last_root()))

# print children in slot 1
print(dpg.get_item_children(dpg.last_root(), 1))

# check draw_line's slot
print(dpg.get_item_slot(dpg.last_item()))

dpg.create_viewport(title='Custom Title', width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()