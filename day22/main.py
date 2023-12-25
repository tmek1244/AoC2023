class Block:
    def __init__(self, start, end):
        self.start = [min(start[0], end[0]), min(start[1], end[1]), min(start[2], end[2])]
        self.end = [max(start[0], end[0]), max(start[1], end[1]), max(start[2], end[2])]

        self.supports = []
        self.lays_on = []
        self.counter = 1

    def __repr__(self):
        return f'{self.start} ~ {self.end}'

    def overlaps(self, other):
        return not (self.start[0] > other.end[0]
                    or self.end[0] < other.start[0]
                    or self.start[1] > other.end[1]
                    or self.end[1] < other.start[1])


def task1(input):
    blocks = []

    for line in input:
        start, end = line.split('~')
        eval('blocks.append(Block((' + start + '), (' + end + ')))')

    blocks.sort(key=lambda x: x.start[2])

    for i in range(len(blocks)):
        in_air = True
        for j in range(i-1, -1, -1):
            # print(blocks[i], blocks[j])
            if blocks[i].overlaps(blocks[j]):
                if blocks[j].end[2] < blocks[i].start[2] and not in_air:
                    continue
                # print(blocks[j].end[2], blocks[i].start[2], not in_air)
                # print('overlaps:', end=' ')
                in_air = False
                blocks[i].end[2] = blocks[i].end[2] - blocks[i].start[2] + blocks[j].end[2] + 1
                blocks[i].start[2] = blocks[j].end[2] + 1
        if in_air:
            blocks[i].end[2] =  blocks[i].end[2] - blocks[i].start[2] + 1
            blocks[i].start[2] = 1
                # print(blocks[i])
        # print(blocks[:i+1])
        # print()

    for i in range(len(blocks)):
        for j in range(i-1, -1, -1):
            if blocks[j].end[2] == blocks[i].start[2] - 1 and blocks[j].overlaps(blocks[i]):
                blocks[i].lays_on.append(blocks[j])
                blocks[j].supports.append(blocks[i])

    total = 0
    for block in blocks:
        for support in block.supports:
            if len(support.lays_on) <= 1:
                break
        else:
            total += 1

    return total


def find_which_fails(starting):
    queue = []
    already_fallen = set()
    counter = 1
    already_fallen.add(starting)
    for support in starting.supports:
        if support not in already_fallen and support not in queue:
            queue.append(support)
    queue = sorted(queue, key=lambda x: x.end[2])
    while queue:
        block = queue.pop(0)

        for lays_on in block.lays_on:
            if lays_on not in already_fallen:
                break
        else:
            counter += 1
            already_fallen.add(block)
            for support in block.supports:
                if support not in already_fallen and support not in queue:
                    queue.append(support)
        queue = sorted(queue, key=lambda x: x.end[2])
    # print(counter, already_fallen)
    return counter


def task2(input):
    blocks = []

    for line in input:
        start, end = line.split('~')
        eval('blocks.append(Block((' + start + '), (' + end + ')))')

    blocks.sort(key=lambda x: x.start[2])

    for i in range(len(blocks)):
        in_air = True
        for j in range(i-1, -1, -1):
            # print(blocks[i], blocks[j])
            if blocks[i].overlaps(blocks[j]):
                if blocks[j].end[2] < blocks[i].start[2] and not in_air:
                    continue
                # print(blocks[j].end[2], blocks[i].start[2], not in_air)
                # print('overlaps:', end=' ')
                in_air = False
                blocks[i].end[2] = blocks[i].end[2] - blocks[i].start[2] + blocks[j].end[2] + 1
                blocks[i].start[2] = blocks[j].end[2] + 1
        if in_air:
            blocks[i].end[2] =  blocks[i].end[2] - blocks[i].start[2] + 1
            blocks[i].start[2] = 1
                # print(blocks[i])
        # print(blocks[:i+1])
        # print()

    for i in range(len(blocks)):
        for j in range(i-1, -1, -1):
            if blocks[j].end[2] == blocks[i].start[2] - 1 and blocks[j].overlaps(blocks[i]):
                blocks[i].lays_on.append(blocks[j])
                blocks[j].supports.append(blocks[i])
    blocks.sort(key=lambda x: x.start[2])
    total = 0

    for block in blocks[::-1]:
        if (x := find_which_fails(block)) > 1:
            total += x - 1

    return total


def read_input():
    with open('input.txt', 'r') as f:
        return f.read().splitlines()


if __name__ == '__main__':
    input = read_input()
    print(task1(input))
    print(task2(input))
