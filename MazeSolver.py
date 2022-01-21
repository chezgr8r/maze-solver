import pygame, sys
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
# WHAT IT NEEDS: fill(WHITE, BLACK, RED, GREEN, BLUE), step(int)
@dataclass
class Cell:
    fill: (int, int, int)
    step: int

# Global variables
WHITE = (255, 255, 255)
GREY = (200, 200, 200)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
COL_NUM = 1
ROW_NUM = 1
CELL_CHANGE = BLACK

# Initialize PyGame
pygame.init()
clock = pygame.time.Clock()
screen_d = Vector2(SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode((screen_d.x, screen_d.y))

# So you can close the window
def check_quit(run):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    return run

# Function to create a new, blank cell
def new_cell():
    return Cell(WHITE, -1)

# Create global grid
GRID = [[new_cell()]]

# Creates all the text on screen
def create_text(col_text, row_text, clear_text):
    screen.blit(col_text, (20, 10))
    screen.blit(row_text, (40, 40))
    screen.blit(clear_text, (180, 15))

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
            for i in GRID:
                i.append(new_cell())
            COL_NUM += 1
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
            for i in range(len(GRID[0])):
                new_row.append(new_cell())
            GRID.append(new_row)
            ROW_NUM += 1
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
        global CELL_CHANGE, GRID
        GRID[self.coord[0]][self.coord[1]].fill = CELL_CHANGE

class ClearGrid(Button):
    def __init__(self, pos, color, size):
        super().__init__(pos, color, size)
    def on_click(self):
        global GRID, WHITE
        for r in range(len(GRID)):
            for c in range(len(GRID[0])):
                GRID[r][c].fill = WHITE

def make_grid(grid):
    #make grid lol
    #should this be a grid of buttons?
    cell_sprites = pygame.sprite.Group()
    blockSize = 20 #Set the size of the grid block
    #xcount = 0
    #ycount = 0
    for c in range(0, blockSize * COL_NUM, blockSize):
        for r in range(0, blockSize * ROW_NUM, blockSize):
            #print(((int(r/blockSize)), int(c/blockSize)))
            cell_sprites.add(CellBtn(
            (c + (SCREEN_WIDTH / 2) - (blockSize * COL_NUM / 2),
            r + (SCREEN_HEIGHT / 2) - (blockSize * ROW_NUM / 2)),
            grid[int(r/blockSize)][int(c/blockSize)].fill, (blockSize, blockSize), (int(r/blockSize), int(c/blockSize))))
            #ycount += 1

            #print((int(x/blockSize), int(y/blockSize)))

            #rect = pygame.Rect(
            #    x + (SCREEN_WIDTH / 2) - (blockSize * COL_NUM / 2),
            #    y + (SCREEN_HEIGHT / 2) - (blockSize * ROW_NUM / 2),
            #    blockSize, blockSize)
            #pygame.draw.rect(screen, BLACK, rect, 1)
        #xcount += 1
    #cell_sprites.draw(screen)
    #print(cell_sprites)
    return cell_sprites

def main():
    # PyGame window initialization
    pygame.display.set_caption("Maze Solver")
    icon = pygame.image.load("mazeicon.png").convert_alpha()
    pygame.display.set_icon(icon)

    # Color screen
    back_color = GREY
    screen.fill(back_color)
    pygame.display.update()

    # TODO: Create a default grid and buttons to change grid size
    # Changing grid size should keep grid roughly the same size, just with more cells --> MATH
    # Might be a good idea to set a maximum and mimimum grid size

    # Create text images
    font1 = pygame.font.SysFont('comicsansms', 24)
    font2 = pygame.font.SysFont('comicsansms', 18)
    col_text = font1.render('- COLUMN +', True, BLACK)
    row_text = font1.render('- ROW +', True, BLACK)
    clear_text = font2.render('Clear Grid', True, BLACK)
    create_text(col_text, row_text, clear_text)

    # Create buttons
    #def __init__(self, pos, image, screen, on_click)
    input_sprites = pygame.sprite.Group()
    col_up = ColUpBtn((153, 29), GREEN, (20, 20))
    col_down = ColDownBtn((25, 29), RED, (20, 20))
    row_up = RowUpBtn((130, 60), GREEN, (20, 20))
    row_down = RowDownBtn((45, 60), RED, (20, 20))
    clear_grid = ClearGrid((222, 28), RED, (90, 25))
    input_sprites.add(col_up, col_down, row_up, row_down, clear_grid)

    #cell_sprites = pygame.sprite.Group()
    #cell_sprites.add(CellBtn(
    #((SCREEN_WIDTH / 2) - (20 * COL_NUM / 2),
    #(SCREEN_HEIGHT / 2) - (20 * ROW_NUM / 2)),
    #GRID[0][0].fill, (20, 20), (0, 0)))
    # Print fonts
    #fonts = pygame.font.get_fonts()
    #print(len(fonts))
    #for f in fonts:
    #    print(f)

    while True:
        grid_sprites = make_grid(GRID)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                x,y = event.pos
                for btn in input_sprites:
                    if btn.rect.collidepoint(x,y):
                        btn.on_click()
                        #print((ROW_NUM, COL_NUM))
                for cel in grid_sprites:
                    if cel.rect.collidepoint(x,y):
                        cel.on_click()

        #pygame.display.update()
        pygame.display.flip()
        screen.fill(back_color)
        input_sprites.draw(screen)
        create_text(col_text, row_text, clear_text)
        grid_sprites.draw(screen)
        clock.tick(60)

if __name__ == "__main__":
    main()
