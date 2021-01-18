# MAVlink Connectivity for Aerobridge Management Server

This repository enables you to connect to a drone and thereby the Registered Flight Module (RFM) to the Aerobridge Management server. This repository proposes two ways to communicate with the RFM:

- As a __Windows Client__ for installation in Windows Systems
- As a __Cross-platform Client__ for use in Windows, OSX or Linux platforms

both these solutions use the MAVLink Protocol as a the library to interact with RFM.

__January 2021__ : This repository is under heavy development, and not for production use, this is why we are testing two ways of connectivity. The installation instructions and user interface **will** change. 

Manufacturers / Operators: if you want to test / integrate this, join our "Canary program" by registering for our [webinar series](http://webinar.aerobridge.in).

## Installation

### Cross Platform Client

1. Download and unzip the repository
2. Go to the folder `cd py_aerobridge_mavlink`
3. Install the dependencies by using pip e.g. `pip install -r requirements.txt`, this will install pymavlink and other libraries
4. Launch the user interface `python aerobridge_connector.py`

### Windows Client

1. Go to the releases page and download the latest release

## Screenshots

### Windows Based Client

![client](https://i.imgur.com/zHPXFcx.png)

### Python Based Client

![plugin](https://i.imgur.com/8MfVv9P.jpg)

## Development

For technical developer only: You can choose to develop either the Plugin or Client. It is recommended that you have Mission Planner installed and the latest copy of the source downloaded per the instructions [here](https://ardupilot.org/dev/docs/building-mission-planner.html#getting-the-mission-planner-source-code-from-github-into-your-computer)

### Python Client

This client uses the [pygubu](https://github.com/alejandroautalan/pygubu) library to develop the user interface, you can use the grid.ui file to see the interface. The main code that interacts with MavLink is in the `aerobridge_connector.py` module.

### Aerobridge Full Client

The Aerobridge Client Solution extends the [SimpleExample](https://ardupilot.org/dev/docs/building-mission-planner.html#building-the-simpleexample) solution as a part of the MissionPlanner code base. You will need Visual Studio Community Edition, which is available for free. To debug this, do the following:

1. Download the repository, open the `AerobridgeClient.sln` file Visual Studio
2. To check the Mavlink dependency, you can click on `Build -> Rebuild Solution` in Visual Studio