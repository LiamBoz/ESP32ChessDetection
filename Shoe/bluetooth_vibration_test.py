import asyncio
from bleak import BleakClient

# Define the UUIDs
SERVICE_UUID = "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
CHARACTERISTIC_UUID = "beb5483e-36e1-4688-b7f5-ea07361b26a8"

async def send_data(client, data):
    await client.write_gatt_char(CHARACTERISTIC_UUID, data)

async def main():
    address = "D4:F9:8D:04:17:46"
    
    async with BleakClient(address) as client:
        while True:
            user_input = input("Enter data to send (q to quit): ")
            if user_input == 'q':
                break

            data_to_send = user_input.encode('utf-8')
            await send_data(client, data_to_send)
            print(f"Sent: {user_input}")

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
