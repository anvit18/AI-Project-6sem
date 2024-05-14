from uuid import uuid4
from nicegui import ui
from data import collect
from identify import extract_device_and_command
from command import execute_command


messages = []
bot = str(uuid4())



@ui.refreshable
def chat_messages(own_id):
    for user_id, avatar, text in messages:
        ui.chat_message(avatar=avatar, text=text, sent=user_id==own_id)

def botResponse(text):
    messages.append((bot, f'https://robohash.org/{bot}?bgset=bg2', text))
    chat_messages.refresh()

@ui.page('/')
async def index():
    await collect()
    async def send():
        messages.append((user, avatar, text.value))
        chat_messages.refresh()
        first = text.value
        devices, device_ids, command = extract_device_and_command(first)
        text.value = ''
        #botResponse(f"Devices Found: {devices}, Device_Ids: {device_ids}, Desired Command: {command}")

        if devices and command:
            for device_id in device_ids:
                await execute_command(device_id, command)
            botResponse(f"Command '{command}' executed on device '{devices}'.")
        else:
            botResponse("Device or Command couldn't be identified. Please try again.")

    user = str(uuid4())
    avatar = f'https://robohash.org/{user}?bgset=bg2'
    with ui.column().classes('w-full items-stretch'):
        chat_messages(user)

    with ui.footer().classes('bg-white'):
        with ui.row().classes('w-full items-center'):
            with ui.avatar():
                ui.image(avatar)
            text = ui.input(placeholder='message') \
                .props('rounded outlined').classes('flex-grow') \
                .on('keydown.enter', send)

ui.run()