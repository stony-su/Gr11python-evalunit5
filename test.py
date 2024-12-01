import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" %(20, 20)

from pygame import * 
init()
screen = display.set_mode((800,600))
myClock = time.Clock()

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
WHITE = (255,255,255)
def rectangles(mx,my):
    screen.fill(WHITE)
    rect1 = Rect(250,250,300,150)
    rect2 = Rect(mx,my,100,100)
    
    draw.rect(screen, GREEN, rect1)
    draw.rect(screen, BLUE, rect2)
    display.flip()
    
    return rect1, rect2
    
running = True
while running:
    
    for e in event.get():
        if e.type == QUIT:
            running = False

        if e.type == MOUSEMOTION:
            mx,my = e.pos      
            rect1, rect2 = rectangles(mx, my)
            
            if rect1.colliderect(rect2):
                draw.rect(screen, RED, rect1, 3)
                display.flip()
        
    myClock.tick(60) 
  
quit()