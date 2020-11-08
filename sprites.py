import pygame
from env import *
from collections import deque
from cast import mapping
from numba.core import types
from numba.typed import Dict
from numba import int32


class Sprites:
    def __init__(self):
        self.build = {
            'cartoon_monster': {
                'sprite': [pygame.image.load(f'sprites/npc/cartoon_monster/base/{i}.png').convert_alpha() for i in range(8)],
                'viewing_angles': True,
                'shift': 0.0,
                'scale': (1.1, 1.1),
                'side': 50,
                'animation': [],
                'death_animation': deque([pygame.image.load(f'sprites/npc/cartoon_monster/death/{i}.png').convert_alpha() for i in range(6)]),
                'died': None,
                'dead_shift': 0.6,
                'animation_dist': None,
                'animation_speed': 10,
                'blocked': True,
                'obj_action': deque(
                    [pygame.image.load(f'sprites/npc/cartoon_monster/anim/{i}.png').convert_alpha() for i in range(6)]),
            },
            'alien_crab': {
                'sprite': [pygame.image.load(f'sprites/npc/alien_crab/base/{i}.png').convert_alpha() for i in range(8)],
                'viewing_angles': True,
                'shift': 0,
                'scale': (0.9, 1.0),
                'side': 30,
                'animation': [],
                'death_animation': deque([pygame.image.load(f'sprites/npc/alien_crab/death/{i}.png')
                                           .convert_alpha() for i in range(9)]),
                'died': None,
                'dead_shift': 0.5,
                'animation_dist': None,
                'animation_speed': 6,
                'blocked': True,
                'obj_action': deque([pygame.image.load(f'sprites/npc/alien_crab/action/{i}.png')
                                    .convert_alpha() for i in range(8)])
            },
            'fat_boy': {
                'sprite': [pygame.image.load(f'sprites/npc/fat_boy/base/{i}.png').convert_alpha() for i in range(8)],
                'viewing_angles': True,
                'shift': 0.8,
                'scale': (0.4, 0.6),
                'side': 30,
                'animation': [],
                'death_animation': deque([pygame.image.load(f'sprites/npc/fat_boy/death/{i}.png')
                                           .convert_alpha() for i in range(9)]),
                'died': None,
                'dead_shift': 1.7,
                'animation_dist': None,
                'animation_speed': 6,
                'blocked': True,
                'obj_action': deque([pygame.image.load(f'sprites/npc/fat_boy/action/{i}.png')
                                           .convert_alpha() for i in range(9)])
            }
        }
        fat_boys = self.make_sprites('fat_boy',
                                     [(2.5, 1.5), (5.51, 1.5), (6.61, 2.92), (7.68, 1.47), (8.75, 3.65), (1.27, 11.5),
                                      (1.26, 8.29), (8.10, 11.93), (12.14, 10.34), (10.5, 1.1), (3.66, 5.27),
                                      (4.38, 6.56), (4.33, 9.01), (4.46, 10.35), (13.16, 2.16), (12.09, 1.28),
                                      (17.02, 14.26), (15.27, 6.56), (14.31, 11.56), (17.62, 9.66), (18.29, 12.66),
                                      (18.53, 8.33), (20.42, 7.53), (22.3, 2.89), (22.76, 10.21)])



        cartoon_monster = self.make_sprites('cartoon_monster', [
            (3.9, 6.41), (14.36, 3.31), (2.14, 13.81), (15.85, 14.74)
            , (18.20, 14.73), (22.53, 9.00)
        ])
        alien_crab = self.make_sprites('alien_crab', [
            (10.73, 3.90), (10.6, 5.52), (11.75, 5.75), (14.87, 14.27)
            , (19.77, 14.26), (20.12, 3.55)
        ])

        self.world = fat_boys + cartoon_monster + alien_crab

    def make_sprites(self, name, positions):
        holder = []
        for pos in positions:
            holder.append(SpriteObject(self.build[name], pos))
        return holder

    @property
    def shot(self):
        return min([sp.can_be_shot for sp in self.world], default=(float('inf'), 0))

    @property
    def blocked_doors(self):
        blocked_doors = Dict.empty(key_type=types.UniTuple(int32, 2), value_type=int32)
        return blocked_doors


