
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


def find_cycle(nodes_edges, star_node):
    visited = []
    good_nodes = []
    current_node = star_node
    while True:
        if current_node in visited:
            return (
                visited.index(current_node),
                len(visited) - visited.index(current_node),
                [node - visited.index(current_node) for node in good_nodes]
            )
        visited.append(current_node)
        if current_node[-1] == "Z":
            good_nodes.append(len(visited) - 1)
        current_node = nodes_edges[current_node]


def combine_phased_rotations(a_period, a_phase, b_period, b_phase):
    """Combine two phased rotations into a single phased rotation

    Returns: combined_period, combined_phase

    The combined rotation is at its reference point if and only if both a and b
    are at their reference points.
    """
    gcd, s, t = extended_gcd(a_period, b_period)
    phase_difference = a_phase - b_phase
    pd_mult, pd_remainder = divmod(phase_difference, gcd)
    if pd_remainder:
        raise ValueError("Rotation reference points never synchronize.")

    combined_period = a_period // gcd * b_period
    combined_phase = (a_phase - s * pd_mult * a_period) % combined_period
    return combined_period, combined_phase


def arrow_alignment(red_len, green_len, advantage):
    """Where the arrows first align, where green starts shifted by advantage"""
    period, phase = combine_phased_rotations(
        red_len, 0, green_len, -advantage % green_len
    )
    return -phase % period


def extended_gcd(a, b):
    """Extended Greatest Common Divisor Algorithm

    Returns:
        gcd: The greatest common divisor of a and b.
        s, t: Coefficients such that s*a + t*b = gcd

    Reference:
        https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm#Pseudocode
    """
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1
    while r:
        quotient, remainder = divmod(old_r, r)
        old_r, r = r, remainder
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t

    return old_r, old_s, old_t


def task2(input):
    nodes_end, path = parse_input(input)

    nodes_values = {x: (0, 0) for x in nodes_end.keys()}

    for node_id in nodes_end.keys():
        r, circle_len, good_nodes = find_cycle(nodes_end, node_id)

        if len(good_nodes) > 1:
            raise Exception("More than one good node")
        if len(good_nodes) == 0:
            continue
        sum = r + good_nodes[0]
        nodes_values[node_id] = (sum, circle_len)

    nodes_for_search = []
    for node_id, node_value in nodes_values.items():
        if node_id[-1] == "A":
            nodes_for_search.append((node_value[0], node_value[1]))

    node_ = nodes_for_search[0]
    current_sum = node_[0]
    step = node_[1]
    idx = 1
    while True:
        for node in nodes_for_search[idx:]:
            if 0 != (current_sum - node[0]) % node[1]:
                current_sum, step = combine_phased_rotations(current_sum, step, node[0], node[1])
                idx += 1
                break
        else:
            break

    return current_sum * len(path)


def read_input():
    with open('input.txt', 'r') as f:
        return f.read().splitlines()


if __name__ == '__main__':
    input = read_input()
    # print(task1(input))
    print(task2(input))
