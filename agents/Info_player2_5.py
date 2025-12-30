from game.players import BasePokerPlayer
import random as rand
import numpy as np
import json
from agents.hand_strength import win_rate as win_rate_approx

INFO_REMAIN = [0.24766699999999994, 0.16949899999999998, 0.12006300000000003, 0]

CONFIDENCE_025 = [0.11617833818181818, 0.04813771599999999, 0.02284125365853659, 0]
CONFIDENCE_040 = [0.18830554444444442, 0.09989621914893616, 0.0475912373493976, 0]
CONFIDENCE_060 = [0.25987088115942025, 0.1495895936507936, 0.08726530243902442, 0]

RANK_ORDER = '23456789TJQKA'
SUIT_ORDER = 'CDHS'
DECK = set([suit + rank for suit in SUIT_ORDER for rank in RANK_ORDER])


class INFO2_5Player(BasePokerPlayer):
    def __init__(self):
        self.previous_bid = 0
        self.already_raised = False
        self.opp_previous_bid = 0
        self.opp_aggresive = False
        self.opp_bluff = False
        self.opp_stack = 0
        self.street_idx = -1
        self.game_info = None
        self.opp_raise = 0
        self.id = -1
        self.uuid = None  # Initialize uuid

    def Kelly_criterion(self, p, stack, pot):
        # Avoid division by zero
        if pot == 0:
            return 0
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

        # Safely access valid_actions
        fold_action_info = next((a for a in valid_actions if a['action'] == 'fold'), None)
        call_action_info = next((a for a in valid_actions if a['action'] == 'call'), None)
        raise_action_info = next((a for a in valid_actions if a['action'] == 'raise'), None)

        if not fold_action_info or not call_action_info:
            raise ValueError("Invalid valid_actions: missing fold or call")

        round_remains = self.game_info['rule']['max_round'] - round_state['round_count']
        if self.already_win(stack, round_remains):
            print("Already win, no need to play")
            return fold_action_info['action'], fold_action_info['amount']

        win_rate = win_rate_approx(hole_card, community_cards, simulations=1000)
        print("win_rate", win_rate)

        uncertainty = CONFIDENCE_025[self.street_idx - 1]
        if self.opp_bluff:
            uncertainty = 0
        safe_rate = win_rate - uncertainty
        if self.opp_aggresive:
            safe_rate *= 0.9
        # Fix safe_margin calculation
        safe_margin = safe_rate - 0.5

        print(f"safe_rate: {safe_rate}, safe_margin: {safe_margin}")

        exp_fold = stack
        # Remove duplicate exp_pass
        exp_pass = stack + pot * safe_rate - (1 - safe_rate) * (call_action_info['amount'] - self.previous_bid)
        # Initialize raise_amount conditionally
        raise_amount = -1
        if raise_action_info:
            raise_amount = max(safe_margin * (raise_action_info['amount']['max']) * (1 - uncertainty), raise_action_info['amount']['min'])

        exp_raise = -1
        if raise_action_info and raise_amount >= 0:
            exp_raise = stack - (raise_amount - self.previous_bid) * (1 - win_rate + uncertainty) + (win_rate - uncertainty) * (pot + (raise_amount - self.previous_bid))

        if self.street_idx == 1:
            if raise_action_info and raise_action_info['amount']['min'] > 20 * sb and safe_rate < 0.4:
                print("Fold due to low safe rate and high risk")
                return fold_action_info['action'], fold_action_info['amount']
            elif raise_action_info and raise_action_info['amount']['min'] > 5 * sb:
                raise_amount = -1
            elif raise_action_info:
                raise_amount = 5 * sb
                raise_amount = max(raise_amount, raise_action_info['amount']['min'])
                raise_amount = min(raise_amount, raise_action_info['amount']['max'])
        elif self.street_idx == 2:
            if safe_rate < 0.4 and call_action_info['amount'] > pot / 4:  # Fix comparison
                print("Fold due to low safe rate and high risk")
                return fold_action_info['action'], fold_action_info['amount']
            elif raise_action_info and raise_action_info['amount']['min'] > pot / 4:
                raise_amount = -1
            elif raise_action_info:
                raise_amount = pot / 4
                raise_amount = max(raise_amount, raise_action_info['amount']['min'])
                raise_amount = min(raise_amount, raise_action_info['amount']['max'])
        elif self.street_idx == 3:
            if safe_rate < 0.4 and call_action_info['amount'] > pot / 2:  # Fix comparison
                print("Fold due to low safe rate and high risk")
                return fold_action_info['action'], fold_action_info['amount']
            elif raise_action_info and safe_rate < 0.5 and raise_action_info['amount']['min'] <= pot / 2:
                raise_amount = min(safe_margin * (raise_action_info['amount']['max']) * (1 - uncertainty), pot / 2)
                raise_amount = max(raise_amount, raise_action_info['amount']['min'])
                raise_amount = min(raise_amount, raise_action_info['amount']['max'])
            elif raise_action_info and safe_rate < 0.5:
                raise_amount = -1
            elif raise_action_info:
                raise_amount = safe_margin * (raise_action_info['amount']['max']) * (1 - uncertainty)
                raise_amount = max(raise_amount, raise_action_info['amount']['min'])
                raise_amount = min(raise_amount, raise_action_info['amount']['max'])
        elif self.street_idx == 4:  # Add river logic
            if safe_rate < 0.5 and call_action_info['amount'] > pot / 2:
                print("Fold due to low safe rate and high risk")
                return fold_action_info['action'], fold_action_info['amount']
            elif raise_action_info and safe_rate >= 0.5:
                raise_amount = safe_margin * (raise_action_info['amount']['max']) * (1 - uncertainty)
                raise_amount = max(raise_amount, raise_action_info['amount']['min'])
                raise_amount = min(raise_amount, raise_action_info['amount']['max'])
            elif raise_action_info:
                raise_amount = -1

        if raise_amount < 0:
            print("Hit constraint, don't raise")
            exp_raise = -1

        if self.already_raised:
            exp_raise = -1
            raise_amount = -1

        # Fix all-in handling
        if raise_action_info and raise_amount >= raise_action_info['amount']['min'] and raise_amount >= raise_action_info['amount']['max']:
            print("ALL IN")
            exp_raise = stack - (raise_amount - self.previous_bid) * (1 - safe_rate) + safe_rate * pot

        print(f"exp_fold: {exp_fold}, exp_pass: {exp_pass}, exp_raise: {exp_raise}, raise_amount: {raise_amount}")

        if exp_fold >= exp_pass and exp_fold >= exp_raise:
            return fold_action_info['action'], fold_action_info['amount']
        if exp_pass >= exp_fold and exp_pass >= exp_raise:
            self.previous_bid = call_action_info['amount']
            return call_action_info['action'], call_action_info['amount']
        if exp_raise >= exp_fold and exp_raise >= exp_pass and raise_action_info and raise_amount >= raise_action_info['amount']['min']:
            self.already_raised = True
            self.previous_bid = raise_amount
            return raise_action_info['action'], raise_amount

        # Default to fold
        return fold_action_info['action'], fold_action_info['amount']

    def receive_game_start_message(self, game_info):
        self.game_info = game_info
        pass

    def receive_round_start_message(self, round_count, hole_card, seats):
        self.opp_raise = 0
        pass

    def receive_street_start_message(self, street, round_state):
        self.previous_bid = 0
        self.already_raised = False
        self.opp_previous_bid = 0
        self.opp_aggresive = False
        self.opp_bluff = False
        self.street_idx = {'preflop': 1, 'flop': 2, 'turn': 3, 'river': 4}.get(street, -1)
        pass

    def receive_game_update_message(self, new_action, round_state):
        if new_action['player_uuid'] != self.uuid:
            cost = max(new_action['amount'] - self.opp_previous_bid, 0)

            for i in range(len(round_state['seats'])):
                if round_state['seats'][i]['uuid'] == new_action['player_uuid']:
                    self.opp_stack = round_state['seats'][i]['stack']
                    break

            if new_action['action'] == "raise":
                if cost >= self.opp_stack * 0.9 and round_state['round_count'] <= 15:
                    self.opp_aggresive = True
                elif cost >= self.opp_stack * 0.9 and round_state['round_count'] > 15:
                    self.opp_bluff = True
                else:
                    self.opp_aggresive = False

            self.opp_previous_bid = new_action['amount']
        pass

    def receive_round_result_message(self, winners, hand_info, round_state):
        pass

def setup_ai():
    return INFO2_5Player()