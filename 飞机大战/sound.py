import pygame


pygame.mixer.init()


def init_sound():


    me_down_sound = pygame.mixer.Sound("./sound/me_down.wav")
    me_down_sound.set_volume(0.2)