class Light:
    def __init__(self, from_field, to_field):
        self.from_field = from_field
        self.to_field = to_field

    def __eq__(self, __value: object) -> bool:
        return self.from_field == __value.from_field and self.to_field == __value.to_field


def get_same_direction_light(light):
    current_positon = light.to_field
    next_position = (
        current_positon[0] + light.to_field[0] - light.from_field[0],
        current_positon[1] + light.to_field[1] - light.from_field[1]
    )
    return [Light(current_positon, next_position)]


LEFT = (0, -1)
RIGHT = (0, 1)
UP = (-1, 0)
DOWN = (1, 0)

DIRECTIONS = {
    LEFT: LEFT,
    RIGHT: RIGHT,
    UP: UP,
    DOWN: DOWN
}


def get_light_direction(light):
    horizontal = light.to_field[0] - light.from_field[0]
    vertical = light.to_field[1] - light.from_field[1]
    return DIRECTIONS[(horizontal, vertical)]


def get_next_lights(light, map):
    current_positon = light.to_field

    if map[current_positon[0]][current_positon[1]] == '.':
        return get_same_direction_light(light)
    elif map[current_positon[0]][current_positon[1]] == '/':
        direction = get_light_direction(light)
        if direction == LEFT:
            return [Light(current_positon, (current_positon[0] + 1, current_positon[1]))]
        elif direction == RIGHT:
            return [Light(current_positon, (current_positon[0] - 1, current_positon[1]))]
        elif direction == UP:
            return [Light(current_positon, (current_positon[0], current_positon[1] + 1))]
        elif direction == DOWN:
            return [Light(current_positon, (current_positon[0], current_positon[1] - 1))]
    elif map[current_positon[0]][current_positon[1]] == '\\':
        direction = get_light_direction(light)
        if direction == LEFT:
            return [Light(current_positon, (current_positon[0] - 1, current_positon[1]))]
        elif direction == RIGHT:
            return [Light(current_positon, (current_positon[0] + 1, current_positon[1]))]
        elif direction == UP:
            return [Light(current_positon, (current_positon[0], current_positon[1] - 1))]
        elif direction == DOWN:
            return [Light(current_positon, (current_positon[0], current_positon[1] + 1))]
    elif map[current_positon[0]][current_positon[1]] == '|':
        direction = get_light_direction(light)
        if direction == LEFT or direction == RIGHT:
            return [Light(current_positon, (current_positon[0] - 1, current_positon[1])),
                    Light(current_positon, (current_positon[0] + 1, current_positon[1]))]
        else:
            return get_same_direction_light(light)
    elif map[current_positon[0]][current_positon[1]] == '-':
        direction = get_light_direction(light)
        if direction == UP or direction == DOWN:
            return [Light(current_positon, (current_positon[0], current_positon[1] - 1)),
                    Light(current_positon, (current_positon[0], current_positon[1] + 1))]
        else:
            return get_same_direction_light(light)


def task1(input, starting_light=Light((0, -1), (0, 0))):
    map = [list(line) for line in input]
    light_map = []
    for i in range(len(map)):
        light_map.append([])
        for j in range(len(map[0])):
            light_map[i].append([])

    lights = [starting_light]
    while lights:
        light = lights.pop()

        if (light.to_field[0] < 0 or light.to_field[0] >= len(map)
                or light.to_field[1] < 0 or light.to_field[1] >= len(map[0])):
            continue
        if light in light_map[light.to_field[0]][light.to_field[1]]:
            continue

        light_map[light.to_field[0]][light.to_field[1]].append(light)
        lights.extend(get_next_lights(light, map))

    sum = 0
    for i in range(len(light_map)):
        for j in range(len(light_map[0])):
            if light_map[i][j]:
                sum += 1

    return sum


def task2(input):
    results = []
    for i in range(len(input)):
        results.append(task1(input, Light((i, -1), (i, 0))))
        results.append(task1(input, Light((i, len(input[0])), (i, len(input[0]) - 1))))
    for j in range(len(input[0])):
        results.append(task1(input, Light((-1, j), (0, j))))
        results.append(task1(input, Light((len(input), j), (len(input) - 1, j))))

    return max(results)


def read_input():
    with open('input.txt', 'r') as f:
        return f.read().splitlines()


if __name__ == '__main__':
    input = read_input()
    print(task1(input))
    print(task2(input))
