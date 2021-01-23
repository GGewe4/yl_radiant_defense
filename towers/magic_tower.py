import pygame

from towers.tower import Tower, load_image

pygame.init()


class MagicTower(Tower):
    main_img = pygame.transform.scale(load_image('data/towers/magic/magic_frame_00.png', -1),
                                      (150, 170))
    attack_imgs = []
    for x in range(16):
        add_str = str(x)
        if x < 10:
            add_str = "0" + add_str
        attack_imgs.append(pygame.transform.scale(load_image(
            f"data/towers/magic/attack/magic_frame_" + add_str + ".png", -1), (150, 170)))

    def __init__(self, x, y):
        super().__init__(x, y)
        self.main_img = MagicTower.main_img
        self.attack_imgs = MagicTower.attack_imgs[:]
        self.image = self.main_img
        self.rect = pygame.Rect(0, 0, self.image.get_width(), self.image.get_height())
        self.rect = self.rect.move(self.x - self.image.get_width() // 2,
                                   self.y - self.image.get_width() // 2 - 60)
        self.range = 100
        self.damage = 2
        self.splash = True

        self.sell_price = [150, 700, 1000]
        self.price = [150, 700, 1000]
