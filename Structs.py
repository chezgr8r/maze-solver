from dataclasses import dataclass

@dataclass
class Vector2:
    x: float
    y: float

@dataclass
class Vector3:
    x: float
    y: float
    z: float

# datatype for each cell/node
@dataclass
class Cell:
    fill: (int, int, int)
    step: int
    pos: (int, int)
    prevCell: (int, int)
