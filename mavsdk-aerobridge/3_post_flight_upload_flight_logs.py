import asyncio
from asyncore import file_dispatcher
from mavsdk import System
import sys
import argparse
import aerobridgetools
import logging
from os import environ as env
from dotenv import load_dotenv, find_dotenv
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

# This file uploads the log objects and sends it to the Aerobridge instance

async def run(operation_id):    
    # This is the main function to upload flight logs from the drone

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

    drone = System()
    await drone.connect(system_address="udp://:14540")

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"Drone discovered and connected!")
            break

    my_aerobridge_client = aerobridgetools.AerobridgeClient(aerobridge_url= env.get('AEROBRIDGE_URL'), token=auth_token['access_token'])

    entries = await get_entries(drone)
    for entry in entries:
        log_file = tempfile.NamedTemporaryFile(delete=False)
        file_progress = await download_log(drone, entry)
        print(file_progress)
        logging.info("File upload complete %s" % file_progress)
        try:
            with open(log_file.name,'r') as l_f:
                log_data = l_f.read()
            logging.info("Uploading log file to Aerobridge")
            my_aerobridge_client.upload_flight_log(operation_id=operation_id, raw_log=log_data)
            logging.info("Log file uploaded successfully")
        except Exception as e: 
            logging.error("Error in uploading log data to Aerobridge: %s" % e)

        finally:             
            os.unlink(log_file.name)
        



async def download_log(drone, entry, file_handle):   
    print(f"Downloading: log {entry.id} from {entry.date}")
    logging.info("File download in progress")
    previous_progress = -1
    async for progress in drone.log_files.download_log_file(entry, file_handle):
        new_progress = round(progress.progress*100)
        if new_progress != previous_progress:
            sys.stdout.write(f"\r{new_progress} %")
            sys.stdout.flush()
            previous_progress = new_progress
    print()


async def get_entries(drone):
    entries = await drone.log_files.get_entries()
    for entry in entries:
        print(f"Log {entry.id} from {entry.date}")
    return entries


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(run())