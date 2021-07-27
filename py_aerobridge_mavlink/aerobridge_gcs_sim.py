import os, sys
import pygubu
import requests


PROJECT_PATH = os.path.dirname(__file__)
PROJECT_UI = os.path.join(PROJECT_PATH, "gcs-grid.ui")


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
    '''
    
    '''
    def __init__(self):
        self.conn = None
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        self.mainwindow = builder.get_object('mainwindow')
        builder.connect_callbacks(self)

    # Replacement of the standard print() function to flush the output
    def progress(self, string):
        print(string, file=sys.stdout)
        sys.stdout.flush()

    def update_application_log(self, message):        
        message = '{0}\n'.format(message)        
        logging_tb = self.builder.get_object('application_logs_msg')
        logging_tb.insert('end', message)


    def download_permission_artefact_clicked(self):
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
                 
        
    def run(self):
        self.mainwindow.mainloop()

if __name__ == '__main__':
    import tkinter as tk
    root = tk.Tk()
    app = AerobridgeRFMApp()
    app.run()