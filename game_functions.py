import sys
import pygame
from random import randint
from time import sleep

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


def check_key_down_events(event, ai_settings, screen, stats, sb, ship,
                          aliens, bullets):
    ''' Respond to keypresses '''
    if event.key == pygame.K_RIGHT:
        ship.move_right = True
    if event.key == pygame.K_LEFT:
        ship.move_left = True
    if event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    if event.key == pygame.K_q:
        sys.exit() 
    if event.key == pygame.K_p:
        start_game(ai_settings, screen, stats, sb, ship, aliens, bullets)

def check_key_release_events(event, ship):
    ''' Respond to key releases '''
    if event.key == pygame.K_RIGHT:
        ship.move_right = False
    if event.key == pygame.K_LEFT:
        ship.move_left = False

def check_events(ai_settings, screen, stats, sb, play_btn, aliens,
                 ship, bullets):
    ''' Respond to keypress and mouse events '''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_key_down_events(event, ai_settings, screen, stats, sb,
                                  ship, aliens, bullets)
        elif event.type == pygame.KEYUP:
            check_key_release_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, 
                              play_btn, ship, aliens, bullets, mouse_x, mouse_y)

def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
    ''' Check if any alien has reached bottom of the screen '''
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)

def check_play_button(ai_settings, screen, stats, sb, play_btn, ship, aliens,
                      bullets, mouse_x, mouse_y):
    ''' Start a new game when user clicks play '''
    button_clicket = play_btn.rect.collidepoint(mouse_x, mouse_y)
    if button_clicket and not stats.game_active:
        # Reset game settings 
        ai_settings.initialize_dynamic_settings()
        start_game(ai_settings, screen, stats, sb, ship, aliens, bullets)

def start_game(ai_settings, screen, stats, sb, ship, aliens, bullets):
    ''' Starts the game '''
    # Reset game stats
    stats.reset_stats()
    stats.game_active = True

    # Reset scoreboard images
    sb.prep_score()
    sb.prep_high_score()
    sb.prep_level()
    sb.prep_ships()

    # Empty aliens and bullets
    aliens.empty()
    bullets.empty()

    # Create new fleet and  center the ship
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()

def build_stars(star, height, width):
    ''' Add star to random x and x coordinates on the screen'''
    x = randint(0, width - 5)
    y = randint(0, height - 5)
    star.build_star(x, y)

def update_screen(ai_settings, screen, stats, sb,
                  star, ship, aliens, bullets, play_btn):
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

    # Draw score info
    sb.show_score()

    if not stats.game_active:
        play_btn.draw_button()

    pygame.display.flip()

def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    ''' Updates the position of bullets and gets rid of old ones '''
    # Update bullets
    bullets.update()

    # Get rid of bullets that disappear
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    
    check_bullet_alien_collision(ai_settings, screen, stats, sb,
                                 ship, bullets, aliens)

def check_bullet_alien_collision(ai_settings, screen, stats, sb,
                                 ship, bullets, aliens):
    ''' Check for alien - bullet collision '''
    # check for any bullets that have hit alien ship
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    
    if collisions:
        for hit_aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(hit_aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        # Destroy existing bullets, step up game speed, create new fleet
        bullets.empty()
        ai_settings.increase_speed()

        # Increase level
        stats.level += 1
        sb.prep_level()

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

def update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets):
    ''' Update the positions of all aliens '''
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # Look for alien-ship collision 
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)

    # Look for aliens hitting/reaching bottom of the screen 
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)

def ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets):
    ''' Respond to ship being hit by aliens '''
    if stats.ship_left > 0:
        stats.ship_left -= 1
        
        # Update scoreboard
        sb.prep_ships()

        # Hide the mouse cursor. 
        pygame.mouse.set_visible(False)

        # Empty the list of aliens and bullets 
        aliens.empty()
        bullets.empty()
        # Create a new fleet and center the ship
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        sleep(1)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_high_score(stats, sb):
    ''' Check and update high score '''
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
