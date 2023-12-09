def reduce(list_input, operator):
    if not any(list_input):
        return 0

    tmp = []
    for i in range(1, len(list_input)):
        tmp.append(list_input[i] - list_input[i-1])
    return operator(sum(tmp) + reduce(tmp, operator), list_input)


def task1(input):
    sum_of_values = 0
    for line in input:
        list_line = [int(x) for x in line.split()]
        value = reduce(list_line, lambda x, y: x + y[0])
        sum_of_values += value
    return sum_of_values


def task2(input):
    sum_of_values = 0
    for line in input:
        list_line = [int(x) for x in line.split()]
        value = reduce(list_line, lambda x, y: y[-1] - x)
        sum_of_values += value
    return sum_of_values


def read_input():
    with open('input.txt', 'r') as f:
        return f.read().splitlines()


if __name__ == '__main__':
    input = read_input()
    print(task1(input))
    print(task2(input))
