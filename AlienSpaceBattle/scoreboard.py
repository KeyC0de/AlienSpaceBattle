import pygame.font
from pygame.sprite import Group
from ship import Ship


class Scoreboard():
	"""Display scoring information"""

	def __init__(self, options, screen, stats):
		self.screen = screen
		self.screenRect = screen.get_rect()
		self.options = options
		self.stats = stats

		# font settings
		self.textColor = (255, 140, 0)
		self.levelColor = (120, 230, 30)
		self.font = pygame.font.SysFont(None, 42)

		self.prepScoreboard()

	# prep methods turn text into a rendered image ready for rendering
	def prepScoreboard(self):
		self.prepLevel()
		self.prepScore()
		self.prepHighScore()
		self.prepShips()

	def prepScore(self):
		scoreStr = str(self.stats.score)
		self.scoreImg = self.font.render(scoreStr, True, self.textColor, self.options.bgColor)

		# display the score at the top left of the screen
		self.scoreRect = self.scoreImg.get_rect()
		self.scoreRect.right = self.screenRect.left + 60
		self.scoreRect.top = 40

	def prepHighScore(self):
		scoreStr = str(self.stats.highscore)
		self.highScoreImg = self.font.render(scoreStr, True, self.textColor, self.options.bgColor)

		# center high score atop the screen
		self.highScoreRect = self.highScoreImg.get_rect()
		self.highScoreRect.centerx = self.screenRect.centerx
		self.highScoreRect.top = 40

	def prepLevel(self):
		levelStr = str(self.stats.level)
		self.levelImg = self.font.render(levelStr, True, self.levelColor, self.options.bgColor)

		# display the score at the top right of the screen
		self.levelRect = self.levelImg.get_rect()
		self.levelRect.right = self.screenRect.left + 60
		self.levelRect.top = 80

	def prepShips(self):
		"""Show how many ships are left"""
		self.ships = Group()
		for i in range(self.stats.shipsLeft):
			ship = Ship(self.options, self.screen)
			ship.rect.x = (self.screenRect.right - 200) + i * (ship.rect.width + 5)
			ship.rect.y = 10
			self.ships.add(ship)

	def displayScore(self):
		self.screen.blit(self.scoreImg, self.scoreRect)
		self.screen.blit(self.highScoreImg, self.highScoreRect)
		self.ships.draw(self.screen)

	def displayLevel(self):
		self.screen.blit(self.levelImg, self.levelRect)