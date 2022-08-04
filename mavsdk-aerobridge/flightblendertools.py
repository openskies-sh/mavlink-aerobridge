from lib2to3.pgen2 import token
from os import environ as env

from dotenv import load_dotenv, find_dotenv
import json
import time
import requests
from dataclasses import dataclass, asdict
from typing import Optional
import pathlib
from os.path import exists
ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

@dataclass
class RIDOperatorDetails():
  id: str
  operator_id: Optional[str]
  operation_description: Optional[str]
  serial_number: Optional[str]
  registration_number: Optional[str]
  aircraft_type:str = 'Helicopter'


class PassportCredentialsGetter():
    def __init__(self):
        pass

    def delete_cached_credentials(self):  
        
        token_exists = exists('token.json')
        if token_exists:
            token_file = pathlib.Path("token.json")
            token_file.unlink()
            
            
    def get_cached_credentials(self):  
        token_exists = exists('token.json')
        print(token_exists)
        if token_exists:
            with open('token.json', 'r') as token_file:
                token_details = token_file.read()
            credentials = json.loads(token_details)         
                       
        else:               
            credentials = self.get_write_credentials()            
            with open('token.json', 'w') as token_file:
                token_file.write(json.dumps(credentials))
            
        return credentials
            
    def get_write_credentials(self):        
        payload = {"grant_type":"client_credentials","client_id": env.get('BLENDER_WRITE_CLIENT_ID'),"client_secret": env.get('BLENDER_WRITE_CLIENT_SECRET'),"audience": env.get('BLENDER_AUDIENCE'),"scope": env.get('BLENDER_WRITE_SCOPE')}        
        
        url = env.get('PASSPORT_URL', None) + env.get('PASSPORT_TOKEN_ENDPOINT', None)
        
        token_data = requests.post(url, data = payload)
        t_data = token_data.json()
        
        return t_data

class BlenderUploader():
    def __init__(self, credentials):        
        self.credentials = credentials
    def upload_to_blender(self, rid_json):
    
        states = rid_json['current_states']
        
        rid_operator_details = RIDOperatorDetails(
            id="382b3308-fa11-4629-a966-84bb96d3b4db",
            serial_number='d29dbf50-f411-4488-a6f1-cf2ae4d4237a',
            operation_description="Medicine Delivery",
            operator_id='CHE-076dh0dq  ',
            registration_number='CHE-5bisi9bpsiesw',
        )

        for state in states: 
            headers = {"Content-Type":'application/json',"Authorization": "Bearer "+ self.credentials['access_token']}     
            
            payload = {"observations":[{"current_states":[state], "flight_details": asdict(rid_operator_details) }]}
            
            securl = env.get('BLENDER_RID_FQDN', 'http://localhost:8000/rid/flight_data') # set this to self (Post the json to itself)
            try:
                response = requests.put(securl, json = payload, headers = headers)
                
            except Exception as e:                
                print(e)
            else:
                if response.status_code == 201:
                    print("Sleeping 3 seconds..")
                    time.sleep(3)
                else: 
                    print(response.json())

