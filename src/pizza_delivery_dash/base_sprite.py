import pygame


class BaseSprite(pygame.sprite.Sprite):
    def __init__(
        self, image: pygame.Surface, z: int, *groups: pygame.sprite.Group
    ) -> None:
        super().__init__(*groups)
        self.image = image
        self.rect = self.image.get_rect()
        self.z = z

    @property
    def x(self) -> int:
        return self.rect.x

    @property
    def y(self) -> int:
        return self.rect.y
