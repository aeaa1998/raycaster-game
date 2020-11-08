from env import *
from numba.core import types
from numba.typed import Dict
from numba import int64
import pygame
_ = False
matrix_map = [
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, _, _, _, _, _, 2, _, _, _, _, _, _, _, _, 3, _, 2, _, _, _, _, _, 1],
[1, _, _, _, _, _, _, _, _, 2, _, 2, 2, _, _, 3, 3, _, _, _, _, _, _, 1],
[1, _, 2, 2, 2, _, 2, _, _, _, _, _, 2, _, 2, _, _, 3, _, _, _, 2, _, 1],
[1, _, 3, _, _, _, 2, _, _, 2, _, _, 2, _, _, _, _, _, _, 2, _, _, _, 1],
[1, _, 3, _, _, _, 2, _, _, 2, 2, _, 2, _, _, _, 2, _, _, _, _, 2, _, 1],
[1, _, _, 3, _, _, 2, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
[1, _, 3, _, _, _, 3, _, _, _, 3, _, _, 3, 3, _, _, _, _, 3, 3, _, _, 1],
[1, _, 3, _, _, _, 3, 3, 3, 3, _, _, _, 3, 3, _, _, _, _, 2, 3, _, _, 1],
[1, _, 2, _, 3, _, _, _, _, 3, _, _, 2, _, _, _, _, _, _, _, _, 2, _, 1],
[1, _, 2, _, 3, _, _, _, _, 3, _, _, 2, _, _, _, _, _, _, _, _, 2, _, 1],
[1, _, _, _, _, _, 2, _, _, _, _, _, 2, 2, _, _, _, _, _, _, 2, 2, _, 1],
[1, _, _, 2, _, _, _, _, 2, _, _, _, _, 2, _, 2, 2, 2, 2, _, 2, _, _, 1],
[1, _, _, 2, 2, 2, 2, _, _, _, 2, 2, 2, 3, _, 3, 3, 3, 3, _, _, _, 3, 1],
[1, _, _, _, _, _, _, _, _, _, 2, _, _, _, _, _, _, _, _, _, _, _, _, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# Set the world variables for the matrix
WORLD_WIDTH, WORLD_HEIGHT = max([len(i) for i in matrix_map]) * TILE, len(matrix_map) * TILE

# Make the world into a dictionary
world_map = Dict.empty(key_type=types.UniTuple(int64, 2), value_type=int64)
mini_map = set()
collision_walls = []
# Populate the world dict

for j, row in enumerate(matrix_map):
    for i, char in enumerate(row):
        if char:
            mini_map.add((i * MAP_TILE, j * MAP_TILE))
            collision_walls.append(pygame.Rect(i * TILE, j * TILE, TILE, TILE))
            if char == 1:
                world_map[(i * TILE, j * TILE)] = 1
            elif char == 2:
                world_map[(i * TILE, j * TILE)] = 2
            elif char == 3:
                world_map[(i * TILE, j * TILE)] = 3
            elif char == 4:
                world_map[(i * TILE, j * TILE)] = 4