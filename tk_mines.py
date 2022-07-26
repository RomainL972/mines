#!/usr/bin/env python
from typing import Literal
import mines
from tkinter import Canvas
import time

xmax = 500
ymax = 500
numRows = mines.NUMBER_OF_ROWS
numCols = mines.NUMBER_OF_COLS
row = ymax / numRows
col = xmax / numCols
numMines = mines.NUMBER_OF_MINES
colors = ["blue", "green", "red", "purple", "orange", "black", "black", "black"]


class TKMines:
    def __init__(self) -> None:
        self.canvas = Canvas(width=xmax, height=ymax)
        self.canvas.pack()
        self.init()
        self.start_time = 0.0

    def relative_rectangle(self, x: float, y: float, xrel: float, yrel: float, fill: str = "white") -> int:
        return self.canvas.create_rectangle(x, y, x + xrel, y + yrel, fill=fill)

    def relative_line(self, x: float, y: float, xrel: float, yrel: float) -> int:
        return self.canvas.create_line(x, y, x + xrel, y + yrel)

    def centeredText(self, j: float, i: float, text: str, color: str = "black") -> int:
        return self.canvas.create_text((j + 0.5) * col, (i + 0.5) * row, text=text, fill=color)

    def init(self, _: None = None) -> None:
        self.canvas.create_rectangle(0, 0, xmax, ymax, fill="blue")
        for i in range(numRows):
            self.relative_line(0, row * i, xmax, 0)
        for i in range(numCols):
            self.relative_line(col * i, 0, 0, ymax)

        self.board = mines.Board()

        self.canvas.bind("<Button-1>", self.onclick)
        self.canvas.bind("<Button-3>", self.onclick)

    def update_board(self) -> None:
        count = 0
        for i in range(len(self.board.board)):
            for j in range(len(self.board.board[i])):
                char = self.board.board[i][j]
                if char != "?" and "F" not in str(char):
                    self.relative_rectangle(j * col, i * row, col, row)
                else:
                    if char == "F":
                        self.board.board[i][j] = "F" + str(self.centeredText(j, i, "F", "red"))
                    count += 1
                try:
                    number = int(char)
                    self.centeredText(j, i, str(char), colors[number - 1])
                except Exception:
                    pass
        if count == numMines:
            self.gameOver("win")

    def gameOver(self, e: Literal["win"]) -> None:
        self.relative_rectangle(0, 0, 500, 500, "white")
        if e == "win":
            self.canvas.create_text(250, 250, text="Congratulations!")
            self.canvas.create_text(
                250, 300, text="Time : " + str(round(time.perf_counter() - self.start_time, 1)) + "s"
            )
        else:
            self.canvas.create_text(250, 250, text="Game Over!")
        self.canvas.bind("<Button-1>", self.init)

    def onclick(self, e) -> None:
        curCol = int(e.x / xmax * numCols)
        curRow = int(e.y / ymax * numRows)
        if e.num == 1:
            if len(self.board.mines) == 0:
                self.start_time = time.perf_counter()
            result = self.board.reveal(curRow, curCol)
            if result == "bomb":
                for bomb in self.board.mines:
                    self.relative_rectangle(bomb[1] * col, bomb[0] * row, col, row, "red")
                self.canvas.bind("<Button-1>", self.gameOver)
        elif e.num == 3:
            if self.board.board[curRow][curCol] == "?":
                self.board.board[curRow][curCol] = "F"
            elif "F" in str(self.board.board[curRow][curCol]):
                ref = str(self.board.board[curRow][curCol]).split("F")[1]
                self.board.board[curRow][curCol] = "?"
                self.canvas.delete(ref)
        self.update_board()


if __name__ == "__main__":
    tk = TKMines()
    tk.canvas.mainloop()
