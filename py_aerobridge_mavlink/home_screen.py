import os
import pygubu


PROJECT_PATH = os.path.dirname(__file__)
PROJECT_UI = os.path.join(PROJECT_PATH, "grid.ui")


class AerobridgeRFMApp:
    def __init__(self):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        self.mainwindow = builder.get_object('mainwindow')
        builder.connect_callbacks(self)
    
    def get_drone_id_clicked(self):
        pass

    def drone_id_reg_post_btn_clicked(self):
        pass

    def generate_keys_btn_clicked(self):
        pass

    def send_permission_button_clicked(self):
        pass

    def get_signed_log_btn_clicked(self):
        pass

    def connect_drone_btn_clicked(self):
        pass

    def run(self):
        self.mainwindow.mainloop()

if __name__ == '__main__':
    import tkinter as tk
    root = tk.Tk()
    app = AerobridgeRFMApp()
    app.run()

