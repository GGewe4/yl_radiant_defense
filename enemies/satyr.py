import pygame
from enemies.enemy import Enemy, load_image


class Satyr(Enemy):
    def __init__(self):
        super().__init__()
        self.frames = []
        self.cur_frame = 0
        self.state = 0  # 0 if walking, 1 if dying
        for x in range(18):
            add_str = str(x)
            if x < 10:
                add_str = "0" + add_str
            self.frames.append(pygame.transform.scale(load_image(
                f"data/enemies/satyr/Walking/Satyr_03_Walking_0" + add_str + ".png"), (80, 65)))
        self.image = self.frames[self.cur_frame]
        self.rect = pygame.Rect(0, 0, self.image.get_width(), self.image.get_width())
        self.rect = self.rect.move(self.x, self.y)
        self.change_vel()