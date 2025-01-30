import pygame

from pizza_delivery_dash.base_sprite import BaseSprite


class Tile(BaseSprite):
    def __init__(
        self,
        image: pygame.Surface,
        x: int,
        y: int,
        z: int,
        *groups: pygame.sprite.Group,
    ) -> None:
        super().__init__(image, z, *groups)
        self.rect = self.image.get_rect(topleft=(x, y))
