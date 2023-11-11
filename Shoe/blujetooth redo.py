import asyncio
from bleak import BleakClient
from simple_chess_game_again import *


dict = {'p':1,'P':1,'n':2,'N':2,'b':3,'B':3,'r':4,'R':4,'Q':5,'q':5,'k':6,'K':6}
dict2 = {'a':'1','b':'2','c':'3','d':'4','e':'5','f':'6','g':'7','h':'8'}


# Define the UUIDs
SERVICE_UUID = "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
CHARACTERISTIC_UUID = "beb5483e-36e1-4688-b7f5-ea07361b26a8"

async def send_data(client, data):
    await client.write_gatt_char(CHARACTERISTIC_UUID, data)

async def main():
    # old mac address
    # address = "D4:F9:8D:04:17:46"
    # new mac address
    address = "D4:F9:8D:01:48:2A"

    
    async with BleakClient(address) as client:
        while True:
            try:
                Move = input("Enter Move:")

                piece = dict[Move[0]]
                row = dict2[Move[1]]
                col = Move[2]
                piece_row_col = f'{piece}+{row}+{col}'
                data_to_send =  piece_row_col.encode('utf-8')
                await send_data(client, data_to_send)
                print(f"Sent: {piece_row_col}")
                
            except:
                print("Invalid Move. Try again.")



loop = asyncio.get_event_loop()
loop.run_until_complete(main())
