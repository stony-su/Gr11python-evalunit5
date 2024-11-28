"""
comments and shit
"""

import random   
rooms_rightleft_levelone = ["Hallway", "Bathroom, Empty"]
rooms_rightleft_leveltwo = ["Hallway", "Bedroom, Dining Room"]
rooms_rightleft_levelthree = ["Hallway", "Living Room, Kitchen"]

global location
location = "Hallway"
global x_pos
x_pos = 1
global y_pos
y_pos = 3

hallway_x_pos = [1, 2, 3]
hallway_y_pos = [3, 4, 5, 6, 7]

living_room_x_pos = [4,5,6]
living_room_y_pos = []

walls_x_pos = [13,13,13,13,13,13,13, 13, 12 ,11, 10, 9, 8, 7, 6, 5, 5, 5,5,4,3, 5, ]
walls_y_pos = [1, 2, 3, 4, 5, 6, 7, 8, 9, 1 , 1, 1, 1, 1, 1, 1, 1, 2, 4, 5,5,]

def movement(direction):
    if direction == "right":
       x_pos = x_pos + 1
    elif direction == "left":
        x_pos = x_pos - 1
    elif direction == "up":
        y_pos = y_pos + 1
    elif direction == "down":
        y_pos = y_pos - 1
    return


def hallway_movement (hallway_x_pos, hallway_y_pos):
    if x_pos in hallway_x_pos and y_pos in hallway_y_pos:
        place = "Hallway"
        
    return place



while True:
    previous_location = location
    print('hello, you are trapped inside this game')
    print("which direction do you go?")

    if y_pos < 0:
        print ("you have exited the house")
        print ("GAME OVER")
        break
    if x_pos < 0:
        print ("you have exited the house")
        print ("GAME OVER")
    
    direction = input("Enter Direction:")
    
    location = hallway_movement(hallway_x_pos, hallway_y_pos)
