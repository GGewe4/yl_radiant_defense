import pygame

from towers.tower import Tower, load_image

pygame.init()


class CrossbowTower(Tower):
    main_img = pygame.transform.scale(
        load_image('data/towers/crossbow/frame_00_delay-0.04s.png', -1),
        (100, 170))
    attack_imgs = []
    for x in range(10):
        add_str = str(x)
        if x < 10:
            add_str = "0" + add_str
        attack_imgs.append(pygame.transform.scale(load_image(
            f"data/towers/crossbow/attack/frame_" + add_str + "_delay-0.04s.png", -1), (100, 170)))

    def __init__(self, x, y):
        super().__init__(x, y)
        self.main_img = CrossbowTower.main_img
        self.attack_imgs = CrossbowTower.attack_imgs[:]
        self.image = self.main_img
        self.rect = pygame.Rect(0, 0, self.image.get_width(), self.image.get_height())
        self.rect = self.rect.move(self.x - self.image.get_width() // 2,
                                   self.y - self.image.get_width() // 2 - 90)
        self.range = 200
        self.splash = False

        self.sell_price = [75, 300, 500]
        self.price = [75, 300, 500]
