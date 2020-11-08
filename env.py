import math

# COLORS SET IN ENV
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 0, 0)
GREEN = (0, 80, 0)
BLUE = (0, 0, 255)
DARKGRAY = (40, 40, 40)
PURPLE = (120, 0, 120)
SKYBLUE = (0, 186, 255)
YELLOW = (220, 220, 0)
SANDY = (244, 164, 96)
DARKBROWN = (97, 61, 25)
DARKORANGE = (255, 140, 0)

# Game env variables
GAME_WIDTH = 1200
GAME_HEIGHT = 800
HALF_WIDTH = GAME_WIDTH // 2
HALF_HEIGHT = GAME_HEIGHT // 2
DOUBLE_WIDTH = 2 * GAME_WIDTH
DOUBLE_HEIGHT = 2 * GAME_HEIGHT
PENTA_HEIGHT = 5 * GAME_HEIGHT
GAME_FPS = 60
TILE = 100
# Position of fps counter
GAME_FPS_POSITION = (0, 5)

# MINIMAP ENVIORMENT
MINI_SCALE = 7
MAP_RES = (GAME_WIDTH // MINI_SCALE, GAME_HEIGHT // MINI_SCALE)
MAP_SCALE = 2 * MINI_SCALE
MAP_TILE = TILE // MAP_SCALE
MAP_POS = (GAME_WIDTH - GAME_WIDTH // MINI_SCALE, 0)

# RAYCASTING ENVIORMENT
FOV = math.pi / 3

NUM_RAYS = 300
# Max depth detected
MAX_DEPTH = 800
D_ANGLE = FOV / NUM_RAYS
DIST = NUM_RAYS / (2 * math.tan(FOV/2))
CF = 3 * DIST * TILE
RAY_SCALE = GAME_WIDTH // NUM_RAYS


DOUBLE_PI = math.pi * 2
CENTER_RAY = NUM_RAYS // 2 - 1
FAKE_RAYS = 200
FAKE_RAYS_RANGE = NUM_RAYS - 1 + 2 * FAKE_RAYS


TXT_WIDTH = 1200
TXT_H = 1200
HALF_TXT_H = TXT_H // 2
TXT_SCALE = TXT_WIDTH // TILE


P_POSITION = (HALF_WIDTH // 4, HALF_HEIGHT - 50)
P_ANGLE = 0
P_SPEED = 5
P_ROTATION_SPEED = 0.02

