workflows = {}


class Workflow:
    def __init__(self, workflow, id=None) -> None:
        self.workflows_steps = workflow.split(',')
        self.id = id

    def __call__(self, x, m, a, s):
        variables = {
            'x': x,
            'm': m,
            'a': a,
            's': s
        }
        for step in self.workflows_steps:
            if ':' in step:
                condition, result = step.split(':')

                if '>' in condition:
                    variable, value = condition.split('>')
                    if variables[variable][1] > int(value):
                        modified = dict(variables)
                        modified[variable] = (int(value) + 1, modified[variable][1])
                        workflows[result](**modified)
                    variables[variable] = (variables[variable][0],
                                           min(int(value), variables[variable][1]))
                elif '<' in condition:
                    variable, value = condition.split('<')
                    if variables[variable][0] < int(value):
                        modified = dict(variables)
                        modified[variable] = (modified[variable][0], int(value) - 1)
                        workflows[result](**modified)
                    variables[variable] = (max(int(value), variables[variable][0]),
                                           variables[variable][1])
                else:
                    raise Exception(f'Invalid condition {step}')
            else:
                workflows[step](**variables)


def preprocess():
    workflows['in']((1, 4000), (1, 4000), (1, 4000), (1, 4000))


def combinations(x, m, a, s):
    return (x[1] - x[0] + 1) * (m[1] - m[0] + 1) * (a[1] - a[0] + 1) * (s[1] - s[0] + 1)


class Workflow1:
    def __init__(self, workflow) -> None:
        self.workflows_steps = workflow.split(',')

    def __call__(self, x, m, a, s):
        for step in self.workflows_steps:
            if ':' in step:
                condition, result = step.split(':')
                if eval(condition):
                    return result
            else:
                return step


def calculate(x, m, a, s):
    return x + m + a + s


def task1(input):
    workflows = {}

    i = 0

    while True:
        line = input[i]
        i += 1
        if line == '':
            break
        id, workflow = line.split('{')
        workflows[id] = Workflow1(workflow[:-1])

    total = 0
    while i < len(input):
        line = input[i]
        instruction = lambda x: f'workflows["{x}"]({line[1:-1]})'
        wf = 'in'
        while (wf := eval(instruction(wf))) not in ['A', 'R']:
            pass
        if wf == 'A':
            total += eval((f'calculate({line[1:-1]})'))
        i += 1

    return total


def task2(input):
    i = 0
    while True:
        line = input[i]
        i += 1
        if line == '':
            break
        id, workflow = line.split('{')
        workflows[id] = Workflow(workflow[:-1], id)

    total = 0

    def add(x, m, a, s):
        nonlocal total
        total += combinations(x, m, a, s)
    workflows['A'] = add
    workflows['R'] = lambda x, m, a, s: None
    preprocess()

    return total


def read_input():
    with open('input.txt', 'r') as f:
        return f.read().splitlines()


if __name__ == '__main__':
    input = read_input()
    print(task1(input))
    print(task2(input))
