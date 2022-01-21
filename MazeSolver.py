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
    clear_grid = ClearGrid((222, 28), RED, (90, 25))
    build_wall = ChangeCell((280, 29), BLACK, (20, 20), BLACK)
    destroy_wall = ChangeCell((320, 29), WHITE, (20, 20), WHITE)
    place_start = ChangeCell((350, 29), GREEN, (20, 20), GREEN)
    place_end = ChangeCell((380, 29), RED, (20, 20), RED)
    rand_grid = RandomizeGrid((410, 29), YELLOW, (20, 20))
    input_sprites.add(col_up, col_down, row_up, row_down, clear_grid, build_wall, destroy_wall, place_start, place_end, rand_grid)

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

        pygame.display.flip()
        screen.fill(back_color)
        input_sprites.draw(screen)
        create_text(col_text, row_text, clear_text)
        grid_sprites.draw(screen)
        clock.tick(60)

if __name__ == "__main__":
    main()
