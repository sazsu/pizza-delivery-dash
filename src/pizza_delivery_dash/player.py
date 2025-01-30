import pygame

from pizza_delivery_dash.animated_sprite import AnimatedSprite


class Player(AnimatedSprite):
    def __init__(
        self,
        size: int,
        z: int,
        subdir: str,
        file_names: list[str],
        velocity: int,
        *groups: pygame.sprite.Group,
    ) -> None:
        super().__init__(size, z, subdir, file_names, *groups)
        self.velocity = velocity
        self.moving = False

    def update(self) -> None:
        if self.moving:
            self.current_frame = self.get_new_frame()
        else:
            self.current_frame = 0
        self.image = self.frames[self.current_frame]
