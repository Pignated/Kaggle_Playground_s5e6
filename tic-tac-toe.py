import pygame as pg
black = (0,0,0)
white = (255,255,255)

red = (255,0,0)
grid_width=70
grid_height=70
grid_margin = 7
grid=[]
red_score=0
blue_score=0

tot_grid_width = grid_width * 3 + grid_margin * 4
tot_grid_height = grid_height * 3 + grid_margin * 4
red_turn = True
red_last_starter = True
for row in range(3):
    grid.append([])
    for column in range(3):
        grid[row].append(0)
pg.init()
window_height = 300
window_width = 400
scr = pg.display.set_mode([window_width, window_height])
pg.display.set_caption("Tic Tac Toe")
done = False
clock = pg.time.Clock()
scoreboard = pg.Rect(tot_grid_width+grid_margin, grid_margin, window_width - tot_grid_width-grid_margin*2, window_height-2*grid_margin)
scoreboard_surface = scr.subsurface(scoreboard)
reset_text = pg.font.SysFont("Arial", 20).render("Reset", True, black)
reset_button = pg.Rect(0,0, 120, 20)
reset_button.center = ((tot_grid_height)/2, (tot_grid_width+window_height)/2)
reset_text_rect = reset_text.get_rect(center=reset_button.center)
round = 0
winner_code = 0

while not done:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True
        elif event.type == pg.MOUSEBUTTONDOWN and pg.mouse.get_focused() == 1:
            pos = pg.mouse.get_pos()
            column = pos[0] // (grid_width + grid_margin)
            row = pos[1] // (grid_height + grid_margin)
            if column < 3 and row < 3 and winner_code == 0:
                if grid[row][column] == 0:
                    if red_turn:
                        grid[row][column] = 1
                        red_turn = False
                    else:
                        grid[row][column] = 2
                        red_turn = True
                    round += 1
                    if round >= 5:
                        # Check for a win
                        for r in range(3):
                            if grid[r][0] == grid[r][1] == grid[r][2] != 0:
                                winner_code = grid[r][0]
                        for c in range(3):
                            if grid[0][c] == grid[1][c] == grid[2][c] != 0:
                                winner_code = grid[0][c]
                        if grid[0][0] == grid[1][1] == grid[2][2] != 0 or grid[0][2] == grid[1][1] == grid[2][0] != 0:
                            winner_code = grid[1][1]
            if round >= 9 and winner_code == 0:
                winner_code = -1
            if reset_button.collidepoint(pos):
                grid = [[0 for _ in range(3)] for _ in range(3)]
                if winner_code == 0:
                    red_turn = not red_last_starter
                    red_last_starter = not red_last_starter
                winner_code = 0
                round = 0
   

    scr.fill(black)
    for row in range(3):
        for column in range(3):
            color = white
            if grid[row][column] == 1:
                color = red
            elif grid[row][column] == 2:
                color = (0, 0, 255)
            pg.draw.rect(scr, color, [(grid_margin + grid_width) * column + grid_margin,
                                       (grid_margin + grid_height) * row + grid_margin, grid_width, grid_height])

    pg.draw.rect(scr,white,(0,tot_grid_height, tot_grid_width, 300-(tot_grid_height)))
    pg.draw.rect(scr,(255,0,255), reset_button,border_radius=10)
    pg.draw.rect(scr, (255,255,255), scoreboard,border_radius=10)
    scr.blit(reset_text, reset_text_rect)
    if winner_code > 0:
        font = pg.font.SysFont("Arial", 30)
        if winner_code == 1:
            text = font.render("Red wins!", True, (255,153,0))
            red_score += 1
            winner_code = 3
            red_turn = False
            red_last_starter = False
        elif winner_code == 2:
            text = font.render("Blue wins!", True, (255,153,0))
            blue_score += 1
            winner_code = 3
            red_turn = True
            red_last_starter = True
        text_rect = text.get_rect(center=(tot_grid_height/2, tot_grid_width/2))
        pg.draw.rect(scr, (0, 0, 0), text_rect.inflate(10,10), border_radius=10)
        
        scr.blit(text, text_rect)
    elif round == 9:
        font = pg.font.SysFont("Arial", 30)
        text = font.render("It's a draw!", True, (255,153,0))
        text_rect = text.get_rect(center=(tot_grid_height/2, tot_grid_width/2))
        pg.draw.rect(scr, (0, 0, 0), text_rect.inflate(10,10), border_radius=10)
        scr.blit(text, text_rect)
        if winner_code != 3:
            red_score +=.5
            blue_score +=.5
            winner_code = 3
            red_turn = not red_last_starter
    #wrap into update scoreboard function called by increasing score
    score_text = pg.font.SysFont("Arial", 20).render(f"Red: {red_score} \nBlue: {blue_score}\n" + ("Red's turn" if red_turn else "Blue's turn"), True, black)
    scoreboard_surface.fill((255,0,255))
    scoreboard_surface.blit(score_text, (10, 10))
    clock.tick(50)
    pg.display.flip()
pg.quit()