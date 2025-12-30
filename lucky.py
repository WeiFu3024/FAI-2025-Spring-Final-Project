import random as rand
import numpy as np
from tqdm import tqdm
from agents.hand_strength import classify_hand

RANK_ORDER = '23456789TJQKA'
SUIT_ORDER = 'CDHS'
DECK = set([suit + rank for suit in SUIT_ORDER for rank in RANK_ORDER])

samples = 20
simulation = 1000

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

win_over_threshold = np.zeros(4)  # Preflop, Flop, Turn, River
threshold = [0.55, 0.6, 0.65, 0.7]

for _ in tqdm(range(samples)):
    hole_card = rand.sample(DECK, 2)
    true_community_cards = rand.sample(DECK - set(hole_card), 5)
    
    for street_idx in range(4):  # 0: preflop, 1: flop, 2: turn, 3: river
        community_cards = true_community_cards[:street_idx + 2] if street_idx > 0 else []
        win_rate_value = win_rate(hole_card, community_cards, simulations=simulation)
        if win_rate_value > threshold[street_idx]:
            win_over_threshold[street_idx] += 1
        else:
            break

print("Win rates over thresholds:", win_over_threshold / samples)