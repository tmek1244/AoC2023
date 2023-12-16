def hash(element):
    value = 0

    for char in element:
        value += ord(char)
        value *= 17
        value %= 256
    return value


def task1(input):
    sum = 0
    for element in input[0].split(','):
        sum += hash(element)
    return sum


def task2(input):
    hashmap = {}
    for i in range(256):
        hashmap[i] = []

    for element in input[0].split(','):
        if '-' in element:
            key = element.split('-')[0]
            position = hash(key)
            for elem in hashmap[position]:
                if elem[0] == key:
                    hashmap[position].remove(elem)
                    break
        else:
            key, value = element.split('=')
            position = hash(key)
            for i, elem in enumerate(hashmap[position]):
                if elem[0] == key:
                    hashmap[position][i] = [key, int(value)]
                    break
            else:
                hashmap[position].append([key, int(value)])

    sum = 0
    for box_nr, key in enumerate(hashmap):
        if hashmap[key]:
            for elem_nr, elem in enumerate(hashmap[key]):
                sum += (box_nr + 1) * (elem_nr + 1) * elem[1]
    return sum


def read_input():
    with open('input.txt', 'r') as f:
        return f.read().splitlines()


if __name__ == '__main__':
    input = read_input()
    print(task1(input))
    print(task2(input))
