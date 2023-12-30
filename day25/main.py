import random
from collections import defaultdict


class Node:
    def __init__(self, id):
        self.id = id
        self.neighbours = []

    def __repr__(self):
        return f'{self.id}'


# def minimum_cut_phase(nodes, node):
#     nodes_set = list([node])
#     left_nodes = list(nodes)
#     left_nodes.remove(node)

#     while len(left_nodes) > 1:
#         mostly_connected_node = None
#         most_connections = 0
#         for node in left_nodes:
#             connections = 0
#             for neighbour in node.neighbours:
#                 if neighbour in nodes_set:
#                     connections += 1

#             if connections > most_connections:
#                 most_connections = connections
#                 mostly_connected_node = node
#         nodes_set.append(mostly_connected_node)
#         left_nodes.remove(mostly_connected_node)
#     print(nodes_set, left_nodes)
#     last_node = left_nodes[0]
#     nr_of_cuts = len(last_node.neighbours)
#     print(last_node, nodes_set[-1], nr_of_cuts)

#     for neighbour in nodes_set[-1].neighbours:
#         neighbour.neighbours.remove(nodes_set[-1])
#         if last_node != neighbour:
#             neighbour.neighbours.append(last_node)
#             last_node.neighbours.append(neighbour)
#     nodes.remove(nodes_set[-1])

#     return nr_of_cuts, last_node


# def minimum_cut(nodes):
#     results = []

#     while len(nodes) > 1:
#         nr_of_cuts, last_node = minimum_cut_phase(nodes, nodes[0])
#         results.append((nr_of_cuts, last_node))

#     print(results)

def minimum_cut_phase(nodes, node):
    nodes_set = list([node])
    left_nodes = list(nodes)
    left_nodes.remove(node)

    while len(left_nodes) > 1:
        mostly_connected_node = None
        most_connections = 0
        for node in left_nodes:
            connections = 0
            for neighbour in node.neighbours:
                if neighbour in nodes_set:
                    connections += 1

            if connections > most_connections:
                most_connections = connections
                mostly_connected_node = node
        nodes_set.append(mostly_connected_node)
        left_nodes.remove(mostly_connected_node)
    print(nodes_set, left_nodes)
    last_node = left_nodes[0]
    nr_of_cuts = len(last_node.neighbours)
    print(last_node, nodes_set[-1], nr_of_cuts)

    for neighbour in nodes_set[-1].neighbours:
        neighbour.neighbours.remove(nodes_set[-1])
        if last_node != neighbour:
            neighbour.neighbours.append(last_node)
            last_node.neighbours.append(neighbour)
    nodes.remove(nodes_set[-1])

    return nr_of_cuts, last_node


def contract(nodes):
    edges = {node.id: defaultdict(int) for node in nodes}
    edges_list = []
    contracted_to = {node.id: node.id for node in nodes}

    for node in nodes:
        for neighbour in node.neighbours:
            edges[node.id][neighbour.id] = 1
            edges_list.append((node.id, neighbour.id))

    for i in range(len(nodes)-2):
        edge = random.choice(edges_list)

        # print(f'removing {edge}')
        node1, node2 = edge
        edges_list.remove(edge)
        edges_list.remove((node2, node1))
        edges[node1].pop(node2)
        contracted_to[node2] = node1

        for node_edge in edges[node2].keys():
            if node_edge == node1:
                continue
            edges[node1][node_edge] += edges[node2][node_edge]
            edges[node_edge][node1] += edges[node2][node_edge]
            edges[node_edge].pop(node2)

        edges.pop(node2)

        edges_list = []
        for node in edges.keys():
            for neighbour, count in edges[node].items():
                for i in range(count):
                    edges_list.append((node, neighbour))

        # print(edges)
        # print(edges_list)
        # print()

    first_node, second_node = edges.keys()

    groups = {
        first_node: set([first_node]),
        second_node: set([second_node])
    }
    node_to_group = {}

    for node in nodes:
        node_id = node.id
        while node_id != contracted_to[node_id]:
            node_id = contracted_to[node_id]
        groups[node_id].add(node.id)
        node_to_group[node.id] = node_id

    # for group in groups.values():
    #     print(group)

    # for node in nodes:
    #     for neighbour in node.neighbours:
    #         if node_to_group[node.id] != node_to_group[neighbour.id]:
    #             edges_to_remove.append((node.id, neighbour.id))
    return edges[first_node][second_node], len(groups[first_node]) * len(groups[second_node])


def task1(input):
    nodes = {}
    edges = []

    for line in input:
        id, neighbours = line.split(':')
        if id not in nodes:
            nodes[id] = Node(id)
        for neighbour in neighbours.split(' '):
            neighbour = neighbour.replace(' ', '')
            if neighbour == '':
                continue
            if neighbour not in nodes:
                nodes[neighbour] = Node(neighbour)
            nodes[id].neighbours.append(nodes[neighbour])
            nodes[neighbour].neighbours.append(nodes[id])
            edges.append((id, neighbour))
        # print(nodes[id].neighbours)
    # for node in nodes.values():
    #     print(node, node.neighbours)
    # print(len(edges))

    nr_of_cuts, groups_mult = contract(list(nodes.values()))
    print(nr_of_cuts, groups_mult)
    while nr_of_cuts > 3:
        nr_of_cuts, groups_mult = contract(list(nodes.values()))
        print(nr_of_cuts, groups_mult)
    return groups_mult


def task2(input):
    pass


def read_input():
    with open('input.txt', 'r') as f:
        return f.read().splitlines()


if __name__ == '__main__':
    input = read_input()
    print(task1(input))
    print(task2(input))
