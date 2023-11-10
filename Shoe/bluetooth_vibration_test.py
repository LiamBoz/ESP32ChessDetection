import asyncio
from bleak import BleakClient
from simple_chess_game_again import *

# Define the UUIDs
SERVICE_UUID = "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
CHARACTERISTIC_UUID = "beb5483e-36e1-4688-b7f5-ea07361b26a8"

async def send_data(client, data):
    await client.write_gatt_char(CHARACTERISTIC_UUID, data)

async def main():
    # old mac address
    address = "D4:F9:8D:04:17:46"
    # new mac address
    # address = "D4:F9:8D:01:48:2A"
    
    async with BleakClient(address) as client:
        while True:
            piece = input("Enter piece number: ")
            if piece.lower() == 'exit':
                break
            row = input("Enter row: ")
            if row.lower() == 'exit':
                break
            col = input("Enter column: ")
            if col.lower() == 'exit':
                break
            piece_row_col = f'{piece}+{row}+{col}'

            data_to_send =  piece_row_col.encode('utf-8')
            await send_data(client, data_to_send)
            print(f"Sent: {piece_row_col}")

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
