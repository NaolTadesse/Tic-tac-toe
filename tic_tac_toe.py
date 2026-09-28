import time
import sys
import os
from customtkinter import *
from tkinter import *
import random
from PIL import Image

if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(os.path.abspath(__file__))


def res(name):
    """Path of a file that sits next to the script (or is bundled in the exe)."""
    return os.path.join(base_path, name)


icon_path = res("favicons.ico")
crown_path = res("crown.png")
bcrown_path = res("bcrown.png")
back_path = res("back.png")

# Save the log next to the exe, because the bundled folder is temporary
if getattr(sys, 'frozen', False):
    data_path = os.path.dirname(sys.executable)
else:
    data_path = base_path
log_path = os.path.join(data_path, "log.txt")

set_appearance_mode("light")
board = [""] * 9
window = CTk()
window.title("Tic tac toe")
try:
    window.iconbitmap(icon_path)
except Exception:
    pass
winner = ""
cp = ""
cb = ""


def read():
    try:
        with open(log_path, "r") as log:
            history = log.read().strip().split(",")
            return list(map(int, history))
    except Exception:
        write([0, 0, 0])
        return [0, 0, 0]


def write(history):
    try:
        with open(log_path, "w") as file:
            file.write(",".join(map(str, history)))
    except Exception:
        pass


history = read()

winners = StringVar()
b1 = StringVar(value="")
b2 = StringVar(value="")
b3 = StringVar(value="")
b4 = StringVar(value="")
b5 = StringVar(value="")
b6 = StringVar(value="")
b7 = StringVar(value="")
b8 = StringVar(value="")
b9 = StringVar(value="")
b = [b1, b2, b3, b4, b5, b6, b7, b8, b9]
player = ""
bot = ""
var = StringVar()
switchvar = StringVar(value="off")
var.set("dark-blue")
set_default_color_theme(var.get())

# First-move choice: set on the home screen, read in main()
YOU_FIRST = "You Go First"
BOT_FIRST = "Bot Goes First"
startvar = StringVar(value=YOU_FIRST)

w = window.winfo_screenwidth()
h = window.winfo_screenheight()
window.geometry(f"{w}x{h}+0+0")
window.minsize(700, 700)
players = ""
select = False


def home():
    global player, bot

    player = ""
    bot = ""

    # (light, dark) color pairs, so dark mode needs no extra code
    UNSELECTED = ("gray86", "gray17")
    SELECTED = ("gray68", "gray38")

    def switcher():
        if switchvar.get() == "on":
            set_appearance_mode("dark")
        else:
            set_appearance_mode("light")

    def choose(symbol):
        global player, bot
        player = symbol
        bot = "O" if symbol == "X" else "X"
        label1.configure(fg_color=SELECTED if symbol == "X" else UNSELECTED)
        label2.configure(fg_color=SELECTED if symbol == "O" else UNSELECTED)

    def X(event):
        choose("X")

    def O(event):
        choose("O")

    def play():
        global select
        if player != "":
            select = True
            for i in window.winfo_children():
                i.destroy()
            main()

    def enter(event):
        if player == "":
            button.configure(fg_color="red")
        else:
            button.configure(fg_color="green")

    def leave(event):
        button.configure(fg_color='#3a7ebf')

    # One centered container keeps the layout the same on any screen
    wrap = CTkFrame(window, fg_color="transparent")
    wrap.place(relx=0.5, rely=0.5, anchor="center")

    lebel = CTkLabel(wrap, text="Tic tac toe", font=("Impact", 50))
    lebel.pack(pady=(0, 30))

    pick = CTkFrame(wrap, fg_color="transparent")
    pick.pack()
    label1 = CTkLabel(pick, height=150, width=155, text="X", font=("Helvetica Bold", 100),
                      text_color="darkblue", corner_radius=20, fg_color=UNSELECTED)
    label1.grid(row=0, column=0, padx=15)
    frame = CTkLabel(pick, text="OR", font=("Arial", 20, "bold"))
    frame.grid(row=0, column=1, padx=15)
    label2 = CTkLabel(pick, height=150, width=155, text="O", font=("Helvetica Bold", 100),
                      text_color="darkred", corner_radius=20, fg_color=UNSELECTED)
    label2.grid(row=0, column=2, padx=15)

    turn_label = CTkLabel(wrap, text="First Move", font=("Arial", 18, "bold"))
    turn_label.pack(pady=(40, 10))
    turn_pick = CTkSegmentedButton(wrap, values=[YOU_FIRST, BOT_FIRST], variable=startvar,
                                   font=("Arial", 18, "bold"), width=420, height=50,
                                   dynamic_resizing=False)
    turn_pick.pack()

    button = CTkButton(wrap, text="Play", command=play, height=40)
    button.pack(pady=(45, 0))

    switch = CTkSwitch(window, text="dark mode", command=switcher, variable=switchvar,
                       offvalue="off", onvalue="on")
    switch.place(relx=1, rely=1, x=-20, y=-20, anchor="se")

    label1.bind("<Button-1>", X)
    label2.bind("<Button-1>", O)
    button.bind("<Enter>", enter)
    button.bind("<Leave>", leave)


