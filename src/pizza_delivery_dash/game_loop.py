from dataclasses import dataclass

import pygame

import pizza_delivery_dash.game
from config import Config
from pizza_delivery_dash.state import State


@dataclass
class GameLoop:
    game: 'pizza_delivery_dash.game.PizzaDeliveryDash'

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.set_state(State.quitting)
            self.handle_event(event)

    def handle_event(self, event: pygame.event.Event) -> None:
        pass

    def set_state(self, new_state: State) -> None:
        self.game.set_state(new_state)

    def loop(self) -> None:
        clock = pygame.time.Clock()
        while self.state != State.quitting:
            self.handle_events()
            self.update_display()
            clock.tick(Config.FPS)

    def update_display(self) -> None:
        current_fps = pygame.time.Clock().get_fps()
        pygame.display.set_caption(f'Current FPS: {current_fps:.0f}')

    @property
    def state(self) -> State:
        return self.game.state

    @property
    def screen(self) -> pygame.Surface | None:
        return self.game.screen

    @property
    def sprites(self) -> dict[str, pygame.Surface]:
        return self.game.sprites
