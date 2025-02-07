from typing import Callable

import pygame
from pygame import Color

from pizza_delivery_dash.app import App
from pizza_delivery_dash.scene.scene import Scene


class GameoverScene(Scene):
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
        self.bg = Color('white')
        # self.last_game_status = -1

    def handle_keyboard(self, pressed: tuple[bool]) -> None:
        if pressed[pygame.K_ESCAPE]:
            self.callback_func(self.id, -1)

    def enter(self, app: App | None = None) -> None:
        if app is not None:
            self.time_taken_secs = (
                pygame.time.get_ticks() - app.level_enter_time
            ) / 1000
            app.database.put_time(self.time_taken_secs)
        super().enter(app)

    def draw_objects(self) -> None:
        game_result_text = f'Level passed in {self.time_taken_secs} seconds'
        font = pygame.font.Font(None, size=128)
        text_img = font.render(game_result_text, True, Color('black'), self.bg)
        self.screen.blit(
            text_img, (self.rect.size[0] // 8, self.rect.size[1] // 4)
        )
        pygame.display.flip()  # full redraw
        current_fps = self.clock.get_fps()
        pygame.display.set_caption(
            f'{self.caption} ({self.id}), FPS: {current_fps:.1f}'
        )
