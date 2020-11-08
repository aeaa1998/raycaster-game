from player import Player
from sprites import *
from cast import ray_casting_walls
from hud import HUD
from gamelogic import GameLogic
pygame.init()
sc = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT), pygame.DOUBLEBUF)
clock = pygame.time.Clock()
mp = pygame.Surface(MAP_RES)
all_s = Sprites()
player = Player(all_s)
drawing = HUD(sc, mp, player, clock)
game_logic = GameLogic(player, all_s, drawing)
drawing.menu()
pygame.mouse.set_visible(False)
game_logic.play_music()
while True:
    player.movement()
    drawing.background()
    walls, wall_shot = ray_casting_walls(player, drawing.textures)
    drawing.world(walls + [obj.locate(player) for obj in all_s.world])
    drawing.hud_fps(clock)
    drawing.mini_map()
    drawing.player_weapon([wall_shot, all_s.shot])
    game_logic.interaction_objects()
    game_logic.npc_action()
    game_logic.clear()
    game_logic.check_win()
    pygame.display.flip()
    clock.tick()