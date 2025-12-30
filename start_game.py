import json
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

from agents.baseline_agent import setup_ai as baseline_agent_ai
from agents.MCT_player import setup_ai as mct_ai
from agents.expectation_player import setup_ai as expectation_ai
from agents.One_Shot import setup_ai as one_shot_ai
from agents.Info_player import setup_ai as info_ai
from agents.Info_player2_5 import setup_ai as info2_5_ai
from agents.Info_player3 import setup_ai as info3_ai
from agents.just_win_player import setup_ai as just_win_ai

config = setup_config(max_round=20, initial_stack=1000, small_blind_amount=5)
config.register_player(name="p2_INFO3", algorithm=info3_ai())
config.register_player(name="p1", algorithm=baseline7_ai())
# config.register_player(name="p2", algorithm=random_ai())
# config.register_player(name="p2_baseline", algorithm=baseline_agent_ai())
# config.register_player(name="p2_MCT", algorithm=mct_ai())
# config.register_player(name="p3_INFO3", algorithm=info3_ai())
# config.register_player(name="p4_JustWin", algorithm=just_win_ai())
# config.register_player(name="p2_OneShot", algorithm=one_shot_ai())
# config.register_player(name="p2", algorithm=random_ai())



## Play in interactive mode if uncomment
# config.register_player(name="me", algorithm=console_ai())
game_result = start_poker(config, verbose=1)

print(json.dumps(game_result, indent=4))