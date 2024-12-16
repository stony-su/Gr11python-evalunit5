"""
Name: Darren Su
Period: 2
Date: Dec 14th
Class Code: ICU3I
Assignment: Treasure hunting house game
something I forgot about

Credits:
https://deepnight.net/tools/rpg-map/
https://itch.io/game-assets/free/tag-characters/tag-top-down
https://stock.adobe.com/ca/images/flashlight-icon-pixel-art-isolated-vector-illustration-design-stickers-logo-mobile-app-8-bit-sprite/529950989
"""

#import packages
import pygame as py
import os
import random

#init
py.init()
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" %(20, 20)
global running
running = True

#Images
global sign_img
textbox_image = py.image.load('assets/textbox/textbox.png')
gui_image = py.image.load('assets/textbox/clues_box.png')
background = py.image.load('assets/map_game.png')
win_cond = py.image.load('assets/wincon.jpg')
win_cond = py.transform.scale(win_cond, (1000, 700))
sign_img1= py.image.load("assets/object_keys/sign1.png")
sign_img2 = py.image.load("assets/object_keys/sign2.png")
sign_img = random.choice([sign_img1, sign_img2])    

#set up crate image (make global for functions to use)
global crates_rect
global crates
crates = py.image.load('assets/crates.png')
crates_w = crates.get_width()*1.6
crates_h = crates.get_height()*1.6
crates = py.transform.scale(crates,(crates_w, crates_h))

# Player starting location
player_x = 300
player_y = 600

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


#Start menu colors
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
room_remenber_once = [True, True, True, True, True, True, True]
y = 0
entered_doors = []

#Clue variables
global clue_found
global clue_rect
global clue_number 
global clue_menu
global current_clue
global current_clue_new
clue_found = True 
clue_number = 0
clue_rect = None
clue_location_horziontal = "right"
clue_location_vertical = "top"
clue_menu = []
current_clue = None
current_clue_new = None

#Flashlight and axe variables
global flash_light
global flashlight_img
flash_light = False
flashlight_img = py.image.load("assets/object_keys/flashlight.png")
flash_w = flashlight_img.get_width()//5
flash_h = flashlight_img.get_height()//5
flashlight_img =  py.transform.scale (flashlight_img, (flash_w, flash_h))


global axe_boolean
global axe_img
global crates_boolean
crates_boolean = True
axe_boolean = False
axe = py.image.load("assets/object_keys/axe.png")
axe_w = axe.get_width()//25
axe_h = axe.get_height()//25
axe_img =  py.transform.scale (axe, (axe_w, axe_h))

#Background img setup
background_w = background.get_width()*1.6
background_h = background.get_height()*1.6
background_img = py.transform.scale(background,(background_w, background_h))

dark_bathroom = py.image.load("assets/dark.png")
dark_background_w = dark_bathroom.get_width()*1.6
dark_background_h = dark_bathroom.get_height()*1.6
dark_bathroom_img = py.transform.scale(dark_bathroom,(dark_background_w, dark_background_h))

#Score
number_of_clues_found = 0
score_file = open("score.1  ", "w")
score_file.write("Clues: " + "\n")

#Time Track
clock = py.time.Clock()

#Pygame Screen 
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

#inventory for your items
def inv():
    rect = py.Rect(5, 500, 300, 50)
    py.draw.rect(screen,LIGHT_GRAY,rect)
    py.draw.rect(screen,BLACK,rect,10)

    #create rectangle item holder boxes
    for x in range(1,6):
        x_multi = x*60
        py.draw.line(screen,BLACK,(0+x_multi,500),(0 +x_multi,545),10)

    #draw the items if found
    flashlight_img_big = py.image.load("assets/object_keys/flashlight.png")
    flash_w = flashlight_img_big.get_width()//8
    flash_h = flashlight_img_big.get_height()//8
    flashlight_img_big =  py.transform.scale (flashlight_img_big, (flash_w, flash_h))
    if flash_light == True:
        screen.blit(flashlight_img_big,(10,505))

    axe_img_big = py.image.load("assets/object_keys/axe.png")
    axe_w = axe_img_big.get_width()//8
    axe_h = axe_img_big.get_height()//8
    axe_img_big =  py.transform.scale (axe_img_big, (axe_w, axe_h))

    if axe_boolean == True:
        screen.blit(axe_img,(70,505))
        
#Sprite Sheet Function - I copy and pasted this from the internet and modified it into a function with your presmission
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

