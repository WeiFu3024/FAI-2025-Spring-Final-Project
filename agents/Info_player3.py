from game.players import BasePokerPlayer
import random as rand
import numpy as np
import bisect
import json
from agents.hand_strength import win_rate as win_rate_approx

INFO_REMAIN = [0.24766699999999994, 0.16949899999999998, 0.12006300000000003, 0]

CONFIDENCE_025 =  [0.11617833818181818, 0.04813771599999999, 0.02284125365853659, 0]
CONFIDENCE_040 = [0.18830554444444442, 0.09989621914893616, 0.0475912373493976, 0]
CONFIDENCE_060 = [0.25987088115942025, 0.1495895936507936, 0.08726530243902442, 0]

RANK_ORDER = '23456789TJQKA'
SUIT_ORDER = 'CDHS'
DECK = set([suit + rank for suit in SUIT_ORDER for rank in RANK_ORDER])


class INFO3Player(BasePokerPlayer):
    def __init__(self):
        pass
    
    def Kelly_criterion(self, p, stack, pot):
        return p / (1 + (1 - p) * stack / pot) * stack
    
    def bluff(self):
        total = self.opp_action['fold'][self.street_idx - 1] + self.opp_action['call'][self.street_idx - 1] + self.opp_action['raise'][self.street_idx - 1]
        rate = self.opp_action['fold'][self.street_idx - 1] / total
        if np.random.rand(1) < rate:
            return True
        return False
    
    def aggressive_rate(self, raise_amount):
        raise_amount_data = self.opp_action['bet_amount'][self.street_idx - 1]
        if len(raise_amount_data) < 5:
            return 0
        rank = sum(1 for x in raise_amount_data if x < raise_amount)
        return rank / len(raise_amount_data) 
        # raise_amount_data = self.opp_action['raise_amount'][self.street_idx - 1]
        # if len(raise_amount_data) < 4:
        #     return 0
        # mean, std = np.mean(raise_amount_data), np.std(raise_amount_data)
        # z_score = (raise_amount - mean) / std if std > 0 else 0
        # return z_score
    
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
        self.street_idx = {'preflop': 1, 'flop': 2, 'turn': 3, 'river': 4}.get(round_state['street'], -1)
        sb = self.game_info['rule']['small_blind_amount']

        # Safely access valid_actions
        fold_action_info = next((a for a in valid_actions if a['action'] == 'fold'), None)
        call_action_info = next((a for a in valid_actions if a['action'] == 'call'), None)
        raise_action_info = next((a for a in valid_actions if a['action'] == 'raise'), None)

        if not fold_action_info or not call_action_info:
            raise ValueError("Invalid valid_actions: missing fold or call")

        # Check if already won
        round_remains = self.game_info['rule']['max_round'] - round_state['round_count']
        if self.already_win(stack, round_remains):
            print("Already win, no need to play")
            return fold_action_info['action'], fold_action_info['amount']
        
        # Win Rate Approximation
        win_rate = win_rate_approx(hole_card, community_cards, simulations=1000)
        print("win_rate", win_rate)

        if self.opp_aggressive:
            uncertainty = CONFIDENCE_040[self.street_idx - 1]
        else:
            uncertainty = 0

        safe_rate = win_rate - uncertainty
        if self.opp_aggressive:
            safe_rate *= 1 - 0.2 * self.opp_aggressive_rate

        safe_margin = safe_rate - 0.5

        print(f"safe_rate: {safe_rate}, safe_margin: {safe_margin}")

        # Expectation Calculations
        exp_fold = int(stack)
        exp_pass = int(stack + pot * safe_rate - (1 - safe_rate) * (call_action_info['amount'] - self.previous_bid))

        # Initialize raise_amount
        raise_amount = -1

        # Raise Calculations
        if self.street_idx == 1:
            if raise_action_info and raise_action_info['amount']['min'] > 10 * sb:
                raise_amount = -1
            elif raise_action_info and safe_rate < 0.4:  # Fix preflop logic
                raise_amount = -1
            elif raise_action_info:
                raise_amount = 5 * sb
                raise_amount = max(raise_amount, raise_action_info['amount']['min'])
                raise_amount = min(raise_amount, raise_action_info['amount']['max'])
        else:  # Remove redundant already_raised check
            if safe_rate < 0.4:
                raise_amount = -1
            elif raise_action_info:
                if safe_rate < 0.6:
                    raise_amount = min(safe_margin * (raise_action_info['amount']['max']) * (1 - uncertainty), pot / 4)
                else:
                    raise_amount = safe_margin * (raise_action_info['amount']['max']) * (1 - uncertainty)
                raise_amount = max(raise_amount, raise_action_info['amount']['min'])
                raise_amount = min(raise_amount, raise_action_info['amount']['max'])
        
        # Fix all-in logic
        if call_action_info['amount'] >= raise_action_info['amount']['max'] and safe_rate > 0.5:  # ALL IN Check
            exp_raise = -1
        if self.already_raised:  # If already raised, don't raise again
            exp_raise = -1
            raise_amount = -1
        elif raise_amount < 0:
            exp_raise = -1

        if raise_amount >= 0:
            exp_raise = int(stack - (raise_amount - self.previous_bid) * (1 - win_rate + uncertainty) + (win_rate - uncertainty) * (pot + (raise_amount - self.previous_bid)))
        else:
            exp_raise = -1

        print(f"exp_fold: {exp_fold}, exp_pass: {exp_pass}, exp_raise: {exp_raise}, raise_amount: {raise_amount}")

        # Expectation Maximization
        if exp_fold >= exp_pass and exp_fold >= exp_raise:
            return fold_action_info['action'], fold_action_info['amount']
        if exp_pass >= exp_fold and exp_pass >= exp_raise:
            self.previous_bid = call_action_info['amount']
            return call_action_info['action'], call_action_info['amount']
        if exp_raise >= exp_fold and exp_raise >= exp_pass and raise_action_info and raise_amount >= raise_action_info['amount']['min']:
            self.previous_bid = raise_amount
            self.already_raised = True
            return raise_action_info['action'], raise_amount

        # Default to fold
        return fold_action_info['action'], fold_action_info['amount']

    def receive_game_start_message(self, game_info):
        self.game_info = game_info  # player_num, rule, max_round, initial_stack, small_blind_amount, ante, blind_structure
        self.opp_action = {
            'fold': [0, 0, 0, 0],
            'call': [0, 0, 0, 0],
            'raise': [0, 0, 0, 0],
            'raise_amount': [[], [], [], []],
            'bet_amount': [[], [], [], []]
        }
        pass

    def receive_round_start_message(self, round_count, hole_card, seats):
        self.opp_raise = 0  # Track opponent's maximum raise in a round
        self.opp_aggressive = False  # Track if opponent is aggressive
        self.opp_aggressive_rate = 0  # Track the aggressive rate of the opponent
        self.opp_bluff = False  # Track if the opponent is bluffing
        # self._final_win_rate = 0
        pass

    def receive_street_start_message(self, street, round_state):
        self.street_idx = {'preflop': 1, 'flop': 2, 'turn': 3, 'river': 4}.get(street, -1)
        self.previous_bid = 0  # Reset previous bid at the start of each street
        self.opp_previous_bid = 0  # Reset opponent's previous bid at the start of each street
        self.already_raised = False  # Track if the player has already raised in the current street
        pass

    def receive_game_update_message(self, new_action, round_state):
        # print("new_action", new_action)
        # print(round_state)
        
        if new_action['player_uuid'] != self.uuid:
            cost = max(new_action['amount'] - self.opp_previous_bid, 0)

            for i in range(len(round_state['seats'])):
                if round_state['seats'][i]['uuid'] == new_action['player_uuid']:
                    self.opp_stack = round_state['seats'][i]['stack']
                    break

            if new_action['action'] == "raise":
                self.opp_aggressive_rate = self.aggressive_rate(new_action['amount'])
                if self.opp_aggressive_rate > 0.8 or cost >= self.opp_stack:  # HYPERPARAMETER
                    self.opp_aggressive = True
                    pass
                else:
                    self.opp_aggressive = False
                if self.opp_aggressive and round_state['round_count'] > 17:
                    self.opp_aggressive = False  # HYPERPARAMETER, reset aggressive state after a certain round
                    self.opp_bluff = True
                print(f"Opponent Aggressive: {self.opp_aggressive}, Aggressive Rate: {self.aggressive_rate(cost)}")
                
                self.opp_action['raise'][self.street_idx - 1] += 1
                self.opp_action['raise_amount'][self.street_idx - 1].append(cost)
            else:
                self.opp_action[new_action['action']][self.street_idx - 1] += 1
            
            bisect.insort(self.opp_action['bet_amount'][self.street_idx - 1], cost)
            self.opp_previous_bid = new_action['amount']
        print(self.opp_action)
        pass

    def receive_round_result_message(self, winners, hand_info, round_state):
        pass

def setup_ai():
    return INFO3Player()