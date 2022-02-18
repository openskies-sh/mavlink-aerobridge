import asyncio
from mavsdk import System
from mavsdk.info import InfoError
import aerobridgetools
import requests
import logging
import sys
from data_definitions import FirmwareVersionAndHash, HardwareUID
from os import environ as env
from dotenv import load_dotenv, find_dotenv
from dataclasses import asdict

load_dotenv(find_dotenv())
 
ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
    level=logging.DEBUG,
    datefmt="%H:%M:%S",
    stream=sys.stderr,
)
logger = logging.getLogger("mavlink-aerobridge")
logging.getLogger("chardet.charsetprober").disabled = True
logger.setLevel(logging.INFO)

# This file checks the drone ID and firmware version against one stored in the management server and allows arming / disarming of the drone


class AuthorityCredentialsGetter():
    ''' All calls to the Aerobridge requires credentials from a oauth server, in this case this is Flight Passport  '''
    def __init__(self):
        pass
        
    def get_credentials(self):  
        payload = {"grant_type":"client_credentials","client_id": env.get('PASSPORT_CLIENT_ID'),"client_secret": env.get('PASSPORT_CLIENT_SECRET'),"audience": env.get('PASSPORT_AUDIENCE'),"scope": 'aerobridge.read'}          
        url = env.get('PASSPORT_URL') + env.get('PASSPORT_TOKEN_URL')               
       
        token_data = requests.post(url, data = payload)
        t_data = token_data.json()     
        return t_data

async def run():    
    my_authorization_helper = AuthorityCredentialsGetter()
    auth_token = my_authorization_helper.get_credentials()    
    
    vehicle = System()
    await vehicle.connect(system_address="udp://:14540")

    async for state in vehicle.core.connection_state():
        if state.is_connected:
            print(f"Vehicle discovered")
            break

    firmware_version_hash = await get_firmware_version(vehicle)  
    # print("Found firmware version %s " %firmware_version_hash)
    firmware = asdict(firmware_version_hash)
    logging.info("Firmware and version hash %s"% firmware['flight_sw_version'])
    
    registered_flight_module_id = await get_flight_module_number(vehicle)
    # print("Found registered flight module %s"% registered_flight_module_id)  

    rfm = asdict(registered_flight_module_id)

    logging.info("RFM ID %s"% rfm['hardware_uid'])
    hardware_uid = rfm['hardware_uid'] if rfm['hardware_uid'] != '000000000000000000000000000000000000' else '004E00403237511538343932'

    # Check Aircraft in Aerobridge
    my_aerobridge_client = aerobridgetools.AerobridgeClient(aerobridge_url= env.get('AEROBRIDGE_URL'), token=auth_token['access_token'], authority_url = env.get('PASSPORT_URL'))
    aircraft_active_check = False

    aircraft_details = my_aerobridge_client.get_aircraft_by_flight_controller_id(registered_flight_module_id= hardware_uid)
    if aircraft_details.status_code ==200:
        logging.info("Successfully found aircraft with matching hardware uid in management server %s" % hardware_uid)
        aircraft_data = aircraft_details.json()
        if aircraft_data['status']:
            logging.info("Aircraft is marked as active in the management server") 
            aircraft_active_check = True
        

    # Aircraft is active, check firmware
    if aircraft_active_check:

        aerobridge_firmware = my_aerobridge_client.get_firmware_by_flight_controller_id(registered_flight_module_id= hardware_uid)
        
        if aerobridge_firmware.status_code == 200:
            firmware_details = aerobridge_firmware.json()
            
            if firmware_details['version'] == firmware['flight_sw_version']:
                logging.info("Firmware version in the vehile and management server match!")
                print("Drone can be armed!")
            else:
                logging.info("Firmware version in the vehile and management server do not match!")
                print("Firmware version mismatch, drone cannot be armed")
        else: 
            logger.error("Error in getting firmware version details from Aerobridge %s" % aerobridge_firmware)    

        # Check RFM in Aerobridge
    else:
        logging.error("Aircraft is not active, it cannot be armed.")
        


async def get_firmware_version(drone: System) -> FirmwareVersionAndHash:
    got_info = False 
    
    firmware_version_hash = None
    while not got_info:
        
        try:
            info = await drone.info.get_version()
        except InfoError as ie:
            logger.debug("Error in getting firmware version details %s" % ie)            
        else:            
            flight_sw_version = str(info.flight_sw_major) + '.' + str(info.flight_sw_minor) + '.' + str(info.flight_sw_patch)
            flight_sw_git_hash = info.flight_sw_git_hash       
            if '\x00' in flight_sw_git_hash:
                flight_sw_git_hash=''.join(flight_sw_git_hash.split('\x00'))     
            
            firmware_version_hash = FirmwareVersionAndHash(flight_sw_version=flight_sw_version, flight_sw_git_hash= flight_sw_git_hash)        
            got_info = True

    return firmware_version_hash 


async def get_flight_module_number(drone: System) -> HardwareUID:
    got_info = False 
    max_tries = 25
    hardware_uid = None
    while (not got_info) and (max_tries > 0):
        max_tries -= 1
        try:
            drone_id = await drone.info.get_identification()
        except InfoError as ie:
            logger.debug("Error in getting identification version details %s" % ie)            
        else:            
            hardware_uid = drone_id.hardware_uid
            if '\x00' in hardware_uid:
                hardware_uid=''.join(hardware_uid.split('\x00'))     
                 
            hardware_uid = HardwareUID(hardware_uid=hardware_uid)
            got_info = True

    return hardware_uid 




if __name__ == '__main__':
    # Start the main function
    asyncio.ensure_future(run())

    # Runs the event loop until the program is canceled with e.g. CTRL-C
    asyncio.get_event_loop().run_forever()