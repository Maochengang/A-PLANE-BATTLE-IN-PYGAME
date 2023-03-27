import pygame
from random import *


class SmallEnemy(pygame.sprite.Sprite):
    def __init__(self, bg_size):
        super(SmallEnemy, self).__init__()
        self.image = pygame.image.load(r"D:\about python\pygame_website\飞机大战\images\enemy1.png")
        self.destroy_images = []
        self.destroy_images.extend([pygame.image.load(r"D:\about python\pygame_website\飞机大战\images\enemy1_down1.png"),
                                   pygame.image.load(r"D:\about python\pygame_website\飞机大战\images\enemy1_down2.png"),
                                   pygame.image.load(r"D:\about python\pygame_website\飞机大战\images\enemy1_down3.png"),
                                   pygame.image.load(r"D:\about python\pygame_website\飞机大战\images\enemy1_down4.png")])
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.speed = 2
        self.rect.left = randint(0, self.width - self.rect.width)
        self.rect.top = randint(-5 * self.height, 0)
        self.active = True
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        self.active = True
        self.rect.left = randint(0, self.width - self.rect.width)
        self.rect.top = randint(-5 * self.height, 0)

    @staticmethod
    def add_small_enemies(group1, group2, bg_size, num):
        for i in range(num):
            e1 = SmallEnemy(bg_size)
            group1.add(e1)
            group2.add(e1)


class MidEnemy(pygame.sprite.Sprite):
    energy = 8

    def __init__(self, bg_size):
        super().__init__()
        self.image = pygame.image.load(r"D:\about python\pygame_website\飞机大战\images\enemy2.png")
        self.hit_image = pygame.image.load(r"D:\about python\pygame_website\飞机大战\images\enemy2_hit.png")
        self.destroy_images = []
        self.destroy_images.extend([pygame.image.load(r"D:\about python\pygame_website\飞机大战\images\enemy2_down1.png"),
                                    pygame.image.load(r"D:\about python\pygame_website\飞机大战\images\enemy2_down2.png"),
                                    pygame.image.load(r"D:\about python\pygame_website\飞机大战\images\enemy2_down3.png"),
                                    pygame.image.load(r"D:\about python\pygame_website\飞机大战\images\enemy2_down4.png")])
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.speed = 2
        self.rect.left = randint(0, self.width - self.rect.width)
        self.rect.top = randint(-10 * self.height, -self.height)
        self.active = True
        self.hit = False
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        self.active = True
        self.energy = MidEnemy.energy
        self.rect.left = randint(0, self.width - self.rect.width)
        self.rect.top = randint(-10 * self.height, -self.height)

    @staticmethod
    def add_mid_enemies(group1, group2, bg_size, num):
        for i in range(num):
            e2 = MidEnemy(bg_size)
            group1.add(e2)
            group2.add(e2)


class BigEnemy(pygame.sprite.Sprite):
    energy = 20

    def __init__(self, bg_size):
        super().__init__()
        self.image1 = pygame.image.load(r"D:\about python\pygame_website\飞机大战\images\enemy3_n1.png")
        self.image2 = pygame.image.load(r"D:\about python\pygame_website\飞机大战\images\enemy3_n2.png")
        self.hit_image = pygame.image.load(r"D:\about python\pygame_website\飞机大战\images\enemy3_hit.png")
        self.destroy_images = []
        self.destroy_images.extend([pygame.image.load(r"D:\about python\pygame_website\飞机大战\images\enemy3_down1.png"),
                                    pygame.image.load(r"D:\about python\pygame_website\飞机大战\images\enemy3_down2.png"),
                                    pygame.image.load(r"D:\about python\pygame_website\飞机大战\images\enemy3_down3.png"),
                                    pygame.image.load(r"D:\about python\pygame_website\飞机大战\images\enemy3_down4.png"),
                                    pygame.image.load(r"D:\about python\pygame_website\飞机大战\images\enemy3_down5.png"),
                                    pygame.image.load(r"D:\about python\pygame_website\飞机大战\images\enemy3_down6.png")])
        self.rect = self.image1.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.speed = 2
        self.rect.left = randint(0, self.width - self.rect.width)
        self.rect.top = randint(-15 * self.height, -5 * self.height)
        self.active = True
        self.hit = False
        self.mask = pygame.mask.from_surface(self.image1)

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        self.active = True
        self.energy = BigEnemy.energy
        self.rect.left = randint(0, self.width - self.rect.width)
        self.rect.top = randint(-15 * self.height, -5 * self.height)

    @staticmethod
    def add_big_enemies(group1, group2, bg_size, num):
        for i in range(num):
            e3 = BigEnemy(bg_size)
            group1.add(e3)
            group2.add(e3)

