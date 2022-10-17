#!/usr/bin/env python3
import argparse
import math
from PIL import Image

parser = argparse.ArgumentParser(description='Converts images to dotted ASCII art')
parser.add_argument('image', metavar='IMAGE', type=str, help='the image to convert')
parser.add_argument('--threshold', '-t', type=int, default=90, help='the lightness threshold for writing a dot')
parser.add_argument('--scale', '-s', type=float, default=1.0, help='the scale factor before conversion')
parser.add_argument('--invert', '-i', action='store_true', help='whether or not to invert the output (turn white to black and vice versa)')

args = parser.parse_args()
image_file_name = args.image
THRESHOLD = args.threshold
SCALE = args.scale
INVERT = args.invert

def gray_value(r: int, g: int, b: int) -> int:
    return int((r + g + b) / 3)

def get_character_for_location(size, pixels, x, y) -> chr:
    if x >= size[0] or y >= size[1]:
        gray = 0
    else:
        try:
            r, g, b = pixels[x, y]
        except:
            r, g, b, _ = pixels[x, y]
        gray = gray_value(r, g, b)

    if INVERT:
        return gray < THRESHOLD
    else:
        return gray >= THRESHOLD

image = Image.open(image_file_name)

width, height = image.size
image.thumbnail((width * SCALE, height * SCALE), Image.ANTIALIAS)
pixels = image.load()

width = width * SCALE
height = height * SCALE
output_width = math.ceil(width)
output_height = math.ceil(height)

output = [[' ' for _ in range(0, output_width)] for _ in range(0, output_height)]

for x in range(0, output_width):
    for y in range(0, output_height):
        output[y][x] = get_character_for_location(image.size, pixels, x, y)
