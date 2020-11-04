import pygame
from pygame.sprite import Sprite

class Missile(Sprite):
    """ A class to manage missiles fired from ship. """
    
    def __init__(self, options, screen, ship):
        """ Create a missile object. """
        
        super(Missile, self).__init__()
        self.screen = screen
        
        # load alien image and set its rectangle
        self.image = pygame.image.load("images/missile_small.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = ship.rect.centerx
        self.rect.y = self.rect.bottom = ship.rect.bottom
        
        # store position
        self.y = float(self.rect.y)
        
        # misc settings
        self.speedFactor = options.missileSpeedFactor
    
    
    def updateMissilePosition(self):
        """ Move Missile """
        
        self.y -= self.speedFactor
        self.rect.y = self.y
    
    def drawMissile(self):
        """ Draws bullet to the screen."""
        
        self.screen.blit(self.image, self.rect)

