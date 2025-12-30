from agents.hand_strength import classify_hand
import random as rand
from tqdm import tqdm
from itertools import combinations

RANK_ORDER = '23456789TJQKA'
SUIT_ORDER = 'CDHS'

simulation = 200

DECK = set([suit + rank for suit in SUIT_ORDER for rank in RANK_ORDER])

def compare_hands_wrapper(my_hole, opp_hole, community):
    my_full_hand = my_hole + community
    opp_full_hand = opp_hole + community

    my_rank = classify_hand(my_full_hand)
    opp_rank = classify_hand(opp_full_hand)

    if my_rank > opp_rank:
        return 1
    elif my_rank < opp_rank:
        return -1
    else:
        return 0

def sample_opponent_hole(hole_cards, community_cards):
    exclude_cards = set(hole_cards + community_cards)
    sample = rand.sample(DECK - exclude_cards, 7 - len(community_cards))
    
    opponent_hole = sample[:2]
    community_cards = community_cards + sample[2:]

    return opponent_hole, community_cards

def win_rate(hole_card, community_cards, simulations=2000):
    win = 0
    tie = 0

    for _ in range(simulations):
        opponent_hole, extended_community_cards = sample_opponent_hole(hole_card, community_cards)
        result = compare_hands_wrapper(hole_card, opponent_hole, extended_community_cards)
        if result > 0:
            win += 1
        elif result == 0:
            tie += 1
        else:
            pass 
    return (win + 0.5 * tie) / simulations

win_rate_values = []

for pair in tqdm(combinations(DECK, 2)):
    opp_hole_card = list(pair)

    win = 0
    tie = 0

    for i in range(simulation):
        hole = rand.sample(DECK - set(opp_hole_card), 2)
        community_cards = rand.sample(DECK - set(opp_hole_card), 5)
        my_rank = classify_hand(hole + community_cards)
        opp_rank = classify_hand(opp_hole_card + community_cards)
        if my_rank > opp_rank:
            win += 1
        elif my_rank == opp_rank:
            tie += 1
        else:
            pass
    if (win + 0.5 * tie) / simulation > 0.5:
        win_rate_values.append(hole)

print(win_rate_values)