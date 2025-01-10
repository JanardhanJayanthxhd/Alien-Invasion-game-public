"""
--- Alien Invation --- 
description : In Alien Invasion, the player controls a ship that appears at
the bottom center of the screen. The player can move the ship
right and left using the arrow keys and shoot bullets using the
spacebar. When the game begins, a fleet of aliens fills the sky
and moves across and down the screen. The player shoots and
destroys the aliens. If the player shoots all the aliens, a new fleet
appears that moves faster than the previous fleet. If any alien hits
the player’s ship or reaches the bottom of the screen, the player
loses a ship. If the player loses three ships, the game ends.
"""

import pygame
from pygame.sprite import Group

from alien import Alien
from settings import Settings
from ship import Ship
from star import Star
import game_functions as gf 

def run_game():
    # pygame setup
    pygame.init()

    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height)
    )
    pygame.display.set_caption("Alien Invation")

    # Create a ship, star, Group of bullets and aliens
    ship = Ship(ai_settings, screen)  
    star = Star(screen)
    bullets = Group()
    aliens = Group()


    # Creating a fleet of aliens 
    gf.create_fleet(ai_settings, screen, ship, aliens)

    while True:
        gf.check_events(ai_settings, screen, ship, bullets)
        ship.update()
        gf.update_bullets(bullets)
        gf.update_screen(ai_settings, screen, star, ship, aliens, bullets) 

run_game()

