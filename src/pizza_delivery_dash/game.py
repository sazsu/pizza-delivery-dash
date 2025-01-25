from dataclasses import dataclass, field

import pygame

from config import Config
from pizza_delivery_dash.main_menu import MainMenu
from pizza_delivery_dash.state import State, StateError
from utils import load_image

WIDTH = Config.WIDTH
HEIGHT = Config.HEIGHT
SCREEN_RECT = pygame.Rect(0, 0, WIDTH, HEIGHT)


@dataclass
class PizzaDeliveryDash:
    screen: pygame.Surface | None
    screen_rect: pygame.Rect
    fullscreen: bool
    state: State
    game_loop: 'MainMenu' = field(init=False)

    @classmethod
    def create(cls, fullscreen: bool = True) -> 'PizzaDeliveryDash':
        game = cls(
            screen=None,
            screen_rect=SCREEN_RECT,
            fullscreen=fullscreen,
            state=State.initializing,
        )
        game.init()

        return game

    def init(self) -> None:
        pygame.init()

        window_style = pygame.FULLSCREEN if self.fullscreen else 0

        if self.fullscreen:
            self.update_screen_rect()

        bit_depth = pygame.display.mode_ok(
            self.screen_rect.size, window_style, 32
        )
        screen = pygame.display.set_mode(
            self.screen_rect.size, window_style, bit_depth
        )

        self.screen = screen
        self.state = State.initialized

    def loop(self) -> None:
        self.game_loop = MainMenu(self)
        self.game_loop.loop()

    def quit(self) -> None:
        pass

    def start_game(self) -> None:
        self.assert_state_is(State.initialized)
        self.set_state(State.main_menu)
        self.loop()

    def assert_state_is(self, target_state: State) -> None:
        if self.state != target_state:
            raise StateError(
                f'Expected state to be {target_state}, got {self.state}'
            )

    def set_state(self, new_state: State) -> None:
        self.state = new_state

    def update_screen_rect(self) -> None:
        display_info = pygame.display.Info()
        self.screen_rect.size = (
            display_info.current_w,
            display_info.current_h,
        )

    def load_sprites(self) -> None:
        self.sprites = {}

        for human_readable_name, file_name in Config.sprites.items():
            image = load_image(file_name)
            self.sprites[human_readable_name] = image
