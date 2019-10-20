import os
import sys
import pygame
from modules import *
from fractions import Fraction


'''Constants'''
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (153, 0, 153)
LIGHT_PURPLE = (255, 204, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
GREEN = (180, 255, 100)
PALETURQUOISE = (175, 238, 238)
AZURE = (0, 204, 204)

# CURRENTPATH = os.path.abspath(os.path.dirname(__file__))
# FONTPATH = os.path.join(CURRENTPATH, 'fonts/font.TTF')
LENGTH = 1920
WIDTH = 1080
# LENGTH = 1080
# WIDTH = 720
SCREENSIZE = (LENGTH, WIDTH)
GROUPTYPES = ['BLANK', 'NUMBER', 'BUTTON']


'''The Puzzle'''
PUZZLEFONT_COLORS = [BLACK, YELLOW]
PUZZLE_COLORS = [PALETURQUOISE, PURPLE, LIGHT_PURPLE]
PUZZLEFONT = 50
PUZZLE_POSITIONS = [(LENGTH*5/36, WIDTH*20/108, LENGTH*5/36, WIDTH*5/36), (LENGTH*10/36, WIDTH*20/108, LENGTH*5/36, WIDTH*5/36), (LENGTH*15/36+10, WIDTH*20/108, LENGTH*5/36, WIDTH*5/36),(LENGTH*20/36+10, WIDTH*20/108, LENGTH*5/36, WIDTH*5/36),
						(LENGTH*5/36, WIDTH*35/108, LENGTH*5/36, WIDTH*5/36), (LENGTH*10/36, WIDTH*35/108, LENGTH*5/36, WIDTH*5/36), (LENGTH*15/36+10, WIDTH*35/108, LENGTH*5/36, WIDTH*5/36), (LENGTH*20/36+10, WIDTH*35/108, LENGTH*5/36, WIDTH*5/36),
						(LENGTH*5/36, WIDTH*50/108+10, LENGTH*5/36, WIDTH*5/36), (LENGTH*10/36, WIDTH*50/108+10, LENGTH*5/36, WIDTH*5/36), (LENGTH*15/36+10, WIDTH*50/108+10, LENGTH*5/36, WIDTH*5/36), (LENGTH*20/36+10, WIDTH*50/108+10, LENGTH*5/36, WIDTH*5/36),
						(LENGTH*5/36, WIDTH*65/108+10, LENGTH*5/36, WIDTH*5/36), (LENGTH*10/36, WIDTH*65/108+10, LENGTH*5/36, WIDTH*5/36), (LENGTH*15/36+10, WIDTH*65/108+10, LENGTH*5/36, WIDTH*5/36), (LENGTH*20/36+10, WIDTH*65/108+10, LENGTH*5/36, WIDTH*5/36)]

'''The Options'''
OPTIONS = [1, 2, 3, 4]
OPTIONSFONT_COLORS = [BLACK, AZURE]
OPTIONS_COLORS = [PALETURQUOISE, YELLOW]
OPTIONSFONT = 50
OPTIONSCARD_POSITIONS = [(LENGTH*11/12, WIDTH*20/108, LENGTH*5/36, WIDTH*5/36), (LENGTH*11/12, WIDTH*35/108, LENGTH*5/36, WIDTH*5/36), (LENGTH*11/12, WIDTH*50/108, LENGTH*5/36, WIDTH*5/36), (LENGTH*11/12, WIDTH*65/108, LENGTH*5/36, WIDTH*5/36)]

'''Buttons'''
BUTTONS = ['RESET', 'NEXT']
BUTTONFONT_COLORS = [BLACK, BLACK]
BUTTONCARD_COLORS = [PALETURQUOISE, ORANGE]
BUTTONFONT = 30
BUTTONCARD_POSITIONS = [(LENGTH*5/36, WIDTH*7/8, LENGTH*5/36, WIDTH*5/36), (LENGTH*11/12, WIDTH*7/8, LENGTH*5/36, WIDTH*5/36)]



'''Find the selected buttons'''
def buttonSelected(group, mouse, group_type, blanks = None):
	selected = []

	if group_type == GROUPTYPES[0]:
		for i, each in enumerate(group):
			x = int(mouse[0])
			y = int(mouse[1])
			if x >= LENGTH/12 and x <= LENGTH*23/36 and y >= WIDTH*5/54 and y <= WIDTH*60/108:
				if each.is_selected:
					each.is_selected = not each.is_selected
			if each.rect.collidepoint(mouse) and (i in blanks):
				each.is_selected = not each.is_selected
			if each.is_selected:
				selected.append(i)
	
	elif group_type == GROUPTYPES[1]:
		for i, each in enumerate(group):
			if each.is_selected:
				each.is_selected = not each.is_selected
			if each.rect.collidepoint(mouse):
				each.is_selected = not each.is_selected
			if each.is_selected:
				selected.append(each.attribute)

	elif group_type == GROUPTYPES[2]:
		for each in group:
			if each.rect.collidepoint(mouse):
				each.is_selected = True
				selected.append(each.attribute)

	return selected


'''Get group of puzzle'''
def getPuzzleGroup(numbers):
	puzzle_group = pygame.sprite.Group()
	for i, number in enumerate(numbers):
		args = (*PUZZLE_POSITIONS[i], str(number), PUZZLEFONT, PUZZLEFONT_COLORS, PUZZLE_COLORS, str(number))
		puzzle_group.add(Card(*args))
	return puzzle_group


'''Get group of options'''
def getOptionGroup(options):
	option_group = pygame.sprite.Group()
	for i, option in enumerate(options):
		args = (*OPTIONSCARD_POSITIONS[i], str(option), OPTIONSFONT, OPTIONSFONT_COLORS, OPTIONS_COLORS, str(option))
		option_group.add(Card(*args))
	return option_group


'''Get group of buttons'''
def getButtonGroup(buttons):
	button_group = pygame.sprite.Group()
	for i, button in enumerate(buttons):
		args = (*BUTTONCARD_POSITIONS[i], str(button), BUTTONFONT, BUTTONFONT_COLORS, BUTTONCARD_COLORS, str(button))
		button_group.add(Button(*args))
	return button_group


'''Show information on screen'''
def showInfo(text, screen, w, h):
	pygame.draw.rect(screen, GREEN, (0, 0, h, w))
	font = pygame.font.SysFont('Consolas', 100)
	screen.blit(font.render(text, True, (0, 0, 0)), ((h-font.size(text)[0])/2, (w-font.size(text)[1])/2))

'''main function of the game'''
def main():
	pygame.init()
	pygame.mixer.init()

	#Get size of screen
	info = pygame.display.Info()

	#width = info.current_w
	width = 1980

	#height = info.current_h
	height = 1080

	SCREENSIZE = (width, height)

	screen = pygame.display.set_mode(SCREENSIZE)

	game_gen = gameGenerator()
	game_gen.generate()

	puzzle_group = getPuzzleGroup(game_gen.puzzle)
	option_group = getOptionGroup(OPTIONS)
	button_group = getButtonGroup(BUTTONS)

	clock = pygame.time.Clock()

	counter = 65

	selected_blank = []
	selected_number = []
	selected_button = []

	blanks = []
	for i in range(len(game_gen.puzzle)):
		if game_gen.puzzle[i] == "?":
			blanks.append(i)

	finished = False
	while True:

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit(-1)
			elif event.type == pygame.MOUSEBUTTONUP:
				mouse_pos = pygame.mouse.get_pos()
				selected_blank = buttonSelected(puzzle_group, mouse_pos, 'BLANK', blanks)
				selected_number = buttonSelected(option_group, mouse_pos, 'NUMBER')
				selected_button = buttonSelected(button_group, mouse_pos, 'BUTTON')
	
		screen.fill((255, 255, 255))

		if len(selected_number) == 1 and len(selected_blank) == 1:
			game_gen.puzzle[selected_blank[0]] = int(selected_number[0])
			print(game_gen.puzzle)

			selected_number = []
			selected_blank = []
			puzzle_group = getPuzzleGroup(game_gen.puzzle)


		for each in puzzle_group:
			each.draw(screen, pygame.mouse.get_pos())
		for each in option_group:
			each.draw(screen, pygame.mouse.get_pos())

		for each in button_group:
			if selected_button and selected_button[0] == "NEXT":
				counter = 60
				print(game_gen.level)
				if game_gen.level == 8:
					finished = True

			if selected_button and each.attribute == selected_button[0]:
				each.is_selected = False
				puzzle_group = each.do(game_gen, getPuzzleGroup, puzzle_group, button_group)
				selected_button = []

				blanks = []
				for i in range(len(game_gen.puzzle)):
					if game_gen.puzzle[i] == "?":
						blanks.append(i)
			each.draw(screen, pygame.mouse.get_pos())

		if counter >= 0:
			if not finished:
				counter -= 1
				showInfo("Ready? Start!", screen, height, width)
			else:
				showInfo("Congrats! You've finished the game", screen, height, width)
	

		pygame.display.flip()
		clock.tick(30)


if __name__ == '__main__':
	main()