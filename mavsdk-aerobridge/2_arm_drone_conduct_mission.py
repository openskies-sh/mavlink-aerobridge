import asyncio, time
from mavsdk import System
import flightblendertools
from dataclasses import dataclass, asdict
from typing import Optional
import arrow, json

@dataclass
class RIDAircraftPosition:
  lat: float
  lng: float
  alt: float
  accuracy_h: str
  accuracy_v: str
  extrapolated: Optional[bool]
  pressure_altitude: Optional[float]

@dataclass
class RIDHeight:
  distance: float
  reference: str


@dataclass
class RIDAircraftState:
  timestamp: str
  timestamp_accuracy: float
  speed_accuracy: str
  position: RIDAircraftPosition
  operational_status: Optional[str]= None
  track: Optional[float] = None
  speed: Optional[float] = None
  vertical_speed: Optional[float] = None
  height: Optional[RIDHeight] = None

  def as_dict(self):
      data = asdict(self)
      return {key: value for key, value in data.items() if value is not None}


async def run():
    drone = System()
    await drone.connect(system_address="udp://:14540")
    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"Drone discovered!")
            break


    my_credentials = flightblendertools.PassportCredentialsGetter()
    credentials = my_credentials.get_cached_credentials()

    my_blender_uploader = flightblendertools.BlenderUploader(credentials=credentials)
    start_time = time.time()
    print_mission_progress_task = asyncio.ensure_future(print_mission_progress(drone))
    position_task=  asyncio.ensure_future(get_position_x_seconds(3, get_drone_position,drone, start_time, my_blender_uploader ))    
    running_tasks = [print_mission_progress_task, position_task]
    termination_task = asyncio.ensure_future(observe_is_in_air(drone, running_tasks))
    
    print("-- Arming")
    await drone.action.arm()
    print("-- Starting mission")
    await drone.mission.start_mission()
    await termination_task

async def print_mission_progress(drone):
    async for mission_progress in drone.mission.mission_progress():
        print(f"Mission progress: "
              f"{mission_progress.current}/"
              f"{mission_progress.total}")

async def get_position_x_seconds(timeout, get_drone_position, drone, start_time, my_blender_uploader):
    while True:
        await asyncio.sleep(timeout)
        position = await get_drone_position(drone, start_time)   
        # send position to Flight Blender
     
     
        position = RIDAircraftPosition(
                "lat": position['lat'],
                "lng": position['lng'],
                "alt": position['altitude'],
                "accuracy_h": "HAUnkown",
                "accuracy_v": "VAUnknown",
                "extrapolated": False)
        rid_json = RIDAircraftState(timestamp=arrow.now().isoformat(),operational_status="Airborne", position = position, height=RIDHeight(distance = 50.0, reference = "TakeoffLocation"), track=181.69, speed= 4.91, timestamp_accuracy=0.0, speed_accuracy="SA3mps", vertical_speed=0.0)
        
        my_blender_uploader.upload_to_blender(rid_json = json.dumps(asdict(rid_json)))
        print(position)

async def observe_is_in_air(drone, running_tasks):
    """ Monitors whether the drone is flying or not and
    returns after landing """
    was_in_air = False
    async for is_in_air in drone.telemetry.in_air():
        if is_in_air:
            was_in_air = is_in_air
        if was_in_air and not is_in_air:
            for task in running_tasks:
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass
            await asyncio.get_event_loop().shutdown_asyncgens()
            return

async def get_drone_position( drone, start_time):
    print(round(time.time() - start_time, 1), "Position Captured")
    async for position in drone.telemetry.position():        
        return position

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())