from dataclasses import dataclass

import pygame

from config import Config
from pizza_delivery_dash.buttons import LevelButton
from pizza_delivery_dash.game_loop import GameLoop
from pizza_delivery_dash.level import Level
from pizza_delivery_dash.state import State


@dataclass
class MainMenu(GameLoop):
    def __post_init__(self) -> None:
        self.buttons_sprites_group = self.create_level_buttons()

    def loop(self) -> None:
        clock = pygame.Clock()
        while self.state != State.quitting:
            self.handle_events()
            self.update_display()
            clock.tick(Config.FPS)

    def update_display(self) -> None:
        self.buttons_sprites_group.draw(self.screen)
        pygame.display.flip()

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.set_state(State.quitting)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.handle_mouse_click()

    def handle_mouse_click(self) -> None:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        # if self.check_mouse_hit_level_button(mouse_x, mouse_y):
        clicked_button = self.get_clicked_button(mouse_x, mouse_y)
        if clicked_button:
            self.enter_level(clicked_button.level_id)

    def enter_level(self, level_id: int) -> None:
        # level = self.game.levels[coords]
        # level.loop()
        print(f'Level with id {level_id} entered')
        Level(self.game, 'level1.txt').loop()

    def get_clicked_button(
        self, mouse_x: int, mouse_y: int
    ) -> LevelButton | None:
        for button in self.buttons_sprites_group:
            if button.rect.collidepoint(mouse_x, mouse_y):
                return button
        return None

    def check_mouse_hit_level_button(self, mouse_x: int, mouse_y: int) -> bool:
        return any(
            button.rect.collidepoint(mouse_x, mouse_y)
            for button in self.buttons_sprites_group
        )

    def create_level_buttons(self) -> pygame.sprite.Group:
        sprites_group = pygame.sprite.Group()

        width, button_height = self.calculate_button_dimensions()
        spacing, left_margin, top_margin = self.calculate_button_offsets(
            width, button_height
        )

        for i in range(3):
            x = left_margin + width * i + spacing * i
            y = top_margin
            x, y = self.calcualte_button_position(
                left_margin, top_margin, width, spacing, i
            )
            self.create_button(
                x,
                y,
                width,
                button_height,
                pygame.Color('white'),
                i,
                sprites_group,
            )
        return sprites_group

    @staticmethod
    def create_button(
        x: int,
        y: int,
        width: int,
        height: int,
        color: pygame.Color,
        level_id: int,
        sprites_group: pygame.sprite.Group,
    ) -> None:
        LevelButton(x, y, width, height, color, level_id, sprites_group)

    def calculate_button_dimensions(self) -> tuple[int, int]:
        return self.screen.width // 5, self.screen.height // 8

    def calculate_button_offsets(
        self, button_width: int, button_height: int
    ) -> tuple[int, int, int]:
        horizontal_spacing = button_width // 2
        left_margin = (
            self.screen.width - button_width * 3 - horizontal_spacing * 2
        ) // 2
        top_margin = (self.screen.height - button_height) // 2
        return horizontal_spacing, left_margin, top_margin

    @staticmethod
    def calcualte_button_position(
        left_margin: int, top_margin: int, width: int, spacing: int, i: int
    ) -> tuple[int, int]:
        x = left_margin + width * i + spacing * i
        y = top_margin
        return x, y
