class Move:
    def __init__(self, field, history, sum):
        self.field = field
        self.history = history
        self.sum = sum

    def __eq__(self, __value: object) -> bool:
        return (
            self.field == __value.field
            and self.history[:3] == __value.history[:3]
        )

    def __repr__(self) -> str:
        return f'{self.field} {self.sum} {self.history}'


directions = [
    (-1, 0),
    (0, 1),
    (1, 0),
    (0, -1)
]


def get_how_many_same_dir(move):
    count_x = 1
    count_y = 1
    for i in range(1, len(move.history)):
        if move.history[i][0] == move.field[0]:
            count_x += 1
        else:
            break

    for i in range(1, len(move.history)):
        if move.history[i][1] == move.field[1]:
            count_y += 1
        else:
            break
    return max(count_x, count_y)


def task1(input):
    map = [list(line) for line in input]

    moves_fields = []

    for i in range(len(map)):
        moves_fields.append([])
        for j in range(len(map[0])):
            moves_fields[i].append(12*[9999999])

    moves = [Move((-1, 0), [], -int(map[0][0]))]
    while moves:
        next_move = moves.pop()

        if next_move.field == (len(map) - 1, len(map[0]) - 1):
            return next_move.sum

        for i, direction in enumerate(directions):
            next_field = (
                next_move.field[0] + direction[0],
                next_move.field[1] + direction[1]
            )

            if (
                next_field[0] < 0
                or next_field[0] >= len(map)
                or next_field[1] < 0
                or next_field[1] >= len(map[0])
                or (len(next_move.history) > 0 and next_field == next_move.history[0])
            ):
                continue

            candidate = Move(
                next_field,
                [next_move.field] + next_move.history,
                next_move.sum + int(map[next_field[0]][next_field[1]])
            )

            if get_how_many_same_dir(candidate) > 3:
                continue

            if candidate.sum >= moves_fields[candidate.field[0]][
                    candidate.field[1]][3*i + get_how_many_same_dir(candidate) - 1]:
                continue
            moves_fields[candidate.field[0]][
                candidate.field[1]][3*i + get_how_many_same_dir(candidate) - 1] = candidate.sum

            moves.append(candidate)
        moves = sorted(moves, key=lambda move: move.sum, reverse=True)

    return 0


def task2(input):
    map = [list(line) for line in input]

    moves_fields = []

    for i in range(len(map)):
        moves_fields.append([])
        for j in range(len(map[0])):
            moves_fields[i].append(7*4*[9999999])

    min_found = 9999999

    moves = [Move((0, 0), [], 0)]
    while moves:
        next_move = moves.pop()
        if next_move.sum >= min_found:
            return min_found
        if next_move.field == (len(map) - 1, len(map[0]) - 1):
            return next_move

        for i, direction in enumerate(directions):
            next_field = (
                next_move.field[0] + direction[0],
                next_move.field[1] + direction[1]
            )

            if (
                next_field[0] < 0
                or next_field[0] >= len(map)
                or next_field[1] < 0
                or next_field[1] >= len(map[0])
                or (len(next_move.history) > 0 and next_field == next_move.history[0])
            ):
                continue

            candidate = Move(
                next_field,
                [next_move.field] + next_move.history,
                next_move.sum + int(map[next_field[0]][next_field[1]])
            )
            if candidate.field == (len(map) - 1, len(map[0]) - 1):
                if candidate.sum < min_found:
                    min_found = candidate.sum
                continue
            not_suitable = False
            while get_how_many_same_dir(candidate) < 4:
                next_field = (
                    candidate.field[0] + direction[0],
                    candidate.field[1] + direction[1]
                )

                if (
                    next_field[0] < 0
                    or next_field[0] >= len(map)
                    or next_field[1] < 0
                    or next_field[1] >= len(map[0])
                ):
                    not_suitable = True
                    break

                candidate = Move(
                    next_field,
                    [candidate.field] + candidate.history,
                    candidate.sum + int(map[next_field[0]][next_field[1]])
                )
                if next_move.field == (len(map) - 1, len(map[0]) - 1):
                    if candidate.sum < min_found:
                        min_found = candidate.sum
                    not_suitable = True
            if not_suitable:
                continue

            if get_how_many_same_dir(candidate) > 10:
                continue

            if candidate.sum >= moves_fields[candidate.field[0]][
                    candidate.field[1]][7*i + get_how_many_same_dir(candidate) - 7]:
                continue
            moves_fields[candidate.field[0]][
                candidate.field[1]][7*i + get_how_many_same_dir(candidate) - 7] = candidate.sum

            moves.append(candidate)

        moves = sorted(moves, key=lambda move: move.sum, reverse=True)


def read_input():
    with open('input.txt', 'r') as f:
        return f.read().splitlines()


if __name__ == '__main__':
    input = read_input()
    print(task1(input))
    print(task2(input))
