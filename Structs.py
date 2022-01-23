from dataclasses import dataclass

# Datatype for each cell/node
# step no longer necessary, should remove this at some point
@dataclass
class Cell:
    fill: (int, int, int)
    step: int
    pos: (int, int)
    prevCell: (int, int)
