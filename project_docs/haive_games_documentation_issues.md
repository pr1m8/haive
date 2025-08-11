# Haive-Games Documentation Build Issues

This document lists all identified issues in the haive-games package that could cause documentation build failures.

## Summary

- **95 files** with module-level instantiations or function calls
- **19 empty Python files** that need content or removal
- Various TypeVar instantiations that may need review

## Empty Files (19 files)

These files are completely empty and may cause import issues:

- [ ] `packages/haive-games/src/haive/games/cards/standard/bs/prompts.py`
- [ ] `packages/haive-games/src/haive/games/core/base/state.py`
- [ ] `packages/haive-games/src/haive/games/core/base/engines.py`
- [ ] `packages/haive-games/src/haive/games/core/base/state_manager.py`
- [ ] `packages/haive-games/src/haive/games/core/base/models.py`
- [ ] `packages/haive-games/src/haive/games/core/base/player.py`
- [ ] `packages/haive-games/src/haive/games/base_v2/state.py`
- [ ] `packages/haive-games/src/haive/games/base_v2/player_agent.py`
- [ ] `packages/haive-games/src/haive/games/base_v2/models.py`
- [ ] `packages/haive-games/src/haive/games/single_player/rubiks/state.py`
- [ ] `packages/haive-games/src/haive/games/single_player/config.py`
- [ ] `packages/haive-games/src/haive/games/single_player/wordle/engines.py`
- [ ] `packages/haive-games/src/haive/games/single_player/towers_of_hanoi/postiition.py` (Note: typo in filename)
- [ ] `packages/haive-games/src/haive/games/single_player/towers_of_hanoi/container.py`
- [ ] `packages/haive-games/src/haive/games/single_player/towers_of_hanoi/piece.py`
- [ ] `packages/haive-games/src/haive/games/single_player/twenty_fourty_eight/game/piece.py`
- [ ] `packages/haive-games/src/haive/games/single_player/crossword_puzzle/game/cell.py`
- [ ] `packages/haive-games/src/haive/games/single_player/word_search/base.py`
- [ ] `packages/haive-games/src/haive/games/single_player/testing/base.py`

## Module-Level Instantiations (95 files)

### Critical Issues - Function/Method Calls

These are module-level function or method calls that execute code during import:

- [ ] `haive/games/battleship/debug.py:27` - `install()` - Rich traceback install
- [ ] `haive/games/benchmark.py:21` - `insert()` - sys.path manipulation
- [ ] `haive/games/benchmark.py:25` - `basicConfig()` - Logging configuration
- [ ] `haive/games/checkers/example.py:38` - `basicConfig()` - Logging configuration
- [ ] `haive/games/clue/example.py:48` - `basicConfig()` - Logging configuration
- [ ] `haive/games/common/voting_system.py:21` - `setLevel()` - Logger level setting
- [ ] `haive/games/connect4/example.py:83` - `basicConfig()` - Logging configuration
- [ ] `haive/games/debate/test_topic_handling.py:12` - `basicConfig()` - Logging configuration
- [ ] `haive/games/debate/test_topic_handling.py:21` - `setLevel()` - Logger level setting
- [ ] `haive/games/debate_v2/agent.py:20` - `setLevel()` - Logger level setting
- [ ] `haive/games/debate_v2/agent_with_judges.py:26` - `setLevel()` - Logger level setting
- [ ] `haive/games/debate_v2/example.py:14` - `basicConfig()` - Logging configuration
- [ ] `haive/games/debate_v2/example_with_judges.py:23` - `basicConfig()` - Logging configuration
- [ ] `haive/games/debate_v2/judges.py:19` - `setLevel()` - Logger level setting
- [ ] `haive/games/debate_v2/simple_test.py:20` - `basicConfig()` - Logging configuration
- [ ] `haive/games/debate_v2/test_judges.py:16` - `basicConfig()` - Logging configuration
- [ ] `haive/games/fox_and_geese/example.py:15` - `basicConfig()` - Logging configuration
- [ ] `haive/games/fox_and_geese/fixed_runner.py:20` - `basicConfig()` - Logging configuration
- [ ] `haive/games/go/example.py:12` - `print()` - Direct print statement
- [ ] `haive/games/hold_em/example.py:31` - `basicConfig()` - Logging configuration
- [ ] `haive/games/hold_em/game_agent.py:57` - `basicConfig()` - Logging configuration
- [ ] `haive/games/mafia/example.py:45` - `basicConfig()` - Logging configuration
- [ ] `haive/games/mafia/mock_runner.py:36` - `basicConfig()` - Logging configuration
- [ ] `haive/games/mafia/simple_runner.py:29` - `basicConfig()` - Logging configuration
- [ ] `haive/games/mafia/verify_imports.py:10,33,41` - `print()` - Direct print statements
- [ ] `haive/games/mastermind/demo.py:21` - `basicConfig()` - Logging configuration
- [ ] `haive/games/monopoly/example.py:18` - `basicConfig()` - Logging configuration
- [ ] `haive/games/monopoly/game/game.py:15` - `basicConfig()` - Logging configuration
- [ ] `haive/games/monopoly/run_game.py:14` - `basicConfig()` - Logging configuration
- [ ] `haive/games/nim/example.py:35` - `basicConfig()` - Logging configuration
- [ ] `haive/games/nim/standalone_game.py:22` - `basicConfig()` - Logging configuration
- [ ] `haive/games/nim/ui.py:32` - `basicConfig()` - Logging configuration
- [ ] `haive/games/poker/example.py:56` - `basicConfig()` - Logging configuration
- [ ] `haive/games/risk/example.py:16` - `basicConfig()` - Logging configuration

