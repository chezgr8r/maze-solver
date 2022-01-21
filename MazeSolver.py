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

# Global variables
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
COL_NUM = 1
ROW_NUM = 1
GRID = [[]]

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

# Creates all the text on screen
def create_text(col_text, row_text):
    screen.blit(col_text, (20, 10))
    screen.blit(row_text, (40, 40))

# Button sprite
class Button(pygame.sprite.Sprite):
    def __init__(self, pos, color, size):
        super().__init__()
        self.image = pygame.Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = pos

        #elf.click_fun = on_click_func
        #self.on_click = on_click()

class ColUpBtn(Button):
    def __init__(self, pos, color, size):
        super().__init__(pos, color, size)
    def on_click(self):
        global COL_NUM
        if COL_NUM < 30:
            COL_NUM += 1

class ColDownBtn(Button):
    def __init__(self, pos, color, size):
        super().__init__(pos, color, size)
    def on_click(self):
        global COL_NUM
        if COL_NUM > 1:
            COL_NUM -= 1

class RowUpBtn(Button):
    def __init__(self, pos, color, size):
        super().__init__(pos, color, size)
    def on_click(self):
        global ROW_NUM
        if ROW_NUM < 30:
            ROW_NUM += 1

class RowDownBtn(Button):
    def __init__(self, pos, color, size):
        super().__init__(pos, color, size)
    def on_click(self):
        global ROW_NUM
        if ROW_NUM > 1:
            ROW_NUM -= 1

def make_grid(grid):
    #make grid lol
    blockSize = 20 #Set the size of the grid block
    for x in range(0, blockSize * COL_NUM, blockSize):
        for y in range(0, blockSize * ROW_NUM, blockSize):
            rect = pygame.Rect(
                x + (SCREEN_WIDTH / 2) - (blockSize * COL_NUM / 2),
                y + (SCREEN_HEIGHT / 2) - (blockSize * ROW_NUM / 2),
                blockSize, blockSize)
            pygame.draw.rect(screen, BLACK, rect, 1)

def main():
    # PyGame window initialization
    pygame.display.set_caption("Maze Solver")
    icon = pygame.image.load("mazeicon.png").convert_alpha()
    pygame.display.set_icon(icon)

    # Color screen
    back_color = WHITE
    screen.fill(back_color)
    pygame.display.update()

    # TODO: Create a default grid and buttons to change grid size
    # Changing grid size should keep grid roughly the same size, just with more cells --> MATH
    # Might be a good idea to set a maximum and mimimum grid size

    # Create text images
    font = pygame.font.SysFont('comicsansms', 24)
    col_text = font.render('- COLUMN +', True, BLACK)
    row_text = font.render('- ROW +', True, BLACK)
    create_text(col_text, row_text)

    # Create buttons
    #def __init__(self, pos, image, screen, on_click)
    input_sprites = pygame.sprite.Group()
    col_up = ColUpBtn((153, 29), GREEN, (20, 20))
    col_down = ColDownBtn((25, 29), RED, (20, 20))
    row_up = RowUpBtn((130, 60), GREEN, (20, 20))
    row_down = RowDownBtn((45, 60), RED, (20, 20))
    input_sprites.add(col_up, col_down, row_up, row_down)

    # Print fonts
    #fonts = pygame.font.get_fonts()
    #print(len(fonts))
    #for f in fonts:
    #    print(f)

    while True:
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

        #pygame.display.update()
        pygame.display.flip()
        screen.fill(back_color)
        input_sprites.draw(screen)
        create_text(col_text, row_text)
        make_grid(GRID)
        clock.tick(60)

if __name__ == "__main__":
    main()
