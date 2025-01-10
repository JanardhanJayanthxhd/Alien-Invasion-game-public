import sys
import pygame
from random import randint

from bullet import Bullet
from alien import Alien


def get_number_rows(ai_settings, ship_height, alien_height):
    ''' Determine the number of rows of aliens that fit into the screen '''
    available_space_y = (ai_settings.screen_height - 
                         (10 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def get_number_aliens_x(ai_settings, alien_width):
    ''' Returns the number of aliens per row '''
    available_space_x = ai_settings.screen_width - (2 * alien_width)
    number_aliens_x = available_space_x // (2 * alien_width)
    return number_aliens_x

def create_alien(ai_settings, screen, aliens, alien_no, row_number):
    ''' Creat an alien and place it in the row '''
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_no
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
    ''' Creates a fleet of aliens onto the screen '''
    # Create an alien and find the number of aliens in a row
    # Spacing between each alien is one alien width
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, 
                                  alien.rect.height)

    # Create the first row of aliens
    for row_no in range(number_rows):
        for alien_no in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_no, row_no)

def fire_bullet(ai_settings, screen, ship, bullets):
    ''' Fire a bullet if limit not reached '''
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def check_key_down_events(event, ai_settings, screen, ship, bullets):
    ''' Respond to keypresses '''
    if event.key == pygame.K_RIGHT:
        ship.move_right = True
    if event.key == pygame.K_LEFT:
        ship.move_left = True
    if event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    if event.key == pygame.K_q:
        sys.exit() 


def check_key_release_events(event, ship):
    ''' Respond to key releases '''
    if event.key == pygame.K_RIGHT:
        ship.move_right = False
    if event.key == pygame.K_LEFT:
        ship.move_left = False

def check_events(ai_settings, screen, ship, bullets):
    ''' Respond to keypress and mouse events '''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_key_down_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_key_release_events(event, ship)

def build_stars(star, height, width):
    ''' Add star to random x and x coordinates on the screen'''
    x = randint(0, width - 5)
    y = randint(0, height - 5)
    star.build_star(x, y)

def update_screen(ai_settings, screen, star, ship, aliens, bullets):
    '''Update image to the screen and flip to new screen'''
    screen.fill(ai_settings.screen_bg)
    
    # width and height of screen
    width, height = screen.get_size()
    build_stars(star, height, width)
    star.update_stars()

    # Redraw all bullets behind ship and aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()
    aliens.draw(screen)

    pygame.display.flip()

def update_bullets(ai_settings, screen, ship, aliens, bullets):
    ''' Updates the position of bullets and gets rid of old ones '''
    # Update bullets
    bullets.update()

    # Get rid of bullets that disappear
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    
    check_bullet_alien_collision(ai_settings, screen, ship, bullets, aliens)

def check_bullet_alien_collision(ai_settings, screen, ship, bullets, aliens):
    ''' Check for alien - bullet collision '''
    # check for any bullets that have hit alien ship
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if len(aliens) == 0:
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)


def check_fleet_edges(ai_settings, aliens):
    ''' respond appropriately if any alien reached edge of screen ''' 
    for alien in aliens:
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    ''' Drop the entire fleet and change fleet direction '''
    for alien in aliens:
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def update_aliens(ai_settings, ship, aliens):
    ''' Update the positions of all aliens '''
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # Look for alien-ship collision 
    if pygame.sprite.spritecollideany(ship, aliens):
        print('Ship Down!!!')
