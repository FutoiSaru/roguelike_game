# 3rd party modules
import pygame
import libtcodpy as libtcod

# Game Files
import constants


# STRUCTS
class struc_Tile:
	def __init__(self, block_path):
		self.block_path = block_path
		self.explored = False


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

	# Draw function
	def draw(self):
		is_visible = libtcod.map_is_in_fov(FOV_MAP, self.x, self.y)

		if is_visible:
			SURFACE_MAIN.blit(self.sprite, (self.x * constants.CELL_WIDTH, self.y * constants.CELL_HEIGHT))


# COMPONENTS
class com_Creature:
	# Creatures have health, can damage other objects by attacking and can die
	def __init__(self, name_instance, hp=10, death_function=None):
		self.name_instance = name_instance
		self.maxhp = hp
		self.hp = hp
		self.death_function = death_function

	# Move function
	def move(self, dx, dy):
		tile_is_wall = GAME_MAP[self.owner.x + dx][self.owner.y + dy].block_path is True
		target = map_check_for_creatures(self.owner.x + dx, self.owner.y + dy, self.owner)

		if target:
			self.attack(target, 3)

		# Move if tile isn't a wall and no target
		if not tile_is_wall and target is None:
			self.owner.x += dx
			self.owner.y += dy

	def attack(self, target, damage):
		print self.name_instance + " attacks " + target.creature.name_instance + " for " + str(damage) + " damage!"
		target.creature.take_damage(damage)

	def take_damage(self, damage):
		self.hp -= damage
		print self.name_instance + "'s health is " + str(self.hp) + "/" + str(self.maxhp)

		if self.hp <= 0:
			if self.death_function is not None:
				self.death_function(self.owner)

# TODO class com_Item:

# TODO class com_Container:


# AI
class ai_Test:
	# Once per turn execute
	def take_turn(self):
		self.owner.creature.move(libtcod.random_get_int(0, -1, 1), libtcod.random_get_int(0, -1, 1))


def death_monster(monster):
		print monster.creature.name_instance + " is dead!"
		monster.creature = None
		monster.ai = None


# MAP
# Create map
def map_create():
	new_map = [[struc_Tile(False) for y in range(0, constants.MAP_HEIGHT)] for x in range(0, constants.MAP_WIDTH)]

	new_map[10][10].block_path = True
	new_map[10][15].block_path = True

	# Create walls on top and bottom
	for x in range(constants.MAP_WIDTH):
		new_map[x][0].block_path = True
		new_map[x][constants.MAP_HEIGHT - 1].block_path = True

	# Create walls on left and right
	for y in range(constants.MAP_HEIGHT):
		new_map[0][y].block_path = True
		new_map[constants.MAP_WIDTH - 1][y].block_path = True

	map_make_fov(new_map)

	return new_map


def map_check_for_creatures(x, y, exclude_object=None):
	target = None

	if exclude_object:
		for object in GAME_OBJECTS:
			# Check if object is not, if it is where we want to move and whether it is a creature
			if (object is not exclude_object and 
				object.x == x and 
				object.y == y and 
				object.creature):
				target = object

			if target:
				return target

	else:
		for object in GAME_OBJECTS:
			# Check if object is not, if it is where we want to move and whether it is a creature
			if (object.x == x and 
				object.y == y and 
				object.creature):
				target = object

			if target:
				return target	


def map_make_fov(incoming_map):
	global FOV_MAP

	FOV_MAP = libtcod.map_new(constants.MAP_WIDTH, constants.MAP_HEIGHT)

	for y in range(constants.MAP_HEIGHT):
		for x in range(constants.MAP_WIDTH):
			libtcod.map_set_properties(FOV_MAP, x, y, not incoming_map[x][y].block_path, not incoming_map[x][y].block_path)


def map_calculate_fov():
	global FOV_CALCULATE

	if FOV_CALCULATE:
		FOV_CALCULATE = False
		libtcod.map_compute_fov(FOV_MAP, PLAYER.x, PLAYER.y, constants.TORCH_RADIUS, constants.FOV_LIGHT_WALLS, constants.FOV_ALGO)


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


# Draw map
def draw_map(map_to_draw):
	for x in range(0, constants.MAP_WIDTH):
		for y in range(0, constants.MAP_HEIGHT):

			is_visible = libtcod.map_is_in_fov(FOV_MAP, x, y)

			if is_visible:
				map_to_draw[x][y].explored = True
				# Draw wall
				if map_to_draw[x][y].block_path is True:
					SURFACE_MAIN.blit(constants.SPR_WALL, (x * constants.CELL_WIDTH, y * constants.CELL_HEIGHT))
				# Draw floor
				else:
					SURFACE_MAIN.blit(constants.SPR_FLOOR, (x * constants.CELL_WIDTH, y * constants.CELL_HEIGHT))

			elif map_to_draw[x][y].explored:
				# Draw wall
				if map_to_draw[x][y].block_path is True:
					SURFACE_MAIN.blit(constants.SPR_WALL_UNSEEN, (x * constants.CELL_WIDTH, y * constants.CELL_HEIGHT))
				# Draw floor
				else:
					SURFACE_MAIN.blit(constants.SPR_FLOOR_UNSEEN, (x * constants.CELL_WIDTH, y * constants.CELL_HEIGHT))


# GAME
# Function to loop main game
def game_main_loop():
	game_quit = False
	player_action = "no-action"

	while not game_quit:
		# Handle player input
		player_action = game_handle_keys()

		map_calculate_fov()

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

	global SURFACE_MAIN, GAME_MAP, PLAYER, ENEMY, GAME_OBJECTS, FOV_CALCULATE

	# Initialize pygame
	pygame.init()

	SURFACE_MAIN = pygame.display.set_mode((constants.MAP_WIDTH * constants.CELL_WIDTH, constants.MAP_HEIGHT * constants.CELL_HEIGHT))

	GAME_MAP = map_create()

	FOV_CALCULATE = True

	creature_com1 = com_Creature("Greg")
	PLAYER = obj_Actor(1, 1, "Python", constants.SPR_PLAYER, creature=creature_com1)

	creature_com2 = com_Creature("Jack", death_function=death_monster)
	ai_com = ai_Test()
	ENEMY = obj_Actor(15, 15, "Crab", constants.SPR_ENEMY, creature=creature_com2, ai=ai_com)

	GAME_OBJECTS = [PLAYER, ENEMY]


def game_handle_keys():
	global FOV_CALCULATE
	# Get player input
	events_list = pygame.event.get()

	# Process input
	for event in events_list:
		# Quit game
		if event.type == pygame.QUIT:
			return "QUIT"

		# Get arrow key input and move accordingly
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				PLAYER.creature.move(0, -1)
				FOV_CALCULATE = True
				return "Player moved"
			if event.key == pygame.K_DOWN:
				PLAYER.creature.move(0, 1)
				FOV_CALCULATE = True
				return "Player moved"
			if event.key == pygame.K_LEFT:
				PLAYER.creature.move(-1, 0)
				FOV_CALCULATE = True
				return "Player moved"
			if event.key == pygame.K_RIGHT:
				PLAYER.creature.move(1, 0)
				FOV_CALCULATE = True
				return "Player moved"

	# Return no action if player didn't press a key
	return "no-action"


# Execute Game
if __name__ == '__main__':
	game_initialize()
	game_main_loop()
