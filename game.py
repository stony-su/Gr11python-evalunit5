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
global running
running = True

#Images
player = py.image.load('assets/Characters/walking_frames/south_n1.png')
textbox_image = py.image.load('assets/textbox/textbox.png')
gui_image = py.image.load('assets/textbox/clues_box.png')

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
YELLOW = (255,255,0)
RED = (255,0,0)
GREEN = (0,128,0)
GREY = (200,200,200)

#movement booleans
global PRESS_RIGHT
global PRESS_DOWN
global PRESS_LEFT
global PRESS_UP
PRESS_RIGHT = False
PRESS_LEFT = False
PRESS_UP = False
PRESS_DOWN = False
START = True

#room booleans (for loops)
global room_remenber_once
room_remenber_once = [True, True, True, True, True, True]
y = 0
entered_doors = []

#clue variables
global clue_found
global clue_rect
global clue_number 
global clue_menu
global current_clue
clue_found = True 
clue_number = 0
clue_rect = None
clue_location_horziontal = "right"
clue_location_vertical = "top"
clue_menu = []
current_clue = None

#Score
number_of_clues_found = 0
score_file = open("score.1  ", "w")
score_file.write("Clues: " + "\n")

#Time Track
clock = py.time.Clock()

#screen 
screen = py.display.set_mode((1000, 700))
screen.fill(WHITE)

#Walking Animation
path = "assets/Characters/walking_frames/"

south_walk = [path+"south_n1.png", path + "south_walk1.png", path + "south_walk2.png", path + "south_n2.png"]

#clue generation function

def start_menu():

    return



def clues_place (y):
    #global clue_location_horziontal
    #global clue_location_vertical
    global clue_number

    rooms = ["Hallway", "Living Room", "Bedroom", "Bathroom", "Kitchen", "Dining Room", "Treasure"]
    room_numbers = ["first", "second", "third", "fourth", "fifth"  ]

    next_room = rooms[y+1]
    if next_room == "Treasure":
        win_condition = "You have found the treasure!"
        running = False
        return win_condition
    room_number = room_numbers[y]

    clue_location_horziontal = random.choice(["left", "right"])
    clue_location_vertical = random.choice(["top", "bottom"])
    
    output_clue = "The %s key to the %s is in the %s %s corner of the %s" %(room_number, next_room, clue_location_vertical, clue_location_horziontal, rooms[y])

    #clue variables
    clue_found = False  
    clue_rect = None
    clue_number = clue_number + 4
    

    return output_clue, clue_location_horziontal, clue_location_vertical

