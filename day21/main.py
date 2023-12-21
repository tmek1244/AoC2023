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
            if map[(i, j)].char == '#':
                print('#', end='')
            elif map[(i, j)].visited[0]:
                total += 1
                print('O', end='')
            else:
                print('.', end='')
        print()

    return total


def task2(input):
    starting = (0, 0)
    visited = set()

    for i in range(0, len(input)):
        for j in range(0, len(input[i])):
            if input[i][j] == 'S':
                starting = (i, j)

    queue = [starting]
    for i in range(5000+1):
        new_queue = []

        for pos in queue:
            if pos in visited:
                continue
            transtated_pos = (pos[0] % len(input), pos[1] % len(input[0]))
            if input[transtated_pos[0]][transtated_pos[1]] == '#':
                continue
            visited.add(pos)

            for (x, y) in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                new_queue.append((pos[0] + x, pos[1] + y))

        queue = new_queue

    return len([x for x in visited if (x[0] + x[1]) % 2 == 0])


def read_input():
    with open('test.txt', 'r') as f:
        return f.read().splitlines()


if __name__ == '__main__':
    input = read_input()
    # print(task1(input))
    print(task2(input))
