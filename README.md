# ❌⭕ Tic Tac Toe Game

A modern, customizable Tic Tac Toe game built using Python and CustomTkinter. Features smooth sliding UI panels, win/loss history tracking, dynamic themes, and a standalone executable (.exe) compiled for Windows.

---

## 🛠️ Tech Stack & Features

* GUI Framework: Built using customtkinter and tkinter.
* Image Processing: Pillow (PIL) for dynamic image rendering.
* Asset Pathing: Built-in sys._MEIPASS dynamic path resolving to ensure bundled images load smoothly inside the standalone .exe.
* Key Features:
  * Dark & Light mode toggle.
  * Option to play as X or O and choose who goes first.
  * Slide-out match history panel tracking wins, ties, and losses.
  * Animated victory and defeat overlay popups.

---

## 🚀 Quick Download (For Players)

Want to play right away without running any code?

1. Go to the Releases Section on the right side of this repository: https://github.com/NaolTadesse/Tic-tac-toe/releases
2. Download TicTacToe.exe.
3. Double-click TicTacToe.exe to launch and play!

---

## 💻 Running from Source Code

If you want to run or inspect the code directly:

### Prerequisites
* Python 3.x installed on your machine.
* Install required libraries:
  pip install customtkinter pillow

### Steps
1. Clone this repository:
   git clone https://github.com/NaolTadesse/Tic-tac-toe.git
   cd Tic-tac-toe

2. Run the application:
   python tic_tac_toe.py

---

## 📁 Repository Structure

Tic-tac-toe/
│
├── asset/                 # UI assets folder
│   ├── favicons.ico       # Application icon
│   ├── crown.png          # Victory crown icon
│   ├── bcrown.png         # Tie crown icon
│   └── back.png           # Slide panel back arrow icon
│
├── tic_tac_toe.py         # Main application source code
└── README.md              # Project documentation
