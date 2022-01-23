import pygame, sys, random
from Dijkstra import *

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
            for i in range(len(GRID)): #THIS LOGIC DOESN'T WORK
                GRID[i].append(new_cell((i, COL_NUM)))
            COL_NUM += 1
            print(GRID)

class ColDownBtn(Button):
    def __init__(self, pos, color, size):
        super().__init__(pos, color, size)
    def on_click(self):
        global COL_NUM
        if COL_NUM > 1:
            for i in GRID:
                i.pop()
            COL_NUM -= 1
            print(GRID)

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
            print(GRID)

class RowDownBtn(Button):
    def __init__(self, pos, color, size):
        super().__init__(pos, color, size)
    def on_click(self):
        global ROW_NUM
        if ROW_NUM > 1:
            GRID.pop()
            ROW_NUM -= 1
            print(GRID)

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
        print("attempted clear")
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

class DijkstraButton(Button):
    def __init__(self, pos, color, size):
        super().__init__(pos, color, size)
    def on_click(self):
        global DIJKSTRA_ANIMATE, DIJKSTRA_FAIL, DIJKSTRA_STEPS
        DIJKSTRA_FAIL = False
        DIJKSTRA_ANIMATE = False
        DIJKSTRA_STEPS = dijkstra()
        print(DIJKSTRA_STEPS)
        if DIJKSTRA_STEPS == None:
            DIJKSTRA_FAIL = True
        else:
            DIJKSTRA_ANIMATE = True
        print("dij animate")
        print(DIJKSTRA_ANIMATE) # for some reason MazeSolver isn't recognizing this change
        # DIJKSTRA_ANIMATE is getting assigned here, how can I check for its assignment in MazeSolver?
        return DIJKSTRA_ANIMATE, DIJKSTRA_FAIL, DIJKSTRA_STEPS
        '''
        DIJKSTRA_END = dij_tup[1]
        vis = dij_tup[0]
        i = 0
        while not not vis:
            new_step = []
            for v in range(len(vis)):
                if v.cell.step == i:
                    new_step.append(v)
            DIJKSTRA_STEPS.append(new_step)
            i += 1
        DIJKSTRA_ANIMATE = True
        '''
        # figure out how to animate dijkstra's
        # make sure to check for None in dij_tup[1]
        # idea: use global variables to create list of lists where each list is a step
        #       taken from dij_tup[0] (<-- visited nodes) and set AnimateDij to True,
        #       then in the drawing section of main() have an if statement for if
        #       AnimateDij run animate_dij() function

class ResetButton(Button):
    def __init__(self, pos, color, size):
        super().__init__(pos, color, size)
    def on_click(self, START, END, DIJKSTRA_STEPS):
        #global START, END, DIJKSTRA_STEPS
        print(START)
        reset(START, END, DIJKSTRA_STEPS)#START, END, DIJKSTRA_STEPS

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

def reset(START, END, DIJKSTRA_STEPS):#START, END, DIJKSTRA_STEPS
    global GRID, WHITE, GREEN, RED
    # reset all in DIJKSTRA_STEPS on GRID to WHITE except START and END
    print(START)
    for stp in DIJKSTRA_STEPS:
        for p in stp:
            if p == START:
                GRID[p[0]][p[1]].fill = GREEN
            elif p == END:
                GRID[p[0]][p[1]].fill = RED
            else:
                GRID[p[0]][p[1]].fill = WHITE
