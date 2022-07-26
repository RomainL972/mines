#!/usr/bin/env python3


from abc import ABC, abstractmethod


class AbsBoard(ABC):
    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractmethod
    def is_valid_pos(self, x: int, y: int) -> bool:
        pass

    @abstractmethod
    def reveal(self, x: int, y: int) -> str | int | None:
        pass
