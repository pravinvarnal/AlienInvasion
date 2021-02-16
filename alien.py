import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """ A class to manage alien ship """

    def __init__(self,ai_game):

        super().__init__()
        self.screen = ai_game.screen

        # Load the alien image and set the alien rect
        self.image = pygame.image.load('images/ufo.png')
        self.rect = self.image.get_rect()

        # Start new alien at the top-left of screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact horizontal position 
        self.x = float(self.rect.x)
        self.settings = ai_game.settings

    def update(self):
        """Move the alien to the right"""
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x
    
    def _check_edges(self):
        """ Return true if an alien hits the edge """
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

