def sum_tuple(t1, t2):
    return (t1[0] + t2[0], t1[1] + t2[1])


def get_neighbours(map, pos):
    char = map[pos][0]
    if char == '|':
        return [(pos[0] - 1, pos[1]), (pos[0] + 1, pos[1])]
    elif char == '-':
        return [(pos[0], pos[1] - 1), (pos[0], pos[1] + 1)]
    elif char == 'L':
        return [(pos[0], pos[1] + 1), (pos[0] - 1, pos[1])]
    elif char == 'J':
        return [(pos[0], pos[1] - 1), (pos[0] - 1, pos[1])]
    elif char == '7':
        return [(pos[0], pos[1] - 1), (pos[0] + 1, pos[1])]
    elif char == 'F':
        return [(pos[0], pos[1] + 1), (pos[0] + 1, pos[1])]
    raise Exception(f"Unknown char: {char}")


def task1(input):
    map = {}
    start = (0, 0)

    for i, line in enumerate(input):
        for j, char in enumerate(line):
            map[(i, j)] = [char, -1]
            if char == 'S':
                start = (i, j)
                map[start][1] = 0

    if map.get(sum_tuple(start, (-1, 0)), ('.', -1))[0] in ['|', '7', 'F']:
        current_position = sum_tuple(start, (-1, 0))
    elif map.get(sum_tuple(start, (0, -1)), ('.', -1))[0] in ['-', 'L', 'F']:
        current_position = sum_tuple(start, (0, -1))
    elif map.get(sum_tuple(start, (0, 1)), ('.', -1))[0] in ['-', 'J', '7']:
        current_position = sum_tuple(start, (0, 1))
    else:
        current_position = sum_tuple(start, (1, 0))
    map[current_position][1] = 1
    counter = 2
    while current_position != start:
        n = get_neighbours(map, current_position)

        if map[n[0]][1] in [-1, 'A', 'B']:
            current_position = n[0]
        elif map[n[1]][1] in [-1, 'A', 'B']:
            current_position = n[1]
        else:
            break
        map[current_position][1] = counter
        counter += 1

    return counter//2, map


LEFT = (0, -1)
RIGHT = (0, 1)
UP = (-1, 0)
DOWN = (1, 0)


def mark_map(map, current, next):
    if sum_tuple(current, UP) == next:
        # FROM DOWN
        if map[next][0] == '|':
            if map.get(sum_tuple(next, RIGHT), ('.', 0))[1] == -1:
                map[sum_tuple(next, RIGHT)][1] = 'A'
            if map.get(sum_tuple(next, LEFT), ('.', 0))[1] == -1:
                map[sum_tuple(next, LEFT)][1] = 'B'
        elif map[next][0] == 'F':
            if map.get(sum_tuple(next, UP), ('.', 0))[1] == -1:
                map[sum_tuple(next, UP)][1] = 'B'
            if map.get(sum_tuple(next, LEFT), ('.', 0))[1] == -1:
                map[sum_tuple(next, LEFT)][1] = 'B'
        elif map[next][0] == '7':
            if map.get(sum_tuple(next, UP), ('.', 0))[1] == -1:
                map[sum_tuple(next, UP)][1] = 'A'
            if map.get(sum_tuple(next, RIGHT), ('.', 0))[1] == -1:
                map[sum_tuple(next, RIGHT)][1] = 'A'
    elif sum_tuple(current, LEFT) == next:
        # FROM RIGHT
        if map[next][0] == '-':
            if map.get(sum_tuple(next, UP), ('.', 0))[1] == -1:
                map[sum_tuple(next, UP)][1] = 'A'
            if map.get(sum_tuple(next, DOWN), ('.', 0))[1] == -1:
                map[sum_tuple(next, DOWN)][1] = 'B'
        elif map[next][0] == 'L':
            if map.get(sum_tuple(next, LEFT), ('.', 0))[1] == -1:
                map[sum_tuple(next, LEFT)][1] = 'B'
            if map.get(sum_tuple(next, DOWN), ('.', 0))[1] == -1:
                map[sum_tuple(next, DOWN)][1] = 'B'
        elif map[next][0] == 'F':
            if map.get(sum_tuple(next, LEFT), ('.', 0))[1] == -1:
                map[sum_tuple(next, LEFT)][1] = 'A'
            if map.get(sum_tuple(next, UP), ('.', 0))[1] == -1:
                map[sum_tuple(next, UP)][1] = 'A'
    elif sum_tuple(current, RIGHT) == next:
        # FROM LEFT
        if map[next][0] == '-':
            if map.get(sum_tuple(next, UP), ('.', 0))[1] == -1:
                map[sum_tuple(next, UP)][1] = 'B'
            if map.get(sum_tuple(next, DOWN), ('.', 0))[1] == -1:
                map[sum_tuple(next, DOWN)][1] = 'A'
        elif map[next][0] == 'J':
            if map.get(sum_tuple(next, RIGHT), ('.', 0))[1] == -1:
                map[sum_tuple(next, RIGHT)][1] = 'A'
            if map.get(sum_tuple(next, DOWN), ('.', 0))[1] == -1:
                map[sum_tuple(next, DOWN)][1] = 'A'
        elif map[next][0] == '7':
            if map.get(sum_tuple(next, RIGHT), ('.', 0))[1] == -1:
                map[sum_tuple(next, RIGHT)][1] = 'B'
            if map.get(sum_tuple(next, UP), ('.', 0))[1] == -1:
                map[sum_tuple(next, UP)][1] = 'B'
    elif sum_tuple(current, DOWN) == next:
        # FROM UP
        if map[next][0] == '|':
            if map.get(sum_tuple(next, RIGHT), ('.', 0))[1] == -1:
                map[sum_tuple(next, RIGHT)][1] = 'B'
            if map.get(sum_tuple(next, LEFT), ('.', 0))[1] == -1:
                map[sum_tuple(next, LEFT)][1] = 'A'
        elif map[next][0] == 'L':
            if map.get(sum_tuple(next, LEFT), ('.', 0))[1] == -1:
                map[sum_tuple(next, LEFT)][1] = 'A'
            if map.get(sum_tuple(next, DOWN), ('.', 0))[1] == -1:
                map[sum_tuple(next, DOWN)][1] = 'A'
        elif map[next][0] == 'J':
            if map.get(sum_tuple(next, RIGHT), ('.', 0))[1] == -1:
                map[sum_tuple(next, RIGHT)][1] = 'B'
            if map.get(sum_tuple(next, DOWN), ('.', 0))[1] == -1:
                map[sum_tuple(next, DOWN)][1] = 'B'


