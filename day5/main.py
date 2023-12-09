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

    locations = []

    for seed_str in seeds:
        current_id = int(seed_str)
        for map in map_list:
            for entry in map:
                if int(entry[1]) <= current_id < int(entry[1]) + int(entry[2]):
                    current_id = current_id - int(entry[1]) + int(entry[0])
                    break
                elif int(entry[1]) > current_id:
                    break
        locations.append(current_id)
    return min(locations)


class Interval:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __repr__(self):
        return f'[{self.start}, {self.end}]'


class Mapping:
    def __init__(self, source, destination, number) -> None:
        self.start = source
        self.end = source + number - 1
        self.to_start = destination
        self.to_end = destination + number - 1

    def __repr__(self) -> str:
        return f'{self.start} - {self.end} -> {self.to_start} - {self.to_end}'


def task2(input):
    seeds, map_list = parse(input)

    current_intervals = [
        Interval(int(seeds[2*i]), int(seeds[2*i]) + int(seeds[2*i+1]) - 1)
        for i in range(len(seeds)//2)]

    for map in map_list:
        new_lvl_intervals = []
        for _mapping in map:
            mapping = Mapping(int(_mapping[1]), int(_mapping[0]), int(_mapping[2]))
            new_intervals = []
            for interval in current_intervals:
                if interval.start >= mapping.start and interval.end <= mapping.end:
                    new_lvl_intervals.append(Interval(
                        mapping.to_start + interval.start - mapping.start,
                        mapping.to_start + interval.end - mapping.start
                    ))
                elif mapping.end >= interval.start >= mapping.start and interval.end > mapping.end:
                    new_lvl_intervals.append(Interval(
                        mapping.to_start + interval.start - mapping.start,
                        mapping.to_end))
                    new_intervals.append(
                        Interval(mapping.end + 1, interval.end))
                elif interval.start < mapping.start and mapping.start <= interval.end <= mapping.end:
                    new_intervals.append(Interval(interval.start, mapping.start - 1))
                    new_lvl_intervals.append(Interval(
                        mapping.to_start,
                        mapping.to_start + interval.end - mapping.start
                    ))
                elif interval.start < mapping.start and interval.end > mapping.end:
                    new_intervals.append(Interval(interval.start, mapping.start - 1))
                    new_lvl_intervals.append(Interval(
                        mapping.to_start,
                        mapping.to_end))
                    new_intervals.append(
                        Interval(mapping.end + 1, interval.end))
                else:
                    new_intervals.append(interval)
            current_intervals = new_intervals
        current_intervals.extend(new_lvl_intervals)
    return min([interval.start for interval in current_intervals])


def read_input():
    with open('input.txt', 'r') as f:
        return f.read().splitlines()


if __name__ == '__main__':
    input = read_input()
    print(task1(input))
    print(task2(input))
