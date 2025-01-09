import sys

import pygame


def check_key_down_events(event, ship):
    ''' Respond to keypresses '''
    if event.key == pygame.K_RIGHT:
        ship.move_right = True
    if event.key == pygame.K_LEFT:
        ship.move_left = True

def check_key_release_events(event, ship):
    ''' Respond to key releases '''
    if event.key == pygame.K_RIGHT:
        ship.move_right = False
    if event.key == pygame.K_LEFT:
        ship.move_left = False



def check_events(ship):
    ''' Respond to keypress and mouse events '''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_key_down_events(event, ship)
        elif event.type == pygame.KEYUP:
            check_key_release_events(event, ship)

def update_screen(ai_settings, screen, ship):
    '''Update image to the screen and flip to new screen'''
    screen.fill(ai_settings.screen_bg)
    ship.blitme()

    pygame.display.flip()


