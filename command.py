import aiohttp
import pysmartthings
import asyncio

#input Token
token='cf38ea00-7214-4a55-af8e-a0877eb6237f'

async def execute_command(device_id, command_name, args=None):
    async with aiohttp.ClientSession() as session:
        api = pysmartthings.SmartThings(session, token)

        device = await api.devices(device_ids=[device_id])
        device = device[0]

        if command_name == 'switch_on':            
            result = await device.switch_on()
            assert result == True
        elif command_name == 'switch_off':
            result = await device.switch_off()
            assert result == True
        else:
            try:
                result = await device.command('main', command_name, command_name)
                assert result == True
            except:
                print("Unable to perform your desired action.")
                return False
        return True
            
            

#Input the device_id and command_name

# asyncio.run(execute_command('56f5bc2b-9e4a-443d-b146-8a4ba0d3cdd9', 'switch'))



