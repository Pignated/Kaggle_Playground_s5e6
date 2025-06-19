import pygame as pg 
pg.init()
window_height = 300
window_width = 400
scr = pg.display.set_mode((window_width, window_height))
pg.display.set_caption("Tic Tac Toe")
pg.display.set_icon(pg.image.load("tic-tac-toe.png"))
grid_box_width = 70
grid_box_height = 70
grid_margin = 7
grid_height = grid_box_height * 3 + grid_margin * 4
grid_width = grid_box_width * 3 + grid_margin * 4
grid_surface = scr.subsurface(pg.Rect(0, 0, grid_width, grid_height))

#game state data
grid=[]
for row in range(3):
    grid.append([])
    for column in range(3):
        grid[row].append(0)
red_score = blue_score = winner_code = 0
red_turn = red_last_starter = True
game_over = False
clock = pg.time.Clock()

def draw_grid(grid, grid_surface):
    grid_surface.fill((255, 255, 255))
    for row in range(3):
        for column in range(3):
            x = column * (grid_box_width + grid_margin) + grid_margin
            y = row * (grid_box_height + grid_margin) + grid_margin
            if grid[row][column] == 1:
                pg.draw.rect(grid_surface, (255, 0, 0), (x, y, grid_box_width, grid_box_height), border_radius=10)
            elif grid[row][column] == 2:
                pg.draw.rect(grid_surface, (0, 0, 255), (x, y, grid_box_width, grid_box_height), border_radius=10)
            else:
                pg.draw.rect(grid_surface, (200, 200, 200), (x, y, grid_box_width, grid_box_height), border_radius=10)

def reset_game(grid, red_turn, red_last_starter, winner_code,game_over):
    grid = [[0] * 3 for _ in range(3)]
    red_turn = red_last_starter
    winner_code = 0
    game_over = False
    return grid, red_turn, red_last_starter, winner_code, game_over

reset_box_rect= pg.Rect(0, grid_height, grid_width, window_height - grid_height)
reset_box_surface = scr.subsurface(reset_box_rect)
reset_button = pg.Rect(0, 0, 120, 20)
reset_button.center = reset_box_surface.get_rect().center
reset_text = pg.font.SysFont("Arial", 20).render("Reset", True, (0, 0, 0))
reset_rext_rect = reset_text.get_rect(center=reset_button.center)
def draw_reset_button():
    reset_box_surface.fill((255, 255, 255))
    pg.draw.rect(reset_box_surface, (255, 0, 255), reset_button,border_radius=10)
    reset_box_surface.blit(reset_text, reset_rext_rect)

scoreboard_surface = scr.subsurface(pg.Rect(grid_width + grid_margin, grid_margin, window_width - grid_width - grid_margin * 2, window_height - 2 * grid_margin))
def draw_scoreboard(red_score, blue_score, red_turn, scoreboard_surface):
    scoreboard_surface.fill((255, 255, 255))
    scoreboard_text = pg.font.SysFont("Arial", 20).render(f"Red: {red_score:g}\nBlue: {blue_score:g}\n" + ("Red's turn" if red_turn else "Blue's turn"), True, (0, 0, 0))
    scoreboard_surface.blit(scoreboard_text, (10, 10))

def draw_game_completed(winner_code):
    if winner_code == 1:
        message = "Red wins!"
    elif winner_code == 2:
        message = "Blue wins!"
    elif winner_code == -1:
        message = "It's a draw!"
    if winner_code != 0:
        game_over_surface = pg.Surface((grid_width,grid_height),pg.SRCALPHA)
        game_over_rect = pg.Rect((0,0, 2*grid_width//3, grid_height//4))
        game_over_rect.center = (grid_width//2, grid_height // 2)
        game_over_text = pg.font.SysFont("Arial", 30).render(message, True, (255, 153, 0))
        game_over_text_rect = game_over_text.get_rect(center=game_over_rect.center)
        pg.draw.rect(game_over_surface, (0, 0, 0,200), game_over_rect, border_radius=10)
        game_over_surface.blit(game_over_text, game_over_text_rect)
        scr.blit(game_over_surface, (0,0))
    return


def score(red_score, blue_score, winner_code, red_turn, red_last_starter,game_over):
    if winner_code == 1:
        red_score += 1
        red_turn = red_last_starter = False
    elif winner_code == 2:
        blue_score += 1
        red_turn = red_last_starter = True
    elif winner_code == -1:
        red_score += 0.5
        blue_score += 0.5
        red_turn = not red_last_starter
        red_last_starter = not red_last_starter
    return red_score, blue_score, winner_code, red_turn, red_last_starter, True

def game_won(grid, winner_code):
    # Check rows and columns
    for i in range(3):
        if grid[i][0] == grid[i][1] == grid[i][2] != 0:
            winner_code = grid[i][0]
            return winner_code
        if grid[0][i] == grid[1][i] == grid[2][i] != 0:
            winner_code = grid[0][i]
            return winner_code
    if grid[0][0] == grid[1][1] == grid[2][2] != 0 or grid[0][2] == grid[1][1] == grid[2][0] != 0:
        winner_code = grid[1][1]
        return winner_code
    if all(cell != 0 for row in grid for cell in row):
        return -1  # Draw
    return 0# No winner yet

done=False
while not done:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True
        elif event.type == pg.MOUSEBUTTONDOWN:
            pos = pg.mouse.get_pos()
            reset_relative_pos = pos[0] - reset_box_rect.x, pos[1] - reset_box_rect.y
            if reset_button.collidepoint(reset_relative_pos):
                # Reset the game
                grid = [[0] * 3 for _ in range(3)]
                grid, red_turn, red_last_starter, winner_code, game_over = reset_game(grid, red_turn, red_last_starter, winner_code,game_over)
            else:
                column = pos[0] // (grid_box_width + grid_margin)
                row = pos[1] // (grid_box_height + grid_margin)
                if column < 3 and row < 3 and grid[row][column] == 0 and not game_over:
                    grid[row][column] = 1 if red_turn else 2
                    red_turn = not red_turn
            winner_code = game_won(grid, winner_code)
            if winner_code != 0 and not game_over:
                red_score, blue_score, winner_code, red_turn, red_last_starter, game_over = score(red_score, blue_score, winner_code, red_turn, red_last_starter, game_over)
    draw_scoreboard(red_score, blue_score, red_turn, scoreboard_surface)
    draw_grid(grid, grid_surface)
    if game_over:
        draw_game_completed(winner_code)
    draw_reset_button()
    clock.tick(50)
    pg.display.flip()
pg.quit()