import pygame as pg


def get_tile(tileset, col, row, atlas_tile_size, tile_size):

    rect = pg.Rect(
        col * atlas_tile_size,
        row * atlas_tile_size,
        atlas_tile_size,
        atlas_tile_size,
    )

    surf = tileset.subsurface(rect).copy()
    surf = pg.transform.scale(surf, (tile_size, tile_size))

    return surf


def get_coin_tiles(atlas, tile_size):
    coin_animation_tiles = []

    for i in range(12):
        rect = pg.Rect(
            i * 16,
            0 * 16,
            16,
            16
        )
        surf = atlas.subsurface(rect).copy()
        surf = pg.transform.scale(surf, (tile_size, tile_size))
        coin_animation_tiles.append(surf)

    return coin_animation_tiles


def get_player_movement_tiles(atlas, tile_size):
    player_movement_tiles = {}

    player_movement_tiles["right"] = get_tile(
        atlas,
        3,
        2,
        26,
        tile_size
    )
    player_movement_tiles["left"] = pg.transform.flip(
        player_movement_tiles["right"],
        True,
        False
    )

    return player_movement_tiles


def get_enemy_tiles(atlas, tile_size):
    enemy_anim = {}
    enemy_anim_tiles_r = []
    enemy_anim_tiles_l = []

    for x in range(3):
        surf_r = get_tile(atlas, x, 1, 26, tile_size + 16)
        enemy_anim_tiles_r.append(surf_r)

    enemy_anim["right"] = enemy_anim_tiles_r

    for img in enemy_anim_tiles_r:
        surf_l = pg.transform.flip(img, True, False)
        enemy_anim_tiles_l.append(surf_l)

    enemy_anim["left"] = enemy_anim_tiles_l
    return enemy_anim


def get_player_death__tiles(atlas, tile_size):
    player_death_anim = []

    for x in range(5, 8):
        surf = get_tile(atlas, x, 2, 26, tile_size)
        player_death_anim.append(surf)
    return player_death_anim
