import os
import random
from typing import Callable

import pygame
from pygame import Color

from config import Config
from pizza_delivery_dash.scene.scene import Scene
from pizza_delivery_dash.sprite.player import Player
from pizza_delivery_dash.sprite.tile import Tile
from utils import parse_level


class LevelScene(Scene):
    def __init__(
        self,
        level_file_name: str,
        screen: pygame.Surface,
        callback_func: Callable[[int, int], None],
        caption: str = 'Pygame',
        remember: bool = True,
        **options: dict[str, int | Color | str | bool | dict],
    ) -> None:
        super().__init__(screen, caption, remember, **options)
        self.callback_func = callback_func
        self.bg = Color('DarkGray')
        self.level_file_name = level_file_name
        self.map_size: tuple[int, int] = (0, 0)
        self.viewport_xy: tuple[int, int] = (0, 0)
        self.viewport_scale: int = -1
        self.min_viewport_scale: int = -1
        self.tile_size: int = 1
        self.parsed_level = parse_level(self.level_file_name)
        self.all_level_sprites = pygame.sprite.Group()
        self.load_tiles()

    def reset(self) -> None:
        self.viewport_xy = (0, 0)
        self.player.absx = 0
        self.player.absy = 0

    def draw_objects(self) -> None:
        self.update_sprites()
        self.draw_sprites()

    def draw_caption(self) -> None:
        pass

    def draw_animated_objects(self) -> None:
        self.player.update_idle()

    def handle_keyboard(self, pressed: tuple[bool]) -> None:  # noqa C901
        collision_list = [
            sprite
            for sprite in self.all_level_sprites
            if sprite != self.player and sprite.blocking
        ]
        action_list = [
            sprite
            for sprite in self.all_level_sprites
            if sprite != self.player and sprite.action != -1
        ]

        if pressed[pygame.K_ESCAPE]:
            self.callback_func(self.id, -1)

        self.player.moving = False
        player_shift = self.calculate_player_shift(pressed)
        self.player.moving = abs(player_shift[0]) + abs(player_shift[1]) != 0
        if self.player.moving:
            self.player.absx += player_shift[0]
            self.player.absy += player_shift[1]
            self.player.update_scale(self.viewport_scale)  # update rect

            # check if player can move to new coordinates
            is_move_invalid = (
                self.player.rect.collidelist(collision_list) != -1
            )
            is_move_invalid = (
                is_move_invalid
                or self.player.absx < 0
                or self.player.absy < 0
                or self.player.absx >= self.map_size[0] - 1
                or self.player.absy >= self.map_size[1] - 1
            )
            if is_move_invalid:
                self.player.absx -= player_shift[0]
                self.player.absy -= player_shift[1]
                self.player.moving = False

            if self.player.moving:
                action_object_index = self.player.rect.collidelist(action_list)
                self.handle_place_interaction(action_object_index, action_list)

        zoom_change = 0
        if pressed[pygame.K_i]:
            zoom_change += 1
        if pressed[pygame.K_o]:
            zoom_change -= 1
        self.viewport_scale += zoom_change
        zoom_changed = False
        if self.viewport_scale < self.min_viewport_scale:
            self.viewport_scale = self.min_viewport_scale
            zoom_changed = True
        elif self.viewport_scale > 16:
            self.viewport_scale = 16
            zoom_changed = True
        else:
            zoom_changed = zoom_change != 0
        if zoom_changed:
            # self.load_tiles(reset_map_scale=False)
            self.update_objects_scale()
        viewport_shift = round(4 * self.viewport_scale)
        (x, y) = self.viewport_xy

        diff_x, diff_y = 0, 0
        boundary_limit = 64

        boundary_rect = (
            self.player.absx * self.viewport_scale - x,
            x
            + self.screen.width
            - (
                self.player.absx * self.viewport_scale + self.player.rect.width
            ),
            self.player.absy * self.viewport_scale - y,
            y
            + self.screen.height
            - (
                self.player.absy * self.viewport_scale
                + self.player.rect.height
            ),
        )

        if pressed[pygame.K_RIGHT] or boundary_rect[1] < boundary_limit:
            diff_x = 1
        if pressed[pygame.K_LEFT] or boundary_rect[0] < boundary_limit:
            diff_x = -1
        if pressed[pygame.K_DOWN] or boundary_rect[3] < boundary_limit:
            diff_y = 1
        if pressed[pygame.K_UP] or boundary_rect[2] < boundary_limit:
            diff_y = -1
        # todo: scroll viewport when player reaches bounds
        x += diff_x * viewport_shift
        y += diff_y * viewport_shift
        if x < 0:
            x = 0
        if y < 0:
            y = 0
        if x + self.screen.width > self.map_size[0] * self.viewport_scale:
            x = self.map_size[0] * self.viewport_scale - self.screen.width
        if y + self.screen.height > self.map_size[1] * self.viewport_scale:
            y = self.map_size[1] * self.viewport_scale - self.screen.height
        viewport_changed = x != self.viewport_xy[0] or y != self.viewport_xy[1]
        self.viewport_xy = (x, y)
        self.game_display_changed = (
            self.player.moving or viewport_changed or zoom_changed
        )

    def update_sprites(self) -> None:
        self.all_level_sprites.update()

    def draw_sprites(self) -> None:
        for sprite in sorted(
            self.all_level_sprites,
            key=lambda sprite: (sprite.z),  # , sprite.y)
        ):
            # self.screen.blit(sprite.image, sprite.rect)
            top_left = (
                round(sprite.x - self.viewport_xy[0]),
                round(sprite.y - self.viewport_xy[1]),
            )
            self.screen.blit(
                sprite.image, sprite.image.get_rect(topleft=top_left)
            )

    def handle_place_interaction(
        self, action_object_index: int, action_list: list[Tile]
    ) -> None:
        if action_object_index != -1:
            action_id = action_list[action_object_index].action
            if action_id == 1:
                self.callback_func(self.id, 0)
            elif action_id == 2:
                self.callback_func(self.id, 1)
            elif action_id == 3:
                self.callback_func(self.id, 2)

    def update_objects_scale(self) -> None:
        for item in self.all_level_sprites:
            item.update_scale(self.viewport_scale)

    def load_tiles(self) -> None:
        tiles_directory = self.get_tiles_directory()
        cache_images = {}
        map_width = len(self.parsed_level[0]) * Config.TILE_SIZE
        map_height = len(self.parsed_level) * Config.TILE_SIZE
        self.map_size = (map_width, map_height)
        self.min_viewport_scale = self.calculate_min_viewport_scale(
            map_width, map_height
        )
        self.viewport_scale = self.min_viewport_scale
        self.viewport_xy = (0, 0)
        player_x = 0  # TODO: randomize player coordinates (from a list)
        player_y = 0

        for y, row in enumerate(self.parsed_level):
            for x, tile_property in enumerate(row):
                tile_properties = tile_property.split('/')
                char = tile_properties[0]
                blocking = False
                action = -1
                prop_count = len(tile_properties)
                if prop_count == 2:
                    if tile_properties[1].startswith('b'):
                        blocking = True
                    if tile_properties[1].startswith('a'):
                        action = int(tile_properties[1].strip('a'))
                if char in cache_images:
                    image = cache_images[char]
                else:
                    image = self.load_tile(
                        char, tiles_directory
                    )  # , self.tile_size)
                    cache_images[char] = image
                if char in ['tr', 'lp']:
                    do_mirror = bool(random.randint(0, 1))
                    if do_mirror:
                        image = pygame.transform.flip(image, True, False)
                z = self.get_z_index(char)
                Tile(
                    image,
                    x * image.width,  # assume w==h==Config>TILE_SIZE
                    y * image.height,
                    z,
                    self.viewport_scale,
                    self.all_level_sprites,
                    blocking=blocking,
                    action=action,
                )
        self.player = Player(
            player_x,
            player_y,
            5,
            self.viewport_scale,
            'player',
            ['player_1', 'player_2', 'player_3'],
            Config.PLAYER_VELOCITY,
            self.all_level_sprites,
        )

    def calculate_min_viewport_scale(
        self, map_width: int, map_height: int
    ) -> int:
        n_x = self.screen.width / map_width
        n_y = self.screen.height / map_height
        return round(max(n_x, n_y)) + 1

    def calculate_player_shift(self, pressed: tuple[bool]) -> list[int]:
        player_shift = [0, 0]
        if pressed[pygame.K_a]:
            player_shift[0] -= self.player.velocity
        if pressed[pygame.K_d]:
            player_shift[0] += self.player.velocity
        if pressed[pygame.K_w]:
            player_shift[1] -= self.player.velocity
        if pressed[pygame.K_s]:
            player_shift[1] += self.player.velocity
        if pressed[pygame.K_LSHIFT]:
            player_shift[0] *= 2
            player_shift[1] *= 2
        return player_shift

    @staticmethod
    def get_z_index(char: str) -> int:
        if char.isnumeric() or char == 'g':
            z = 0
        elif char in Config.BUILDING_LAYER:
            z = 10
        else:
            z = 1
        return z

    @staticmethod
    def get_tiles_directory() -> str:
        return os.path.join(
            os.getcwd(),
            'src',
            'pizza_delivery_dash',
            'assets',
            'tiles',
            # os.getcwd(), 'pizza_delivery_dash', 'assets', 'tiles'
        )

    @staticmethod
    def load_tile(tile_name: str, directory: str) -> pygame.Surface:
        image_file_name = f'{tile_name}.png'
        loaded_image = pygame.image.load(
            os.path.join(directory, image_file_name)
        )
        return loaded_image
