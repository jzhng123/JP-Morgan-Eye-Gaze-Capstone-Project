import copy
import random
import pygame

LENGTH = 1280
WIDTH = 720
BLACK = [0,0,0]

class Card(pygame.sprite.Sprite):
	def __init__(self, x, y, width, height, text, font, font_colors, bg_colors, attribute, **kwargs):
		pygame.sprite.Sprite.__init__(self)
		self.rect = pygame.Rect(x, y, width, height)
		self.text = text
		self.attribute = attribute
		self.font_info = font
		self.font = pygame.font.SysFont("comicsansms", font)
		self.font_colors = font_colors
		self.is_selected = False
		self.select_order = None
		self.bg_colors = bg_colors
	def draw(self, screen, mouse_pos):
		pygame.draw.rect(screen, self.bg_colors[1], self.rect, 0)

		pygame.draw.rect(screen, BLACK, [LENGTH*5/36, WIDTH*35/108, LENGTH*20/36+10, 3])
		pygame.draw.rect(screen, BLACK, [LENGTH*5/36, WIDTH*50/108, LENGTH*20/36+10, 10])
		pygame.draw.rect(screen, BLACK, [LENGTH*5/36, WIDTH*65/108+10, LENGTH*20/36+10, 3])

		pygame.draw.rect(screen, BLACK, [LENGTH*10/36, WIDTH*10/54, 3, WIDTH*20/36+10])
		pygame.draw.rect(screen, BLACK, [LENGTH*15/36, WIDTH*10/54, 10, WIDTH*20/36+10])
		pygame.draw.rect(screen, BLACK, [LENGTH*20/36+10, WIDTH*10/54, 3, WIDTH*20/36+10])

		pygame.draw.rect(screen, BLACK, [LENGTH*11/12, WIDTH*35/108, LENGTH*5/36, 3])
		pygame.draw.rect(screen, BLACK, [LENGTH*11/12, WIDTH*50/108, LENGTH*5/36, 3])
		pygame.draw.rect(screen, BLACK, [LENGTH*11/12, WIDTH*65/108, LENGTH*5/36, 3])

		if self.text == "?":
			pygame.draw.rect(screen, self.bg_colors[2], self.rect, 0)
			if self.rect.collidepoint(mouse_pos):
				pygame.draw.rect(screen, self.bg_colors[0], self.rect, 0)

		font_color = self.font_colors[self.is_selected]
		text_render = self.font.render(self.text, True, font_color)
		font_size = self.font.size(self.text)
		screen.blit(text_render, (self.rect.x+(self.rect.width-font_size[0])/2,
								  self.rect.y+(self.rect.height-font_size[1])/2))



class Button(Card):
	def __init__(self, x, y, width, height, text, font, font_colors, bg_colors, attribute, **kwargs):
		Card.__init__(self, x, y, width, height, text, font, font_colors, bg_colors, attribute)

	def do(self, game_gen, func, sprites_group, objs):
		if self.attribute == 'NEXT':
			for obj in objs:
				obj.font = pygame.font.SysFont("comicsansms", obj.font_info)
				obj.text = obj.attribute
			self.font = pygame.font.SysFont("comicsansms", self.font_info)
			self.text = self.attribute
			game_gen.generate(True)
			sprites_group = func(game_gen.puzzle)

		elif self.attribute == 'RESET':
			for obj in objs:
				obj.font = pygame.font.SysFont("comicsansms", obj.font_info)
				obj.text = obj.attribute

			game_gen.puzzle = game_gen.puzzle_ori
			sprites_group = func(game_gen.puzzle)

		return sprites_group


class gameGenerator():
	def __init__(self):
		self.level = 0
		self.info = 'gameGenerator'
	def generate(self, next_level = False):
		self.__reset()

		if next_level:
			self.level += 1
		
		self.puzzle_ori = self.__game(self.level)
		self.puzzle = copy.deepcopy(self.puzzle_ori)

	def __reset(self):
		self.puzzle = []
		self.puzzle_ori = []

	def __game(self, level):

		#easy
		if level == 0:
			self.puzzle = [1, "?", 3, 4, 4, 3, 2, 1, 2, 4, "?", 3, 3, 1, 4, 2]
		elif level == 1:
			self.puzzle = [2, 4, 3, 1, 3, 1, 4, 2, 1, 3, "?", 4, 4, "?", 1, 3]
		elif level == 2:
			self.puzzle = ["?", 2, 4, 1, 4, 1, 3, 2, 2, 4, "?", 3, 1, 3, 2, 4]
		elif level == 3:
			self.puzzle = [2, 4, "?", 3, 3, 1, 2, 4, 1, 3, 4, "?", 4, 2, 3, 1]
		#medium
		elif level == 4:
			self.puzzle = ["?", 3, 1, "?", 1, "?", "?", 3, 2, "?", 3, 4, "?", 4, 2, "?"]
		elif level == 5:
			self.puzzle = [2, 4, 3, 1, 3, "?", 4, "?", "?", 3, "?", "?", "?", "?", "?", 3]
		elif level == 6:
			self.puzzle = [3, "?", 1, "?", "?", 1, "?", 3, "?", 3, 4, "?", 1, 4, "?", 2]
		elif level == 7:
			self.puzzle = [1, "?", 2, 3, "?", 3, "?", 4, 3, "?", 4, "?", "?", 1, "?", 2]

		#hard
		elif level == 8:
			self.puzzle = [2, "?", "?", "?", "?", "?", 4, "?", "?", 3, "?", "?", "?", "?", "?", 3]
		elif level == 9:
			self.puzzle = ["?", 4, "?", "?", "?", "?", 3, "?", "?", 2, "?", "?", 1, "?", "?", "?"]
		elif level == 10:
			self.puzzle = ["?", "?", "?", 3, "?", 3, 4, "?", "?", "?", 2, "?", "?", 2, "?", "?"]
		elif level == 11:
			self.puzzle = ["?", "?", 1, "?", "?", "?", "?", "?", "?", 3, "?", 2, "?", 2, "?", "?"]
		
		return self.puzzle