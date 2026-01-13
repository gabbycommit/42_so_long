import sys
import random

from Srcs import map as map_generator
from Srcs import utils


def load_game(gs):
    gs.game_map = map_generator.load_map(
        f"./Map/valid_map/map{gs.current_lvl}.ber"
    )
    if not map_generator.is_valid_map(gs.game_map):
        sys.exit(1)

    gs.width = len(gs.game_map[0])
    gs.height = len(gs.game_map)

    gs.hint_timer = 0

    gs.coin_pos_anim = utils.coin_pos_anim_init(gs.game_map)
    gs.total_coin = utils.total_coin_cal(gs.game_map)
    gs.coin_collected = 0

    gs.player_pos = utils.get_player_pos(gs.game_map)
    py, px = gs.player_pos
    gs.game_map[py][px] = '0'

    gs.enemy_info = utils.enemy_pos_anim_init(gs.game_map)
    if gs.enemy_info:
        gs.enemy_anim_timer = 0
        gs.enemy_move_timer = 0

    gs.key_pos = utils.get_key_pos(gs.game_map)
    ky, kx = gs.key_pos
    gs.game_map[ky][kx] = '0'
    gs.show_key = False
    gs.key_collected = False

    gs.door_pos = utils.get_door_pos(gs.game_map)
    gs.win_game = False
    gs.win_msg = random.choice(gs.win_msg_list)
    gs.win_lvl_sfx_played = False

    gs.is_death = False
    gs.death_timer = 0
    gs.death_anim_idx = 0

    gs.show_death_msg = False
    gs.game_over_sfx_played = False
    gs.death_msg_timer = 0

    gs.last_game = False


def update_game(gs, coin_anim_tiles, enemy_anim_tiles, audio):
    coin_anim_cal(gs, coin_anim_tiles)
    player_movement_cal(gs)

    if gs.enemy_info:
        enemy_anim_cal(gs, enemy_anim_tiles)
        enemy_movement_cal(gs)

    coin_collection(gs, audio)
    is_show_key(gs)
    is_key_collected(gs, audio)
    is_death(gs)
    is_win(gs)


def coin_anim_cal(gs, coin_anim_tiles):
    gs.coin_timer += 1

    if gs.coin_timer >= gs.coin_delay:
        for pos in gs.coin_pos_anim:
            cal = (gs.coin_pos_anim[pos] + 1) % len(coin_anim_tiles)
            gs.coin_pos_anim[pos] = cal
        gs.coin_timer = 0


def player_movement_cal(gs):
    py, px = gs.player_pos
    ny, nx = gs.next_player_pos

    ny += py
    nx += px

    if gs.game_map[ny][nx] != '1':
        gs.player_pos = ny, nx

    gs.next_player_pos = (0, 0)
    return gs.player_pos


def enemy_movement_cal(gs):
    gs.enemy_move_timer += 1

    if gs.enemy_move_timer < gs.enemy_move_delay:
        return gs.enemy_info
    gs.enemy_move_timer = 0

    occupied = utils.get_enemy_pos_occupied(gs.enemy_info)
    enemy_intentions = utils.build_enemy_intentions(gs, occupied)

    enemy_intentions = utils.resolve_enemy_intentions(
        gs, enemy_intentions, occupied
    )

    for eid, t in gs.enemy_info.items():
        t["position"] = enemy_intentions[eid]

        dy,  dx = t["enemy_next_pos"]
        if dx == 1:
            t["enemy_dir"] = "right"
        elif dx == -1:
            t["enemy_dir"] = "left"

        t["enemy_next_pos"] = (0, 0)

    return gs.enemy_info


def enemy_anim_cal(gs, enemy_anim_tiles):
    gs.enemy_anim_timer += 1

    if gs.enemy_anim_timer >= gs.enemy_anim_delay:
        gs.enemy_anim_timer = 0
        for t in gs.enemy_info.values():
            t["enemy_anim_idx"] += 1

            if t["enemy_anim_idx"] >= len(enemy_anim_tiles[t["enemy_dir"]]):
                t["enemy_anim_idx"] = 0


def coin_collection(gs, audio):
    if gs.player_pos in gs.coin_pos_anim:
        cy, cx = gs.player_pos
        gs.game_map[cy][cx] = '0'
        del gs.coin_pos_anim[(cy, cx)]

        gs.coin_collected += 1
        audio.play_sfx("coin")
        print(f"coin collected: {gs.coin_collected} / {gs.total_coin}")


def is_show_key(gs):
    if gs.coin_collected == gs.total_coin:
        gs.show_key = True


def is_key_collected(gs, audio):
    if (
        not gs.key_collected and
        gs.player_pos == gs.key_pos and
        gs.coin_collected == gs.total_coin
    ):
        gs.key_collected = True
        audio.play_sfx("key")
        print("key collected")


def is_win(gs):
    if (
        gs.coin_collected == gs.total_coin and
        gs.key_collected and
        gs.player_pos == gs.door_pos
    ):
        gs.win_game = True


def show_hint_cal(gs):
    gs.hint_timer += 1

    if gs.hint_timer >= gs.hint_delay:
        gs.show_hint = not gs.show_hint
        gs.hint_timer = 0


def is_last_game(gs, levels):
    if gs.current_lvl >= len(levels):
        gs.last_game = True


def is_death(gs):
    for t in gs.enemy_info.values():
        if gs.player_pos == t["position"]:
            gs.is_death = True
    return False


def death_anim_cal(gs, death_tiles):
    gs.death_timer += 1

    if gs.death_timer >= gs.death_delay:
        gs.death_anim_idx += 1
        gs.death_timer = 0

        if gs.death_anim_idx >= len(death_tiles) - 1:
            gs.death_anim_idx = len(death_tiles) - 1
            gs.death_msg_timer += 1

            if gs.death_msg_timer >= gs.death_msg_delay:
                gs.show_death_msg = True
