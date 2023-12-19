import copy


def sum_tuples(a, b):
    return (a[0] + b[0], a[1] + b[1])


class Line:
    def __init__(self, start, end, x):
        self.start = max(start, end)
        self.end = min(start, end) - 1
        self.x = x

    def __len__(self):
        return abs(self.start - self.end)

    def __repr__(self) -> str:
        return f'({self.start}, {self.end})'


def check_intersection(_vertical_lines, _open_lines):
    vertical_lines = copy.deepcopy(_vertical_lines)
    open_lines = copy.deepcopy(_open_lines)

    i, j = 0, 0

    next_open_lines = []
    addition = 0

    while i < len(vertical_lines) and j < len(open_lines):
        if vertical_lines[i].start < open_lines[j][1]:
            next_open_lines.append(open_lines[j])
            j += 1
        elif vertical_lines[i].end > open_lines[j][0]:
            next_open_lines.append(
                (vertical_lines[i].start, vertical_lines[i].end))
            i += 1
        elif vertical_lines[i].start <= open_lines[j][0] and vertical_lines[i].end >= open_lines[j][1]:
            if vertical_lines[i].start != open_lines[j][0]:
                next_open_lines.append(
                    (open_lines[j][0], vertical_lines[i].start - 1))
                addition -= 1
            if vertical_lines[i].end != open_lines[j][1]:
                open_lines[j] = (vertical_lines[i].end + 1, open_lines[j][1])
                addition -= 1
            else:
                j += 1
            addition += vertical_lines[i].start - vertical_lines[i].end
            i += 1
        elif vertical_lines[i].start == open_lines[j][1] + 1:
            vertical_lines[i].start = open_lines[j][0]

            j += 1
        elif vertical_lines[i].end == open_lines[j][0] - 1:
            open_lines[j] = (vertical_lines[i].start, open_lines[j][1])
            i += 1

    for k in range(i, len(vertical_lines)):
        next_open_lines.append(
            (vertical_lines[k].start, vertical_lines[k].end))
    for k in range(j, len(open_lines)):
        next_open_lines.append(open_lines[k])

    return next_open_lines, addition


def calculate(input, parse_line):
    position = (0, 0)

    vertical_lines = {}

    current_opens = []

    for line in input:
        length, dir = parse_line(line)

        if dir in [1, 3]:
            if position[0] not in vertical_lines:
                vertical_lines[position[0]] = []
            vertical_lines[position[0]].append(Line(
                position[1], position[1] + (dir-2)*length, position[0]))
            position = sum_tuples(position, (0, length * (dir - 2)))
        if dir in [0, 2]:
            position = sum_tuples(position, (length * (1 - dir), 0))

    vertical_lines = {
        key: sorted(value, key=lambda x: x.start, reverse=True)
        for key, value in vertical_lines.items()
    }

    next_stops = sorted(vertical_lines.keys())
    total = 0
    prev_stop = -9999
    for stop in next_stops:
        total += sum([x[0] - x[1] for x in current_opens]) * (stop - prev_stop)
        current_opens, addition = check_intersection(vertical_lines[stop], current_opens)
        total += addition
        prev_stop = stop

    return total


def task1(input):
    def parse_line(line):
        dir, length, _ = line.split(' ')
        return int(length), {
            'R': 0, 'D': 1, 'L': 2, 'U': 3
        }[dir]

    return calculate(input, parse_line)


def task2(input):
    def parse_line(line):
        _, _, color = line.split(' ')
        color = color[2:-1]
        return int(color[:-1], 16), int(color[-1])

    return calculate(input, parse_line)


def read_input():
    with open('input.txt', 'r') as f:
        return f.read().splitlines()


if __name__ == '__main__':
    input = read_input()
    print(task1(input))
    print(task2(input))
