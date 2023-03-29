#!/usr/bin/env python3
from typing import Literal
from board import AbsBoard
from selenium_wrapper import SeleniumWrapper
from selenium.webdriver.remote.webelement import WebElement

DIFFICULTY = "medium"
if DIFFICULTY == "easy":
    NUMBER_OF_MINES = 10
    NUMBER_OF_ROWS = 9
    NUMBER_OF_COLS = 9
    URL_SUFFIX = "#beginner"
elif DIFFICULTY == "medium":
    NUMBER_OF_MINES = 40
    NUMBER_OF_ROWS = 16
    NUMBER_OF_COLS = 16
    URL_SUFFIX = "#intermediate"
else:
    NUMBER_OF_MINES = 99
    NUMBER_OF_ROWS = 16
    NUMBER_OF_COLS = 30
    URL_SUFFIX = "#"



class SeleniumBoard(AbsBoard):
    def __init__(self) -> None:
        self.wrapper = SeleniumWrapper("firefox")
        self.wrapper.access_url(f"https://minesweeperonline.com/{URL_SUFFIX}")
        self.board: list[list[WebElement]] = []
        self.cache = {}
        for i in range(NUMBER_OF_ROWS):
            for j in range(NUMBER_OF_COLS):
                self.cache[i, j] = "?"
        self.generate_board()

    def generate_board(self):
        game = self.wrapper.get_element("id", "game")
        self.board = []
        for i in range(NUMBER_OF_ROWS):
            self.board.append([])
            for j in range(NUMBER_OF_COLS):
                id = f"{i+1}_{j+1}"
                self.board[i].append(self.wrapper.get_element("id", id, game))

    def get(self, x: int, y: int, disable_cache: bool = False) -> Literal["?"] | Literal[" "] | int | None:
        if not self.is_valid_pos(x, y):
            return None
        if not disable_cache:
            cached_value = self.cache.get((x, y))
            if cached_value is not None:
                return cached_value
        className = self.board[x][y].get_attribute("class").split(" ")[1]
        value = None
        if className == "blank":
            value = "?"
        elif className == "bombflagged":
            value = "F"
        elif className == "bombdeath":
            raise ValueError("DEATHHHH")
        elif className == "open0":
            value = " "
        elif className.startswith("open"):
            value = int(className.split("open")[1])
        else:
            raise ValueError(f"Unknown class : {className}")

        self.cache[(x, y)] = value
        return value

    def flag(self, x: int, y: int, _: bool):
        if not self.is_valid_pos(x, y):
            return None
        self.wrapper.right_click_element(self.board[x][y])
        cached_value = self.cache.get((x, y))
        if cached_value is None or cached_value == "?":
            self.cache[(x, y)] = "F"
        else:
            self.cache[(x, y)] = "?"

    def __str__(self) -> str:
        return ""

    def is_valid_pos(self, x: int, y: int) -> bool:
        return not (x < 0 or x > NUMBER_OF_ROWS - 1 or y < 0 or y > NUMBER_OF_COLS - 1)

    def update_around(self, x: int, y: int):
        for i in range(x-1, x+2):
            for j in range(y-1, y+2):
                value = self.get(i, j)
                if value == "?":
                    value = self.get(i, j, True)
                    if value == " ":
                        self.update_around(i, j)

    def reveal(self, x: int, y: int) -> Literal["?"] | Literal[" "] | int | None:
        if not self.is_valid_pos(x, y):
            return None
        self.board[x][y].click()
        value = self.get(x, y, True)
        if value == " ":
            self.update_around(x, y)
        return value


if __name__ == "__main__":
    b = SeleniumBoard()
    while True:
        pass
