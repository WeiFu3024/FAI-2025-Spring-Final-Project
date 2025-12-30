import json
from tqdm import tqdm
from game.game import setup_config, start_poker
from agents.call_player import setup_ai as call_ai
from agents.random_player import setup_ai as random_ai
from agents.console_player import setup_ai as console_ai
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

mct_wr = [[], []]
exp_wr = [[], []]
one_wr = [[], []]
info_wr = [[], []]
info2_wr = [[], []]
info2_5_wr = [[], []]
info3_wr = [[], []]

num_agent = 8

# for i in range(num_agent):
#     # Left
#     config = setup_config(max_round=20, initial_stack=1000, small_blind_amount=5)
#     config.register_player(name="p1", algorithm=baseline[i])
#     config.register_player(name="p2_MCT", algorithm=mct_ai())
#     wins = 0
#     ties = 0
#     for _ in tqdm(range(simulation), desc=f"Baseline {i} vs MCT"):
#         game_result = start_poker(config, verbose=1)
#         if game_result['players'][0]["stack"] < game_result['players'][1]["stack"]:
#             wins += 1
#         elif game_result['players'][0]["stack"] == game_result['players'][1]["stack"]:
#             ties += 1
#         print("wins:", wins, " ties: ", ties)
#     print(f"Baseline {i} vs MCT: {wins} wins, {ties} ties")
#     mct_wr[0].append((wins + 0.5 * ties) / simulation)

#     # Right
#     config = setup_config(max_round=20, initial_stack=1000, small_blind_amount=5)
#     config.register_player(name="p2_MCT", algorithm=mct_ai())
#     config.register_player(name="p1", algorithm=baseline[i])
#     wins = 0
#     ties = 0
#     for _ in tqdm(range(simulation), desc=f"Baseline {i} vs MCT"):
#         game_result = start_poker(config, verbose=1)
#         if game_result['players'][1]["stack"] < game_result['players'][0]["stack"]:
#             wins += 1
#         elif game_result['players'][1]["stack"] == game_result['players'][0]["stack"]:
#             ties += 1
#         print("wins:", wins, " ties: ", ties)
#     print(f"Baseline {i} vs MCT: {wins} wins, {ties} ties")
#     mct_wr[1].append((wins + 0.5 * ties) / simulation)


# for i in range(num_agent - 1, -1, -1):
#     # Left
#     config = setup_config(max_round=20, initial_stack=1000, small_blind_amount=5)
#     config.register_player(name="p1", algorithm=baseline[i])
#     config.register_player(name="p2_Exp", algorithm=expectation_ai())
#     wins = 0
#     ties = 0
#     for _ in tqdm(range(simulation), desc=f"Baseline {i} vs Exp"):
#         game_result = start_poker(config, verbose=1)
#         if game_result['players'][0]["stack"] < game_result['players'][1]["stack"]:
#             wins += 1
#         elif game_result['players'][0]["stack"] == game_result['players'][1]["stack"]:
#             ties += 1
#         print("wins:", wins, " ties: ", ties)
#     print(f"Baseline {i} vs Exp: {wins} wins, {ties} ties")
#     exp_wr[0].append((wins + 0.5 * ties) / simulation)

    # # Right
    # config = setup_config(max_round=20, initial_stack=1000, small_blind_amount=5)
    # config.register_player(name="p2_Exp", algorithm=expectation_ai())
    # config.register_player(name="p1", algorithm=baseline[i])
    # wins = 0
    # ties = 0
    # for _ in tqdm(range(simulation), desc=f"Baseline {i} vs Exp"):
    #     game_result = start_poker(config, verbose=1)
    #     if game_result['players'][1]["stack"] < game_result['players'][0]["stack"]:
    #         wins += 1
    #     elif game_result['players'][1]["stack"] == game_result['players'][0]["stack"]:
    #         ties += 1
    #     print("wins:", wins, " ties: ", ties)
    # print(f"Baseline {i} vs Exp: {wins} wins, {ties} ties")
    # exp_wr[1].append((wins + 0.5 * ties) / simulation)

# for i in range(num_agent):
#     # Left
#     config = setup_config(max_round=20, initial_stack=1000, small_blind_amount=5)
#     config.register_player(name="p1", algorithm=baseline[i])
#     config.register_player(name="p2_One", algorithm=one_shot_ai())
#     wins = 0
#     ties = 0
#     for _ in tqdm(range(simulation), desc=f"Baseline {i} vs One"):
#         game_result = start_poker(config, verbose=1)
#         if game_result['players'][0]["stack"] < game_result['players'][1]["stack"]:
#             wins += 1
#         elif game_result['players'][0]["stack"] == game_result['players'][1]["stack"]:
#             ties += 1
#         print("wins:", wins, " ties: ", ties)
#     print(f"Baseline {i} vs One: {wins} wins, {ties} ties")
#     one_wr[0].append((wins + 0.5 * ties) / simulation)

