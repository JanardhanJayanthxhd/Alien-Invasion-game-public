import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    ''' Manage bullets fired from shpip '''

    def __init__(self, ai_settings, screen, ship):
        ''' create bullet object at current ship's position '''
        super().__init__()
        self.screen = screen
    
        # Create bullet rectangle at (0, 0) then set correct position
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width,
                                ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top + 1
        
        # Store bullets position as a decimal
        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        ''' Move bullet up in screen '''
        # Update decimal position of the bullet
        self.y -= self.speed_factor
        # Update the rect position
        self.rect.y = self.y

    def draw_bullet(self):
        ''' Draw the bullet to the screen '''
        pygame.draw.rect(self.screen, self.color, self.rect)
