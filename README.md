# Mission Planner Connectivity for Aerobridge Management Server

This repository enables you to connect Mission Planner Ground Control Station (GCS) and thereby the Registered Flight Module (RFM) to the Aerobridge Management server. This repository proposes two ways to communicate with the RFM using MissionPlanner:

- As a __MissionPlanner Plugin__
- As a __Standalone Client__ using the MAVLink Protocol

__January 2021__ : This repository is under heavy development, and not for production use, this is why we are testing two ways of connectivity. The installation instructions and user interface **will** change. Manufacturers / Operators: if you want to test / integrate this, join our "Canary program" by registering for our [webinar series](http://webinar.aerobridge.in).

## Installation

### Installing the Plugin

For the moment please follow the following steps:

1. Ensure that you have Mission Planner Installed on your PC.
2. Please copy the `Aerobridge_Plugin.cs` file into the `C:\Program Files (x86)\Mission Planner\plugins` directory.
3. Open Mission Planner and go to the `Plan` section
4. Right-click on the map and you will see a Aerobridge menu, click to launch it

### Run the Client

1. Go to the releases page and download the latest release

## Screenshots

### Aerobridge Client

![client](https://imgur.com/zHPXFcx)

### Aerobridge Plugin

![plugin](https://imgur.com/IkSyxtl)

## Development

For technical developer only: You can choose to develop either the Plugin or Client. It is recommended that you have Mission Planner installed and the latest copy of the source downloaded per the instructions [here](https://ardupilot.org/dev/docs/building-mission-planner.html#getting-the-mission-planner-source-code-from-github-into-your-computer)

### Plugin only

The plugin is in the `MissionPLanner.Aerobridge.sln` file in Visual Studio Community Edition for free. If you want to access the Mission Planner Namespace, download the latest solution from [MissionPlanner Releases](https://github.com/ArduPilot/MissionPlanner/releases/) page, open it in Visual Studio Community Edition. Then you can add this solution to your project by following [Microsoft help directions](https://docs.microsoft.com/en-us/sql/ssms/solution/add-an-existing-project-to-a-solution?view=sql-server-ver15)

### Aerobridge Full Client

The Aerobridge Client Solution extends the [SimpleExample](https://ardupilot.org/dev/docs/building-mission-planner.html#building-the-simpleexample) solution as a part of the MissionPlanner code base. You will need Visual Studio Community Edition, which is available for free. To debug this, do the following:

1. Download the Mission Planner [source code](https://github.com/ArduPilot/MissionPlanner/releases/tag/)
2. Unzip the file on for e.g. Desktop
3. Copy the `Aerobridge-FullClient` folder in the `ExtLibs` folder
4. Open the `AerobridgeClient.sln` in Visual Studio
5. You should be able the solution in Visual Studio and edit it. 
6. Make your changes and then send the pull requests to the original code.