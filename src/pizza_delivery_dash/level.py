import os
from dataclasses import dataclass, field

import pygame

from config import Config
from pizza_delivery_dash.game_loop import GameLoop
from pizza_delivery_dash.player import Player
from pizza_delivery_dash.state import State
from pizza_delivery_dash.tile import Tile
from utils import parse_level


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
            5,
            self.all_level_sprites,
        )

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.set_state(State.quitting)
            self.handle_keyboard(pygame.key.get_pressed())
            self.handle_event(event)

    def update_display(self) -> None:
        self.fill_bg()
        self.draw_sprites()
        self.update_sprites()
        pygame.display.flip()

    def handle_keyboard(self, pressed: tuple[bool]) -> None:
        self.player.moving = False
        if pressed[pygame.K_a]:
            self.player.rect.x -= self.player.velocity
            self.player.moving = True
        if pressed[pygame.K_d]:
            self.player.rect.x += self.player.velocity
            self.player.moving = True
        if pressed[pygame.K_w]:
            self.player.rect.y -= self.player.velocity
            self.player.moving = True
        if pressed[pygame.K_s]:
            self.player.rect.y += self.player.velocity
            self.player.moving = True

    def fill_bg(self) -> None:
        self.screen.fill(pygame.Color('black'))

    def update_sprites(self) -> None:
        self.all_level_sprites.update()

    def draw_sprites(self) -> None:
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
                z = self.get_z_index(char)
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
    def get_z_index(char: str) -> int:
        if char.isnumeric() or char == 'g':
            z = 0
        elif char in Config.BUILDING_LAYER:
            z = 2
        else:
            z = 1
        return z

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
