import pygame

from pizza_delivery_dash.sprite.base_sprite import BaseSprite


class Tile(BaseSprite):
    def __init__(
        self,
        image: pygame.Surface,
        x: float,
        y: float,
        z: int,
        scale: float,
        *groups: pygame.sprite.Group,
        blocking: bool = False,
        action: int = -1,
    ) -> None:
        super().__init__(image, x, y, z, scale, *groups)
        self.blocking = blocking
        self.action = action
