import dearpygui.dearpygui as dpg

dpg.create_context()

def button_callback(sender, app_data, user_data):
    print(f"sender is: {sender}")
    print(f"app_data is: {app_data}")
    print(f"user_data is: {user_data}")

def callback(sender, app_data):
    print('OK was clicked.')
    print("Sender: ", sender)
    print("App Data: ", app_data)

def cancel_callback(sender, app_data):
    print('Cancel was clicked.')
    print("Sender: ", sender)
    print("App Data: ", app_data)

dpg.add_file_dialog(
    directory_selector=True, show=False, callback=callback, tag="file_dialog_id",
    cancel_callback=cancel_callback, width=700 ,height=400)

with dpg.window(label="Tutorial"):
    # user data and callback set when button is created
    dpg.add_button(label="Decrypt", callback=button_callback, user_data="Some Data")
    dpg.add_input_text(label="Master password", default_value="********")

    # user data and callback set any time after button has been created
    btn = dpg.add_button(label="Apply 2", )
    dpg.set_item_callback(btn, button_callback)
    dpg.set_item_user_data(btn, "Some Extra User Data")


with dpg.window(label="Tutorial", width=800, height=300):
    dpg.add_button(label="Choose db file", callback=lambda: dpg.show_item("file_dialog_id"))

dpg.create_viewport(title='Micoto login', width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()