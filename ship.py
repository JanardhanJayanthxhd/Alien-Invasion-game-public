
import pygame

class Ship():
    def __init__(self, ai_settings, screen) -> None:
        ''' Initialize a ship and its initial position '''
        self.screen = screen
        self.ai_settings = ai_settings

        # Load the ship image and get its rect.
        self.image = pygame.image.load('img/rocket.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # start each new ship at the bottom of the screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # Center for ships center 
        self.center = float(self.rect.centerx)

        # Right and left flag
        self.move_right = False
        self.move_left = False

    def update(self):
        ''' Update ship's position based on flag '''
        if self.move_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.move_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor

        # Updating rect obj from sefl.center
        self.rect.centerx = int(self.center)

    def blitme(self):
        """ Draw the ship at its current location """
        self.screen.blit(self.image, self.rect)



