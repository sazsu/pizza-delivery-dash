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

    def handle_event(self, event: pygame.Event) -> None:
        pass

    def set_state(self, new_state: State) -> None:
        self.game.set_state(new_state)

    def loop(self) -> None:
        clock = pygame.Clock()
        while self.state != State.quitting:
            current_fps = clock.get_fps()
            pygame.display.set_caption(f'Current FPS: {current_fps:.0f}')
            clock.tick(Config.FPS)
            self.handle_events()

    def load_background_image(self, image_name: str) -> None:
        self.screen.blit(self.sprites[image_name])

    @property
    def state(self) -> State:
        return self.game.state

    @property
    def screen(self) -> pygame.Surface | None:
        return self.game.screen

    @property
    def sprites(self) -> dict[str, pygame.Surface]:
        return self.game.sprites
