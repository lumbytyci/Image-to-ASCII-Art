from PIL import Image
import numpy as np
from collections import namedtuple

Size = namedtuple('Size', ['width', 'height'])

tile_size = Size(width = 10, height = 20)
image_size = Size(width = 800, height = 800)
no_horizontal_tiles = int(image_size.width / tile_size.width) 
no_vertical_tiles = int(image_size.height / tile_size.height)

try:
    img = Image.open('rocket.png')
    img = img.convert('L')
    img = img.resize(image_size)
    # img.show()
except Exception as e:
    print(e)
    print("Some error occurred, image could not be displayed!")
    exit()


def find_tile_brightness(img_section):
    width, height = img_section.size
    pixels = np.array(img_section)
    # brightness_sum = sum([sum(x) for x in pixels])
    # return brightness_sum / (width * height)
    return np.average(pixels.reshape(width * height))


brightness_grid = []

for y in range(0, image_size.height, tile_size.height):
    row = []
    for x in range(0, image_size.width, tile_size.width):
        img_tile = img.crop((x,y,x + tile_size.width, y + tile_size.height))
        row.append(find_tile_brightness(img_tile))
    brightness_grid.append(row)



print("ASCII Masterpiece: \n")

for x in range(0, no_vertical_tiles):
    for y in range(0, no_horizontal_tiles):
        filler = ''
        if brightness_grid[x][y] < 10:
            filler = '.'
        elif brightness_grid[x][y] >= 10 and brightness_grid[x][y] < 20:
            filler = ','
        elif brightness_grid[x][y] >= 20 and brightness_grid[x][y] < 50:
            filler = '+'
        elif brightness_grid[x][y] >= 50 and brightness_grid[x][y] < 100:
            filler = '='
        elif brightness_grid[x][y] >= 100 and brightness_grid[x][y] < 140:
            filler = 's'
        elif brightness_grid[x][y] >= 140 and brightness_grid[x][y] < 180:
            filler = '?'
        elif brightness_grid[x][y] >= 180 and brightness_grid[x][y] < 200:
            filler = '$'
        elif brightness_grid[x][y] >= 200 and brightness_grid[x][y] < 220:
            filler = '#'
        elif brightness_grid[x][y] >= 220:
            filler = '@'


        print(filler, end="")

    print("", end="\n")