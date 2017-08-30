import pygame

pygame.init()

# Game sizes
GAME_WIDTH = 800
GAME_HEIGHT = 600
CELL_WIDTH = 32
CELL_HEIGHT = 32

# Map variables
MAP_WIDTH = 20
MAP_HEIGHT = 20

# Colour definitions
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_GREY = (100, 100, 100)

# Game colours
COLOR_DEFAULT_BG = COLOR_GREY

# Sprites
SPR_PLAYER = pygame.image.load("data/sprites/python.png")
SPR_ENEMY = pygame.image.load("data/sprites/crab.png")
SPR_WALL = pygame.image.load("data/sprites/wall.jpg")
SPR_FLOOR = pygame.image.load("data/sprites/floor.jpg")
