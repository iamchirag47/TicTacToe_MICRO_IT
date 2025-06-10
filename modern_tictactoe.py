import tkinter as tk
from tkinter import messagebox
import pygame

# Initialize sound engine
pygame.mixer.init()

# Load sound files
click_sound = pygame.mixer.Sound("click.wav")
win_sound = pygame.mixer.Sound("win.wav")

# Game state variables
player = "X"
board = [["" for _ in range(3)] for _ in range(3)]
buttons = [[None for _ in range(3)] for _ in range(3)]
player1_name = ""
player2_name = ""
turn_label = None


def play_click_sound():
    click_sound.play()


def play_win_sound():
    win_sound.play()


def check_winner(p):
    for i in range(3):
        if all(board[i][j] == p for j in range(3)) or all(board[j][i] == p for j in range(3)):
            return True
    if all(board[i][i] == p for i in range(3)) or all(board[i][2 - i] == p for i in range(3)):
        return True
    return False


def is_draw():
    return all(board[i][j] != "" for i in range(3) for j in range(3))


def reset_board():
    global player, board
    player = "X"
    board = [["" for _ in range(3)] for _ in range(3)]
    turn_label.config(text=f"{player1_name}'s Turn (X)", fg="#00E5FF")
    for i in range(3):
        for j in range(3):
            buttons[i][j].config(text="", bg="#1e1e1e")


def on_click(row, col):
    global player
    if board[row][col] == "":
        board[row][col] = player
        buttons[row][col].config(
            text=player,
            fg="#FF4081" if player == "X" else "#00E5FF",
            bg="#2c2c2c"
        )
        play_click_sound()

        if check_winner(player):
            play_win_sound()
            winner = player1_name if player == "X" else player2_name
            messagebox.showinfo("🎉 Game Over", f"{winner} ({player}) wins!")
            reset_board()
        elif is_draw():
            messagebox.showinfo("Game Over", "It's a draw!")
            reset_board()
        else:
            player = "O" if player == "X" else "X"
            turn_label.config(
                text=f"{player1_name if player == 'X' else player2_name}'s Turn ({player})",
                fg="#FF4081" if player == "X" else "#00E5FF"
            )


def setup_board():
    global root, buttons, turn_label
    root = tk.Tk()
    root.title("🔥 Modern Tic-Tac-Toe")
    root.configure(bg="#121212")

    turn_label = tk.Label(root, text=f"{player1_name}'s Turn (X)", font=("Helvetica", 16, "bold"),
                          fg="#00E5FF", bg="#121212")
    turn_label.grid(row=0, column=0, columnspan=3, pady=10)

    for i in range(3):
        for j in range(3):
            btn = tk.Button(root, text="", font=("Courier New", 32, "bold"), width=4, height=2,
                            bg="#1e1e1e", fg="#CCCCCC", activebackground="#333",
                            command=lambda r=i, c=j: on_click(r, c))
            btn.grid(row=i+1, column=j, padx=5, pady=5)
            buttons[i][j] = btn

    root.mainloop()


def get_player_names():
    def start_game():
        global player1_name, player2_name
        player1_name = entry1.get() or "Player 1"
        player2_name = entry2.get() or "Player 2"
        name_window.destroy()
        setup_board()

    name_window = tk.Tk()
    name_window.title("Enter Player Names")
    name_window.configure(bg="#121212")

    tk.Label(name_window, text="Player X Name:", bg="#121212", fg="#FFFFFF").pack(pady=5)
    entry1 = tk.Entry(name_window)
    entry1.pack(pady=5)

    tk.Label(name_window, text="Player O Name:", bg="#121212", fg="#FFFFFF").pack(pady=5)
    entry2 = tk.Entry(name_window)
    entry2.pack(pady=5)

    tk.Button(name_window, text="Start Game", bg="#00E676", fg="black",
              font=("Arial", 12, "bold"), command=start_game).pack(pady=10)

    name_window.mainloop()


# Run the game
get_player_names()
