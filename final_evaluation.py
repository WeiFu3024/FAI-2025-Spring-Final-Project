import json
from tqdm import tqdm
from game.game import setup_config, start_poker
from agents.call_player import setup_ai as call_ai
from agents.random_player import setup_ai as random_ai
from agents.console_player import setup_ai as console_ai
import bisect
from baseline0 import setup_ai as baseline0_ai
from baseline1 import setup_ai as baseline1_ai
from baseline2 import setup_ai as baseline2_ai
from baseline3 import setup_ai as baseline3_ai
from baseline4 import setup_ai as baseline4_ai
from baseline5 import setup_ai as baseline5_ai
from baseline6 import setup_ai as baseline6_ai
from baseline7 import setup_ai as baseline7_ai

from agents.MCT_player import setup_ai as mct_ai
from agents.expectation_player import setup_ai as expectation_ai
from agents.One_Shot import setup_ai as one_shot_ai
from agents.Info_player import setup_ai as info_ai
from agents.Info_player2_5 import setup_ai as info2_5_ai
from agents.Info_player2 import setup_ai as info2_ai
from agents.Info_player3 import setup_ai as info3_ai

baseline = [baseline0_ai(), baseline1_ai(), baseline2_ai(), baseline3_ai(), baseline4_ai(), baseline5_ai(), baseline6_ai(), baseline7_ai()]

baseline_strong = [baseline4_ai(), baseline6_ai(), baseline7_ai()]

simulation = 5
num_agent = 8

total_score = [[], []]

for i in range(num_agent - 1, 0, -1):
    # Left
    config = setup_config(max_round=20, initial_stack=1000, small_blind_amount=5)
    config.register_player(name="p1", algorithm=baseline[i])
    config.register_player(name="p2_Info3", algorithm=info3_ai())
    wins = 0
    ties = 0
    score = []
    for _ in tqdm(range(simulation), desc=f"Baseline {i} vs Exp"):
        game_result = start_poker(config, verbose=1)
        if game_result['players'][0]["stack"] < game_result['players'][1]["stack"]:
            wins += 1
            bisect.insort(score, 1.5)
        elif game_result['players'][1]["stack"] >= 500:
            bisect.insort(score, game_result['players'][1]["stack"] / 1000)
        else:
            bisect.insort(score, 0)
    
    if wins >= 3:
        final_score = 5
    else:
        final_score = score[-1] + score[-2]
    total_score[0].append(final_score)

    # Right
    config = setup_config(max_round=20, initial_stack=1000, small_blind_amount=5)
    config.register_player(name="p2_Info3", algorithm=info3_ai())
    config.register_player(name="p1", algorithm=baseline[i])
    wins = 0
    ties = 0
    score = []
    for _ in tqdm(range(simulation), desc=f"Baseline {i} vs Exp"):
        game_result = start_poker(config, verbose=1)
        if game_result['players'][1]["stack"] < game_result['players'][0]["stack"]:
            wins += 1
            bisect.insort(score, 1.5)
        elif game_result['players'][0]["stack"] >= 500:
            bisect.insort(score, game_result['players'][1]["stack"] / 1000)
        else:
            bisect.insort(score, 0)
    
    if wins >= 3:
        final_score = 5
    else:
        final_score = score[-1] + score[-2]
    total_score[1].append(final_score)
    
print("Total Score:", total_score)