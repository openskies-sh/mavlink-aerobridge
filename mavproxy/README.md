# Using MAVProxy to communicate with the drone

In this section, we will detail how to install and detail the steps to communicate with the drone in the context of NPNT. Mainly you will have to retrieve and send files, logs and also the ID.  

## Pre-requisite: Install Mavproxy

Follow the instructions [here](https://ardupilot.org/mavproxy/docs/getting_started/download_and_installation.html) to install Mavproxy for your machine and review some of the [startup options](https://ardupilot.org/mavproxy/docs/getting_started/starting.html)

## Pre-requisite: Setting the appropriate connection string

Follow instructions here to [start MAVProxy](https://ardupilot.org/mavproxy/docs/getting_started/quickstart.html) with your setup, note your connection string can accommodate both a live drone or a SITL

## 1. Getting Drone ID

Once you have connected and launched MAVProxy, to get your drone ID, please execute the following commands in the console

```
watch AUTOPILOT_*
module load message
message AUTOPILOT_VERSION_REQUEST 0 0
```

This will give a output similar to the following:

`1: AUTOPILOT_VERSION {capabilities : 64495, flight_sw_version : 67174400, middleware_sw_version : 0, os_sw_version : 0, board_version : 0, flight_custom_version : [97, 97, 49, 100, 49, 99, 54, 53], middleware_custom_version : [0, 0, 0, 0, 0, 0, 0, 0], os_custom_version : [0, 0, 0, 0, 0, 0, 0, 0], vendor_id : 0, product_id : 0, uid : 0, uid2 : [85, 28, 99, 105, 73, 19, 100, 77, 07, 84, 32, 46, 19, 33, 96, 100, 28, 10]}`

The `uid2` parameter is the necessary, you can copy that and then update that with the Drone ID on Aerobridge.

## 2. Getting Public Key

Getting the Public Key is done via FTP and a few other comments. You will need to install the appropriate firmware before you can use this. Follow the following steps to test out FTP.
```
module load ftp
ftp list
ftp get logs/LASTLOG.txt
ftp put LASTLOG.txt logs/NEWLOG.txt
```

## 3. Upload permission artefact

TBC

## 4. Getting Drone Logs

TBC

## 5. Testing signed Ardupilot firmware and secure bootloader

`https://github.com/ArduPilot/ardupilot/pull/16738`

1. Clone and initialize the ardupilot repository for pr-digitalsky-india
```
# Make a new folder for the project
mkdir npnt_ardupilot; cd npnt_ardupilot

git clone https://github.com/CubePilot/ardupilot.git --branch pr-digitalsky-india
cd ardupilot
git submodule update --init --recursive
```

2. Generating the firmware and secure bootloader
```
# Generate key
openssl ecparam -out privatekey.pem -name secp256r1 -genkey
# Create virtual environment
python3 -m venv ./npnt_venv
source npnt_venv/bin/activate
pip3 install pycryptodome future pyserial

# Generate a Secure Bootloader using following command:
./Tools/scripts/build_bootloaders.py CubeOrange --secure-key ../privatekey.pem --debug

# Generate a firmware file with following command
./waf configure --board CubeOrange --secure-key ../privatekey.pem --ds-publickey modules/libnpnt/test/dgca_pubkey.der --debug

# Upload to target
./waf copter --upload
```

3. Setting pin and flashing secure bootloader using modified mavproxy and pymavlink

```
git clone https://github.com/CubePilot/MAVProxy.git --branch pr-securebootloader
source npnt_env/bin/activate
pip3 install -r requirements.txt

# Uninstall any other mavproxy installations
pip uninstall mavproxy

# Then install the newly cloned mavproxy
python setup.py install
# Uninstall pymavlink already on system
pip uninstall pymavlink
# Install pymavlink from inside ardupilot
cd /modules/mavlink/pymavlink
python setup.py install

# Launch mavproxy
mavproxy.py --master=/dev/ttyACM0

changepin 0 123456 # sets up pincode <1000 to 1000000>
setpin 123456 # sets input pin, verified when using secure features like update bootloader
flashsecurebootloader

# Power cycle to start key generation and bootloader flash
```
