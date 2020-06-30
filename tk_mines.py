import mines
from tkinter import *

xmax = 500
ymax = 500
numRows = 9
numCols = 9
row = ymax / numRows
col = xmax / numCols
numMines = 10
colors = ["blue", "green", "red", "purple", "orange", "black"]

board = mines.initBoard()
minesBoard = []

def relative_rectangle(c, x, y, xrel, yrel, fill="white"):
    return c.create_rectangle(x, y, x+xrel, y+yrel, fill=fill)

def relative_line(c, x, y, xrel, yrel):
    return c.create_line(x, y, x+xrel, y+yrel)

def centeredText(c, j, i, text, color="black"):
    return c.create_text((j+0.5)*col, (i+0.5)*row, text=text, fill=color)

c = Canvas(width=xmax, height=ymax)
c.pack()

c.create_rectangle(0,0,xmax,ymax,fill="blue")
for i in range(numRows):
    relative_line(c, 0, row*i, xmax, 0)
for i in range(numCols):
    relative_line(c, col*i, 0, 0, ymax)

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
        print("Congratulations!")
        c.bind("<Button-1>", exit)

def onclick(e):
    global board, minesBoard
    curCol = int(e.x/xmax*numCols)
    curRow = int(e.y/ymax*numRows)
    if e.num == 1:
        if not minesBoard:
            minesBoard = mines.initMines(board, curRow, curCol)
        result, board = mines.reveal(board, minesBoard, curRow, curCol)
        if result == "bomb":
            print("Game Over!")
            for bomb in minesBoard:
                relative_rectangle(c, bomb[1]*col, bomb[0]*row, col, row, "red")
            c.bind("<Button-1>", exit)
    elif e.num == 3:
        if board[curRow][curCol] == "?":
            board[curRow][curCol] = "F"
        elif "F" in board[curRow][curCol]:
            ref = board[curRow][curCol].split("F")[1]
            board[curRow][curCol] = "?"
            c.delete(ref)
    updateBoard(board)

c.bind("<Button-1>", onclick)
c.bind("<Button-3>", onclick)

c.mainloop()
