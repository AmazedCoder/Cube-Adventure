# Importing the pygame module
import pygame
from pygame.locals import *
from pygame import mixer

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

width, height = 60, 60
x_offset, y_offset = (width / 2), (height / 2)

x_speed = 0
gravity = 0

jump_height = 20
friction = 0.875

level1 = [(0, 630, 200, 90), (200, 500, 150, 50), (500, 400, 150, 50), (800, 300, 150, 50), (1100, 200, 150, 50)] # (x_pos, y_pos, width, height)
level2 = [(1100, 300, 150, 50), (500, 180, 450, 50), (500, 400, 250, 50)]
level3 = [(500, 600, 250, 50), (500, 210, 250, 50)]
level4 = [(500, 210, 250, 50), (500, 610, 250, 50), (100, 410, 250, 50), (900, 410, 250, 50)]
level5 = [(500, 610, 250, 50), (1100, 200, 150, 50)]
level6 = [(390, 190, 250, 50), (640, 90, 25, 150)]
level7 = [(390, 190, 400, 50), (780, -50, 50, 290), (390, 190, 50, 110), (390, 490, 50, 450), (830, 190, 50, 110), (830, 540, 50, 450), (780, 190, 200, 50), (880, 590, 180, 50)]
level8 = [(620, 190, 460, 50), (780, -50, 50, 290), (920, 190, 50, 160), (920, 540, 50, 450), (250, -50, 50, 290)]
level9 = [(250, -50, 50, 390), (140, 290, 110, 50), (300, 240, 110, 50)]
level10 = [(300, 240, 110, 50), (410, 240, 450, 50), (700, -50, 50, 340)]
level11 = [(0, 630, 1280, 90)]

vertical_levels = [[], [], [[100, 600, 250, 50], [900, 600, 250, 50]], [], [], [[1100, 610, 150, 50], [400, 850, 150, 50], [50, 750, 200, 50]], [[570, 800, 150, 50], [1060, 590, 180, 50]], [[770, 850, 150, 50], [470, 660, 150, 50], [25, 660, 150, 50]], [[300, 1000, 150, 50]], [[400, 1000, 75, 50], [1100, 700, 50, 50]], []]
vertical_level_y_origin = [[], [], [[600, 0], [600, 0]], [], [], [[610, 0], [850, 0], [750, 0]], [[800, 0], [590, 0]], [[850, 0], [660, 0], [660, 0]], [[1000, 0]], [[1000, 0], [700, 0]], []] # y_pos, (0 or 1) direction

dropped_levels = [[], [], [], [], [[100, 450, 250, 50], [500, 310, 250, 50], [900, 200, 200, 50]], [[750, 310, 150, 50]], [[130, 375, 150, 50]], [[1080, 190, 200, 50], [300, 190, 130, 50]], [[0, 290, 140, 50], [700, 600, 150, 50], [1000, 550, 150, 50], [1220, 400, 60, 50], [1000, 250, 150, 50], [700, 100, 150, 50]], [[60, 375, 110, 50], [800, 700, 50, 50]], []]
dropped_levels_y_origin = [[], [], [], [], [[450, 0, 0], [310, 0, 0], [200, 0, 0]], [[310, 0, 0]], [[375, 0, 0]], [[190, 0, 0], [190, 0, 0]], [[290, 0, 0], [600, 0, 0], [550, 0, 0], [400, 0, 0], [250, 0, 0], [100, 0, 0]], [[375, 0, 0], [700, 0, 0]], []] # y_pos, (0 or 1) drop?, gravity

lava = [[], [], [], [], [], [], [(390, 300, 50, 25), (390, 465, 50, 25), (830, 300, 50, 25), (830, 515, 50, 25)], [(920, 350, 50, 25), (920, 515, 50, 25), (630, 240, 50, 110), (630, 540, 50, 450)], [], [(300, 290, 50, 35), (300, 540, 50, 450)], []]

font = pygame.font.Font('Assets/font.ttf', 60)
win_font = pygame.font.Font("Assets/font.ttf", 90)

# print(pygame.font.get_fonts())
# font = pygame.font.SysFont("comicsans", 40)

levels = [level1, level2, level3, level4, level5, level6, level7, level8, level9, level10, level11]

level_goals = [(1140, 90, 70, 110), (640, 290, 70, 110), (590, 100, 70, 110), (590, 500, 70, 110), (1140, 90, 70, 110), (490, 80, 70, 110), (860, 80, 70, 110), (100, 100, 150, 70), (300, 130, 70, 110), (750, 130, 70, 110), (9999, 9999, 1, 1)]

spawn_points = [(50, 500), (1140, 240), (590, 540), (590, 150), (590, 550), (1140, 200), (480, 130), (890, 130), (150, 0), (340, 0), (640, 500)]

