import sys
from Srcs import utils


def load_map(map_path):
    game_map = []

    with open(map_path, 'r') as file:
        try:
            for row in file:
                line = row.strip()
                if line:
                    game_map.append(list(line))
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
    status = True

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

    if not player:
        print("Error: 1 'P' needed within the map")
        status = False
    if player > 1:
        print("Error: only 1 'P' needed within the map")
        status = False
    if not exit_point:
        print("Error: 1 'E' needed within the map")
        status = False
    if exit_point > 1:
        print("Error: only 1 'E' needed within the map")
        status = False
    if not collection > 0:
        print("Error: at leat 1 'C' within the map")
        status = False
    if not key:
        print("Error: 1 'K' needed within the map")
        status = False
    if key > 1:
        print("Error: only 1 'K' needed within the map")
        status = False
    

    return status


def is_valid_map_shape(game_map):
    width = len(game_map[0])

    for row in game_map:
        if len(row) != width:
            print("Error: length must be equal")
            return False
    return True


def is_valid_path(game_map):
    chrs = ['C', 'E', 'K']
    start_pos = utils.get_player_pos(game_map)
    py, px = start_pos

    targets_to_find = []
    for y, row in enumerate(game_map):
        for x, cell in enumerate(row):
            if cell in chrs:
                targets_to_find.append((y, x))
    
    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    queue = [start_pos]
    visited = set(start_pos)

    reachable_targets = 0
    width = len(game_map[0])
    height = len(game_map)

    while queue:
        cur_y, cur_x = queue.pop(0)

        for dy, dx in dirs:
            ny, nx = cur_y + dy, cur_x + dx

            if (
                ny >= 0 and
                ny < height and
                nx >= 0 and
                nx < width and
                game_map[ny][nx] != '1' and
                (ny, nx) not in visited
            ):
                visited.add((ny, nx))
                queue.append((ny, nx))

                if game_map[ny][nx] in chrs:
                    reachable_targets += 1
    
    return reachable_targets == len(targets_to_find)


def is_valid_map(game_map):
    if not game_map:
        print("Error: game map cannot be empty")
        return False

    if not (
        is_valid_map_shape(game_map) and
        is_valid_outer_wall(game_map) and
        is_valid_chr(game_map)
    ):
        return False

    if not is_valid_path(game_map):
        print("Error: flood fill checking failed")
        return False
    
    return True
