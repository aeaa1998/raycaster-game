import pygame
from env import *
from map import world_map, WORLD_WIDTH, WORLD_HEIGHT
from numba import njit

@njit(fastmath=True, cache=True)
def ray_npc(npc_x, npc_y, blocks, map, position):
    player_x, player_y = position
    xm, ym = mapping(player_x, player_y)
    delta_x, delta_y = player_x - npc_x, player_y - npc_y
    angle = math.atan2(delta_y, delta_x)
    angle += math.pi
    sin_a = math.sin(angle)
    cos_a = math.cos(angle)
    x, dx = (xm + TILE, 1) if cos_a >= 0 else (xm, -1)
    for i in range(int(abs(delta_x) // TILE)):
        depth_v = (x - player_x) / cos_a
        yv = player_y + depth_v * sin_a
        tv = mapping(x + dx, yv)
        if tv in map or tv in blocks:
            return False
        x += dx * TILE
    y, dy = (ym + TILE, 1) if sin_a >= 0 else (ym, -1)
    for i in range(int(abs(delta_y) // TILE)):
        depth_h = (y - player_y) / sin_a
        xh = player_x + depth_h * cos_a
        tile_h = mapping(xh, y + dy)
        if tile_h in map or tile_h in blocks:
            return False
        y += dy * TILE
    return True

@njit(fastmath=True, cache=True)
def mapping(a, b):
    return int((a // TILE) * TILE), int((b // TILE) * TILE)


@njit(fastmath=True, cache=True)
def ray_casting(player_pos, player_angle, world_map):
    casted_walls = []
    ox, oy = player_pos
    xm, ym = mapping(ox, oy)
    cur_angle = player_angle - (FOV/2)
    texture_v, texture_h = 1, 1
    for ray in range(NUM_RAYS):
        sin_a = math.sin(cur_angle)
        cos_a = math.cos(cur_angle)

        # verticals
        x, dx = (xm + TILE, 1) if cos_a >= 0 else (xm, -1)
        for i in range(0, WORLD_WIDTH, TILE):
            depth_v = (x - ox) / cos_a
            yv = oy + depth_v * sin_a
            tile_v = mapping(x + dx, yv)
            if tile_v in world_map:
                texture_v = world_map[tile_v]
                break
            x += dx * TILE

        # horizontals
        y, dy = (ym + TILE, 1) if sin_a >= 0 else (ym, -1)
        for i in range(0, WORLD_HEIGHT, TILE):
            depth_h = (y - oy) / sin_a
            xh = ox + depth_h * cos_a
            tile_h = mapping(xh, y + dy)
            if tile_h in world_map:
                texture_h = world_map[tile_h]
                break
            y += dy * TILE

        # projection
        depth, offset, texture = (depth_v, yv, texture_v) if depth_v < depth_h else (depth_h, xh, texture_h)
        offset = int(offset) % TILE
        # del_fish_eye = math.cos(player_angle - cur_angle)
        depth *= math.cos(player_angle - cur_angle)
        depth = max(depth, 0.00001)
        proj_height = int(CF / depth)

        casted_walls.append((depth, offset, proj_height, texture))
        cur_angle += D_ANGLE
    return casted_walls


def ray_casting_walls(player, textures):
    walls = []
    casted_walls = ray_casting(player.position, player.angle, world_map)
    # wall shot
    wall_shot = casted_walls[CENTER_RAY][0], casted_walls[CENTER_RAY][2]
    # ---------
    for ray, casted_values in enumerate(casted_walls):
        depth, offset, proj_height, texture = casted_values
        if proj_height > GAME_HEIGHT:
            texture_height = TXT_H / (proj_height / GAME_HEIGHT)
            wall_column = textures[texture].subsurface(offset * TXT_SCALE,
                                                       HALF_TXT_H - texture_height // 2,
                                                       TXT_SCALE, texture_height)
            wall_column = pygame.transform.scale(wall_column, (RAY_SCALE, GAME_HEIGHT))
            wall_pos = (ray * RAY_SCALE, 0)
        else:
            wall_column = textures[texture].subsurface(offset * TXT_SCALE, 0, TXT_SCALE, TXT_H)
            wall_column = pygame.transform.scale(wall_column, (RAY_SCALE, proj_height))
            wall_pos = (ray * RAY_SCALE, HALF_HEIGHT - proj_height // 2)

        walls.append((depth, wall_column, wall_pos))
    return walls, wall_shot
