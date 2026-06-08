from dataclasses import dataclass

@dataclass
class Team:
    id: int
    name: str
    country: str


@dataclass
class Pilot:
    id: int
    name: str
    country: str
    team: str


@dataclass
class GrandPrix:
    id: int
    name: str
    circuit: str
    date: str
    winner: str = ""
