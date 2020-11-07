#rocket.py
'''火箭类'''
import pygame
from pygame.sprite import Sprite


class Rocket(Sprite):

    def __init__(self, settings, screen):
        super().__init__()

        self.screen = screen

        self.settings = settings
        self.image = pygame.image.load('image/飞船.bmp')

        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        self.centerx = float(self.rect.centerx)
        self.bottom = float(self.rect.bottom)

        self.move_right = \
            self.move_left = \
            self.move_up = \
            self.move_down = \
            settings.rocket_moveing

    def rocket_update(self):

        if self.move_right and self.rect.right < self.screen_rect.right:
            self.centerx += self.settings.rocket_speed_grade
        elif self.move_left and self.rect.left > 0:
            self.centerx -= self.settings.rocket_speed_grade
        elif self.move_up and self.rect.top > 0:
            self.bottom -= self.settings.rocket_speed_grade
        elif self.move_down and self.rect.bottom < self.screen_rect.bottom:
            self.bottom += self.settings.rocket_speed_grade

        self.rect.centerx = self.centerx
        self.rect.bottom = self.bottom

    def rocket_display(self):

        self.screen.blit(self.image, self.rect)

    def center_rocket(self):
        '''让飞船在屏幕上居中'''
        self.centerx = self.screen_rect.centerx
        self.bottom = self.screen_rect.bottom