#     # Right
#     config = setup_config(max_round=20, initial_stack=1000, small_blind_amount=5)
#     config.register_player(name="p2_One", algorithm=one_shot_ai())
#     config.register_player(name="p1", algorithm=baseline[i])
#     wins = 0
#     ties = 0
#     for _ in tqdm(range(simulation), desc=f"Baseline {i} vs One"):
#         game_result = start_poker(config, verbose=1)
#         if game_result['players'][0]["stack"] < game_result['players'][1]["stack"]:
#             wins += 1
#         elif game_result['players'][0]["stack"] == game_result['players'][1]["stack"]:
#             ties += 1
#         print("wins:", wins, " ties: ", ties)
#     print(f"Baseline {i} vs One: {wins} wins, {ties} ties")
#     one_wr[1].append((wins + 0.5 * ties) / simulation)

# for i in range(num_agent):
#     config = setup_config(max_round=20, initial_stack=1000, small_blind_amount=5)
#     config.register_player(name="p1", algorithm=baseline[i])
#     config.register_player(name="p2_INFO", algorithm=info_ai())
#     wins = 0
#     ties = 0
#     for _ in tqdm(range(simulation), desc=f"Baseline {i} vs Info"):
#         game_result = start_poker(config, verbose=1)
#         if game_result['players'][0]["stack"] < game_result['players'][1]["stack"]:
#             wins += 1
#         elif game_result['players'][0]["stack"] == game_result['players'][1]["stack"]:
#             ties += 1
#         print("wins:", wins, " ties: ", ties)
#     print(f"Baseline {i} vs Info: {wins} wins, {ties} ties")
#     info_wr[0].append((wins + 0.5 * ties) / simulation)

#     config = setup_config(max_round=20, initial_stack=1000, small_blind_amount=5)
#     config.register_player(name="p2_INFO", algorithm=info_ai())
#     config.register_player(name="p1", algorithm=baseline[i])
#     wins = 0
#     ties = 0
#     for _ in tqdm(range(simulation), desc=f"Baseline {i} vs Info"):
#         game_result = start_poker(config, verbose=1)
#         if game_result['players'][1]["stack"] < game_result['players'][0]["stack"]:
#             wins += 1
#         elif game_result['players'][1]["stack"] == game_result['players'][0]["stack"]:
#             ties += 1
#         print("wins:", wins, " ties: ", ties)
#     print(f"Baseline {i} vs Info: {wins} wins, {ties} ties")
#     info_wr[1].append((wins + 0.5 * ties) / simulation)

# for i in range(num_agent - 1, -1, -1):
#     config = setup_config(max_round=20, initial_stack=1000, small_blind_amount=5)
#     config.register_player(name="p1", algorithm=baseline[i])
#     config.register_player(name="p2_INFO", algorithm=info2_ai())
#     wins = 0
#     ties = 0
#     for _ in tqdm(range(simulation), desc=f"Baseline {i} vs Info2"):
#         game_result = start_poker(config, verbose=1)
#         if game_result['players'][0]["stack"] < game_result['players'][1]["stack"]:
#             wins += 1
#         elif game_result['players'][0]["stack"] == game_result['players'][1]["stack"]:
#             ties += 1
#         print("wins:", wins, " ties: ", ties)
#     print(f"Baseline {i} vs Info2: {wins} wins, {ties} ties")
#     info2_wr[0].append((wins + 0.5 * ties) / simulation)

#     config = setup_config(max_round=20, initial_stack=1000, small_blind_amount=5)
#     config.register_player(name="p2_INFO", algorithm=info2_ai())
#     config.register_player(name="p1", algorithm=baseline[i])
#     wins = 0
#     ties = 0
#     for _ in tqdm(range(simulation), desc=f"Baseline {i} vs Info2"):
#         game_result = start_poker(config, verbose=1)
#         if game_result['players'][1]["stack"] < game_result['players'][0]["stack"]:
#             wins += 1
#         elif game_result['players'][1]["stack"] == game_result['players'][0]["stack"]:
#             ties += 1
#         print("wins:", wins, " ties: ", ties)
#     print(f"Baseline {i} vs Info2: {wins} wins, {ties} ties")
#     info2_wr[1].append((wins + 0.5 * ties) / simulation)

# for i in range(num_agent - 1, -1, -1):
#     config = setup_config(max_round=20, initial_stack=1000, small_blind_amount=5)
#     config.register_player(name="p1", algorithm=baseline[i])
#     config.register_player(name="p2_5_INFO", algorithm=info2_5_ai())
#     wins = 0
#     ties = 0
#     for _ in tqdm(range(simulation), desc=f"Baseline {i} vs Info2_5"):
#         game_result = start_poker(config, verbose=1)
#         if game_result['players'][0]["stack"] < game_result['players'][1]["stack"]:
#             wins += 1
#         elif game_result['players'][0]["stack"] == game_result['players'][1]["stack"]:
#             ties += 1
#         print("wins:", wins, " ties: ", ties)
#     print(f"Baseline {i} vs Info2_5: {wins} wins, {ties} ties")
#     info2_5_wr[0].append((wins + 0.5 * ties) / simulation)

