
class GameStats():
    ''' Track statistics for Alien invasion '''

    def __init__(self, ai_settings) -> None:
        ''' Initialize stats '''
        self.ai_settings = ai_settings
        self.reset_stats()
        self.game_active = False

    def reset_stats(self):
        ''' Initialize statistics that can change during the game '''
        self.ship_left = self.ai_settings.ship_limit

