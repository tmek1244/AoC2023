DIRECTIONS = {
    'R': (0, 1),
    'L': (0, -1),
    'U': (-1, 0),
    'D': (1, 0)
}


def sum_tuples(a, b):
    return (a[0] + b[0], a[1] + b[1])


def mark_map(map, position, direction):
    if direction == 'R':
        if (pos := sum_tuples(position, (-1, 0))) not in map:
            map[pos] = 'A'
        if (pos := sum_tuples(position, (1, 0))) not in map:
            map[pos] = 'B'
    if direction == 'L':
        if (pos := sum_tuples(position, (1, 0))) not in map:
            map[pos] = 'A'
        if (pos := sum_tuples(position, (-1, 0))) not in map:
            map[pos] = 'B'
    if direction == 'U':
        if (pos := sum_tuples(position, (0, -1))) not in map:
            map[pos] = 'A'
        if (pos := sum_tuples(position, (0, 1))) not in map:
            map[pos] = 'B'
    if direction == 'D':
        if (pos := sum_tuples(position, (0, 1))) not in map:
            map[pos] = 'A'
        if (pos := sum_tuples(position, (0, -1))) not in map:
            map[pos] = 'B'


def task1(input):
    map = {}

    position = (0, 0)
    map[position] = '#'

    for line in input:
        direction, lenght, _ = line.split(' ')
        lenght = int(lenght)
        mark_map(map, position, direction)
        for _ in range(lenght):
            position = sum_tuples(position, DIRECTIONS[direction])
            mark_map(map, position, direction)

            map[position] = '*'
        map[position] = '#'

    min_x = min(map.keys(), key=lambda x: x[0])[0]
    max_x = max(map.keys(), key=lambda x: x[0])[0]
    min_y = min(map.keys(), key=lambda x: x[1])[1]
    max_y = max(map.keys(), key=lambda x: x[1])[1]

    char_at_top = ''
    for i in range(min_x, max_x + 1):
        if map.get((i, min_y)):
            char_at_top = map.get((i, min_y))
            break
    char_inside = 'A' if char_at_top == 'B' else 'B'

    total = 0

    elems = []

    for key, value in map.items():
        if value == char_inside:
            elems.append(key)

    while elems:
        elem = elems.pop()
        map[elem] = char_inside
        for direction in DIRECTIONS.values():
            if (pos := sum_tuples(elem, direction)) not in map:
                elems.append(pos)

    for i in range(min_x, max_x + 1):
        for j in range(min_y, max_y + 1):
            if map.get((i, j)) in ['#', '*', char_inside]:
                total += 1
        #     print(map.get((i, j), '.'), end='')
        # print()

    return total


def task2(input):
    return 0


def read_input():
    with open('input.txt', 'r') as f:
        return f.read().splitlines()


if __name__ == '__main__':
    input = read_input()
    print(task1(input))
    print(task2(input))
