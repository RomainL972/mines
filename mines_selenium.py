#!/usr/bin/env python3
from board import AbsBoard
from selenium_wrapper import SeleniumWrapper


class SeleniumBoard(AbsBoard):
    def __init__(self) -> None:
        self.wrapper = SeleniumWrapper("firefox")

    def __str__(self) -> str:
        pass

    def is_valid_pos(self, x: int, y: int) -> bool:
        pass

    def reveal(self, x: int, y: int) -> str | int | None:
        pass


if __name__ == "__main__":
    b = SeleniumBoard()
