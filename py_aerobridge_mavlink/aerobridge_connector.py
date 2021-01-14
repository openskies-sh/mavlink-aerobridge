import os
import pygubu
from pymavlink import mavutil
import threading
import requests, json


PROJECT_PATH = os.path.dirname(__file__)
PROJECT_UI = os.path.join(PROJECT_PATH, "grid.ui")
# lock for thread synchronization
lock = threading.Lock()
mavlink_thread_should_exit = False

# Replacement of the standard print() function to flush the output
def progress(string):
    print(string, file=sys.stdout)
    sys.stdout.flush()


class AerobridgeClient():
    '''
    This a a Python client that uses the Aerobridge API to make calls
    and return data. It requires the requests package and the json module. 
    '''

    def __init__(self, url, token):
        '''
        Declare your project id, token and the url (optional). 
        '''
        self.token = token
        self.securl = url if url else 'https://aerobridgetestflight.herokuapp.com/'


    def ping_server(self):
        ''' This method Pings the Aerobridge Server for a response  '''
        securl = self.securl+ 'ping'
        headers = {'Authorization': 'Bearer '+ self.token}
        r = requests.get(securl, headers=headers)
        return r


    def get_operations(self):
        ''' This method Pings the Aerobridge Server for a response  '''
        securl = self.securl+ 'gcs/flight-operations'
        headers = {'Authorization': 'Bearer '+ self.token}
        r = requests.get(securl, headers=headers)
        return r




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

    def on_connect_aerobridge_clicked(self):
        jwt_tb = self.builder.get_object('jwt_text')
        
        ab_conn_lbl = self.builder.get_variable('ab_conn_status_lbl')
        
        jwt = jwt_tb.get()
        if (jwt=='Paste Aerobridge JWT Token'):          
            ab_conn_lbl.set('Invalid Token, contact your administrator')
        else:
            myAerobridgeClient = AerobridgeClient(url='https://aerobridgetestflight.herokuapp.com/', token=jwt)
            r = myAerobridgeClient.ping_server()
            try:
                assert r.status_code == 200
                ab_conn_lbl.set('Connected and Verified Token!')
            except AssertionError as ae:
                ab_conn_lbl.set('Invalid Token, contact your administrator')
            else:
                # Downloading Operations
                ops = myAerobridgeClient.get_operations()
                print (ops, ops.status_code)
                if ops.status_code == 200: 
                    all_operations = ops.json()
                    print(all_operations)
                    ops_combo_list = []
                    all_operations_cb = self.builder.get_object('operations_details_combo')
                    for operation in all_operations:
                        ops_combo_list.append((operation['id'], operation['name']))
                    
                    all_operations_cb.configure(values=set(ops_combo_list))
                    print(ops_combo_list)
                        


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

