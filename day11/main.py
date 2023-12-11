def get_values_between(input, start, end, multiplier=1):
    counter = 0

    _start, _end = (start, end) if start <= end else (end, start)

    for value in input:
        if _start < value < _end:
            counter += 1
        if value > _end:
            break
    return counter * multiplier


def task1(input, multiplier=1):
    galaxies_positions = []
    empty_lines = []
    empty_columns = []

    for i in range(len(input)):
        for j in range(len(input[i])):
            if input[i][j] == '#':
                galaxies_positions.append((i, j))

    for i in range(len(input)):
        if input[i].count('#') == 0:
            empty_lines.append(i)
    for i in range(len(input[0])):
        if [input[j][i] for j in range(len(input))].count('#') == 0:
            empty_columns.append(i)

    sum = 0

    for i in range(len(galaxies_positions)):
        for j in range(i + 1, len(galaxies_positions)):
            galaxy_1 = galaxies_positions[i]
            galaxy_2 = galaxies_positions[j]

            value = (
                abs(galaxy_1[0] - galaxy_2[0])
                + get_values_between(
                    empty_lines, galaxy_1[0], galaxy_2[0], multiplier)
                + abs(galaxy_1[1] - galaxy_2[1])
                + get_values_between(
                    empty_columns, galaxy_1[1], galaxy_2[1], multiplier)
            )
            sum += value
    return sum


def task2(input):
    return task1(input, 999_999)


def read_input():
    with open('input.txt', 'r') as f:
        return f.read().splitlines()


if __name__ == '__main__':
    input = read_input()
    print(task1(input))
    print(task2(input))
