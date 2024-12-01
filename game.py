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

py.init()
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" %(20, 20)
running = True

# Player Varibles
player_x = 300 
player_y = 600
player = py.image.load('assets/Characters/walking_frames/tile000.png')
#you had to do this to make the transparent background - ask teacher if ok

#setup player
player_width = player.get_width() *3
player_height = player.get_height() *3
player =  py.transform.scale (player, (player_height, player_width))
move_rate = 20
mask = py.mask.from_surface(player)

#Colors
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)


#Time Track
clock = py.time.Clock()

#screen 
screen = py.display.set_mode((1000, 700))
screen.fill(WHITE)

def factor_rect(rect, factor):
    return py.Rect(rect.x * factor, rect.y * factor, rect.width * factor, rect.height * factor)

def room():
    screen.fill(WHITE)

    global walls
    global player_rect

    player_rect = py.Rect(player_x, player_y, player_width, player_height)

    walls = [
        py.Rect(100, 500, 100, 100)
    ]

    for x in walls:
        rect = factor_rect(x, 0.54)
        py.draw.rect(screen, BLACK, rect)

    screen.blit(player, player_rect)

    py.display.flip()

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

    for x in walls:
        rect = factor_rect(x, 0.54)
        if player_rect.colliderect(rect):
            player_x = previous_x
            player_y = previous_y
            break
    
    py.display.flip()

    clock.tick(60)