current_lvl_id = 0
current_level = levels[current_lvl_id]

x_pos = spawn_points[current_lvl_id][0]
y_pos = spawn_points[current_lvl_id][1]

x_dir = 1

texts = ["Hello! Welcome to my platformer! Get to the green rectangle.", "Good job! This is a bit of a tricky one. I hope you can do it!", "Be careful! The platforms move up and down.", "Oops! Sorry, I messed up the controls (trust me, it's an accident)", "OK, now the platforms fall. I definitely didn't do that.", "This is going to be tricky! Don't mess up!", "Another tricky one. Let's see your skills!", "Just do it!", "Good luck!", "Last level. You can do it! (hopefully)", "Congratulations! You won!"]

mixer.init()
mixer.music.load('Audio/bg.ogg')
mixer.music.play(-1)

pygame.display.set_caption("Cube Adventure")
icon = pygame.image.load("Assets/icon.png")
pygame.display.set_icon(icon)

cup = pygame.image.load("Assets/cup.png")

win_played = 0

while running:
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    if current_lvl_id == 10 and win_played == 0:
        win_played = 1
        
        mixer.music.load("Audio/win.ogg")
        mixer.music.play() 

    screen.fill("white")
    gravity -= 1
    
    if current_lvl_id == 3:
        x_dir = -1
    else:
        x_dir = 1
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        x_speed += 1 * x_dir
    if keys[pygame.K_LEFT]:
        x_speed -= 1 * x_dir
    if keys[pygame.K_p]:
        print("{}, {}".format(x_pos, y_pos))
    
    x_speed *= friction
    x_pos += x_speed 
    
    # normal platforms
    for level in current_level:
        collide = pygame.Rect.colliderect(Rect(x_pos, y_pos, width, height), Rect(level))
        if collide:
            while collide:
                x_pos += (abs(x_speed) / x_speed * -1)
                collide = pygame.Rect.colliderect(Rect(x_pos, y_pos, width, height), Rect(level))
            x_speed = 0
    
    for level in dropped_levels[current_lvl_id]:
        collide = pygame.Rect.colliderect(Rect(x_pos, y_pos, width, height), Rect(level))
        if collide:
            while collide:
                x_pos += (abs(x_speed) / x_speed * -1)
                collide = pygame.Rect.colliderect(Rect(x_pos, y_pos, width, height), Rect(level))
            x_speed = 0
            
    y_pos -= gravity
    for level in current_level:
        collide = pygame.Rect.colliderect(Rect(x_pos, y_pos, width, height), Rect(level))
        if collide:
            while collide:
                y_pos += (abs(gravity) / gravity)
                collide = pygame.Rect.colliderect(Rect(x_pos, y_pos, width, height), Rect(level))
            gravity = 0
            
    for level in dropped_levels[current_lvl_id]:
        collide = pygame.Rect.colliderect(Rect(x_pos, y_pos, width, height), Rect(level))
        if collide:
            dropped_levels_y_origin[current_lvl_id][dropped_levels[current_lvl_id].index(level)][1] = 1
            while collide:
                y_pos += (abs(gravity) / gravity)
                collide = pygame.Rect.colliderect(Rect(x_pos, y_pos, width, height), Rect(level))
            gravity = 0
            
    for level in vertical_levels[current_lvl_id]:
        collide = pygame.Rect.colliderect(Rect(x_pos, y_pos, width, height), Rect(level))
        if collide:
            if x_speed != 0:
                x_pos += (abs(x_speed) / x_speed * -1) * 10

            collide = pygame.Rect.colliderect(Rect(x_pos, y_pos, width, height), Rect(level))
            #print(collide)
            if collide:
                while collide:
                    if y_pos != 0:
                        y_pos -= (gravity / abs(gravity) * -1)
                        #print(gravity)
                    else:
                        y_pos -= 1
                    #print(str(y_pos) + " " + str(gravity))
                    collide = pygame.Rect.colliderect(Rect(x_pos, y_pos, width, height), Rect(level))
                gravity = 0
            
            if x_speed != 0:
                x_pos -= (abs(x_speed) / x_speed * -1) * 10
    
    # vertical platforms
    for level in vertical_levels[current_lvl_id]:
        collide = pygame.Rect.colliderect(Rect(x_pos, y_pos, width, height), Rect(level))
        if collide:
            while collide:
                x_pos += (abs(x_speed) / x_speed * -1)
                collide = pygame.Rect.colliderect(Rect(x_pos, y_pos, width, height), Rect(level))
            x_speed = 0
            
    for level in current_level:
        y_pos += 1
        collide = pygame.Rect.colliderect(Rect(x_pos, y_pos, width, height), Rect(level))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and collide:
            gravity = jump_height
        y_pos -= 1
    
    for level in vertical_levels[current_lvl_id]:
        y_pos += 1
        collide = pygame.Rect.colliderect(Rect(x_pos, y_pos, width, height), Rect(level))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and collide:
            gravity = jump_height
        y_pos -= 1
    
    for level in dropped_levels[current_lvl_id]:
        y_pos += 1
        collide = pygame.Rect.colliderect(Rect(x_pos, y_pos, width, height), Rect(level))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and collide:
            gravity = jump_height
        y_pos -= 1
        
    for level in current_level:
        pygame.draw.rect(screen, "black", pygame.Rect(level))
    
    for level in vertical_levels[current_lvl_id]:
        #print(level)
        #print(vertical_levels[current_lvl_id].index(level))
        
        y_origin = vertical_level_y_origin[current_lvl_id][vertical_levels[current_lvl_id].index(level)][0]
        
        
        if level[1] >= (y_origin - 400):
            if vertical_level_y_origin[current_lvl_id][vertical_levels[current_lvl_id].index(level)][1] == 1:
                if level[1] >= y_origin:
                    vertical_level_y_origin[current_lvl_id][vertical_levels[current_lvl_id].index(level)][1] = 0
            else:
                vertical_level_y_origin[current_lvl_id][vertical_levels[current_lvl_id].index(level)][1] = 0
        else:
            vertical_level_y_origin[current_lvl_id][vertical_levels[current_lvl_id].index(level)][1] = 1
        
        direction = vertical_level_y_origin[current_lvl_id][vertical_levels[current_lvl_id].index(level)][1]
        
        if direction == 0:
            level[1] -= 4
        elif direction == 1:
            level[1] += 4
        
        pygame.draw.rect(screen, "black", pygame.Rect(level))
    
    for level in dropped_levels[current_lvl_id]:
        
        if dropped_levels_y_origin[current_lvl_id][dropped_levels[current_lvl_id].index(level)][1] == 1:
            dropped_levels_y_origin[current_lvl_id][dropped_levels[current_lvl_id].index(level)][2] += 0.1
            level[1] += dropped_levels_y_origin[current_lvl_id][dropped_levels[current_lvl_id].index(level)][2]
            
        pygame.draw.rect(screen, "black", pygame.Rect(level))
       
    pygame.draw.rect(screen, "green", pygame.Rect(level_goals[current_lvl_id]))
    
    collide = pygame.Rect.colliderect(Rect(x_pos, y_pos, width, height), Rect(level_goals[current_lvl_id]))
    if collide:
        current_lvl_id += 1
        current_level = levels[current_lvl_id]

    for level in lava[current_lvl_id]:
        pygame.draw.rect(screen, "red", pygame.Rect(level))
        collide = pygame.Rect.colliderect(Rect(x_pos, y_pos, width, height), Rect(level))
        
        if collide:
            x_pos = spawn_points[current_lvl_id][0]
            y_pos = spawn_points[current_lvl_id][1]
            gravity = 0
            
            for level in dropped_levels[current_lvl_id]:
                level[1] = dropped_levels_y_origin[current_lvl_id][dropped_levels[current_lvl_id].index(level)][0]
                dropped_levels_y_origin[current_lvl_id][dropped_levels[current_lvl_id].index(level)][1] = 0
                dropped_levels_y_origin[current_lvl_id][dropped_levels[current_lvl_id].index(level)][2] = 0

    if y_pos > screen.get_height():
        x_pos = spawn_points[current_lvl_id][0]
        y_pos = spawn_points[current_lvl_id][1]
        gravity = 0
        
        for level in dropped_levels[current_lvl_id]:
            level[1] = dropped_levels_y_origin[current_lvl_id][dropped_levels[current_lvl_id].index(level)][0]
            dropped_levels_y_origin[current_lvl_id][dropped_levels[current_lvl_id].index(level)][1] = 0
            dropped_levels_y_origin[current_lvl_id][dropped_levels[current_lvl_id].index(level)][2] = 0
    
    pygame.draw.rect(screen, "red", pygame.Rect(x_pos, y_pos, width, height))
    
    if current_lvl_id == 10:
        text = win_font.render(texts[current_lvl_id], 1, (0, 0, 0))
        screen.blit(text, (280, 30))
        
        screen.blit(cup, (550, 150))
    else:
        text = font.render(texts[current_lvl_id], 1, (0, 0, 0))
        screen.blit(text, (10, 0))
    
    """text = STAT_FONT.render("Score: " + str(score), 1, (255, 255, 255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))
    """
                     
    # flip() the display to put your work on screen
    pygame.display.flip()
    
    #print("{}, {}".format(x_pos, y_pos))

    clock.tick(60)  # limits FPS to 60

pygame.quit()