
class Node:
    def __init__(self, id, left, right):
        self.id = id
        self.right = right
        self.left = left


def parse_input(input):
    nodes = {}

    path = input[0]

    for line in input[2:]:
        node_id, children = line.replace(' ', '').split('=')
        children = children[1 : -1]
        children = children.split(',')

        if children[0] not in nodes:
            nodes[children[0]] = Node(children[0], None, None)
        if children[1] not in nodes:
            nodes[children[1]] = Node(children[1], None, None)
        if node_id not in nodes:
            nodes[node_id] = Node(node_id, nodes[children[0]], nodes[children[1]])
        else:
            nodes[node_id].left = nodes[children[0]]
            nodes[node_id].right = nodes[children[1]]
    
    nodes_end = {x: "" for x in nodes.keys()}

    for node_id, node in nodes.items():
        current_node = node_id
        for turn in path:
            # print(turn, current_node)
            if turn == 'L':
                current_node = nodes[current_node].left.id
            else:
                current_node = nodes[current_node].right.id
        nodes_end[node_id] = current_node
    
    return nodes_end, path


def task1(input):
    nodes_end, path = parse_input(input)
    
    steps = 0
    current_node = "AAA"
    while current_node != "ZZZ":
        current_node = nodes_end[current_node]
        steps += len(path)

    return steps


def task2(input):
    nodes_end, path = parse_input(input)

    steps = 0
    currents_nodes = []
    for node_id in nodes_end.keys():
        if node_id[-1] == 'A':
            currents_nodes.append(node_id)

    sum = 0
    for node in nodes_end.keys():
        if node[-1] == "Z":
            sum += 1
    print(sum)
    while True:
        # print(currents_nodes)
        for node in currents_nodes:
            if node[-1] != "Z":
                break
        else:
            break
        steps += len(path)

        new_currents_nodes = []
        for node in currents_nodes:
            new_currents_nodes.append(nodes_end[node])

        currents_nodes = new_currents_nodes
    
    return steps


def read_input():
    with open('input.txt', 'r') as f:
        return f.read().splitlines()


if __name__ == '__main__':
    input = read_input()
    print(task1(input))
    print(task2(input))