#     config = setup_config(max_round=20, initial_stack=1000, small_blind_amount=5)
#     config.register_player(name="p2_5_INFO", algorithm=info2_5_ai())
#     config.register_player(name="p1", algorithm=baseline[i])
#     wins = 0
#     ties = 0
#     for _ in tqdm(range(simulation), desc=f"Baseline {i} vs Info2_5"):
#         game_result = start_poker(config, verbose=1)
#         if game_result['players'][1]["stack"] < game_result['players'][0]["stack"]:
#             wins += 1
#         elif game_result['players'][1]["stack"] == game_result['players'][0]["stack"]:
#             ties += 1
#         print("wins:", wins, " ties: ", ties)
#     print(f"Baseline {i} vs Info2_5: {wins} wins, {ties} ties")
#     info2_5_wr[1].append((wins + 0.5 * ties) / simulation)


for i in range(num_agent - 1, -1, -1):
    config = setup_config(max_round=20, initial_stack=1000, small_blind_amount=5)
    config.register_player(name="p1", algorithm=baseline[i])
    config.register_player(name="p3_INFO", algorithm=info3_ai())
    wins = 0
    ties = 0
    for _ in tqdm(range(simulation), desc=f"Baseline {i} vs Info3"):
        game_result = start_poker(config, verbose=1)
        if game_result['players'][0]["stack"] < game_result['players'][1]["stack"]:
            wins += 1
        elif game_result['players'][0]["stack"] == game_result['players'][1]["stack"]:
            ties += 1
        print("wins:", wins, " ties: ", ties)
    print(f"Baseline {i} vs Info3: {wins} wins, {ties} ties")
    info3_wr[0].append((wins + 0.5 * ties) / simulation)

    config = setup_config(max_round=20, initial_stack=1000, small_blind_amount=5)
    config.register_player(name="p3_INFO", algorithm=info3_ai())
    config.register_player(name="p1", algorithm=baseline[i])
    wins = 0
    ties = 0
    for _ in tqdm(range(simulation), desc=f"Baseline {i} vs Info3"):
        game_result = start_poker(config, verbose=1)
        if game_result['players'][1]["stack"] < game_result['players'][0]["stack"]:
            wins += 1
        elif game_result['players'][1]["stack"] == game_result['players'][0]["stack"]:
            ties += 1
        print("wins:", wins, " ties: ", ties)
    print(f"Baseline {i} vs Info3: {wins} wins, {ties} ties")
    info3_wr[1].append((wins + 0.5 * ties) / simulation)


# for i, baseline_ai in enumerate(baseline_strong):
#     config = setup_config(max_round=20, initial_stack=1000, small_blind_amount=5)
#     config.register_player(name="p1", algorithm=baseline_ai)
#     config.register_player(name="p2_INFO2", algorithm=info2_ai())
#     wins = 0
#     ties = 0
#     for _ in tqdm(range(simulation), desc=f"Baseline {i} vs Info3"):
#         game_result = start_poker(config, verbose=1)
#         if game_result['players'][0]["stack"] < game_result['players'][1]["stack"]:
#             wins += 1
#         elif game_result['players'][0]["stack"] == game_result['players'][1]["stack"]:
#             ties += 1
#         print("wins:", wins, " ties: ", ties)
#     print(f"Baseline {i} vs Info2: {wins} wins, {ties} ties")
#     info2_wr.append((wins + 0.5 * ties) / simulation)


# for i, baseline_ai in enumerate(baseline_strong):
#     config = setup_config(max_round=20, initial_stack=1000, small_blind_amount=5)
#     config.register_player(name="p1", algorithm=baseline_ai)
#     config.register_player(name="p2_INFO3", algorithm=info3_ai())
#     wins = 0
#     ties = 0
#     for _ in tqdm(range(simulation), desc=f"Baseline {i} vs Info3"):
#         game_result = start_poker(config, verbose=1)
#         if game_result['players'][0]["stack"] < game_result['players'][1]["stack"]:
#             wins += 1
#         elif game_result['players'][0]["stack"] == game_result['players'][1]["stack"]:
#             ties += 1
#         print("wins:", wins, " ties: ", ties)
#     print(f"Baseline {i} vs Info3: {wins} wins, {ties} ties")
#     info3_wr.append((wins + 0.5 * ties) / simulation)


print("MCT win rates:", mct_wr)
print("Expectation win rates:", exp_wr)
# print("One Shot win rates:", one_wr)
print("Info win rates:", info_wr)
print("Info2 win rates:", info2_wr)
print("Info2_5 win rates:", info2_5_wr)
print("Info3 win rates:", info3_wr)