#settings.py
'''设置类'''


class Setting():

    def __init__(self):
        '''初始化游戏的静态设置'''
        # 窗口属性
        self.screen_width = 400
        self.screen_hight = 647
        self.bg_color = (255, 255, 255)
        self.screen_caption = '武装飞船最终版'
        # 火箭属性
        self.rocket_speed_grade = 1.5
        self.rocket_moveing = False
        self.rocket_limit = 3
        # 子弹属性
        self.bullet_speed_factor = 1.5
        self.bullet_width = 5
        self.bullet_height = 20
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 10
        # 外星人属性
        self.alien_speed = 0.6
        self.fleet_speed = 5
        # fleet_direction为1表示右移,为-1表示左移
        self.fleet_direction = 1
        # 以什么样的速度加快游戏节奏
        self.speedup_scale = 1.1
        # 外星人点数的提高速度
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        '''初始化随游戏而进行变化的设置'''
        self.rocket_speed_grade = 1.5
        self.bullet_speed_factor = 1.5
        self.alien_speed = 0.6

        # fleet_direction为q表示向右；为-1表示向左
        self.fleet_direction = 1

        # 记分
        self.alien_points = 50

    def increase_speed(self):
        '''提高速度设置'''
        self.rocket_speed_grade *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
