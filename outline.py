import sys
import math
from PIL import Image


def outline(img):
    image = Image.open(img)
    out = Image.new("I", image.size, 0xffffff)
    width, height = image.size
    for x in range(1, width):
        for y in range(1, height):
            r1, g1, b1 = image.getpixel((x, y))
            r2, g2, b2 = image.getpixel((x - 1, y - 1))
            diff = math.sqrt((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2)
            if diff > 5:
                out.putpixel((x, y), 0)
    out.save(img)


if __name__ == "__main__":
    image_path = sys.argv[1]
    outline(image_path)
