#!/usr/bin/env python3
import mines_selenium as mines


class Solver:
    def __init__(self):
        self.board = mines.SeleniumBoard()
        self.board.reveal(int(mines.NUMBER_OF_ROWS / 2), int(mines.NUMBER_OF_COLS / 2))

    def get_number_boxes(self):
        positions = {}
        for i in range(mines.NUMBER_OF_ROWS):
            for j in range(mines.NUMBER_OF_COLS):
                if self.board.get(i, j) != "?" and self.board.get(i, j) != " ":
                    positions[(i, j)] = self.board.get(i, j)
        return positions

    def count_unknowns(self, x: int, y: int):
        count = 0
        count_flags = 0
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if self.board.is_valid_pos(i, j):
                    if self.board.get(i, j) == "?":
                        count += 1
                    if self.board.get(i, j) == "F":
                        count += 1
                        count_flags += 1
        return count, count_flags

    def is_unknown(self, x: int, y: int):
        return self.board.get(x, y) == "?"

    def set_flags(self, x: int, y: int):
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if self.board.is_valid_pos(i, j) and self.is_unknown(i, j):
                    self.board.flag(i, j, True)

    def reveal_unknowns(self, x: int, y: int):
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if self.board.is_valid_pos(i, j) and self.is_unknown(i, j):
                    self.board.reveal(i, j)

    def solve(self):
        success = False
        done = True
        positions = self.get_number_boxes()
        for coord, number in positions.items():
            count, count_flags = self.count_unknowns(coord[0], coord[1])
            if count != count_flags:
                done = False
                if count == number:
                    print(f"Setting flags around {coord}")
                    self.set_flags(coord[0], coord[1])
                    success = True
                    # print(solver.board)
                elif count_flags == number:
                    print(f"Revealing around {coord}")
                    self.reveal_unknowns(coord[0], coord[1])
                    success = True
                    # print(solver.board)
        return success, done


if __name__ == "__main__":
    solver = Solver()
    while True:
        # print(solver.board)
        success = True
        done = False
        while success:
            success, done = solver.solve()

        print("Success!" if done else "Failure!")
        if done:
            break
        solver.board.wrapper.driver.refresh()
        solver.board.cache = {}
        solver.board.generate_board()
        solver.board.reveal(int(mines.NUMBER_OF_ROWS / 2), int(mines.NUMBER_OF_COLS / 2))
        # input("Press enter to continue")
        # solver.board.cache = {}
    while True:
        pass
