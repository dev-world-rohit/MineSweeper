import pygame
from data.scripts.image_functions import import_image
from data.scripts.text import font


class ScoreBoard:
    def __init__(self, screen):
        self.time = 0
        self.screen = screen
        self.items = 2
        self.item_width = 40
        self.offset = 10
        self.flag_image = import_image('flag_post.png', (0, 0, 0))
        self.time_post = import_image('time_post.png')
        self.text = font('small_font.png', (10, 10, 10), 4)
        self.position = ((self.screen.get_width() - self.flag_image.get_width()) // 2, (
                self.screen.get_height() -
                (self.flag_image.get_height() * self.items + (self.items - 1) * self.offset)) // 2)

    def display_flags(self, flags):
        self.screen.blit(self.flag_image, self.position)
        self.text.display_fonts(self.screen, str(flags) if flags == 10 else "0" + str(flags),
                                [self.position[0] + 35, self.position[1] + 5])

    def display_time(self, time):
        self.screen.blit(self.time_post, (self.position[0], self.position[1] + self.item_width + self.offset))
        self.text.display_fonts(self.screen, str(time // 1000),
                                [self.position[0] + 15, self.position[1] + self.item_width + self.offset + 5])
