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