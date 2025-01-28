import os
from dataclasses import dataclass, field

import pygame

from config import Config
from pizza_delivery_dash.base_sprite import BaseSprite
from pizza_delivery_dash.game_loop import GameLoop
from pizza_delivery_dash.player import Player
from pizza_delivery_dash.state import State


def parse_level(level_name: str) -> list[list[str]]:
    cwd = os.getcwd()
    with open(
        os.path.join(cwd, 'src', 'pizza_delivery_dash', 'levels', level_name)
    ) as f:
        data = f.readlines()
    data = list(map(lambda x: x.strip().split(), data))
    return data


class Tile(BaseSprite):
    def __init__(
        self,
        image: pygame.Surface,
        x: int,
        y: int,
        z: int,
        *groups: pygame.sprite.Group,
    ) -> None:
        super().__init__(image, z, *groups)
        self.rect = self.image.get_rect(topleft=(x, y))


@dataclass
class Level(GameLoop):
    level_file_name: str
    parsed_level: list[list[str]] = field(init=False)
    all_level_sprites: pygame.sprite.Group = field(init=False)

    def __post_init__(self) -> None:
        self.parsed_level = parse_level(self.level_file_name)
        tile_size = self.calculate_tile_size()
        self.all_level_sprites = pygame.sprite.Group()
        self.load_tiles(tile_size)
        self.player = Player(
            self.screen.height // Config.TILES_PER_SCREEN_VERT,
            1,
            'player',
            ['player_1', 'player_2', 'player_3'],
            self.all_level_sprites,
        )

    def loop(self) -> None:
        clock = pygame.time.Clock()
        while self.state != State.quitting:
            self.handle_events()
            self.update_display()
            clock.tick(Config.FPS)

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.set_state(State.quitting)
            self.handle_keyboard(pygame.key.get_pressed())
            self.handle_event(event)

    def handle_keyboard(self, pressed: tuple[bool]) -> None:
        if pressed[pygame.K_a]:
            self.player.rect.x -= 10
        elif pressed[pygame.K_d]:
            self.player.rect.x += 10
        elif pressed[pygame.K_w]:
            self.player.rect.y -= 10
        elif pressed[pygame.K_s]:
            self.player.rect.y += 10

    def update_display(self) -> None:
        self.screen.fill(pygame.Color('black'))
        self.draw_tiles()
        self.all_level_sprites.update()
        pygame.display.flip()

    def draw_tiles(self) -> None:
        for sprite in sorted(
            self.all_level_sprites, key=lambda sprite: (sprite.z, sprite.y)
        ):
            self.screen.blit(sprite.image, sprite.rect)

    def load_tiles(self, tile_size: int) -> None:
        tiles_directory = self.get_tiles_directory()
        cache_images = {}

        for y, row in enumerate(self.parsed_level):
            for x, char in enumerate(row):
                if char in cache_images:
                    image = cache_images[char]
                else:
                    image = self.load_tile(char, tiles_directory, tile_size)
                    cache_images[char] = image
                if char.isnumeric() or char == 'g':
                    z = 0
                elif char in ['a', 'b', 'c', 'd', 'i', 'j', 'k', 'l']:
                    z = 2
                else:
                    z = 1
                z = 0 if char.isnumeric() or char == 'g' else 1
                Tile(
                    image,
                    x * tile_size,
                    y * tile_size,
                    z,
                    self.all_level_sprites,
                )

    def calculate_tile_size(self) -> int:
        return round(self.screen.height / Config.TILES_PER_SCREEN_VERT)

    @staticmethod
    def get_tiles_directory() -> str:
        return os.path.join(
            os.getcwd(), 'src', 'pizza_delivery_dash', 'assets', 'tiles'
        )

    @staticmethod
    def load_tile(
        tile_name: str, directory: str, tile_size: int
    ) -> pygame.Surface:
        image_file_name = f'{tile_name}.png'
        loaded_image = pygame.image.load(
            os.path.join(directory, image_file_name)
        )
        scaled_image = pygame.transform.scale(
            loaded_image, (tile_size, tile_size)
        )
        return scaled_image
