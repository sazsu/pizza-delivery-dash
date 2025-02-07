import pygame
from pygame import Color


class Button(pygame.sprite.Sprite):
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        color: pygame.Color,
        button_code: int,
        button_text: str,
        *groups: pygame.sprite.Group,
    ) -> None:
        super().__init__(*groups)
        self.image = pygame.Surface((width, height))

        self.color = color
        self.button_code = button_code
        self.button_text = button_text
        pygame.draw.rect(self.image, color, (0, 0, width, height))
        # draw text
        self.font = pygame.font.Font(None, size=24)
        img = self.font.render(
            self.button_text, True, Color('black'), self.color
        )
        self.image.blit(img, (x // 16, y // 8))
        self.rect = self.image.get_rect(topleft=(x, y))
