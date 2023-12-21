
ON = True
OFF = False

HIGH = True
LOW = False


QUEUE = []


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

    def add_as_receiver(self, sender):
        self.state[sender.id] = OFF

    def process(self, signal, sender):
        self.state[sender.id] = signal
        if all(self.state.values()):
            state = OFF
        else:
            state = ON

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
    while QUEUE:
        sender, receiver, signal = QUEUE.pop(0)
        counter[signal] += 1
        receiver.process(signal, sender)
    return counter


def get_states(devices):
    states = []
    for device in devices.values():
        if isinstance(device.state, bool):
            states.append((device.state))
        else:
            states.append(tuple(device.state.values()))
    return tuple(states)


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
    i = 0
    while True:
        i += 1
        if i % 1_000_000 == 0:
            print(f'Iteration {i}')
        for receiver in broadcaster_receivers:
            QUEUE.append(('broadcaster', receiver, LOW))

        process_queue()
        # if get_states(devices) in states:
        #     print('ALREADY SEEN')
        #     return i
        # else:
        #     states.add(get_states(devices))
        if devices['rx'].state == ON:
            return i

    return -1


def read_input():
    with open('input.txt', 'r') as f:
        return f.read().splitlines()


if __name__ == '__main__':
    input = read_input()
    print(task1(input))
    print(task2(input))
