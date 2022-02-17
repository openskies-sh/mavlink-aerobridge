
import asyncio
from mavsdk import System

async def run():
    drone = System()
    # await drone.connect(system_address="tcp://127.0.0.1:5762")

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"Drone discovered!")
            break
    
    info = await drone.info.get_identification()
    print(info)


if __name__ == "__main__":
    asyncio.ensure_future(run())
    asyncio.get_event_loop().run_forever()