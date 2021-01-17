import pygame
import os
import math

towers_sprites = pygame.sprite.Group()


class Tower(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(towers_sprites)
        self.x = x
        self.y = y
        self.width = 0
        self.height = 0
        self.sell_price = [0, 0, 0]
        self.price = [0, 0, 0]
        self.level = 0
        self.selected = False
        self.imgs = []
        self.img = None

    def upgrade(self):
        pass

    def click(self):
        pass


def load_image(name, colorkey=None):
    pygame.init()
    fullname = os.path.join(name)
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image
