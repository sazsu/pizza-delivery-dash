import os

import pygame


def load_image(
    name: str, colorkey: None | int | pygame.Color = None
) -> pygame.Surface:
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        raise FileNotFoundError(f'Cannot find image file with the name {name}')

    image = pygame.image.load(fullname)

    if colorkey is not None:
        image = set_colorkey(image, colorkey)
    else:
        image = convert_alpha(image)
    return image


def set_colorkey(
    image: pygame.Surface, colorkey: int | pygame.Color
) -> pygame.Surface:
    image = image.convert()
    if colorkey == -1:
        colorkey = image.get_at((0, 0))
    image.set_colorkey(colorkey)
    return image


def convert_alpha(image: pygame.Surface) -> pygame.Surface:
    return image.convert_alpha()
