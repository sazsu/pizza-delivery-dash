import pygame

from pizza_delivery_dash.animated_sprite import AnimatedSprite


class Player(AnimatedSprite):
    def __init__(
        self,
        size: int,
        z: int,
        subdir: str,
        file_names: list[str],
        *groups: pygame.sprite.Group,
    ) -> None:
        super().__init__(size, z, subdir, file_names, *groups)
