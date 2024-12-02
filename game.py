"""
Name: Darren Su
Period: 2
Class Code: ICU3I
Assignment: Treasure hunting house game
something I forgot about
"""

#pygame init
import pygame as py
import os
import random

#init
py.init()
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" %(20, 20)
running = True

#Images
player = py.image.load('assets/Characters/walking_frames/tile000.png')
textbox_image = py.image.load('assets/textbox/textbox.png')

# Player Varibles
player_x = 200*0.45
player_y = 1100*0.45

#setup player
player_width = player.get_width() *2
player_height = player.get_height() *2
player =  py.transform.scale (player, (player_height, player_width))
move_rate = 10

#Colors
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREY = (200,200,200)

# movement key booleans
PRESS_RIGHT = False
PRESS_LEFT = False
PRESS_UP = False
PRESS_DOWN = False
START = True

#Time Track
clock = py.time.Clock()

#screen 
screen = py.display.set_mode((1000, 700))
screen.fill(WHITE)

#game clues

def clues (x):
    global clues
    global rooms

    rooms = ["Hallway", "Living Room", "Bedroom", "Bathroom", "Kitchen", "Dining Room"]
    room_numbers = ["first", "second", "third", "fourth", "fifth", "sixth"]

    next_room = rooms[x]
    room_number = room_numbers[x]
    
    output_clue = "The %s key to the %s is in the top left corner of the hallway" %(room_number, next_room)

    return output_clue


def factor_rect(rect):
    factor = 0.50
    width_factor = 0.5
    height_factor = 0.5
    x_move = 100
    y_move = 25

    #this scales the walls, as well as centers it
    return py.Rect(rect.x * factor + x_move, rect.y * factor - y_move, rect.width * width_factor, rect.height * height_factor)
     #ask if ok

def room():
    screen.fill(WHITE)

    global walls
    global doors
    global player_rect

    player_rect = py.Rect(player_x, player_y, player_width, player_height)

    walls = [
        #top wall
        py.Rect(100, 100, 900, 100),  

        #left-most wall
        py.Rect(100, 200, 100, 800), 

        #bottom-left door
        py.Rect(200, 900, 100, 100), 
        py.Rect(400, 900, 200, 100), 

        #hallway - bathroom wall
        py.Rect(500, 200, 100, 400), 

        #bedroom - dining room wall
        py.Rect(900, 200, 100, 800), 

        #living room - kitchen wall
        py.Rect(500, 900, 100, 500),  

        #bottom-most wall
        py.Rect(500, 1300, 500, 100),  

        #living room - kitchen wall, right side bottom
        py.Rect(900, 1100, 100, 200), 

        #kitchen wall bottom
        py.Rect(900, 1100, 600, 100), 

        #bedroom-living room wal
        py.Rect(500, 700, 600, 100),
        
        #bedroom-dinning top wall
        py.Rect(700, 300, 800, 100),

        #right-most wall
        py.Rect(1400, 300, 100, 900),

        #kitchen-dining room door
        py.Rect(1300, 700, 200, 100),
    ]

    doors = [
        #hallway
        py.Rect(300, 900, 100, 100),

        #hallway - livingroom door
        py.Rect(500, 800, 100, 100),
        
        #hallway - bedroom door
        py.Rect(500, 500, 100, 100),

        #bedroom - bathroom door
        py.Rect(600, 300, 100, 100),

        #living room - kitchen door
        py.Rect(900, 1000, 100, 100),

        #kitchen - dining room door
        py.Rect(1100, 700, 200, 100),

    ]

    for x in walls:
        rect = factor_rect(x)
        py.draw.rect(screen, BLACK, rect)

    screen.blit(player, player_rect)

    py.display.flip()

def textbox (text):
    print(text)
    text = str(text)
    textbox_rect = py.Rect(150, 400, 500, 100)
    screen.blit(textbox_image, textbox_rect)
    py.display.flip()

    font = py.font.Font(None, 36)
    x = 0
    x_spacing = 0
    while x < len(text):
        text_surface = font.render(text[x], True, GREY)
        screen.blit(text_surface, (200+ x_spacing, 500))

        py.display.flip()
        py.time.delay(50)

        x_spacing = x_spacing + text_surface.get_width()
        x = x + 1

        for e in py.event.get():
            if e.type == py.KEYDOWN:
                screen.blit(textbox_image, textbox_rect)
                text_surface = font.render(text, True, GREY)
                screen.blit(text_surface, (200, 500))
                x = len(text)
                py.display.flip()

    while True:
        for e in py.event.get():
            if e.type == py.KEYDOWN:
                return


while running == True:

    if START == True:
        textbox("hint: spacebar to move through textboxes")
        textbox("controls: arrow keys to move")
        textbox("You are trapped in a house, find the key to escape")
        START = False
    
    for e in py.event.get():
        if e.type == py.QUIT:
            running = False

        elif e.type == py.KEYDOWN:
            if e.key == py.K_RIGHT: 
                PRESS_RIGHT = True
            if e.key == py.K_LEFT: 
                PRESS_LEFT = True
            if e.key == py.K_UP: 
                PRESS_UP = True
            if e.key == py.K_DOWN: 
                PRESS_DOWN = True

        elif e.type == py.KEYUP:
            if e.key == py.K_RIGHT: 
                PRESS_RIGHT = False
            if e.key == py.K_LEFT: 
                PRESS_LEFT = False
            if e.key == py.K_UP: 
                PRESS_UP = False
            if e.key == py.K_DOWN: 
                PRESS_DOWN = False
    
    room()
    previous_x = player_x
    previous_y = player_y

    if PRESS_RIGHT == True: 
        player_x = player_x + move_rate
    if PRESS_LEFT == True: 
        player_x = player_x - move_rate
    if PRESS_UP == True: 
        player_y = player_y - move_rate
    if PRESS_DOWN == True: 
        player_y = player_y + move_rate

    player_rect = py.Rect(player_x, player_y, player_width, player_height)

    for x in walls:
        rect = factor_rect(x)
        if player_rect.colliderect(rect):
            player_x = previous_x
            player_y = previous_y
            break

    for x in doors:
        rect = factor_rect(x)
        if player_rect.colliderect(rect):
            textbox(case[x])
            break 
    
    py.display.flip()
    print(player_x, player_y)


    clock.tick(60)