#Start menu function - Allows you to swap characters and start the game
def start_menu():
    #start menu variables
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

    #while loop for start menu
    while start_menu_boolean == True:
        
        #always check for mouse location for button clicks
        for e in py.event.get():
            mouse_y_scroll = py.mouse.get_pos()[1]
            mouse_x_scroll = py.mouse.get_pos()[0]
            if e.type == py.MOUSEBUTTONDOWN:
                mx, my = e.pos
                mouse_button = e.button
        
        #draw buttons
        screen.fill(BACKGROUND)
        py.draw.rect(screen, BUTTON_FILL, rectangle)
        py.draw.rect(screen, BUTTON, rectangle, 5)
        py.draw.rect(screen,BUTTON_FILL, next_char)

        #if button collides do x action
        if rectangle.collidepoint(mx, my) and mouse_button == 1:

            #changes the button to a different color for a click effect
            py.draw.rect(screen, BUTTON_FILL_CLICK, rectangle)
            py.display.flip()
            py.time.delay(100)
            start_menu_boolean = False    

        button_text = new_roman.render("start", True, BUTTON)
        screen.blit(button_text, (460, 225))
        char_text = new_roman_small.render("next character", True, BUTTON)
        screen.blit(char_text, (415, 570))
        
        #adds triangles so user can see that the button is selected
        if 300 > mouse_y_scroll > 200:
            py.draw.polygon(screen, BUTTON, [(375, 250), (330, 225), (330, 275)])

        if 740 > mouse_y_scroll > 550:
            py.draw.polygon(screen, BUTTON, [(385, 590), (340, 570), (340, 612)])


        #Character selection
        if next_char.collidepoint(mouse_x_scroll, mouse_y_scroll) and mouse_button == 1:
            character_select = character_select + 1
            click = True
            if character_select > 9:
                character_select = 0
            
            #picks character from spreadsheet and then scales it
            char_one_walk = load_sprite_images(spritesheets[character_select], 4, 3)
            player = char_one_walk[0]
            player_width = player.get_width() *10
            player_height = player.get_height() *10
            player =  py.transform.scale (player, (player_height, player_width))

        #draws new character
        screen.blit(player, (413,340))
        
        #click effect
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

    #rooms and room numbers
    rooms = ["Hallway", "Living Room", "Bedroom", "Bathroom", "Kitchen", "Dining Room", "Treasure"]
    room_numbers = ["first", "second", "third", "fourth", "fifth"  , "Placehold"]

    next_room = rooms[y+1]

    room_number = room_numbers[y]

    #randomly generate the location of the clue
    clue_location_horziontal = random.choice(["left", "right"])
    clue_location_vertical = random.choice(["top", "bottom"])
    
    #output the clue onto the screen using timer function
    output_clue = "The %s key to the %s is in the %s %s corner of the %s" %(room_number, next_room, clue_location_vertical, clue_location_horziontal, rooms[y])

    #clue variables, add four because there are 4 potienal clues for each room, and this switches to the next room
    clue_number = clue_number + 4

    return output_clue, clue_location_horziontal, clue_location_vertical

