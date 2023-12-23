class Field:
    def __init__(self, char):
        self.char = char
        self.visited = [False, False]


def task1(input):
    map = {}

    starting = (0, 0)

    for i in range(0, len(input)):
        for j in range(0, len(input[i])):
            if input[i][j] == 'S':
                starting = (i, j)
            map[(i, j)] = Field(input[i][j])

    queue = [starting]
    for i in range(64+1):
        new_queue = []

        for pos in queue:
            field = map[pos]
            if field.char == '#':
                continue
            if field.visited[i % 2]:
                continue
            field.visited[i % 2] = True

            for (x, y) in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                new_pos = (pos[0] + x, pos[1] + y)
                if new_pos in map:
                    new_queue.append(new_pos)

        queue = new_queue

    total = 0
    for i in range(0, len(input)):
        for j in range(0, len(input[i])):
            if map[(i, j)].visited[0]:
                total += 1

    return total


def traverse(map, start_pos, max_steps):
    visited = set()
    queue = [start_pos]
    for i in range(max_steps+1):
        new_queue = []

        for pos in queue:
            if map[pos] == '#':
                continue
            if pos in visited:
                continue
            visited.add(pos)

            for (x, y) in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                new_pos = (pos[0] + x, pos[1] + y)
                if new_pos in map:
                    new_queue.append(new_pos)

        queue = new_queue

    odd = len([x for x in visited if (x[0] + x[1]) % 2 == 1])
    even = len([x for x in visited if (x[0] + x[1]) % 2 == 0])
    return odd, even


def task2(input):
    starting = (0, 0)
    map = {}

    counter = 0
    for i in range(0, len(input)):
        for j in range(0, len(input[i])):
            if input[i][j] == 'S':
                starting = (i, j)
            map[(i, j)] = input[i][j]
            if input[i][j] == '#':
                counter += 1

    steps = 26501365

    shift = (steps - starting[0])//len(input)
    result = traverse(map, starting, 10000)
    PARITY = steps % 2

    total = (
        traverse(map, (65, 130), 130)[(PARITY + shift + 1) % 2] + traverse(map, (65, 0), 130)[(PARITY + shift + 1) % 2]
        + traverse(map, (0, 65), 130)[(PARITY + shift + 1) % 2] + traverse(map, (130, 65), 130)[(PARITY + shift + 1) % 2]
    )

    total += shift**2 * result[(PARITY + shift) % 2] + (shift - 1)**2 * result[(PARITY + shift + 1) % 2]

    total += shift * traverse(map, (0, 0), 64)[(PARITY + shift) % 2]
    total += shift * traverse(map, (0, 130), 64)[(PARITY + shift) % 2]
    total += shift * traverse(map, (130, 0), 64)[(PARITY + shift) % 2]
    total += shift * traverse(map, (130, 130), 64)[(PARITY + shift) % 2]

    total += (shift - 1) * traverse(map, (0, 0), 130 + 65)[(PARITY + shift + 1) % 2]
    total += (shift - 1) * traverse(map, (0, 130), 130 + 65)[(PARITY + shift + 1) % 2]
    total += (shift - 1) * traverse(map, (130, 0), 130 + 65)[(PARITY + shift + 1) % 2]
    total += (shift - 1) * traverse(map, (130, 130), 130 + 65)[(PARITY + shift + 1) % 2]

    return total


def read_input():
    with open('input.txt', 'r') as f:
        return f.read().splitlines()


if __name__ == '__main__':
    input = read_input()
    print(task1(input))
    print(task2(input))
