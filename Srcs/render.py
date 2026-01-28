def render_menu(window, fonts, gs):
    width, height = window.get_size()

    title = fonts["bold_48"].render(
        "SO LONG",
        True,
        (255, 255, 255)
    )
    level = fonts["normal"].render(
        f"level {gs.current_lvl}",
        True,
        (6, 83, 207)
    )
    hint = fonts["small"].render(
        "Press Enter to start...",
        False,
        (200, 200, 200)
    )

    title_rect = title.get_rect(center=(width / 2, height / 2 - 50))
    level_rect = level.get_rect(center=(width / 2, height / 2))
    hint_rect = hint.get_rect(center=(width / 2, height / 2 + 50))

    window.fill((0, 0, 0))
    window.blit(title, title_rect)
    window.blit(level, level_rect)

    if gs.show_hint:
        window.blit(hint, hint_rect)


def render_win_state(window, fonts, gs):
    width, height = window.get_size()

    level = fonts["normal"].render(
        f"level {gs.current_lvl}",
        True,
        (255, 255, 255)
    )
    win_msg = fonts["bold_24"].render(
        gs.win_msg,
        True,
        (207, 156, 6)
    )
    exit_msg = fonts["normal"].render(
        "You finished the game!",
        True,
        (207, 156, 6)
    )
    exit_msg2 = fonts["normal"].render(
        "Thanks for playing",
        True,
        (207, 156, 6)
    )
    hint = fonts["small"].render(
        "Press Enter to next level...",
        False,
        (200, 200, 200)
    )

    level_rect = level.get_rect(center=(width / 2, height / 2 - 40))
    win_msg_rect = win_msg.get_rect(center=(width / 2, height / 2))
    exit_msg_rect = exit_msg.get_rect(center=(width / 2, height / 2 - 40))
    exit_msg2_rect = exit_msg2.get_rect(center=(width / 2, height / 2 + 40))
    hint_rect = hint.get_rect(center=(width / 2, height / 2 + 50))

    window.fill((0, 0, 0))

    if not gs.last_game:
        window.blit(level, level_rect)
        window.blit(win_msg, win_msg_rect)
    else:
        window.blit(exit_msg, exit_msg_rect)
        window.blit(exit_msg2, exit_msg2_rect)

    if gs.show_hint and not gs.last_game:
        window.blit(hint, hint_rect)


def render_death_state(window, fonts, gs):
    width, height = window.get_size()

    death = fonts["bold_24"].render(
        "Oops...you're dead",
        False,
        (207, 156, 6)
    )
    hint = fonts["small"].render(
        "Press Enter to restart the level or press Esc to quit...",
        False,
        (200, 200, 200)
    )

    death_rect = death.get_rect(center=(width / 2, height / 2 - 30))
    hint_rect = hint.get_rect(center=(width / 2, height / 2 + 30))

    if gs.show_death_msg:
        window.fill((0, 0, 0))
        window.blit(death, death_rect)

        if gs.show_hint:
            window.blit(hint, hint_rect)


def render_base(window, game_map, tiles, tile_size):
    window.fill((0, 0, 0))

    for y, row in enumerate(game_map):
        for x, cell in enumerate(row):
            if cell == '1':
                window.blit(
                    tiles["1"],
                    (x * tile_size, y * tile_size)
                )
            elif cell == '0':
                window.blit(
                    tiles["0"],
                    (x * tile_size, y * tile_size)
                )
            elif cell == 'E':
                window.blit(
                    tiles["E"],
                    (x * tile_size, y * tile_size)
                )


def render_coin(window, coin_anim_tiles, gs, tile_size):
    for pos, anim_idx in gs.coin_pos_anim.items():
        y, x = pos
        window.blit(
            coin_anim_tiles[anim_idx],
            (x * tile_size, y * tile_size)
        )


def render_player(window, player_idle_img, gs, tile_size):
    py, px = gs.player_pos

    window.blit(
        player_idle_img,
        (px * tile_size, py * tile_size)
    )


def render_enemy(window, anim_tiles, gs, title_size):
    if not gs.enemy_info:
        return

    for t in gs.enemy_info.values():
        ey, ex = t["position"]
        enemy_img = anim_tiles[t["enemy_dir"]][t["enemy_anim_idx"]]

        if t["enemy_dir"] == "right":
            window.blit(
                enemy_img,
                (ex * title_size - 3, ey * title_size - 12)
            )
        else:
            window.blit(
                enemy_img,
                (ex * title_size - 12, ey * title_size - 12)
            )


def render_key(window, key_img, gs, tile_size):
    ky, kx = gs.key_pos

    if gs.show_key and not gs.key_collected:
        window.blit(
            key_img,
            (kx * tile_size, ky * tile_size)
        )


def render_player_death(window, death_tiles, gs, tile_size):
    py, px = gs.player_pos

    window.blit(
        death_tiles[gs.death_anim_idx],
        (px * tile_size, py * tile_size)
    )
