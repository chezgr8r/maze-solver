import pygame, sys, random
from Structs import *
from GlobalVariables import *

# Function to create a new, blank cell
def new_cell(pos):
    return Cell(WHITE, -1, pos, (-1, -1))

# Create global grid
GRID = [[new_cell((0, 0))]]

# Button sprite
class Button(pygame.sprite.Sprite):
    def __init__(self, pos, color, size):
        super().__init__()
        self.image = pygame.Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = pos

class ColUpBtn(Button):
    def __init__(self, pos, color, size):
        super().__init__(pos, color, size)
    def on_click(self):
        global COL_NUM
        global GRID
        if COL_NUM < 30:
            COL_NUM += 1
            for i in GRID:
                i.append(new_cell((i, COL_NUM)))
            #print(GRID)

class ColDownBtn(Button):
    def __init__(self, pos, color, size):
        super().__init__(pos, color, size)
    def on_click(self):
        global COL_NUM
        if COL_NUM > 1:
            for i in GRID:
                i.pop()
            COL_NUM -= 1
            #print(GRID)

class RowUpBtn(Button):
    def __init__(self, pos, color, size):
        super().__init__(pos, color, size)
    def on_click(self):
        global ROW_NUM
        if ROW_NUM < 30:
            new_row = []
            ROW_NUM += 1
            for i in range(len(GRID[0])):
                new_row.append(new_cell((ROW_NUM, i)))
            GRID.append(new_row)
            #print(GRID)

class RowDownBtn(Button):
    def __init__(self, pos, color, size):
        super().__init__(pos, color, size)
    def on_click(self):
        global ROW_NUM
        if ROW_NUM > 1:
            GRID.pop()
            ROW_NUM -= 1
            #print(GRID)

class CellBtn(pygame.sprite.Sprite):
    def __init__(self, pos, color, size, coord):
        super().__init__()
        self.image = pygame.Surface((size[0] - 1, size[1] - 1))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = pos

        self.coord = coord
    def on_click(self):
        global CELL_CHANGE, GRID, GREEN, RED
        if not CELL_CHANGE in (GREEN, RED):
            GRID[self.coord[0]][self.coord[1]].fill = CELL_CHANGE
        else:
            startExists = False
            endExists = False
            for r in range(len(GRID)):
                for c in range(len(GRID[0])):
                    if GRID[r][c].fill == GREEN:
                        startExists = True
                    elif GRID[r][c].fill == RED:
                        endExists = True
            if (not(startExists) and (CELL_CHANGE == GREEN)) or not(endExists) and (CELL_CHANGE == RED):
                GRID[self.coord[0]][self.coord[1]].fill = CELL_CHANGE

class ClearGrid(Button):
    def __init__(self, pos, color, size):
        super().__init__(pos, color, size)
    def on_click(self):
        global GRID, WHITE
        for r in range(len(GRID)):
            for c in range(len(GRID[0])):
                GRID[r][c].fill = WHITE

class ChangeCell(Button):
    def __init__(self, pos, color, size, new_color):
        super().__init__(pos, color, size)
        self.new_color = new_color
    def on_click(self):
        global CELL_CHANGE
        CELL_CHANGE = self.new_color

class RandomizeGrid(Button):
    def __init__(self, pos, color, size):
        super().__init__(pos, color, size)
    def on_click(self):
        randomize_grid()

# Create and draw the grid
def make_grid(grid):
    cell_sprites = pygame.sprite.Group()
    blockSize = 20

    for c in range(0, blockSize * COL_NUM, blockSize):
        for r in range(0, blockSize * ROW_NUM, blockSize):
            cell_sprites.add(CellBtn(
            (c + (SCREEN_WIDTH / 2) - (blockSize * COL_NUM / 2),
            r + (SCREEN_HEIGHT / 2) - (blockSize * ROW_NUM / 2)),
            grid[int(r/blockSize)][int(c/blockSize)].fill, (blockSize, blockSize), (int(r/blockSize), int(c/blockSize))))

    return cell_sprites

# Randomize each cell of the grid
def randomize_grid():
    rand = -1
    row_len = len(GRID)
    col_len = len(GRID[0])

    for r in range(row_len):
        for c in range(col_len):
            rand = random.randrange(10)
            if rand % 3 == 0:
                GRID[r][c].fill = BLACK
            else:
                GRID[r][c].fill = WHITE

    if (row_len > 1) or (col_len > 1):
        randr = random.randrange(row_len)
        randc = random.randrange(col_len)
        GRID[randr][randc].fill = GREEN

        randre = random.randrange(row_len)
        if randre == randr:
            randce = random.choice(list(set(range(col_len)) - set([randc])))
        else:
            randce = random.randrange(col_len)
        GRID[randre][randce].fill = RED
