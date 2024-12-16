import random
import pygame as py
sign_img1= py.image.load("assets/object_keys/sign1.png")
sign_img2 = py.image.load("assets/object_keys/sign2.png")
sign_img = random.choice([sign_img1, sign_img2])    
def sign (): 
    sign_rect = []
    w = sign_img.get_width()//5
    h = sign_img.get_height()//5

    def margin (x):
        return x - 150
    room_list_space_clues = [(random.randint(200,margin(500)),random.randint(200,margin(900))), (random.randint(600,margin(900)),random.randint(400,margin(700))), (random.randint(600,margin(900)),random.randint(800,margin(1300))), (random.randint(600,margin(900)),random.randint(150,200)), (random.randint(600,margin(900)),random.randint(700,margin(1200))), (random.randint(1000,margin(1400)),random.randint(700,margin(1000)))]

    x = 0

    for x in range(len(room_list_space_clues)):
        xy = room_list_space_clues[x] 
        sign_rect.append(py.Rect(xy[0], xy[1], w, h  ))

    return sign_rect

sign_lis = sign()
print(sign_lis)

def factor_rect(rect):
    factor = 0.50
    width_factor = 0.5
    height_factor = 0.5
    x_move = 225
    y_move = 25

    #this scales the walls, as well as centers it
    return py.Rect(rect.x * factor + x_move, rect.y * factor - y_move, rect.width * width_factor, rect.height * height_factor)


for x in sign_lis:
        rect = factor_rect(x)
        print(rect)

