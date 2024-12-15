import pygame as py

# Initialize Pygame
py.init()

# Set up display
screen = py.display.set_mode((800, 600))
py.display.set_caption('Walking Animation')

# Walking Animation
one_img = 'Fantasy RPG (Toony) 32x32.png'

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

# Walking frames
char_one_walk = load_sprite_images(one_img, 8, 11)
x = 0  # Initial x position for drawing on the screen
y = 0  # Initial y position
clock = py.time.Clock()

running = True
while running:
    for event in py.event.get():
        if event.type == py.QUIT:
            running = False
            
    screen.fill((255, 255, 255))  # Clear screen with white background
    for index, img in enumerate(char_one_walk):
        screen.blit(img, (x + index * 50, y))
    
    py.display.flip()
    py.time.delay(100)  # 100 ms between frames
    clock.tick(10)  # Adjust the frame rate for smooth animation

# Quit Pygame
py.quit()
