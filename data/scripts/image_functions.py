import pygame


def import_image(path, colorkey=(0, 0, 0), alpha=255):
    img = pygame.image.load('data/images/' + path).convert()
    img.set_colorkey(colorkey)
    img.set_alpha(alpha)
    return img.copy()


def scale_image_size(img, size):
    img = pygame.transform.scale(img, size)
    return img.copy()


def scale_image_ratio(img, ratio=1):
    img_size = [img.get_width(), img.get_height()]
    img = pygame.transform.scale(
            img, (int(img_size[0] * ratio), int(img_size[1] * ratio)))
    return img.copy()


def rotate_image(img, angle):
    img = pygame.transform.rotate(img, angle)
    return img.copy()


def flip_image(img, flip_horizontal=False, flip_verticle=False):
    img = pygame.transform.flip(img, flip_horizontal, flip_verticle)
    return img.copy()


def swap_color(image, old_color, new_color, colorkey):
    image.set_colorkey(old_color)
    surface = image.copy()
    surface.fill(new_color)
    surface.blit(image, (0, 0))
    surface.set_colorkey(colorkey)
    return surface.copy()


def blit_centre(surface, img, pos):
    pos_x = pos[0] - img.get_width() // 2
    pos_y = pos[1] - img.get_height() // 2
    surface.blit(img, (pos_x, pos_y))
