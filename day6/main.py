import math


def task1(input):
    r = lambda x: map(int, x.split(':')[1].split().
    times = input[0].split(':')[1].split()
    distances = input[1].split(':')[1].split()
    result = 1
    for time, distance in zip(times, distances):
        lower_bound = math.ceil(-math.sqrt(1/4*int(time)**2 - int(distance)) + int(time)/2 + 0.0000001)
        upper_bound = math.floor(math.sqrt(1/4*int(time)**2 - int(distance)) + int(time)/2 - 0.0000001)

        result *= (upper_bound - lower_bound + 1)

    return result


def task2(input):
    time = ''.join(input[0].split(':')[1].split())
    distance = ''.join(input[1].split(':')[1].split())
    result = 1
    lower_bound = math.ceil(-math.sqrt(1/4*int(time)**2 - int(distance)) + int(time)/2 + 0.0000001)
    upper_bound = math.floor(math.sqrt(1/4*int(time)**2 - int(distance)) + int(time)/2 - 0.0000001)

    result *= (upper_bound - lower_bound + 1)

    return result


def read_input():
    with open('input.txt', 'r') as f:
        return f.read().splitlines()


if __name__ == '__main__':
    input = read_input()
    print(task1(input))
    print(task2(input))
