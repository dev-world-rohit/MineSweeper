import pygame
from data.scripts.image_functions import import_image, scale_image_ratio
from data.scripts.clip import clip_surface


def extract_images(size_ratio):
    images = import_image('minesweeper.png', (255, 255, 255))
    images_names = ['mine', 'mine_2', 'flag', 'spark', 'hiding_tile', 'frame', '1', '2', '3', '4', '5', '6', '7', '8',
                    '0']
    images_hash = {}
    image_width = images.get_width()
    image_height = images.get_height()

    total_images = image_width // image_height

    for i in range(total_images):
        start_x = i * 16
        end_x = (i + 1) * 16
        images_hash[images_names[i]] = scale_image_ratio(clip_surface(images, start_x, 0, 16, 16, (255, 255, 255)),
                                                         size_ratio)

    return images_hash
