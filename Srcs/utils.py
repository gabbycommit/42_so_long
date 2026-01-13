import random
import pygame as pg

from collections import Counter


def total_coin_cal(game_map):
    total_coin = 0

    for row in game_map:
        for cell in row:
            if cell == 'C':
                total_coin += 1

    return total_coin


def coin_pos_anim_init(game_map):
    coin_pos_anim = {}

    for y, row in enumerate(game_map):
        for x, cell in enumerate(row):
            if cell == 'C':
                coin_pos_anim[(y, x)] = 0

    return coin_pos_anim


def get_player_pos(game_map):
    for y, row in enumerate(game_map):
        for x, cell in enumerate(row):
            if cell == 'P':
                return (y, x)

    return (None, None)


def get_key_pos(game_map):
    for y, row in enumerate(game_map):
        for x, cell in enumerate(row):
            if cell == 'K':
                return (y, x)

    return (None, None)


def get_door_pos(game_map):
    for y, row in enumerate(game_map):
        for x, cell in enumerate(row):
            if cell == 'E':
                return (y, x)

    return (None, None)


def enemy_pos_anim_init(game_map):
    enemy_pos_anim = {}
    num = 1

    for y, row in enumerate(game_map):
        for x, cell in enumerate(row):
            if cell == 'T':
                enemy_pos_anim[f"t{num}"] = {}
                enemy_pos_anim[f"t{num}"]["position"] = (y, x)
                enemy_pos_anim[f"t{num}"]["enemy_dir"] = "right"
                enemy_pos_anim[f"t{num}"]["enemy_anim_idx"] = 0
                enemy_pos_anim[f"t{num}"]["enemy_next_pos"] = (0, 0)
                game_map[y][x] = '0'
                num += 1

    return enemy_pos_anim


def get_enemy_pos_occupied(enemy_info):
    return {t["position"] for t in enemy_info.values()}


def build_enemy_intentions(gs, occupied):
    enemy_intentions = {}
    direction = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    for eid, t in gs.enemy_info.items():
        t["enemy_next_pos"] = random.choice(direction)
        dy, dx = t["enemy_next_pos"]
        y, x = t["position"]

        ny = dy + y
        nx = dx + x

        if (
            gs.game_map[ny][nx] == '0' and
            (ny, nx) not in occupied
        ):
            enemy_intentions[eid] = (ny, nx)
        else:
            enemy_intentions[eid] = t["position"]
            t["enemy_next_pos"] = (0, 0)

    return enemy_intentions


def resolve_enemy_intentions(gs, enemy_intentions, occupied):
    max_loop = 10
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    for _ in range(max_loop):
        counter = Counter(enemy_intentions.values())
        conflicted_pos = {
            pos for pos, count in counter.items()
            if count > 1
        }

        if not conflicted_pos:
            return enemy_intentions

        conflicted_eids = [
            eid for eid, pos in enemy_intentions.items()
            if pos in conflicted_pos
        ]

        for eid in conflicted_eids:
            t = gs.enemy_info[eid]
            y, x = t["position"]

            dy, dx = random.choice(directions)
            ny = dy + y
            nx = dx + x

            if (
                gs.game_map[ny][nx] == '0' and
                (ny, nx) not in occupied
            ):
                enemy_intentions[eid] = (ny, nx)
                t["enemy_next_pos"] = (0, 0)

    for eid, pos in enemy_intentions.items():
        counter = Counter(enemy_intentions.values())
        if counter[pos] > 1:
            enemy_intentions[eid] = gs.enemy_info[eid]["position"]
            gs.enemy_info[eid]["enemy_next_pos"] = (0, 0)

    return enemy_intentions


def play_bgm(music_path):
    pg.mixer.music.load(music_path)
    pg.mixer.music.play(-1)
