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
textbox_image = py.image.load('assets/textbox/textbox.png')
gui_image = py.image.load('assets/textbox/clues_box.png')

# Player Varibles
player_x = 200*0.45
player_y = 1100*0.45

#setup player movement
move_rate = 5

#Colors
BLACK = (0,0,0)
WHITE = (255,255,255)
YELLOW = (255,255,0)
FAINT_YELLOW_1 = (255,253,175)
FAINT_YELLOW_2 = (255,253,141)
FAINT_YELLOW_HALF = (255,254,224)
RED = (255,0,0)
GREEN = (0,128,0)
GREY = (200,200,200)
GRAY = (237,233,223)
BLUE = (65,182,232)
LIGHT_GRAY = (211, 211, 211)
PURPLE = (211,144,240)


#start menu colors
BACKGROUND = (16, 30, 31)
BUTTON = (254, 173, 65)
BUTTON_FILL = (104, 56, 46)
BUTTON_FILL_CLICK = (84, 36, 24)


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

#Objects
global flash_light
global flashlight_img
flash_light = False
flashlight_img = py.image.load("assets/object_keys/flashlight.png")
flash_w = flashlight_img.get_width()//10
flash_h = flashlight_img.get_height()//10
flashlight_img =  py.transform.scale (flashlight_img, (flash_w, flash_h))

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
spritesheets = [
'assets/spritesheets/1 walk.png',
'assets/spritesheets/2 walk.png',
"assets/spritesheets/3 walk.png",
"assets/spritesheets/4 walk.png",
"assets/spritesheets/5 walk.png",
"assets/spritesheets/6 walk.png",
"assets/spritesheets/7 walk.png",
"assets/spritesheets/8 walk.png",
"assets/spritesheets/9 walk.png",
"assets/spritesheets/10 walk.png"
]

def load_sprite_images(filename, num_rows, num_cols):
    x_margin = 0
    x_padding = 0
    y_margin = 0 
    y_padding = 0
    sheet = py.image.load(filename).convert()
    
    def image_at(sheet, rectangle):
        rect = py.Rect(rectangle)
        image = py.Surface(rect.size).convert()
        image.blit(sheet, (0, 0), rect)

        colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, py.RLEACCEL)
        return image   

    sheet_rect = sheet.get_rect()
    sheet_width, sheet_height = sheet_rect.size
    x_sprite_size = (sheet_width - 2 * x_margin - (num_cols - 1) * x_padding) / num_cols
    y_sprite_size = (sheet_height - 2 * y_margin - (num_rows - 1) * y_padding) / num_rows

    sprite_rects = []
    for row_num in range(num_rows):
        for col_num in range(num_cols):
            x = x_margin + col_num * (x_sprite_size + x_padding)
            y = y_margin + row_num * (y_sprite_size + y_padding)
            sprite_rect = (x, y, x_sprite_size, y_sprite_size)
            sprite_rects.append(sprite_rect)

    grid_images = [image_at(sheet, rect) for rect in sprite_rects]
    
    return grid_images

#Button Function
def start_menu():
    start_menu_boolean = True
    mx = 0
    my = 0 
    mouse_button = 0
    mouse_y_scroll = 0
    mouse_x_scroll = 0
    new_roman = py.font.SysFont("Times New Roman", 50)
    new_roman_small = py.font.SysFont("Times New Roman", 30)
    rectangle = py.Rect(400, 200, 200, 100)
    next_char = py.Rect(405, 550, 190, 80)
    character_select = 0
    char_one_walk = load_sprite_images(spritesheets[0], 4, 3)
    player = char_one_walk[0]
    player_width = player.get_width() *10
    player_height = player.get_height() *10
    player =  py.transform.scale (player, (player_height, player_width))
    click = False

    while start_menu_boolean == True:
        for e in py.event.get():
            mouse_y_scroll = py.mouse.get_pos()[1]
            mouse_x_scroll = py.mouse.get_pos()[0]
            if e.type == py.MOUSEBUTTONDOWN:
                mx, my = e.pos
                mouse_button = e.button
                
        screen.fill(BACKGROUND)
        py.draw.rect(screen, BUTTON_FILL, rectangle)
        py.draw.rect(screen, BUTTON, rectangle, 5)
        py.draw.rect(screen,BUTTON_FILL, next_char)

        if rectangle.collidepoint(mx, my) and mouse_button == 1:
            py.draw.rect(screen, BUTTON_FILL_CLICK, rectangle)
            py.display.flip()
            py.time.delay(100)
            start_menu_boolean = False    

        button_text = new_roman.render("start", True, BUTTON)
        screen.blit(button_text, (460, 225))
        char_text = new_roman_small.render("next character", True, BUTTON)
        screen.blit(char_text, (415, 570))

        if 300 > mouse_y_scroll > 200:
            py.draw.polygon(screen, BUTTON, [(375, 250), (330, 225), (330, 275)])

        if 740 > mouse_y_scroll > 550:
            py.draw.polygon(screen, BUTTON, [(375, 637), (330, 575), (330, 700)])


        #Character selection
        if next_char.collidepoint(mouse_x_scroll, mouse_y_scroll) and mouse_button == 1:
            character_select = character_select + 1
            click = True
            if character_select > 9:
                character_select = 0
                
            char_one_walk = load_sprite_images(spritesheets[character_select], 4, 3)
            player = char_one_walk[0]
            player_width = player.get_width() *10
            player_height = player.get_height() *10
            player =  py.transform.scale (player, (player_height, player_width))

        screen.blit(player, (413,340))
        
        if click == True:
            py.draw.rect(screen, BUTTON_FILL_CLICK, next_char)
            py.display.flip()
            py.time.delay(100)
            click = False

        mouse_button = 0

        py.display.flip()

    screen.fill(WHITE)

    return character_select

