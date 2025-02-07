import pygame

from pizza_delivery_dash.buttons import Button


class FoodItem(Button):
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        image: pygame.Surface,
        *groups: pygame.sprite.Group,
    ) -> None:
        super().__init__(
            x, y, width, height, pygame.color.Color('black'), 0, '', *groups
        )
        self.regular_image: pygame.Surface = pygame.transform.scale(
            image, (width, height)
        )
        self.image = self.regular_image
        self.make_crossed_out()
        self.make_checked()
        self.crossed_out: bool = False
        self.possible_to_move: bool = True

    def cross_out(self) -> None:
        self.image = self.crossed_out_image
        self.crossed_out = True

    def make_crossed_out(self) -> None:
        x, y, width, height = self.get_dimensions()
        surface = pygame.surface.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.line(
            surface,
            pygame.Color('red'),
            (x, y),
            (x + width, y + height),
            width=3,
        )
        pygame.draw.line(
            surface,
            pygame.Color('red'),
            (x + width, y),
            (x, y + height),
            width=3,
        )
        self.crossed_out_image = self.regular_image.copy()
        self.crossed_out_image.blit(surface, (0, 0))

    def check(self) -> None:
        self.image = self.checked_image

    def make_checked(self) -> None:
        x, y, width, height = self.get_dimensions()
        surface = pygame.surface.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.line(
            surface,
            pygame.Color('green'),
            (int(x * 0.15), y + height // 2),
            (x + width // 2, y + int(height * 0.85)),
            width=3,
        )
        pygame.draw.line(
            surface,
            pygame.Color('green'),
            (x + width // 2, y + int(height * 0.85)),
            (x + width, y),
            width=3,
        )
        self.checked_image = self.regular_image.copy()
        self.checked_image.blit(surface, (0, 0))

    def get_dimensions(self) -> tuple[int, int, int, int]:
        image_rect = self.image.get_rect()
        width, height = self.image.size
        x, y = image_rect.x, image_rect.y
        return x, y, width, height
