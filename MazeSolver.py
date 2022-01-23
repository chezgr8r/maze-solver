from time import sleep
from Buttons import *

# Initialize PyGame
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# So you can close the window
def check_quit(run):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    return run

# Creates all the text on screen
def create_text(col_text, row_text, clear_text, wall_text, break_wall_text, start_text, end_text, rand_text, dij_text, reset_text):
    screen.blit(col_text, (20, 10))
    screen.blit(row_text, (40, 40))
    screen.blit(clear_text, (180, 15))
    screen.blit(wall_text, (200, 45))
    screen.blit(break_wall_text, (325, 15))
    screen.blit(start_text, (325, 45))
    screen.blit(end_text, (450, 45))
    screen.blit(rand_text, (450, 15))
    screen.blit(dij_text, (590, 15))
    screen.blit(reset_text, (590, 45))

# Main function
def main():
    global DIJKSTRA_FAIL, DIJKSTRA_ANIMATE, DIJKSTRA_STEPS, START, END

    # PyGame window initialization
    pygame.display.set_caption("Maze Solver")
    icon = pygame.image.load("mazeicon.png").convert_alpha()
    pygame.display.set_icon(icon)

    # Color screen
    back_color = GREY
    screen.fill(back_color)
    pygame.display.update()

    # Create text images
    font1 = pygame.font.SysFont('comicsansms', 24)
    font2 = pygame.font.SysFont('comicsansms', 18)
    col_text = font1.render('- COLUMN +', True, BLACK)
    row_text = font1.render('- ROW +', True, BLACK)
    clear_text = font2.render('Clear Grid', True, BLACK)
    wall_text = font2.render('Place Wall', True, BLACK)
    break_wall_text = font2.render('Break Wall', True, BLACK)
    start_text = font2.render('Start Tile', True, BLACK)
    end_text = font2.render('End Tile', True, BLACK)
    rand_text = font2.render('Randomize', True, BLACK)
    dij_text = font2.render("Run Dijkstra's Algorithm", True, BLACK)
    reset_text = font2.render('Reset Algorithm', True, BLACK)

    # Create buttons
    # Grid manipulation
    input_sprites = pygame.sprite.Group()
    col_up = ColUpBtn((153, 29), GREEN, (20, 20))
    col_down = ColDownBtn((25, 29), RED, (20, 20))
    row_up = RowUpBtn((130, 60), GREEN, (20, 20))
    row_down = RowDownBtn((45, 60), RED, (20, 20))
    build_wall = ChangeCell((187, 58), BLACK, (20, 20), BLACK)
    destroy_wall = ChangeCell((310, 28), WHITE, (20, 20), WHITE)
    place_start = ChangeCell((310, 58), GREEN, (20, 20), GREEN)
    place_end = ChangeCell((435, 58), RED, (20, 20), RED)
    input_sprites.add(col_up, col_down, row_up, row_down, build_wall, destroy_wall, place_start, place_end)

    # Clear button
    clear_sprites = pygame.sprite.Group()
    clear_grid = ClearGrid((222, 28), RED, (90, 25))
    rand_grid = RandomizeGrid((435, 28), YELLOW, (20, 20))
    clear_sprites.add(clear_grid, rand_grid)

    # Algorithm button(s)
    algo_sprites = pygame.sprite.Group()
    dij_button = DijkstraButton((575, 28), BLUE, (20, 20))
    algo_sprites.add(dij_button)

    # Reset button
    reset_sprites = pygame.sprite.Group()
    reset_button = ResetButton((575, 58), ORANGE, (20, 20))
    reset_sprites.add(reset_button)

    # Main loop
    while True:
        # Create grid_sprites
        grid_sprites = make_grid(GRID)
        # Check for PyGame events
        for event in pygame.event.get():
            # Quit program if X button clicked
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Check for mouse input
            if event.type == pygame.MOUSEBUTTONUP:
                x,y = event.pos # Coordinates of mouse click
                for btn in input_sprites: # Iterate through group of sprites
                    if btn.rect.collidepoint(x,y): # Check for collision
                        btn.on_click()
                for cel in grid_sprites:
                    if cel.rect.collidepoint(x,y):
                        cel.on_click()
                for clr in clear_sprites:
                    if clr.rect.collidepoint(x,y):
                        clr.on_click()
                        # Clear START/END history
                        START = None
                        END = None
                        DIJKSTRA_STEPS = []
                for alg in algo_sprites:
                    if alg.rect.collidepoint(x,y):
                        # Assign global variables for drawing
                        DIJKSTRA_ANIMATE, DIJKSTRA_FAIL, DIJKSTRA_STEPS = alg.on_click()
                for res in reset_sprites:
                    if res.rect.collidepoint(x,y):
                        res.on_click(START, END, DIJKSTRA_STEPS)

        # Draw everything
        pygame.display.flip()
        screen.fill(back_color)
        input_sprites.draw(screen)
        algo_sprites.draw(screen)
        reset_sprites.draw(screen)
        clear_sprites.draw(screen)
        create_text(col_text, row_text, clear_text, wall_text, break_wall_text, start_text, end_text, rand_text, dij_text, reset_text)
        grid_sprites.draw(screen)
        # Check if Dijkstra button has been clicked
        if DIJKSTRA_FAIL: # Fails if start/end aren't placed or if grid needs to be reset
            fontf = pygame.font.SysFont('comicsansms', 32)
            fail_text = font1.render('PLEASE INCLUDE START AND END OR RESET', True, BLACK)
            screen.blit(fail_text, (140, 750))
            pygame.display.update()
            sleep(1.5)
            DIJKSTRA_FAIL = False
        if DIJKSTRA_ANIMATE: # Animates process of Dijkstra's algorithm
            # Finds if Dijkstra reached red by checking last step
            last_step = DIJKSTRA_STEPS[-1]
            last = None
            for c in range(len(last_step)):
                if GRID[last_step[c][0]][last_step[c][1]].fill == RED:
                    last = last_step[c]

            # Animate
            for stp in DIJKSTRA_STEPS:
                for c in stp:
                    GRID[c[0]][c[1]].fill = BLUE
                grid_sprites = make_grid(GRID)
                grid_sprites.draw(screen)
                pygame.display.update()
                sleep(0.4)

            # Different end results if Dijkstra reaches end or not
            if last != None:
                # End was found, trace path using Cell data
                path = [last]
                cur_prev = GRID[last[0]][last[1]].prevCell
                while cur_prev != None: # Start is guarenteed to exist
                    path.append(cur_prev)
                    cur_prev = GRID[cur_prev[0]][cur_prev[1]].prevCell

                # Clear blue and make final path yellow
                for stp in DIJKSTRA_STEPS:
                    for c in stp:
                        if c in path:
                            GRID[c[0]][c[1]].fill = YELLOW
                        else:
                            GRID[c[0]][c[1]].fill = WHITE

                # Draw new grid
                grid_sprites = make_grid(GRID)
                grid_sprites.draw(screen)
                pygame.display.update()
                START = DIJKSTRA_STEPS[0][0]
                END = last
            else:
                # End wasn't found, reset
                fontf = pygame.font.SysFont('comicsansms', 32)
                fail_text = font1.render('NO PATH EXISTS', True, BLACK)
                screen.blit(fail_text, (180, 750))
                pygame.display.update()
                sleep(1.5)
                START = DIJKSTRA_STEPS[0][0]
                for r in range(len(GRID)):
                    for c in range(len(GRID[0])):
                        if GRID[r][c].fill == RED:
                            END = (r, c)
                reset(START, END, DIJKSTRA_STEPS)

            DIJKSTRA_ANIMATE = False
        clock.tick(60)

if __name__ == "__main__":
    main()
