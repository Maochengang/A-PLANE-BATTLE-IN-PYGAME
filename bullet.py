from pygame import image, sprite, mask


class Bullet1(sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = image.load(r"D:\about python\pygame_website\飞机大战\images\bullet3.png")
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = position
        self.speed = 15
        self.active = False
        self.mask = mask.from_surface(self.image)

    def move(self):
        self.rect.top -= self.speed
        if self.rect.top < 0:
            self.active = False

    def reset(self, position):
        self.rect.left, self.rect.top = position
        self.active = True


class Bullet2(sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = image.load(r"D:\about python\pygame_website\飞机大战\images\bullet4.png")
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = position
        self.speed = 15
        self.active = False
        self.mask = mask.from_surface(self.image)

    def move(self):
        self.rect.top -= self.speed
        if self.rect.top < 0:
            self.active = False

    def reset(self, position):
        self.rect.left, self.rect.top = position
        self.active = True

