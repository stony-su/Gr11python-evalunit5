from pygame import *
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,255,255)
running = True
player_x = 300 
player_y = 600

screen = (1500, 1500)
screen.fill(WHITE)
player = image.load(f'assets\Characters\walking_frames\tile000.png')
player_width = player.get_width() //12
player_height = player.get_height()//12

def room():
    screen.fill(WHITE)

    global walls
    global player_rect

    walls = [
        Rect(x,y, 100, 100)
    ]

    for x in walls:
        draw.rect(screen,BLACK, rect)

    player_rect = Rect(player_x, player_y, player_width, player_height)
    screen.blit(player, player_rect)
    display.flip

previous_x = player_x
previous_y = player_y

if PRESS_RIGHT == True:
    player_y = player_y + moverate

player_rect = Rect(player_x, player_y, player)
for rect in walls:
    if player_rect.colliderect(rect):
        player_x = previous_x
        player_y = previous_y
        break
clock.tick(60)

quit()
