# 3rd party modules
import pygame
import libtcodpy as libtcod

# Game Files
import constants


class struc_Tile:
	def __init__(self, block_path):
		self.block_path = block_path


# Create map
def map_create():
	new_map = [[struc_Tile(False) for y in range(0, constants.MAP_HEIGHT)] for x in range(0, constants.MAP_WIDTH)]

	new_map[10][10].block_path = True
	new_map[10][15].block_path = True

	return new_map


# Function to draw game
def draw_game():
	global SURFACE_MAIN
	# Clear the surface
	SURFACE_MAIN.fill(constants.COLOR_DEFAULT_BG)

	# Draw the map
	draw_map(GAME_MAP)

	# Draw character
	SURFACE_MAIN.blit(constants.SPR_PLAYER, (200, 200))

	# Update display
	pygame.display.flip()


def draw_map(map_to_draw):
	for x in range(0, constants.MAP_WIDTH):
		for y in range(0, constants.MAP_HEIGHT):
			# Draw wall
			if map_to_draw[x][y].block_path == True:
				SURFACE_MAIN.blit(constants.SPR_WALL, (x * constants.CELL_WIDTH, y * constants.CELL_HEIGHT))
			# Draw floor
			else:
				SURFACE_MAIN.blit(constants.SPR_FLOOR, (x * constants.CELL_WIDTH, y * constants.CELL_HEIGHT))


# Function to loop main game
def game_main_loop():
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


# Function to initialize the game
def game_initialize():

	global SURFACE_MAIN, GAME_MAP

	# Initialize pygame
	pygame.init()

	SURFACE_MAIN = pygame.display.set_mode(
		(constants.GAME_WIDTH, constants.GAME_HEIGHT))

	GAME_MAP = map_create()


# Execute Game
if __name__ == '__main__':
	game_initialize()
	game_main_loop()
