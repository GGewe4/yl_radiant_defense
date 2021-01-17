import pygame
from enemies.enemy import Enemy, load_image
import os


class Wraith(Enemy):
    imgs = []
    for x in range(12):
        add_str = str(x)
        if x < 10:
            add_str = "0" + add_str
        imgs.append(pygame.transform.scale(load_image(
            f"data/enemies/wraith/Walking/Wraith_01_MovingForward_0" + add_str + ".png"), (80, 65)))

    def __init__(self):
        super().__init__()
        self.frames = Wraith.imgs[:]
        self.cur_frame = 0
        self.state = 0  # 0 if walking, 1 if dying
        self.image = self.frames[self.cur_frame]
        self.rect = pygame.Rect(0, 0, self.image.get_width(), self.image.get_width())
        self.rect = self.rect.move(self.x, self.y)
        self.change_vel()
