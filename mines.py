#!/usr/bin/env python3
import math
import random

from board import AbsBoard

NUMBER_OF_MINES = 40
NUMBER_OF_ROWS = 16
NUMBER_OF_COLS = 16


class Board(AbsBoard):
    def __init__(self) -> None:
        self.board: list[list[str | int]] = [["?" for _ in range(NUMBER_OF_COLS)] for _ in range(NUMBER_OF_ROWS)]
        self.mines: list[tuple[int, int]] = []

    def __str__(self) -> str:
        rowindex_space = int(math.log10(NUMBER_OF_ROWS)) + 2
        colindex_space = int(math.log10(NUMBER_OF_COLS)) + 2
        res = " " * rowindex_space
        for i in range(NUMBER_OF_COLS):
            res += str(i).ljust(colindex_space, " ")
        res += "\n"
        for i in range(len(self.board)):
            res += str(i).ljust(rowindex_space, " ")
            for char in self.board[i]:
                res += str(char).ljust(colindex_space, " ")
            res += "\n"
        return res

    def is_valid_pos(self, x: int, y: int) -> bool:
        return not (x < 0 or x > NUMBER_OF_ROWS - 1 or y < 0 or y > NUMBER_OF_COLS - 1)

    def init_mines(self, x: int, y: int) -> None:
        safe = []
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if self.is_valid_pos(i, j):
                    safe.append((i, j))

        for i in range(NUMBER_OF_MINES):
            while (x, y) in self.mines or (x, y) in safe:
                x, y = random.randint(0, NUMBER_OF_ROWS - 1), random.randint(0, NUMBER_OF_COLS - 1)
            self.mines.append((x, y))

    def reveal(self, x: int, y: int) -> str | int | None:
        if len(self.mines) == 0:
            self.init_mines(x, y)

        if self.board[x][y] != "?":
            return None
        if (x, y) in self.mines:
            return "bomb"
        count = 0
        check = []
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if self.is_valid_pos(i, j):
                    if (i, j) in self.mines:
                        count += 1
                    else:
                        check.append((i, j))
        if count == 0:
            self.board[x][y] = " "
            for x, y in check:
                self.reveal(x, y)
        else:
            self.board[x][y] = count
        return count


def main() -> None:
    board = Board()
    while True:
        print(board)
        coord = input("XY : ")
        try:
            x = int(coord[0])
            y = int(coord[1])
            if not board.is_valid_pos(x, y):
                print("Wrong coordinates")
                continue
            if "f" in coord:
                if board.board[x][y] == "?":
                    board.board[x][y] = "F"
                elif board.board[x][y] == "F":
                    board.board[x][y] = "?"
                continue
        except Exception:
            print("Wrong coordinates")
            continue

        result = board.reveal(x, y)
        if result == "bomb":
            print("Game Over !")
            exit()


if __name__ == "__main__":
    main()
