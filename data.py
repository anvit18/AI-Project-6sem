import aiohttp
import pysmartthings
import asyncio
import pandas as pd

#input token
token='cf38ea00-7214-4a55-af8e-a0877eb6237f'

async def collect():
    async with aiohttp.ClientSession() as session:
        api = pysmartthings.SmartThings(session, token)
        devices = await api.devices()
        devices_data = []

        for device in devices:
            for capability in device.capabilities:
                device_info = {
                    'device_id': device.device_id,
                    'label': device.label,
                    'command_name': capability
                    }
                devices_data.append(device_info)

    # Create a DataFrame from the collected data
    df = pd.DataFrame(devices_data)

    # Save the collected data to a CSV file



    df.to_csv("data.csv", index=False)         # update this path accordingly

loop = asyncio.get_event_loop()
loop.run_until_complete(collect())
loop.close()


