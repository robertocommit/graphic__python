import scipy.misc
import numpy as np
import time
import math
import imageio
from random import randint, sample


def check(x, y):
    if 0 < x < 5000:
        if 0 < y < 2500:
            return True
    return False


def insert_point(image, color, x, y):
    if check(x, y):
        image[y][x][0], image[y][x][1], image[y][x][2] = color[0], color[1], color[2]


def horizontal_line(image, color, x_start, y, length):
    for i in range(0, length):
        insert_point(image, color, x_start + i, y)


def vertical_line(image, color, y_start, x, length):
    for i in range(0, length):
        insert_point(image, color, x, y_start + i)


def diagonal_line(image, color, direction, x, y, length, slope):
    base_length = length / (math.sqrt(1 + (slope * slope)))
    if direction > 0:
        x_new = int(base_length + x)
        while x < x_new:
            insert_point(image, color, int(x), int(y))
            x += 1
            y += slope
    else:
        x_new = int(x - base_length)
        while x > x_new:
            insert_point(image, color, int(x), int(y))
            x -= 1
            y -= slope
    return x_new, y


def sin_horitz(image, color, x, y, length, amplitude, frequency):
    x_final = x + length
    while x < x_final:
        y_double = amplitude * math.sin((frequency * x * math.pi / 180)) * 100 + y
        insert_point(image, color, x, int(y_double))
        x = x + 1


def fourier(image, colors, x, y, length, array_amptitude, array_frequency, corr):
    x_final = x + length
    while x < x_final:
        if check(x, y):
            y_double = array_amptitude[0] * math.sin(array_frequency[0] * x * math.pi / 180) * 100 + y # / array_dividendum[0]
            for r in range(len(array_amptitude)):
                y_double = y_double + array_amptitude[r] * math.sin(array_frequency[r] * x * math.pi / 180) * 100# / array_dividendum[i]
            insert_point(image, colors, x + corr, int(y_double))
        x += 1


def cube(image, cube_width, x_start, y_start, l, d, color):
    for r in range(0, cube_width):
        for q in range(x_start, x_start + l, 1):
            insert_point(image, color, y_start + r, q)  # primo quadrato orizz
            insert_point(image, color, y_start + l + r, q)  # primo quadrato orizz
            insert_point(image, color, y_start - d + r, q + d)  # secondo quadrato orizz
            insert_point(image, color, y_start + l - d + r, q + d)  # secondo quadrato orizz
        for q in range(y_start, y_start + l + cube_width, 1):
            insert_point(image, color, q, x_start + r)  # primo quadrato verticale
            insert_point(image, color, q, x_start + l + r)  # primo quadrato verticale
            insert_point(image, color, q - d, x_start + d + r)  # secondo quadrato verticale
            insert_point(image, color, q - d, x_start + l + d + r)  # secondo quadrato verticale
        for q in range(y_start, y_start - d, -1):
            insert_point(image, color, q + r, x_start + (y_start - q))  # diagonale alto sinistra
            insert_point(image, color, q + l + r, x_start + (y_start - q) + cube_width)  # diagonale basso sinistra
            insert_point(image, color, q + r + cube_width, x_start + l + (y_start - q))  # diagonale alto destra
            insert_point(image, color, q + l + r, x_start + l + (y_start - q) + cube_width)  # diagonale basso destra


def parallepipede(image, x_start, y_start, hight, width, color):
    index = np.full([hight, width], True)
    image[x_start:x_start + hight, y_start:y_start + width][index] = color


def circle(image, radius, ecntre_x, centre_y, colors):
    y, x = np.ogrid[-radius: radius, -radius: radius]
    index = x ** 2 + y ** 2 <= radius ** 2
    image[centre_y - radius:centre_y + radius, centre_x - radius:centre_x + radius][index] = colors


def triangle(image, radius, centre_x, centre_y, colors, direction):
    y, x = np.ogrid[-radius: radius, -radius: radius]
    if direction == 'upper':
        index = x + y < 0
        image[centre_x - radius:centre_x + radius, centre_y - radius:centre_y + radius][index] = colors
    if direction == 'lower':
        index = x + y > 0
        image[centre_x - radius:centre_x + radius, centre_y - radius:centre_y + radius][index] = colors


class Sequence:
    slope = []
    lenght = []

    def __init__(self, max_iter):
        self.slope = [i / 100.0 for i in sample(xrange(140), max_iter)]
        self.length = sample(xrange(200, 500), max_iter)


def generative(image, sequence, counter, max_iter, width, x_start, y_start, color, direction):
    counter += 1
    if counter > max_iter:
        return True
    try:
        for i in range(1, width):
            x_new, y_new = diagonal_line(image, color, direction, x_start, y_start + i, sequence.length[counter], sequence.slope[counter])
        generative(image, sequence, counter, max_iter, width, x_new, y_new - width, color, direction)
    except:
        pass


def diagonal_numpy(image, radius, start_x, start_y, colors, direction):
    index = np.full([radius[0], radius[1]], False)
    np.fill_diagonal(index, True, wrap=True)
    if direction < 0:
        index = np.fliplr(index)
        image[start_x:start_x + radius[0], start_y:start_y + radius[1]][index] = colors
    else:
        image[start_x:start_x + radius[0], start_y:start_y + radius[1]][index] = colors


def main(image):
    for i in range(0, 10):
        sin_horitz(image, [0, 120, 255], 0, 2000 + i, 4000, 1, 1)


if __name__ == '__main__':
    width, height, channels = 5000, 4000, 3
    image = np.zeros((width, height, channels), dtype=np.uint8)
    main(image)
    image = np.flip(image, 0)
    imageio.imwrite('image_output.jpg', image)