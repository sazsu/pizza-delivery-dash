import pygame


class Button(pygame.sprite.Sprite):
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        color: pygame.Color,
        *groups: pygame.sprite.Group,
    ) -> None:
        super().__init__(*groups)
        self.image = pygame.Surface((width, height))
        pygame.draw.rect(self.image, color, (0, 0, width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.color = color


class LevelButton(Button):
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        color: pygame.Color,
        level_id: int,
        *groups: pygame.sprite.Group,
    ) -> None:
        super().__init__(x, y, width, height, color, *groups)
        self.level_id: int = level_id
