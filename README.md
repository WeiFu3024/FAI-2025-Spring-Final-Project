# Texas Hold'em Poker AI Project

This is a Texas Hold'em Poker AI project that implements various AI strategies for playing poker. The project includes a complete game engine, multiple AI player implementations, and an evaluation system.

## Project Structure

```
final_project-1/
├── agents/              # AI player implementations
│   ├── expectation_player.py    # Expected value calculation strategy
│   ├── MCT_player.py            # Monte Carlo Tree Search strategy
│   ├── Info_player*.py          # Information theory strategies (multiple versions)
│   ├── hand_strength.py         # Hand strength calculation utilities
│   ├── random_player.py         # Random strategy (for testing)
│   ├── call_player.py           # Call strategy (for testing)
│   └── ...
├── game/                # Game engine
│   ├── game.py         # Main game program
│   ├── players.py       # Base player class
│   └── engine/          # Core game engine modules
├── start_game.py        # Quick start game script
├── evaluation.py        # Evaluation script
├── final_evaluation.py  # Final evaluation script
└── requirement.txt      # Dependency list
```

## Features

### Implemented AI Strategies

1. **ExpectationPlayer** (`agents/expectation_player.py`)
   - Decision strategy based on expected value calculations
   - Uses hand win rate estimation to calculate expected values for different actions
   - Considers pot size, bet amounts, and other factors

2. **MCTPlayer** (`agents/MCT_player.py`)
   - Monte Carlo Tree Search (MCTS) strategy
   - Evaluates optimal actions through simulation

3. **InfoPlayer Series** (`agents/Info_player*.py`)
   - Information theory-based strategies
   - Multiple improved versions (Info_player, Info_player2, Info_player2_5, Info_player3)

4. **Other Strategies**
   - `just_win_player.py`: Only bets when win rate is sufficiently high
   - `One_Shot.py`: One-shot decision strategy
   - `baseline_agent.py`: Baseline strategy

### Game Engine

- Complete Texas Hold'em rules implementation
- Multi-player support
- Complete game state management
- Hand evaluation system

## Installation & Setup

### Requirements

- Python 3.8+
- Required Python packages (see `requirement.txt`)

### Installation Steps

1. Clone or download the project:
```bash
cd final_project-1
```

2. Install dependencies:
```bash
pip install -r requirement.txt
```

## Usage

### Quick Start Game

Run `start_game.py` to play a game:

```bash
python start_game.py
```

You can modify player configuration in `start_game.py`:

```python
config = setup_config(max_round=20, initial_stack=1000, small_blind_amount=5)
config.register_player(name="p1", algorithm=baseline7_ai())
config.register_player(name="p2_INFO3", algorithm=info3_ai())
```

### Evaluate AI Performance

Run the evaluation script to test different AI performances:

```bash
python evaluation.py
```

Or use the final evaluation script:

```bash
python final_evaluation.py
```

### Implement Your Own AI Player

To implement your own AI player, you need to inherit from the `BasePokerPlayer` class and implement the following methods:

```python
from game.players import BasePokerPlayer

class MyPlayer(BasePokerPlayer):
    def declare_action(self, valid_actions, hole_card, round_state):
        # Implement decision logic
        # Return (action, amount)
        # action: 'fold', 'call', 'raise'
        pass
    
    def receive_game_start_message(self, game_info):
        # Receive game start message
        pass
    
    def receive_round_start_message(self, round_count, hole_card, seats):
        # Receive round start message
        pass
    
    def receive_street_start_message(self, street, round_state):
        # Receive street start message (preflop, flop, turn, river)
        pass
    
    def receive_game_update_message(self, new_action, round_state):
        # Receive game update message (other players' actions)
        pass
    
    def receive_round_result_message(self, winners, hand_info, round_state):
        # Receive round result message
        pass

def setup_ai():
    return MyPlayer()
```

For detailed message format specifications, please refer to `data_flow.md`.

## Key Modules

### `agents/hand_strength.py`

Provides hand strength calculation functionality:

- `win_rate(hole_card, community_cards, simulations=2000)`: Calculate hand win rate
- `classify_hand(cards)`: Classify hand type (straight flush, four of a kind, full house, etc.)
- `compare_hands_wrapper(my_hole, opp_hole, community)`: Compare two hands

### `game/game.py`

Main game program:

- `setup_config()`: Configure game settings
- `start_poker()`: Start the game

### `game/players.py`

Defines the `BasePokerPlayer` base class that all AI players need to inherit from.

## Game Rules

- **Game Type**: Texas Hold'em
- **Default Settings**:
  - Max rounds: 20
  - Initial stack: 1000
  - Small blind: 5
  - Big blind: 10

These parameters can be adjusted in `setup_config()`.

## Evaluation Metrics

The evaluation script calculates the following metrics:

- **Win Rate**: Win rate against different baseline AIs
- **Stack Change**: Chip difference at the end of the game
- **Tie Rate**: Proportion of ties

## File Descriptions

- `start_game.py`: Quick start for a single game
- `evaluation.py`: Batch evaluation of different AI performances
- `final_evaluation.py`: Final evaluation script (includes more detailed statistics)
- `confidence_interval.py`: Calculate confidence intervals
- `data_flow.md`: Detailed message format specification document

## Notes

1. Some baseline players are compiled `.so` files (baseline0-7), ensure these files are in the correct location
2. AI decisions have a time limit (50 seconds), exceeding the limit will automatically fold
3. Hand strength calculation uses Monte Carlo simulation, the number of simulations can be adjusted

## License

Please refer to the `LICENSE.md` file.

## Author

Project ID: b10202064

## References

- Texas Hold'em rules
- Monte Carlo Tree Search algorithm
- Information theory applications in game AI
