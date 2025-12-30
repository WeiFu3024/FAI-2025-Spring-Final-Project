from game.players import BasePokerPlayer
import random

class BaselineAgent(BasePokerPlayer):
    def __init__(self):
        super().__init__()
        self.my_uuid = None
        self.hole_cards = []
        self.small_blind_amount = 0

    def _get_card_rank(self, card_str):
        rank_char = card_str[1:]
        if rank_char.isdigit():
            return int(rank_char)
        return {'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}[rank_char]

    def receive_game_start_message(self, game_info):
        self.my_uuid = self.uuid
        self.small_blind_amount = game_info['rule']['small_blind_amount']

    def receive_round_start_message(self, round_count, hole_card, seats):
        self.hole_cards = hole_card # Store current hole cards

    def _simple_evaluate_hand_strength(self, hole_cards, community_cards):
        """
        Evaluates hand strength based on hole cards and community cards.
        Returns a score:
        0: High Card
        1: One Pair
        2: Two Pair
        3: Three of a Kind
        6: Full House
        7: Four of a Kind
        (Simplified: does not detect straights or flushes)
        """
        all_cards = hole_cards + community_cards
        if not all_cards:
            return 0

        ranks = [self._get_card_rank(card) for card in all_cards]
        rank_counts = {rank: 0 for rank in range(2, 15)}  # Ranks 2 through Ace
        for r_val in ranks:
            rank_counts[r_val] += 1

        has_four_of_a_kind = any(count == 4 for count in rank_counts.values())
        trips_ranks = [rank for rank, count in rank_counts.items() if count == 3]
        pairs_ranks = [rank for rank, count in rank_counts.items() if count == 2]

        if has_four_of_a_kind:
            return 7  # Four of a Kind

        # Full House: one trip and one pair, or two trips (best trip + second trip as pair)
        if (len(trips_ranks) >= 1 and len(pairs_ranks) >= 1) or len(trips_ranks) >= 2:
            return 6  # Full House

        if len(trips_ranks) >= 1:
            return 3  # Three of a Kind

        if len(pairs_ranks) >= 2:
            return 2  # Two Pair

        if len(pairs_ranks) == 1:
            return 1  # One Pair

        return 0  # High Card

    def declare_action(self, valid_actions, hole_card, round_state):
        # hole_card is passed directly, self.hole_cards is also available
        street = round_state['street']
        community_cards = round_state['community_card']
        pot_size = round_state['pot']['main']['amount']

        call_action_info = valid_actions[1]
        amount_to_call = call_action_info['amount']

        fold_action_tuple = valid_actions[0]['action'], valid_actions[0]['amount']
        call_action_tuple = call_action_info['action'], amount_to_call

        can_raise = valid_actions[2]['amount']['min'] != -1
        min_raise_total = valid_actions[2]['amount']['min'] if can_raise else float('inf')
        max_raise_total = valid_actions[2]['amount']['max'] if can_raise else 0

        # Pre-flop strategy
        if street == "preflop":
            rank1 = self._get_card_rank(hole_card[0])
            rank2 = self._get_card_rank(hole_card[1])
            is_pair = (rank1 == rank2)
            # Both cards are Ten or higher (e.g., TT+, AK, AQ, AJ, KQ, KJ, QJ)
            is_high_cards_connector_or_pair = (rank1 >= 10 and rank2 >= 10)

            is_strong_preflop = is_pair or is_high_cards_connector_or_pair

            if is_strong_preflop:
                if can_raise:
                    big_blind = self.small_blind_amount * 2
                    target_raise_total = 3 * big_blind
                    
                    # Ensure raise is within valid bounds
                    actual_raise_amount = max(min_raise_total, target_raise_total)
                    actual_raise_amount = min(actual_raise_amount, max_raise_total)

                    if actual_raise_amount >= min_raise_total : # Check if the clamped amount is still a valid raise
                        return "raise", actual_raise_amount
                    else: # Cannot make desired raise, or min_raise is too high
                        return call_action_tuple
                else: # Cannot raise
                    return call_action_tuple
            else: # Not a strong preflop hand
                if amount_to_call == 0:  # Can check
                    return call_action_tuple # ("call", 0) which is a check
                else: # Must pay to see flop, and hand is weak
                    return fold_action_tuple

        # Post-flop strategy (flop, turn, river)
        else:
            hand_strength_score = self._simple_evaluate_hand_strength(hole_card, community_cards)
            
            # Default to checking or folding if hand is weak
            action_to_take = fold_action_tuple
            if amount_to_call == 0:
                action_to_take = call_action_tuple # Check

            if hand_strength_score >= 3:  # Trips, Full House, Quads
                if can_raise:
                    # Try to raise by pot size (total bet = call_amount + pot_size)
                    # This is a common way to express "pot-sized raise" in terms of total bet amount
                    target_raise_total = amount_to_call + pot_size 
                    actual_raise_amount = max(min_raise_total, target_raise_total)
                    actual_raise_amount = min(actual_raise_amount, max_raise_total)
                    if actual_raise_amount >= min_raise_total:
                        return "raise", actual_raise_amount
                return call_action_tuple # If cannot raise or raise not chosen, call

            elif hand_strength_score == 2:  # Two Pair
                if can_raise:
                    # Try to raise by 1/2 pot size
                    target_raise_total = amount_to_call + int(pot_size * 0.5)
                    actual_raise_amount = max(min_raise_total, target_raise_total)
                    actual_raise_amount = min(actual_raise_amount, max_raise_total)
                    if actual_raise_amount >= min_raise_total:
                        return "raise", actual_raise_amount
                return call_action_tuple

            elif hand_strength_score == 1:  # One Pair
                if amount_to_call == 0 and can_raise:  # Checked to us, try a small bet
                    target_raise_total = amount_to_call + int(pot_size * 0.33)
                    actual_raise_amount = max(min_raise_total, target_raise_total)
                    actual_raise_amount = min(actual_raise_amount, max_raise_total)
                    if actual_raise_amount >= min_raise_total:
                        return "raise", actual_raise_amount
                    return call_action_tuple # Cannot make small bet, just check
                else: # Facing a bet, or cannot raise
                    return call_action_tuple # Call
            
            # High Card (score 0) or unhandled cases
            if amount_to_call == 0:
                return call_action_tuple # Check
            else:
                return fold_action_tuple # Fold if must pay and hand is weak

    # Other receive methods can be left as pass for this baseline agent
    def receive_street_start_message(self, street, round_state):
        pass

    def receive_game_update_message(self, new_action, round_state):
        pass

    def receive_round_result_message(self, winners, hand_info, round_state):
        pass

def setup_ai():
    return BaselineAgent()