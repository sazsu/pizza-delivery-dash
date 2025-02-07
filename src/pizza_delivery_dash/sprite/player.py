import time

import pygame

from pizza_delivery_dash.sprite.animated_sprite import AnimatedSprite


class Player(AnimatedSprite):
    def __init__(
        self,
        x: float,
        y: float,
        z: int,
        scale: float,
        subdir: str,
        file_names: list[str],
        velocity: int,
        *groups: pygame.sprite.Group,
    ) -> None:
        super().__init__(x, y, z, scale, subdir, file_names, *groups)
        self.velocity = velocity
        self.moving = False

    def update(self) -> None:
        if self.moving:
            super().update()
            self.last_update_time = time.time()
            self.moving = False

    def update_idle(self) -> None:
        super().update()
