

class Settings():
    ''' A class to store all settings '''
    def __init__(self) -> None:
        ''' Initializes game's settings '''
        self.screen_width = 1000
        self.screen_height = 800
        self.screen_bg = (28, 14, 96)

        # Ship's settings
        self.ship_speed_factor = 1.5
