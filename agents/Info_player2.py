from game.players import BasePokerPlayer
import random as rand
import numpy as np
import json
from agents.hand_strength import win_rate as win_rate_approx

INFO_REMAIN = [0.24766699999999994, 0.16949899999999998, 0.12006300000000003, 0]

CONFIDENCE_025 =  [0.11617833818181818, 0.04813771599999999, 0.02284125365853659, 0]
CONFIDENCE_040 = [0.18830554444444442, 0.09989621914893616, 0.0475912373493976, 0]
CONFIDENCE_060 = [0.25987088115942025, 0.1495895936507936, 0.08726530243902442, 0]

RANK_ORDER = '23456789TJQKA'
SUIT_ORDER = 'CDHS'
DECK = set([suit + rank for suit in SUIT_ORDER for rank in RANK_ORDER])


class INFO2Player(BasePokerPlayer):
    def __init__(self):
        pass
    
    def Kelly_criterion(self, p, stack, pot):
        return p / (1 + (1 - p) * stack / pot) * stack
    
    def already_win(self, stack, round_remains):
        sb = self.game_info['rule']['small_blind_amount']
        bb = 2 * sb
        potential_future_risk = round_remains * (sb + bb) / 2 + bb
        return stack - self.game_info['rule']['initial_stack'] > potential_future_risk

    def declare_action(self, valid_actions, hole_card, round_state):
        self.id = round_state['next_player']
        print("id: ", self.id)
        community_cards = round_state['community_card']
        stack = round_state['seats'][self.id]['stack']
        pot = round_state['pot']['main']['amount']
        sb = self.game_info['rule']['small_blind_amount']
        self.street_idx = {'preflop': 1, 'flop': 2, 'turn': 3, 'river': 4}.get(round_state['street'], -1)

        fold_action_info = valid_actions[0]
        call_action_info = valid_actions[1]
        raise_action_info = valid_actions[2]

        round_remains = self.game_info['rule']['max_round'] - round_state['round_count']
        if self.already_win(stack, round_remains):
            print("Already win, no need to play")
            return fold_action_info['action'], fold_action_info['amount']

        win_rate = win_rate_approx(hole_card, community_cards, simulations=500)
        print("win_rate", win_rate)

        uncertainty = CONFIDENCE_040[self.street_idx - 1]
        # uncertainty2 = CONFIDENCE_040[self.street_idx - 1]
        # uncertainty3 = CONFIDENCE_060[self.street_idx - 1]
        safe_rate = win_rate - uncertainty
        safe_margin = win_rate - uncertainty - 0.5

        exp_fold = stack
        # exp_pass = stack + pot * safe_rate - (1 - safe_rate) * (call_action_info['amount'] - self.previous_bid)
        exp_pass = stack + pot * safe_rate - (1 - safe_rate) * (call_action_info['amount'] - self.previous_bid)
        raise_amount = max(safe_margin * (raise_action_info['amount']['max']) * (1 -uncertainty), raise_action_info['amount']['min'])

        exp_raise = stack - (raise_amount - self.previous_bid) * (1 - win_rate + uncertainty) + (win_rate - uncertainty) * (pot + (raise_amount - self.previous_bid))

        if self.already_raised:     # If already raised, don't raise again
            exp_raise = -1
            raise_amount = -1
        
        if raise_amount == int(raise_action_info['amount']['max']):     # Handle all in raise
            exp_raise = int(stack - (raise_amount - self.previous_bid) * (1 - safe_rate) + (safe_rate) * pot)     # Heuristic
        
        print(f"exp_fold: {exp_fold}, exp_pass: {exp_pass}, exp_raise: {exp_raise}, raise_amount: {raise_amount}")

        if exp_fold >= exp_pass and exp_fold >= exp_raise:
            return fold_action_info['action'], fold_action_info['amount']
        if exp_pass >= exp_fold and exp_pass >= exp_raise:
            self.previous_bid = call_action_info['amount']
            return call_action_info['action'], call_action_info['amount']
        if exp_raise >= exp_fold and exp_raise >= exp_pass:
            self.already_raised = True
            self.previous_bid = raise_amount
            return raise_action_info['action'], raise_amount

    def receive_game_start_message(self, game_info):
        self.game_info = game_info  # player_num, rule, max_round, initial_stack, small_blind_amount, ante, blind_structure
        # print("game info:", game_info)
        # self.opp_timid = False  # Track if opponent is timid
        pass

    def receive_round_start_message(self, round_count, hole_card, seats):
        self.opp_raise = 0  # Track opponent's maximum raise in a round
        pass

    def receive_street_start_message(self, street, round_state):
        self.previous_bid = 0  # Reset previous bid at the start of each street
        self.already_raised = False  # Track if the player has already raised in the current round
        pass

    def receive_game_update_message(self, new_action, round_state):
        # print("new_action", new_action)
        pass

    def receive_round_result_message(self, winners, hand_info, round_state):
        pass

def setup_ai():
    return INFO2Player()