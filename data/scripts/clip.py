import pygame


def clip_surface(surface, x, y, x_size, y_size, colorkey=(0, 0, 0), alpha=255):
    copy_surface = surface.copy()
    clip_rectangle = pygame.Rect(x, y, x_size, y_size)
    copy_surface.set_clip(clip_rectangle)
    image = surface.subsurface(copy_surface.get_clip()).convert()
    return image
