import pygame

from db.manager import Database
from pizza_delivery_dash.app import App
from pizza_delivery_dash.scene.scene_confirmation import ConfirmationScene
from pizza_delivery_dash.scene.scene_gameover import GameoverScene
from pizza_delivery_dash.scene.scene_level import LevelScene
from pizza_delivery_dash.scene.scene_mainmenu import MainMenuScene
from pizza_delivery_dash.scene.scene_pizzeria import PizzeriaScene
from pizza_delivery_dash.scene.scene_shop import ShopScene
from pizza_delivery_dash.scene.scene_stats import GameStatisticScene


class PizzaApp(App):
    def __init__(
        self,
        size: tuple[int, int] = (1920, 1080),
        shortcuts: dict[tuple[int, int], str] = {},
    ) -> None:
        super().__init__(size, shortcuts)
        self.game_results = []  # player_name, date_time, result, score
        self.shop_visited = False
        self.pizzeria_visited = False
        self.toggle_fullscreen()
        # TODO: make a dictionary to navigate from scene to scene
        self.add_scene(
            MainMenuScene(self.screen, self.callback_result, 'Main Menu')
        )
        self.add_scene(
            LevelScene(
                'level1.txt', self.screen, self.callback_result, 'Level 1'
            )
        )
        self.add_scene(
            GameStatisticScene(self.screen, self.callback_result, 'Stats')
        )
        self.add_scene(
            GameoverScene(self.screen, self.callback_result, 'Game Over')
        )
        self.add_scene(
            ShopScene(self.screen, self.callback_result, 'Supermarket')
        )
        self.add_scene(
            PizzeriaScene(self.screen, self.callback_result, 'Pizzeria')
        )
        self.add_scene(
            ConfirmationScene(
                self.screen, self.callback_result, 'Confirm Leaving'
            )
        )
        self.database = Database('pizza_db.sqlite3')
        self.navigate_scene(0)

    def callback_result(self, scene_id: int, result_code: int) -> None:  # noqa
        if self.previous_scene_id[-1] != 0:
            self.previous_scene_id.pop(-1)
        if result_code == -1:
            if scene_id == 0:  # main menu
                self.navigate_scene(6)  # switch to confirm exit
            elif scene_id in [4, 5]:
                self.navigate_scene(1)
            else:
                previous_id = self.previous_scene_id[-1]
                if previous_id == 0:
                    self.previous_scene_id = []
                self.navigate_scene(previous_id)
        else:
            if scene_id == 0:  # main menu
                if result_code == 0:  # switch to level scene
                    self.level_enter_time = pygame.time.get_ticks()
                    self.reset_level()
                    self.navigate_scene(1)
                elif result_code == 1:  # switch to stats scene
                    self.update_stats()
                    self.navigate_scene(2)
            elif scene_id == 1:  # level 1
                if (
                    result_code == 0
                    and self.shop_visited
                    and not self.pizzeria_visited
                ):  # switch to pizzeria
                    self.navigate_scene(5)
                elif result_code == 1:  # switch to shop
                    self.navigate_scene(4)
                elif result_code == 2 and self.pizzeria_visited:
                    self.navigate_scene(3)
            elif scene_id == 6:  # confirmation_menu
                if result_code == 0:  # exit game
                    self.exit_program()

    def add_new_stat(self, time_taken: float) -> None:
        self.database.put_time(time_taken)

    def update_stats(self) -> None:
        self.stats = self.database.get_stats()

    def reset_level(self) -> None:
        App.inventory.clear()
        self.shop_visited = False
        self.pizzeria_visited = False
        self.scenes[1].reset()
        self.scenes[4].reset()

    def exit_program(self) -> None:
        App.running = False
