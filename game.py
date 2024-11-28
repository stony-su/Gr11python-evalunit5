"""
Name: Darren Su
Period: 2
Class Code: ICU3I
Assignment: Treasure hunting house game
something I forgot about
"""

#pygame init
import pygame as py

py.display.init()
running = True

# Player Varibles
player_x = 300 
player_y = 600
player = py.image.load('C:\\Users\\Darre\\Downloads\\Counter\\Gr11python-evalunit5\\assets\\Characters\\walking_frames\\tile000.png')
player_width = player.get_width()
player_height = player.get_height()
player = player.transform.scale (player, player_height, player_width)
move_rate = 5

#Colors
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,255,255)

#Time Track
clock = py.time.Clock

#screen 
screen = py.display.set_mode((1000, 1000))
screen.fill(WHITE)



def room():
    screen.fill(WHITE)

    global walls
    global player_rect

    player_rect = py.Rect(player_x, player_y, player_width, player_height)

    walls = [
        py.Rect(700, 800, 100, 100)
    ]

    for x in walls:
        py.draw.rect(screen, BLACK, x)

    screen.blit(player, player_rect)

    py.display.flip

while running == True:
    previous_x = player_x
    previous_y = player_y

    events = py.event.get()
    for event in events:
        if event.type == py.KEYDOWN:
            if event.key == py.K_LEFT:
                player_x = player_x - move_rate
            if event.key == py.K_RIGHT:
                player_x = player_x + move_rate

            if event.key == py.K_UP:
                player_y = player_y - move_rate
            if event.key == py.K_DOWN:
                player_y = player_y + move_rate

    room()

    for rect in walls:
        if player_rect.colliderect(rect):
            player_x = previous_x
            player_y = previous_y
            break
    
    py.display.flip

    #clock.tick(60)

