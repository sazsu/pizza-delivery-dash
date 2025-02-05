import os
import pygame
from config import Config
from utils import load_image
from pizza_delivery_dash.state import State, StateError
from pizza_delivery_dash.game import PizzaDeliveryDash
from pizza_delivery_dash.main_menu import MainMenu
from pizza_delivery_dash.game_loop import GameLoop
from pizza_delivery_dash.cooking_classes import FoodSprite


class Cooking(PizzaDeliveryDash):
    game: 'pizza_delivery_dash.game.PizzaDeliveryDash'

    def __init__(self):
        self.sprites_group = pygame.sprite.Group
        self.screen = pygame.Surface
        print(self.screen.width)
        self.pizza = FoodSprite((self.screen.width // 2 - self.screen.width // 8, self.screen.height // 2), 'pizza')
        self.cheese = FoodSprite((self.screen.width // 100, self.screen.height // 100), 'cheese')
        self.chicken = FoodSprite((self.screen.width // 100 * 20, self.screen.height // 100), 'chicken')
        self.mushrooms = FoodSprite((self.screen.width // 100 * 40, self.screen.height // 100), 'mushrooms')
        self.fullscreen = True
        self.screen_rect = pygame.Rect(0, 0, Config.WIDTH, Config.HEIGHT)
        # self.game = # PizzaDeliveryDash # pizza_delivery_dash.game.PizzaDeliveryDash
        self.init()
        # self.create(True)
        self.set_state(State.inside_pizzeria)
        self.loop()

    def loop(self):
        clock = pygame.Clock()
        while self.state != State.quitting:
            self.handle_events()
            pygame.display.flip()
            # self.update_display()
            clock.tick(Config.FPS)

    def handle_events(self):
        for event in pygame.event.get():
            self.image_rendering()
            if event.type == pygame.QUIT:
                self.set_state(State.quitting)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.image_moving(event.pos)
                # self.handle_mouse_click()

    def load_image(
            self, name: str, colorkey: None | int | pygame.Color = None
    ) -> pygame.Surface:
        fullname = os.path.join('src', 'pizza_delivery_dash', 'assets', 'cooking assets', name)
        if not os.path.isfile(fullname):
            raise FileNotFoundError(f'Cannot find image file with the name {fullname}')
        image = pygame.image.load(fullname)
        if colorkey is not None:
            image = image.convert()
            colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
        # else:
            # image = convert_alpha(image)
        return image

    def image_rendering(self):
        self.image_load = self.load_image(f"background.png")
        self.image_loaded = pygame.transform.scale(self.image_load, (self.screen.width, self.screen.height))
        self.screen.blit(self.image_loaded,
                         (0, 0))
        self.image_load = self.load_image("pizza.png", pygame.Color(0, 0, 0))
        self.image_loaded = pygame.transform.scale(self.image_load, (self.screen.width // 4, self.screen.width // 4))
        self.screen.blit(self.image_loaded,
                         (self.screen.width // 2 - self.screen.width // 8, self.screen.height // 2))
        self.image_load = self.load_image("cheese.png", pygame.Color(0, 0, 0))
        self.image_loaded = pygame.transform.scale(self.image_load, (self.screen.width // 6, self.screen.width // 6))
        self.screen.blit(self.image_loaded,
                         (self.screen.width // 100, self.screen.height // 100))
        self.image_load = self.load_image("chicken.png", pygame.Color(0, 0, 0))
        self.image_loaded = pygame.transform.scale(self.image_load, (self.screen.width // 6, self.screen.width // 6))
        self.screen.blit(self.image_loaded,
                         (self.screen.width // 100 * 20, self.screen.height // 100))
        self.image_load = self.load_image("mushrooms.png", pygame.Color(0, 0, 0))
        self.image_loaded = pygame.transform.scale(self.image_load, (self.screen.width // 6, self.screen.width // 6))
        self.screen.blit(self.image_loaded,
                         (self.screen.width // 100 * 40, self.screen.height // 100))

    def image_moving(self, mousepos) -> None:
        pass

    # def update_display(self):
        # self.sprites_group.draw(self, self.screen)
        # pygame.display.flip()

    # def sprites(self):
        # return self.load_sprites()

    # def load_sprites(self) -> None:
        # self.sprites = {}
        # for human_readable_name, file_name in self.sprites_group.items():
            # image = load_image(file_name)
            # self.sprites[human_readable_name] = image


# a = PizzaDeliveryDash
# a.create(True)
# a.set_state(a, State.inside_pizzeria)
# b = MainMenu()
# a.b.loop()
a = Cooking()