#the clue + timer function
def timer (clue):
    #draws pixel art box for menu
    textbox_rect = py.Rect(5, 0, 400, 700)
    screen.blit(gui_image, textbox_rect)

    #draws the time
    time = py.time.get_ticks() - init_time
    font = py.font.Font(None, 36)
    font_small = py.font.Font(None, 18)
    text = "Time:  " + str(time/1000) + "s"
    text_surface = font.render(text, True, GREY)
    screen.blit(text_surface, (40, 30))

    #draws the clue if not found yet
    if clue not in clue_menu and clue != None:
        clue_menu.append(clue)
        score_file.write(clue + "\n")
    
    y_menu_move = 0

    #makes the sentence cut off then it reaches the end of the box
    if clue != None:
        for n in range(len(clue_menu)):
            clue_rect_one = py.Rect(30, 75 + y_menu_move, 400, 700)
            clue_surface_one_half = font_small.render(str(clue_menu[n])[:(len(str(clue_menu[n]))//2)], True, GREY)
        
            clue_rect_two = py.Rect(25, 100 + y_menu_move, 400, 700)
            clue_surface_two_half = font_small.render(str(clue_menu[n])[(len(str(clue_menu[n]))//2):], True, GREY)

            screen.blit(clue_surface_one_half, clue_rect_one)
            screen.blit(clue_surface_two_half, clue_rect_two)

            y_menu_move = y_menu_move + 75

#I drew the map with 100 x 100 boxes, but since the map is 1000 x 700, I need to scale it down to fit the all the tiles
def factor_rect(rect):
    factor = 0.50
    width_factor = 0.5
    height_factor = 0.5
    x_move = 225
    y_move = 25

    #also centers it according to my needs, I got your premission to use rect.x, rect.y, etc
    return py.Rect(rect.x * factor + x_move, rect.y * factor - y_move, rect.width * width_factor, rect.height * height_factor)

#the sign must be scale and centered futher, because each sign location is different, so I made a new function
def sign_factor(rect):
    width_factor = 4
    height_factor = 4
    x_move = 12
    y_move = 25

    return py.Rect(rect.x + x_move, rect.y + y_move, rect.width * width_factor, rect.height * height_factor)

#sign generation function
def sign (): 
    sign_rect = []
    w = sign_img.get_width()//5
    h = sign_img.get_height()//5

    def margin (x):
        return x - 150
    
    #randomly generate the location of the sign within each room
    room_list_space_clues = [(random.randint(200,margin(500)),random.randint(200,margin(900))), (random.randint(600,margin(900)),random.randint(400,margin(700))), (random.randint(600,margin(900)),random.randint(800,margin(1300))), (random.randint(600,margin(900)),random.randint(150,200)), (random.randint(1000,margin(1400)),random.randint(700,margin(1000)))]

    x = 0

    for x in range(len(room_list_space_clues)):
        xy = room_list_space_clues[x] 
        sign_rect.append(py.Rect(xy[0], xy[1], w, h  ))

    return sign_rect

#randomly places the flashlight and axe in random locations, I got your premission to use coordinate tuples (xy[0], xy[1])
def flashlight ():
    w = flashlight_img.get_width()//5
    h = flashlight_img.get_height()//5
    def margin (x):
        return x - 150
    room_list_space = [(random.randint(200,margin(500)),random.randint(200,margin(900))), (random.randint(600,margin(900)),random.randint(400,margin(700))), (random.randint(600,margin(900)),random.randint(800,margin(1300)))]
    xy = random.choice(room_list_space)
    flash_rect = factor_rect(py.Rect(xy[0], xy[1], w+70, h+70))   
    return flash_rect

def axe ():
    w2 = axe_img.get_width()//25
    h2 = axe_img.get_height()//25

    def margin (x):
        return x - 50
    
    room_list_space = [(random.randint(200,margin(500)),random.randint(200,margin(900))), (random.randint(600,margin(900)),random.randint(400,margin(700))), (random.randint(600,margin(900)),random.randint(800,margin(1300)))]
    xy = random.choice(room_list_space)
    axe_rect = factor_rect(py.Rect(xy[0], xy[1], w2+70, h2+70))   
    return axe_rect

#sets up the variables
global flash_rect_global
flash_rect_global = flashlight()

global axe_rect_global
axe_rect_global = axe()
 
sign_rect = sign()

#room draw function - draws the entire game
def room():
    screen.fill(WHITE)
    screen.blit(background_img,(0,0))

    global walls
    global doors
    global clues
    global player_rect

    #player hitbox
    player_rect = py.Rect(player_x, player_y, player_width, player_height)

    #list of all walls
    walls = [
        #top wall
        py.Rect(100, 0, 900, 100),  

        #left-most wall
        py.Rect(0, 100, 100, 800), 

        #bottom-left door
        py.Rect(100, 900, 125, 100), 
        py.Rect(400, 900, 100, 100), 

        #hallway - bathroom wall
        py.Rect(500, 100, 50, 450), 

        #bedroom - dining room wall
        py.Rect(900, 100, 50, 800), 

        #living room - kitchen wall
        py.Rect(500, 900, 50, 500),  

        #bottom-most wall
        py.Rect(500, 1300, 500, 50),  

        #living room - kitchen wall, right side bottom
        py.Rect(900, 1100, 100, 200), 

        #kitchen wall bottom
        py.Rect(900, 1100, 600, 100), 

        #bedroom-living room wal
        py.Rect(500, 700, 600, 50),
        
        #bedroom-dinning top wall
        py.Rect(700, 300, 800, 50),

        #right-most wall
        py.Rect(1400, 300, 50, 900),

        #kitchen-dining room door
        py.Rect(1300, 700, 200, 50),
    ]

    #door locations
    doors = [
        #hallway
        py.Rect(275, 875, 100, 100),

        #hallway - livingroom door
        py.Rect(500, 775, 100, 100),
        
        #hallway - bedroom door
        py.Rect(500, 550, 100, 100),

        #bedroom - bathroom door
        py.Rect(570, 200, 100, 100),

        #living room - kitchen door
        py.Rect(900, 975, 100, 100),

        #kitchen - dining room door
        py.Rect(1100, 600, 200, 100)

    ]

    #clue locations
    clues = [
        #order is topleft, top right, bottom left, bottom right
        #hallway
        py.Rect(100, 100, 100, 100),
        py.Rect(400, 100, 100, 100),
        py.Rect(100, 800, 100, 100),
        py.Rect(400, 800, 100, 100),

        #living room
        py.Rect(550, 750, 100, 100),
        py.Rect(800, 750, 100, 100),
        py.Rect(550, 1200, 100, 100),
        py.Rect(800, 1200, 100, 100),

        #bedroom
        py.Rect(500, 300, 100, 100),
        py.Rect(800, 300, 100, 100),
        py.Rect(500, 600, 100, 100),
        py.Rect(800, 600, 100, 100),

        #bathroom
        py.Rect(550, 100, 100, 100),
        py.Rect(800, 100, 100, 100),
        py.Rect(550, 150, 100, 100),
        py.Rect(800, 150, 100, 100),

        #kitchen
        py.Rect(950, 750, 100, 100),
        py.Rect(1325, 750, 100, 100),
        py.Rect(950, 1000, 100, 100),
        py.Rect(1325, 1000, 100, 100),

    ]

    #if the player picks up an item, the item will disappear
    bathroom_rect = factor_rect(py.Rect(500, 100, 400, 200))
        
    if flash_light == False or player_rect.colliderect(bathroom_rect) == False:
        #py.draw.rect(screen, BLACK, bathroom_rect)
        screen.blit(dark_bathroom_img,(0,0))

    #if the player has the flashlight, the bathroom will be lit up
    if player_rect.colliderect(bathroom_rect):
        screen.blit(background_img,(0,0))
    
    if crates_boolean == True:
        screen.blit(crates,crates_rect)

    if flash_light == False:
        screen.blit (flashlight_img, flash_rect_global)

    if axe_boolean == False:
        screen.blit (axe_img, axe_rect_global)
    
    #for all randomly randomly generated signs in the list, draw them
    for x in sign_rect:
        rect = factor_rect(x)
        screen.blit(sign_img, rect)

    if chest_boolean == False:
        chest = chest_anime[0]
        chest =  py.transform.scale (chest, (60, 60))
        screen.blit(chest, chest_rect)

    screen.blit(player, player_rect)
    timer(current_clue_new)
    inv()

    py.display.flip()

#textbox function allowing me to tell the player what to do and clues
def textbox (text):
    text = str(text)
    textbox_rect = py.Rect(150, 400, 500, 100)
    screen.blit(textbox_image, textbox_rect)
    py.display.flip()

    font = py.font.Font(None, 36)
    x = 0
    x_spacing = 0

    #if the text is bigger than the textbox, it will cut off and continue on the next line
    while x < len(text):
        if x > 50:
            new_line = text[x:]
            textbox(new_line)
            break

        text_surface = font.render(text[x], True, GREY)
        screen.blit(text_surface, (200+ x_spacing, 500))

        py.display.flip()
        py.time.delay(20)

        x_spacing = x_spacing + text_surface.get_width()
        x = x + 1


    while True:
        for e in py.event.get():
            if e.type == py.KEYDOWN:
                return

#more variables setup
doors_list = []
walk_frame_1 = 2
walk_frame_2 = 2
walk_frame_3 = 1
walk_frame_4 = 0
walk_slowed = 0
first_right = False
first_left = False
first_top = False
first_bottom = False

cretes_w = crates.get_width()
cretes_h = crates.get_height()
crates_rect = py.Rect(0,342, cretes_w, cretes_h)
crates_rect_blockage = factor_rect(py.Rect(940,720, 400,100))

#main game loop
while running == True:
    
    #at the start, init a bunch of things
    if START == True:
        #this inits the chest 

        current_direction = "DOWN"

        global chest_anime
        global chest_rect
        global chest_boolean
        chest_boolean = False
        chest = 'assets/chest.png'
        chest_anime = load_sprite_images(chest, 4, 1)
        chest_rect = factor_rect(py.Rect(1125, 400, 60, 60))
        character_select = start_menu()

        #inits walking frames for selected charater
        char_one_walk = load_sprite_images(spritesheets[character_select], 4, 3)
        player = char_one_walk[0]
        player_width = player.get_width() *2
        player_height = player.get_height() *2
        player =  py.transform.scale (player, (player_height, player_width))

        #gives the player hints and controls
        textbox("hint: spacebar to move through textboxes")
        textbox("controls: arrow keys to move")
        textbox("There is a chest in the house, find it to win")
        textbox("Pick up items and destory crates using space")
        textbox("Your final score will be based off")
        textbox("the total amount of clues you used")
        textbox("and the time it took you to find the chest")
        global init_time
        init_time = py.time.get_ticks()
        START = False
    
    #controls loop
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
    #draws the screen
    room()

    #sets up the previous x and y for the player
    previous_x = player_x
    previous_y = player_y

    #if player moves, change the player sprite animation
    if PRESS_RIGHT == True:
        if walk_slowed % 10 == 0:
            if walk_frame_1 < 12:
                player = char_one_walk[0 + walk_frame_1]
                player =  py.transform.scale (player, (player_height, player_width))
                walk_frame_1 = walk_frame_1 + 3
            else: 
                walk_frame_1 = 2

        walk_slowed = walk_slowed + 2
        player_x = player_x + move_rate

    if PRESS_LEFT == True: 
        if walk_slowed % 10 == 0:
            if walk_frame_2 < 12:
                player = char_one_walk[0 + walk_frame_2]
                player =  py.transform.scale (player, (player_height, player_width))
                player = py.transform.flip(player, True, False)
                walk_frame_2 = walk_frame_2 + 3
            else: 
                walk_frame_2 = 2

        walk_slowed = walk_slowed + 2
        player_x = player_x - move_rate

    if PRESS_UP == True: 
        if walk_slowed % 10 == 0:
            if walk_frame_3 < 12:
                player = char_one_walk[0 + walk_frame_3]
                player =  py.transform.scale (player, (player_height, player_width))
                walk_frame_3 = walk_frame_3 + 3
            else: 
                walk_frame_3 = 1
        walk_slowed = walk_slowed + 2
        player_y = player_y - move_rate
        
    if PRESS_DOWN == True: 
        if walk_slowed % 10 == 0:
            if walk_frame_4 < 12:
                player = char_one_walk[0 + walk_frame_4]
                player =  py.transform.scale (player, (player_height, player_width))
                walk_frame_4 = walk_frame_4 + 3
            else: 
                walk_frame_4 = 0
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
            if current_clue == "Finished":
                running = False
                break  

            number_of_clues_found = number_of_clues_found + 1

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
            textbox("The door is locked")
            PRESS_RIGHT = False
            PRESS_LEFT = False
            PRESS_UP = False
            PRESS_DOWN = False
            
            break

    for x in sign_rect:
        sign_rect_single = sign_factor(factor_rect(x))
        if player_rect.colliderect(sign_rect_single):
            player_x = previous_x
            player_y = previous_y
            textbox(current_clue)
            current_clue_new = current_clue
            PRESS_RIGHT = False
            PRESS_LEFT = False
            PRESS_UP = False
            PRESS_DOWN = False
    
    if running == False:
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
    
    if axe_boolean == False:
        if player_rect.colliderect(axe_rect_global):
            if keys[py.K_SPACE]:
                textbox("You found an axe!")
                axe_boolean = True
                PRESS_RIGHT = False
                PRESS_LEFT = False
                PRESS_UP = False
                PRESS_DOWN = False
        
    if player_rect.colliderect(crates_rect_blockage) and crates_boolean == True:
        if axe_boolean == True: 
            textbox("Chop Chop Chop...")
            crates_boolean = False

        if crates_boolean == True:
            player_x = previous_x
            player_y = previous_y       
            textbox("A pile of crates block your path")
            PRESS_RIGHT = False
            PRESS_LEFT = False
            PRESS_UP = False
            PRESS_DOWN = False

    if player_rect.colliderect(chest_rect):
        
        textbox("You found the treasure!")
        break

    py.display.flip()
    clock.tick(60)

score = 10*number_of_clues_found - (py.time.get_ticks()-init_time)/1000
score_text = str(int(score))
score_file.write("Score: " + score_text)

while True:
    screen.blit(win_cond,(0,0))
    new_roman = py.font.SysFont("Times New Roman", 50)
    win_text = new_roman.render("Score:"+score_text, True, WHITE)
    screen.blit(win_text, (350, 500))
    py.display.flip()
