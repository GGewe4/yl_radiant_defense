import pygame


class GameBar:
    def __init__(self):
        self.img = pygame.transform.scale(pygame.image.load('data/ui/game_bar.png'),
                                          (96, 480)).convert_alpha()
        self.heart = pygame.transform.scale(pygame.image.load('data/ui/heart.png'),
                                            (80, 80)).convert_alpha()
        self.coins = pygame.transform.scale(pygame.image.load('data/ui/coins.png'),
                                            (80, 80)).convert_alpha()
        self.health = pygame.font.Font(None, 50)
        self.money = pygame.font.Font(None, 50)
        self.x = 1170
        self.y = 20
        self.showing = False

    def draw(self, wind, health, money):
        if self.showing:
            wind.blit(self.img, (self.x, self.y))
        health = self.health.render(f"{health}", True, (255, 255, 255))
        money = self.money.render(f"{money}", True, (255, 255, 255))
        wind.blit(health, (115, 33))
        wind.blit(money, (115, 113))
        wind.blit(self.heart, (30, 10))
        wind.blit(self.coins, (30, 90))

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
