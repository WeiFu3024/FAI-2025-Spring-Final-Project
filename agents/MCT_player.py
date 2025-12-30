from game.players import BasePokerPlayer
import random as rand
import numpy as np
from agents.hand_strength import win_rate as win_rate_approx
import time

RANK_ORDER = '23456789TJQKA'
SUIT_ORDER = 'CDHS'
DECK = set([suit + rank for suit in SUIT_ORDER for rank in RANK_ORDER])

class MCTPlayer(BasePokerPlayer):
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
        community_cards = round_state['community_card']
        stack = round_state['seats'][self.id]['stack']
        print("stack", stack)

        fold_action_info = valid_actions[0]
        call_action_info = valid_actions[1]
        raise_action_info = valid_actions[2]

        if self.already_win(stack, self.game_info['rule']['max_round'] - round_state['round_count']):
            print("Already win, no need to play")
            return fold_action_info['action'], fold_action_info['amount']

        win_rate = win_rate_approx(hole_card, community_cards, simulations=500)
        print("win_rate", win_rate)

        if win_rate > 0.55 and not self.already_raised:
            raise_amount = (win_rate - 0.55) * raise_action_info['amount']['max'] * (1 + len(community_cards)) / 6
            self.already_raised = True
            return raise_action_info['action'], max(min(raise_amount, raise_action_info['amount']['max']), raise_action_info['amount']['min'])
        elif win_rate > 0.35 and call_action_info['amount'] < (win_rate - 0.35) * stack:
            return call_action_info['action'], call_action_info['amount']
        else:
            return fold_action_info['action'], fold_action_info['amount']
        
    def receive_game_start_message(self, game_info):
        self.game_info = game_info  # player_num, rule, max_round, initial_stack, small_blind_amount, ante, blind_structure
        pass

    def receive_round_start_message(self, round_count, hole_card, seats):
        self.previous_bid = 0
        pass

    def receive_street_start_message(self, street, round_state):
        self.street_idx = {'preflop': 1, 'flop': 2, 'turn': 3, 'river': 4}.get(street, -1)
        self.already_raised = False
        pass

    def receive_game_update_message(self, new_action, round_state):
        pass

    def receive_round_result_message(self, winners, hand_info, round_state):
        pass

def setup_ai():
    return MCTPlayer()