from game.players import BasePokerPlayer
import random as rand


class RandomPlayer(BasePokerPlayer):
    def __init__(self):
        self.fold_ratio = self.call_ratio = raise_ratio = 1.0 / 3

    def set_action_ratio(self, fold_ratio, call_ratio, raise_ratio):
        ratio = [fold_ratio, call_ratio, raise_ratio]
        scaled_ratio = [1.0 * num / sum(ratio) for num in ratio]
        self.fold_ratio, self.call_ratio, self.raise_ratio = scaled_ratio

    def declare_action(self, valid_actions, hole_card, round_state):
        # print("\n", "round status:", round_state, "\n")
        choice = self.__choice_action(valid_actions)
        action = choice["action"]
        amount = choice["amount"]
        if action == "raise":
            amount = rand.randrange(
                amount["min"], max(amount["min"], amount["max"]) + 1
            )
        return action, amount

    def __choice_action(self, valid_actions):
        r = rand.random()
        if r <= self.fold_ratio:
            return valid_actions[0]
        elif r <= self.call_ratio:
            return valid_actions[1]
        else:
            return valid_actions[2]

    def receive_game_start_message(self, game_info):
        # print("game info:", game_info)
        pass

    def receive_round_start_message(self, round_count, hole_card, seats):
        # print(f"Round {round_count} started with hole cards: {hole_card}")
        pass

    def receive_street_start_message(self, street, round_state):
        print(f"Street {street} started with round state: {round_state}")
        pass

    def receive_game_update_message(self, new_action, round_state):
        # print(f"Game updated with action: {new_action} and round state: {round_state}")
        pass

    def receive_round_result_message(self, winners, hand_info, round_state):
        # print(f"Round ended with winners: {winners}, hand info: {hand_info}, and round state: {round_state}")
        pass


def setup_ai():
    return RandomPlayer()
