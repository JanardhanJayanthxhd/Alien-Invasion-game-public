

class Settings():
    ''' A class to store all settings '''
    def __init__(self) -> None:
        ''' Initializes game's settings '''
        self.screen_width = 1000
        self.screen_height = 800
        self.screen_bg = (28, 14, 96)

        # Ship's settings
        self.ship_limit = 3

        # Bullet's settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (0, 255, 27)
        self.bullets_allowed = 3 
        
        # Alien settings
        self.fleet_drop_speed = 10

        # How quickly the game speeds up
        self.speedup_scale = 1.1
        # How quickly alien point values increase
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        ''' Initializes the settings that change throughout the game '''
        print('reset to old speeds')
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1
        # fleet dir : 1 - right and -1 for left
        self.fleet_direction = 1
        # Scoring 
        self.alien_points = 50
    
    def increase_speed(self):
        ''' Increases speed settings '''
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
        print(self.alien_points)

