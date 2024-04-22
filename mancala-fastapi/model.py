from typing import List

from pydantic import BaseModel


class Player(BaseModel):
    name: str
    hasTurn: bool
    pits: List[int]

    def __init__(self, name: str, hasTurn: bool, pits: List[int], **data):
        super().__init__(id=id, name=name, hasTurn = hasTurn, pits = pits, **data)
        self.name = name
        self.hasTurn = hasTurn
        self.pits = pits


class MancalaStatus(BaseModel):
    winner: str
    endOfGame: bool

    def __init__(self, winner: str, endOfGame: bool, **data):
        super().__init__(winner=winner, endOfGame=endOfGame, **data)
        self.winner = winner
        self.endOfGame = endOfGame
