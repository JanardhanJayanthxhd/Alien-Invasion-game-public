import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    ''' A class to represent a single alien from the fleet '''

    def __init__(self, ai_settings, screen) -> None:
        ''' Initialize alien and its starting position '''
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Load the alien image and set its rect attribute
        self.image = pygame.image.load('img/ufo-10.bmp')
        self.rect = self.image.get_rect()

        # Start new alien near the top of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height + 500

        # store the aliens start position
        self.x = float(self.rect.x + 500)

    def check_edges(self):
        ''' Return True if any alien reaches either edge '''
        screen_rect = self.screen.get_rect()
        if self.rect.right > screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        ''' Move the alien right '''
        self.x += (self.ai_settings.alien_speed_factor *
                   self.ai_settings.fleet_direction)
        self.rect.x = self.x

    def blitme(self):
        ''' Draw alien at its current position '''
        self.screen.blit(self.image, self.rect)