#clue generation function
def clues_place (y):
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

def flashlight ():
    global w
    w = flashlight_img.get_width()//10
    h = flashlight_img.get_height()//10
    def margin (x):
        return x - 50
    room_list_space = [(random.randint(200,margin(500)),random.randint(200,margin(900))), (random.randint(600,margin(900)),random.randint(400,margin(700))), (random.randint(600,margin(900)),random.randint(800,margin(1300)))]
    xy = random.choice(room_list_space)
    flash_rect = factor_rect(py.Rect(xy[0], xy[1], w+70, h+70))   
    return flash_rect

global flash_rect_global
flash_rect_global = flashlight()

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
    
    for x in clues:
        clue_rect = factor_rect(x)
        py.draw.rect(screen, YELLOW, clue_rect)

    for rect in clues:
        rect_clue = factor_rect(rect)
        py.draw.rect(screen, YELLOW, rect_clue)

    bathroom_rect = factor_rect(py.Rect(600, 200, 300, 100))
    if flash_light == False or player_rect.colliderect(bathroom_rect) == False:
        py.draw.rect(screen, BLACK, bathroom_rect)

    if player_rect.colliderect(bathroom_rect):
        py.draw.rect(screen, FAINT_YELLOW_1, bathroom_rect)

    if flash_light == False:
        screen.blit (flashlight_img, flash_rect_global)


    screen.blit(player, player_rect)
    timer(current_clue)

    py.display.flip()

def textbox (text):
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
walk_frame = 4
walk_slowed = 0
first_right = False
first_left = False
first_top = False
first_bottom = False
while running == True:

    if START == True:
        character_select = start_menu()
        #walking frames
        char_one_walk = load_sprite_images(spritesheets[character_select], 4, 3)
        player = char_one_walk[0]
        player_width = player.get_width() *2
        player_height = player.get_height() *2
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
        if first_right == True:
                walk_frame = 2
        if walk_slowed % 10 == 0:
            if walk_frame < 12:
                player = char_one_walk[0 + walk_frame]
                player =  py.transform.scale (player, (player_height, player_width))
                walk_frame = walk_frame + 3
            else: 
                walk_frame = 2
        walk_slowed = walk_slowed + 2
        player_x = player_x + move_rate

    if PRESS_LEFT == True: 
        player_x = player_x - move_rate

    if PRESS_UP == True: 
        if walk_slowed % 10 == 0:
            if walk_frame < 12:
                player = char_one_walk[0 + walk_frame]
                player =  py.transform.scale (player, (player_height, player_width))
                walk_frame = walk_frame + 3
            else: 
                walk_frame = 1
        walk_slowed = walk_slowed + 2
        player_y = player_y - move_rate
        
    if PRESS_DOWN == True: 
        first_right = False
        first_left = False
        first_top = False
        if walk_slowed % 10 == 0:
            if walk_frame < 12:
                player = char_one_walk[0 + walk_frame]
                player =  py.transform.scale (player, (player_height, player_width))
                walk_frame = walk_frame + 3
            else: 
                walk_frame = 0
        walk_slowed = walk_slowed + 2
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
    
            #loop changes  
            current_clue, clue_location_horziontal, clue_location_vertical  = clues_place(y) 
            number_of_clues_found = number_of_clues_found + 1
            textbox(current_clue)

            #loop changes  
            clue_found = False
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

    bathroom_rect = factor_rect(py.Rect(600, 200, 200, 100))
    keys = py.key.get_pressed()

    if flash_light == False:
        if player_rect.colliderect(flash_rect_global):
            if keys[py.K_SPACE]:
                textbox("You found a flashlight!")
                flash_light = True
                PRESS_RIGHT = False
                PRESS_LEFT = False
                PRESS_UP = False
                PRESS_DOWN = False

        if player_rect.colliderect(bathroom_rect):
            player_x = previous_x
            player_y = previous_y       
            textbox("It seems that the light in the bathroom is broken")
            PRESS_RIGHT = False
            PRESS_LEFT = False
            PRESS_UP = False
            PRESS_DOWN = False

    py.display.flip()
    clock.tick(60)

score = number_of_clues_found - py.time.get_ticks()/1000 
score_file.write("Score: " + str(score))

