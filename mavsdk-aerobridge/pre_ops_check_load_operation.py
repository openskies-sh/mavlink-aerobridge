import asyncio
from mavsdk import System
from mavsdk.info import InfoError
import aerobridgetools
import json
import logging
import sys
from data_definitions import FirmwareVersionAndHash, HardwareUID
from os import environ as env
from dotenv import load_dotenv, find_dotenv
from dataclasses import asdict
import jwt
from cryptography.hazmat.primitives import serialization
import argparse

parser = argparse.ArgumentParser(description='Load mission into drone and arm')
parser.add_argument("-o", "--operation_id", type=str, help ="Specify a Aerobridge Flight Operation ID")


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

def generate_public_key_pem(jwks):
    public_keys = {}
    for jwk in jwks['keys']:
        kid = jwk['kid']
        public_keys[kid] = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk))
    
    public_key = public_keys.get(env.get('PASSPORT_PUBLIC_KEY_ID', None))
    pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo)       
    
    return pem

async def run(operation_id):    
    my_authorization_helper = aerobridgetools.AuthorityCredentialsGetter(client_id = env.get('PASSPORT_CLIENT_ID', None), client_secret= env.get('PASSPORT_CLIENT_SECRET', None), audience = env.get('PASSPORT_AUDIENCE', None), base_url= env.get('PASSPORT_URL') ,token_endpoint = env.get('PASSPORT_TOKEN_ENDPOINT'), jwks_endpoint=env.get('PASSPORT_JWKS_ENDPOINT'))
    logging.info("Getting token from Authority server")
    auth_token = my_authorization_helper.get_credentials()        
    logging.info("Getting public key from Authority server")
    jwks = my_authorization_helper.get_public_key()    
    # Convert public key to PEM and send to drone
    
    pem = generate_public_key_pem(jwks)
    # print(operation_id)

    
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

    else:
        logging.error("Aircraft is not active, it cannot be armed.")
        
    if aircraft_active_check:    
        # All checks passed, download flight operation permission and public key    
        operation_permission = my_aerobridge_client.get_aircraft_by_flight_controller_id(operation_id=operation_id)
        if operation_permission.status_code ==200:
            logging.info("Successfully found permission with operation id %s in management server" % operation_id)
            permission_data = operation_permission.json()
            logging.info("Permission for flight successfully retrieved") 
            if permission_data['status'] == "granted":
                print("Permission Granted")
            else:
                print("Cannot arm drone, permission status %s" % permission_data['status'])
            
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
    args = parser.parse_args()
    operation_id = args.operation_id
    if not operation_id:
        print("A valid operation ID (UUID) from your Aerobridge instance must be provided before arming the drone" )
        exit()

    loop = asyncio.get_event_loop()
    asyncio.set_event_loop(loop)
    tasks = asyncio.gather(run(operation_id))
    try:
        loop.run_until_complete(tasks)
    except (Exception, KeyboardInterrupt) as e:
        print('ERROR', str(e))
        exit()