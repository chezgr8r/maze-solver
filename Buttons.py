import pygame, sys, random
from Dijkstra import *

# Basic button sprite
class Button(pygame.sprite.Sprite):
    def __init__(self, pos, color, size):
        super().__init__()
        self.image = pygame.Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = pos

# Button for increasing the number of columns
class ColUpBtn(Button):
    def __init__(self, pos, color, size):
        super().__init__(pos, color, size)
    def on_click(self):
        global COL_NUM
        global GRID
        if COL_NUM < 30:
            for i in range(len(GRID)): #THIS LOGIC DOESN'T WORK
                GRID[i].append(new_cell((i, COL_NUM)))
            COL_NUM += 1

# Button for decreasing the number of columns
class ColDownBtn(Button):
    def __init__(self, pos, color, size):
        super().__init__(pos, color, size)
    def on_click(self):
        global COL_NUM
        if COL_NUM > 1:
            for i in GRID:
                i.pop()
            COL_NUM -= 1

# Button for increasing the number of rows
class RowUpBtn(Button):
    def __init__(self, pos, color, size):
        super().__init__(pos, color, size)
    def on_click(self):
        global ROW_NUM
        if ROW_NUM < 30:
            new_row = []
            for i in range(len(GRID[0])):
                new_row.append(new_cell((ROW_NUM, i)))
            GRID.append(new_row)
            ROW_NUM += 1

# Button for decreasing the number of rows
class RowDownBtn(Button):
    def __init__(self, pos, color, size):
        super().__init__(pos, color, size)
    def on_click(self):
        global ROW_NUM
        if ROW_NUM > 1:
            GRID.pop()
            ROW_NUM -= 1

# Makes a cell into a button
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
        # Check for existing start/end cells before placing new ones
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

# Button that clears the grid completely
class ClearGrid(Button):
    def __init__(self, pos, color, size):
        super().__init__(pos, color, size)
    def on_click(self):
        global GRID, WHITE
        for r in range(len(GRID)):
            for c in range(len(GRID[0])):
                GRID[r][c].fill = WHITE

# Button that changes the color of a grid cell
class ChangeCell(Button):
    def __init__(self, pos, color, size, new_color):
        super().__init__(pos, color, size)
        self.new_color = new_color
    def on_click(self):
        global CELL_CHANGE
        CELL_CHANGE = self.new_color

# Button that randomizes the grid
class RandomizeGrid(Button):
    def __init__(self, pos, color, size):
        super().__init__(pos, color, size)
    def on_click(self):
        randomize_grid()

# Button that runs Dijkstra's algorithm
class DijkstraButton(Button):
    def __init__(self, pos, color, size):
        super().__init__(pos, color, size)
    def on_click(self):
        global DIJKSTRA_ANIMATE, DIJKSTRA_FAIL, DIJKSTRA_STEPS
        DIJKSTRA_FAIL = False
        DIJKSTRA_ANIMATE = False
        DIJKSTRA_STEPS = dijkstra()

        if DIJKSTRA_STEPS == None:
            DIJKSTRA_FAIL = True
        else:
            DIJKSTRA_ANIMATE = True

        return DIJKSTRA_ANIMATE, DIJKSTRA_FAIL, DIJKSTRA_STEPS

# Button that resets the board after running Dijkstra's algorithm
class ResetButton(Button):
    def __init__(self, pos, color, size):
        super().__init__(pos, color, size)
    def on_click(self, START, END, DIJKSTRA_STEPS):
        reset(START, END, DIJKSTRA_STEPS)

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

    # Randomizes white/black cells
    for r in range(row_len):
        for c in range(col_len):
            rand = random.randrange(10)
            if rand % 3 == 0:
                GRID[r][c].fill = BLACK
            else:
                GRID[r][c].fill = WHITE

    # Makes sure its possible to place both a start and end, then makes sure
    #   to place them in different cells using sets
    if (row_len > 1) or (col_len > 1):
        randr = random.randrange(row_len)
        randc = random.randrange(col_len)
        GRID[randr][randc].fill = GREEN

        if col_len > 1:
            randre = random.randrange(row_len)
            if randre == randr:
                randce = random.choice(list(set(range(col_len)) - set([randc])))
            else:
                randce = random.randrange(col_len)
        else:
            randce = random.randrange(col_len)
            if randce == randc:
                randre = random.choice(list(set(range(row_len)) - set([randr])))
            else:
                randre = random.randrange(row_len)
        GRID[randre][randce].fill = RED

def reset(START, END, DIJKSTRA_STEPS):
    global GRID, WHITE, GREEN, RED

    # Resets all visited cells to blue unless the its the start or end
    for stp in DIJKSTRA_STEPS:
        for p in stp:
            if p == START:
                GRID[p[0]][p[1]].fill = GREEN
            elif p == END:
                GRID[p[0]][p[1]].fill = RED
            else:
                GRID[p[0]][p[1]].fill = WHITE
