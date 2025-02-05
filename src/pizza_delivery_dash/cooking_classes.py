import pygame

class FoodSprite(pygame.sprite.Sprite):
    def __init__(self, pos: tuple, *ingredient: str):
        self.ingredient = ingredient
        self.pos = pos