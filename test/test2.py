import dearpygui.dearpygui as dpg
import sys


def main(arg1):
    def save_callback():
        print("Save Clicked")

    dpg.create_context()
    dpg.create_viewport()
    dpg.setup_dearpygui()

    with dpg.window(label="AMOGUS"):
        dpg.add_text(arg1)
        dpg.add_text("PENIS")
        dpg.add_button(label="Save", callback=save_callback)
        dpg.add_input_text(label="string")
        dpg.add_slider_float(label="float")

    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == "__main__":
    main(sys.argv[1])