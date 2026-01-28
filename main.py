import pygame as pg
import sys

from Srcs import update, tile, render, audio_manager

TILE_SIZE = 32
STATE_MENU = 0
STATE_PLAYING = 1
STATE_WIN = 2
STATE_DEATH = 3
STATE_DEATH_MSG = 4
LEVELS = list(range(1, 6))
FPS = 60
BGM_PLAYING = "./Assets/music/background.wav"


class GameState:
    def __init__(self):
        self.state = STATE_MENU
        self.current_lvl = 1

        self.game_map = None
        self.width = 0
        self.height = 0

        self.hint_timer = 0
        self.hint_delay = 50
        self.show_hint = True

        self.coin_pos_anim = None
        self.total_coin = 0
        self.coin_collected = 0
        self.coin_timer = 0
        self.coin_delay = 10

        self.player_pos = (0, 0)
        self.next_player_pos = (0, 0)

        self.enemy_info = None
        self.enemy_anim_timer = 0
        self.enemy_anim_delay = 10
        self.enemy_move_timer = 0
        self.enemy_move_delay = 20

        self.key_pos = (0, 0)
        self.show_key = False
        self.key_collected = False

        self.door_pos = (0, 0)

        self.win_game = False
        self.win_msg_list = [
            "You did it!",
            "Level Complete!",
            "Victory is yours!",
            "Well played!",
            "Mission accomplished!",
            "You Won!"
        ]
        self.win_msg = ""
        self.win_lvl_sfx_played = False
        self.game_completed_sfx_played = False

        self.is_death = False
        self.death_anim_idx = 0
        self.death_timer = 0
        self.death_delay = 20

        self.show_death_msg = False
        self.game_over_sfx_played = False
        self.death_msg_timer = 0
        self.death_msg_delay = 8

        self.last_game = False


pg.init()

gs = GameState()
audio = audio_manager.AudioManager()

update.load_game(gs)
window = pg.display.set_mode((gs.width * TILE_SIZE, gs.height * TILE_SIZE))
pg.display.set_caption("so long")
clock = pg.time.Clock()

fonts = {
    "bold_48": pg.font.Font("./Assets/font/PixelOperator8-Bold.ttf", 48),
    "bold_24": pg.font.Font("./Assets/font/PixelOperator8-Bold.ttf", 24),
    "normal": pg.font.Font("./Assets/font/PixelOperator8.ttf", 24),
    "small": pg.font.Font("./Assets/font/PixelOperator8.ttf", 12),
}

tileset = pg.image.load("./Assets/tiles/tileset1.png").convert_alpha()
tiles = {
    "1": tile.get_tile(tileset, 1, 0, 26, TILE_SIZE),
    "0": tile.get_tile(tileset, 5, 4, 26, TILE_SIZE),
    "E": tile.get_tile(tileset, 8, 1, 26, TILE_SIZE),
    "K": tile.get_tile(tileset, 8, 0, 26, TILE_SIZE),
}

coin_tileset = pg.image.load("./Assets/tiles/coin.png").convert_alpha()
coin_animation_tiles = tile.get_coin_tiles(coin_tileset, TILE_SIZE)

player_movement_tiles = tile.get_player_movement_tiles(tileset, TILE_SIZE)
player_death_tiles = tile.get_player_death__tiles(tileset, TILE_SIZE)
player_idle_img = player_movement_tiles["right"]

enemy_tileset = pg.image.load("./Assets/tiles/enemy.png").convert_alpha()
enemy_anim_tiles = tile.get_enemy_tiles(enemy_tileset, TILE_SIZE)

audio.load_sfx("coin", "./Assets/music/coin1.wav", 0.5)
audio.load_sfx("death", "./Assets/music/ouch.wav", 0.5)
audio.load_sfx("enter", "./Assets/music/enter.wav", 0.5)
audio.load_sfx("game_completed", "./Assets/music/game_completed.wav", 0.3)
audio.load_sfx("game_over", "./Assets/music/game_over.wav", 0.5)
audio.load_sfx("key", "./Assets/music/key_collected.wav", 0.5)
audio.load_sfx("lvl_win", "./Assets/music/level_win.wav", 0.5)
audio.load_sfx("move", "./Assets/music/player_move.wav", 0.5)


running = True

