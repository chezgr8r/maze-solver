from time import sleep
from Buttons import *

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
def create_text(col_text, row_text, clear_text):
    screen.blit(col_text, (20, 10))
    screen.blit(row_text, (40, 40))
    screen.blit(clear_text, (180, 15))


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
    create_text(col_text, row_text, clear_text)

    # Create buttons
    input_sprites = pygame.sprite.Group()
    col_up = ColUpBtn((153, 29), GREEN, (20, 20))
    col_down = ColDownBtn((25, 29), RED, (20, 20))
    row_up = RowUpBtn((130, 60), GREEN, (20, 20))
    row_down = RowDownBtn((45, 60), RED, (20, 20))
    build_wall = ChangeCell((280, 29), BLACK, (20, 20), BLACK)
    destroy_wall = ChangeCell((320, 29), WHITE, (20, 20), WHITE)
    place_start = ChangeCell((350, 29), GREEN, (20, 20), GREEN)
    place_end = ChangeCell((380, 29), RED, (20, 20), RED)
    rand_grid = RandomizeGrid((410, 29), YELLOW, (20, 20))
    input_sprites.add(col_up, col_down, row_up, row_down, build_wall, destroy_wall, place_start, place_end, rand_grid)

    clear_sprites = pygame.sprite.Group()
    clear_grid = ClearGrid((222, 28), RED, (90, 25))
    clear_sprites.add(clear_grid)

    algo_sprites = pygame.sprite.Group()
    dij_button = DijkstraButton((440, 29), BLUE, (20, 20))
    algo_sprites.add(dij_button)

    reset_sprites = pygame.sprite.Group()
    reset_button = ResetButton((470, 29), RED, (20, 30))
    reset_sprites.add(reset_button)

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
                for cel in grid_sprites:
                    if cel.rect.collidepoint(x,y):
                        cel.on_click()
                for clr in clear_sprites:
                    if clr.rect.collidepoint(x,y):
                        clr.on_click()
                        START = None
                        END = None
                for alg in algo_sprites:
                    if alg.rect.collidepoint(x,y):
                        DIJKSTRA_ANIMATE, DIJKSTRA_FAIL, DIJKSTRA_STEPS = alg.on_click()
                for res in reset_sprites:
                    if res.rect.collidepoint(x,y):
                        res.on_click(START, END, DIJKSTRA_STEPS)

        pygame.display.flip()
        screen.fill(back_color)
        input_sprites.draw(screen)
        algo_sprites.draw(screen)
        reset_sprites.draw(screen)
        clear_sprites.draw(screen)
        create_text(col_text, row_text, clear_text)
        grid_sprites.draw(screen)
        if DIJKSTRA_FAIL:
            fontf = pygame.font.SysFont('comicsansms', 32)
            fail_text = font1.render('PLEASE INCLUDE START AND END OR RESET', True, BLACK)
            screen.blit(fail_text, (180, 750))
            pygame.display.update()
            sleep(1.5)
            DIJKSTRA_FAIL = False
        if DIJKSTRA_ANIMATE:
            print("Success")
            print(DIJKSTRA_STEPS)
            # animate dijkstra function
            # PLAN FOR ANIMATE_DIJKSTRA:
            # 1. Find RED in final step, or if red doesn't exist
            # 2. Find path from RED to GREEN if such a path exists using prevPos
            # 3. Animate using a for loop and a timer
            # 4. If path exists, turn all blue not in path to white and path to yellow
            # 5. If path doesn't exist, flash text that says no path then reset
            # OPTIONAL: Create reset button that resets all blue to white except start and end
            # NOT OPTIONAL: Check in dijkstra for blue and don't run if blue exists
            last_step = DIJKSTRA_STEPS[-1]
            print(last_step)
            last = None
            for c in range(len(last_step)):
                if GRID[last_step[c][0]][last_step[c][1]].fill == RED:
                    last = last_step[c]

            # animate
            # ERROR: COLOR CHANGE NOT SHOWING
            for stp in DIJKSTRA_STEPS:
                for c in stp:
                    GRID[c[0]][c[1]].fill = BLUE
                grid_sprites = make_grid(GRID)
                grid_sprites.draw(screen)
                pygame.display.update()
                sleep(1)

            if last != None:
                # reaches red, find path
                path = [last]
                print(last)
                print(GRID[last[0]][last[1]])
                cur_prev = GRID[last[0]][last[1]].prevCell
                while cur_prev != None:
                    print(cur_prev)
                    path.append(cur_prev)
                    cur_prev = GRID[cur_prev[0]][cur_prev[1]].prevCell

                for stp in DIJKSTRA_STEPS:
                    for c in stp:
                        if c in path:
                            GRID[c[0]][c[1]].fill = YELLOW
                        else:
                            GRID[c[0]][c[1]].fill = WHITE

                grid_sprites = make_grid(GRID)
                grid_sprites.draw(screen)
                pygame.display.update()
                START = DIJKSTRA_STEPS[0][0]
                END = last
                print("start")
                print(START)
            else:
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
