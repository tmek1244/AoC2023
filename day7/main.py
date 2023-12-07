from collections import Counter


CARDS = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
CARDS2 = ['A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2', 'J']


def get_hand_rank(hand):
    hand_counter = sorted(Counter(hand).values(), reverse=True)
    # print(hand_counter)
    if hand_counter == [5]:
        return 6
    if hand_counter == [4, 1]:
        return 5
    if hand_counter == [3, 2]:
        return 4
    if hand_counter == [3, 1, 1]:
        return 3
    if hand_counter == [2, 2, 1]:
        return 2
    if hand_counter == [2, 1, 1, 1]:
        return 1
    if hand_counter == [1, 1, 1, 1, 1]:
        return 0
    return -1


def gt_hands(hand1, hand2):
    for i in range(len(hand1)):
        if CARDS.index(hand1[i]) == CARDS.index(hand2[i]):
            continue
        return CARDS.index(hand1[i]) < CARDS.index(hand2[i])
    return False


class Hand:
    def __init__(self, hand, bid) -> None:
        self.hand = hand
        self.bid = int(bid)

    def __gt__(self, other):
        if get_hand_rank(self.hand) == get_hand_rank(other.hand):
            return gt_hands(self.hand, other.hand)
        return get_hand_rank(self.hand) > get_hand_rank(other.hand)

    def __eq__(self, other) -> bool:
        return (
            get_hand_rank(self.hand) == get_hand_rank(other.hand) 
            and not gt_hands(other.hand, self.hand) 
            and not gt_hands(self.hand, other.hand)
        )


def task1(input):
    hands = []
    for line in input:
        hands.append(Hand(*line.split()))
        
    sum = 0
    for i, hand in enumerate(sorted(hands)):
        # print(hand.hand, hand.bid)
        sum += hand.bid * (i + 1)
    return sum


def get_hand_rank2(hand):
    hand_counter = Counter(hand)
    if 'J' in hand_counter:
        J_counter = hand_counter.pop('J')
    else:
        J_counter = 0
    # print(hand_counter)
    hand_counter = list(sorted(hand_counter.values(), reverse=True))
    if len(hand_counter) == 0:
        hand_counter = [5]
    else:
        hand_counter[0] += J_counter
    # print(J_counter, hand_counter)
    if hand_counter == [5]:
        return 6
    if hand_counter == [4, 1]:
        return 5
    if hand_counter == [3, 2]:
        return 4
    if hand_counter == [3, 1, 1]:
        return 3
    if hand_counter == [2, 2, 1]:
        return 2
    if hand_counter == [2, 1, 1, 1]:
        return 1
    if hand_counter == [1, 1, 1, 1, 1]:
        return 0
    return -1


def task2(input):
    global get_hand_rank, CARDS
    get_hand_rank = get_hand_rank2
    CARDS = CARDS2
    hands = []
    for line in input:
        hands.append(Hand(*line.split()))
        
    sum = 0
    for i, hand in enumerate(sorted(hands)):
        # print(hand.hand, hand.bid)
        sum += hand.bid * (i + 1)
    return sum


def read_input():
    with open('input.txt', 'r') as f:
        return f.read().splitlines()


if __name__ == '__main__':
    input = read_input()
    print(task1(input))
    print(task2(input))
