
from __future__ import print_function

from pymavlink import mavutil


from argparse import ArgumentParser
parser = ArgumentParser(description=__doc__)

parser.add_argument("--baudrate", type=int,
                  help="master port baud rate", default=115200)
parser.add_argument("--device", default='tcp:127.0.0.1:5762',help="SITL")
parser.add_argument("--source-system", dest='SOURCE_SYSTEM', type=int,
                  default=1, help='MAVLink source system for this GCS')
args = parser.parse_args()

def wait_heartbeat(m):
    '''wait for a heartbeat so we know the target system IDs'''
    print("Waiting for APM heartbeat")
    msg = m.recv_match(type=['SYS_STATUS'], blocking=True)
    
    print("\nMessage Dictionary: %s" % msg.to_dict())
    print("Heartbeat from APM (system %u component %u)" % (m.target_system, m.target_component))

def wait_id(m):
    
    print("Waiting for DRONEID")
    msg = m.recv_match(type='AUTOPILOT_VERSION', blocking=True)


    print("\nAutopilot Version as Dictionary: %s" % msg.to_dict())
    print(msg)


# create a mavlink serial instance
master = mavutil.mavlink_connection(args.device, baud=args.baudrate, source_system=args.SOURCE_SYSTEM)

# wait for the heartbeat msg to find the system ID
# wait_heartbeat(master)

## Get the autopilot version
# print(dir(master.mav))
master.mav.autopilot_version_request_send(master.target_system, master.target_component)
wait_id(master)
