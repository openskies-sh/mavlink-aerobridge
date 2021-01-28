
from __future__ import print_function

from pymavlink import mavutil
from time import sleep
import os
from argparse import ArgumentParser
parser = ArgumentParser(description=__doc__)

os.environ["MAVLINK20"] = "1"

parser.add_argument("--baudrate", type=int,
                  help="master port baud rate", default=115200)
parser.add_argument("--device", default='tcp:127.0.0.1:5762',help="SITL")
parser.add_argument("--source-system", dest='SOURCE_SYSTEM', type=int,
                  default=1, help='MAVLink source system for this GCS')
args = parser.parse_args()

# def wait_heartbeat(m):    
    
#     print("Waiting for APM heartbeat")
#     msg = m.recv_match(type=['SYS_STATUS'], blocking=True)    
#     print("Heartbeat from APM (system %u component %u)" % (m.target_system, m.target_component))
    

def wait_id(m):
    received_params =[]
    '''wait for a heartbeat so we know the target system IDs'''
    print("Waiting for DRONEID")
    msg = m.recv_match(type=['AUTOPILOT_VERSION'], blocking=True)
    print("\nMessage Dictionary: %s" % msg.to_dict())
    return received_params


def get_specified_params(mavconn, params):
    '''given a mavlink_connection, gets the parameters with the names specified in params'''    
    received_params =[]# send all the "get parameter" requests
    for param in params:        
        mavconn.param_fetch_one(param)# try to receive a number of parameters equal to the length of params.
        # note that because we pass a timeout to recv_match, if a parameter# isn't found, None will be returned 
        while len(received_params)< len(params):
            msg = mavconn.recv_match(type='PARAM_VALUE', blocking=True,timeout=1)        
            received_params.append(msg)
        return received_params


def get_all_params(mavconn):
    '''given a mavlink_connection, gets the parameters with the names specified in params'''    
    received_params =[] # send the "get all parameters" request    
    mavconn.param_fetch_all()
    while mavconn.param_fetch_complete():
        msg = mavconn.recv_match(type='PARAM_VALUE', blocking=True,timeout=1)        
        received_params.append(msg)

    return received_params
# create a mavlink serial instance
master = mavutil.mavlink_connection(args.device, baud=args.baudrate, source_system=args.SOURCE_SYSTEM)
# params = master.param_fetch_all()

# wait_id(master)
# params = get_all_params(master)
# print(params)
# for p in params:# don't print None params - ones we requested that didn't exist
#     if not p:
#         continue
#     print(str(p.param_id),'\t', p.param_value )
# master.close()
# wait for the heartbeat msg to find the system ID
# wait_heartbeat(master)

## Get the autopilot version
# print(dir(master.mav))
master.mav.autopilot_version_request_send(master.target_system, master.target_component)
wait_id(master)
master.close()