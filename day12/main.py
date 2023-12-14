MEMORY = {}


def calculate(line, config):
    # print(line, config)
    if (line, tuple(config)) in MEMORY:
        return MEMORY[(line, tuple(config))]
    if not line:
        return 1 if not config else 0
    if len(config) == 0:
        return 1 if '#' not in line else 0
    if sum(config) + len(config) - 1 > len(line):
        return 0

    if line[-1] == '.':
        MEMORY[(line, tuple(config))] = calculate(line[:-1], config)
        return MEMORY[(line, tuple(config))]
    if line[-1] == '#':
        for i in range(len(line)-1, len(line)-config[-1]-1, -1):
            if line[i] == '.':
                MEMORY[(line, tuple(config))] = 0
                return 0
        if len(line) == config[-1]:
            MEMORY[(line, tuple(config))] = 1 if len(config) == 1 else 0
            return 1 if len(config) == 1 else 0
        if line[-config[-1]-1] == '#':
            MEMORY[(line, tuple(config))] = 0
            return 0
        MEMORY[(line, tuple(config))] = calculate(line[:-config[-1]-1], config[:-1])
        return MEMORY[(line, tuple(config))]
    if line[-1] == '?':
        for i in range(len(line)-1, len(line)-config[-1]-1, -1):
            if line[i] == '.':
                MEMORY[(line, tuple(config))] = calculate(line[:-1], config)
                return MEMORY[(line, tuple(config))]
        if len(line) == config[-1]:
            return 1 if len(config) == 1 else 0
        if line[-config[-1]-1] == '#':
            MEMORY[(line, tuple(config))] = calculate(line[:-1], config)
            return MEMORY[(line, tuple(config))]
        MEMORY[(line, tuple(config))] = (
            calculate(line[:-1], config)
            + calculate(line[:-config[-1]-1], config[:-1])
        )
        return MEMORY[(line, tuple(config))]
    raise Exception('Invalid line')


def task1(input):
    sum = 0
    for whole_line in input:
        line, config = whole_line.split(' ')
        config = [int(i) for i in config.split(',')]

        sum += calculate(line, config)
    return sum


def task2(input):
    sum = 0
    for whole_line in input:
        line, config = whole_line.split(' ')
        line = '?'.join(5*[line])
        config = 5*[int(i) for i in config.split(',')]

        sum += calculate(line, config)
    return sum


def read_input():
    with open('input.txt', 'r') as f:
        return f.read().splitlines()


if __name__ == '__main__':
    input = read_input()
    print(task1(input))
    print(task2(input))
