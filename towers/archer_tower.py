import pygame

from towers.tower import Tower, load_image

pygame.init()


class ArcherTower(Tower):
    main_img = pygame.transform.scale(load_image('data/towers/archer/frame_0_delay-0.04s.png', -1),
                                      (100, 170))
    attack_imgs = []
    for x in range(10):
        add_str = str(x)
        attack_imgs.append(pygame.transform.scale(load_image(
            f"data/towers/archer/attack/frame_" + add_str + "_delay-0.04s.png", -1), (100, 170)))

    def __init__(self, x, y):
        super().__init__(x, y)
        self.main_img = ArcherTower.main_img
        self.attack_imgs = ArcherTower.attack_imgs[:]
        self.image = self.main_img
        self.rect = pygame.Rect(0, 0, self.image.get_width(), self.image.get_height())
        self.rect = self.rect.move(self.x - self.image.get_width() // 2,
                                   self.y - self.image.get_width() // 2 - 90)
        self.range = 120
        self.splash = False

        self.sell_price = [50, 150, 300]
        self.price = [50, 150, 300]
