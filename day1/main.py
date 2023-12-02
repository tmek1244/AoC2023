def task1(input):
    result = 0
    for line in input:
        a = list(filter(lambda x: ord(x) > 48 and ord(x) < 58, line))
        result += int(a[0] + a[-1])
    print(result)


def task2(input):
    for line in input:



def read_input():
    with open('input.txt', 'r') as f:
        return f.read().splitlines()


if __name__ == '__main__':
    input = read_input()
    task1(input)
    task2(input)
