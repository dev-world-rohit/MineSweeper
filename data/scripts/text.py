import pygame
from data.scripts.clip import *
from data.scripts.image_functions import import_image, swap_color, scale_image_ratio


class font:
    def __init__(self, path, color, size_ratio=1):
        self.size_ratio = size_ratio
        self.image = import_image('fonts/' + path, (0, 0, 0))
        self.image = swap_color(self.image, (255, 0, 0), color, (0, 0, 0))
        self.image_size = [self.image.get_width(), self.image.get_height()]
        self.image = scale_image_ratio(self.image, size_ratio)
        self.image_height = self.image.get_height()
        self.character_size = {'A': 3, 'B': 3, 'C': 3, 'D': 3, 'E': 3, 'F': 3, 'G': 3, 'H': 3, 'I': 3, 'J': 3, 'K': 3,
                               'L': 3, 'M': 5,
                               'N': 3, 'O': 3, 'P': 3, 'Q': 3, 'R': 3, 'S': 3, 'T': 3, 'U': 3, 'V': 3, 'W': 5, 'X': 3,
                               'Y': 3, 'Z': 3,
                               'a': 3, 'b': 3, 'c': 3, 'd': 3, 'e': 3, 'f': 3, 'g': 3, 'h': 3, 'i': 3, 'j': 3, 'k': 3,
                               'l': 3, 'm': 5,
                               'n': 3, 'o': 3, 'p': 3, 'q': 3, 'r': 3, 's': 3, 't': 3, 'u': 3, 'v': 3, 'w': 5, 'x': 3,
                               'y': 3, 'z': 3,
                               '.': 1, '-': 3, ',': 2, ':': 1, '+': 3, "'": 1, '!': 1, '?': 3, '0': 3, '1': 3, '2': 3,
                               '3': 3, '4': 3,
                               '5': 3, '6': 3, '7': 3, '8': 3, '9': 3, '(': 2, ')': 2, '/': 3, '_': 5, '=': 3, '\\': 3,
                               '[': 2, ']': 2,
                               '*': 3, '"': 3, '<': 3, '>': 3, ';': 1, ' ': 3}
        self.image_characters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
                                 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
                                 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
                                 'z', '.', '-', ',', ':', '+', "'", '!', '?', '0', '1', '2', '3', '4', '5', '6', '7',
                                 '8', '9', '(', ')', '/', '_', '=', '\\', '[', ']', '*', '"', '<', '>', ';', ' ']
        self.image_character_dict = {}
        self.image_character = 0
        self.image_x = 0
        self.image_x_size = 0

        for pixel in range(0, self.image.get_width()):
            pixel_color = self.image.get_at((pixel, 0))

            if pixel_color == (127, 127, 127):
                if self.image_x_size == 0:
                    continue
                self.image_character_dict[self.image_characters[self.image_character]] = [
                    clip_surface(self.image, pixel - self.image_x_size, 0, self.image_x_size, self.image_height),
                    self.image_x_size]
                self.image_x_size = 0
                self.image_character += 1
                continue
            else:
                self.image_x_size += 1

    def display_fonts(self, surface, string, pos, text_spacing=3):
        for character in string:
            if character == ' ':
                pos[0] += 5 * self.size_ratio
            else:
                surface.blit(self.image_character_dict[character][0], pos)
                pos[0] += self.image_character_dict[character][1] + text_spacing
