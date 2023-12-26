
ON = True
OFF = False

HIGH = True
LOW = False


QUEUE = []

GLOBAL_COUNTER = 0
PRESS_COUNTER = 0


class Device:
    def __init__(self, id):
        self.state = OFF
        self.id = id
        self.receivers = []

    def add_receivers(self, receivers):
        self.receivers.extend(receivers)
        for receiver in receivers:
            if receiver:
                receiver.add_as_receiver(self)

    def add_as_receiver(self, sender):
        pass

    def process(self, signal, sender):
        pass

    def __repr__(self):
        return f'{self.id}'


class FlipFlop(Device):
    def __init__(self, id):
        self.state = OFF
        self.id = id
        self.flipped = False
        self.receivers = []

    def add_as_receiver(self, sender):
        pass

    def process(self, signal, sender):
        if signal == LOW:
            self.state = not self.state

            for receiver in self.receivers:
                QUEUE.append((self, receiver, self.state))


class Conjunction(Device):
    def __init__(self, id):
        self.state = {}
        self.id = id
        self.receivers = []
        self.counter = 0
        self.prev_counter = 0
        self.prev_send = None

    def add_as_receiver(self, sender):
        self.state[sender.id] = OFF

    def process(self, signal, sender):
        self.counter += 1
        self.state[sender.id] = signal
        if all(self.state.values()):
            if self.id in ['tx', 'vg', 'kp', 'gc'] and self.prev_send == ON:
                print(self.id, 'OFF', PRESS_COUNTER, PRESS_COUNTER - self.prev_counter)
                # print(self.state, self.counter - self.prev_counter)
                self.prev_counter = PRESS_COUNTER
            state = OFF
        else:
            if self.id in ['tx', 'vg', 'kp', 'gc']:
                print(self.id, 'ON', PRESS_COUNTER, PRESS_COUNTER - self.prev_counter)
                # print(self.state, self.counter - self.prev_counter)
                self.prev_counter = PRESS_COUNTER
            state = ON

        self.prev_send = state

        for receiver in self.receivers:
            QUEUE.append((self, receiver, state))


class Final(Device):
    def __init__(self, id):
        self.state = OFF
        self.id = id
        self.receivers = []

    def add_as_receiver(self, sender):
        pass

    def process(self, signal, sender):
        if signal == LOW:
            self.state = ON


DEVICE_TYPES = {
    '%': FlipFlop,
    '&': Conjunction,
}


def process_queue():
    counter = {
        LOW: 0,
        HIGH: 0,
    }
    global GLOBAL_COUNTER
    while QUEUE:
        sender, receiver, signal = QUEUE.pop(0)
        GLOBAL_COUNTER += 1
        counter[signal] += 1
        receiver.process(signal, sender)
    return counter


# def get_states(devices):
#     states = []
#     for device in devices.values():
#         if isinstance(device.state, bool):
#             states.append((device.state))
#         else:
#             states.append(tuple(device.state.values()))
#     return tuple(states)


def get_states(devices):
    states = {}
    for device in devices.values():
        if isinstance(device.state, bool):
            states[device.id] = device.state
        else:
            states[device.id] = dict(device.state)
    return states


def print_differences(states1, states2):
    for id, state in states1.items():
        if isinstance(state, bool):
            if state != states2[id]:
                print(f'{id}: {state} -> {states2[id]}')
        else:
            # print(state, states2[id])
            for id2, state2 in state.items():
                if state2 != states2[id][id2]:
                    print(f'{id} {id2}: {state2} -> {states2[id][id2]}')


def task1(input):
    devices = {}

    broadcaster_receivers = []

    for line in input:
        id, _ = line.split(' -> ')

        if id != 'broadcaster':
            devices_type, id = id[0], id[1:]
            devices[id] = DEVICE_TYPES[devices_type](id)

    for line in input:
        id, receivers = line.split(' -> ')
        receivers = receivers.split(', ')

        if id == 'broadcaster':
            broadcaster_receivers = [devices[rec] for rec in receivers]
        else:
            devices_type, id = id[0], id[1:]
            for receiver in receivers:
                if receiver not in devices:
                    empty_device = Device(receiver)
                    devices[receiver] = empty_device
                devices[id].add_receivers([devices[receiver]])

    counter = {
        LOW: 0,
        HIGH: 0,
    }
    for i in range(1000):
        for receiver in broadcaster_receivers:
            QUEUE.append(('broadcaster', receiver, LOW))

        signals = process_queue()
        counter[LOW] += signals[LOW] + 1
        counter[HIGH] += signals[HIGH]

    return counter[HIGH] * counter[LOW]


def is_parent(dev, visited=None, looking_for='rx'):
    if dev.id == looking_for:
        return True, [dev.id]
    child_parents = []
    is_this_parent = False
    for receiver in dev.receivers:
        if receiver.id in visited:
            continue
        res = is_parent(receiver, visited + [dev.id], looking_for)
        if res[0]:
            is_this_parent = True
            child_parents.extend(res[1])

    if is_this_parent:
        return True, [dev.id] + child_parents
    return False, []


def task2(input):
    devices = {}
    states = set()

    broadcaster_receivers = []

    for line in input:
        id, _ = line.split(' -> ')

        if id != 'broadcaster':
            devices_type, id = id[0], id[1:]
            devices[id] = DEVICE_TYPES[devices_type](id)

    for line in input:
        id, receivers = line.split(' -> ')
        receivers = receivers.split(', ')

        if id == 'broadcaster':
            broadcaster_receivers = [devices[rec] for rec in receivers]
        else:
            devices_type, id = id[0], id[1:]
            for receiver in receivers:
                if receiver not in devices:
                    devices[receiver] = (Final(receiver) if receiver == 'rx'
                                         else Device(receiver))
                devices[id].add_receivers([devices[receiver]])

    # vh -> gc
    # sp -> kp
    # lg -> vg
    # mh -> tx

    mapping = {
        'vh': 'gc',
        'sp': 'kp',
        'lg': 'vg',
        'mh': 'tx',
    }

    starting = 'mh'

    for dev in broadcaster_receivers:
        print(is_parent(dev, visited=[], looking_for=mapping[starting]))
    global PRESS_COUNTER
    prev_state = get_states(devices)
    # prev_state = None
    print(devices[mapping[starting]].state)
    while PRESS_COUNTER < 10_0000:
        PRESS_COUNTER += 1
        # if i % 1_000_000 == 0:
        #     print(f'Iteration {i}')
        #     print_differences(prev_state, get_states(devices))
        #     prev_state = get_states(devices)
        # print(devices[mapping[starting]].state)

        for receiver in broadcaster_receivers:
            # if receiver.id == starting:
            QUEUE.append(('broadcaster', receiver, LOW))
        process_queue()
        # print("After iteration", i)
        # print(f'tx: {devices["tx"].counter}')
        # print(f'vg: {devices["vg"].counter}')
        # print(f'kp: {devices["kp"].counter}')
        # print(f'gc: {devices["gc"].counter}')
        # if not all(devices[mapping[starting]].state.values()):
        #     print(i)
        # print(devices[mapping[starting]].state)
        # print(get_states(devices))

        # state = get_states(devices)
        # if prev_state:
        #     print_differences(prev_state, state)
        # prev_state = state
        # print("===================")
    # print(i)

    return -1


def read_input():
    with open('input.txt', 'r') as f:
        return f.read().splitlines()


if __name__ == '__main__':
    input = read_input()
    # print(task1(input))
    print(task2(input))
