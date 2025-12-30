from game.players import BasePokerPlayer
import random as rand
import numpy as np
from agents.hand_strength import win_rate as win_rate_approx

RANK_ORDER = '23456789TJQKA'
SUIT_ORDER = 'CDHS'
DECK = set([suit + rank for suit in SUIT_ORDER for rank in RANK_ORDER])
STREET_IDX = {'preflop': 1, 'flop': 2, 'turn': 3, 'river': 4}

THRESHOLD = [0.55, 0.6, 0.65, 0.7]  # Preflop, Flop, Turn, River

RAISE_AMOUNT = [25, 50, 50, 0]

class JustWinPlayer(BasePokerPlayer):
    def __init__(self):
        self.win_rate_record = [[], [], [], []]
        pass
    
    def Kelly_criterion(self, p, stack, pot):
        return p / (1 + (1 - p) * stack / pot) * stack
    
    def already_win(self, stack, round_remains):
        sb = self.game_info['rule']['small_blind_amount']
        bb = 2 * sb
        potential_future_risk = round_remains * (sb + bb) / 2 + bb
        return stack - self.game_info['rule']['initial_stack'] > potential_future_risk
    
    def how_much_to_win(self, stack, pot, round_remains):
        sb = self.game_info['rule']['small_blind_amount']
        bb = 2 * sb
        potential_future_risk = round_remains * (sb + bb) / 2 + bb
        return self.game_info['rule']['initial_stack'] - stack + potential_future_risk - pot


    def declare_action(self, valid_actions, hole_card, round_state):
        self.id = round_state['next_player']
        community_cards = round_state['community_card']
        stack = round_state['seats'][self.id]['stack']
        pot = round_state['pot']['main']['amount']
        round_remains = self.game_info['rule']['max_round'] - round_state['round_count']

        fold_action_info = valid_actions[0]
        call_action_info = valid_actions[1]
        raise_action_info = valid_actions[2]

        if self.already_win(stack, self.game_info['rule']['max_round'] - round_state['round_count']):
            print("Already win, no need to play")
            return fold_action_info['action'], fold_action_info['amount']

        win_rate = win_rate_approx(hole_card, community_cards, simulations=1000)
        self.win_rate_record[self.street_idx - 1].append(win_rate)
        print("win_rate", win_rate)

        if win_rate > THRESHOLD[self.street_idx - 1]:
            if self.street_idx == 4 and not self.already_raised:
                self.already_raised = True
                return raise_action_info['action'], max(self.how_much_to_win(stack, pot, round_remains), raise_action_info['amount']['min'])
            else:
                if win_rate > THRESHOLD[self.street_idx - 1] + 0.1 and not self.already_raised:
                    self.already_raised = True
                    raise_amount = RAISE_AMOUNT[self.street_idx - 1]
                    return raise_action_info['action'], max(raise_amount, raise_action_info['amount']['min'])
                else:
                    return call_action_info['action'], call_action_info['amount']
        return fold_action_info['action'], fold_action_info['amount']
        
    def receive_game_start_message(self, game_info):
        self.game_info = game_info  # player_num, rule, max_round, initial_stack, small_blind_amount, ante, blind_structure

    def receive_round_start_message(self, round_count, hole_card, seats):
        self.round_count = round_count
        self.hole_cards = hole_card  # Store current hole cards

    def receive_street_start_message(self, street, round_state):
        print(street)
        self.street_idx = STREET_IDX[street]
        self.previous_bid = 0
        self.already_raised = False

    def receive_game_update_message(self, new_action, round_state):
        pass

    def receive_round_result_message(self, winners, hand_info, round_state):
        self.hand_info = hand_info
        print(self.win_rate_record)

def setup_ai():
    return JustWinPlayer()