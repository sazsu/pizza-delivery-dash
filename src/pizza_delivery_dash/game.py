from dataclasses import dataclass

import pygame

from config import Config
from pizza_delivery_dash.state import State, StateError

WIDTH = Config.WIDTH
HEIGHT = Config.HEIGHT
SCREEN_RECT = pygame.Rect(0, 0, WIDTH, HEIGHT)


@dataclass
class PizzaDeliveryDash:
    screen: pygame.Surface | None
    screen_rect: pygame.Rect
    fullscreen: bool
    state: State

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
        bit_depth = pygame.display.mode_ok(
            self.screen_rect.size, window_style, 32
        )
        screen = pygame.display.set_mode(
            self.screen_rect.size, window_style, bit_depth
        )

        self.screen = screen
        self.state = State.initialized

    def loop(self) -> None:
        pass

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
