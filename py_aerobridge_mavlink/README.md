# Scripts for connecting to RFM to perform NPNT operations

These scripts will help you connect to your drone / SITL and perform actions (fetch / send) data necessary for NPNT compliance. Before you begin: 

1. Make sure you have the latest version of pymavlink, you use `pip install pymavlink --upgrade`
2. In case of SITL / Drone, make sure you have the latest versions of Ardrupilot if possible
3. You must use **Mavlink 2** for these to run, you can set your environment variable e.g. `export MAVLINK20=1` on Linux. 

| Script        | Details           | Comments / Known Issues  |
| ------------- |:-------------:| -----:|
| 1-get_drone_id.py  | Get the ID of the flight controller `machine-id`, and encodes it you will need this when you register your drone / flight controller with Digital Sky / DGCA | - |
