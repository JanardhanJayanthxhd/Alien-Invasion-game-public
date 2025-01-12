import pygame.font
from pygame.sprite import Group

from ship import Ship


class Scoreboard():
    ''' A class for scoring information '''

    def __init__(self, ai_settings, screen, stats) -> None:
        ''' Initializes score keeping attributes '''
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats

        # Font setting and color info
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # Prep initial scoreing image
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_ships(self):
        ''' Show how many ships are left '''
        self.ships = Group()
        for ship_no in range(self.stats.ship_left):
            ship = Ship(self.ai_settings, self.screen)
            ship.rect.x = 10 + ship_no * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def prep_level(self):
        ''' Turn level into rendered image '''
        self.level_image = self.font.render(str(self.stats.level), True, 
                                self.text_color, self.ai_settings.screen_bg)

        # Position the level
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_high_score(self):
        ''' Turn high score into rendered image '''
        high_score = int(round(self.stats.high_score, -1))
        high_score_str = "{:,}".format(high_score)
        self.high_score_img = self.font.render(high_score_str, True, 
                                self.text_color, self.ai_settings.screen_bg)
        
        # Create highscore at top-mid of screen 
        self.high_score_rect = self.high_score_img.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.screen_rect.top

    def prep_score(self):
        ''' Turn this score into a rendered image '''
        rounded_score = round(self.stats.score, -1)
        score_str = "{:,}".format(rounded_score)
        self.score_img = self.font.render(score_str, True, self.text_color,
                                          self.ai_settings.screen_bg)

        # Display the score at top-right of screen
        self.score_rect = self.score_img.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_score(self):
        ''' Draw score to the screen '''
        self.screen.blit(self.score_img, self.score_rect)
        self.screen.blit(self.high_score_img, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)

