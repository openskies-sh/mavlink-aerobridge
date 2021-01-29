
from __future__ import print_function
import base64
from pymavlink import mavutil
from argparse import ArgumentParser
parser = ArgumentParser(description=__doc__)

## Please note UID2 requires you are using Mavlink 2

# os.environ["MAVLINK20"] = "1"
# export MAVLINK20=1

parser.add_argument("--baudrate", type=int,
                  help="master port baud rate", default=115200)
parser.add_argument("--device", default='tcp:127.0.0.1:5762',help="SITL")
parser.add_argument("--source-system", dest='SOURCE_SYSTEM', type=int,
                  default=1, help='MAVLink source system for this GCS')
args = parser.parse_args()


def wait_id(m):
        
    def encode(message):
        message_bytes = message.encode('ascii')
        base64_bytes = base64.b64encode(message_bytes)
        base64_message = base64_bytes.decode('ascii')
        return base64_message

    def decode(base64_message):
        base64_bytes = base64_message.encode('ascii')
        message_bytes = base64.b64decode(base64_bytes)
        message = message_bytes.decode('ascii')
        return message

    '''wait for a heartbeat so we know the target system IDs'''
    print("Waiting for DRONEID")
    msg = m.recv_match(type=['AUTOPILOT_VERSION'], blocking=True)
    msg_dict = msg.to_dict()
    uid2 = msg_dict.get('uid2', 0)
    if uid2:        
        uid_string = ' '.join([str(elem) for elem in uid2]) 
        encoded = encode(uid_string)
        print ("Encoded Drone ID %s" % encoded)
        return encoded
    else: 
        print("No UID2 found")        
        print("\nMessage Dictionary: %s" % msg_dict)


master = mavutil.mavlink_connection(args.device, baud=args.baudrate, source_system=args.SOURCE_SYSTEM)

master.mav.autopilot_version_request_send(master.target_system, master.target_component)
wait_id(master)
master.close()