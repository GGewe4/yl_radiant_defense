import pygame
import os
import math

from towers.tower import Tower, load_image

pygame.init()


class StoneTower(Tower):
    main_img = pygame.transform.scale(load_image('data/towers/stone/frame_00_delay-0.04s.png'),
                                      (100, 200))
    attack_imgs = []
    for x in range(23):
        add_str = str(x)
        if x < 10:
            add_str = "0" + add_str
        attack_imgs.append(pygame.transform.scale(load_image(
            f"data/towers/stone/attack/frame_" + add_str + "_delay-0.04s-removebg-preview.png",), (100, 200)))

    def __init__(self, x, y):
        super().__init__(x, y)
        self.main_img = StoneTower.main_img
        self.attack_imgs = StoneTower.attack_imgs[:]
        self.image = self.main_img
        self.rect = pygame.Rect(0, 0, self.image.get_width(), self.image.get_height())
        self.rect = self.rect.move(self.x - self.image.get_width() // 2,
                                   self.y - self.image.get_width() // 2 - 120)
        self.range = 150
