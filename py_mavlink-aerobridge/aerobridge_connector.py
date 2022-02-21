import os, sys
import pygubu
from pymavlink import mavutil
import threading
import requests, json


PROJECT_PATH = os.path.dirname(__file__)
PROJECT_UI = os.path.join(PROJECT_PATH, "grid.ui")
# lock for thread synchronization
lock = threading.Lock()
mavlink_thread_should_exit = False


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

class AerobridgeRFMApp:
    def __init__(self):
        self.conn = None
        self.drone_id = None
        self.drone_is_connected = False
        self.connection_string = '/dev/ttyUSB0'
        self.connection_baud_rate = 921600
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        self.mainwindow = builder.get_object('mainwindow')
        builder.connect_callbacks(self)


        self.con_type_combo = builder.get_object('connection_string')

        con_options = [('Select an option',''), ('/dev/ttyUSB0','Linux computer connected to the vehicle via USB'), ('dev/cu.usbmodem1','OSX computer connected to the vehicle via USB'), ('com14','Windows computer connected to the vehicle via USB'),('tcp:127.0.0.1:5762','Running SITL via TCP (e.g. MissionPlanner)'),]

        self.con_type_combo.configure(values=con_options)
        self.con_type_combo.bind('<<ComboboxSelected>>', self.on_con_string_changed)
            

    # Replacement of the standard print() function to flush the output
    def progress(self, string):
        print(string, file=sys.stdout)
        sys.stdout.flush()


    def id_callback(self,value):    
        # self.progress("\nAutopilot Version as Dictionary: %s" % value.to_dict())
        self.drone_id = value.uid
        self.update_applicaiton_log("Your Drone ID is %s" % value.uid)

    def heartbeat_callback(self, value):

        self.progress("INFO: Heartbeat from APM (system %u and status %u)" % (value.target_system, value.system_status))
        # self.progress("\nAs dictionary: %s" % value.to_dict())
        
    def mavlink_loop(self, conn, callbacks):
        '''a main routine for a thread; reads data from a mavlink connection,
        calling callbacks based on message type received.
        '''
        # source: https://github.com/mavlink-router/mavlink-router/blob/master/examples/heartbeat-print.py
        interesting_messages = list(callbacks.keys())
        while not mavlink_thread_should_exit:
            # send a heartbeat msg            
            # conn.mav.heartbeat_send(mavutil.mavlink.MAV_TYPE_GCS,
            #                         mavutil.mavlink.MAV_AUTOPILOT_INVALID,
            #                         0,
            #                         0,
            #                         0)
            m = conn.recv_match(type=interesting_messages, timeout=1, blocking=True)
            if m is None:
                continue
            callbacks[m.get_type()](m)



    def update_applicaiton_log(self, message):
        
        message = '{0}\n'.format(message)        
        logging_tb = self.builder.get_object('application_logs_msg')
        logging_tb.insert('end', message)
        # current_text = logging_tb.get("1.0","end-1c")  # Get the current text 
        # print(current_text)

    def on_con_string_changed(self, event):        
        self.connection_string = self.con_type_combo.get()
        

    def get_drone_id_clicked(self):
        if self.drone_is_connected:
            self.conn.mav.autopilot_version_request_send(self.conn.target_system, self.conn.target_component)
            self.progress("INFO: Autopilot version request sent")            
            
        else:
            self.progress("WARNING: Connection string not set, please connect to the drone first!")
             
    def drone_id_reg_post_btn_clicked(self):
        pass

    def get_public_key_btn_clicked(self):
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
                
                if ops.status_code == 200: 
                    all_operations = ops.json()
                    ops_combo_list = []
                    all_operations_cb = self.builder.get_object('operations_details_combo')
                    for operation in all_operations:
                        ops_combo_list.append((operation['id'], operation['name']))
                    
                    all_operations_cb.configure(values=set(ops_combo_list))
                    
                 
    def connect_drone_btn_clicked(self):
        # Source: https://github.com/thien94/vision_to_mavros/blob/master/scripts/t265_to_mavlink.py 
        self.progress("INFO: Starting Vehicle communications")
        try:
            conn = mavutil.mavlink_connection(
                self.connection_string,
                autoreconnect = True,
                baud=self.connection_baud_rate,
                source_system = 255,
            )
            self.conn = conn
        except Exception as e:
            self.progress("ERROR: Error in connecting to vehicle %s" % e)
        
        else:
            mavlink_callbacks = {
                # 'HEARTBEAT': self.heartbeat_callback,
                'AUTOPILOT_VERSION': self.id_callback,
            }

            mavlink_thread = threading.Thread(target=self.mavlink_loop, args=(conn, mavlink_callbacks))
            mavlink_thread.start()
            self.drone_is_connected = True
            # disable connect button
            self.builder.get_object('connect_drone_btn').config(state="disable")
            connection_status_lbl = self.builder.get_variable('drone_conn_status_lbl')
            connection_status_lbl.set('Connected to Drone!')        

        
    def run(self):
        self.mainwindow.mainloop()

if __name__ == '__main__':
    import tkinter as tk
    root = tk.Tk()
    app = AerobridgeRFMApp()
    app.run()