def mark_remaining(input, map, color):
    positions = []

    for i in range(len(input)):
        for j in range(len(input[i])):
            if map[(i, j)][1] == color:
                positions.append((i, j))

    while positions:
        current = positions.pop()
        if current not in map:
            continue
        map[current][1] = color

        for direction in [UP, DOWN, LEFT, RIGHT]:
            if map.get(sum_tuple(current, direction), ('.', 0))[1] == -1:
                positions.append(sum_tuple(current, direction))


def task2(input):
    map = {}
    start = (0, 0)

    for i, line in enumerate(input):
        for j, char in enumerate(line):
            map[(i, j)] = [char, -1]
            if char == 'S':
                start = (i, j)
                map[start][1] = 0

    for i in range(-1, len(input)+1):
        map[(i, -1)] = ['.', -1]
        map[(i, len(input[0]))] = ['.', -1]

    for i in range(-1, len(input[0])+1):
        map[(-1, i)] = ['.', -1]
        map[(len(input), i)] = ['.', -1]

    if map.get(sum_tuple(start, (-1, 0)), ('.', -1))[0] in ['|', '7', 'F']:
        current_position = sum_tuple(start, (-1, 0))
    elif map.get(sum_tuple(start, (0, -1)), ('.', -1))[0] in ['-', 'L', 'F']:
        current_position = sum_tuple(start, (0, -1))
    elif map.get(sum_tuple(start, (0, 1)), ('.', -1))[0] in ['-', 'J', '7']:
        current_position = sum_tuple(start, (0, 1))
    else:
        current_position = sum_tuple(start, (1, 0))
    map[current_position][1] = 1
    counter = 2
    while current_position != start:
        n = get_neighbours(map, current_position)

        if map[n[0]][1] in [-1, 'A', 'B']:
            mark_map(map, current_position, n[0])
            current_position = n[0]
        elif map[n[1]][1] in [-1, 'A', 'B']:
            mark_map(map, current_position, n[1])
            current_position = n[1]
        else:
            break
        map[current_position][1] = counter
        counter += 1

    mark_remaining(input, map, 'A')
    mark_remaining(input, map, 'B')

    color_counter = {
        'A': 0,
        'B': 0,
    }

    for i in range(-1, len(input)+1):
        for j in range(-1, len(input[0])+1):
            if map[(i, j)][1] == 'A':
                color_counter['A'] += 1
            elif map[(i, j)][1] == 'B':
                color_counter['B'] += 1

    outside_color = map[(-1, -1)][1]

    return color_counter['A'] if outside_color == 'B' else color_counter['B']


def read_input():
    with open('input.txt', 'r') as f:
        return f.read().splitlines()


if __name__ == '__main__':
    input = read_input()
    print(task1(input)[0])
    print(task2(input))
