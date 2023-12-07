def task1(input):
    sum = 0
    for line in input:
        splitted = line.split(':')[1]
        winning, yours = splitted.split('|')

        splitted_winning = winning.split()
        splitted_yours = yours.split()

        counter = -1
        for y in splitted_yours:
            if y in splitted_winning:
                counter += 1
        if counter >= 0:
            sum += 2**counter

    return sum


def task2(input):
    card_counter = [1 for _ in range(len(input))]

    for line_nr, line in enumerate(input):
        splitted = line.split(':')[1]
        winning, yours = splitted.split('|')

        splitted_winning = winning.split()
        splitted_yours = yours.split()

        counter = 0
        for y in splitted_yours:
            if y in splitted_winning:
                counter += 1
        for i in range(counter):
            if line_nr + i >= len(input) - 1:
                return
            card_counter[line_nr + i + 1] += card_counter[line_nr]

    return sum(card_counter)


def read_input():
    with open('test.txt', 'r') as f:
        return f.read().splitlines()


if __name__ == '__main__':
    input = read_input()
    print(task1(input))
    print(task2(input))
