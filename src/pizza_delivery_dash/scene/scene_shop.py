import os
import random
from typing import Callable

import pygame
from pygame import Color

from pizza_delivery_dash.app import App
from pizza_delivery_dash.food_item import FoodItem
from pizza_delivery_dash.scene.scene import Scene


class ShopScene(Scene):
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
        self.bg = Color('Brown')
        self.map_size = (16, 9)
        self.tile_size = self.calculate_tile_size()
        self.floor_tiles_group = pygame.sprite.Group()
        self.buttons_group = pygame.sprite.Group()
        self.load_floor_tiles()
        self.load_food_images()
        self.load_food_items()

    def reset(self) -> None:
        self.buttons_group.empty()
        self.load_food_items()

    def enter(self, app: App | None = None) -> None:
        if app:
            app.shop_visited = True
        super().enter(app)

    def handle_keyboard(self, pressed: tuple[bool]) -> None:
        if pressed[pygame.K_ESCAPE]:
            self.callback_func(self.id, -1)

    def handle_event(self, event: pygame.event.Event) -> None:
        super().handle_event(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_mouse_click()

    def handle_mouse_click(self) -> None:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for food_item in self.buttons_group:
            if (
                food_item.rect.collidepoint(mouse_x, mouse_y)
                and food_item.crossed_out is False
            ):
                self.inventory.append(food_item)
                food_item.check()

    def load_floor_tiles(self) -> None:
        assets_dir = self.get_assets_directory()
        floor_tile = self.load_floor_tile('shop_floor_tile', assets_dir)
        cols, rows = self.map_size
        for r in range(rows):
            for c in range(cols):
                FloorTile(
                    c * self.tile_size,
                    r * self.tile_size,
                    self.tile_size,
                    self.tile_size,
                    floor_tile,
                    self.floor_tiles_group,
                )

    def load_food_items(self) -> None:
        button_size = self.tile_size // 2
        button_offset = self.tile_size // 4
        images = list(self.surface_to_image_name.keys())

        for r in range(3, 6):
            for c in range(5, 11):
                image = random.choice(images)

                FoodItem(
                    c * self.tile_size + button_offset,
                    r * self.tile_size + button_offset,
                    button_size,
                    button_size,
                    image,
                    self.buttons_group,
                )

    def draw_objects(self) -> None:
        self.fill_bg()
        self.draw_sprites()

    def fill_bg(self) -> None:
        self.screen.fill(pygame.color.Color('black'))

    def draw_sprites(self) -> None:
        self.floor_tiles_group.draw(self.screen)
        self.buttons_group.draw(self.screen)

    def calculate_tile_size(self) -> int:
        return round(
            max(
                self.screen.width / self.map_size[0],
                self.screen.height / self.map_size[1],
            )
        )

    @staticmethod
    def get_assets_directory(subdir: str = '') -> str:
        return os.path.join(
            os.getcwd(),
            'src',
            'pizza_delivery_dash',
            'assets',
            subdir,
        )

    def load_food_images(self) -> None:
        self.surface_to_image_name = {}
        food_dir = self.get_assets_directory(subdir='store food')
        for img_name in os.listdir(food_dir):
            loaded_image = self.load_food_item(img_name, food_dir)
            self.surface_to_image_name[loaded_image] = img_name

    @staticmethod
    def load_food_item(image_name: str, directory: str) -> pygame.Surface:
        image_file_name = image_name
        loaded_image = pygame.image.load(
            os.path.join(directory, image_file_name)
        )
        color_key = loaded_image.get_at((0, 0))
        loaded_image.set_colorkey(color_key)
        return loaded_image

    def load_floor_tile(
        self, image_name: str, directory: str
    ) -> pygame.Surface:
        image_file_name = f'{image_name}.png'
        loaded_image = pygame.image.load(
            os.path.join(directory, image_file_name)
        )
        return pygame.transform.scale(
            loaded_image, (self.tile_size, self.tile_size)
        )


class FloorTile(pygame.sprite.Sprite):
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        image: pygame.surface.Surface,
        *groups: pygame.sprite.Group,
    ) -> None:
        super().__init__(*groups)
        self.image = image
        self.rect = pygame.rect.Rect(x, y, width, height)
