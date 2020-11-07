#game_stats.py
class GameStats():
    '''跟踪游戏的统计信息'''

    def __init__(self, settings):
        '''初始化统计信息'''
        self.settings = settings
        self.reset_stats()
        # 游戏刚启动时处于非活动状态
        self.game_active = False
        # 在任何情况下都不应重置最高得分
        self.high_score = 0

    def reset_stats(self):
        '''初始化在游戏运行期间可能变化的统计信息'''
        self.rocket_left = self.settings.rocket_limit
        self.score = 0
        self.level = 1
