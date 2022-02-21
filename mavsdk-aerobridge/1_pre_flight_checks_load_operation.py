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
import tempfile
import os

parser = argparse.ArgumentParser(description='Load mission into drone and arm')
parser.add_argument("-o", "--operation_id", type=str, help ="Specify a Aerobridge Flight Operation ID, e.g. try 3408bce9-dbab-4665-abfc-8ea03b0ad871")

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
# Set logging level for messages
logger = logging.getLogger("mavlink-aerobridge")
logging.getLogger("chardet.charsetprober").disabled = True
logger.setLevel(logging.INFO)

# This file checks the drone ID and firmware version against one stored in the management server and allows arming / disarming of the drone

def generate_public_key_pem(jwks):
    # This method converts the JWKS JSON to return a dict of the key id and PEM formatted JSON.

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
    # This is the main function to execute the preflight checks, for loading the operation.

    my_authorization_helper = aerobridgetools.AuthorityCredentialsGetter(client_id = env.get('PASSPORT_CLIENT_ID', None), client_secret= env.get('PASSPORT_CLIENT_SECRET', None), audience = env.get('PASSPORT_AUDIENCE', None), base_url= env.get('PASSPORT_URL') ,token_endpoint = env.get('PASSPORT_TOKEN_ENDPOINT'), jwks_endpoint=env.get('PASSPORT_JWKS_ENDPOINT'))
    logging.info("Getting token from Authority server")
    auth_token = my_authorization_helper.get_credentials()       
    try: 
        assert 'access_token' in auth_token.keys()
    except AssertionError as ae: 
        logging.info("Error in getting access token from auth server %s" % auth_token)
        print("Error in getting access token")
        exit()
    else:
        logging.info("Successfully retrieved access token") 
    logging.info("Getting public key from Authority server")
    jwks = my_authorization_helper.get_public_key()    
    # Convert public key to PEM and send to drone
    logging.debug("Converting JWKS to PEM format")
    pem = generate_public_key_pem(jwks)
    logging.debug("JWKS to PEM conversion successful")    
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
    # When running against SITL sometimes the hardware ID is a series of 0s, if that is the case we use a "real" id as is stored in Aerobridge Testflight
    hardware_uid = rfm['hardware_uid'] if rfm['hardware_uid'] != '000000000000000000000000000000000000' else '004E00403237511538343932'
    
    # Check Aircraft in Aerobridge
    my_aerobridge_client = aerobridgetools.AerobridgeClient(aerobridge_url= env.get('AEROBRIDGE_URL'), token=auth_token['access_token'])

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
            
            firmware_dict = {'aerobridge_firmware':firmware_details['version'],'board_firmware':firmware['flight_sw_version']}
            if firmware_details['version'] == firmware['flight_sw_version']:
                logging.info("Firmware version in the vehile and management server match!")
                print("Firmware check validated and complete")
            else:
                logging.info("Firmware version in the vehile and management server do not match!")
                print("Firmware version mismatch {board_firmware} on the drone vs {aerobridge_firmware} on Aerobridge, therefore drone cannot be armed!".format(**firmware_dict))
                exit()
        else: 
            logger.error("Error in getting firmware version details for the drone from Aerobridge %s" % aerobridge_firmware)               
            exit() 

    else:
        logging.error("Aircraft is not active, it cannot be armed.")        
        exit()
    permission_granted = False
    plan_id = '0'
    if aircraft_active_check:    
        # All checks passed, download flight operation permission and public key in Aerobridge
        operation_permission= my_aerobridge_client.download_flight_permission(operation_id=operation_id)
        if operation_permission.status_code == 200:
            logging.info("Successfully found permission with operation id %s in management server" % operation_id)
            permission_data = operation_permission.json()
            logging.info("Permission for flight successfully retrieved") 
            
            if permission_data['status_code'] == "granted":
                logging.info("Permission has been issued for this flight")
                permission_granted = True                
                plan_id = permission_data['operation']['flight_plan']
            else:
                print("Cannot arm drone, permission status is %s" % permission_data['status_code'])                
                exit()
    mission_plan_data = False

    if permission_granted:
        # Flight permission has been granted download the mission plan 
        # All checks passed, download flight operation permission and public key    
        flight_plan_details = my_aerobridge_client.download_flight_plan(plan_id=plan_id)
        if flight_plan_details.status_code == 200:
            logging.info("Successfully found flight plan with id %s in management server" % plan_id)
            flight_plan_data = flight_plan_details.json()
            logging.info("Plan data for mission successfully retrieved") 
            mission_plan_data = flight_plan_data['plan_file_json']
        else:
            print("Plan data for the operation cannot be retrieved")
            exit()
    # Send mission data
    if mission_plan_data: 
        mission_file = tempfile.NamedTemporaryFile(delete=False)
        try:
            with open(mission_file.name, 'w') as f:
                f.writelines(json.dumps(mission_plan_data))
        except Exception as e: 
            logging.error("Error in writing file details")
            exit()
        else:
            mission_import_data = await vehicle.mission_raw.import_qgroundcontrol_mission(mission_file.name)
            print(f"{len(mission_import_data.mission_items)} mission items imported")
        finally:
            mission_file.close()
            os.unlink(mission_file.name)
        
        logging.info("Uploading mission file to the aircraft..")
        await vehicle.mission_raw.upload_mission(mission_import_data.mission_items)
        await vehicle.mission.set_return_to_launch_after_mission(True)
        logging.info("Mission File uploaded")
        print("Mission uploaded succesfully")

    # Write Token and Public Key
    logging.info("Creating 'guardian' directory on the board..")
    guardian_directory = await vehicle.ftp.create_directory("guardian")
    logging.info("Guardian directory successfully created!")

    # Create a temporary file to hold PEM
    pem_file = tempfile.NamedTemporaryFile(prefix='auth_server_public_key', suffix='.pem',delete = False)

    try:
        logging.debug("Writing PEM file data")
        with open(pem_file.name, 'wb') as f:
            f.write(pem)
    except Exception as e: 
        logging.error("Error in writing file details %s" % e)
        exit()
    else:
        # send file to drone         
        logging.info("Uploading public key to the drone")
        pem_upload = vehicle.ftp.upload(pem_file.name, guardian_directory)
        logging.info("PEM File uploaded successfully")
    finally:
        pem_file.close()
        os.unlink(pem_file.name)
        logging.debug("PEM file succesfully deleted")

    # Create a file to hold permission OTP
    auth_token_file = tempfile.NamedTemporaryFile(prefix='guardian.jwt', suffix='.json', delete = False)
    try:
        with open(auth_token_file.name, 'w') as f:
            f.writelines(json.dumps(auth_token))
    except Exception as e: 
        logging.error("Error in writing file details")
        exit()
    else:
        # send file to drone 
        auth_token_upload = vehicle.ftp.upload(auth_token_file.name, guardian_directory)
    finally:
        auth_token_file.close()
        os.unlink(auth_token_file.name)

    # All checks done, drone ready to be armed. 
    print("All checks passed, flight permission, public key and mission transferred to the drone.")
    

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
            # remove spaces, in the simulator sometimes data is returned with are trailing spaces    
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
            # remove spaces, in the simulator sometimes data is returned with are trailing spaces    
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
        print("A valid Operation ID (UUID) from your Aerobridge instance must be provided before arming the drone with a mission, e.g. try -o 3408bce9-dbab-4665-abfc-8ea03b0ad871" )
        exit()

    loop = asyncio.get_event_loop()
    asyncio.set_event_loop(loop)
    tasks = asyncio.gather(run(operation_id))
    try:
        loop.run_until_complete(tasks)
    except (Exception, KeyboardInterrupt) as e:
        print('ERROR', str(e))
        exit()