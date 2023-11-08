import chess
import chess.svg
import chess.engine
import tkinter as tk
from tkinter import messagebox
import subprocess
import time
import socket

# Global variables
start_time = None
client_socket = None

def svg_to_png():
    subprocess.run(["C:\\Users\\cayde\\Desktop\\Shit\\inkscape\\bin\\inkscape.exe", "board.svg", "--export-type=png", "--export-filename=board.png"])

def update_display():
    svg_data = chess.svg.board(board=board)
    with open("board.svg", "w") as svg_file:
        svg_file.write(svg_data)
    svg_to_png()
    img = tk.PhotoImage(file="board.png")
    board_display.configure(image=img)
    board_display.image = img

def make_move():
    global board, start_time
    move = move_entry.get()
    if chess.Move.from_uci(move) not in board.legal_moves:
        messagebox.showerror("Invalid Move", "Invalid move! Try again.")
        return
    board.push_uci(move)
    update_display()
    move_entry.delete(0, tk.END)
    start_time = time.time()

    if not board.is_game_over():
        play_stockfish_move()

def play_stockfish_move():
    global start_time, client_socket
    with chess.engine.SimpleEngine.popen_uci("C:\\Users\\cayde\\Desktop\\Shit\\stockfish\\stockfish-windows-x86-64-avx2.exe") as engine:
        result = engine.play(board, chess.engine.Limit(time=0.2))
        move = result.move.uci()
        board.push_uci(move)
        update_display()
        if board.is_game_over():
            messagebox.showinfo("Game Over", f"Game over: {board.result()}")
        else:
            end_time = time.time()
            move_time = end_time - start_time
            time_label.config(text=f"AI Move Time: {move_time:.2f} seconds")
            print(f"AI move took {move_time:.2f} seconds")

            # Send AI's move to phone
            send_move(client_socket, move)

            # Receive user's move from phone
            user_move = receive_move(client_socket)
            if user_move not in [move.uci() for move in board.legal_moves]:
                messagebox.showerror("Invalid Move", "Invalid move! Try again.")
            else:
                board.push_uci(user_move)
                update_display()

def start_server():
    global client_socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 5555))  # Choose a port (e.g., 5555)
    server_socket.listen(1)

    print("Waiting for connection...")
    client_socket, client_address = server_socket.accept()
    print(f"Connection from: {client_address}")

def receive_move(client_socket):
    move = client_socket.recv(1024).decode()
    return move

def send_move(client_socket, move):
    client_socket.send(move.encode())

def main():
    global board, board_display, move_entry, time_label

    board = chess.Board()

    root = tk.Tk()
    root.title("Chess Game")

    board_display = tk.Label(root)
    board_display.pack()

    move_label = tk.Label(root, text="Enter your move (e.g., e2e4):")
    move_label.pack()

    move_entry = tk.Entry(root, width=10)
    move_entry.pack()

    move_button = tk.Button(root, text="Make Move", command=make_move)
    move_button.pack()

    time_label = tk.Label(root, text="AI Move Time: ")
    time_label.pack()

    update_display()

    start_server()  # Start the server

    root.mainloop()

if __name__ == "__main__":
    main()
