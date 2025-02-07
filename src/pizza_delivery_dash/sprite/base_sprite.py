import pygame

from config import Config


class BaseSprite(pygame.sprite.Sprite):
    def __init__(
        self,
        image: pygame.Surface,
        x: float,
        y: float,
        z: int,
        scale: float,
        *groups: pygame.sprite.Group,
    ) -> None:
        super().__init__(*groups)
        self.scale = scale
        self.base_image = image
        self.z = z
        self.absx = x
        self.absy = y
        self.update_scale(scale)

    @property
    def x(self) -> int:
        return round(self.absx * self.scale)

    @property
    def y(self) -> int:
        return round(self.absy * self.scale)

    def update_scale(self, new_scale: float) -> None:
        tile_size = round(new_scale * Config.TILE_SIZE)
        self.scale = new_scale
        self.image = pygame.transform.scale(
            self.base_image, (tile_size, tile_size)
        )
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
