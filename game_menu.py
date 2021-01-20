import pygame


class GameBar:
    def __init__(self):
        self.img = pygame.transform.scale(pygame.image.load('data/game_bar.png'),
                                          (96, 480)).convert_alpha()
        self.x = 1170
        self.y = 20

    def draw(self, wind):
        wind.blit(self.img, (self.x, self.y))

    def collide(self, x, y):
        if 1183 <= x <= 1252:
            if 64 <= y <= 129:
                return 1
            elif 168 <= y <= 233:
                return 2
            elif 274 <= y <= 339:
                return 3
            elif 380 <= y <= 445:
                return 4
        return 0
