#game_functions.py
import sys
from time import sleep

import pygame

from alien import Alien
from bullet import Bullet


def key_down(event, settings, screen, rocket, bullets):
    if event.key == pygame.K_RIGHT:
        rocket.move_right = True
    elif event.key == pygame.K_LEFT:
        rocket.move_left = True
    elif event.key == pygame.K_UP:
        rocket.move_up = True
    elif event.key == pygame.K_DOWN:
        rocket.move_down = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(settings=settings, screen=screen,
                    rocket=rocket, bullets=bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def key_up(event, rocket):
    if event.key == pygame.K_RIGHT:
        rocket.move_right = False
    elif event.key == pygame.K_LEFT:
        rocket.move_left = False
    elif event.key == pygame.K_UP:
        rocket.move_up = False
    elif event.key == pygame.K_DOWN:
        rocket.move_down = False


def check_key(
        settings,
        screen,
        rocket,
        aliens,
        bullets,
        play_button,
        stats,
        sb):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            key_down(event=event, settings=settings,
                     screen=screen, rocket=rocket, bullets=bullets)
        elif event.type == pygame.KEYUP:
            key_up(event=event, rocket=rocket)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(settings=settings,
                              screen=screen,
                              stats=stats,
                              play_button=play_button,
                              rocket=rocket,
                              aliens=aliens,
                              bullets=bullets,
                              mouse_x=mouse_x,
                              mouse_y=mouse_y,
                              sb=sb)


def check_play_button(
        settings,
        screen,
        stats,
        play_button,
        rocket,
        aliens,
        bullets,
        mouse_x,
        mouse_y,
        sb):
    '''在玩家单机play按钮时开始新游戏'''
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # 重置游戏设置
        settings.initialize_dynamic_settings()

        # 隐藏光标
        pygame.mouse.set_visible(False)

        # 重置游戏统计信息
        stats.reset_stats()
        stats.game_active = True

        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_rockets()

        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        # 创建一群新的外星人，并让飞船居中
        create_fleet(
            settings=settings,
            screen=screen,
            rocket=rocket,
            aliens=aliens)
        rocket.center_rocket()


def update_bullets(settings, screen, rocket, aliens, bullets, sb, stats):
    """更新子弹的位置，并删除已消失的子弹"""
    # 更新子弹的位置
    bullets.update()

    # 删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(settings=settings,
                                  screen=screen,
                                  rocket=rocket,
                                  aliens=aliens,
                                  bullets=bullets,
                                  sb=sb,
                                  stats=stats)


def check_bullet_alien_collisions(
        settings,
        screen,
        rocket,
        stats,
        aliens,
        sb,
        bullets):
    '''子弹击中外星人'''
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += settings.alien_points * len(aliens)
            sb.prep_score()
        # 外星人最高分的更新
        check_hight_score(stats, sb)

    if len(aliens) == 0:
        # 如果整群外星人被消灭，就提高一个等级
        # 删除现有的子弹，加快游戏节奏，并创建一群新的外星人
        settings.increase_speed()
        # 删除现有的子弹并更新一群外星人
        bullets.empty()

        # 提高等级
        stats.level += 1
        sb.prep_level()
        create_fleet(settings=settings,
                     screen=screen,
                     rocket=rocket,
                     aliens=aliens, )


def fire_bullet(settings, screen, rocket, bullets):
    """如果还没有到达极限，就发射一颗子弹"""
    # 创建一颗新子弹，并其加入到编组bullets中
    if len(bullets) < settings.bullets_allowed:
        new_bullet = Bullet(settings, screen, rocket)
        bullets.add(new_bullet)


def create_fleet(settings, screen, rocket, aliens):
    '''创建外星人群'''
    alien = Alien(settings=settings, screen=screen)

    number_aliens_x = get_number_aliens_x(settings=settings,
                                          alien_width=alien.rect.width)

    number_rows = get_number_rows(
        settings=settings,
        rocket_height=rocket.rect.height,
        alien_height=alien.rect.height)

    # 创建外星人群
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            # 创建第一个外星人并将其加入当前行
            create_alien(settings=settings, screen=screen,
                         aliens=aliens, alien_number=alien_number,
                         row_number=row_number)


def get_number_aliens_x(settings, alien_width):
    '''计算每行可容纳多少人'''
    available_space_x = settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def create_alien(settings, screen, aliens, alien_number, row_number):
    '''创建一个外星人并将其放在当前行'''
    alien = Alien(settings=settings, screen=screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def get_number_rows(settings, rocket_height, alien_height):
    '''计算屏幕可容纳多少行外星人'''
    available_space_y = (settings.screen_hight -
                         (3 * alien_height) - rocket_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def update_aliens(settings, stats, screen, sb, rocket, aliens, bullets):
    '''更新外星人群中所有外星人的位置'''
    '''
    检查是否有外星人位于屏幕边缘，并更新整群外星人的位置
    '''
    check_fleet_edges(settings=settings, aliens=aliens)
    aliens.update()

    # 检测外星人和飞船之间的碰撞
    if pygame.sprite.spritecollideany(rocket, aliens):
        rocket_hit(settings=settings,
                   stats=stats,
                   screen=screen,
                   rocket=rocket,
                   sb=sb,
                   aliens=aliens,
                   bullets=bullets)

    check_aliens_bottom(settings=settings,
                        stats=stats,
                        screen=screen,
                        rocket=rocket,
                        sb=sb,
                        aliens=aliens,
                        bullets=bullets)


def check_fleet_edges(settings, aliens):
    '''有外星人到达边缘时采取相应的措施'''
    for alien in aliens.sprites():
        if alien.check_edges():
            chage_fleet_direction(settings=settings, aliens=aliens)
            break


def chage_fleet_direction(settings, aliens):
    '''将整群外星人下移，并改变它们的方向'''
    for alien in aliens.sprites():
        alien.rect.y += settings.fleet_speed
    settings.fleet_direction *= -1


def rocket_hit(settings, stats, screen, rocket, aliens, bullets, sb):
    '''响应被外星人撞到的飞船'''
    if stats.rocket_left > 0:
        # 将ships_left减1
        stats.rocket_left -= 1

        # 更新记分牌
        sb.prep_rockets()

        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        # 创建一群新的外星人，并将飞船放到屏幕底端中央
        create_fleet(settings=settings,
                     screen=screen,
                     rocket=rocket,
                     aliens=aliens)

        rocket.center_rocket()

        # 暂停
        sleep(0.5)

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(settings, stats, screen, rocket, aliens, bullets, sb):
    '''检查是否有外星人到达了屏幕底端'''
    screen_rect = screen.get_rect()

    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # 像飞船被撞到一样进行处理
            rocket_hit(settings=settings,
                       stats=stats,
                       screen=screen,
                       rocket=rocket,
                       aliens=aliens,
                       bullets=bullets,
                       sb=sb)
            break


def check_hight_score(stats, sb):
    '''检查是否诞生可新的最高分'''
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def screen_display(
        screen,
        settings,
        rocket,
        bullets,
        aliens,
        stats,
        play_button,
        sb):
    screen.fill(settings.bg_color)

    for bullet in bullets.sprites():
        bullet.draw_bullet()

    rocket.rocket_display()

    aliens.draw(screen)

    sb.show_score()

    # 如果游戏处于非活动状态，就绘制Play按钮
    if not stats.game_active:
        play_button.draw_button()

    pygame.display.flip()
