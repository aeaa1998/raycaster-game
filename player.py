from map import collision_walls
from env import *
import pygame
import math


class Player:
    def __init__(self, sprites):
        self.x, self.y = P_POSITION
        self.angle = P_ANGLE
        self.sensitivity = 0.004
        self.sprites = sprites
        self.side = 50
        #We set the
        self.rect = pygame.Rect(*P_POSITION, self.side, self.side)
        self.shot = False

    def movement(self):
        self.watch_keys()
        self.update_mouse_angle()
        self.rect.center = self.x, self.y
        self.angle %= DOUBLE_PI

    def detect_collision(self, dx, dy):
        next_rect = self.rect.copy()
        next_rect.move_ip(dx, dy)
        hit_indexes = next_rect.collidelistall(self.collisions)
        if len(hit_indexes):
            delta_x, delta_y = 0, 0
            for hit_index in hit_indexes:
                hit_rect = self.collisions[hit_index]
                if dx > 0:
                    delta_x += next_rect.right - hit_rect.left
                else:
                    delta_x += hit_rect.right - next_rect.left
                if dy > 0:
                    delta_y += next_rect.bottom - hit_rect.top
                else:
                    delta_y += hit_rect.bottom - next_rect.top

            if abs(delta_x - delta_y) < 20: # <-------------
                dx, dy = 0, 0
            elif delta_x > delta_y:
                dy = 0
            elif delta_x < delta_y:
                dx = 0
        self.x += dx
        self.y += dy

    # Logic of the keyboard movement
    def watch_keys(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        dx, dy = 0, 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            exit()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dx, dy = P_SPEED * cos_a, P_SPEED * sin_a
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dx, dy = -P_SPEED * cos_a, -P_SPEED * sin_a
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx, dy = P_SPEED * sin_a, -P_SPEED * cos_a
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx, dy = -P_SPEED * sin_a, P_SPEED * cos_a

        self.detect_collision(dx, dy)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            # Shoot on mouse click
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not self.shot:
                    self.shot = True

    # Update the angle on the mouse movement
    def update_mouse_angle(self):
        if pygame.mouse.get_focused():
            difference = pygame.mouse.get_pos()[0] - HALF_WIDTH
            pygame.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])
            self.angle += difference * self.sensitivity


    @property
    def position(self):
        return (self.x, self.y)

    @property
    def collisions(self):
        return collision_walls + [pygame.Rect(*obj.position, obj.side, obj.side) for obj
                                  in self.sprites.world if obj.blocked]
