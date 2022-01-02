

import pygame
import time
import random
import sys
import json
import ConstellationMapGeneration as gen
import ConstellationBot2 as bot

pygame.init()

screen_dimensions = [1440, 760]
screen = pygame.display.set_mode(screen_dimensions, pygame.RESIZABLE)

difficulties = {1:((1,1),(1,1)), 2:((1,1,1),(3,2,1)), 3:((3,2,1),(3,2,1)), 4:((4,3,2,1,1,1), (3, 2, 1.5, 1.25, 1.2, 1.15)), 5:((5,4,3,2,1,1,1),(3, 2, 1.5, 1.25, 1.2, 1.15, 1.1))}

opening_sequence_stars = [[19, 3, 0, 0], [30, 2, 0, 1], [40, 6, 0, 2], [50, 8, 0, 3], [66, 6, 0, 4], [53, 16, 0, 5], [65, 16, 0, 6], 
                          [5, 15, 0, 7], [13, 32, 0, 8], [15, 24, 0, 9], [24, 35, 0, 10], [47, 34, 0, 11], [52, 29, 0, 12], [17, 31, 0, 13], 
                          [21.75, 13.25, 0, 14], [20.5, 15.25, 0, 15], [29.5, 16.25, 0, 16], [37.5, 15.5, 0, 17], [49.5, 16, 0, 18]]


