from env import *
from map import world_map
from cast import ray_npc
import pygame


class GameLogic:
    def __init__(self, player, sprites, drawing):
        self.player = player
        self.sprites = sprites
        self.drawing = drawing
        self.pain_sound = pygame.mixer.Sound('sound/death.mp3')

    def interaction_objects(self):
        if self.player.shot and self.drawing.shot_animation_trigger:
            for sp in sorted(self.sprites.world, key=lambda obj: obj.distance_from):
                if sp.can_be_shot[1]:
                    if sp.died != 'immortal' and not sp.died:
                        if ray_npc(sp.x_p, sp.y_p,
                                   self.sprites.blocked_doors,
                                   world_map, self.player.position):

                            self.pain_sound.play()
                            sp.died = True
                            sp.blocked = None
                            self.drawing.shot_animation_trigger = False
                    break

    def npc_action(self):
        for sp in self.sprites.world:
            if not sp.died:
                if ray_npc(sp.x_p, sp.y_p,
                           self.sprites.blocked_doors,
                           world_map, self.player.position):
                    sp.npc_action_trigger = True
                    self.npc_move(sp)
                else:
                    sp.npc_action_trigger = False

    def npc_move(self, sp):
        if abs(sp.distance_from) > TILE:
            dx = sp.x_p - self.player.position[0]
            dy = sp.y_p - self.player.position[1]
            sp.x_p = sp.x_p + 1 if dx < 0 else sp.x_p - 1
            sp.y_p = sp.y_p + 1 if dy < 0 else sp.y_p - 1

    def clear(self):
        deleted_objects = self.sprites.world[:]
        [self.sprites.world.remove(obj) for obj in deleted_objects if obj.delete]

    def check_win(self):
        if not len([sp for sp in self.sprites.world if not sp.died]):
            # Stop current music and put win gg
            pygame.mixer.music.stop()
            pygame.mixer.music.load('sound/win.mp3')
            pygame.mixer.music.play()
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit()
                self.drawing.win()

    def play_music(self):
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init()
        pygame.mixer.music.load('sound/intro.mp3')
        pygame.mixer.music.play(10)
