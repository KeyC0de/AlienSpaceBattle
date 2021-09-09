import pygame
from pygame.sprite import Sprite


class Bullet( Sprite ):
    """ A class to manage bullets fired from the ship"""
    
    def __init__(self, options, screen, ship):
        """ Create a bullet object at the ship's current position. """
        
        super(Bullet, self).__init__()
        self.screen = screen
        
        # create a bullet rect at (0, 0) and then set correct position
        self.rect = pygame.Rect(0, 0, options.bulletWidth,
                                        options.bulletHeight)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top
        
        # store the bullet's position as a floating value
        self.y = float(self.rect.y)
        
        # misc settings
        self.color = options.bulletColor
        self.speedFactor = options.bulletSpeedFactor
    
    
    def update(self): # inherited from Sprite
        """Move the bullet"""
        
        self.y -= self.speedFactor
        self.rect.y = self.y
    
    def drawBullet(self):
        """ Draws bullet to the screen."""
        
        pygame.draw.rect(self.screen, self.color, self.rect)

