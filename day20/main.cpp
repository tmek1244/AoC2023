#include <iostream>
#include <vector>
#include <map>
#include <queue>
#include <functional>
#include <tuple>
#include <fstream>
#include <sstream>
#include <set>

#define ON true
#define OFF false
#define HIGH true
#define LOW false

class Device {
public:
    bool state = OFF;
    std::string id;
    std::vector<Device*> receivers;

    Device(std::string id) : id(id) {}

    void add_receiver(Device* new_receiver) {
        receivers.push_back(new_receiver);
        new_receiver->add_as_receiver(this);
    }

    virtual void add_as_receiver(Device* sender) {}

    virtual void process(bool signal, Device* sender) {}

    std::string repr() {
        return id;
    }
};

struct QueueElement {
public:
    Device* sender;
    Device* receiver;
    bool signal;

    QueueElement(Device* sender, Device* receiver, bool signal) : sender(sender), receiver(receiver), signal(signal) {}
};

std::queue<QueueElement> QUEUE;


class FlipFlop : public Device {
public:
    bool flipped = false;

    FlipFlop(std::string id) : Device(id) {}

    void add_as_receiver(Device* sender) override {}

    void process(bool signal, Device* sender) override {
        if (signal == LOW) {
            state = !state;
            for (Device* receiver : receivers) {
                QUEUE.push(QueueElement(this, receiver, state));
            }
        }
    }
};

class Conjunction : public Device {
public:
    std::map<std::string, bool> state;

    Conjunction(std::string id) : Device(id) {}

    void add_as_receiver(Device* sender) override {
        state[sender->id] = OFF;
    }

    void process(bool signal, Device* sender) override {
        state[sender->id] = signal;
        bool state = OFF;
        for (auto const& x : this->state) {
            if (!x.second) {
                state = ON;
                break;
            }
        }
        for (Device* receiver : receivers) {
            QUEUE.push(QueueElement(this, receiver, state));
        }
    }
};

class Final : public Device {
public:
    Final(std::string id) : Device(id) {}

    void process(bool signal, Device* sender) override {
        if (signal == LOW) {
            this->state = ON;
        }
    }
};

std::map<char, std::function<Device*(std::string)>> DEVICE_TYPES = {
    {'%', [](std::string id) { return new FlipFlop(id); }},
    {'&', [](std::string id) { return new Conjunction(id); }},
};

std::map<bool, int> process_queue() {
    std::map<bool, int> counter = {
        {LOW, 0},
        {HIGH, 0},
    };
    while (!QUEUE.empty()) {
        auto [sender, receiver, signal] = QUEUE.front();
        // std::cout << " -> " << receiver->repr() << " " << signal << std::endl;
        QUEUE.pop();
        counter[signal] += 1;
        receiver->process(signal, sender);
    }
    return counter;
}

int task2(std::vector<std::string> input) {
    std::map<std::string, Device*> devices;

    std::vector<Device*> broadcaster_receivers;

    for (std::string line : input) {
        std::istringstream iss(line);
        std::string id, arrow, receivers;
        iss >> id >> arrow;

        if (id != "broadcaster") {
            char device_type = id[0];
            id = id.substr(1);
            devices[id] = DEVICE_TYPES[device_type](id);
        }
    }

    for (std::string line : input) {
        std::istringstream iss(line);
        std::string id, arrow, receiver;
        iss >> id >> arrow;

        std::vector<std::string> receiver_ids;

        while (std::getline(iss, receiver, ',')) {
            size_t first = receiver.find_first_not_of(' ');
            size_t last = receiver.find_last_not_of(' ');
            receiver = receiver.substr(first, (last - first + 1));

            receiver_ids.push_back(receiver);
        }
        if (id == "broadcaster") {
            for (std::string receiver : receiver_ids) {
                broadcaster_receivers.push_back(devices[receiver]);
            }
        } else {
            char device_type = id[0];
            id = id.substr(1);
            for (std::string receiver : receiver_ids) {
                if (devices.find(receiver) == devices.end()) {
                    devices[receiver] = (receiver == "rx" ? new Final(receiver) : new Device(receiver));
                }
                devices[id]->add_receiver(devices[receiver]);
            }
        }
    }

    int i = 0;
    long long counter_low = 0;
    long long counter_high = 0;

    while (true) {
        i += 1;
        if (i % 1000000 == 0) {
            std::cout << "Iteration " << i << std::endl;
        }
        for (Device* receiver : broadcaster_receivers) {
            QUEUE.push(QueueElement(nullptr, receiver, LOW));
        }

        std::map<bool, int> signals = process_queue();
        // counter_low += signals[LOW] + 1;
        // counter_high += signals[HIGH];

        if (devices["rx"]->state == ON) {
            return i;
        }
        // if (i == 1000){
        //     return counter_high * counter_low;
        // }
    }

    return -1;
}

std::vector<std::string> read_input() {
    std::vector<std::string> lines;
    std::ifstream file("input.txt");
    for (std::string line; std::getline(file, line); ) {
        lines.push_back(line);
    }
    return lines;
}

int main() {
    std::vector<std::string> input = read_input();
    std::cout << task2(input) << std::endl;
    return 0;
}
