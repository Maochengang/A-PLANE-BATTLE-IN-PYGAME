import pygame


class Background(pygame.sprite.Sprite):
    def __init__(self, is_other=False):  # 默认是第一张图像，若为True则为第二章图像
        super().__init__()
        self.image = pygame.image.load("./images/background.png")  # 在初始化函数里面直接传入图像位置
        self.rect = self.image.get_rect()
        print(self.rect.size)
        if is_other:
            self.rect.y = -self.rect.height

    def update(self):
        self.rect.y += 1
        if self.rect.y >= 700:
            self.rect.y = -self.rect.height
