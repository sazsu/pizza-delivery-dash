import math
import os
from typing import Callable

import pygame
from pygame import Color

from pizza_delivery_dash.app import App
from pizza_delivery_dash.food_item import FoodItem
from pizza_delivery_dash.scene.scene import Scene


class PizzeriaScene(Scene):
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
        self.bg = Color('Yellow')
        self.food_item_holding: FoodItem | None = None
        self.load_pizza_dough_bg()
        self.pizza_radius: int = int(self.screen.height * 0.425)

    def reset(self) -> None:
        self.load_sprites()

    def load_pizza_dough_bg(self) -> None:
        assets_dir = os.path.join(
            os.getcwd(), 'src', 'pizza_delivery_dash', 'assets'
        )

        pizza_dough: pygame.Surface = pygame.image.load(
            os.path.join(assets_dir, 'pizza_dough.png')
        )
        self.pizza_dough: pygame.Surface = pygame.transform.scale(
            pizza_dough, self.screen.size
        )

    def draw_bg(self) -> None:
        self.screen.blit(self.pizza_dough)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            self.handle_keyboard(pygame.key.get_pressed())
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_mouse_click()
        elif event.type == pygame.MOUSEMOTION:
            self.handle_mouse_motion()

    def enter(self, app: App | None = None) -> None:
        if app:
            app.pizzeria_visited = True
        self.load_sprites()
        super().enter(app)

    def load_sprites(self) -> None:
        self.sprites = pygame.sprite.Group()
        for food_item in self.inventory:
            if food_item.possible_to_move:
                food_item.image = pygame.transform.scale2x(
                    food_item.regular_image
                )
                food_item.crossed_out_image = pygame.transform.scale2x(
                    food_item.crossed_out_image
                )
                food_item.rect = food_item.image.get_rect(
                    topleft=(
                        food_item.rect.x + self.screen.width // 4,
                        food_item.rect.y,
                    )
                )
        self.sprites.add(*self.inventory)

    def draw_objects(self) -> None:
        self.sprites.draw(self.screen)

    def handle_keyboard(self, pressed: tuple[bool]) -> None:
        if pressed[pygame.K_ESCAPE]:
            self.callback_func(self.id, -1)

    def handle_mouse_click(self) -> None:
        x, y = pygame.mouse.get_pos()
        if self.food_item_holding:
            screen_width, screen_height = self.screen.size
            dist_from_pizza_center = self.calculate_dist_from_pizza_center(
                x, y
            )
            if dist_from_pizza_center > self.pizza_radius:
                self.food_item_holding.cross_out()
            self.food_item_holding.possible_to_move = False
            self.food_item_holding = None
            pygame.mouse.set_visible(True)
        else:
            self.food_item_holding = self.get_food_item_on_click(x, y)
            if self.food_item_holding:
                pygame.mouse.set_visible(False)

    def handle_mouse_motion(self) -> None:
        x, y = pygame.mouse.get_pos()
        if self.food_item_holding:
            self.food_item_holding.rect.center = (x, y)

    def get_food_item_on_click(self, x: int, y: int) -> FoodItem | None:
        for food_item in self.inventory:
            if (
                food_item.rect.collidepoint((x, y))
                and food_item.possible_to_move
            ):
                return food_item
        return None

    def calculate_dist_from_pizza_center(self, x: int, y: int) -> int:
        cx = int(self.screen.width / 2.28)
        cy = self.screen.height // 2
        dist = math.sqrt((cx - x) ** 2 + (cy - y) ** 2)
        return int(dist)