def timer (clue):
    textbox_rect = py.Rect(5, 0, 400, 700)
    screen.blit(gui_image, textbox_rect)

    time = py.time.get_ticks()
    font = py.font.Font(None, 36)
    font_small = py.font.Font(None, 18)
    text = "Time:  " + str(time/1000) + "s"
    text_surface = font.render(text, True, GREY)
    screen.blit(text_surface, (40, 30))

    if clue not in clue_menu and clue != None:
        clue_menu.append(clue)
        score_file.write(clue + "\n")
    
    y_menu_move = 0
    if clue != None:
        for n in range(len(clue_menu)):
            clue_rect_one = py.Rect(30, 75 + y_menu_move, 400, 700)
            clue_surface_one_half = font_small.render(str(clue_menu[n])[:(len(str(clue_menu[n]))//2)], True, GREY)
        
            clue_rect_two = py.Rect(25, 100 + y_menu_move, 400, 700)
            clue_surface_two_half = font_small.render(str(clue_menu[n])[(len(str(clue_menu[n]))//2):], True, GREY)

            screen.blit(clue_surface_one_half, clue_rect_one)
            screen.blit(clue_surface_two_half, clue_rect_two)

            y_menu_move = y_menu_move + 75


def factor_rect(rect):
    factor = 0.50
    width_factor = 0.5
    height_factor = 0.5
    x_move = 225
    y_move = 25

    #this scales the walls, as well as centers it
    return py.Rect(rect.x * factor + x_move, rect.y * factor - y_move, rect.width * width_factor, rect.height * height_factor)
     #ask if ok

def room():
    screen.fill(WHITE)

    global walls
    global doors
    global clues
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
        py.Rect(500, 600, 100, 100),

        #bedroom - bathroom door
        py.Rect(600, 300, 100, 100),

        #living room - kitchen door
        py.Rect(900, 1000, 100, 100),

        #kitchen - dining room door
        py.Rect(1100, 700, 200, 100)

    ]

    clues = [
        #order is topleft, top right, bottom left, bottom right
        #hallway
        py.Rect(200, 200, 100, 100),
        py.Rect(400, 200, 100, 100),
        py.Rect(200, 800, 100, 100),
        py.Rect(400, 800, 100, 100),

        #living room
        py.Rect(600, 800, 100, 100),
        py.Rect(800, 800, 100, 100),
        py.Rect(600, 1200, 100, 100),
        py.Rect(800, 1200, 100, 100),

        #bedroom
        py.Rect(600, 400, 100, 100),
        py.Rect(800, 400, 100, 100),
        py.Rect(600, 600, 100, 100),
        py.Rect(800, 600, 100, 100),

        #bathroom
        py.Rect(600, 200, 100, 100),
        py.Rect(800, 200, 100, 100),
        py.Rect(600, 200, 100, 100),
        py.Rect(800, 200, 100, 100),

        #kitchen
        py.Rect(1000, 800, 100, 100),
        py.Rect(1300, 800, 100, 100),
        py.Rect(1000, 1000, 100, 100),
        py.Rect(1300, 1000, 100, 100),

    ]

    for x in walls:
        rect = factor_rect(x)
        py.draw.rect(screen, BLACK, rect)

    z = 0
    for rect_num in doors:
        
        door = factor_rect(rect_num)

        if room_remenber_once[z] == True:
            py.draw.rect(screen,RED,door)
        elif room_remenber_once[z] == False:
            py.draw.rect(screen,GREEN,door)

        z = z + 1

    for rect in clues:
        rect_clue = factor_rect(rect)
        py.draw.rect(screen, YELLOW, rect_clue)

    screen.blit(player, player_rect)
    timer(current_clue)

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
        if x > 50:
            new_line = text[x:]
            textbox(new_line)
            break

        text_surface = font.render(text[x], True, GREY)
        screen.blit(text_surface, (200+ x_spacing, 500))

        py.display.flip()
        py.time.delay(50)

        x_spacing = x_spacing + text_surface.get_width()
        x = x + 1

        """
        if len(text) > 50:
            for e in py.event.get():
                if e.type == py.KEYDOWN:
                    half_length_text = len(text)//2
                    existing_text = text [0:half_length_text]
                    
                    screen.blit(textbox_image, textbox_rect)
                    text_surface = font.render(existing_text, True, GREY)
                    screen.blit(text_surface, (200, 500))
                    py.display.flip()
                    new_line = text[half_length_text:]
                    textbox(new_line)

                    break
        else:
        """
        #remove if bug not resolved
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

doors_list = []
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
        #counter = 0
        #player = py.image.load(south_walk[counter])
        #counter = counter + 1
        player_y = player_y + move_rate

    player_rect = py.Rect(player_x, player_y, player_width, player_height)

    for x in walls:
        rect = factor_rect(x)
        if player_rect.colliderect(rect):
            player_x = previous_x
            player_y = previous_y
            break

    for x in doors:
        door_single = factor_rect(x)
        doors_list.append(factor_rect(x))
        
        if room_remenber_once[y] == True and player_rect.colliderect(doors_list[y]) and clue_found == True:
            room_remenber_once[y] = False   
            if y in [0,3,5]:
                for z in range (1,21):
                    player_y = player_y - 5
                    player_rect.y = player_y
                    room()
                    py.display.flip()
                    py.time.delay(20)
            elif y in [1,2,4]:
                for z in range (1,21):
                    player_x = player_x + 5
                    player_rect.x = player_x
                    room()
                    py.display.flip()
                    py.time.delay(20)

            current_clue, clue_location_horziontal, clue_location_vertical = clues_place(y) 
            number_of_clues_found = number_of_clues_found + 1
            textbox(current_clue)

            #loop changes  
            clue_found = False
            print("falsed")
            entered_doors.append(doors[y])
            y = y + 1

            PRESS_RIGHT = False
            PRESS_LEFT = False
            PRESS_UP = False
            PRESS_DOWN = False


        elif player_rect.colliderect(door_single) and x not in entered_doors:
                player_x = previous_x
                player_y = previous_y
                break
    
    if clue_found == False:

        if clue_location_horziontal == "left" and clue_location_vertical == "top":
            clue_rect = factor_rect(clues[clue_number-4])
        
        elif clue_location_horziontal == "right" and clue_location_vertical == "top":
            clue_rect = factor_rect(clues[clue_number-3])
        
        elif clue_location_horziontal == "left" and clue_location_vertical == "bottom":
            clue_rect = factor_rect(clues[clue_number-2])
        
        elif clue_location_horziontal == "right" and clue_location_vertical == "bottom":
            clue_rect = factor_rect(clues[clue_number-1])
        keys = py.key.get_pressed()
        if keys[py.K_SPACE]:
                if player_rect.colliderect(clue_rect):
                    clue_found = True
                    textbox("You found the key!")
                    textbox("Now you can go to the next room!")
                    PRESS_RIGHT = False
                    PRESS_LEFT = False
                    PRESS_UP = False
                    PRESS_DOWN = False
            
    print(clue_found)
    py.display.flip()
    clock.tick(60)

score = number_of_clues_found - py.time.get_ticks()/1000 
score_file.write("Score: " + str(score))

