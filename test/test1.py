import dearpygui.dearpygui as dpg
import subprocess

def save_callback():
    print("Save Clicked")
    txt=str()
    for r in pes:
        txt+=str(r)+","
    subprocess.run(["python", "test2.py", txt])

dpg.create_context()
dpg.create_viewport()
dpg.setup_dearpygui()

with dpg.window(label="Example Window"):
    dpg.add_text("Hello world")
    dpg.add_button(label="RUN", callback=save_callback)
    pes=[1, "2", True]
    dpg.add_input_text(label="string", tag="input")
    dpg.add_slider_float(label="float")

dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()