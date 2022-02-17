import asyncio
from mavsdk import System
from mavsdk.info import InfoError
async def run():

    # Init the drone
    vehicle = System()
    await vehicle.connect(system_address="udp://:14540")

    async for state in vehicle.core.connection_state():
        if state.is_connected:
            print(f"Vehicle discovered")
            break

    got_info = False 
    while not got_info:
        try:
            id_info = await vehicle.info.get_version()
        except InfoError as infoError:
            print(infoError)
        else: 
            print(id_info)
            got_info = True

if __name__ == '__main__':
    # Start the main function
    asyncio.ensure_future(run())

    # Runs the event loop until the program is canceled with e.g. CTRL-C
    asyncio.get_event_loop().run_forever()