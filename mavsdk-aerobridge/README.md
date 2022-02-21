# MavSDK <-> Aerobridge connector

This directory has files to implement the Aerobridge guardian workflow for trusted flights. You will need a working Aerobridge instance and the ability to issue and get OAUTH Tokens in the form of JWTs.

## Sequence

1. Pre-flight: Transfer the OTP/JWT, mission and perform pre-arming checks for the drone: `python 1_pre_flight_checks_load_operation.py`
2. Conduct mission and arm `python 2_arm_drone_conduct_mission.py`
3. Upload flight logs `python 3_post_flight_upload_flight_logs.py`

## Install pre-requisites

Use `pip install -r requirements.txt` to install all the pre-requisites. This library uses the MavSDK toolkit to communicate with the drone via Mavlink. It should work as expected with PX4 drones but ArduPilot will display warnings. 