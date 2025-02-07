from typing import ClassVar

import pygame

# from pygame.locals import *
from config import Config


class App:
    """
    Create a single-window app with multiple scenes
    having multiple objects.
    """

    scenes = []  # noqa
    scene = None  # current scene
    screen = None  # main display window
    running = True  # the app is running
    focus = None  # current object for cut/copy/paste
    root = None
    key_repeat = 200, 100
    clock = pygame.time.Clock()
    previous_scene_id: ClassVar[list[int]] = []
    inventory = []  # noqa

    def __init__(
        self,
        size: tuple[int, int] = (800, 600),
        shortcuts: dict[tuple[int, int], str] = {},
    ) -> None:
        """Initialize pygame and the application."""
        pygame.init()
        pygame.key.set_repeat(*App.key_repeat)
        self.flags = 0  # RESIZABLE, FULLSCREEN, NOFRAME
        self.rect = pygame.rect.Rect(0, 0, *size)
        App.screen = pygame.display.set_mode(self.rect.size, self.flags)
        App.root = self

        self.shortcuts = {
            (pygame.K_f, pygame.KMOD_ALT): 'self.toggle_fullscreen()',
            (pygame.K_r, pygame.KMOD_ALT): 'self.toggle_resizable()',
            (pygame.K_g, pygame.KMOD_ALT): 'self.toggle_frame()',
        }
        self.shortcuts.update(shortcuts)

    def callback_result(self, scene_id: int, result_code: int) -> None:
        pass

    def run(self) -> None:
        """Run the main event loop."""
        while App.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    App.running = False

                elif event.type == pygame.KEYDOWN:
                    self.do_shortcut(event)

                # Send the event to the scene
                if App.scene is not None:
                    # App.scene.do_event(event)
                    App.scene.handle_event(event)
            if App.scene is not None:
                App.scene.update()
                App.scene.draw()
                App.scene.clock.tick(Config.FPS)

        pygame.quit()

    def add_scene(self, scene) -> None:  # noqa
        App.scenes.append(scene)
        App.scene = scene

    def navigate_scene(self, scene_id: int = 0) -> None:
        """Switch to scene."""
        self.previous_scene_id.append(scene_id)
        App.scene = App.scenes[scene_id]
        App.scene.enter(app=self)
        App.scene.update()
        App.scene.draw()

    def do_shortcut(self, event: pygame.event.Event) -> None:
        """
        Find the key/mod combination in the dictionary
        and execute the cmd.
        """
        k = pygame.key.get_pressed()
        m = event.mod
        for key, mod in self.shortcuts:
            if (k[key] and m & mod) or (k[key] and mod == pygame.KMOD_NONE):
                exec(self.shortcuts[key, mod])
                break

    def toggle_fullscreen(self) -> None:
        """Toggle between full screen and windowed screen."""
        self.flags ^= pygame.FULLSCREEN
        pygame.display.set_mode((0, 0), self.flags)

    def toggle_resizable(self) -> None:
        """Toggle between resizable and fixed-size window."""
        self.flags ^= pygame.RESIZABLE
        pygame.display.set_mode(self.rect.size, self.flags)

    def toggle_frame(self) -> None:
        """Toggle between frame and noframe window."""
        self.flags ^= pygame.NOFRAME
        pygame.display.set_mode(self.rect.size, self.flags)

    def __str__(self) -> str:
        return self.__class__.__name__
