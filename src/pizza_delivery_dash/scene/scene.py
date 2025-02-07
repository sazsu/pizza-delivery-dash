import time

import pygame

# from pygame.locals import *
from pizza_delivery_dash.app import App
from pizza_delivery_dash.food_item import FoodItem


class Scene:
    """Create a new scene and initialize the node options."""

    options = {  # noqa
        'id': 0,
        'bg': pygame.color.Color('gray'),  # background color
        # 'caption': 'Pygame',  # window caption
        'img_folder': '',  # image folder
        'snd_folder': '',  # sound folder
        'file': '',  # background image file
        'focus': None,  # currently active node
        'status': '',
        'shortcuts': {},
        'moving': False,
    }
    selection_border = (pygame.color.Color('cyan'), 1)
    status_line = (
        pygame.color.Color('black'),
        pygame.color.Color('gray'),
        20,
    )  # col, bg, size
    game_display_changed = True
    last_animation_update = time.time()
    game_animation_changed = True
    clock = pygame.time.Clock()

    def __init__(
        self,
        screen: pygame.Surface,
        caption: str = 'Pygame',
        remember: bool = True,
        **options: dict[str, int | pygame.Color | str | bool | dict],
    ) -> None:
        self.nodes = []
        self.caption = caption
        self.screen = screen
        self.sprite_group = pygame.sprite.Group()
        # Add/update instance options from class options
        self.__dict__.update(Scene.options)
        if not remember:
            self.__dict__.update(options)
        self.id = Scene.options['id']
        Scene.options['id'] += 1

        self.rect = self.screen.get_rect()
        if self.file != '':
            self.load_img(self.file)
        else:
            self.img = pygame.Surface(self.rect.size)
            self.img.fill(self.bg)

        self.font = pygame.font.Font(None, size=64)
        self.caption_img = self.font.render(
            self.caption, True, pygame.color.Color('black'), self.bg
        )
        self.app = None
        self.enter()

    def handle_events(self) -> None:
        pass

    def handle_keyboard(self, pressed: tuple[bool]) -> None:
        pass

    def handle_input(self) -> None:
        pass

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            self.handle_keyboard(pygame.key.get_pressed())

    def draw_objects(self) -> None:
        pass

    def draw_animated_objects(self) -> None:
        pass

    def draw_caption(self) -> None:
        self.screen.blit(
            self.caption_img, (self.rect.size[0] // 16, self.rect.size[1] // 8)
        )

    def update_animations(self) -> None:
        if time.time() - self.last_animation_update > 0.5:
            self.game_animation_changed = True
            self.last_animation_update = time.time()

    def draw_bg(self) -> None:
        self.screen.fill(self.bg)

    def draw(self) -> None:
        self.draw_bg()
        self.draw_caption()
        self.update_animations()
        self.draw_objects()
        if self.game_animation_changed:
            self.draw_animated_objects()
            self.game_animation_changed = False

        pygame.display.flip()  # full redraw
        self.game_display_changed = False

        current_fps = self.clock.get_fps()
        pygame.display.set_caption(
            f'{self.caption} ({self.id}), FPS: {current_fps:.1f}'
        )

    def enter(self, app=None) -> None:  # noqa
        """Enter a scene."""
        pygame.display.set_caption(self.caption)
        self.app = app

    def update(self) -> None:
        """Update the nodes in a scene."""
        for node in self.nodes:
            node.update()

    @property
    def inventory(self) -> list[FoodItem]:
        return App.inventory

    def __str__(self) -> str:
        return f'Scene{self.id}'
