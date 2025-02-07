from typing import Callable

import pygame
from pygame import Color

from pizza_delivery_dash.buttons import Button
from pizza_delivery_dash.scene.scene_mainmenu import MainMenuScene


class ConfirmationScene(MainMenuScene):
    def __init__(
        self,
        screen: pygame.Surface,
        callback_func: Callable[[int, int], None],
        caption: str = 'Pygame',
        remember: bool = True,
        **options: dict[str, int | Color | str | bool | dict],
    ) -> None:
        super().__init__(screen, callback_func, caption, remember, **options)
        self.buttons_sprites_group = self.create_buttons()

    def handle_keyboard(self, pressed: tuple[bool]) -> None:
        if pressed[pygame.K_ESCAPE]:
            self.callback_func(self.id, -1)
        elif pressed[pygame.K_END]:
            self.callback_func(self.id, 0)

    def handle_mouse_click(self) -> None:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        clicked_button = self.get_clicked_button(mouse_x, mouse_y)
        if clicked_button:
            self.button_callback(clicked_button.button_code)

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
        if button_code == 0:  # back to main menu
            self.callback_func(self.id, -1)
        elif button_code == 1:  # exit game
            self.callback_func(self.id, 0)

    def create_buttons(self) -> pygame.sprite.Group:
        sprites_group = pygame.sprite.Group()
        buttons_text = ['Go back to menu', 'Leave']
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
