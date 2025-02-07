from typing import Callable

import pygame
from pygame import Color

from pizza_delivery_dash.scene.scene import Scene


class GameStatisticScene(Scene):
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
        self.bg = Color('DarkGreen')

    def handle_keyboard(self, pressed: tuple[bool]) -> None:
        if pressed[pygame.K_ESCAPE]:
            self.callback_func(self.id, -1)

    def draw_objects(self) -> None:
        if self.app is not None:
            y = self.rect.size[1] // 4
            for result_id in range(len(self.app.stats)):
                game_timestamp, time_taken = self.app.stats[result_id]
                result_text = f'{game_timestamp}   {time_taken}'
                font = pygame.font.Font(None, size=96)
                text_img = font.render(
                    result_text, True, Color('black'), self.bg
                )
                self.screen.blit(text_img, (self.rect.size[0] // 8, y))
                y += round(text_img.height * 1.2)
                if y > self.screen.height:
                    break
            pygame.display.flip()  # full redraw

        current_fps = self.clock.get_fps()
        pygame.display.set_caption(
            f'{self.caption} ({self.id}), FPS: {current_fps:.1f}'
        )
