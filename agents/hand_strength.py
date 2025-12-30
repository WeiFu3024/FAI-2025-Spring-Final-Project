from itertools import combinations
from collections import Counter
import random as rand
import time

RANK_ORDER = '23456789TJQKA'
SUIT_ORDER = 'CDHS'
DECK = set([suit + rank for suit in SUIT_ORDER for rank in RANK_ORDER])

def card_value(card):
    """Returns numeric value of a card's rank and its suit."""
    suit, rank = card[0], card[1]
    return RANK_ORDER.index(rank), suit

def is_straight(ranks):
    """Checks if the hand is a straight."""
    ranks = sorted(set(ranks))
    if len(ranks) < 5:
        return False
    for i in range(len(ranks) - 4):
        if ranks[i+4] - ranks[i] == 4:
            return ranks[i+4]
    if ranks[-4:] == [0, 1, 2, 3] and 12 in ranks:  # A-2-3-4-5
        return 3
    return False

def classify_hand(cards):
    """Evaluates the best 5-card hand from 7 cards."""
    best = (0, [])
    for combo in combinations(cards, 5):
        ranks = [card_value(c)[0] for c in combo]
        suits = [card_value(c)[1] for c in combo]

        rank_counts = Counter(ranks)
        suit_counts = Counter(suits)
        is_flush = any(v >= 5 for v in suit_counts.values())
        straight_high = is_straight(ranks)

        score = ()
        if is_flush and straight_high is not False:
            score = (8, straight_high)
        elif 4 in rank_counts.values():
            quad_rank = [r for r, c in rank_counts.items() if c == 4][0]
            kicker = max([r for r in ranks if r != quad_rank])
            score = (7, quad_rank, kicker)
        elif 3 in rank_counts.values() and 2 in rank_counts.values():
            triple = [r for r, c in rank_counts.items() if c == 3][0]
            pair = [r for r, c in rank_counts.items() if c == 2][0]
            score = (6, triple, pair)
        elif is_flush:
            flush_ranks = sorted([r for r, s in zip(ranks, suits) if suit_counts[s] >= 5], reverse=True)
            score = (5, flush_ranks)
        elif straight_high is not False:
            score = (4, straight_high)
        elif 3 in rank_counts.values():
            triple = [r for r, c in rank_counts.items() if c == 3][0]
            kickers = sorted([r for r in ranks if r != triple], reverse=True)[:2]
            score = (3, triple, kickers)
        elif list(rank_counts.values()).count(2) >= 2:
            pairs = sorted([r for r, c in rank_counts.items() if c == 2], reverse=True)
            kicker = max([r for r in ranks if r not in pairs])
            score = (2, pairs[0], pairs[1], kicker)
        elif 2 in rank_counts.values():
            pair = [r for r, c in rank_counts.items() if c == 2][0]
            kickers = sorted([r for r in ranks if r != pair], reverse=True)[:3]
            score = (1, pair, kickers)
        else:
            score = (0, sorted(ranks, reverse=True))

        best = max(best, score)
    return best

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
    time_start = time.time()

    for i in range(simulations):
        opponent_hole, extended_community_cards = sample_opponent_hole(hole_card, community_cards)
        result = compare_hands_wrapper(hole_card, opponent_hole, extended_community_cards)
        if result > 0:
            win += 1
        elif result == 0:
            tie += 1
        else:
            pass 
        if time.time() - time_start >= 4:
            print(f"Simulation stopped at {i} due to time limit.")
            return (win + 0.5 * tie) / (i + 1)
    return (win + 0.5 * tie) / simulations
