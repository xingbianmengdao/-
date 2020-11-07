#rocketgame.py
import pygame
from pygame.sprite import Group

import game_functions
from button import Button
from game_stats import GameStats
from rocket import Rocket
from scoreboard import Scoreboard
from settings import Setting


def rocket_game():
    pygame.init()

    settings = Setting()

    screen = pygame.display.set_mode(
        (settings.screen_width, settings.screen_hight))

    pygame.display.set_caption(settings.screen_caption)

    # 创建Play按钮
    play_button = Button(settings, screen, 'play')

    # 创建一个用于存储游戏统计信息的实例,并创建记分牌
    stats = GameStats(settings)
    sb = Scoreboard(settings=settings, screen=screen, stats=stats)

    # 创建一艘飞船、一个子弹编组和一个外星人编组
    aliens = Group()

    rocket = Rocket(settings=settings, screen=screen)

    # 创建外星人群
    game_functions.create_fleet(settings=settings, screen=screen,
                                aliens=aliens, rocket=rocket)

    # 创建一个用于存储子弹的编组
    bullets = Group()

    # 开始游戏主循环

    while True:

        game_functions.check_key(settings=settings, screen=screen,
                                 rocket=rocket, bullets=bullets,
                                 stats=stats, play_button=play_button,
                                 aliens=aliens, sb=sb)

        if stats.game_active:
            game_functions.update_bullets(settings=settings,
                                          screen=screen,
                                          rocket=rocket,
                                          aliens=aliens,
                                          bullets=bullets,
                                          sb=sb,
                                          stats=stats)

            game_functions.update_aliens(settings=settings,
                                         stats=stats,
                                         screen=screen,
                                         rocket=rocket,
                                         aliens=aliens,
                                         bullets=bullets,
                                         sb=sb)

            rocket.rocket_update()

        game_functions.screen_display(
            settings=settings,
            screen=screen,
            stats=stats,
            rocket=rocket,
            bullets=bullets,
            aliens=aliens,
            sb=sb,
            play_button=play_button)


rocket_game()
