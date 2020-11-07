#scoreboard.py
import pygame.font
from pygame.sprite import Group

from rocket import Rocket


class Scoreboard():
    '''显示得分信息的类'''

    def __init__(self, settings, screen, stats):
        '''初始化显示得分涉及的属性'''
        self.screen = screen

        self.screen_rect = screen.get_rect()

        self.settings = settings
        self.stats = stats

        # 显示得分信息时使用的字体设置
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 22)

        # 准备初始得分图像
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_rockets()

    def prep_score(self):
        '''将得分转换为一幅渲染的图像'''
        rounded_score = int(round(self.stats.score, -1))
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(
            'Score: ' + score_str,
            True,
            self.text_color,
            self.settings.bg_color)

        # 非得分数放在屏幕右上角
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_score(self):
        '''在屏幕上显示得分'''
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.rockets.draw(self.screen)

    def prep_high_score(self):
        '''将最高得分转换为渲染的图像'''
        high_score = int(round(self.stats.high_score, -1))
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(
            'High Score: ' +
            high_score_str,
            True,
            self.text_color,
            self.settings.bg_color)

        # 将最高分数放在屏幕顶部中央
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.screen_rect.top

    def prep_level(self):
        '''将等级转换为渲染的图像'''
        self.level_image = self.font.render(
            'Lvevl: ' + str(self.stats.level), True, self.text_color, self.settings.bg_color)

        # 将等级放在的饭下方
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_rockets(self):
        '''显示还余下多少艘飞船'''
        self.rockets = Group()
        for rocket_number in range(self.stats.rocket_left):
            rocket = Rocket(self.settings, self.screen)
            rocket.rect.x = 10 + rocket_number * rocket.rect.width
            rocket.rect.y = 10
            self.rockets.add(rocket)
