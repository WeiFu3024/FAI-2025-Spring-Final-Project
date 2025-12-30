from game.players import BasePokerPlayer
import random as rand
from agents.hand_strength import win_rate as win_rate_approx
import numpy as np
import json

RANK_ORDER = '23456789TJQKA'
SUIT_ORDER = 'CDHS'
DECK = set([suit + rank for suit in SUIT_ORDER for rank in RANK_ORDER])

class OneShotPlayer(BasePokerPlayer):
    def __init__(self):
        self.fold_ratio = self.call_ratio = raise_ratio = 1.0 / 3
        
    def set_action_ratio(self, fold_ratio, call_ratio, raise_ratio):
        ratio = [fold_ratio, call_ratio, raise_ratio]
        scaled_ratio = [1.0 * num / sum(ratio) for num in ratio]
        self.fold_ratio, self.call_ratio, self.raise_ratio = scaled_ratio
    
    def already_win(self, stack, round_remains):
        potential_future_risk = round_remains * (self.sb + self.bb) / 2 + self.bb
        return stack - self.game_info['rule']['initial_stack'] > potential_future_risk

    
    def Kelly_criterion(self, p, stack, pot):
        return p / (1 + (1 - p) * stack / pot) * stack

    def declare_action(self, valid_actions, hole_card, round_state):
        self.id = round_state['next_player']
        stack = round_state['seats'][self.id]['stack']

        community_cards = round_state['community_card']
        street = round_state['street']
        street_idx = {'pre_flop': 1, 'flop': 2, 'turn': 3, 'river': 4}.get(street, -1)
        self.street_idx = street_idx

        fold_action_info = valid_actions[0]
        call_action_info = valid_actions[1]
        raise_action_info = valid_actions[2]

        round_remains = self.game_info['rule']['max_round'] - round_state['round_count']
        
        if self.already_win(stack, round_remains):
            # print("Already win, no need to play")
            return fold_action_info['action'], fold_action_info['amount']

        win_rate = win_rate_approx(hole_card, community_cards, 1000)
        print("win_rate", win_rate)

        if street_idx <= 2:
            if win_rate > 0.5 and not self.already_win(2 * self.game_info['rule']['initial_stack'] - (stack - call_action_info['amount']), round_remains):
                return call_action_info['action'], call_action_info['amount']
            elif win_rate > 0.65:
                return call_action_info['action'], call_action_info['amount']
            else:
                return fold_action_info['action'], fold_action_info['amount']
        else:
            if win_rate < 0.7:
                return fold_action_info['action'], fold_action_info['amount']
            else:
                raise_amount = max((self.bb + round_remains * (self.bb + self.sb)/2 + 10)/2, raise_action_info['amount']['min'])
                # raise_amount = max(min(kelly_bet, raise_action_info['amount']['max']), raise_action_info['amount']['min'])
                # raise_amount = min(raise_amount, self.round_state['seats'][self.id]['stack'] * 0.6)
                return raise_action_info['action'], raise_amount

    def receive_game_start_message(self, game_info):
        self.game_info = game_info  # player_num, rule, max_round, initial_stack, small_blind_amount, ante, blind_structure
        self.sb = self.game_info['rule']['small_blind_amount']
        self.bb = 2 * self.sb
        pass

    def receive_round_start_message(self, round_count, hole_card, seats):
        self.round_count = round_count
        self.hole_cards = hole_card  # Store current hole cards
        pass

    def receive_street_start_message(self, street, round_state):
        self.street_idx = {'preflop': 1, 'flop': 2, 'turn': 3, 'river': 4}.get(street, -1)
        pass

    def receive_game_update_message(self, new_action, round_state):
        pass

    def receive_round_result_message(self, winners, hand_info, round_state):
        pass

def setup_ai():

    return OneShotPlayer()