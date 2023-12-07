def parse(input):
    seeds = input[0].split(':')[1].split()
    map_list = []

    line_nr = 1

    for i in range(7):
        map = []
        line_nr += 2
        while line_nr < len(input) and input[line_nr] != '':
            map.append(input[line_nr].split())
            line_nr += 1

        map_list.append(sorted(map, key=lambda x: int(x[1])))
    return seeds, map_list


def task1(input):
    seeds, map_list = parse(input)

    # print(seeds, map_list)
    locations = []

    for seed_str in seeds:
        current_id = int(seed_str)
        # print(current_id)
        for map in map_list:
            for entry in map:
                # print(int(entry[1]), int(entry[1]) + int(entry[2]))
                if int(entry[1]) <= current_id < int(entry[1]) + int(entry[2]):
                    current_id = current_id - int(entry[1]) + int(entry[0])
                    break
                elif int(entry[1]) > current_id:
                    break
            # print(current_id)
        locations.append(current_id)
        # print()
    return min(locations)


def task2(input):
    return 0


def read_input():
    with open('input.txt', 'r') as f:
        return f.read().splitlines()


if __name__ == '__main__':
    input = read_input()
    print(task1(input))
    print(task2(input))
