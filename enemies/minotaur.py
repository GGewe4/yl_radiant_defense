import pygame
from enemies.enemy import Enemy, load_image
import os


class Minotaur(Enemy):
    imgs = []
    for x in range(18):
        add_str = str(x)
        if x < 10:
            add_str = "0" + add_str
        imgs.append(pygame.transform.scale(load_image(
            f"data/enemies/minotaur/Walking/Minotaur_01_Walking_0" + add_str + ".png"), (80, 65)))

    def __init__(self):
        super().__init__()
        self.frames = Minotaur.imgs[:]
        self.cur_frame = 0
        self.state = 0  # 0 if walking, 1 if dying
        self.image = self.frames[self.cur_frame]
        self.rect = pygame.Rect(0, 0, self.image.get_width(), self.image.get_width())
        self.rect = self.rect.move(self.x, self.y)
        self.change_vel()
