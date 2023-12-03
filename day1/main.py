def task1(i):
    a = lambda y: list(filter(lambda x: x.isdigit(), y))
    return sum([int(a(l)[0]+a(l)[-1]) for l in i])


def task2(i):
    import re
    d = ["one", "two", "three", "four",
         "five", "six", "seven", "eight", "nine"]

    def g(l):
        r = re.findall(fr'(?=(\d|{"|".join(d)}))', l)
        f = lambda x: str(d.index(x) + 1) if x in d else x
        return int(f(r[0]) + f(r[-1]))

    return sum([g(l) for l in i])


def read_input():
    with open('input.txt', 'r') as f:
        return f.read().splitlines()


if __name__ == '__main__':
    input = read_input()
    print(task1(input))
    print(task2(input))
