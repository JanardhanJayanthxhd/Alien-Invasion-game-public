import pygame


class Star():
    def __init__(self, screen) -> None:
        ''' Initializes a star '''
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.star = pygame.image.load('../alien invation/img/star-fin.bmp')
        self.star_rect = self.star.get_rect()
        
        self.active_stars = []
        self.star_limit = 30

    def build_star(self, x, y, lifetime=100):
        ''' Updates the acitve stars list with a new star '''
        if len(self.active_stars) <= self.star_limit:
            self.active_stars.append({'position': (x, y), 'lifetime': lifetime})

    def update_stars(self):
        ''' 
        Updates sceen with the stars from active_stars list and
        cleans that list once liftime is 0 
        '''
        for star in self.active_stars[:]:
            self.screen.blit(self.star, star['position'])

            star['lifetime'] -= 1

            if star['lifetime'] <= 0:
                self.active_stars.remove(star)