class SpriteObject:
    def __init__(self, build, p):
        self.set_up(build)
        self.x_p, self.y_p = p[0] * TILE, p[1] * TILE
        self.dead_animation_count = 0
        self.animation_count = 0
        self.npc_action_trigger = False
        self.door_open_trigger = False
        self.door_prev_pos = self.x_p
        self.delete = False
        if self.v_angles:
            if len(self.object) == 8:
                self.sprite_angles = [frozenset(range(338, 361)) | frozenset(range(0, 23))] + \
                                     [frozenset(range(i, i + 45)) for i in range(23, 338, 45)]
            else:
                self.sprite_angles = [frozenset(range(348, 361)) | frozenset(range(0, 11))] + \
                                     [frozenset(range(i, i + 23)) for i in range(11, 348, 23)]
            self.sprite_positions = {angle: pos for angle, pos in zip(self.sprite_angles, self.object)}

    def set_up(self, build):
        self.own_action = build['obj_action'].copy()
        self.animation = build['animation'].copy()
        self.death_animation = build['death_animation'].copy()
        self.died = build['died']
        self.dead_shift = build['dead_shift']
        self.animation_distance_trigger = build['animation_dist']
        self.animation_speed = build['animation_speed']
        self.blocked = build['blocked']
        self.object = build['sprite'].copy()
        self.v_angles = build['viewing_angles']
        self.shift = build['shift']
        self.scale = build['scale']
        self.side = build['side']


    def locate(self, player):

        dx, dy = self.x_p - player.x, self.y_p - player.y
        self.distance_from = math.sqrt(dx ** 2 + dy ** 2)
        self.th = math.atan2(dy, dx)
        gm = self.th - player.angle
        if dx > 0 and 180 <= math.degrees(player.angle) <= 360 or dx < 0 and dy < 0:
            gm += DOUBLE_PI
        self.th -= 1.4 * gm
        delta_rays = int(gm / D_ANGLE)
        self.current_ray = CENTER_RAY + delta_rays
        self.distance_from *= math.cos((FOV / 2) - self.current_ray * D_ANGLE)
        fake_ray = self.current_ray + FAKE_RAYS
        if 0 <= fake_ray <= FAKE_RAYS_RANGE and self.distance_from > 30:
            self.proj_height = min(int(CF / self.distance_from),
                                   DOUBLE_HEIGHT)
            sprite_width = int(self.proj_height * self.scale[0])
            sprite_height = int(self.proj_height * self.scale[1])
            half_sprite_width = sprite_width // 2
            half_sprite_height = sprite_height // 2
            shift = half_sprite_height * self.shift

            if self.died and self.died != 'immortal':
                sprite_object = self.animate_death()
                shift = half_sprite_height * self.dead_shift
                sprite_height = int(sprite_height / 1.3)
            elif self.npc_action_trigger:
                sprite_object = self.animate_action()
            else:
                # choose sprite for angle
                self.object = self.visible()
                # sprite animation
                sprite_object = self.animate()
            sprite = pygame.transform.scale(sprite_object, (sprite_width, sprite_height))
            sprite_pos = (self.current_ray * RAY_SCALE - half_sprite_width, HALF_HEIGHT - half_sprite_height + shift)

            return (self.distance_from, sprite, sprite_pos)
        else:
            return (False,)

    def animate_death(self):
        if len(self.death_animation):
            if self.dead_animation_count < self.animation_speed:
                self.dead_sprite = self.death_animation[0]
                self.dead_animation_count += 1
            else:
                self.dead_sprite = self.death_animation.popleft()
                self.dead_animation_count = 0
        return self.dead_sprite

    def animate_action(self):
        sprite_object = self.own_action[0]
        if self.animation_count < self.animation_speed:
            self.animation_count += 1
        else:
            self.own_action.rotate()
            self.animation_count = 0
        return sprite_object



    def animate(self):
        if self.animation and self.distance_from < self.animation_distance_trigger:
            sprite_object = self.animation[0]
            if self.animation_count < self.animation_speed:
                self.animation_count += 1
            else:
                self.animation.rotate(-1)
                self.animation_count = 0
            return sprite_object
        return self.object

    def visible(self):
        if self.v_angles:
            if self.th < 0:
                self.th += DOUBLE_PI
            self.th = 360 - int(math.degrees(self.th))

            for angles in self.sprite_angles:
                if self.th in angles:
                    return self.sprite_positions[angles]
        return self.object


    @property
    def can_be_shot(self):
        if CENTER_RAY - self.side // 2 < self.current_ray < CENTER_RAY + self.side // 2 and self.blocked:
            return (self.distance_from, self.proj_height)
        return (float('inf'), None)

    @property
    def position(self):
        return self.x_p - self.side // 2, self.y_p - self.side // 2