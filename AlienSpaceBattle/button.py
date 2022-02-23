import pygame.font


class Button():

	def __init__(self, options, screen, msg):
		self.screen = screen
		self.screen_rect = screen.get_rect()

		# button properties
		self.width, self.height = 200, 50
		self.color = (0, 255, 0)
		self.textColor = (255, 255, 255)
		self.font = pygame.font.SysFont(None, 48)   # None = default font

		# Build button's rect and center it
		self.rect = pygame.Rect(0, 0, self.width, self.height)
		self.rect.center = self.screen_rect.center

		# button text
		self.prepareMessage(msg)

	def prepareMessage(self, msg):
		"""Turn msg into a rendered image and center text on the button"""
		self.msgImage = self.font.render(msg, True, self.textColor, self.color)
		self.msgImageRect = self.msgImage.get_rect()
		self.msgImageRect.center = self.rect.center

	def draw(self):
		'''draw blank button and then draw message'''
		self.screen.fill(self.color, self.rect)
		self.screen.blit(self.msgImage, self.msgImageRect)