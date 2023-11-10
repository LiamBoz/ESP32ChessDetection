import asyncio
from bleak import BleakClient
import chess
import chess.engine

# Define the UUIDs
SERVICE_UUID = "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
CHARACTERISTIC_UUID = "beb5483e-36e1-4688-b7f5-ea07361b26a8"


def print_board(board):
    # Function to print the board in a readable format
    print("  a b c d e f g h")
    print(" +----------------")
    for i in range(7, -1, -1):  # Iterate in reverse order (from 7 to 0)
        print(f"{i+1}|", end=" ")  # Add 1 to i to display rows as 1-indexed
        for j in range(8):
            piece = board.piece_at(8*i+j)
            if piece is not None:
                print(piece.symbol(), end=" ")
            else:
                print(".", end=" ")
        print("|")

def get_engine_move(board, engine_path):
    # Function to get the engine's recommended move
    with chess.engine.SimpleEngine.popen_uci(engine_path) as engine:
        result = engine.play(board, chess.engine.Limit(time=0.1))
        print(result.move)
        #print(board.piece_at(square))
        return result.move

async def send_data(client, data):
    await client.write_gatt_char(CHARACTERISTIC_UUID, data)

async def main():
    # old mac address
    address = "D4:F9:8D:04:17:46"
    # new mac address
    # address = "D4:F9:8D:01:48:2A"
    
    async with BleakClient(address) as client:
        while True:

            engine_path = "C://Users//durpy//Downloads//stockfish-windows-x86-64-avx2//stockfish//stockfish-windows-x86-64-avx2.exe"  # Update this path with the correct engine path
            board = chess.Board()

            color = input("Choose your color (w for white, b for black): ")
            if color.lower() not in ('w', 'b'):
                print("Invalid choice. Please enter 'w' for white or 'b' for black.")
                return
            
            if color.lower() == 'b':
                board = board.mirror()
                first_move = True

            while not board.is_game_over():
                print_board(board)  # Display the board with rows and columns

                # User makes a move
                move = input(f"Enter your move for {'white' if board.turn == chess.WHITE else 'black'} (e.g., e2e4): ")
                try:
                    board.push_uci(move)
                except ValueError:
                    print("Invalid move! Try again.")
                    continue

                # Engine recommends a move
                if not board.is_game_over():
                    engine_move = get_engine_move(board, engine_path)
                    square = engine_move.uci()[:2]    
                    PIECE = board.piece_at(chess.parse_square(square))
                    print(f"Engine recommends: {engine_move.uci()}")
                    #board.push(engine_move)  # Make the engine's move on the board

                data_to_send =  PIECE.encode('utf-8')
                await send_data(client, data_to_send)
                print(f"Sent: {PIECE}")

            print(f"Game over: {board.result()}")




loop = asyncio.get_event_loop()
loop.run_until_complete(main())
