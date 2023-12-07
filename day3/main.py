def task1(input):
    def check_for_symbols(nr_begin, nr_end, line_nr):
        # print(list(range(max(nr_begin - 1, 0), min(nr_end + 1, len(input[0])))))
        for i in range(max(nr_begin - 1, 0), min(nr_end + 1, len(input[0]))):
            if line_nr != 0 and input[line_nr - 1][i] != '.':
                return True
            if line_nr != len(input) - 1 and input[line_nr + 1][i] != '.':
                return True
        # print(nr_begin, nr_end, line_nr)
        if nr_begin != 0 and input[line_nr][nr_begin - 1] != '.':
            return True
        if nr_end < len(input[0]) - 1 and input[line_nr][nr_end] != '.':
            return True
        return False

    sum = 0
    for line_nr, line in enumerate(input):
        current_number = ""
        for char_nr, char in enumerate(line):
            if char.isdigit():
                current_number += char
            elif current_number != "":
                if check_for_symbols(
                        char_nr - len(current_number), char_nr, line_nr):
                    sum += int(current_number)
                # else:
                    # print(current_number)
                current_number = ""
        if current_number != "":
            if check_for_symbols(
                    len(line) - len(current_number), len(line), line_nr):
                sum += int(current_number)
    return sum


def task2(input):
    number_list = []
    sum = 0
    map = [[0 for i in range(len(input[0]))] for j in range(len(input))]
    for line_nr, line in enumerate(input):
        current_number = ""
        for char_nr, char in enumerate(line):
            map[line_nr][char_nr] = char
            if char.isdigit():
                current_number += char
            elif current_number != "":
                number_list.append(int(current_number))
                for i in range(char_nr - len(current_number), char_nr):
                    map[line_nr][i] = len(number_list) - 1
                current_number = ""
        if current_number != "":
            number_list.append(int(current_number))
            for i in range(len(line) - len(current_number), len(line)):
                map[line_nr][i] = len(number_list) - 1

    def check_for_number(x, y):
        if isinstance(map[x][y], int):
            numbers_around.add(map[x][y])
        return None

    for line_nr, line in enumerate(map):
        for char_nr, char in enumerate(line):
            if char == '*':
                numbers_around = set()

                if line_nr > 0:
                    if char_nr > 0:
                        check_for_number(line_nr - 1, char_nr - 1)
                    check_for_number(line_nr - 1, char_nr)
                    if char_nr < len(input[0]) - 1:
                        check_for_number(line_nr - 1, char_nr + 1)
                if char_nr > 0:
                    check_for_number(line_nr, char_nr - 1)
                if char_nr < len(input[0]) - 1:
                    check_for_number(line_nr, char_nr + 1)
                if line_nr < len(input) - 1:
                    if char_nr > 0:
                        check_for_number(line_nr + 1, char_nr - 1)
                    check_for_number(line_nr + 1, char_nr)
                    if char_nr < len(input[0]) - 1:
                        check_for_number(line_nr + 1, char_nr + 1)

                if len(numbers_around) == 2:
                    sum += number_list[numbers_around.pop()] * number_list[numbers_around.pop()]

    return sum


def read_input():
    with open('input.txt', 'r') as f:
        return f.read().splitlines()


if __name__ == '__main__':
    input = read_input()
    # print(task1(input))
    print(task2(input))
