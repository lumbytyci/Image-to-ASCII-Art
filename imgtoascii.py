import sys

from collections import namedtuple
from PIL import Image
import numpy as np

Size = namedtuple('Size', ['width', 'height'])

props = {
    'tile_size': Size(width=10, height=20),
    'image_size': Size(width=800, height=800),
}


def open_resized_image(image_path):
    try:
        image = Image.open(image_path)
        image = image.convert('L')
        image = image.resize(props['image_size'])
        return image
    except Exception as e:
        print("Exception occurred, image could not be displayed!", e)
        exit()


def find_tile_brightness(image_section):
    width, height = image_section.size
    pixels = np.array(image_section)
    return np.average(pixels.reshape(width * height))


def create_brightness_grid(image):
    brightness_grid = []
    for y in range(0, props['image_size'].height, props['tile_size'].height):
        row = []
        for x in range(0, props['image_size'].width, props['tile_size'].width):
            image_tile = image.crop((x, y, x + props['tile_size'].width,
                                     y + props['tile_size'].height))
            row.append(find_tile_brightness(image_tile))
        brightness_grid.append(row)

    return brightness_grid


def convert_image_to_text(brightness_grid):
    output_text = ''
    num_horizontal_tiles = int(
        props['image_size'].width / props['tile_size'].width)
    num_vertical_tiles = int(
        props['image_size'].height / props['tile_size'].height)

    for x in range(0, num_vertical_tiles):
        for y in range(0, num_horizontal_tiles):
            if brightness_grid[x][y] < 10:
                output_text += '.'
            elif brightness_grid[x][y] >= 10 and brightness_grid[x][y] < 20:
                output_text += ','
            elif brightness_grid[x][y] >= 20 and brightness_grid[x][y] < 50:
                output_text += '+'
            elif brightness_grid[x][y] >= 50 and brightness_grid[x][y] < 100:
                output_text += '='
            elif brightness_grid[x][y] >= 100 and brightness_grid[x][y] < 140:
                output_text += 's'
            elif brightness_grid[x][y] >= 140 and brightness_grid[x][y] < 180:
                output_text += '?'
            elif brightness_grid[x][y] >= 180 and brightness_grid[x][y] < 200:
                output_text += '$'
            elif brightness_grid[x][y] >= 200 and brightness_grid[x][y] < 220:
                output_text += '#'
            elif brightness_grid[x][y] >= 220:
                output_text += '@'
        output_text += '\n'

    return output_text


def main():
    if len(sys.argv) < 2:
        exit(f"Usage: {sys.argv[0]} <path-to-image>")

    image = open_resized_image(sys.argv[1])
    brightness_grid = create_brightness_grid(image)
    print(convert_image_to_text(brightness_grid))


if __name__ == "__main__":
    main()
