import mines
from tkinter import *
import time

xmax = 500
ymax = 500
numRows = mines.NUMBER_OF_ROWS
numCols = mines.NUMBER_OF_COLS
row = ymax / numRows
col = xmax / numCols
numMines = mines.NUMBER_OF_MINES
colors = ["blue", "green", "red", "purple", "orange", "black", "black", "black"]
startTime = 0

board = []
minesBoard = []

def relative_rectangle(c, x, y, xrel, yrel, fill="white"):
    return c.create_rectangle(x, y, x+xrel, y+yrel, fill=fill)

def relative_line(c, x, y, xrel, yrel):
    return c.create_line(x, y, x+xrel, y+yrel)

def centeredText(c, j, i, text, color="black"):
    return c.create_text((j+0.5)*col, (i+0.5)*row, text=text, fill=color)

c = Canvas(width=xmax, height=ymax)
c.pack()

def init(_=None):
    global board, minesBoard
    c.create_rectangle(0,0,xmax,ymax,fill="blue")
    for i in range(numRows):
        relative_line(c, 0, row*i, xmax, 0)
    for i in range(numCols):
        relative_line(c, col*i, 0, 0, ymax)

    board = mines.initBoard()
    minesBoard = []

    c.bind("<Button-1>", onclick)
    c.bind("<Button-3>", onclick)

def updateBoard(board):
    count = 0
    for i in range(len(board)):
        for j in range(len(board[i])):
            char = board[i][j]
            if char != "?" and "F" not in str(char):
                relative_rectangle(c, j*col, i*row, col, row)
            else:
                if char == "F":
                    board[i][j] = "F" + str(centeredText(c, j, i, "F", "red"))
                count += 1
            try:
                number = int(char)
                centeredText(c, j, i, char, colors[number-1])
            except Exception as e:
                pass
    if count == numMines:
        gameOver("win")

def gameOver(e):
    relative_rectangle(c, 0, 0, 500, 500, "white")
    if e == "win":
        c.create_text(250, 250, text="Congratulations!")
        c.create_text(250, 300, text="Time : " + str(round(time.perf_counter()-startTime,1)) + "s")
    else:
        c.create_text(250, 250, text="Game Over!")
    c.bind("<Button-1>", init)

def exitGame(_):
    exit()

def onclick(e):
    global board, minesBoard, startTime
    curCol = int(e.x/xmax*numCols)
    curRow = int(e.y/ymax*numRows)
    if e.num == 1:
        if not minesBoard:
            minesBoard = mines.initMines(board, curRow, curCol)
            startTime = time.perf_counter()
        result, board = mines.reveal(board, minesBoard, curRow, curCol)
        if result == "bomb":
            for bomb in minesBoard:
                relative_rectangle(c, bomb[1]*col, bomb[0]*row, col, row, "red")
            c.bind("<Button-1>", gameOver)
    elif e.num == 3:
        if board[curRow][curCol] == "?":
            board[curRow][curCol] = "F"
        elif "F" in board[curRow][curCol]:
            ref = board[curRow][curCol].split("F")[1]
            board[curRow][curCol] = "?"
            c.delete(ref)
    updateBoard(board)

init()

c.mainloop()
