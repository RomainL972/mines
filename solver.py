import mines


class Solver:
    def __init__(self):
        self.board = mines.Board()
        self.board.reveal(4, 4)

    def get_number_boxes(self):
        positions = {}
        for i in range(mines.NUMBER_OF_ROWS):
            for j in range(mines.NUMBER_OF_COLS):
                if self.board.board[i][j] != "?" and self.board.board[i][j] != " ":
                    positions[(i, j)] = self.board.board[i][j]
        return positions

    def count_unknowns(self, x: int, y: int):
        count = 0
        count_flags = 0
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if self.board.is_valid_pos(i, j):
                    if self.board.board[i][j] == "?":
                        count += 1
                    if self.board.board[i][j] == "F":
                        count += 1
                        count_flags += 1
        return count, count_flags

    def is_unknown(self, x: int, y: int):
        return self.board.board[x][y] == "?"

    def set_flags(self, x: int, y: int):
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if self.board.is_valid_pos(i, j) and self.is_unknown(i, j):
                    self.board.board[i][j] = "F"

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
                    print(solver.board)
                elif count_flags == number:
                    print(f"Revealing around {coord}")
                    self.reveal_unknowns(coord[0], coord[1])
                    success = True
                    print(solver.board)
        return success, done


if __name__ == "__main__":
    solver = Solver()
    print(solver.board)
    success = True
    done = False
    while success:
        success, done = solver.solve()

    print("Success!" if done else "Failure!")
