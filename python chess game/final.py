import chess
import chess.engine
import time

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
        #print(result.move)
        return result.move

def main():
    
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
            print(f"Engine recommends: {engine_move.uci()}")
            #board.push(engine_move)  # Make the engine's move on the board

    print(f"Game over: {board.result()}")

if __name__ == "__main__":
    main()