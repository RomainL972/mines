import json
import random

NUMBER_OF_MINES = 10
NUMBER_OF_ROWS = 9
NUMBER_OF_COLS = 9

def initBoard():
    board = []

    for i in range(NUMBER_OF_ROWS):
        row = []
        for j in range(NUMBER_OF_COLS):
            row.append('?')
        board.append(row)
    return board

def displayBoard(board):
    print("  0 1 2 3 4 5 6 7 8")
    for i in range(len(board)):
        print(i, "", end="")
        for char in board[i]:
            print(char, "",end="")
        print()

def isValidPos(x, y):
    return not (x < 0 or x > NUMBER_OF_ROWS-1 or y < 0 or y > NUMBER_OF_COLS-1)

def initMines(board, x, y):
    safe = []
    mines = []
    for i in range(x-1, x+2):
        for j in range(y-1, y+2):
            if isValidPos(i, j):
                safe.append((i, j))

    for i in range(NUMBER_OF_MINES):
        while (x, y) in mines or (x, y) in safe:
            x, y = random.randint(0, NUMBER_OF_ROWS-1), random.randint(0, NUMBER_OF_COLS-1)
        mines.append((x, y))
    return mines

def reveal(board, mines, x, y):
    if board[x][y] != "?":
        return None, board
    if (x, y) in mines:
        return "bomb", board
    count = 0
    check = []
    for i in range(x-1, x+2):
        for j in range(y-1, y+2):
            if isValidPos(i, j):
                if (i, j) in mines:
                    count += 1
                else:
                    check.append((i, j))
    if count == 0:
        board[x][y] = " "
        for x, y in check:
            _, board = reveal(board, mines, x, y)
    else:
        board[x][y] = count
    return count, board


if __name__ == "__main__":
    mines = []
    board = initBoard()
    while True:
        displayBoard(board)
        coord = input("XY : ")
        try:
            x = int(coord[0])
            y = int(coord[1])
            if not isValidPos(x, y):
                print("Wrong coordinates")
                continue
            if "f" in coord:
                if board[x][y] == "?":
                    board[x][y] = "F"
                elif board[x][y] == "F":
                    board[x][y] = "?"
                continue
        except Exception as e:
            print("Wrong coordinates")
            continue
        if not mines:
            mines = initMines(board, x, y)
            print(mines)
        result, board = reveal(board, mines, x, y)
        if result == "bomb":
            print("Game Over !")
            exit()
