import os
import pygubu
from pymavlink import mavutil
import threading

PROJECT_PATH = os.path.dirname(__file__)
PROJECT_UI = os.path.join(PROJECT_PATH, "grid.ui")
# lock for thread synchronization
lock = threading.Lock()
mavlink_thread_should_exit = False

# Replacement of the standard print() function to flush the output
def progress(string):
    print(string, file=sys.stdout)
    sys.stdout.flush()


def mavlink_loop(conn, callbacks):
    '''a main routine for a thread; reads data from a mavlink connection,
    calling callbacks based on message type received.
    '''
    # source: https://github.com/mavlink-router/mavlink-router/blob/master/examples/heartbeat-print.py
    interesting_messages = list(callbacks.keys())
    while not mavlink_thread_should_exit:
        # send a heartbeat msg
        conn.mav.heartbeat_send(mavutil.mavlink.MAV_TYPE_ONBOARD_CONTROLLER,
                                mavutil.mavlink.MAV_AUTOPILOT_GENERIC,
                                0,
                                0,
                                0)
        m = conn.recv_match(type=interesting_messages, timeout=1, blocking=True)
        if m is None:
            continue
        callbacks[m.get_type()](m)

class AerobridgeRFMApp:
    def __init__(self):
        self.connecton_string = '/dev/ttyUSB0'
        self.connection_baud_rate = 921600
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        self.mainwindow = builder.get_object('mainwindow')
        builder.connect_callbacks(self)
        self.con_type_combo = builder.get_object('connection_string')

        con_options = [('Select an option',''), ('/dev/ttyUSB0','Linux computer connected to the vehicle via USB'), ('dev/cu.usbmodem1','OSX computer connected to the vehicle via USB'), ('com14','Windows computer connected to the vehicle via USB'),]

        self.con_type_combo.configure(values=con_options)
        self.con_type_combo.bind('<<ComboboxSelected>>', self.on_con_string_changed)
        

    def on_con_string_changed(self, event):
        self.connecton_string = self.con_type_combo.get()
        


    def get_drone_id_clicked(self):
        pass

    def drone_id_reg_post_btn_clicked(self):
        pass

    def generate_keys_btn_clicked(self):
        pass

    def send_permission_button_clicked(self):
        pass

    def download_permission_artefact_clicked(self):
        pass

    def get_signed_log_btn_clicked(self):
        pass

    def upload_signed_log_clicked(self):
        pass

    def connect_drone_btn_clicked(self):
        # Source: https://github.com/thien94/vision_to_mavros/blob/master/scripts/t265_to_mavlink.py 
        progress("INFO: Starting Vehicle communications")
        conn = mavutil.mavlink_connection(
            self.connection_string,
            autoreconnect = True,
            source_system = 1,
            source_component = 93,
            baud=self.connection_baudrate,
            force_connected=True,
        )

        mavlink_callbacks = {
        #     'ATTITUDE': att_msg_callback,
        }

        mavlink_thread = threading.Thread(target=mavlink_loop, args=(conn, mavlink_callbacks))
        mavlink_thread.start()


    def run(self):
        self.mainwindow.mainloop()

if __name__ == '__main__':
    import tkinter as tk
    root = tk.Tk()
    app = AerobridgeRFMApp()
    app.run()

