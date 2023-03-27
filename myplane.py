import webbrowser

import pygame


class MyPlane(pygame.sprite.Sprite):
    def __init__(self, bg_size):
        self.image1 = pygame.image.load(r"D:\about python\pygame_website\飞机大战\images\me1.png")
        self.image2 = pygame.image.load(r"D:\about python\pygame_website\飞机大战\images\me2.png")
        self.destroy_images = []
        self.destroy_images.extend([pygame.image.load(r"D:\about python\pygame_website\飞机大战\images\me_destroy_1.png"),
                                    pygame.image.load(r"D:\about python\pygame_website\飞机大战\images\me_destroy_2.png"),
                                    pygame.image.load(r"D:\about python\pygame_website\飞机大战\images\me_destroy_3.png"),
                                    pygame.image.load(r"D:\about python\pygame_website\飞机大战\images\me_destroy_4.png")])
        self.active = True
        self.invincible = False
        self.mask = pygame.mask.from_surface(self.image1)
        self.width = bg_size[0]
        self.height = bg_size[1]
        self.rect = self.image1.get_rect()
        self.rect.bottom = bg_size[1] - 60
        self.rect.left = (bg_size[0] - self.rect.width) // 2
        self.speed = 8

    def move_up(self):
        if self.rect.top > 0:
            self.rect.top -= self.speed
        else:
            self.rect.top = 0

    def move_down(self):
        if self.rect.bottom < self.height - 60:
            self.rect.bottom += self.speed
        else:
            self.rect.bottom = self.height - 60

    def move_left(self):
        if self.rect.left > 0:
            self.rect.left -= self.speed
        else:
            self.rect.left = 0

    def move_right(self):
        if self.rect.right < self.width:
            self.rect.right += self.speed
        else:
            self.rect.right = self.width

    def reset(self):
        self.rect.left = (self.width - self.rect.width) // 2
        self.rect.bottom = self.height - 60
        self.active = True
        self.invincible = True

    def change_face(self, bg_size):
        self.image1 = pygame.image.load(r"D:\about python\pygame_website\飞机大战\images\me5.png")
        self.image2 = pygame.image.load(r"D:\about python\pygame_website\飞机大战\images\me6.png")
        self.mask = pygame.mask.from_surface(self.image1)
        self.rect = self.image1.get_rect()
        self.rect.bottom = bg_size[1] - 60
        self.rect.left = (bg_size[0] - self.rect.width) // 2
        self.speed = 10

