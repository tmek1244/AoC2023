def find_vertical(mirror, error_num=0):
    for i in range(len(mirror[0])-1):
        error_found = 0
        length = min(len(mirror[0]) - i - 1, i+1)
        # print(length)
        for row in range(len(mirror)):
            for j in range(length):
                if mirror[row][i-j] != mirror[row][i+j+1]:
                    error_found += 1
                    if error_found > error_num:
                        break
            else:
                continue
            break
            # if mirror[row][i-length+1:i+1] != mirror[row][i+1:i+length+1][::-1]:
            #     break
        else:
            if error_found == error_num:
                return i+1
    return 0


def find_horizontal(mirror, error_num=0):
    for i in range(len(mirror)-1):
        error_found = 0
        length = min(len(mirror) - i - 1, i+1)
        for j in range(length):
            for col in range(len(mirror[0])):
                if mirror[i-j][col] != mirror[i+j+1][col]:
                    error_found += 1
                    if error_found > error_num:
                        break
            else:
                continue
            break
            # if mirror[i-j] != mirror[i+j+1]:
            #     break
        else:
            if error_found == error_num:
                return i+1
    return 0


def task1(input):
    mirrors = []
    mirror = []
    for i in range(len(input)):
        if input[i] == '':
            mirrors.append(mirror)
            mirror = []
        else:
            mirror.append(input[i])
    mirrors.append(mirror)
    sum = 0
    for mirror in mirrors:
        sum += find_vertical(mirror) + 100*find_horizontal(mirror)
    return sum


def task2(input):
    mirrors = []
    mirror = []
    for i in range(len(input)):
        if input[i] == '':
            mirrors.append(mirror)
            mirror = []
        else:
            mirror.append(input[i])
    mirrors.append(mirror)
    sum = 0
    for mirror in mirrors:
        sum += find_vertical(mirror, 1) + 100*find_horizontal(mirror, 1)
    return sum


def read_input():
    with open('input.txt', 'r') as f:
        return f.read().splitlines()


if __name__ == '__main__':
    input = read_input()
    print(task1(input))
    print(task2(input))
