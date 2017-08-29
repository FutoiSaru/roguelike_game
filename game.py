# 3rd party modules
import pygame
import libtcodpy as libtcod

# Game Files
import constants


# STRUCTS
class struc_Tile:
	def __init__(self, block_path):
		self.block_path = block_path


# OBJECTS
class obj_Actor:
	def __init__(self, x, y, name_object, sprite, creature=None, ai=None):
		# Map address
		self.x = x
		self.y = y
		self.sprite = sprite
		self.creature = creature
		self.ai = ai

		if creature:
			creature.owner = self

		if ai:
			ai.owner = self

	def draw(self):
		SURFACE_MAIN.blit(self.sprite, (self.x * constants.CELL_WIDTH, self.y * constants.CELL_HEIGHT))

	def move(self, dx, dy):
		if GAME_MAP[self.x + dx][self.y + dy].block_path is False:
			self.x += dx
			self.y += dy


# COMPONENTS
class com_Creature:
	# Creatures have health, can damage other objects by attacking and can die
	def __init__(self, name_instance, hp=10):
		self.name_instance = name_instance
		self.hp = hp


# TODO class com_Item:

# TODO class com_Container:

# AI
class ai_Test:
	# Once per turn execute
	def take_turn(self):
		self.owner.move(-1, 0)


# MAP
# Create map
def map_create():
	new_map = [[struc_Tile(False) for y in range(0, constants.MAP_HEIGHT)] for x in range(0, constants.MAP_WIDTH)]

	new_map[10][10].block_path = True
	new_map[10][15].block_path = True

	return new_map


# DRAWING
# Function to draw game
def draw_game():
	global SURFACE_MAIN
	# Clear the surface
	SURFACE_MAIN.fill(constants.COLOR_DEFAULT_BG)

	# Draw the map
	draw_map(GAME_MAP)

	# Draw character
	for obj in GAME_OBJECTS:
		obj.draw()

	# Update display
	pygame.display.flip()


def draw_map(map_to_draw):
	for x in range(0, constants.MAP_WIDTH):
		for y in range(0, constants.MAP_HEIGHT):
			# Draw wall
			if map_to_draw[x][y].block_path is True:
				SURFACE_MAIN.blit(constants.SPR_WALL, (x * constants.CELL_WIDTH, y * constants.CELL_HEIGHT))
			# Draw floor
			else:
				SURFACE_MAIN.blit(constants.SPR_FLOOR, (x * constants.CELL_WIDTH, y * constants.CELL_HEIGHT))


# GAME
# Function to loop main game
def game_main_loop():
	game_quit = False
	player_action = "no-action"

	while not game_quit:
		# Handle player input
		player_action = game_handle_keys()

		if player_action == "QUIT":
			game_quit = True

		elif player_action != "no-action":
			for obj in GAME_OBJECTS:
				if obj.ai:
					obj.ai.take_turn()

		# Draw game
		draw_game()


# Function to initialize the game
def game_initialize():

	global SURFACE_MAIN, GAME_MAP, PLAYER, ENEMY, GAME_OBJECTS

	# Initialize pygame
	pygame.init()

	SURFACE_MAIN = pygame.display.set_mode(
		(constants.GAME_WIDTH, constants.GAME_HEIGHT))

	GAME_MAP = map_create()

	creature_com1 = com_Creature("Greg")
	PLAYER = obj_Actor(0, 0, "Python", constants.SPR_PLAYER, creature=creature_com1)

	creature_com2 = com_Creature("Jack")
	ai_com = ai_Test()
	ENEMY = obj_Actor(15, 15, "Crab", constants.SPR_ENEMY, creature=creature_com2, ai=ai_com)

	GAME_OBJECTS = [PLAYER, ENEMY]


def game_handle_keys():
	# Get player input
	events_list = pygame.event.get()

	# Process input
	for event in events_list:
		# Quit game
		if event.type == pygame.QUIT:
			return "QUIT"

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				PLAYER.move(0, -1)
				return "Player moved"
			if event.key == pygame.K_DOWN:
				PLAYER.move(0, 1)
				return "Player moved"
			if event.key == pygame.K_LEFT:
				PLAYER.move(-1, 0)
				return "Player moved"
			if event.key == pygame.K_RIGHT:
				PLAYER.move(1, 0)
				return "Player moved"

	return "no-action"


# Execute Game
if __name__ == '__main__':
	game_initialize()
	game_main_loop()