while running:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            running = False
        elif e.type == pg.KEYDOWN:
            if e.key == pg.K_ESCAPE:
                running = False

            if gs.state == STATE_MENU:
                if e.key == pg.K_RETURN:
                    gs.state = STATE_PLAYING
                    audio.play_sfx("enter")
                    audio.play_bgm(BGM_PLAYING)

            elif gs.state == STATE_PLAYING:
                if e.key == pg.K_w or e.key == pg.K_UP:
                    gs.next_player_pos = (-1, 0)
                    audio.play_sfx("move")
                elif e.key == pg.K_s or e.key == pg.K_DOWN:
                    gs.next_player_pos = (1, 0)
                    audio.play_sfx("move")
                elif e.key == pg.K_a or e.key == pg.K_LEFT:
                    gs.next_player_pos = (0, -1)
                    audio.play_sfx("move")
                    player_idle_img = player_movement_tiles["left"]
                elif e.key == pg.K_d or e.key == pg.K_RIGHT:
                    gs.next_player_pos = (0, 1)
                    audio.play_sfx("move")
                    player_idle_img = player_movement_tiles["right"]

            elif gs.state == STATE_DEATH:
                pass

            elif gs.state == STATE_DEATH_MSG:
                if e.key == pg.K_RETURN:
                    audio.play_sfx("enter")
                    audio.play_bgm(BGM_PLAYING)
                    update.load_game(gs)

                    window = pg.display.set_mode(
                        (gs.width * TILE_SIZE, gs.height * TILE_SIZE)
                    )
                    gs.state = STATE_PLAYING

            elif gs.state == STATE_WIN:
                if gs.current_lvl + 1 <= len(LEVELS):
                    if e.key == pg.K_RETURN:
                        audio.play_sfx("enter")
                        audio.play_bgm(BGM_PLAYING)
                        gs.win_lvl_sfx_played = False

                        gs.current_lvl += 1
                        update.load_game(gs)
                        window = pg.display.set_mode(
                            (gs.width * TILE_SIZE, gs.height * TILE_SIZE)
                        )
                        gs.state = STATE_PLAYING

    if gs.state == STATE_MENU:
        update.show_hint_cal(gs)

        render.render_menu(window, fonts, gs)

    elif gs.state == STATE_PLAYING:
        update.update_game(gs, coin_animation_tiles, enemy_anim_tiles, audio)

        render.render_base(window, gs.game_map, tiles, TILE_SIZE)
        render.render_coin(window, coin_animation_tiles, gs, TILE_SIZE)
        render.render_player(window, player_idle_img, gs, TILE_SIZE)
        render.render_key(window, tiles["K"], gs, TILE_SIZE)
        render.render_enemy(window, enemy_anim_tiles, gs, TILE_SIZE)

        if gs.is_death:
            audio.play_sfx("death")
            audio.stop_bgm()
            gs.state = STATE_DEATH
            gs.hint_timer = 0

        if gs.win_game:
            audio.stop_bgm()
            gs.state = STATE_WIN
            gs.hint_timer = 0

    elif gs.state == STATE_DEATH:
        update.death_anim_cal(gs, player_death_tiles)

        render.render_base(window, gs.game_map, tiles, TILE_SIZE)
        render.render_coin(window, coin_animation_tiles, gs, TILE_SIZE)
        render.render_enemy(window, enemy_anim_tiles, gs, TILE_SIZE)
        render.render_player_death(window, player_death_tiles, gs, TILE_SIZE)

        if gs.show_death_msg:
            gs.state = STATE_DEATH_MSG
            gs.hint_timer = 0

    elif gs.state == STATE_DEATH_MSG:
        update.show_hint_cal(gs)

        render.render_death_state(window, fonts, gs)
        if not gs.game_over_sfx_played:
            audio.play_sfx("game_over")
            gs.game_over_sfx_played = True

    elif gs.state == STATE_WIN:
        update.show_hint_cal(gs)
        update.is_last_game(gs, LEVELS)

        render.render_win_state(window, fonts, gs)
        if gs.last_game:
            if not gs.game_completed_sfx_played:
                audio.play_sfx("game_completed")
                gs.game_completed_sfx_played = True
        else:
            if not gs.win_lvl_sfx_played:
                audio.play_sfx("lvl_win")
                gs.win_lvl_sfx_played = True

    pg.display.flip()
    clock.tick(FPS)

pg.quit()
sys.exit()
