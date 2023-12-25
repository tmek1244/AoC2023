class Hike:
    def __init__(self) -> None:
        self.history = []


def task1(input):
    starting = (0, 0)
    ending = (0, 0)
    for i in range(0, len(input[0])):
        if input[0][i] == '.':
            starting = (0, i)
        if input[-1][i] == '.':
            ending = (len(input)-1, i)

    hikes = [Hike()]
    hikes[0].history.append(starting)
    done_hikes = []

    while hikes:
        hike = hikes.pop()
        if hike.history[-1] == ending:
            done_hikes.append(hike)
            continue
        for i, direction in enumerate([(0, 1), (1, 0), (0, -1), (-1, 0)]):
            new_pos = (hike.history[-1][0] + direction[0], hike.history[-1][1] + direction[1])
            if new_pos in hike.history:
                continue
            if input[new_pos[0]][new_pos[1]] == '#':
                continue
            nf = input[new_pos[0]][new_pos[1]]
            if nf == '.' or (nf == '>' and i == 0) or (nf == 'v' and i == 1) or (nf == '<' and i == 2) or (nf == '^' and i == 3):
                new_hike = Hike()
                new_hike.history = hike.history.copy()
                new_hike.history.append(new_pos)
                hikes.append(new_hike)
    return max([len(h.history) - 1 for h in done_hikes])


class Node:
    def __init__(self, id) -> None:
        self.id = id
        self.children = {}


def get_path_length(node_history, node_dict):
    total = 0

    for i in range(len(node_history) - 1):
        total += node_dict[node_history[i]].children[node_history[i+1]]

    return total


def parse_input(input, starting, ending):
    graph_map = {starting: 0, ending: -1}
    node_dict = {0: Node(0), -1: Node(-1)}

    node_counter = 1

    for i in range(len(input)):
        for j in range(len(input[0])):
            if input[i][j] == '#':
                continue
            new_directions = []
            for direction in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                new_pos = (i + direction[0], j + direction[1])
                if new_pos[0] < 0 or new_pos[0] >= len(input) or new_pos[1] < 0 or new_pos[1] >= len(input[0]):
                    continue
                if input[new_pos[0]][new_pos[1]] == '#':
                    continue
                new_directions.append(direction)

            if len(new_directions) > 2:
                node_dict[node_counter] = Node(node_counter)
                graph_map[(i, j)] = node_counter
                node_counter += 1

    queue = [(starting, 0)]
    visited = set()

    while queue:
        path_len = 1
        pos, parent = queue.pop(0)
        # print(pos, parent)
        visited.add(pos)
        while pos not in graph_map:
            # print(pos)
            path_len += 1
            for direction in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                new_pos = (pos[0] + direction[0], pos[1] + direction[1])
                if input[new_pos[0]][new_pos[1]] == '#':
                    continue
                if new_pos in graph_map and graph_map[new_pos] != parent:
                    pos = new_pos
                    break
                if new_pos in visited:
                    continue
                pos = new_pos
                break
            else:
                break
            visited.add(pos)
        if pos not in graph_map:
            continue

        if graph_map[pos] != parent:
            node_dict[graph_map[pos]].children[parent] = path_len
            node_dict[parent].children[graph_map[pos]] = path_len

        for direction in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_pos = (pos[0] + direction[0], pos[1] + direction[1])
            if new_pos[0] < 0 or new_pos[0] >= len(input) or new_pos[1] < 0 or new_pos[1] >= len(input[0]):
                continue
            if input[new_pos[0]][new_pos[1]] == '#':
                continue
            if new_pos in visited:
                continue
            queue.append((new_pos, graph_map[pos]))

    hikes = [Hike()]
    hikes[0].history.append(0)
    done_hikes = []

    while hikes:
        hike = hikes.pop()
        if hike.history[-1] == -1:
            done_hikes.append(hike)
            continue
        for child in node_dict[hike.history[-1]].children:
            if child in hike.history:
                continue
            new_hike = Hike()
            new_hike.history = hike.history.copy()
            new_hike.history.append(child)
            hikes.append(new_hike)

    return max([get_path_length(h.history, node_dict) for h in done_hikes])


def task2(input):
    starting = (0, 0)
    ending = (0, 0)
    for i in range(0, len(input[0])):
        if input[0][i] == '.':
            starting = (0, i)
        if input[-1][i] == '.':
            ending = (len(input)-1, i)

    return parse_input(input, starting, ending)


def read_input():
    with open('input.txt', 'r') as f:
        return f.read().splitlines()


if __name__ == '__main__':
    input = read_input()
    print(task1(input))
    print(task2(input))
