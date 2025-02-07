from typing import Callable

import pygame
from pygame import Color

from pizza_delivery_dash.buttons import Button
from pizza_delivery_dash.scene.scene import Scene


class MainMenuScene(Scene):
    def __init__(
        self,
        screen: pygame.Surface,
        callback_func: Callable[[int, int], None],
        caption: str = 'Pygame',
        remember: bool = True,
        **options: dict[str, int | Color | str | bool | dict],
    ) -> None:
        super().__init__(screen, caption, remember, **options)
        self.callback_func = callback_func
        self.bg = Color('LightGray')
        self.buttons_sprites_group = self.create_buttons()

    def draw_objects(self) -> None:
        self.buttons_sprites_group.draw(self.screen)

    def handle_keyboard(self, pressed: tuple[bool]) -> None:
        if pressed[pygame.K_ESCAPE]:
            self.callback_func(self.id, -1)

    def handle_event(self, event: pygame.event.Event) -> None:
        super().handle_event(event)
        if event.type == pygame.MOUSEBUTTONUP:
            self.handle_mouse_click()

    def handle_mouse_click(self) -> None:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        clicked_button = self.get_clicked_button(mouse_x, mouse_y)
        if clicked_button:
            self.button_callback(clicked_button.button_code)

    def enter_level(self, level_id: int) -> None:
        self.callback_func(self.id, 0)

    def get_clicked_button(self, mouse_x: int, mouse_y: int) -> Button | None:
        for button in self.buttons_sprites_group:
            if button.rect.collidepoint(mouse_x, mouse_y):
                return button
        return None

    def check_mouse_hit_level_button(self, mouse_x: int, mouse_y: int) -> bool:
        return any(
            button.rect.collidepoint(mouse_x, mouse_y)
            for button in self.buttons_sprites_group
        )

    def button_callback(self, button_code: int) -> None:
        if button_code == 0:  # start level 0
            self.enter_level(0)
        elif button_code == 1:  # show statistics
            self.callback_func(self.id, 1)
        elif button_code == 2:  # show statistics
            self.callback_func(self.id, -1)

    def create_buttons(self) -> pygame.sprite.Group:
        sprites_group = pygame.sprite.Group()

        buttons_text = ['Play', 'Stats', 'Leave']
        width, button_height = self.calculate_button_dimensions()
        spacing, left_margin, top_margin = self.calculate_button_offsets(
            width, button_height, len(buttons_text)
        )
        for i in range(len(buttons_text)):
            x = left_margin + width * i + spacing * i
            y = top_margin
            x, y = self.calculate_button_position(
                left_margin, top_margin, width, spacing, i
            )
            Button(
                x,
                y,
                width,
                button_height,
                pygame.Color('white'),
                i,
                buttons_text[i],
                sprites_group,
            )
        return sprites_group

    def calculate_button_dimensions(self) -> tuple[int, int]:
        return self.screen.width // 5, self.screen.height // 8

    def calculate_button_offsets(
        self, button_width: int, button_height: int, button_count: int
    ) -> tuple[int, int, int]:
        horizontal_spacing = button_width // 2
        left_margin = (
            self.screen.width
            - button_width * button_count
            - horizontal_spacing * 2
        ) // 2
        top_margin = (self.screen.height - button_height) // 2
        return horizontal_spacing, left_margin, top_margin

    @staticmethod
    def calculate_button_position(
        left_margin: int, top_margin: int, width: int, spacing: int, i: int
    ) -> tuple[int, int]:
        x = left_margin + width * i + spacing * i
        y = top_margin
        return x, y
