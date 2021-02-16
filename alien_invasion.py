import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from gamestats import GameStats
from time import sleep

class AlienInvasion:
    """Overall class to manage game assets and behavior"""

    def __init__(self):
        """Initialize pygame resources"""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion 2021")

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.gamestats = GameStats(self)
        self._create_fleet()


    def run_game(self):
        while True:
            # Watch for keyboard and mouse events
            self._check_events()

            if self.gamestats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            
            self._update_screen()

    def _check_events(self):
        # Method to handle events
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self._check_keydown_events(event)
                elif event.type == pygame.KEYUP:
                    self._check_keyup_events(event)
        
    
    def _update_screen(self):
        # Update screen after every event
        # Fill bg color
        self.screen.fill(self.settings.bg_color)
        # Draw ship 
        self.ship.blitme()
        # Draw bullets
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        # Make the most recent screen visible
        self.aliens.draw(self.screen)
        pygame.display.flip()

    
    def _check_keydown_events(self,event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    
    def _check_keyup_events(self,event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    
    def _fire_bullet(self):
        """Create a new bullet and add it to the group"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    
    def _update_bullets(self):
        """ Fire bullets and update bullet position """
        self.bullets.update()
        # Delete bullets after it leaves the screen
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0 :
                self.bullets.remove(bullet)
        #print(len(self.bullets))
        self._check_bullets_aliens_collision()

    
    def _create_fleet(self):
        """ Create a fleet of aliens """
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # Determine the number of rows of aliens 
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - alien_height)
        number_rows = available_space_y // (5 * alien_height)

        # Create first row of aliens
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                # Create an alien x and place it in a row
                self._create_alien(alien_number,row_number)
        
    
    def _create_alien(self,alien_number,row_number):
        """ Create an alien and place it in a row """
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    
    def _update_aliens(self):
        """ Check if the fleet hits edge, then change direction """
        self._check_fleet_edges()
        self.aliens.update()

        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            self._ship_hit()
        
        self._check_aliens_bottom()
    
    
    def _check_fleet_edges(self):
        """Tells if an alien fleet hits the edge"""
        for alien in self.aliens.sprites():
            if alien._check_edges():
                self._change_fleet_direction()
                break
    
    
    def _change_fleet_direction(self):
        """Drop the entire fleet and change its direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    
    def _check_bullets_aliens_collision(self):

        collisions = pygame.sprite.groupcollide(self.bullets,self.aliens,True,True)

        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()

    
    def _ship_hit(self):

        if self.gamestats.ships_left > 0:
            self.gamestats.ships_left -= 1

            self.aliens.empty()
            self.bullets.empty()

            self._create_fleet()
            self.ship._center_ship()

            sleep(1.0)
        
        else:
            self.gamestats.game_active = False

    
    def _check_aliens_bottom(self):
        """Check if the aliens hit the screen bottom"""
        screen_rect = self.screen.get_rect()

        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

if __name__ == '__main__':
    # Make a game instance
    ai = AlienInvasion()
    # Run the game
    ai.run_game()
