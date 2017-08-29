# 3rd party modules
import pygame
import libtcodpy as libtcod

# Game Files
import constants


def draw_game():

	global SURFACE_MAIN

	# Clear the surface
	SURFACE_MAIN.fill(constants.COLOR_DEFAULT_BG)

	# TODO Draw the map

	# Draw character
	SURFACE_MAIN.blit(constants.SPR_PLAYER, (200, 200))

	# Update display
	pygame.display.flip()


def game_main_loop():
	# Function to loop main game
	game_quit = False

	while not game_quit:

		# Get player input
		events_list = pygame.event.get()

		# Process input
		for event in events_list:
			# Quit game
			if event.type == pygame.QUIT:
				game_quit = True

		# Draw game
		draw_game()

	# Quit the game
	pygame.quit()
	exit()


def game_initialize():
	# Function to initialize the game

	global SURFACE_MAIN

	# Initialize pygame
	pygame.init()

	SURFACE_MAIN = pygame.display.set_mode((constants.GAME_WIDTH, constants.GAME_HEIGHT))


if __name__ == '__main__':
	game_initialize()
	game_main_loop()
