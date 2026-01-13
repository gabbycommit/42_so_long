import sys


def load_map(map_path):
    game_map = []

    with open(map_path, 'r') as file:
        try:
            for row in file:
                game_map.append(list(row.strip()))
        except FileNotFoundError:
            print("Error: file not found")
            sys.exit(1)
    return game_map


def is_valid_outer_wall(game_map):
    width = len(game_map[0])
    height = len(game_map)

    for x in range(width):
        if (
            game_map[0][x] != '1' or
            game_map[height - 1][x] != '1'
        ):
            print("Error: outer wall must be '1' : width")
            return False

    for y in range(height):
        if (
            game_map[y][0] != '1' or
            game_map[y][width - 1] != '1'
        ):
            print("Error: outer wall must be '1' : height")
            return False
    return True


def is_valid_chr(game_map):
    valid_chr = {'1', '0', 'P', 'C', 'E', 'K', 'T'}
    player = 0
    key = 0
    exit_point = 0
    collection = 0

    for y, row in enumerate(game_map):
        for x, cell in enumerate(row):
            if cell not in valid_chr:
                print("Error: invalid char input")
                return False
            if cell == 'P':
                player += 1
            elif cell == 'C':
                collection += 1
            elif cell == 'E':
                exit_point += 1
            elif cell == 'K':
                key += 1

    if not player == 1:
        print("Error: only 1 'P' needed within the map")
        return False
    if not exit_point == 1:
        print("Error: only 1 'E' needed within the map")
        return False
    if not collection > 0:
        print("Error: at leat 1 'C' within the map")
        return False
    if not key == 1:
        print("Error: at least 1 'K' within the map")
    return True


def is_valid_map_shape(game_map):
    width = len(game_map[0])

    for row in game_map:
        if len(row) != width:
            print("Error: length must be equal")
            return False
    return True


def is_valid_map(game_map):
    if not game_map:
        print("Error: game map cannot be empty")
        return False
    if not (
        is_valid_outer_wall(game_map) and
        is_valid_map_shape(game_map) and
        is_valid_chr(game_map)
    ):
        return False
    return True
