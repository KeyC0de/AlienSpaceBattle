import pygame
from random import randrange
from pygame.sprite import Sprite


class Star(Sprite):
	""" class describes a raindrop object """
	
	def __init__(self, screen, options):
		
		super(Star, self).__init__()
		self.screen = screen
		
		self.img = pygame.image.load('images/star.png').convert_alpha()
		self.img = pygame.transform.scale(self.img, (40,40))
		self.rect = self.img.get_rect()
		
		# draw on screen
		self.rect.x = randrange(0, options.screenWidth - self.rect.width)
		self.rect.y = randrange(0, options.screenHeight - self.rect.height)

		self.x = float(self.rect.x)
		self.y = float(self.rect.y)
	

	def draw(self):
		""" Set raindrop on the screen """
		
		self.screen.blit(self.img, self.rect)