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
from dataclasses import dataclass
from typing import Optional
from enum import Enum

SpecificSessionID = str
@dataclass
class LatLngPoint:
  lat: float
  lng: float

class Reference1(Enum):
    W84 = 'W84'

class Units(Enum):
    M = 'M'

class Category(Enum):
    EUCategoryUndefined = 'EUCategoryUndefined'
    Open = 'Open'
    Specific = 'Specific'
    Certified = 'Certified'

class Class(Enum):
    EUClassUndefined = 'EUClassUndefined'
    Class0 = 'Class0'
    Class1 = 'Class1'
    Class2 = 'Class2'
    Class3 = 'Class3'
    Class4 = 'Class4'
    Class5 = 'Class5'
    Class6 = 'Class6'

@dataclass
class Altitude:
    value: float
    reference: Reference1
    units: Units

class AltitudeType(Enum):
    Takeoff = 'Takeoff'
    Dynamic = 'Dynamic'
    Fixed = 'Fixed'

@dataclass
class RIDAuthData:
    data: Optional[str] = ''
    format: Optional[int] = 0

@dataclass
class OperatorLocation:
    position: LatLngPoint
    altitude: Optional[Altitude] = None
    altitude_type: Optional[AltitudeType] = None

@dataclass
class UASID:
    specific_session_id: Optional[SpecificSessionID] = None
    serial_number: Optional[str] = ''
    registration_id: Optional[str] = ''
    utm_id: Optional[str] = ''


@dataclass
class UAClassificationEU:
    category: Optional[Category] = 'EUCategoryUndefined'
    class_: Optional[Class] = 'EUClassUndefined'



@dataclass
class RIDFlightDetails:
    id: str
    eu_classification: Optional[UAClassificationEU] = None
    uas_id: Optional[UASID] = None
    operator_location: Optional[OperatorLocation] = None
    auth_data: Optional[RIDAuthData] = None
    operator_id: Optional[str] = ''
    operation_description: Optional[str] = ''


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
        states = rid_json['states']
        
        uas_id = UASID(registration_id = 'CHE-5bisi9bpsiesw',  serial_number='d29dbf50-f411-4488-a6f1-cf2ae4d4237a',utm_id= '07a06bba-5092-48e4-8253-7a523f885bfe')
      
        operator_location = OperatorLocation(position = LatLngPoint(lat = 46.97615311620088,lng = 7.476099729537965))
        rid_operator_details = RIDFlightDetails(
            id="382b3308-fa11-4629-a966-84bb96d3b4db",
            uas_id = uas_id,
            operation_description="Medicine Delivery",
            operator_id='CHE-076dh0dq',
            eu_classification = 'Class0',            
            operator_location=  operator_location
        )



        securl = env.get('BLENDER_RID_FQDN', 'http://localhost:8000/flight_stream/set_telemetry') # set this to self (Post the json to itself)
        
        headers = {"Content-Type":'application/json',"Authorization": "Bearer "+ self.credentials['access_token']} 
        
        for state in states:
            
            payload = {"observations":[{"current_states":[state], "flight_details": {"rid_details" :asdict(rid_operator_details), "aircraft_type": "Helicopter","operator_name": "Thomas-Roberts" }}]}
            
            try:
                response = requests.put(securl, json = payload, headers = headers)                
            except Exception as e:                
                print(e)
            else:
                if response.status_code == 201:
                    print("Successfully submitted telemetry information..")
                else: 
                    print(response.json())

