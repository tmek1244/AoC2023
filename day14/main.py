def tilt_up(input):
    for col in range(len(input[0])):
        counter = 0
        for row in range(len(input)):
            if input[row][col] == '#':
                counter = row + 1
            if input[row][col] == 'O':
                input[row][col] = '.'
                input[counter][col] = 'O'
                counter += 1
    return input


def tilt_down(input):
    for col in range(len(input[0])):
        counter = len(input) - 1
        for row in range(len(input) - 1, -1, -1):
            if input[row][col] == '#':
                counter = row - 1
            if input[row][col] == 'O':
                input[row][col] = '.'
                input[counter][col] = 'O'
                counter -= 1
    return input


def tilt_left(input):
    for row in range(len(input)):
        counter = 0
        for col in range(len(input[0])):
            if input[row][col] == '#':
                counter = col + 1
            if input[row][col] == 'O':
                input[row][col] = '.'
                input[row][counter] = 'O'
                counter += 1
    return input


def tilt_right(input):
    for row in range(len(input)):
        counter = len(input[0]) - 1
        for col in range(len(input[0]) - 1, -1, -1):
            if input[row][col] == '#':
                counter = col - 1
            if input[row][col] == 'O':
                input[row][col] = '.'
                input[row][counter] = 'O'
                counter -= 1
    return input


def rotation(input):
    return tilt_right(tilt_down(tilt_left(tilt_up(input))))


def score(input):
    sum = 0
    for i in range(len(input)):
        for j in range(len(input[0])):
            if input[i][j] == 'O':
                sum += len(input) - i
    return sum


def task1(input):
    map = [list(line) for line in input]

    return score(tilt_up(map))


def task2(input):
    map = [list(line) for line in input]

    memory = {}
    tilted = map
    for i in range(1, 1000000001):
        tilted = rotation(tilted)
        current_map = ''.join([''.join(line) for line in tilted])
        if current_map in memory:
            difference = i - memory[current_map]
            last_position = (1_000_000_000 - i) % difference

            for _ in range(last_position):
                tilted = rotation(tilted)

            return score(tilted)
        else:
            memory[current_map] = i

    return 0


def read_input():
    with open('input.txt', 'r') as f:
        return f.read().splitlines()


if __name__ == '__main__':
    input = read_input()
    print(task1(input))
    print(task2(input))