opening_sequence_matrix = [[1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                           [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                           [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                           [0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                           [0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                           [0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                           [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                           [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                           [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0], 
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0], 
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0], 
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0], 
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1]]

black = (0,0,0)
white = (255, 255, 255)
home = (20,20,255)
enemy = (255, 50, 255)
human = (20,255,20)
#first 4 friend, last 4 bot
frienemy_colors = ((20,20,255),(20,255,20),(138,43,226),(0,200,255),(255, 50, 255),(138,43,226), (255, 22, 12),(255, 165, 0))

dddwhite = (20,20,40)
ddwhite = (50, 50, 50)
dwhite = (100,100,100)
yayaya = (150,150,150)
bluish_white = (150,150,250)
dark_white = (150, 150, 150)
dark_blue = (20, 40, 230)
dd_blue = (20, 40, 130)
dark_purple = (230, 50, 230)
dark_green = (15,230,15)
dd_green = (15,110,15)
green = (20,180,20)
red = (235,20,20)
dd_red = (120,20,20)
yellow = (180,180,20)
dd_yellow = (100,100,20)


def render_stars(stars, color=white):
    button_list = []
    for star in stars:
        if star[3] == 10000:
            pygame.draw.circle(screen, bluish_white, ((star[0]*20+10), (star[1]*20+10)), 9)
        elif star[2] == 0:
            pygame.draw.circle(screen, color, ((star[0]*20+10), (star[1]*20+10)), 9)
            button_list.append([(star[0]*20 + 10), (star[1]*20 + 10)])
        else:
            pygame.draw.circle(screen, frienemy_colors[star[2] - 1], ((star[0]*20 + 10), (star[1]*20 + 10)), 9)
            button_list.append(None)
        #render_star_tag(star)
    return button_list


def render_conns(stars, adjacency_matrix):
    score = [["Blue",0],["Green",0],["Purple",0],["Cyan",0],["Pink",0],["Purple",0],["Red",0],["Yellow",0]]
    for star in range(len(adjacency_matrix)):
        for conn in range(len(adjacency_matrix[star])):
            if adjacency_matrix[star][conn] == 1:
                if stars[star][2] == stars[conn][2]:
                    if stars[star][2] == 0:
                        pygame.draw.line(screen, white, ((stars[star][0]*20 + 10),(stars[star][1]*20 + 10)), ((stars[conn][0]*20 + 10),(stars[conn][1]*20 + 10)), 4)
                    else:
                        pygame.draw.line(screen, (frienemy_colors[stars[star][2] - 1]), ((stars[star][0]*20 + 10),(stars[star][1]*20 + 10)), ((stars[conn][0]*20 + 10),(stars[conn][1]*20 + 10)), 4)
                        score[stars[star][2] - 1][1] += round(bot.pyth((stars[star][0], stars[star][1]), (stars[conn][0], stars[conn][1])))
                else:
                    pygame.draw.line(screen, white, ((stars[star][0]*20 + 10),(stars[star][1]*20 + 10)), ((stars[conn][0]*20 + 10),(stars[conn][1]*20 + 10)), 4)               
    return score
    

def render_score(score):
    font = pygame.font.SysFont(None, 42)
    num_players = 0
    for scor in score:
        if scor[1] != 0:
            text = font.render((scor[0]+": "+str(scor[1])), True, (white))
            screen.blit(text,(1430 - (len(str(scor[1])) + len(str(scor[0])))*18, 10+num_players*30))  
            num_players += 1
    return score
    
    
def render_star_tag(star_info):
    font = pygame.font.SysFont(None, 30)
    text = font.render((str(star_info[3])), True, (home))
    screen.blit(text,((star_info[0]*20 + 5), (star_info[1]*20+1)))   


def click_check(event, button_list, stars, moves_availiable, color_num):
    buttonclicked = False
    mouse = pygame.mouse.get_pos()
    if event.type == pygame.MOUSEBUTTONDOWN:
            for button in range(len(button_list)):
                if button_list[button] == None:
                    pass
                else:
                    if bot.pyth(button_list[button], mouse) <= 9:
                        buttonclicked = True
                        if moves_availiable >= 1:
                            stars[button][2] = color_num
    return buttonclicked


def opening_sequence(opening_sequence_stars, opening_sequence_matrix):
    pygame.display.flip()
    rectangle_list = [(640,400,1,dark_blue,home),(735,410,1,dark_blue,home),
                      (580,475,2,dark_blue,home),(680,490,2,dark_purple,enemy),(800,480,2,dark_blue,home),
                      (550,540,3,dark_blue,home),(680,550,3,dark_green,human),(820,555,3,dark_blue,home),
                      (625,610,4,dark_blue,home),(755,620,4,dark_blue,home)]
    running = True

    splash_text = random.choice([("Selecting a high bot difficulty and a high number"," of stars means the bot can be quite slow!"),("Tip: Hold SHIFT while changing the game ","parameters - this will increment them by 10"),("Gee, I sure do love splash text!",None),("Play with friends or bots!", None)])
    
    
    while running:
        screen.fill((0, 0, 0))
        mouse = pygame.mouse.get_pos()
        
        font = pygame.font.SysFont(None, 36)
        pygame.draw.rect(screen, home, pygame.Rect(0, 730, 100, 30))

        if mouse[0] >= 0 and mouse[0] <= 100 and mouse[1] >= 730 and mouse[1] <= 760:
            pygame.draw.rect(screen, home, pygame.Rect(0, 725, 105, 35))

        text = font.render(("EXIT"), True, (0,0,0))
        screen.blit(text,(20,735))
        
        in_rectangle = False
        
        smolfont = pygame.font.SysFont('applesymbols', 30)
        for i in range(len(splash_text)):
            text = smolfont.render(splash_text[i], True, white)
            text = pygame.transform.rotate(text, 20)
            screen.blit(text, [40,80+i*40])
        
        for rectangle in rectangle_list:
            if abs(rectangle[0] - mouse[0]) <= 100 and abs(rectangle[1] - mouse[1]) <= 30:
                in_rectangle = True
                rectangle_val = rectangle
        
        if in_rectangle == True:
            for rectangle2 in rectangle_list:
                if rectangle2[2] == rectangle_val[2]:
                    pygame.draw.rect(screen, rectangle2[4], pygame.Rect(rectangle2[0] - 105, rectangle2[1] - 22, 210, 44))
                else:
                    pygame.draw.rect(screen, rectangle2[3], pygame.Rect(rectangle2[0] - 100, rectangle2[1] - 20, 200, 40))
                            
            
        if in_rectangle == False:
            for rectangle3 in rectangle_list:
                pygame.draw.rect(screen, rectangle3[3], pygame.Rect(rectangle3[0] - 100, rectangle3[1] - 20, 200, 40))
        
        x = 20
        y = -20

        font = pygame.font.SysFont('applesymbols', 130)
        text = font.render(("Constellation"), True, (white))
        screen.blit(text,(390+x, 240+y))  
        
        font = pygame.font.SysFont('applesymbols', 60)
        text = font.render(("Single Player"), True, (white))
        text2 = font.render(("Play Against Bots"), True, (white))
        text3 = font.render(("Play Against a Friend"), True, (white))
        text4 = font.render(("Map Generator"), True, (white))
        
        screen.blit(text,(545+x, 400+y))
        screen.blit(text2,(490+x, 470+y))
        screen.blit(text3, (450+x, 540+y))
        screen.blit(text4, (515+x, 610+y))
        
        render_stars(opening_sequence_stars)
        render_conns(opening_sequence_stars, opening_sequence_matrix)
        

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                sys.exit()
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                for rectangle in rectangle_list:
                    if abs(rectangle[0] - mouse[0]) <= 100 and abs(rectangle[1] - mouse[1]) <= 30:
                        gamemode = rectangle[2]
                        running = False
                if mouse[0] >= 0 and mouse[0] <= 100 and mouse[1] >= 730 and mouse[1] <= 760:
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()
        
    return(gamemode)


def sub_opening_sequence(gamemode, premap = False):
    pygame.display.flip()
    running = True
    
    sub_stars = [[43, 4.5, 0, 0], [65, 4.5, 0, 1], [65, 32, 0, 3], [43, 32, 0, 2], [46, 7.5, 0, 0], [62, 7.5, 0, 1], [62, 29, 0, 3], [46, 29, 0, 2]]
    sub_matrix = [[1, 1, 0, 1, 1, 0, 0, 0], 
                  [1, 1, 1, 0, 0, 1, 0, 0], 
                  [0, 1, 1, 1, 0, 0, 1, 0], 
                  [1, 0, 1, 1, 0, 0, 0, 1], 
                  [1, 0, 0, 0, 1, 1, 0, 1], 
                  [0, 1, 0, 0, 1, 1, 1, 0], 
                  [0, 0, 1, 0, 0, 1, 1, 1], 
                  [0, 0, 0, 1, 1, 0, 1, 1]]
    
    stars = 20
    rounds = 10
    movespr = 1
    secondspr = 10
    botsplayers = 1
    difficulty = 3
    
    if gamemode == 1:
        if premap:
            scale_list = [[125,250,100,"Number of Rounds","rounds",rounds], [125,500,10,"Moves Per Round","movespr",movespr]]
        else:
            scale_list = [[175,170,50,"Number of Stars","stars",stars],[175,382.5,100,"Number of Rounds","rounds",rounds], [175,590,10,"Moves Per Round","movespr",movespr]]
    elif gamemode == 2:
        if premap:
            scale_list = [[250,125,100,"Number of Rounds","rounds",rounds], [125,250,10,"Moves Per Round","movespr",movespr],[250,375,30, "Seconds Per Round","secondspr",secondspr],[125,500,4,"Number of Bots","botsplayers",botsplayers],[250,620,5,"Bot Difficulty","difficulty",difficulty]]
        else:
            scale_list = [[125,100,50,"Number of Stars","stars",stars],[250,210,100,"Number of Rounds","rounds",rounds], [125,320,10,"Moves Per Round","movespr",movespr],[250,430,30, "Seconds Per Round","secondspr",secondspr],[125,540,4,"Number of Bots","botsplayers",botsplayers],[250,650,5,"Bot Difficulty","difficulty",difficulty]]
    elif gamemode == 3:
        if premap:
            scale_list = [[175,170,100,"Number of Rounds","rounds",rounds], [175,382.5,10,"Moves Per Round","movespr",movespr],[175,590,3,"Other Players","botsplayers",botsplayers]]
        else:
            scale_list = [[125,180,50,"Number of Stars","stars",stars],[250,315,100,"Number of Rounds","rounds",rounds], [125,450,10,"Moves Per Round","movespr",movespr],[250,580,3,"Other Players","botsplayers",botsplayers]]


    
    tri_size = 30
    
    go_pressed = False
    while running:
        screen.fill((0, 0, 0))
        mouse = pygame.mouse.get_pos()

        font = pygame.font.SysFont(None, 36)
        pygame.draw.rect(screen, home, pygame.Rect(0, 730, 100, 30))

        if mouse[0] >= 0 and mouse[0] <= 100 and mouse[1] >= 730 and mouse[1] <= 760:
            pygame.draw.rect(screen, home, pygame.Rect(0, 725, 105, 35))

        text = font.render(("EXIT"), True, (0,0,0))
        screen.blit(text,(20,735))
        
        keys = pygame.key.get_pressed()
        
        font = pygame.font.SysFont('applesymbols', tri_size*2)
        numfont = pygame.font.SysFont(None, round(tri_size * 1.8))
        playfont = pygame.font.SysFont('applesymbols', 100)
        
        
        if mouse[0] > sub_stars[0][0]*20+10 and mouse[0] < sub_stars[1][0]*20+10 and mouse[1] > sub_stars[1][1]*20+10 and mouse[1] < sub_stars[2][1]*20+10:
             pygame.draw.polygon(screen, dd_green, ((sub_stars[0][0]*20+10, sub_stars[0][1]*20+10),(sub_stars[1][0]*20+10, sub_stars[1][1]*20+10),(sub_stars[2][0]*20+10, sub_stars[2][1]*20+10),(sub_stars[3][0]*20+10, sub_stars[3][1]*20+10)))
             pygame.draw.polygon(screen, dark_green, ((sub_stars[4][0]*20+10, sub_stars[4][1]*20+10),(sub_stars[5][0]*20+10, sub_stars[5][1]*20+10),(sub_stars[6][0]*20+10, sub_stars[6][1]*20+10),(sub_stars[7][0]*20+10, sub_stars[7][1]*20+10)))
             
        if go_pressed == True:
                pygame.draw.polygon(screen, dark_green, ((sub_stars[0][0]*20+10, sub_stars[0][1]*20+10),(sub_stars[1][0]*20+10, sub_stars[1][1]*20+10),(sub_stars[2][0]*20+10, sub_stars[2][1]*20+10),(sub_stars[3][0]*20+10, sub_stars[3][1]*20+10)))
                pygame.draw.polygon(screen, dd_green, ((sub_stars[4][0]*20+10, sub_stars[4][1]*20+10),(sub_stars[5][0]*20+10, sub_stars[5][1]*20+10),(sub_stars[6][0]*20+10, sub_stars[6][1]*20+10),(sub_stars[7][0]*20+10, sub_stars[7][1]*20+10)))
                
        
        render_conns(sub_stars, sub_matrix)
        render_stars(sub_stars)
        
        playtext = playfont.render(("PLAY"), True, (white))
        screen.blit(playtext, (1000, 340))
        
        for scale in scale_list:
            pygame.draw.polygon(screen, white, ((scale[0]-tri_size,scale[1]-tri_size),(scale[0]+tri_size,scale[1]-tri_size),(scale[0],scale[1]-3*tri_size)))
            pygame.draw.polygon(screen, white, ((scale[0]-tri_size,scale[1]+tri_size),(scale[0]+tri_size,scale[1]+tri_size),(scale[0],scale[1]+3*tri_size)))
            
            text = font.render((scale[3]), True, white)
            screen.blit(text, (scale[0]+3*tri_size, scale[1] - 0.8*tri_size))
            numtext = numfont.render((str(scale[5])),True,white)
            screen.blit(numtext, (scale[0]-0.3*tri_size - tri_size*0.4*(len(str(scale[5]))-1), scale[1]-tri_size*0.5))
            
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                sys.exit()
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if mouse[0] > sub_stars[0][0]*20+10 and mouse[0] < sub_stars[1][0]*20+10 and mouse[1] > sub_stars[1][1]*20+10 and mouse[1] < sub_stars[2][1]*20+10:
                    go_pressed = True
                for scale in scale_list:
                    if bot.pyth(mouse, (scale[0], scale[1]+2*tri_size)) <= tri_size and scale[5] > 1:
                        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                            if scale[5] > 10:
                                scale[5] -= 10
                            else:
                                scale[5] -= scale[5] - 1
                        else: 
                            scale[5] -= 1
                    elif bot.pyth(mouse, (scale[0], scale[1]-2*tri_size)) <= tri_size and scale[5] < scale[2]:
                        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                            if scale[5] < scale[2] - 10:
                                scale[5] += 10
                            else:
                                scale[5] += scale[2] - scale[5]
                        else:
                            scale[5] += 1
                
            if event.type == pygame.MOUSEBUTTONUP:
                if mouse[0] > sub_stars[0][0]*20+10 and mouse[0] < sub_stars[1][0]*20+10 and mouse[1] > sub_stars[1][1]*20+10 and mouse[1] < sub_stars[2][1]*20+10:
                    go_pressed = False
                    running = False
                if mouse[0] >= 0 and mouse[0] <= 100 and mouse[1] >= 730 and mouse[1] <= 760:
                    play_game()
        
        pygame.display.flip()
    
    x = False
    game_data = []
    for data in ("stars", "rounds", "movespr", "secondspr", "botsplayers", "difficulty", "gamemode"):
        x = False
        for scale in scale_list:
            if scale[4] == data:
                game_data.append(scale[5])
                x = True
        if x == False:
            game_data.append(None)
            
    #stars, rounds, movespr, secondspr, botsplayers, difficulty, gamemode
    return(game_data)


def run_bot(stars, un_stars, adjacency_matrix, control_list, multiplier_list, multimove, color_num):
    
    availiable_moves = []
    past_moves = [[]]
    for star in stars:
        if star[2] == 0:
            availiable_moves.append(star.copy())
        if star[2] == color_num:
            past_moves[0].append(star.copy())

    for move in past_moves[0]:
        move[2] = 0
        
    past_moves[0].append(0)

    opt_moves = bot.run_bot(past_moves, availiable_moves, control_list, multiplier_list, un_stars, adjacency_matrix)
    
    for i in range(multimove):
        for star in stars:
            try:
                if star == opt_moves[len(past_moves[0]) - 1 + i]:
                    star[2] = color_num
            except:
                pass




def run_turn(current_round, stars, adjacency_matrix, time_per_round, multimove, color_num):

    running = True
    moves = multimove
    movesleft = True
    start = time.time()
    elapsed = 0
    
    while running and elapsed < time_per_round:
        screen.fill((0, 0, 0))

        mouse = pygame.mouse.get_pos()
        font = pygame.font.SysFont(None, 36)
        pygame.draw.rect(screen, home, pygame.Rect(0, 710, 100, 30))

        if mouse[0] >= 0 and mouse[0] <= 100 and mouse[1] >= 710 and mouse[1] <= 760:
            pygame.draw.rect(screen, home, pygame.Rect(0, 705, 105, 35))

        text = font.render(("EXIT"), True, (0,0,0))
        screen.blit(text,(20,715))
        
        
        elapsed = time.time() - start # to avoid division by 0
        
        pygame.draw.rect(screen, home, pygame.Rect(0, 740, 1440*((time_per_round - elapsed)/time_per_round), 20))
        font = pygame.font.SysFont(None, 36)
        text = font.render(("Round " + str(current_round)), True, (white))
        screen.blit(text,(10,10))    
        
        all_score = render_score(render_conns(stars, adjacency_matrix))
        button_list = render_stars(stars)

        if movesleft == False:
            font = pygame.font.SysFont(None, 72)
            text = font.render(("No Moves Left."), True, (enemy))
            screen.blit(text,(screen_dimensions[0]/2 - 160, screen_dimensions[1] - 70)) 
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if click_check(event, button_list, stars, moves, color_num) == True:
                if moves <= 0:
                    movesleft = False
                moves -= 1
            if event.type == pygame.MOUSEBUTTONUP:
                if mouse[0] >= 0 and mouse[0] <= 100 and mouse[1] >= 710 and mouse[1] <= 760:
                    play_game()
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                sys.exit()
                running = False
    return all_score


def run_untimed_turn(current_round, stars, adjacency_matrix, time_per_round, multimove, color_num, single_player = False):

    running = True
    moves = multimove
    movesleft = True
    
    while running:
        
        screen.fill((0, 0, 0))

        mouse = pygame.mouse.get_pos()
        font = pygame.font.SysFont(None, 36)

        if not single_player:
            pygame.draw.rect(screen, home, pygame.Rect(0, 710, 100, 30))
            if mouse[0] >= 0 and mouse[0] <= 100 and mouse[1] >= 710 and mouse[1] <= 760:
                pygame.draw.rect(screen, home, pygame.Rect(0, 705, 105, 35))
    
            text = font.render(("EXIT"), True, (0,0,0))
            screen.blit(text,(20,715))
            
            pygame.draw.rect(screen, frienemy_colors[color_num - 1], pygame.Rect(0, 740, 1440, 20))  
            
        else:
            font = pygame.font.SysFont(None, 36)
            pygame.draw.rect(screen, home, pygame.Rect(0, 730, 100, 30))
    
            if mouse[0] >= 0 and mouse[0] <= 100 and mouse[1] >= 730 and mouse[1] <= 760:
                pygame.draw.rect(screen, home, pygame.Rect(0, 725, 105, 35))
    
            text = font.render(("EXIT"), True, (0,0,0))
            screen.blit(text,(20,735))
        
        all_score = render_score(render_conns(stars, adjacency_matrix))
        button_list = render_stars(stars)
        text = font.render(("Round " + str(current_round)), True, (white))
        screen.blit(text,(10,10))  

        if movesleft == False:
            font = pygame.font.SysFont(None, 72)
            text = font.render(("No Moves Left."), True, (enemy))
            screen.blit(text,(screen_dimensions[0]/2 - 160, screen_dimensions[1] - 70)) 
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if click_check(event, button_list, stars, moves, color_num) == True:
                if moves <= 0:
                    movesleft = False
                moves -= 1
            if event.type == pygame.MOUSEBUTTONUP:
                if single_player:
                    if mouse[0] >= 0 and mouse[0] <= 100 and mouse[1] >= 730 and mouse[1] <= 760:
                        play_game()
                else:
                    if mouse[0] >= 0 and mouse[0] <= 100 and mouse[1] >= 710 and mouse[1] <= 760:
                        play_game()
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                sys.exit()
                running = False
        
        if moves <= 0:
            running = False
    return all_score


def ending_sequence(total_score):
    pygame.display.flip()
    running = True
    while running:
        screen.fill((0, 0, 0))
        
        font = pygame.font.SysFont(None, 100)
        text = font.render(("Game Over."), True, (white))
        screen.blit(text,(screen_dimensions[0]/2 - 200, screen_dimensions[1]/2 - 200))  
        
        font2 = pygame.font.SysFont(None, 50)
        
        mouse = pygame.mouse.get_pos()
        
        font3 = pygame.font.SysFont(None, 70)
        pygame.draw.rect(screen, home, pygame.Rect(540, 550, 350, 70))

        if mouse[0] >= 540 and mouse[0] <= 890 and mouse[1] >= 550 and mouse[1] <= 620:
            pygame.draw.rect(screen, home, pygame.Rect(530, 545, 370, 80))

        text = font3.render(("NEW GAME"), True, (0,0,0))
        screen.blit(text,(570,565))
        
        num_players = 0
        for scor in total_score:
            if scor[1] != 0:
                text = font2.render((scor[0]+" score:  "+str(scor[1])), True, (white))
                screen.blit(text,(screen_dimensions[0]/2 - 170, screen_dimensions[1]/2 - 100 + 50*num_players))  
                num_players += 1

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                if mouse[0] >= 540 and mouse[0] <= 890 and mouse[1] >= 550 and mouse[1] <= 620:
                    play_game()
            if event.type == pygame.QUIT:
                running = False
    pygame.display.quit()
    pygame.quit()
    sys.exit()
    
    
def name_sequence():
    import pygame
    running = True
    name_stars = [[20.5,15,0,0],[48, 15,0,0], [48,20,0,0],[20.5,20,0,0]]
    name_matrix = [[1,1,0,1],[1,1,1,0],[0,1,1,1],[1,0,1,1]]

    base_font = pygame.font.SysFont("applesymbols", 75)
    title_font = pygame.font.SysFont('applesymbols', 100)
    font = pygame.font.SysFont(None, 36)
    user_text = ''

    input_rect = pygame.Rect(20.5*20+10, 15*20+10, 27.5*20, 5*20)
      
    color_active = (0,0,0)
      
    while running:
        screen.fill((0, 0, 0))
        
        mouse = pygame.mouse.get_pos()
        pygame.draw.rect(screen, home, pygame.Rect(0, 730, 100, 30))
        pygame.draw.rect(screen, frienemy_colors[1], pygame.Rect(1340, 730, 100, 30))
        
        if mouse[0] >= 0 and mouse[0] <= 100 and mouse[1] >= 730 and mouse[1] <= 760:
            pygame.draw.rect(screen, home, pygame.Rect(0, 725, 105, 35))
        if mouse[0] >= 1340 and mouse[0] <= 1440 and mouse[1] >= 730 and mouse[1] <= 760:
            pygame.draw.rect(screen, frienemy_colors[1], pygame.Rect(1335, 725, 105, 35))
        
        text = font.render(("CANCEL"), True, (0,0,0))
        screen.blit(text,(0,735))
        text2 = font.render(("SAVE"), True, (0,0,0))
        screen.blit(text2,(1355, 735))
        title_text = title_font.render(("Save Map As: "), True, white)
        screen.blit(title_text, (450, 200))
        
        pygame.draw.rect(screen, color_active, input_rect)
      
        text_surface = base_font.render(user_text, True, white)

        screen.blit(text_surface, (input_rect.x+20, input_rect.y+20))
          
        input_rect.w = max(27.5*20, text_surface.get_width()+10)
        
        render_stars(name_stars)
        render_conns(name_stars, name_matrix)
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                sys.exit()
                running = False
      
            if event.type == pygame.MOUSEBUTTONUP:
                
                if mouse[0] >= 0 and mouse[0] <= 100 and mouse[1] >= 730 and mouse[1] <= 760:
                    save = False
                    running = False
                elif mouse[0] >= 1340 and mouse[0] <= 1440 and mouse[1] >= 730 and mouse[1] <= 760:
                    save = True
                    running = False
      
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    if text_surface.get_width() < 25*20:
                        user_text += event.unicode
        
        pygame.display.flip()
        
    return (user_text, save)
    

def user_map(map_data):
    if map_data == "create":
        stars = []
        adj_matrix = []
        running = True
    elif map_data[0] == "edit":
        stars = map_data[1]
        adj_matrix = map_data[2]
        running = True

    finish = False
    down_pressed = False
    start_corner = (0,0)
    user_text = None
    
    while running:
        star_in_box = False
        screen.fill((0, 0, 0))
        mouse = pygame.mouse.get_pos()
        
        mouse_coords = (round((mouse[0]-10)/20), round((mouse[1]-10)/20))
        
        if down_pressed == True:
            pygame.draw.polygon(screen, dddwhite, ((start_corner[0], start_corner[1]), (start_corner[0], mouse[1]), (mouse[0], mouse[1]), (mouse[0], start_corner[1])))
        else:
            render_stars([[mouse_coords[0], mouse_coords[1],0 ,0]], ddwhite)
        
        render_conns(stars, adj_matrix)
        render_stars(stars)
        
                
        pygame.draw.rect(screen, home, pygame.Rect(0, 730, 100, 30))
        pygame.draw.rect(screen, frienemy_colors[1], pygame.Rect(1340, 730, 100, 30))
        
        if mouse[0] >= 0 and mouse[0] <= 100 and mouse[1] >= 730 and mouse[1] <= 760:
            pygame.draw.rect(screen, home, pygame.Rect(0, 725, 105, 35))
        if mouse[0] >= 1340 and mouse[0] <= 1440 and mouse[1] >= 730 and mouse[1] <= 760:
            pygame.draw.rect(screen, frienemy_colors[1], pygame.Rect(1335, 725, 105, 35))
        
        font = pygame.font.SysFont(None, 36)
        text = font.render(("CANCEL"), True, (0,0,0))
        screen.blit(text,(0,735))
        text2 = font.render(("SAVE"), True, (0,0,0))
        screen.blit(text2,(1355, 735))
        
        keys = pygame.key.get_pressed()
            
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                start_corner = mouse
                down_pressed = True
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                for indx, starr in enumerate(stars):
                    if mouse_coords[0] == starr[0] and mouse_coords[1] == starr[1]:
                        del stars[indx]
                        del adj_matrix[indx]
                        for i in adj_matrix:
                            del i[indx]
            
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                for star in stars:
                    if ((round((start_corner[0]-10)/20) <= star[0] <= round((mouse[0]-10)/20)) or (round((start_corner[0]-10)/20) >= star[0] >= round((mouse[0]-10)/20))) and ((round((start_corner[1]-10)/20) <= star[1] <= round((mouse[1]-10)/20)) or (round((start_corner[1]-10)/20) >= star[1] >= round((mouse[1]-10)/20))) and (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]):
                        star_in_box = True
                        for indx, starr in enumerate(stars):
                            if starr == star:
                                star1 = indx
                            if starr[3] == 10000:
                                star2 = indx
                        adj_matrix[star1][star2] = 1
                        adj_matrix[star2][star1] = 1
                down_pressed = False
                
                if mouse[0] >= 0 and mouse[0] <= 100 and mouse[1] >= 730 and mouse[1] <= 760:
                    finish = False
                    running = False
                elif mouse[0] >= 1340 and mouse[0] <= 1440 and mouse[1] >= 730 and mouse[1] <= 760:
                    if map_data[0] == "edit":
                        finish = True
                        user_text = None
                        running = False
                    else:
                        name_data = name_sequence()
                        finish = name_data[1]
                        user_text = name_data[0]
                        if finish:
                            running = False
                                    
                elif keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                    if [mouse_coords[0], mouse_coords[1], 0,0] in stars:
                        for indx, star in enumerate(stars):
                            if star == [mouse_coords[0], mouse_coords[1], 0,0]:
                                star1 = indx
                            elif star[3] == 10000:
                                star2 = indx
                        adj_matrix[star1][star2] = 1
                        adj_matrix[star2][star1] = 1
                    
                    elif star_in_box == False:
                        try:
                            stars.append([mouse_coords[0], mouse_coords[1], 0,10000])
                            for starconns in adj_matrix:
                                starconns.append(0)
                            adj_matrix.append([0 for i in adj_matrix])
                            adj_matrix[-1].append(1)
                            for indx, starr in enumerate(stars):
                                if starr[3] == 10000:
                                    star1 = indx
                            for indx, starr in enumerate(stars):
                                if starr[3] == 10000 and indx != star1:
                                    star2 = indx
                            adj_matrix[star1][star2] = 1
                            adj_matrix[star2][star1] = 1
                                    
                            for star in stars:
                                star[3] = 0
                            stars[-1][3] = 10000
                        except:
                            for i in stars:
                                i[3] = 0
                            if [mouse_coords[0], mouse_coords[1], 0,0] in stars:
                                for i in stars:
                                    if i == [mouse_coords[0], mouse_coords[1], 0,0]:
                                        i[3] = 10000
                            else:
                                stars.append([mouse_coords[0], mouse_coords[1], 0,10000])
                                for starconns in adj_matrix:
                                    starconns.append(0)
                                adj_matrix.append([0 for i in adj_matrix])
                                adj_matrix[-1].append(1)
                        
                else: 
                    for i in stars:
                        i[3] = 0
                    if [mouse_coords[0], mouse_coords[1], 0,0] in stars:
                        for i in stars:
                            if i == [mouse_coords[0], mouse_coords[1], 0,0]:
                                i[3] = 10000
                    else:
                        stars.append([mouse_coords[0], mouse_coords[1], 0,10000])
                        for starconns in adj_matrix:
                            starconns.append(0)
                        adj_matrix.append([0 for i in adj_matrix])
                        adj_matrix[-1].append(1)
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                sys.exit()
                running = False
        pygame.display.flip()

    for i in stars:
        i[3] = 0
    return (stars, adj_matrix, user_text, finish)




def choose_map(edit):
    pygame.display.flip()
    running = True
    pressed = False
    selected = None
    outside = True
    
    if edit:
        sub_stars = [[20, 6, 0, 0], [51, 6, 0, 0], [20, 38, 0, 0], [51, 38, 0, 0], [68, 8, 0, 0], [3, 8, 0, 0], [16, 8, 0, 0], [16, 17, 0, 0], [3, 17, 0, 0], [68, 17, 0, 0], [55, 8, 0, 0], [55, 17, 0, 0], [3, 20, 0, 0], [16, 20, 0, 0], [3, 29, 0, 0], [16, 29, 0, 0], [55, 20, 0, 0], [68, 20, 0, 0], [55, 29, 0, 0], [68, 29, 0, 0]]
        sub_matrix = [[1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1]]

    else:
        sub_stars = [[20, 6, 0, 0], [51, 6, 0, 0], [20, 38, 0, 0], [51, 38, 0, 0], [68, 8, 0, 0], [3, 8, 0, 0], [16, 8, 0, 0], [16, 17, 0, 0], [3, 17, 0, 0], [68, 17, 0, 0], [55, 8, 0, 0], [55, 17, 0, 0]]
        sub_matrix = [[1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0], [0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1], [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1]]


    base_font = pygame.font.SysFont("applesymbols", 75)
    title_font = pygame.font.SysFont('applesymbols', 100)
    


    map_list = open("map_list", "r")
    maps = map_list.readlines()
    map_list.close()

    for indx, value in enumerate(maps):
        maps[indx] = value.strip()
    

    while running:
        screen.fill((0, 0, 0))
        mouse = pygame.mouse.get_pos()
        
        font = pygame.font.SysFont(None, 36)
        pygame.draw.rect(screen, home, pygame.Rect(0, 730, 100, 30))

        if mouse[0] >= 0 and mouse[0] <= 100 and mouse[1] >= 730 and mouse[1] <= 760:
            pygame.draw.rect(screen, home, pygame.Rect(0, 725, 105, 35))

        text = font.render(("EXIT"), True, (0,0,0))
        screen.blit(text,(20,735))
        
        
        for indx, mapp in enumerate(maps):
            if mouse[0] > sub_stars[0][0]*20+10 and mouse[0] < sub_stars[1][0]*20+10 and mouse[1] > 130+(indx)*80 and mouse[1] < 130+(1+indx)*80:
                width = abs((sub_stars[0][0]*20+10) - (sub_stars[1][0]*20+10))
                height = abs((indx)*80 - (1+indx)*80)
                if pressed == True:
                    pygame.draw.rect(screen, yayaya, (sub_stars[0][0]*20+10, 130+(indx)*80, width, height))
                else:
                    pygame.draw.rect(screen, dwhite, (sub_stars[0][0]*20+10, 130+(indx)*80, width, height))
            if selected == indx:
                pygame.draw.rect(screen, yayaya, (sub_stars[0][0]*20+10, 130+(indx)*80, width, height))
        
        
        if mouse[0] > 55*20+10 and mouse[0] < 68*20+10 and mouse[1] > 8*20+10 and mouse[1] < 17*20+10:
            if pressed == True:
                pygame.draw.rect(screen, frienemy_colors[1], (55*20+10, 8*20+10, (68*20+10) - (55*20+10), (17*20+10) - (8*20+10)))
            else:
                pygame.draw.rect(screen, dd_green, (55*20+10, 8*20+10, (68*20+10) - (55*20+10), (17*20+10) - (8*20+10)))
                
        if mouse[0] > 3*20+10 and mouse[0] < 16*20+10 and mouse[1] > 8*20+10 and mouse[1] < 17*20+10:
            if pressed == True:
                pygame.draw.rect(screen, home, (3*20+10, 8*20+10, (16*20+10) - (3*20+10), (17*20+10) - (8*20+10)))
            else:
                pygame.draw.rect(screen, dd_blue, (3*20+10, 8*20+10, (16*20+10) - (3*20+10), (17*20+10) - (8*20+10)))

        if edit:
            if mouse[0] > 55*20+10 and mouse[0] < 68*20+10 and mouse[1] > 20*20+10 and mouse[1] < 29*20+10:
                if pressed == True:
                    pygame.draw.rect(screen, yellow, (55*20+10, 20*20+10, (68*20+10) - (55*20+10), (17*20+10) - (8*20+10)))
                else:
                    pygame.draw.rect(screen, dd_yellow, (55*20+10, 20*20+10, (68*20+10) - (55*20+10), (17*20+10) - (8*20+10)))
                    
            if mouse[0] > 3*20+10 and mouse[0] < 16*20+10 and mouse[1] > 20*20+10 and mouse[1] < 29*20+10:
                if pressed == True:
                    pygame.draw.rect(screen, red, (3*20+10, 20*20+10, (16*20+10) - (3*20+10), (17*20+10) - (8*20+10)))
                else:
                    pygame.draw.rect(screen, dd_red, (3*20+10, 20*20+10, (16*20+10) - (3*20+10), (17*20+10) - (8*20+10)))

        
        render_conns(sub_stars, sub_matrix)
        render_stars(sub_stars)
        
        title_text = title_font.render(("Choose a Map:"), True, (white))
        screen.blit(title_text, (450, 20))
        map_text = base_font.render("Create", True, white)
        screen.blit(map_text, (110, 195))
        map_text = base_font.render("New Map", True, white)
        screen.blit(map_text, (85, 265))
        
        if edit:
            rand_text = base_font.render("Edit", True, white)
            screen.blit(rand_text, (1190, 195))
            rand_text = base_font.render("Map", True, white)
            screen.blit(rand_text, (1190, 270))
            
            
            map_text = base_font.render("Delete", True, white)
            screen.blit(map_text, (115, 430))
            map_text = base_font.render("Map", True, white)
            screen.blit(map_text, (145, 500))
            
            rand_text = base_font.render("Copy", True, white)
            screen.blit(rand_text, (1175, 430))
            rand_text = base_font.render("Map", True, white)
            screen.blit(rand_text, (1185, 505))
            
            
            
        else:
            rand_text = base_font.render("Randomly", True, white)
            screen.blit(rand_text, (1120, 195))
            rand_text = base_font.render("Generate", True, white)
            screen.blit(rand_text, (1125, 270))
        
        for indx, mapp in enumerate(maps):
            text = base_font.render(mapp, True, white)
            screen.blit(text, (715 - 55*((len(mapp)/2) - 0.25*len(mapp)),140+80*indx))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                sys.exit()
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pressed = True

            if event.type == pygame.MOUSEBUTTONUP:
                pressed = False
                outside = True
                if mouse[0] >= 0 and mouse[0] <= 100 and mouse[1] >= 730 and mouse[1] <= 760:
                    play_game()
                
                if edit:
                    for indx, mapp in enumerate(maps):
                        if mouse[0] > sub_stars[0][0]*20+10 and mouse[0] < sub_stars[1][0]*20+10 and mouse[1] > 130+(indx)*80 and mouse[1] < 130+(1+indx)*80:
                            selected = indx
                            outside = False
                    
                else:
                    for indx, mapp in enumerate(maps):
                        if mouse[0] > sub_stars[0][0]*20+10 and mouse[0] < sub_stars[1][0]*20+10 and mouse[1] > 130+(indx)*80 and mouse[1] < 130+(1+indx)*80:
                            x = open(mapp, "r")
                            info = x.readlines()
                            x.close()
                            adj_matrix = json.loads(info[-1])
                            stars = json.loads(info[-2])
                            return(stars, adj_matrix)
                    
                    
                if mouse[0] > 55*20+10 and mouse[0] < 68*20+10 and mouse[1] > 8*20+10 and mouse[1] < 17*20+10:
                    if edit:
                        if selected != None:
                            x = open(maps[selected], "r")
                            info = x.readlines()
                            x.close()
                            adj_matrix = json.loads(info[-1])
                            stars = json.loads(info[-2])
                            return("edit", stars, adj_matrix, maps[selected])
                    else:
                        return("random")
                elif mouse[0] > 3*20+10 and mouse[0] < 16*20+10 and mouse[1] > 8*20+10 and mouse[1] < 17*20+10:
                    return("create")
                if edit:
                    if mouse[0] > 55*20+10 and mouse[0] < 68*20+10 and mouse[1] > 20*20+10 and mouse[1] < 29*20+10:
                        if selected != None:
                            x = open(maps[selected], "r")
                            info = x.readlines()
                            x.close()
                            adj_matrix = json.loads(info[-1])
                            stars = json.loads(info[-2])
                            return("copy", stars, adj_matrix)

                    
                    elif mouse[0] > 3*20+10 and mouse[0] < 16*20+10 and mouse[1] > 20*20+10 and mouse[1] < 29*20+10:
                        if selected != None:
                            return("delete", selected)
            if outside == True:
                selected = None
        #If edit, returns (action, stars, adj_matrix) or (action) or ("delete", mapname)
        #Else, either just returns (action) or (stars, adj_matrix)
        pygame.display.flip()



def play_game():
    pygame.display.set_caption('Constellation')
    
    file1 = open("map_list", "a")
    file1.close()
    
    current_round = 0
    gamemode = opening_sequence(opening_sequence_stars, opening_sequence_matrix)
    def asdf():
            map_data = choose_map(True)
            if map_data[0] == "delete":
                my_file = open("map_list")
                string_list = my_file.readlines()
                my_file.close()
                del string_list[map_data[1]]
                my_file = open("map_list", "w")
                new_file_contents = "".join(string_list)
                my_file.write(new_file_contents)
                my_file.close()
                asdf()
            elif map_data[0] == "copy":
                user_text = name_sequence()
                data = (map_data[1], map_data[2], user_text[0])
                new_file = open(data[2], "w+")
                map_list = open("map_list", "a+")
                new_file.write(str(data[0]) + "\n")
                new_file.write(str(data[1]) + "\n")
                map_list.write(data[2] + "\n")
                new_file.close()
                map_list.close()
                asdf()
            else:
                data = user_map(map_data)
                if data[3]:
                    if map_data[0] == "edit":
                        new_file = open(map_data[3], "w+")
                        new_file.write(str(data[0]) + "\n")
                        new_file.write(str(data[1]) + "\n")
                        new_file.close()
                    else:
                        new_file = open(data[2], "w+")
                        map_list = open("map_list", "a+")
                        new_file.write(str(data[0]) + "\n")
                        new_file.write(str(data[1]) + "\n")
                        map_list.write(data[2] + "\n")
                        new_file.close()
                        map_list.close()
                asdf()
    if gamemode == 4:
        asdf()

    else: 
        map_data = choose_map(False)
        if map_data == "random":
            game_data = sub_opening_sequence(gamemode)
            ###########
            rounds = game_data[1]
    
            coord_range = (71,37)
            #the area in which new random stars are placed
            new_star_count = game_data[0]
            #the number of new stars created and connected
            try:
                weight_dist = (round(game_data[0]/4),1)
            except:
                pass
            #probability of having no connection vs a connection (0 vs 1). Weights from 0-1. 

            stars = gen.star_gen(new_star_count, coord_range)
            un_stars = stars.copy()
            #stars are in a 72 by 38 grid - starting from top left, right is x, down is y
            #coordinates of each star. 0 = empty, 1 = occupied, 2 = enemy. 
            
            adjacency_matrix = gen.matrix_gen(new_star_count, weight_dist)
            #defines which stars are connected. shallow = which star it applies to, deep = which stars are connected to that star. 
            
            try:
                control_list = difficulties[game_data[5]][0]
                multiplier_list = difficulties[game_data[5]][1]
            except:
                pass
        
            time_per_round = game_data[3]
            multimove = game_data[2] #has to be less than length of control_list
            botsplayers = game_data[4]
            ############
        elif map_data == "create":
            data = user_map(map_data)
            if data[3]:
                new_file = open(data[2], "w+")
                map_list = open("map_list", "a+")
                new_file.write(str(data[0]) + "\n")
                new_file.write(str(data[1]) + "\n")
                map_list.write(data[2] + "\n")
                new_file.close()
                map_list.close()
            play_game()
        else:
            game_data = sub_opening_sequence(gamemode, True)
            ###########
            rounds = game_data[1]
            
            stars = map_data[0]
            
            for indx, star in enumerate(stars):
                star[3] = indx
            
            un_stars = stars.copy()
            adjacency_matrix = map_data[1]
            try:
                control_list = difficulties[game_data[5]][0]
                multiplier_list = difficulties[game_data[5]][1]
            except:
                pass
            
            time_per_round = game_data[3]
            multimove = game_data[2] #has to be less than length of control_list
            botsplayers = game_data[4]
            ############
        
        if gamemode == 1:
            for turn in range(rounds):
                current_round += 1
                total_score = run_untimed_turn(current_round, stars, adjacency_matrix, time_per_round, multimove, 1, True)
                
        elif gamemode == 2:
            
            for turn in range(rounds):
                current_round += 1
                total_score = run_turn(current_round, stars, adjacency_matrix, time_per_round, multimove, 1)
                for bots in range(botsplayers):
                    
                    run_bot(stars, un_stars, adjacency_matrix, control_list, multiplier_list, multimove, bots+5)

        elif gamemode == 3:
            
            for turn in range(rounds):
                current_round += 1
                for player in range(botsplayers + 1):
                    total_score = run_untimed_turn(current_round, stars, adjacency_matrix, time_per_round, multimove, player+1)
            
        ending_sequence(total_score)

    play_game()


play_game()








