# Tetris Clone

A tetris terminal game written in Python 3 using the builtin curses module (a Python wrapper for the C ncurses library). I focused on object-oriented programming and having clean easy-to-read code spread over multiple files.

![Demo](tetris_demo.gif)


## Getting Started


### Prerequisites

Python >=3.5.2

### Running the program

To run the program, type:

```
python3 main.py
```

For best results, use Ubuntu's GNOME terminal and a monospace font.

Monospace font can be achieved by:
```
> open terminal
> edit profile preferences
> general tab
> tick custom font
> monospace font of your choice (I used monospace regular in 12pt)
```

### Controls

Directional keys:
* right, left, down move the piece in that direction
* up rotates the piece clockwise

q/y/n:
* q quits at any time
* y/n allow continuing or quitting after a loss
