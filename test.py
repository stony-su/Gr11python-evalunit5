import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" %(20, 20)

from pygame import * 
init()
screen = display.set_mode((500,500))

BLACK = (0,0,0)
WHITE= (255,255,255)
RED = (255,0,0)
GREEN = (134,235,140)
YELLOW = (255,255,0)
GRAY = (237,233,223)
BLUE = (65,182,232)
PURPLE = (211,144,240)

myFont = font.SysFont("Times New Roman",50)

rectangle = Rect(150, 200, 200, 100)

mx = 0
my = 0
button = 0

def drawRectangle(screen,button,mx,my):
    screen.fill(WHITE)
    
    draw.rect(screen, GRAY, rectangle)
    draw.rect(screen, BLACK, rectangle, 3)
    
    if rectangle.collidepoint(mx,my) and button == 1:
        draw.rect(screen, YELLOW, rectangle)
        draw.rect(screen, BLACK, rectangle, 2)
    elif rectangle.collidepoint(mx,my) and button == 3:
        draw.rect(screen, GREEN, rectangle)
        draw.rect(screen, BLACK, rectangle, 2)
    elif rectangle.collidepoint(mx,my) and button == 4:
        draw.rect(screen, BLUE, rectangle)
        draw.rect(screen, BLACK, rectangle, 2)
    elif rectangle.collidepoint(mx,my) and button == 5:
        draw.rect(screen, PURPLE, rectangle)
        draw.rect(screen, BLACK, rectangle, 2)    
    
    string = str(button)
    text = myFont.render(string, True, RED)
    screen.blit(text, (240,225))
    display.flip()

running = True
while running:
    
    for e in event.get():
        if e.type == QUIT:
            running = False
        if e.type == MOUSEBUTTONDOWN:
            mx, my = e.pos          
            button = e.button
                    
    drawRectangle(screen, button, mx, my)
    
quit()