def main():
    job = [None]  # pending "bot opens the round" timer

    def action(num):
        global cp
        if winner != "" or job[0] is not None:
            return
        if board[num - 1] == "":
            b[num - 1].set(player)
            board[num - 1] = player
            if player == "X":
                buttons[num - 1].configure(text_color="darkblue")
                cp = "darkblue"
            else:
                buttons[num - 1].configure(text_color="darkred")
                cp = "darkred"
            check()
            display()
            if winner == "":
                botmove()
                check()
                display()

    def display():
        if winner != "":
            winners.set(winner)
            for i in buttons:
                i.configure(state=DISABLED)
            ph.configure(image=pic)
            if winner == "You won!!!":
                diswinner.configure(border_color=cp)
                history[0] = int(history[0]) + 1
            elif winner == " You lost :(":
                diswinner.configure(border_color=cb)
                ph.configure(image="")
                history[2] = int(history[2]) + 1
            else:
                diswinner.configure(border_color="grey")
                bc = CTkImage(light_image=Image.open(bcrown_path), size=(50, 50))
                ph.configure(image=bc)
                history[1] = int(history[1]) + 1
            write(history)
            # slide the result box up to the center
            steps = 30
            for step in range(steps + 1):
                y = 1.3 - 0.8 * step / steps
                diswinner.place(relx=0.5, rely=y, anchor="center")
                window.update()
                time.sleep(0.01)
        wa.set(history[0])
        ta.set(history[1])
        la.set(history[2])

    def botmove():
        global cb
        color = ""
        if winner != "":
            return
        if bot == "X":
            color = "darkblue"
            cb = color
        else:
            color = "darkred"
            cb = color

        def bot_procces():
            # Returns the winning cell if the bot has one, otherwise a cell that blocks the player
            # (or "" so a random cell is used)
            idx = ""
            for i in range(3):
                current = [board[i], board[i + 3], board[i + 6]]
                if (current.count("X") == 2 or current.count("O") == 2) and current.count("") == 1:
                    idx = current.index("")
                    idx = i + 3 * idx
                    if current.count(bot) == 2:
                        return idx

                j = i * 3
                current = [board[j], board[j + 1], board[j + 2]]
                if (current.count("X") == 2 or current.count("O") == 2) and current.count("") == 1:
                    idx = current.index("")
                    idx = j + idx
                    if current.count(bot) == 2:
                        return idx
            current = [board[0], board[4], board[8]]
            if (current.count("X") == 2 or current.count("O") == 2) and current.count("") == 1:
                idx = current.index("")
                idx = idx * 4
                if current.count(bot) == 2:
                    return idx
            current = [board[2], board[4], board[6]]
            if (current.count("X") == 2 or current.count("O") == 2) and current.count("") == 1:
                idx = current.index("")
                idx = 2 + idx * 2
            return idx

        idx = bot_procces()
        while True:
            if idx != "" and board[idx] == "":
                i = idx
            else:
                i = random.randint(0, 8)
            if board[i] == "":
                b[i].set(bot)
                buttons[i].configure(text_color=color)
                board[i] = bot
                break

    def check():
        # Sets winner when a row, column or diagonal is complete, or the board is full
        global winner
        for i in [0, 3, 6]:
            if board[i] == board[i + 1] == board[i + 2]:
                if board[i] == player:
                    winner = "You won!!!"
                    return
                elif board[i] == bot:
                    winner = " You lost :("
                    return
        for i in [0, 1, 2]:
            if board[i] == board[i + 3] == board[i + 6]:
                if board[i] == player:
                    winner = "You won!!!"
                    return
                elif board[i] == bot:
                    winner = " You lost :("
                    return
        if board[0] == board[4] == board[8]:
            if board[0] == player:
                winner = "You won!!!"
                return
            elif board[0] == bot:
                winner = " You lost :("
                return
        elif board[2] == board[4] == board[6]:
            if board[2] == player:
                winner = "You won!!!"
                return
            elif board[2] == bot:
                winner = " You lost :("
                return
        tie()

    def tie():
        global winner
        if "" in board:
            return
        else:
            winner = "         Tie    "

    def switcher():
        if switchvar.get() == "on":
            set_appearance_mode("dark")
        else:
            set_appearance_mode("light")

    def start_round():
        """If the bot goes first, lock the board and let it open after a short pause."""
        if startvar.get() == BOT_FIRST:
            for i in buttons:
                i.configure(state=DISABLED)
            job[0] = window.after(500, bot_opening)

    def bot_opening():
        job[0] = None
        botmove()
        check()
        display()
        if winner == "":
            for i in buttons:
                i.configure(state=NORMAL)

    def reset_board():
        global winner, board
        if job[0] is not None:
            window.after_cancel(job[0])
            job[0] = None
        board = [""] * 9
        winner = ""
        for i in b:
            i.set("")

    def restart():
        reset_board()
        diswinner.place(relx=0.5, rely=1.5, anchor="center")
        for i in buttons:
            i.configure(state=NORMAL)
        start_round()

    def go_home():
        reset_board()
        for i in window.winfo_children():
            i.destroy()
        home()

    hidden_x = [-120]

    def enter(event):
        while hover.winfo_x() < 5:
            hover.place(x=min(hover.winfo_x() + 3, 5), rely=0.5, anchor="w")
            window.update()
            time.sleep(0.001)

    def leave(event):
        while hover.winfo_x() > hidden_x[0]:
            hover.place(x=max(hover.winfo_x() - 1, hidden_x[0]), rely=0.5, anchor="w")
            window.update()
            time.sleep(0.001)

    if player == "X":
        cp = "darkblue"
    else:
        cp = "darkred"

    # Top bar: title in the middle, Restart left, Home right
    lebel = CTkLabel(window, text=f"Player is {player}", font=("Arial", 40, "bold"))
    lebel.place(relx=0.5, y=20, anchor="n")
    rebutton = CTkButton(window, command=restart, text="Restart", width=60)
    rebutton.place(x=10, y=10)
    hbutton = CTkButton(window, text="Home", command=go_home, width=60)
    hbutton.place(relx=1, x=-10, y=10, anchor="ne")

    # Board: black frame with the 9 cells
    can = CTkFrame(window, fg_color="black", corner_radius=0)
    can.place(relx=0.5, rely=0.55, anchor="center")
    buttons = []
    for n in range(9):
        cell = CTkButton(can, command=lambda n=n: action(n + 1), width=150, height=150,
                         fg_color="white", corner_radius=0, bg_color="black",
                         textvariable=b[n], hover_color="lightblue",
                         font=("Helvetica Bold", 120))
        cell.grid(row=n // 3, column=n % 3, padx=3, pady=3)
        buttons.append(cell)

    switch = CTkSwitch(window, text="dark mode", command=switcher, variable=switchvar,
                       offvalue="off", onvalue="on")
    switch.place(relx=1, rely=1, x=-20, y=-20, anchor="se")

    # Result box: parked below the window until the round ends
    pic = CTkImage(light_image=Image.open(crown_path), size=(50, 50))
    diswinner = CTkFrame(window, fg_color="white", width=320, height=300, corner_radius=20,
                         bg_color="white", border_color="blue", border_width=10)
    diswinner.place(relx=0.5, rely=1.5, anchor="center")
    ph = CTkLabel(diswinner, image=pic, text="")
    ph.place(relx=0.5, y=25, anchor="n")
    ltext = CTkLabel(diswinner, textvariable=winners, font=("impact", 60))
    ltext.place(relx=0.5, rely=0.6, anchor="center")

    # Stats panel that slides in from the left
    hover = CTkFrame(window, corner_radius=20, fg_color="white", border_width=5, border_color=cp)
    hover.bind("<Button-1>", enter)
    pk = CTkImage(light_image=Image.open(back_path), size=(30, 30))
    picl = CTkLabel(hover, text="", image=pk)
    picl.grid(row=1, column=3)
    picl.bind("<Button-1>", leave)
    wa = IntVar(value=history[0])
    ta = IntVar(value=history[1])
    la = IntVar(value=history[2])
    winl = CTkLabel(hover, text="Win", font=("Helvetica Bold", 20))
    tiel = CTkLabel(hover, text="Tie", font=("Helvetica Bold", 20))
    losel = CTkLabel(hover, text="Lose", font=("Helvetica Bold", 20))
    wina = CTkLabel(hover, textvariable=wa, font=("Helvetica Bold", 20))
    tiea = CTkLabel(hover, textvariable=ta, font=("Helvetica Bold", 20))
    losea = CTkLabel(hover, textvariable=la, font=("Helvetica Bold", 20))
    winl.grid(row=1, column=0, padx=30, pady=15)
    tiel.grid(row=2, column=0, padx=30, pady=15)
    losel.grid(row=3, column=0, padx=30, pady=15)
    wina.grid(row=1, column=1)
    tiea.grid(row=2, column=1)
    losea.grid(row=3, column=1)

    # Hide the panel, leaving a 40px strip visible
    hover.update_idletasks()
    hidden_x[0] = -(hover.winfo_reqwidth() - 40)
    hover.place(x=hidden_x[0], rely=0.5, anchor="w")

    start_round()


home()
window.mainloop()