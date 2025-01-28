import os

import pygame

from pizza_delivery_dash.base_sprite import BaseSprite


class AnimatedSprite(BaseSprite):
    def __init__(
        self,
        size: int,
        z: int,
        subdir: str,
        file_names: list[str],
        *groups: pygame.sprite.Group,
    ) -> None:
        self.frames = self.convert_to_frames(subdir, file_names)
        self.current_frame: int = 0
        super().__init__(self.frames[0], 1, *groups)

    def update(self) -> None:
        self.current_frame = self.get_new_frame()
        self.image = self.frames[self.current_frame]

    def flip_frames_horizontally(self) -> None:
        for i, frame in enumerate(self.frames):
            self.frames[i] = self.flip_frame_horizontally(frame)

    def get_new_frame(self) -> int:
        return (self.current_frame + 1) % len(self.frames)

    @staticmethod
    def flip_frame_horizontally(frame: pygame.Surface) -> pygame.Surface:
        return pygame.transform.flip(frame, True, False)

    def convert_to_frames(
        self, subdir: str, file_names: list[str]
    ) -> list[pygame.Surface]:
        directory = self.get_directory_path(subdir)
        frames = [
            self.load_image(file_name, directory, 1440 // 32)
            for file_name in file_names
        ]
        return frames

    @staticmethod
    def get_directory_path(subdir: str) -> str:
        return os.path.join(
            os.getcwd(), 'src', 'pizza_delivery_dash', 'assets', subdir
        )

    @staticmethod
    def load_image(
        tile_name: str, directory: str, size: int
    ) -> pygame.Surface:
        image_file_name = f'{tile_name}.png'
        loaded_image = pygame.image.load(
            os.path.join(directory, image_file_name)
        )
        scaled_image = pygame.transform.scale(loaded_image, (size, size))
        return scaled_image
