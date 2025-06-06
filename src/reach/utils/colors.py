from collections import Counter

import numpy as np
from PIL import Image


def reduce_colors(image_rgb):
    img = Image.fromarray(image_rgb)
    img_8bit = img.convert("P", palette=Image.Palette.ADAPTIVE, colors=256)
    img_8bit_np = np.array(img_8bit)
    return img_8bit_np


def average_color(colors):
    # Initialize sum variables for RGB components
    total_r = total_g = total_b = 0

    # Loop through each RGB color (as tuples or lists)
    for color in colors:
        total_r += color[0]  # Red component
        total_g += color[1]  # Green component
        total_b += color[2]  # Blue component

    # Calculate the average for each component
    num_colors = len(colors)
    avg_r = total_r / num_colors
    avg_g = total_g / num_colors
    avg_b = total_b / num_colors

    # Return the average color as a tuple
    return (int(avg_r), int(avg_g), int(avg_b))


def most_common_pixel(image):
    # Reshape the image to (number_of_pixels, 3) if it's an RGB image
    pixels = image.reshape(-1, 3)

    # Convert rows of RGB values into tuples so they can be counted
    pixel_tuples = [tuple(pixel) for pixel in pixels]

    # Count the frequency of each pixel
    pixel_counts = Counter(pixel_tuples)

    # Find the most common pixel (tuple)
    most_common_pixel = pixel_counts.most_common(1)[0][0]

    return most_common_pixel
