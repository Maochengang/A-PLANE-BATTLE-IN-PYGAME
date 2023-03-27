import pygame
from random import *


class BulletSupply(pygame.sprite.Sprite):
    def __init__(self, bg_size):
        super().__init__()
        self.image = pygame.image.load(r"D:\about python\pygame_website\飞机大战\images\bullet_supply.png")
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.rect.left = randint(0, self.width - self.rect.width)
        self.rect.top = -100
        self.speed = 5
        self.active = False
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        if self.rect.y < self.height:
            self.rect.y += self.speed
        else:
            self.active = False

    def reset(self):
        self.rect.x = randint(0, self.width - self.rect.width)
        self.rect.top = -100
        self.active = True


class BombSupply(pygame.sprite.Sprite):
    def __init__(self, bg_size):
        super().__init__()
        self.image = pygame.image.load(r"D:\about python\pygame_website\飞机大战\images\bomb_supply.png")
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.rect.left = randint(0, self.width - self.rect.width)
        self.rect.top = -100
        self.speed = 4
        self.active = False
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        if self.rect.y < self.height:
            self.rect.y += self.speed
        else:
            self.active = False

    def reset(self):
        self.rect.x = randint(0, self.width - self.rect.width)
        self.rect.top = -100
        self.active = True

