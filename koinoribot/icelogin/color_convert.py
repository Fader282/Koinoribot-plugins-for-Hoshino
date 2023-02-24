from skimage import color
import numpy as np


def lab2rgb(lightness, a, b) -> tuple:
    lab = np.array([lightness, a, b], dtype=float)

    value = list(color.lab2rgb(lab))
    red = int(value[0] * 255)
    green = int(value[1] * 255)
    blue = int(value[2] * 255)
    rgb = (red, green, blue)
    return rgb