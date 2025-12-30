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


class INFOPlayer(BasePokerPlayer):
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
        self.street_idx = {'pre_flop': 1, 'flop': 2, 'turn': 3, 'river': 4}.get(round_state['street'], -1)

        fold_action_info = valid_actions[0]
        call_action_info = valid_actions[1]
        raise_action_info = valid_actions[2]

        if self.already_win(stack, self.game_info['rule']['max_round'] - round_state['round_count']):
            print("Already win, no need to play")
            return fold_action_info['action'], fold_action_info['amount']

        win_rate = win_rate_approx(hole_card, community_cards, simulations=500)
        print("win_rate", win_rate)

        uncertainty = CONFIDENCE_040[self.street_idx - 1]
        margin = win_rate - 0.5

        if win_rate > 0.5 + uncertainty and not self.already_raised:
            self.already_raised = True
            raise_amount = (win_rate - 0.5 - uncertainty) * raise_action_info['amount']['max'] * (1 - INFO_REMAIN[self.street_idx - 1])
            return raise_action_info['action'], max(min(raise_amount, raise_action_info['amount']['max']), raise_action_info['amount']['min'])
        elif win_rate > 0.35 + uncertainty and call_action_info['amount'] < (win_rate - 0.35 - uncertainty) * stack:
            return call_action_info['action'], call_action_info['amount']
        else:
            return fold_action_info['action'], fold_action_info['amount']
        
    def receive_game_start_message(self, game_info):
        self.game_info = game_info  # player_num, rule, max_round, initial_stack, small_blind_amount, ante, blind_structure
        # print("game info:", game_info)
        pass

    def receive_round_start_message(self, round_count, hole_card, seats):
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
    return INFOPlayer()