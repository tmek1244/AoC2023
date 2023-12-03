import re


def task1(i):
    f = lambda x, b, l: all([int(x) <= b for x in re.findall(fr'(\d*) {x}', l)])

    return sum([
        i for i, l in enumerate(i, 1)
        if f('r', 12, l) and f('g', 13, l) and f('b', 14, l)
    ])


def task2(i):
    f = lambda x, l: max([int(x) for x in re.findall(fr'(\d*) {x}', l)])

    return sum([
        f('r', l) * f('g', l) * f('b', l) for l in i
    ])


def read_input():
    with open('input.txt', 'r') as f:
        return f.read().splitlines()


if __name__ == '__main__':
    input = read_input()
    print(task1(input))
    print(task2(input))
