import pygame
import libtcodpy as libtcod

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
SPR_WALL_UNSEEN = pygame.image.load("data/sprites/wallunseen.png")
SPR_FLOOR = pygame.image.load("data/sprites/floor.jpg")
SPR_FLOOR_UNSEEN = pygame.image.load("data/sprites/floorunseen.png")

# FOV settings
FOV_ALGO = libtcod.FOV_BASIC
FOV_LIGHT_WALLS = True
TORCH_RADIUS = 10
