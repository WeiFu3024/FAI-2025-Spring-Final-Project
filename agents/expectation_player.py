from game.players import BasePokerPlayer
import random as rand
import numpy as np
from agents.hand_strength import win_rate as win_rate_approx

RANK_ORDER = '23456789TJQKA'
SUIT_ORDER = 'CDHS'
DECK = set([suit + rank for suit in SUIT_ORDER for rank in RANK_ORDER])

class ExpectationPlayer(BasePokerPlayer):
    def __init__(self):
        pass
    
    def already_win(self, stack, round_remains):
        sb = self.game_info['rule']['small_blind_amount']
        bb = 2 * sb
        potential_future_risk = round_remains * (sb + bb) / 2 + bb
        return stack - self.game_info['rule']['initial_stack'] > potential_future_risk

    def declare_action(self, valid_actions, hole_card, round_state):
        self.id = round_state['next_player']
        community_cards = round_state['community_card']
        stack = round_state['seats'][self.id]['stack']
        pot = round_state['pot']['main']['amount']
        sb = self.game_info['rule']['small_blind_amount']

        fold_action_info = valid_actions[0]
        call_action_info = valid_actions[1]
        raise_action_info = valid_actions[2]

        if self.already_win(stack, self.game_info['rule']['max_round'] - round_state['round_count']):
            return fold_action_info['action'], fold_action_info['amount']

        win_rate = win_rate_approx(hole_card, community_cards, simulations=500)
        # print("win_rate", win_rate)

        exp_fold = stack
        exp_pass = stack + pot * win_rate - (1 - win_rate) * (call_action_info['amount'] - self.previous_bid)
        raise_amount = max((win_rate - 0.5) * (raise_action_info['amount']['max']) * (1 + len(community_cards)) / 6, raise_action_info['amount']['min'])
        exp_raise = stack + (pot + raise_amount - self.previous_bid) * win_rate - (1 - win_rate) * (raise_amount - self.previous_bid)

        if call_action_info['amount'] >= raise_action_info['amount']['max']:
            exp_raise = -1
        if raise_amount < 0:
            exp_raise = -1
        else:
            exp_raise = int(stack - (raise_amount - self.previous_bid) * (1 - win_rate) + (win_rate) * (pot + (raise_amount - self.previous_bid)))     # Heuristic


        # print(f"Expected values: Fold={exp_fold}, Call={exp_pass}, Raise={exp_raise}")
        if self.already_raised:
            exp_raise = -1

        if exp_fold >= exp_pass and exp_fold >= exp_raise:
            return fold_action_info['action'], fold_action_info['amount']
        if exp_pass >= exp_fold and exp_pass >= exp_raise:
            self.previous_bid = call_action_info['amount']
            return call_action_info['action'], call_action_info['amount']
        if exp_raise >= exp_fold and exp_raise >= exp_pass:
            self.previous_bid = raise_amount
            self.already_raised = True
            return raise_action_info['action'], raise_amount
        
    def receive_game_start_message(self, game_info):
        self.game_info = game_info  # player_num, rule, max_round, initial_stack, small_blind_amount, ante, blind_structure

    def receive_round_start_message(self, round_count, hole_card, seats):
        self.round_count = round_count
        self.hole_cards = hole_card  # Store current hole cards

    def receive_street_start_message(self, street, round_state):
        self.street_idx = {'preflop': 1, 'flop': 2, 'turn': 3, 'river': 4}.get(street, -1)
        self.previous_bid = 0
        self.already_raised = False

    def receive_game_update_message(self, new_action, round_state):
        pass

    def receive_round_result_message(self, winners, hand_info, round_state):
        self.hand_info = hand_info

def setup_ai():
    return ExpectationPlayer()