### High Priority - Factory/Engine Instantiations

These create singleton instances at module level:

- [ ] `haive/games/among_us/generic_engines.py:146` - `among_us_factory = AmongUsEngineFactory()`
- [ ] `haive/games/battleship/generic_engines.py:115` - `battleship_factory = BattleshipEngineFactory()`
- [ ] `haive/games/checkers/generic_engines.py:132-134` - Multiple factory instantiations
- [ ] `haive/games/chess/generic_engines.py:123-125` - Multiple factory instantiations
- [ ] `haive/games/clue/generic_engines.py:112` - `clue_factory = ClueEngineFactory()`
- [ ] `haive/games/connect4/generic_engines.py:113-115` - Multiple factory instantiations
- [ ] `haive/games/debate/generic_engines.py:113` - `debate_factory = DebateEngineFactory()`
- [ ] `haive/games/dominoes/generic_engines.py:112` - `dominoes_factory = DominoesEngineFactory()`
- [ ] `haive/games/fox_and_geese/generic_engines.py:113` - `fox_and_geese_factory = FoxAndGeeseEngineFactory()`
- [ ] `haive/games/hold_em/generic_engines.py:134` - `holdem_factory = HoldemEngineFactory()`
- [ ] `haive/games/mafia/generic_engines.py:112` - `mafia_factory = MafiaEngineFactory()`
- [ ] `haive/games/mancala/generic_engines.py:113` - `mancala_factory = MancalaEngineFactory()`
- [ ] `haive/games/mastermind/generic_engines.py:112` - `mastermind_factory = MastermindEngineFactory()`
- [ ] `haive/games/monopoly/generic_engines.py:157` - `monopoly_factory = MonopolyEngineFactory()`
- [ ] `haive/games/nim/generic_engines.py:113` - `nim_factory = NimEngineFactory()`
- [ ] `haive/games/poker/generic_engines.py:113` - `poker_factory = PokerEngineFactory()`
- [ ] `haive/games/reversi/generic_engines.py:113` - `reversi_factory = ReversiEngineFactory()`
- [ ] `haive/games/risk/generic_engines.py:113` - `risk_factory = RiskEngineFactory()`
- [ ] `haive/games/tic_tac_toe/generic_engines.py:111-113` - Multiple factory instantiations

### Medium Priority - Console/App Instantiations

These create UI or application instances:

- [ ] `haive/games/battleship/debug.py:28` - `console = Console()`
- [ ] `haive/games/battleship/example.py:37` - `console = Console()`
- [ ] `haive/games/connect4/example.py:80` - `console = Console()`
- [ ] `haive/games/monopoly/simple_demo.py:29` - `console = Console()`
- [ ] `haive/games/single_player/towers_of_hanoi/ui.py:15` - `console = Console()`
- [ ] `haive/games/tic_tac_toe/example.py:70` - `console = Console()`
- [ ] `haive/games/chess/api_example.py:27` - `app = FastAPI()`

### Low Priority - TypeVar Instantiations

These are type variable declarations (generally safe but worth reviewing):

- [ ] Multiple files with `T = TypeVar()`, `TMove = TypeVar()`, etc. (44 instances)

### Special Cases

- [ ] `haive/games/cards/standard/blackjack/factory.py:115` - `final_state = run_blackjack_game()` - Game execution at import
- [ ] `haive/games/debate_v2/__init__.py:7` - `DebateV2AgentConfig = type()` - Dynamic type creation
- [ ] `haive/games/mafia/aug_llms.py:172-175` - Multiple analyzer instantiations
- [ ] `haive/games/poker/engines.py:240` - `poker_agent_configs = create_poker_agent_configs()` - Config creation

## Recommendations

1. **Empty Files**: Either add content (even just docstrings) or remove these files
2. **Module-Level Function Calls**: Move all `basicConfig()`, `setLevel()`, `print()` calls inside functions or `if __name__ == "__main__":` blocks
3. **Factory Instantiations**: Consider lazy initialization or factory functions instead of module-level instances
4. **Console Instantiations**: Move inside functions or classes
5. **TypeVar**: These are generally safe but should be reviewed for proper usage

## Priority Order

1. Fix empty files (add content or remove)
2. Fix module-level function calls (especially logging configuration)
3. Fix factory instantiations (use lazy initialization)
4. Fix console instantiations
5. Review TypeVar usage
