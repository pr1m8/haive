# haive-games Documentation Report

## Package Overview

- **Package Path**: /home/will/Projects/haive/backend/haive/packages/haive-games
- **Has Main **init**.py**: ❌
- **Has README**: ✅
- **Has Examples**: ✅
- **Total Issues**: 1203

## Missing Example Files

- games/core/agent

## Issues by File

### src/haive/games/benchmark.py

- 🔵 **Line 32**: Function 'run_monopoly_benchmark' missing type hints
- 🔵 **Line 57**: Function 'run_poker_benchmark' missing type hints
- 🔵 **Line 82**: Function 'main' missing type hints

### src/haive/games/clue/state.py

- 🔵 **Line 50**: Method 'ClueState.current_turn_number' missing type hints
- 🔵 **Line 55**: Method 'ClueState.is_game_over' missing type hints
- 🔵 **Line 60**: Method 'ClueState.board_string' missing type hints
- 🔵 **Line 73**: Method 'ClueState.initialize' missing type hints

### src/haive/games/clue/engines.py

- 🔵 **Line 11**: Function 'generate_player_prompt' missing type hints
- 🔵 **Line 43**: Function 'generate_analysis_prompt' missing type hints

### src/haive/games/clue/state_manager.py

- 🔵 **Line 18**: Method 'ClueStateManager.initialize' missing type hints

### src/haive/games/clue/models.py

- 🔵 **Line 112**: Method 'ClueCard.to_dict' missing type hints
- 🔵 **Line 125**: Method 'ClueSolution.to_dict' missing type hints
- 🔵 **Line 142**: Method 'ClueGuess.to_dict' missing type hints
- 🔵 **Line 159**: Method 'ClueResponse.to_dict' missing type hints
- 🔵 **Line 199**: Method 'ClueHypothesis.to_dict' missing type hints

### src/haive/games/clue/configurable_config.py

- 🔵 **Line 251**: Function 'create_budget_clue_config' missing type hints
- 🔵 **Line 256**: Function 'create_advanced_clue_config' missing type hints
- 🔵 **Line 261**: Function 'create_experimental_clue_config' missing type hints
- 🔵 **Line 307**: Function 'list_example_configurations' missing type hints

### src/haive/games/clue/controller.py

- 🔵 **Line 116**: Method 'ClueGameController.get_game_state' missing type hints
- 🔵 **Line 218**: Method 'ClueGameController.generate_board_string' missing type hints

### src/haive/games/clue/generic_engines.py

- 🔴 **Line 1**: Could not parse file: unexpected character after line continuation character (<unknown>, line 49)

### src/haive/games/clue/example.py

- 🔵 **Line 51**: Function 'run_clue_game' missing type hints

### src/haive/games/checkers/state.py

- 🔵 **Line 186**: Method 'CheckersState.initialize' missing type hints

### src/haive/games/checkers/engines.py

- 🔵 **Line 160**: Function 'build_checkers_aug_llms' missing type hints

### src/haive/games/checkers/state_manager.py

- 🔵 **Line 44**: Method 'CheckersStateManager.initialize' missing type hints

### src/haive/games/checkers/config.py

- 🔵 **Line 78**: Method 'CheckersAgentConfig.default' missing type hints

### src/haive/games/checkers/configurable_config.py

- 🔵 **Line 253**: Function 'create_budget_checkers_config' missing type hints
- 🔵 **Line 258**: Function 'create_competitive_checkers_config' missing type hints
- 🔵 **Line 263**: Function 'create_experimental_checkers_config' missing type hints
- 🔵 **Line 309**: Function 'list_example_configurations' missing type hints

### src/haive/games/checkers/ui.py

- 🔵 **Line 602**: Method 'CheckersUI.display_state' missing type hints
- 🔵 **Line 638**: Method 'CheckersUI.show_thinking' missing type hints
- 🔵 **Line 662**: Method 'CheckersUI.show_move' missing type hints
- 🔵 **Line 688**: Method 'CheckersUI.show_game_over' missing type hints

### src/haive/games/checkers/generic_engines.py

- 🔵 **Line 119**: Method 'CheckersPromptGenerator.get_move_output_model' missing type hints
- 🔵 **Line 123**: Method 'CheckersPromptGenerator.get_analysis_output_model' missing type hints
- 🔵 **Line 246**: Function 'compare_checkers_with_other_games' missing type hints
- 🔵 **Line 310**: Function 'create_multi_game_checkers_demo' missing type hints

### src/haive/games/checkers/agent.py

- 🔵 **Line 459**: Method 'CheckersAgent.run_game_with_ui' missing type hints
- 🔵 **Line 521**: Method 'CheckersAgent.setup_workflow' missing type hints

### src/haive/games/checkers/example.py

- 🔵 **Line 23**: Function 'run_example_game' missing type hints

### src/haive/games/mastermind/state.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 47**: Method 'MastermindState.initialize' missing docstring
- 🔵 **Line 78**: Method 'MastermindState.current_turn_number' missing type hints
- 🔵 **Line 84**: Method 'MastermindState.turns_remaining' missing type hints
- 🔵 **Line 90**: Method 'MastermindState.is_game_over' missing type hints
- 🔵 **Line 96**: Method 'MastermindState.last_guess' missing type hints
- 🔵 **Line 102**: Method 'MastermindState.last_feedback' missing type hints
- 🔵 **Line 108**: Method 'MastermindState.board_string' missing type hints

### src/haive/games/mastermind/engines.py

- 🔵 **Line 14**: Function 'generate_codemaker_prompt' missing type hints

### src/haive/games/mastermind/state_manager.py

- 🔵 **Line 29**: Method 'MastermindStateManager.initialize' missing type hints

### src/haive/games/mastermind/config.py

- 🔵 **Line 55**: Method 'MastermindConfig.default_config' missing type hints

### src/haive/games/mastermind/models.py

- 🔵 **Line 69**: Method 'MastermindFeedback.is_winning' missing type hints

### src/haive/games/mastermind/configurable_config.py

- 🔵 **Line 255**: Function 'create_budget_mastermind_config' missing type hints
- 🔵 **Line 260**: Function 'create_advanced_mastermind_config' missing type hints
- 🔵 **Line 265**: Function 'create_experimental_mastermind_config' missing type hints
- 🔵 **Line 311**: Function 'list_example_configurations' missing type hints

### src/haive/games/mastermind/ui.py

- 🔵 **Line 57**: Method 'MastermindUI.display_welcome' missing type hints
- 🔵 **Line 261**: Method 'MastermindUI.display_game_state' missing type hints
- 🔵 **Line 270**: Method 'MastermindUI.display_final_results' missing type hints
- 🔵 **Line 324**: Method 'MastermindUI.print_debug_info' missing type hints

### src/haive/games/mastermind/demo.py

- 🔵 **Line 61**: Method 'MastermindState.is_game_over' missing type hints
- 🔵 **Line 333**: Function 'main' missing type hints
- 🔵 **Line 232**: Method 'MastermindUI.display_game_state' missing type hints
- 🔵 **Line 262**: Method 'MastermindUI.show_result' missing type hints
- 🔵 **Line 285**: Method 'MastermindUI.display_game_state' missing type hints
- 🔵 **Line 328**: Method 'MastermindUI.show_result' missing type hints

### src/haive/games/mastermind/generic_engines.py

- 🔵 **Line 200**: Function 'create_advanced_mastermind_engines' missing type hints
- 🔵 **Line 205**: Function 'create_budget_mastermind_engines' missing type hints
- 🔵 **Line 210**: Function 'create_mixed_mastermind_engines' missing type hints

### src/haive/games/mastermind/agent.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 494**: Method 'MastermindAgent.setup_workflow' missing type hints

### src/haive/games/mastermind/example.py

- 🔵 **Line 16**: Function 'parse_args' missing type hints
- 🔵 **Line 52**: Function 'main' missing type hints

### src/haive/games/mafia/state.py

- 🔵 **Line 160**: Method 'MafiaGameState.update_alive_counts' missing type hints
- 🔵 **Line 274**: Method 'MafiaGameState.model_copy' missing type hints
- 🟡 **Line 157**: Class 'Config' missing docstring

### src/haive/games/mafia/engines.py

- 🔵 **Line 31**: Function 'generate_villager_prompt' missing type hints
- 🔵 **Line 81**: Function 'generate_mafia_prompt' missing type hints
- 🔵 **Line 131**: Function 'generate_detective_prompt' missing type hints
- 🔵 **Line 181**: Function 'generate_doctor_prompt' missing type hints
- 🔵 **Line 231**: Function 'generate_narrator_prompt' missing type hints

### src/haive/games/mafia/simple_demo.py

- 🔵 **Line 16**: Function 'run_simple_demo' missing type hints
- 🔵 **Line 137**: Function 'visualize_state' missing type hints

### src/haive/games/mafia/models.py

- 🔵 **Line 158**: Method 'MafiaAction.to_dict' missing type hints
- 🟡 **Line 123**: Class 'Config' missing docstring
- 🟡 **Line 226**: Class 'Config' missing docstring
- 🟡 **Line 263**: Class 'Config' missing docstring
- 🟡 **Line 287**: Class 'Config' missing docstring
- 🟡 **Line 325**: Class 'Config' missing docstring
- 🟡 **Line 386**: Class 'Config' missing docstring

### src/haive/games/mafia/mock_runner.py

- 🔵 **Line 308**: Method 'MockEngine.invoke' missing type hints
- 🔵 **Line 632**: Function 'main' missing type hints

### src/haive/games/mafia/configurable_config.py

- 🔵 **Line 245**: Function 'create_budget_mafia_config' missing type hints
- 🔵 **Line 250**: Function 'create_advanced_mafia_config' missing type hints
- 🔵 **Line 255**: Function 'create_experimental_mafia_config' missing type hints
- 🔵 **Line 301**: Function 'list_example_configurations' missing type hints

### src/haive/games/mafia/generic_engines.py

- 🔴 **Line 1**: Could not parse file: unexpected character after line continuation character (<unknown>, line 48)

### src/haive/games/mafia/agent.py

- 🔵 **Line 454**: Method 'MafiaAgent.extract_move' missing type hints
- 🔵 **Line 1106**: Method 'MafiaAgent.visualize_state' missing type hints

### src/haive/games/mafia/example.py

- 🔵 **Line 261**: Function 'main' missing type hints

### src/haive/games/mafia/simple_runner.py

- 🔵 **Line 317**: Function 'main' missing type hints

### src/haive/games/dominoes/state.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 43**: Method 'DominoesState.left_value' missing type hints
- 🔵 **Line 50**: Method 'DominoesState.right_value' missing type hints
- 🔵 **Line 57**: Method 'DominoesState.board_string' missing type hints
- 🔵 **Line 72**: Method 'DominoesState.initialize' missing type hints

### src/haive/games/dominoes/enhanced_example.py

- 🔵 **Line 20**: Function 'run_dominoes_game' missing type hints
- 🔵 **Line 90**: Function 'demo_ui_features' missing type hints

### src/haive/games/dominoes/engines.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/games/dominoes/state_manager.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/games/dominoes/config.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 30**: Method 'DominoesAgentConfig.default_config' missing docstring
- 🔵 **Line 30**: Method 'DominoesAgentConfig.default_config' missing type hints

### src/haive/games/dominoes/models.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 12**: Method 'DominoTile.is_double' missing type hints
- 🔵 **Line 16**: Method 'DominoTile.sum' missing type hints
- 🔵 **Line 20**: Method 'DominoTile.reversed' missing type hints

### src/haive/games/dominoes/configurable_config.py

- 🔵 **Line 249**: Function 'create_budget_dominoes_config' missing type hints
- 🔵 **Line 254**: Function 'create_advanced_dominoes_config' missing type hints
- 🔵 **Line 259**: Function 'create_experimental_dominoes_config' missing type hints
- 🔵 **Line 305**: Function 'list_example_configurations' missing type hints

### src/haive/games/dominoes/ui.py

- 🔵 **Line 499**: Method 'DominoesUI.display_welcome' missing type hints

### src/haive/games/dominoes/generic_engines.py

- 🔴 **Line 1**: Could not parse file: unexpected character after line continuation character (<unknown>, line 49)

### src/haive/games/dominoes/agent.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 702**: Method 'DominoesAgent.setup_workflow' missing type hints

### src/haive/games/dominoes/example.py

- 🔵 **Line 16**: Function 'run_dominoes_game' missing type hints

### src/haive/games/dominoes/rich_ui.py

- 🔵 **Line 789**: Method 'DominoesRichUI.display_welcome' missing type hints
- 🔵 **Line 965**: Method 'DominoesRichUI.run_game_with_ui' missing type hints

### src/haive/games/base/state.py

- 🔵 **Line 56**: Method 'GameState.initialize' missing type hints
- 🟡 **Line 51**: Class 'Config' missing docstring

### src/haive/games/base/state_manager.py

- 🔵 **Line 53**: Method 'GameStateManager.initialize' missing type hints

### src/haive/games/base/models.py

- 🔵 **Line 52**: Method 'MoveModel.validate_move' missing type hints

### src/haive/games/base/utils.py

- 🔵 **Line 22**: Function 'run_game' missing type hints

### src/haive/games/base/agent.py

- 🔵 **Line 66**: Method 'GameAgent.setup_workflow' missing type hints
- 🔵 **Line 449**: Function 'run_game' missing type hints

### src/haive/games/monopoly/state.py

- 🔵 **Line 98**: Method 'MonopolyState.current_player' missing type hints
- 🔵 **Line 117**: Method 'MonopolyState.active_players' missing type hints
- 🔵 **Line 123**: Method 'MonopolyState.bankrupt_players' missing type hints
- 🔵 **Line 169**: Method 'MonopolyState.next_player' missing type hints
- 🔵 **Line 266**: Method 'MonopolyState.to_dict' missing type hints
- 🔵 **Line 312**: Method 'MonopolyState.validate_state_consistency' missing type hints

### src/haive/games/monopoly/engines.py

- 🔵 **Line 149**: Function 'build_monopoly_player_aug_llms' missing type hints

### src/haive/games/monopoly/player_agent.py

- 🔵 **Line 67**: Method 'PlayerDecisionState.decision' missing type hints
- 🔵 **Line 179**: Method 'MonopolyGameAgentConfig.create_initial_state' missing type hints
- 🔵 **Line 222**: Method 'MonopolyGameAgentConfig.create_player_agent' missing type hints
- 🔵 **Line 235**: Method 'MonopolyGameAgentConfig.setup_player_agent_engines' missing type hints
- 🔵 **Line 264**: Method 'MonopolyPlayerAgent.setup_workflow' missing type hints
- 🟡 **Line 111**: Class 'Config' missing docstring

### src/haive/games/monopoly/config.py

- 🔵 **Line 116**: Method 'MonopolyGameAgentConfig.create_initial_state' missing type hints
- 🔵 **Line 159**: Method 'MonopolyGameAgentConfig.create_player_agent' missing type hints
- 🔵 **Line 172**: Method 'MonopolyGameAgentConfig.setup_player_agent_engines' missing type hints
- 🟡 **Line 44**: Class 'Config' missing docstring

### src/haive/games/monopoly/simple_demo.py

- 🔵 **Line 31**: Function 'print_divider' missing type hints
- 🔵 **Line 36**: Function 'print_property' missing type hints
- 🔵 **Line 61**: Function 'print_player_status' missing type hints
- 🔵 **Line 99**: Function 'print_recent_events' missing type hints
- 🔵 **Line 321**: Function 'run_demo' missing type hints

### src/haive/games/monopoly/models.py

- 🔵 **Line 84**: Method 'PropertyDecision.validate_property_action' missing type hints
- 🔵 **Line 100**: Method 'JailDecision.validate_jail_action' missing type hints
- 🔵 **Line 126**: Method 'BuildingDecision.validate_building_action' missing type hints
- 🔵 **Line 134**: Method 'BuildingDecision.validate_quantity' missing type hints
- 🔵 **Line 175**: Method 'TradeResponse.validate_trade_action' missing type hints
- 🔵 **Line 233**: Method 'DiceRoll.total' missing type hints
- 🔵 **Line 238**: Method 'DiceRoll.is_doubles' missing type hints
- 🔵 **Line 261**: Method 'Property.current_rent' missing type hints

### src/haive/games/monopoly/standalone_demo.py

- 🟡 **Line 16**: Class 'PropertyType' missing docstring
- 🟡 **Line 23**: Class 'PropertyColor' missing docstring
- 🟡 **Line 39**: Class 'Property' missing docstring
- 🟡 **Line 55**: Class 'Player' missing docstring
- 🔵 **Line 66**: Method 'Player.can_afford' missing docstring
- 🟡 **Line 71**: Class 'DiceRoll' missing docstring
- 🔵 **Line 76**: Method 'DiceRoll.total' missing docstring
- 🔵 **Line 76**: Method 'DiceRoll.total' missing type hints
- 🔵 **Line 80**: Method 'DiceRoll.is_doubles' missing docstring
- 🔵 **Line 80**: Method 'DiceRoll.is_doubles' missing type hints
- 🟡 **Line 85**: Class 'GameEvent' missing docstring
- 🟡 **Line 95**: Class 'GameState' missing docstring
- 🔵 **Line 104**: Method 'GameState.current_player' missing docstring
- 🔵 **Line 104**: Method 'GameState.current_player' missing type hints
- 🔵 **Line 112**: Method 'GameState.active_players' missing docstring
- 🔵 **Line 112**: Method 'GameState.active_players' missing type hints
- 🔵 **Line 115**: Method 'GameState.next_player' missing docstring
- 🔵 **Line 115**: Method 'GameState.next_player' missing type hints
- 🔵 **Line 247**: Function 'create_board' missing type hints
- 🔵 **Line 291**: Function 'roll_dice' missing type hints
- 🟡 **Line 362**: Class 'Color' missing docstring
- 🔵 **Line 374**: Function 'print_divider' missing type hints
- 🔵 **Line 379**: Function 'print_property' missing type hints
- 🔵 **Line 405**: Function 'print_player_status' missing type hints
- 🔵 **Line 443**: Function 'print_recent_events' missing type hints
- 🔵 **Line 669**: Function 'run_demo' missing type hints

### src/haive/games/monopoly/configurable_config.py

- 🔵 **Line 262**: Function 'create_budget_monopoly_config' missing type hints
- 🔵 **Line 267**: Function 'create_real_estate_mogul_monopoly_config' missing type hints
- 🔵 **Line 272**: Function 'create_property_tycoon_monopoly_config' missing type hints
- 🔵 **Line 277**: Function 'create_experimental_monopoly_config' missing type hints
- 🔵 **Line 327**: Function 'list_example_configurations' missing type hints

### src/haive/games/monopoly/ui.py

- 🔵 **Line 52**: Method 'MonopolyRichUI.render_header' missing type hints
- 🔵 **Line 69**: Method 'MonopolyRichUI.render_footer' missing type hints
- 🔵 **Line 100**: Method 'MonopolyRichUI.render_board' missing type hints
- 🔵 **Line 157**: Method 'MonopolyRichUI.render_current_player' missing type hints
- 🔵 **Line 194**: Method 'MonopolyRichUI.render_players' missing type hints
- 🔵 **Line 240**: Method 'MonopolyRichUI.render_recent_events' missing type hints
- 🔵 **Line 310**: Method 'MonopolyRichUI.run' missing type hints
- 🔵 **Line 380**: Function 'main' missing type hints

### src/haive/games/monopoly/generic_engines.py

- 🔵 **Line 229**: Function 'create_real_estate_mogul_monopoly_engines' missing type hints
- 🔵 **Line 234**: Function 'create_budget_monopoly_engines' missing type hints
- 🔵 **Line 239**: Function 'create_property_tycoon_monopoly_engines' missing type hints
- 🔵 **Line 244**: Function 'create_mixed_monopoly_engines' missing type hints

### src/haive/games/monopoly/utils.py

- 🔵 **Line 388**: Function 'create_board' missing type hints
- 🔵 **Line 434**: Function 'roll_dice' missing type hints
- 🔵 **Line 513**: Function 'shuffle_cards' missing type hints

### src/haive/games/monopoly/run_game.py

- 🔵 **Line 11**: Function 'main' missing type hints

### src/haive/games/monopoly/game_agent.py

- 🔵 **Line 51**: Method 'MonopolyGameAgent.setup_workflow' missing type hints
- 🔵 **Line 408**: Method 'MonopolyGameAgent.offer_property_purchase' missing type hints
- 🔵 **Line 501**: Method 'MonopolyGameAgent.pay_rent' missing type hints
- 🟡 **Line 38**: Class 'Config' missing docstring

### src/haive/games/monopoly/example.py

- 🔵 **Line 21**: Function 'main' missing type hints
- 🔵 **Line 42**: Function 'run_manual_turn' missing type hints

### src/haive/games/monopoly/ui_fixed.py

- 🔵 **Line 51**: Method 'MonopolyRichUI.render_header' missing type hints
- 🔵 **Line 73**: Method 'MonopolyRichUI.render_footer' missing type hints
- 🔵 **Line 105**: Method 'MonopolyRichUI.render_board' missing type hints
- 🔵 **Line 151**: Method 'MonopolyRichUI.render_current_player' missing type hints
- 🔵 **Line 186**: Method 'MonopolyRichUI.render_players' missing type hints
- 🔵 **Line 220**: Method 'MonopolyRichUI.render_recent_events' missing type hints
- 🔵 **Line 290**: Method 'MonopolyRichUI.run' missing type hints
- 🔵 **Line 370**: Function 'main' missing type hints

### src/haive/games/monopoly/prompts.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 4**: Function 'generate_move_decision_prompt' missing type hints
- 🔵 **Line 38**: Function 'generate_property_decision_prompt' missing type hints
- 🔵 **Line 76**: Function 'generate_strategy_analysis_prompt' missing type hints
- 🔵 **Line 114**: Function 'generate_turn_decision_prompt' missing type hints

### src/haive/games/monopoly/main_agent.py

- 🔴 **Line 1**: Could not parse file: unterminated string literal (detected at line 161) (<unknown>, line 161)

### src/haive/games/hold_em/state.py

- 🔵 **Line 147**: Method 'HoldemState.active_players' missing type hints
- 🔵 **Line 153**: Method 'HoldemState.players_in_hand' missing type hints
- 🔵 **Line 163**: Method 'HoldemState.total_pot' missing type hints
- 🔵 **Line 170**: Method 'HoldemState.players_to_act' missing type hints
- 🔵 **Line 181**: Method 'HoldemState.current_player' missing type hints
- 🔵 **Line 202**: Method 'HoldemState.is_betting_complete' missing type hints
- 🔵 **Line 218**: Method 'HoldemState.advance_to_next_player' missing type hints

### src/haive/games/hold_em/engines.py

- 🔵 **Line 230**: Function 'build_holdem_game_engines' missing type hints
- 🔵 **Line 402**: Function 'prepare_situation_context' missing type hints
- 🔵 **Line 417**: Function 'prepare_hand_context' missing type hints
- 🔵 **Line 430**: Function 'prepare_opponent_context' missing type hints
- 🔵 **Line 442**: Function 'prepare_decision_context' missing type hints

### src/haive/games/hold_em/player_agent.py

- 🔵 **Line 209**: Method 'HoldemPlayerAgent.setup_workflow' missing type hints
- 🔵 **Line 1007**: Method 'HoldemPlayerAgent.save_debug_logs' missing type hints
- 🟡 **Line 119**: Class 'Config' missing docstring

### src/haive/games/hold_em/config.py

- 🔵 **Line 361**: Method 'HoldemGameSettings.to_game_config' missing type hints
- 🔵 **Line 486**: Function 'create_fallback_game_engines' missing type hints

### src/haive/games/hold_em/configurable_config.py

- 🔵 **Line 248**: Function 'create_budget_holdem_config' missing type hints
- 🔵 **Line 253**: Function 'create_poker_pro_holdem_config' missing type hints
- 🔵 **Line 258**: Function 'create_heads_up_holdem_config' missing type hints
- 🔵 **Line 263**: Function 'create_experimental_holdem_config' missing type hints
- 🔵 **Line 313**: Function 'list_example_configurations' missing type hints

### src/haive/games/hold_em/ui.py

- 🔵 **Line 67**: Method 'HoldemRichUI.render_header' missing type hints
- 🔵 **Line 87**: Method 'HoldemRichUI.render_footer' missing type hints
- 🔵 **Line 108**: Method 'HoldemRichUI.render_table' missing type hints
- 🔵 **Line 158**: Method 'HoldemRichUI.render_community_cards' missing type hints
- 🔵 **Line 206**: Method 'HoldemRichUI.render_pot_info' missing type hints
- 🔵 **Line 231**: Method 'HoldemRichUI.render_player_info' missing type hints
- 🔵 **Line 286**: Method 'HoldemRichUI.render_action_log' missing type hints
- 🔵 **Line 330**: Method 'HoldemRichUI.render_hand_history' missing type hints
- 🔵 **Line 357**: Method 'HoldemRichUI.render_game_stats' missing type hints
- 🔵 **Line 382**: Method 'HoldemRichUI.run' missing type hints
- 🔵 **Line 580**: Function 'main' missing type hints

### src/haive/games/hold_em/aug_llms.py

- 🔵 **Line 494**: Function 'get_table_dynamics_analyzer' missing type hints
- 🟡 **Line 472**: Class 'BluffDetectionResult' missing docstring

### src/haive/games/hold_em/generic_engines.py

- 🔵 **Line 221**: Function 'create_poker_pro_holdem_engines' missing type hints
- 🔵 **Line 226**: Function 'create_budget_holdem_engines' missing type hints
- 🔵 **Line 231**: Function 'create_heads_up_holdem_engines' missing type hints
- 🔵 **Line 236**: Function 'create_mixed_holdem_engines' missing type hints

### src/haive/games/hold_em/utils.py

- 🔵 **Line 15**: Function 'create_standard_deck' missing type hints

### src/haive/games/hold_em/game_agent.py

- 🔵 **Line 138**: Method 'HoldemGameAgent.setup_player_agents' missing type hints
- 🔵 **Line 175**: Method 'HoldemGameAgent.log_agent_config' missing type hints
- 🔵 **Line 210**: Method 'HoldemGameAgent.setup_workflow' missing type hints
- 🟡 **Line 97**: Class 'Config' missing docstring

### src/haive/games/hold_em/example.py

- 🔵 **Line 107**: Function 'run_example_game' missing type hints
- 🔵 **Line 173**: Function 'analyze_game_results' missing type hints
- 🔵 **Line 215**: Function 'main' missing type hints

### src/haive/games/hold_em/engine_logging.py

- 🔵 **Line 61**: Method 'EngineInvocationLogger.log_invocation_end' missing type hints
- 🔵 **Line 117**: Method 'EngineInvocationLogger.invocation_context' missing type hints
- 🔵 **Line 193**: Method 'EngineInvocationLogger.print_timing_summary' missing type hints
- 🔵 **Line 224**: Method 'EngineInvocationLogger.print_invocation_tree' missing type hints
- 🔵 **Line 279**: Method 'LoggedAugLLMConfig.create_runnable' missing type hints

### src/haive/games/nim/state.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 34**: Method 'NimState.board_string' missing type hints
- 🔵 **Line 43**: Method 'NimState.is_game_over' missing type hints
- 🔵 **Line 48**: Method 'NimState.stones_left' missing type hints
- 🔵 **Line 53**: Method 'NimState.nim_sum' missing type hints

### src/haive/games/nim/state_manager.py

- 🔵 **Line 21**: Method 'NimStateManager.initialize' missing type hints

### src/haive/games/nim/config.py

- 🔵 **Line 40**: Method 'NimConfig.default_config' missing type hints

### src/haive/games/nim/configurable_config.py

- 🔵 **Line 249**: Function 'create_budget_nim_config' missing type hints
- 🔵 **Line 254**: Function 'create_advanced_nim_config' missing type hints
- 🔵 **Line 259**: Function 'create_experimental_nim_config' missing type hints
- 🔵 **Line 305**: Function 'list_example_configurations' missing type hints

### src/haive/games/nim/ui.py

- 🔵 **Line 236**: Method 'NimUI.display_game_state' missing type hints

### src/haive/games/nim/standalone_game.py

- 🔵 **Line 55**: Method 'NimState.board_string' missing type hints
- 🔵 **Line 64**: Method 'NimState.is_game_over' missing type hints
- 🔵 **Line 69**: Method 'NimState.stones_left' missing type hints
- 🔵 **Line 74**: Method 'NimState.nim_sum' missing type hints
- 🔵 **Line 98**: Method 'NimUI.display_game_state' missing type hints
- 🔵 **Line 271**: Method 'NimUI.announce_winner' missing type hints
- 🔵 **Line 350**: Function 'parse_args' missing type hints
- 🔵 **Line 393**: Function 'main' missing type hints

### src/haive/games/nim/generic_engines.py

- 🔴 **Line 1**: Could not parse file: unexpected character after line continuation character (<unknown>, line 49)

### src/haive/games/nim/agent.py

- 🔵 **Line 424**: Method 'NimAgent.setup_workflow' missing type hints

### src/haive/games/nim/example.py

- 🔵 **Line 22**: Function 'parse_args' missing type hints
- 🔵 **Line 65**: Function 'main' missing type hints

### src/haive/games/multi_player/state.py

- 🔵 **Line 83**: Method 'MultiPlayerGameState.current_player' missing type hints
- 🔵 **Line 98**: Method 'MultiPlayerGameState.advance_player' missing type hints
- 🟡 **Line 79**: Class 'Config' missing docstring

### src/haive/games/multi_player/agent.py

- 🔵 **Line 114**: Method 'MultiPlayerGameAgent.setup_workflow' missing type hints

### src/haive/games/tic_tac_toe/state.py

- 🔵 **Line 92**: Method 'TicTacToeState.validate_board' missing type hints
- 🔵 **Line 121**: Method 'TicTacToeState.empty_cells' missing type hints
- 🔵 **Line 126**: Method 'TicTacToeState.is_board_full' missing type hints
- 🔵 **Line 131**: Method 'TicTacToeState.current_player_name' missing type hints
- 🔵 **Line 140**: Method 'TicTacToeState.board_string' missing type hints
- 🔵 **Line 161**: Method 'TicTacToeState.initialize' missing type hints

### src/haive/games/tic_tac_toe/state_manager.py

- 🔵 **Line 16**: Method 'TicTacToeStateManager.initialize' missing type hints

### src/haive/games/tic_tac_toe/config.py

- 🔵 **Line 54**: Method 'TicTacToeConfig.default_config' missing type hints

### src/haive/games/tic_tac_toe/configurable_config.py

- 🔵 **Line 241**: Function 'create_budget_ttt_config' missing type hints
- 🔵 **Line 246**: Function 'create_quick_ttt_config' missing type hints
- 🔵 **Line 251**: Function 'create_experimental_ttt_config' missing type hints
- 🔵 **Line 297**: Function 'list_example_configurations' missing type hints

### src/haive/games/tic_tac_toe/ui.py

- 🔵 **Line 266**: Method 'RichTicTacToeRunner.show_thinking_animation' missing type hints
- 🔵 **Line 400**: Method 'RichTicTacToeRunner.show_game_summary' missing type hints

### src/haive/games/tic_tac_toe/generic_engines.py

- 🔵 **Line 98**: Method 'TicTacToePromptGenerator.get_move_output_model' missing type hints
- 🔵 **Line 102**: Method 'TicTacToePromptGenerator.get_analysis_output_model' missing type hints
- 🔵 **Line 217**: Function 'compare_chess_vs_ttt_patterns' missing type hints
- 🔵 **Line 267**: Function 'create_multi_game_comparison' missing type hints

### src/haive/games/tic_tac_toe/agent.py

- 🔵 **Line 97**: Method 'TicTacToeAgent.make_move' missing type hints
- 🔵 **Line 180**: Method 'TicTacToeAgent.analyze_position' missing type hints
- 🔵 **Line 268**: Method 'TicTacToeAgent.setup_workflow' missing type hints
- 🔵 **Line 288**: Method 'TicTacToeAgent.run_game' missing type hints

### src/haive/games/tic_tac_toe/configurable_engines.py

- 🔵 **Line 93**: Function 'get_tic_tac_toe_role_definitions' missing type hints

### src/haive/games/tic_tac_toe/example.py

- 🔵 **Line 23**: Function 'main' missing type hints
- 🔵 **Line 81**: Function 'run_simple_game' missing type hints
- 🔵 **Line 116**: Function 'run_analysis_showcase' missing type hints

### src/haive/games/mancala/state.py

- 🔵 **Line 57**: Method 'MancalaState.validate_board' missing type hints
- 🔵 **Line 65**: Method 'MancalaState.handle_initialization_data' missing type hints
- 🔵 **Line 145**: Method 'MancalaState.handle_analysis_data' missing type hints
- 🔵 **Line 260**: Method 'MancalaState.player1_score' missing type hints
- 🔵 **Line 265**: Method 'MancalaState.player2_score' missing type hints
- 🔵 **Line 270**: Method 'MancalaState.board_string' missing type hints
- 🔵 **Line 290**: Method 'MancalaState.is_game_over' missing type hints
- 🔵 **Line 302**: Method 'MancalaState.get_winner' missing type hints
- 🔵 **Line 336**: Method 'MancalaState.copy' missing type hints
- 🔵 **Line 353**: Method 'MancalaState.model_dump' missing type hints

### src/haive/games/mancala/state_manager.py

- 🔵 **Line 22**: Method 'MancalaStateManager.initialize' missing type hints

### src/haive/games/mancala/config.py

- 🔵 **Line 38**: Method 'MancalaConfig.default_config' missing type hints

### src/haive/games/mancala/models.py

- 🔵 **Line 27**: Method 'MancalaMove.validate_pit_index' missing type hints

### src/haive/games/mancala/configurable_config.py

- 🔵 **Line 249**: Function 'create_budget_mancala_config' missing type hints
- 🔵 **Line 254**: Function 'create_advanced_mancala_config' missing type hints
- 🔵 **Line 259**: Function 'create_experimental_mancala_config' missing type hints
- 🔵 **Line 305**: Function 'list_example_configurations' missing type hints

### src/haive/games/mancala/generic_engines.py

- 🔵 **Line 200**: Function 'create_advanced_mancala_engines' missing type hints
- 🔵 **Line 205**: Function 'create_budget_mancala_engines' missing type hints
- 🔵 **Line 210**: Function 'create_mixed_mancala_engines' missing type hints

### src/haive/games/mancala/agent.py

- 🔵 **Line 535**: Method 'MancalaAgent.visualize_state' missing type hints
- 🔵 **Line 579**: Method 'MancalaAgent.setup_workflow' missing type hints

### src/haive/games/connect4/state.py

- 🔵 **Line 80**: Method 'Connect4State.board_string' missing type hints
- 🔵 **Line 166**: Method 'Connect4State.validate_board_dimensions' missing type hints
- 🔵 **Line 185**: Method 'Connect4State.initialize' missing type hints

### src/haive/games/connect4/engines.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/games/connect4/state_manager.py

- 🔵 **Line 43**: Method 'Connect4StateManager.initialize' missing type hints

### src/haive/games/connect4/factory.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 12**: Function 'run_connect4_game' missing type hints

### src/haive/games/connect4/configurable_config.py

- 🔵 **Line 117**: Method 'ConfigurableConnect4Config.configure_engines_and_names' missing type hints

### src/haive/games/connect4/generic_engines.py

- 🔵 **Line 102**: Method 'Connect4PromptGenerator.get_move_output_model' missing type hints
- 🔵 **Line 106**: Method 'Connect4PromptGenerator.get_analysis_output_model' missing type hints

### src/haive/games/connect4/example.py

- 🔵 **Line 43**: Function 'run_connect4_game' missing type hints

### src/haive/games/among_us/state.py

- 🟡 **Line 1**: Module missing docstring
- 🟡 **Line 22**: Class 'AmongUsState' missing docstring
- 🔵 **Line 43**: Method 'AmongUsState.get_alive_players' missing type hints
- 🔵 **Line 47**: Method 'AmongUsState.get_task_completion_percentage' missing type hints
- 🔵 **Line 58**: Method 'AmongUsState.check_win_condition' missing type hints
- 🔵 **Line 118**: Method 'AmongUsState.add_observation' missing type hints
- 🔵 **Line 126**: Method 'AmongUsState.add_observation_to_all_in_room' missing type hints
- 🔵 **Line 139**: Method 'AmongUsState.get_active_sabotage' missing type hints
- 🔵 **Line 150**: Method 'AmongUsState.set_player_cooldown' missing type hints
- 🔵 **Line 154**: Method 'AmongUsState.decrement_cooldowns' missing type hints
- 🔵 **Line 160**: Method 'AmongUsState.initialize_map' missing type hints

### src/haive/games/among_us/engines.py

- 🔵 **Line 24**: Function 'generate_crewmate_prompt' missing type hints
- 🔵 **Line 62**: Function 'generate_impostor_prompt' missing type hints
- 🔵 **Line 103**: Function 'generate_analysis_prompt' missing type hints
- 🔵 **Line 137**: Function 'build_among_us_aug_llms' missing type hints
- 🔵 **Line 183**: Function 'get_crewmate_engine' missing type hints
- 🔵 **Line 188**: Function 'get_impostor_engine' missing type hints
- 🔵 **Line 193**: Function 'get_analyzer_engine' missing type hints

### src/haive/games/among_us/state_manager.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/games/among_us/config.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 46**: Method 'AmongUsAgentConfig.set_defaults' missing type hints

### src/haive/games/among_us/models.py

- 🟡 **Line 1**: Module missing docstring
- 🟡 **Line 7**: Class 'PlayerRole' missing docstring
- 🟡 **Line 12**: Class 'TaskType' missing docstring
- 🟡 **Line 19**: Class 'TaskStatus' missing docstring
- 🟡 **Line 25**: Class 'Task' missing docstring
- 🟡 **Line 92**: Class 'PlayerState' missing docstring
- 🔵 **Line 104**: Method 'PlayerState.is_impostor' missing type hints
- 🔵 **Line 108**: Method 'PlayerState.is_crewmate' missing type hints
- 🔵 **Line 121**: Method 'PlayerState.can_use_vent' missing type hints
- 🟡 **Line 126**: Class 'SabotageType' missing docstring
- 🟡 **Line 134**: Class 'SabotageStatus' missing docstring
- 🔵 **Line 159**: Method 'SabotageEvent.is_critical' missing type hints
- 🔵 **Line 163**: Method 'SabotageEvent.is_resolved' missing type hints
- 🟡 **Line 168**: Class 'AmongUsGamePhase' missing docstring

### src/haive/games/among_us/factory.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/games/among_us/configurable_config.py

- 🔵 **Line 263**: Function 'create_budget_among_us_config' missing type hints
- 🔵 **Line 268**: Function 'create_detective_among_us_config' missing type hints
- 🔵 **Line 273**: Function 'create_experimental_among_us_config' missing type hints
- 🔵 **Line 319**: Function 'list_example_configurations' missing type hints

### src/haive/games/among_us/ui.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/games/among_us/enhanced_ui.py

- 🔵 **Line 1371**: Method 'EnhancedAmongUsUI.display_welcome' missing type hints
- 🔵 **Line 1558**: Method 'EnhancedAmongUsUI.run_among_us_game' missing type hints

### src/haive/games/among_us/demo.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 17**: Function 'run_among_us_demo' missing type hints
- 🔵 **Line 325**: Function 'format_action' missing type hints
- 🔵 **Line 365**: Function 'get_role_color' missing type hints
- 🔵 **Line 372**: Function 'process_player_turn' missing type hints
- 🔵 **Line 510**: Function 'process_player_turn_enhanced' missing type hints
- 🔵 **Line 606**: Function 'process_meeting_discussion' missing type hints
- 🔵 **Line 714**: Function 'process_meeting_discussion_enhanced' missing type hints
- 🔵 **Line 807**: Function 'process_voting_phase_enhanced' missing type hints
- 🔵 **Line 981**: Function 'process_voting_phase' missing type hints
- 🔵 **Line 1122**: Function 'process_random_events_enhanced' missing type hints
- 🔵 **Line 1221**: Function 'process_random_events' missing type hints

### src/haive/games/among_us/generic_engines.py

- 🔵 **Line 234**: Function 'create_detective_among_us_engines' missing type hints
- 🔵 **Line 241**: Function 'create_budget_among_us_engines' missing type hints
- 🔵 **Line 246**: Function 'create_mixed_among_us_engines' missing type hints

### src/haive/games/among_us/egnines.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/games/among_us/agent.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 61**: Method 'AmongUsAgent.get_engine_for_player' missing type hints

### src/haive/games/among_us/prompts.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/games/chess/state.py

- 🔵 **Line 108**: Method 'ChessState.board_fen' missing type hints
- 🔵 **Line 118**: Method 'ChessState.current_board_fen' missing type hints
- 🔵 **Line 126**: Method 'ChessState.get_board' missing type hints

### src/haive/games/chess/engines.py

- 🔵 **Line 20**: Function 'create_white_player_engine' missing type hints
- 🔵 **Line 90**: Function 'create_black_player_engine' missing type hints
- 🔵 **Line 160**: Function 'create_white_analyzer_engine' missing type hints
- 🔵 **Line 217**: Function 'create_black_analyzer_engine' missing type hints
- 🔵 **Line 274**: Function 'build_chess_aug_llms' missing type hints

### src/haive/games/chess/state_manager.py

- 🔵 **Line 48**: Method 'ChessGameStateManager.initialize' missing type hints

### src/haive/games/chess/example_configurable.py

- 🔵 **Line 20**: Function 'run_chess_with_custom_llms' missing type hints
- 🔵 **Line 104**: Function 'run_advanced_chess_example' missing type hints
- 🔵 **Line 152**: Function 'list_available_providers' missing type hints

### src/haive/games/chess/config.py

- 🔵 **Line 120**: Method 'ChessConfig.get_role_definitions' missing type hints
- 🔵 **Line 147**: Method 'ChessConfig.get_example_configs' missing type hints
- 🔵 **Line 163**: Method 'ChessConfig.build_legacy_engines' missing type hints
- 🔵 **Line 168**: Method 'ChessConfig.create_simple_player_configs' missing type hints
- 🔵 **Line 204**: Method 'ChessConfig.finalize_config' missing type hints

### src/haive/games/chess/models.py

- 🔵 **Line 40**: Method 'ChessMoveModel.to_move' missing type hints

### src/haive/games/chess/configurable_config.py

- 🔵 **Line 127**: Method 'ConfigurableChessConfig.configure_engines_and_names' missing type hints

### src/haive/games/chess/ui.py

- 🔵 **Line 64**: Method 'ChessRichUI.render_header' missing type hints
- 🔵 **Line 77**: Method 'ChessRichUI.render_footer' missing type hints
- 🔵 **Line 103**: Method 'ChessRichUI.render_board' missing type hints
- 🔵 **Line 194**: Method 'ChessRichUI.render_current_move' missing type hints
- 🔵 **Line 304**: Method 'ChessRichUI.render_move_history' missing type hints
- 🔵 **Line 343**: Method 'ChessRichUI.render_game_info' missing type hints
- 🔵 **Line 424**: Method 'ChessRichUI.run' missing type hints
- 🔵 **Line 538**: Function 'main' missing type hints

### src/haive/games/chess/llm_utils.py

- 🔵 **Line 187**: Function 'get_available_chess_providers' missing type hints
- 🔵 **Line 196**: Function 'get_recommended_chess_models' missing type hints

### src/haive/games/chess/aug_llms.py

- 🔵 **Line 109**: Function 'build_chess_aug_llms_per_color' missing type hints

### src/haive/games/chess/generic_engines.py

- 🔵 **Line 111**: Method 'ChessPromptGenerator.get_move_output_model' missing type hints
- 🔵 **Line 115**: Method 'ChessPromptGenerator.get_analysis_output_model' missing type hints
- 🔵 **Line 239**: Function 'create_typed_chess_engines' missing type hints
- 🔵 **Line 263**: Function 'create_role_specific_chess_engines' missing type hints
- 🔵 **Line 301**: Function 'demonstrate_generic_pattern' missing type hints

### src/haive/games/chess/example_configurable_players.py

- 🔵 **Line 22**: Function 'example_1_simple_models' missing type hints
- 🔵 **Line 38**: Function 'example_2_canonical_strings' missing type hints
- 🔵 **Line 54**: Function 'example_3_example_configs' missing type hints
- 🔵 **Line 72**: Function 'example_4_custom_player_configs' missing type hints
- 🔵 **Line 102**: Function 'example_5_budget_friendly' missing type hints
- 🔵 **Line 119**: Function 'example_6_same_model' missing type hints
- 🔵 **Line 169**: Function 'main' missing type hints

### src/haive/games/chess/agent.py

- 🔵 **Line 63**: Method 'ChessAgent.setup_workflow' missing type hints

### src/haive/games/chess/configurable_engines.py

- 🔵 **Line 109**: Function 'get_chess_role_definitions' missing type hints

### src/haive/games/chess/debug_schema.py

- 🔵 **Line 14**: Function 'debug_field' missing type hints
- 🔵 **Line 46**: Function 'main' missing type hints

### src/haive/games/chess/example.py

- 🔵 **Line 21**: Function 'run_chess_game' missing type hints

### src/haive/games/chess/api_client_example.py

- 🔵 **Line 19**: Method 'ChessAPIClient.list_providers' missing type hints
- 🔵 **Line 24**: Method 'ChessAPIClient.create_game' missing type hints
- 🔵 **Line 50**: Method 'ChessAPIClient.get_game_state' missing type hints
- 🔵 **Line 55**: Method 'ChessAPIClient.stream_game' missing type hints
- 🔵 **Line 70**: Method 'ChessAPIClient.list_games' missing type hints
- 🔵 **Line 75**: Method 'ChessAPIClient.delete_game' missing type hints
- 🔵 **Line 81**: Function 'main' missing type hints
- 🔵 **Line 116**: Function 'handle_event' missing type hints

### src/haive/games/chess/dynamic_config.py

- 🔵 **Line 68**: Method 'ChessConfig.get_role_definitions' missing type hints
- 🔵 **Line 95**: Method 'ChessConfig.get_example_configs' missing type hints
- 🔵 **Line 137**: Method 'ChessConfig.build_legacy_engines' missing type hints
- 🔵 **Line 141**: Method 'ChessConfig.create_simple_player_configs' missing type hints
- 🔵 **Line 267**: Function 'create_legacy_chess_config' missing type hints
- 🔵 **Line 284**: Function 'budget_chess' missing type hints
- 🔵 **Line 289**: Function 'competitive_chess' missing type hints
- 🔵 **Line 294**: Function 'experimental_chess' missing type hints

### src/haive/games/utils/test_helpers.py

- 🔵 **Line 232**: Function 'test_basic_game_structure' missing type hints

### src/haive/games/core/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/games/poker/state.py

- 🔵 **Line 89**: Method 'PokerState.initialize_game' missing type hints
- 🔵 **Line 117**: Method 'PokerState.initialize_deck' missing type hints
- 🔵 **Line 132**: Method 'PokerState.deal_hands' missing type hints
- 🔵 **Line 148**: Method 'PokerState.post_blinds' missing type hints
- 🔵 **Line 189**: Method 'PokerState.deal_community_cards' missing type hints
- 🔵 **Line 219**: Method 'PokerState.start_new_hand' missing type hints
- 🔵 **Line 364**: Method 'PokerState.handle_player_action' missing type hints
- 🔵 **Line 595**: Method 'PokerState.advance_game_phase' missing type hints
- 🔵 **Line 1120**: Method 'PokerState.log_event' missing type hints

### src/haive/games/poker/engines.py

- 🔵 **Line 61**: Function 'generate_hand_analysis_prompt' missing type hints
- 🔵 **Line 82**: Function 'get_available_providers' missing type hints
- 🔵 **Line 109**: Function 'get_poker_llm_provider' missing type hints
- 🔵 **Line 146**: Function 'create_llm_config_for_provider' missing type hints
- 🔵 **Line 179**: Function 'create_poker_agent_configs' missing type hints
- 🔵 **Line 220**: Function 'create_default_agent_configs' missing type hints

### src/haive/games/poker/state_manager.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 38**: Method 'PokerStateManager.initialize_game' missing type hints
- 🔵 **Line 55**: Method 'PokerStateManager.start_new_hand' missing type hints
- 🔵 **Line 128**: Method 'PokerStateManager.advance_phase' missing type hints
- 🔵 **Line 156**: Method 'PokerStateManager.complete_hand' missing type hints
- 🔵 **Line 184**: Method 'PokerStateManager.get_game_summary' missing type hints
- 🔵 **Line 314**: Method 'PokerStateManager.export_history' missing type hints
- 🔵 **Line 318**: Method 'PokerStateManager.reset' missing type hints
- 🔵 **Line 323**: Method 'PokerStateManager.is_game_over' missing type hints

### src/haive/games/poker/config.py

- 🔵 **Line 114**: Method 'PokerAgentConfig.default_config' missing type hints

### src/haive/games/poker/models.py

- 🔵 **Line 185**: Method 'Card.numeric_value' missing type hints
- 🔵 **Line 190**: Method 'Card.numeric_value_low' missing type hints
- 🔵 **Line 443**: Method 'PokerGameState.active_player_count' missing type hints
- 🟡 **Line 561**: Class 'Config' missing docstring

### src/haive/games/poker/configurable_config.py

- 🔵 **Line 249**: Function 'create_budget_poker_config' missing type hints
- 🔵 **Line 254**: Function 'create_advanced_poker_config' missing type hints
- 🔵 **Line 259**: Function 'create_experimental_poker_config' missing type hints
- 🔵 **Line 305**: Function 'list_example_configurations' missing type hints

### src/haive/games/poker/ui.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 55**: Method 'PokerUI.assign_ai_models' missing type hints
- 🔵 **Line 73**: Method 'PokerUI.render_header' missing type hints
- 🔵 **Line 80**: Method 'PokerUI.render_footer' missing type hints
- 🔵 **Line 97**: Method 'PokerUI.render_game_info' missing type hints
- 🔵 **Line 124**: Method 'PokerUI.render_action_history' missing type hints
- 🔵 **Line 170**: Method 'PokerUI.render_table' missing type hints
- 🔵 **Line 202**: Method 'PokerUI.render_players' missing type hints
- 🔵 **Line 295**: Method 'PokerUI.render_active_player' missing type hints

### src/haive/games/poker/generic_engines.py

- 🔵 **Line 200**: Function 'create_advanced_poker_engines' missing type hints
- 🔵 **Line 205**: Function 'create_budget_poker_engines' missing type hints
- 🔵 **Line 210**: Function 'create_mixed_poker_engines' missing type hints

### src/haive/games/poker/agent.py

- 🔵 **Line 163**: Method 'PokerAgent.setup_workflow' missing type hints

### src/haive/games/poker/example.py

- 🟡 **Line 1**: Module missing docstring
- 🟡 **Line 35**: Function 'main' missing docstring
- 🔵 **Line 35**: Function 'main' missing type hints
- 🔵 **Line 110**: Function 'launch_in_separate_window' missing type hints
- 🔵 **Line 173**: Function 'create_config_from_args' missing type hints
- 🔵 **Line 185**: Function 'run_rich_ui_game' missing type hints
- 🔵 **Line 295**: Function 'update_ui' missing type hints
- 🔵 **Line 328**: Function 'run_text_game' missing type hints
- 🔵 **Line 432**: Function 'visualize_game_state' missing type hints

### src/haive/games/poker/debug.py

- 🔵 **Line 130**: Method 'StructuredOutputTester.print_report' missing type hints
- 🔵 **Line 169**: Method 'GameStatePrinter.print_game_state' missing type hints
- 🔵 **Line 289**: Method 'DecisionAnalyzer.validate_decision' missing type hints

### src/haive/games/debate/state.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 56**: Method 'DebateState.current_speaker' missing type hints

### src/haive/games/debate/engines.py

- 🟡 **Line 1**: Module missing docstring
- 🟡 **Line 13**: Function 'generate_moderator_prompt' missing docstring
- 🔵 **Line 13**: Function 'generate_moderator_prompt' missing type hints
- 🟡 **Line 38**: Function 'generate_debater_prompt' missing docstring
- 🟡 **Line 69**: Function 'generate_judge_prompt' missing docstring
- 🔵 **Line 69**: Function 'generate_judge_prompt' missing type hints
- 🟡 **Line 93**: Function 'generate_prosecutor_prompt' missing docstring
- 🔵 **Line 93**: Function 'generate_prosecutor_prompt' missing type hints
- 🟡 **Line 115**: Function 'generate_defense_prompt' missing docstring
- 🔵 **Line 115**: Function 'generate_defense_prompt' missing type hints
- 🟡 **Line 141**: Function 'generate_persona_prompt' missing docstring
- 🔵 **Line 167**: Function 'build_debate_engines' missing type hints

### src/haive/games/debate/state_manager.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/games/debate/config.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 44**: Method 'DebateAgentConfig.default' missing type hints
- 🔵 **Line 56**: Method 'DebateAgentConfig.presidential' missing type hints
- 🔵 **Line 69**: Method 'DebateAgentConfig.trial' missing type hints
- 🔵 **Line 87**: Method 'DebateAgentConfig.panel_discussion' missing type hints

### src/haive/games/debate/models.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/games/debate/factory.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/games/debate/configurable_config.py

- 🔵 **Line 253**: Function 'create_budget_debate_config' missing type hints
- 🔵 **Line 258**: Function 'create_advanced_debate_config' missing type hints
- 🔵 **Line 263**: Function 'create_experimental_debate_config' missing type hints
- 🔵 **Line 309**: Function 'list_example_configurations' missing type hints

### src/haive/games/debate/generic_engines.py

- 🔴 **Line 1**: Could not parse file: unexpected character after line continuation character (<unknown>, line 49)

### src/haive/games/debate/agent.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 582**: Method 'DebateAgent.setup_workflow' missing type hints

### src/haive/games/debate/example.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 9**: Function 'run_debate' missing type hints
- 🔵 **Line 79**: Function 'run_trial_debate' missing type hints
- 🔵 **Line 111**: Function 'run_policy_debate' missing type hints

### src/haive/games/fox_and_geese/state.py

- 🔵 **Line 141**: Method 'FoxAndGeeseState.initialize' missing type hints
- 🔵 **Line 165**: Method 'FoxAndGeeseState.board_string' missing type hints
- 🔵 **Line 185**: Method 'FoxAndGeeseState.model_dump' missing type hints

### src/haive/games/fox_and_geese/enhanced_example.py

- 🔵 **Line 22**: Function 'run_fox_and_geese_game' missing type hints
- 🔵 **Line 90**: Function 'demo_ui_features' missing type hints

### src/haive/games/fox_and_geese/engines.py

- 🔵 **Line 17**: Function 'generate_fox_move_prompt' missing type hints
- 🔵 **Line 47**: Function 'generate_geese_move_prompt' missing type hints
- 🔵 **Line 78**: Function 'generate_fox_analysis_prompt' missing type hints
- 🔵 **Line 111**: Function 'generate_geese_analysis_prompt' missing type hints

### src/haive/games/fox_and_geese/state_manager.py

- 🔵 **Line 23**: Method 'FoxAndGeeseStateManager.initialize' missing type hints

### src/haive/games/fox_and_geese/config.py

- 🔵 **Line 43**: Method 'FoxAndGeeseConfig.default_config' missing type hints

### src/haive/games/fox_and_geese/configurable_config.py

- 🔵 **Line 243**: Function 'create_budget_fox_and_geese_config' missing type hints
- 🔵 **Line 248**: Function 'create_advanced_fox_and_geese_config' missing type hints
- 🔵 **Line 253**: Function 'create_experimental_fox_and_geese_config' missing type hints
- 🔵 **Line 299**: Function 'list_example_configurations' missing type hints

### src/haive/games/fox_and_geese/ui.py

- 🔵 **Line 358**: Method 'FoxAndGeeseUI.display_welcome' missing type hints

### src/haive/games/fox_and_geese/generic_engines.py

- 🔴 **Line 1**: Could not parse file: unexpected character after line continuation character (<unknown>, line 49)

### src/haive/games/fox_and_geese/agent.py

- 🔵 **Line 763**: Method 'FoxAndGeeseAgent.setup_workflow' missing type hints

### src/haive/games/fox_and_geese/example.py

- 🔵 **Line 17**: Function 'run_fox_and_geese_game' missing type hints
- 🔵 **Line 88**: Function 'run_fox_and_geese_with_ui' missing type hints

### src/haive/games/fox_and_geese/rich_ui.py

- 🔵 **Line 779**: Method 'FoxAndGeeseRichUI.display_welcome' missing type hints
- 🔵 **Line 957**: Method 'FoxAndGeeseRichUI.run_fox_and_geese_game' missing type hints

### src/haive/games/fox_and_geese/fixed_runner.py

- 🔵 **Line 127**: Function 'parse_arguments' missing type hints
- 🔵 **Line 145**: Function 'main' missing type hints

### src/haive/games/base_v2/state.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/games/base_v2/player_agent.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/games/base_v2/models.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/games/base_v2/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/games/go/state.py

- 🔵 **Line 86**: Method 'GoGameState.validate_turn' missing type hints

### src/haive/games/go/engines.py

- 🔵 **Line 23**: Function 'generate_black_prompt' missing type hints
- 🔵 **Line 62**: Function 'generate_white_prompt' missing type hints
- 🔵 **Line 101**: Function 'generate_analysis_prompt' missing type hints
- 🔵 **Line 136**: Function 'build_go_aug_llms' missing type hints
- 🔵 **Line 182**: Function 'get_black_engine' missing type hints
- 🔵 **Line 187**: Function 'get_white_engine' missing type hints
- 🔵 **Line 192**: Function 'get_analyzer_engine' missing type hints

### src/haive/games/go/models.py

- 🔵 **Line 59**: Method 'GoMoveModel.validate_move' missing type hints
- 🔵 **Line 82**: Method 'GoMoveModel.to_tuple' missing type hints

### src/haive/games/go/agent.py

- 🔵 **Line 66**: Method 'GoAgent.setup_workflow' missing type hints
- 🔵 **Line 293**: Function 'run_go_game' missing type hints

### src/haive/games/go/go_engine.py

- 🔵 **Line 25**: Method 'GoGame.play_move' missing type hints
- 🔵 **Line 59**: Method 'GoGame.to_sgf' missing type hints
- 🔵 **Line 81**: Method 'GoGame.turn' missing type hints
- 🔵 **Line 127**: Method 'sgf.loads' missing type hints
- 🔵 **Line 132**: Method 'sgf.dumps' missing type hints

### src/haive/games/reversi/state.py

- 🔵 **Line 61**: Method 'ReversiState.validate_board' missing type hints
- 🔵 **Line 86**: Method 'ReversiState.current_player_name' missing type hints
- 🔵 **Line 95**: Method 'ReversiState.disc_count' missing type hints
- 🔵 **Line 106**: Method 'ReversiState.board_string' missing type hints

### src/haive/games/reversi/engines.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/games/reversi/state_manager.py

- 🔵 **Line 28**: Method 'ReversiStateManager.initialize' missing type hints

### src/haive/games/reversi/config.py

- 🔵 **Line 53**: Method 'ReversiConfig.default_config' missing type hints

### src/haive/games/reversi/configurable_config.py

- 🔵 **Line 247**: Function 'create_budget_reversi_config' missing type hints
- 🔵 **Line 252**: Function 'create_advanced_reversi_config' missing type hints
- 🔵 **Line 257**: Function 'create_experimental_reversi_config' missing type hints
- 🔵 **Line 303**: Function 'list_example_configurations' missing type hints

### src/haive/games/reversi/generic_engines.py

- 🔵 **Line 198**: Function 'create_advanced_reversi_engines' missing type hints
- 🔵 **Line 203**: Function 'create_budget_reversi_engines' missing type hints
- 🔵 **Line 208**: Function 'create_mixed_reversi_engines' missing type hints

### src/haive/games/reversi/agent.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 411**: Method 'ReversiAgent.setup_workflow' missing type hints

### src/haive/games/reversi/example.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/games/board/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/games/risk/state.py

- 🔵 **Line 391**: Method 'RiskState.is_game_over' missing type hints
- 🔵 **Line 399**: Method 'RiskState.get_winner' missing type hints

### src/haive/games/risk/config.py

- 🔵 **Line 43**: Method 'RiskConfig.classic' missing type hints
- 🔵 **Line 63**: Method 'RiskConfig.modern' missing type hints

### src/haive/games/risk/configurable_config.py

- 🔵 **Line 249**: Function 'create_budget_risk_config' missing type hints
- 🔵 **Line 254**: Function 'create_advanced_risk_config' missing type hints
- 🔵 **Line 259**: Function 'create_experimental_risk_config' missing type hints
- 🔵 **Line 305**: Function 'list_example_configurations' missing type hints

### src/haive/games/risk/generic_engines.py

- 🔵 **Line 198**: Function 'create_advanced_risk_engines' missing type hints
- 🔵 **Line 203**: Function 'create_budget_risk_engines' missing type hints
- 🔵 **Line 208**: Function 'create_mixed_risk_engines' missing type hints

### src/haive/games/risk/agent.py

- 🔵 **Line 32**: Method 'RiskAgent.analyze_position' missing type hints
- 🔵 **Line 73**: Method 'RiskAgent.get_move' missing type hints

### src/haive/games/single_player/state_manager.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/games/single_player/base.py

- 🔵 **Line 107**: Method 'SinglePlayerGameState.is_game_over' missing type hints
- 🔵 **Line 111**: Method 'SinglePlayerGameState.is_victory' missing type hints
- 🔵 **Line 115**: Method 'SinglePlayerGameState.is_defeat' missing type hints
- 🔵 **Line 119**: Method 'SinglePlayerGameState.increment_move_count' missing type hints
- 🔵 **Line 123**: Method 'SinglePlayerGameState.use_hint' missing type hints
- 🔵 **Line 544**: Method 'SinglePlayerGameAgent.setup_workflow' missing type hints
- 🔵 **Line 642**: Method 'SinglePlayerGameAgent.save_state_history' missing type hints

### src/haive/games/single_player/config.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/games/single_player/example.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 1**: Function 'run_interactive_game' missing type hints
- 🔵 **Line 88**: Function 'run_auto_game' missing type hints

### src/haive/games/battleship/state.py

- 🔵 **Line 128**: Method 'BattleshipState.is_setup_complete' missing type hints
- 🔵 **Line 145**: Method 'BattleshipState.is_game_over' missing type hints

### src/haive/games/battleship/engines.py

- 🔵 **Line 20**: Function 'build_battleship_engines' missing type hints

### src/haive/games/battleship/state_manager.py

- 🔵 **Line 46**: Method 'BattleshipStateManager.initialize' missing type hints

### src/haive/games/battleship/config.py

- 🔵 **Line 72**: Method 'BattleshipAgentConfig.update_player_names_from_engines' missing type hints

### src/haive/games/battleship/models.py

- 🔵 **Line 42**: Method 'Coordinates.to_tuple' missing type hints
- 🔵 **Line 60**: Method 'Ship.is_sunk' missing type hints
- 🔵 **Line 64**: Method 'Ship.get_occupied_positions' missing type hints
- 🔵 **Line 81**: Method 'ShipPlacement.validate_coordinates' missing type hints
- 🔵 **Line 108**: Method 'ShipPlacementWrapper.validate_placements' missing type hints
- 🔵 **Line 151**: Method 'MoveCommand.to_coordinates' missing type hints
- 🔵 **Line 186**: Method 'Analysis.validate_targets' missing type hints
- 🔵 **Line 309**: Method 'PlayerBoard.all_ships_sunk' missing type hints
- 🔵 **Line 313**: Method 'PlayerBoard.get_occupied_positions' missing type hints

### src/haive/games/battleship/configurable_config.py

- 🔵 **Line 247**: Function 'create_budget_battleship_config' missing type hints
- 🔵 **Line 252**: Function 'create_naval_battleship_config' missing type hints
- 🔵 **Line 257**: Function 'create_experimental_battleship_config' missing type hints
- 🔵 **Line 303**: Function 'list_example_configurations' missing type hints

### src/haive/games/battleship/generic_engines.py

- 🔵 **Line 203**: Function 'create_naval_battleship_engines' missing type hints
- 🔵 **Line 208**: Function 'create_budget_battleship_engines' missing type hints
- 🔵 **Line 213**: Function 'create_mixed_battleship_engines' missing type hints

### src/haive/games/battleship/agent.py

- 🔵 **Line 89**: Method 'BattleshipAgent.setup_workflow' missing type hints

### src/haive/games/battleship/example.py

- 🔵 **Line 38**: Function 'run_game' missing type hints
- 🔵 **Line 222**: Function 'main' missing type hints

### src/haive/games/battleship/debug.py

- 🔵 **Line 30**: Function 'test_battleship' missing type hints

### src/haive/games/monopoly/game/property.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/games/monopoly/game/player.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/games/monopoly/game/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/games/monopoly/game/types.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/games/monopoly/game/card.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/games/monopoly/game/game.py

- 🔵 **Line 581**: Method 'MonopolyGame.roll_dice' missing type hints
- 🔵 **Line 600**: Method 'MonopolyGame.get_current_player' missing type hints
- 🔵 **Line 1758**: Method 'MonopolyGame.get_game_state' missing type hints
- 🔵 **Line 1805**: Method 'MonopolyGame.print_game_state' missing type hints

### src/haive/games/framework/base/state.py

- 🔵 **Line 56**: Method 'GameState.initialize' missing type hints
- 🟡 **Line 51**: Class 'Config' missing docstring

### src/haive/games/framework/base/state_manager.py

- 🔵 **Line 53**: Method 'GameStateManager.initialize' missing type hints

### src/haive/games/framework/base/utils.py

- 🔵 **Line 22**: Function 'run_game' missing type hints

### src/haive/games/framework/base/agent.py

- 🔵 **Line 66**: Method 'GameAgent.setup_workflow' missing type hints
- 🔵 **Line 449**: Function 'run_game' missing type hints

### src/haive/games/framework/multi_player/state.py

- 🔵 **Line 83**: Method 'MultiPlayerGameState.current_player' missing type hints
- 🔵 **Line 98**: Method 'MultiPlayerGameState.advance_player' missing type hints
- 🟡 **Line 79**: Class 'Config' missing docstring

### src/haive/games/framework/multi_player/agent.py

- 🔵 **Line 114**: Method 'MultiPlayerGameAgent.setup_workflow' missing type hints

### src/haive/games/framework/core/turn.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 42**: Method 'Turn.get_move_count' missing type hints
- 🔵 **Line 54**: Method 'Turn.next_phase' missing type hints

### src/haive/games/framework/core/move.py

- 🟡 **Line 1**: Module missing docstring
- 🟡 **Line 22**: Class 'Config' missing docstring

### src/haive/games/framework/core/player.py

- 🟡 **Line 1**: Module missing docstring
- 🟡 **Line 28**: Class 'Config' missing docstring

### src/haive/games/framework/core/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/games/framework/core/board.py

- 🟡 **Line 1**: Module missing docstring
- 🟡 **Line 33**: Class 'Config' missing docstring

### src/haive/games/framework/core/agent.py

- 🟡 **Line 1**: Module missing docstring
- 🟡 **Line 6**: Class 'BasePlayerAgent' missing docstring
- 🔵 **Line 18**: Method 'BasePlayerAgent.setup_workflow' missing docstring
- 🔵 **Line 18**: Method 'BasePlayerAgent.setup_workflow' missing type hints

### src/haive/games/framework/core/container.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 61**: Method 'GamePieceContainer.count' missing type hints
- 🔵 **Line 65**: Method 'GamePieceContainer.is_empty' missing type hints
- 🔵 **Line 69**: Method 'GamePieceContainer.shuffle' missing type hints
- 🟡 **Line 27**: Class 'Config' missing docstring

### src/haive/games/framework/core/grid.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 39**: Method 'GridPosition.coordinates' missing type hints
- 🔵 **Line 45**: Method 'GridPosition.display_coords' missing type hints

### src/haive/games/framework/core/position.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 36**: Method 'Position.serialize' missing type hints
- 🟡 **Line 19**: Class 'Config' missing docstring

### src/haive/games/framework/core/game.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 56**: Method 'Game.current_turn' missing type hints
- 🔵 **Line 64**: Method 'Game.turn_number' missing type hints
- 🔵 **Line 68**: Method 'Game.start_game' missing type hints
- 🔵 **Line 83**: Method 'Game.get_current_player' missing type hints
- 🔵 **Line 93**: Method 'Game.start_turn' missing type hints
- 🔵 **Line 108**: Method 'Game.end_turn' missing type hints
- 🔵 **Line 154**: Method 'Game.check_game_over' missing type hints
- 🟡 **Line 51**: Class 'Config' missing docstring

### src/haive/games/framework/core/space.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 50**: Method 'Space.remove_piece' missing type hints
- 🔵 **Line 60**: Method 'Space.is_occupied' missing type hints
- 🟡 **Line 31**: Class 'Config' missing docstring

### src/haive/games/framework/core/rule.py

- 🟡 **Line 1**: Module missing docstring
- 🟡 **Line 20**: Class 'Config' missing docstring

### src/haive/games/framework/core/piece.py

- 🟡 **Line 1**: Module missing docstring
- 🟡 **Line 28**: Class 'Config' missing docstring

### src/haive/games/framework/core/boards/grid.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/games/framework/core/spaces/grid.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 20**: Method 'GridSpace.get_row' missing type hints
- 🔵 **Line 24**: Method 'GridSpace.get_col' missing type hints
- 🔵 **Line 28**: Method 'GridSpace.is_dark_square' missing type hints
- 🔵 **Line 36**: Method 'GridSpace.get_chess_notation' missing type hints

### src/haive/games/framework/core/positions/grid.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 39**: Method 'GridPosition.coordinates' missing type hints
- 🔵 **Line 45**: Method 'GridPosition.display_coords' missing type hints

### src/haive/games/framework/core/containers/deck.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 24**: Method 'Deck.draw' missing type hints
- 🔵 **Line 61**: Method 'Deck.create_standard_deck' missing type hints

### src/haive/games/cards/uno/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/games/cards/models/card.py

- 🔵 **Line 47**: Method 'Suit.color' missing type hints
- 🔵 **Line 199**: Method 'Card.long_name' missing type hints
- 🔵 **Line 233**: Method 'Card.blackjack_value' missing type hints
- 🔵 **Line 248**: Method 'Card.is_face_card' missing type hints

### src/haive/games/cards/standard/bs/state.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/games/cards/standard/bs/state_manager.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/games/cards/standard/bs/config.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 14**: Function 'generate_claim_prompt' missing type hints
- 🔵 **Line 37**: Function 'generate_challenge_prompt' missing type hints
- 🔵 **Line 78**: Method 'BullshitAgentConfig.build_bullshit_aug_llms' missing type hints
- 🔵 **Line 96**: Method 'BullshitAgentConfig.default' missing type hints
- 🔵 **Line 112**: Function 'build_bullshit_aug_llms' missing type hints

### src/haive/games/cards/standard/bs/models.py

- 🟡 **Line 1**: Module missing docstring
- 🟡 **Line 7**: Class 'CardSuit' missing docstring
- 🔵 **Line 24**: Method 'Card.create_deck' missing type hints

### src/haive/games/cards/standard/bs/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/games/cards/standard/bs/agent.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 285**: Method 'BullshitAgent.setup_workflow' missing type hints

### src/haive/games/cards/standard/bs/prompts.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/games/cards/standard/poker/state.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 74**: Method 'PokerGameState.setup_active_players' missing type hints
- 🔵 **Line 80**: Method 'PokerGameState.start_game' missing type hints
- 🔵 **Line 162**: Method 'PokerGameState.deal_hole_cards' missing type hints
- 🔵 **Line 198**: Method 'PokerGameState.advance_phase' missing type hints

### src/haive/games/cards/standard/poker/actions.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 163**: Method 'BetAction.validate_bet' missing type hints
- 🔵 **Line 232**: Method 'RaiseAction.validate_raise' missing type hints

### src/haive/games/cards/standard/poker/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/games/cards/standard/poker/scoring.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/games/cards/standard/blackjack/state_manager.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 18**: Method 'BlackjackStateManager.create_deck' missing type hints

### src/haive/games/cards/standard/blackjack/config.py

- 🟡 **Line 1**: Module missing docstring
- 🟡 **Line 11**: Function 'generate_betting_prompt' missing docstring
- 🔵 **Line 11**: Function 'generate_betting_prompt' missing type hints
- 🟡 **Line 33**: Function 'generate_player_action_prompt' missing docstring
- 🔵 **Line 33**: Function 'generate_player_action_prompt' missing type hints
- 🔵 **Line 76**: Method 'BlackjackAgentConfig.build_blackjack_aug_llms' missing type hints
- 🔵 **Line 95**: Method 'BlackjackAgentConfig.default' missing type hints
- 🔵 **Line 112**: Function 'build_blackjack_aug_llms' missing type hints

### src/haive/games/cards/standard/blackjack/models.py

- 🟡 **Line 1**: Module missing docstring
- 🟡 **Line 7**: Class 'CardSuit' missing docstring
- 🔵 **Line 23**: Method 'Card.point_value' missing type hints
- 🔵 **Line 51**: Method 'PlayerHand.total_value' missing type hints
- 🔵 **Line 63**: Method 'PlayerHand.is_bust' missing type hints
- 🔵 **Line 67**: Method 'PlayerHand.is_blackjack' missing type hints
- 🔵 **Line 81**: Method 'PlayerState.add_hand' missing type hints

### src/haive/games/cards/standard/blackjack/factory.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/games/cards/standard/blackjack/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/games/cards/standard/blackjack/agent.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 230**: Method 'BlackjackAgent.setup_workflow' missing type hints

### src/haive/games/core/piece/tile.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 7**: Method 'Tile.flip' missing type hints

### src/haive/games/core/players/base.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/games/core/players/agent.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/games/core/base/state.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/games/core/base/engines.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/games/core/base/state_manager.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/games/core/base/config.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/games/core/base/models.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/games/core/base/player.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/games/core/game/core-position.py

- 🔵 **Line 39**: Method 'Position.serialize' missing type hints
- 🔵 **Line 74**: Method 'GridPosition.coordinates' missing type hints
- 🔵 **Line 80**: Method 'GridPosition.display_coords' missing type hints
- 🔵 **Line 93**: Method 'GridPosition.neighbors' missing type hints
- 🔵 **Line 106**: Method 'GridPosition.neighbors_with_diagonals' missing type hints
- 🔵 **Line 158**: Method 'PointPosition.coordinates' missing type hints
- 🔵 **Line 212**: Method 'HexPosition.axial_coords' missing type hints
- 🔵 **Line 216**: Method 'HexPosition.neighbors' missing type hints
- 🟡 **Line 24**: Class 'Config' missing docstring

### src/haive/games/core/game/core-board.py

- 🔵 **Line 151**: Method 'Board.get_all_pieces' missing type hints
- 🔵 **Line 305**: Method 'GridBoard.size' missing type hints
- 🟡 **Line 38**: Class 'Config' missing docstring

### src/haive/games/core/game/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/games/core/game/core-game.py

- 🔵 **Line 115**: Method 'Game.initialize' missing type hints
- 🔵 **Line 145**: Method 'Game.setup_game' missing type hints
- 🔵 **Line 152**: Method 'Game.start' missing type hints
- 🔵 **Line 166**: Method 'Game.start_turn' missing type hints
- 🔵 **Line 181**: Method 'Game.end_turn' missing type hints
- 🔵 **Line 195**: Method 'Game.get_current_player' missing type hints
- 🔵 **Line 201**: Method 'Game.is_finished' missing type hints
- 🔵 **Line 219**: Method 'Game.abort' missing type hints
- 🔵 **Line 226**: Method 'Game.pause' missing type hints
- 🔵 **Line 234**: Method 'Game.resume' missing type hints
- 🔵 **Line 335**: Method 'Game.check_end_condition' missing type hints
- 🔵 **Line 344**: Method 'Game.determine_winner' missing type hints
- 🔵 **Line 485**: Method 'TurnBasedGame.end_turn' missing type hints
- 🔵 **Line 505**: Method 'TurnBasedGame.reverse_turn_order' missing type hints
- 🔵 **Line 512**: Method 'TurnBasedGame.skip_turn' missing type hints
- 🟡 **Line 112**: Class 'Config' missing docstring

### src/haive/games/core/game/core-space.py

- 🔵 **Line 27**: Method 'SpaceProtocol.is_occupied' missing docstring
- 🔵 **Line 27**: Method 'SpaceProtocol.is_occupied' missing type hints
- 🔵 **Line 28**: Method 'SpaceProtocol.place_piece' missing docstring
- 🔵 **Line 29**: Method 'SpaceProtocol.remove_piece' missing docstring
- 🔵 **Line 29**: Method 'SpaceProtocol.remove_piece' missing type hints
- 🔵 **Line 49**: Method 'Space.is_occupied' missing type hints
- 🔵 **Line 75**: Method 'Space.remove_piece' missing type hints
- 🔵 **Line 141**: Method 'GridSpace.get_grid_position' missing type hints
- 🔵 **Line 153**: Method 'GridSpace.coordinates' missing type hints
- 🔵 **Line 172**: Method 'HexSpace.coordinates' missing type hints
- 🟡 **Line 46**: Class 'Config' missing docstring

### src/haive/games/core/game/piece.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 39**: Method 'GamePieceProtocol.can_move_to' missing docstring
- 🔵 **Line 40**: Method 'GamePieceProtocol.assign_to_player' missing docstring
- 🔵 **Line 41**: Method 'GamePieceProtocol.place_at' missing docstring

### src/haive/games/core/move/**init**.py

- 🔴 **Line 1**: Could not parse file: '{' was never closed (<unknown>, line 488)

### src/haive/games/core/agent/player_agent.py

- 🔵 **Line 24**: Method 'PlayerRole.get_role_name' missing type hints
- 🔵 **Line 28**: Method 'PlayerRole.get_prompt_template' missing type hints
- 🔵 **Line 32**: Method 'PlayerRole.get_structured_output_model' missing type hints
- 🔵 **Line 86**: Method 'PlayerAgentConfig.create_llm_config' missing type hints
- 🔵 **Line 207**: Method 'ConfigurableGameAgent.get_role_definitions' missing type hints
- 🟡 **Line 54**: Class 'Config' missing docstring
- 🟡 **Line 83**: Class 'Config' missing docstring

### src/haive/games/core/agent/game_config.py

- 🔴 **Line 1**: Could not parse file: expected ':' (<unknown>, line 13)

### src/haive/games/core/agent/generic_player_agent.py

- 🔵 **Line 50**: Method 'GamePlayerIdentifiers.get_players' missing type hints
- 🔵 **Line 114**: Method 'GenericPromptGenerator.get_move_output_model' missing type hints
- 🔵 **Line 119**: Method 'GenericPromptGenerator.get_analysis_output_model' missing type hints
- 🔵 **Line 143**: Method 'GenericGameEngineFactory.create_role_definitions' missing type hints
- 🔵 **Line 495**: Function 'example_chess_usage' missing type hints
- 🔵 **Line 531**: Function 'example_custom_game_usage' missing type hints
- 🟡 **Line 47**: Class 'Config' missing docstring
- 🟡 **Line 85**: Class 'Config' missing docstring
- 🟡 **Line 499**: Class 'ChessPromptGenerator' missing docstring
- 🔵 **Line 500**: Method 'ChessPromptGenerator.create_move_prompt' missing docstring
- 🔵 **Line 508**: Method 'ChessPromptGenerator.create_analysis_prompt' missing docstring
- 🔵 **Line 516**: Method 'ChessPromptGenerator.get_move_output_model' missing docstring
- 🔵 **Line 516**: Method 'ChessPromptGenerator.get_move_output_model' missing type hints
- 🔵 **Line 519**: Method 'ChessPromptGenerator.get_analysis_output_model' missing docstring
- 🔵 **Line 519**: Method 'ChessPromptGenerator.get_analysis_output_model' missing type hints
- 🟡 **Line 536**: Class 'SPSPromptGenerator' missing docstring
- 🔵 **Line 537**: Method 'SPSPromptGenerator.create_move_prompt' missing docstring
- 🔵 **Line 545**: Method 'SPSPromptGenerator.create_analysis_prompt' missing docstring
- 🔵 **Line 553**: Method 'SPSPromptGenerator.get_move_output_model' missing docstring
- 🔵 **Line 553**: Method 'SPSPromptGenerator.get_move_output_model' missing type hints
- 🔵 **Line 556**: Method 'SPSPromptGenerator.get_analysis_output_model' missing docstring
- 🔵 **Line 556**: Method 'SPSPromptGenerator.get_analysis_output_model' missing type hints

### src/haive/games/core/agent/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/games/core/position/base.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 45**: Method 'GridPosition.display_coords' missing type hints
- 🔵 **Line 65**: Method 'HexPosition.s' missing type hints
- 🔵 **Line 69**: Method 'HexPosition.neighbors' missing type hints
- 🟡 **Line 17**: Class 'Config' missing docstring

### src/haive/games/core/position/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/games/core/components/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/games/core/config/base.py

- 🔵 **Line 86**: Method 'BaseGameConfig.get_role_definitions' missing type hints
- 🔵 **Line 103**: Method 'BaseGameConfig.get_example_configs' missing type hints
- 🔵 **Line 126**: Method 'BaseGameConfig.build_legacy_engines' missing type hints
- 🔵 **Line 148**: Method 'BaseGameConfig.determine_config_mode' missing type hints
- 🔵 **Line 162**: Method 'BaseGameConfig.create_simple_player_configs' missing type hints
- 🔵 **Line 211**: Method 'BaseGameConfig.configure_engines' missing type hints
- 🔵 **Line 235**: Method 'BaseGameConfig.get_player_names' missing type hints

### src/haive/games/core/board/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition
- 🔵 **Line 74**: Method 'Space.is_occupied' missing type hints
- 🔵 **Line 87**: Method 'Space.remove_piece' missing type hints
- 🔵 **Line 109**: Method 'GridSpace.coordinates' missing type hints
- 🔵 **Line 121**: Method 'HexSpace.coordinates' missing type hints
- 🔵 **Line 127**: Method 'HexSpace.cube_coords' missing type hints
- 🔵 **Line 205**: Method 'Board.get_all_pieces' missing type hints
- 🔵 **Line 232**: Method 'GridBoard.validate_dimensions' missing docstring
- 🔵 **Line 252**: Method 'GridBoard.initialize_grid' missing type hints
- 🔵 **Line 275**: Method 'GridBoard.size' missing type hints
- 🔵 **Line 287**: Method 'HexBoard.validate_radius' missing docstring
- 🔵 **Line 307**: Method 'HexBoard.initialize_hex_grid' missing type hints

### src/haive/games/core/game/pieces/core-game.py

- 🔵 **Line 115**: Method 'Game.initialize' missing type hints
- 🔵 **Line 145**: Method 'Game.setup_game' missing type hints
- 🔵 **Line 152**: Method 'Game.start' missing type hints
- 🔵 **Line 166**: Method 'Game.start_turn' missing type hints
- 🔵 **Line 181**: Method 'Game.end_turn' missing type hints
- 🔵 **Line 195**: Method 'Game.get_current_player' missing type hints
- 🔵 **Line 201**: Method 'Game.is_finished' missing type hints
- 🔵 **Line 219**: Method 'Game.abort' missing type hints
- 🔵 **Line 226**: Method 'Game.pause' missing type hints
- 🔵 **Line 234**: Method 'Game.resume' missing type hints
- 🔵 **Line 335**: Method 'Game.check_end_condition' missing type hints
- 🔵 **Line 344**: Method 'Game.determine_winner' missing type hints
- 🔵 **Line 485**: Method 'TurnBasedGame.end_turn' missing type hints
- 🔵 **Line 505**: Method 'TurnBasedGame.reverse_turn_order' missing type hints
- 🔵 **Line 512**: Method 'TurnBasedGame.skip_turn' missing type hints
- 🟡 **Line 112**: Class 'Config' missing docstring

### src/haive/games/core/game/containers/base.py

- 🔵 **Line 70**: Method 'GamePieceContainer.count' missing type hints
- 🔵 **Line 78**: Method 'GamePieceContainer.is_empty' missing type hints
- 🔵 **Line 86**: Method 'GamePieceContainer.shuffle' missing type hints
- 🔵 **Line 101**: Method 'GamePieceContainer.draw' missing type hints
- 🔵 **Line 150**: Method 'GamePieceContainer.clear' missing type hints
- 🔵 **Line 188**: Method 'Deck.draw' missing type hints
- 🔵 **Line 260**: Method 'Deck.draw_bottom' missing type hints
- 🟡 **Line 33**: Class 'Config' missing docstring

### src/haive/games/core/game/containers/deck.py

- 🔵 **Line 24**: Method 'Card.flip' missing type hints
- 🔵 **Line 42**: Method 'Deck.draw' missing type hints
- 🔵 **Line 114**: Method 'Deck.draw_bottom' missing type hints

### src/haive/games/core/game/containers/containers_tilebag (1).py

- 🔵 **Line 25**: Method 'TileBag.draw_random' missing type hints
- 🔵 **Line 50**: Method 'TileBag.peek_random' missing type hints
- 🔵 **Line 71**: Method 'TileBag.create_from_distribution' missing type hints

### src/haive/games/core/game/containers/container.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 36**: Method 'GamePieceContainer.count' missing type hints
- 🔵 **Line 40**: Method 'GamePieceContainer.is_empty' missing type hints
- 🔵 **Line 44**: Method 'GamePieceContainer.shuffle' missing type hints
- 🔵 **Line 52**: Method 'GamePieceContainer.draw' missing type hints
- 🔵 **Line 82**: Method 'Deck.draw' missing type hints
- 🔵 **Line 102**: Method 'Deck.create_standard_deck' missing type hints
- 🔵 **Line 116**: Method 'TileBag.draw_random' missing type hints

### src/haive/games/core/components/cards/base.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 43**: Method 'Card.flip' missing type hints
- 🔵 **Line 77**: Method 'CardContainer.count' missing type hints
- 🔵 **Line 81**: Method 'CardContainer.is_empty' missing type hints
- 🔵 **Line 85**: Method 'CardContainer.shuffle' missing type hints
- 🔵 **Line 100**: Method 'Deck.draw' missing type hints
- 🟡 **Line 32**: Class 'Config' missing docstring
- 🟡 **Line 55**: Class 'Config' missing docstring

### src/haive/games/core/components/cards/actions.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 35**: Method 'CardAction.validate_action' missing type hints
- 🔵 **Line 55**: Method 'DrawCardAction.validate_action' missing type hints
- 🟡 **Line 31**: Class 'Config' missing docstring

### src/haive/games/core/components/cards/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/games/core/components/cards/scoring.py

- 🟡 **Line 1**: Module missing docstring
- 🟡 **Line 31**: Class 'Config' missing docstring

### src/haive/games/core/components/cards/turns.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 42**: Method 'CardGameTurn.get_next_phase' missing type hints
- 🔵 **Line 121**: Method 'TurnManager.get_current_player' missing type hints
- 🔵 **Line 127**: Method 'TurnManager.reverse_direction' missing type hints
- 🟡 **Line 30**: Class 'Config' missing docstring
- 🟡 **Line 63**: Class 'Config' missing docstring

### src/haive/games/core/components/cards/standard.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 66**: Method 'StandardCard.set_value' missing type hints
- 🔵 **Line 78**: Method 'StandardCard.set_face_card' missing type hints
- 🔵 **Line 87**: Method 'StandardCard.set_color' missing type hints
- 🔵 **Line 101**: Method 'StandardCard.set_name' missing type hints
- 🔵 **Line 114**: Method 'StandardCard.format' missing type hints
- 🔵 **Line 172**: Method 'StandardDeckFactory.create_pinochle_deck' missing type hints

### src/haive/games/single_player/rubiks/state.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/games/single_player/rubiks/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/games/single_player/rubiks/agent.py

- 🔵 **Line 36**: Method 'RubiksCubeAgent.setup_workflow' missing type hints

### src/haive/games/single_player/wordle/state.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 81**: Method 'WordConnectionsState.board_string' missing type hints

### src/haive/games/single_player/wordle/engines.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/games/single_player/wordle/state_manager.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/games/single_player/wordle/config.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 21**: Function 'create_game_prompt' missing type hints

### src/haive/games/single_player/wordle/models.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 20**: Method 'WordConnectionsMove.validate_words_length' missing type hints
- 🔵 **Line 54**: Method 'WordConnectionsState.remaining_words' missing type hints
- 🔵 **Line 62**: Method 'WordConnectionsState.display_grid' missing type hints

### src/haive/games/single_player/wordle/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/games/single_player/wordle/agent.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 17**: Method 'WordConnectionsAgent.setup_workflow' missing type hints
- 🔵 **Line 180**: Method 'WordConnectionsAgent.setup_routing' missing type hints

### src/haive/games/single_player/wordle/example.py

- 🔵 **Line 21**: Method 'WordConnectionsUI.display_grid' missing type hints
- 🔵 **Line 85**: Method 'WordConnectionsUI.display_solution' missing type hints

### src/haive/games/single_player/flow_free/state.py

- 🔵 **Line 95**: Method 'FlowFreeState.is_solved' missing type hints
- 🔵 **Line 114**: Method 'FlowFreeState.completion_percentage' missing type hints
- 🔵 **Line 126**: Method 'FlowFreeState.total_cells' missing type hints
- 🔵 **Line 132**: Method 'FlowFreeState.filled_cells' missing type hints
- 🔵 **Line 138**: Method 'FlowFreeState.board_fill_percentage' missing type hints
- 🔵 **Line 197**: Method 'FlowFreeState.to_display_string' missing type hints

### src/haive/games/single_player/flow_free/engines.py

- 🔵 **Line 14**: Function 'generate_move_prompt' missing type hints
- 🔵 **Line 59**: Function 'generate_analysis_prompt' missing type hints

### src/haive/games/single_player/flow_free/base.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 107**: Method 'FlowPipe.is_corner' missing type hints
- 🔵 **Line 132**: Method 'FlowGridSpace.has_endpoint' missing type hints
- 🔵 **Line 142**: Method 'FlowGridSpace.has_pipe' missing type hints
- 🔵 **Line 152**: Method 'FlowGridSpace.color' missing type hints
- 🔵 **Line 169**: Method 'FlowBoard.initialize_grid' missing type hints
- 🔵 **Line 363**: Method 'FlowBoard.is_solved' missing type hints
- 🔵 **Line 395**: Method 'FlowFreeGame.start_game' missing type hints
- 🔵 **Line 513**: Method 'FlowFreeGame.reset' missing type hints
- 🔵 **Line 533**: Method 'FlowFreeLevel.create_game' missing type hints

### src/haive/games/single_player/flow_free/config.py

- 🔵 **Line 62**: Method 'FlowFreeConfig.default_config' missing type hints
- 🔵 **Line 83**: Method 'FlowFreeConfig.easy_config' missing type hints
- 🔵 **Line 104**: Method 'FlowFreeConfig.interactive_config' missing type hints

### src/haive/games/single_player/flow_free/models.py

- 🔵 **Line 105**: Method 'FlowFreeAnalysis.completion_percentage' missing type hints

### src/haive/games/single_player/flow_free/example.py

- 🔵 **Line 23**: Function 'main' missing type hints
- 🔵 **Line 66**: Function 'parse_arguments' missing type hints
- 🔵 **Line 111**: Function 'create_config' missing type hints

### src/haive/games/single_player/logic_grid/base.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 55**: Method 'LogicGridPosition.display_coords' missing type hints
- 🔵 **Line 95**: Method 'LogicGridSpace.mark_type' missing type hints
- 🔵 **Line 127**: Method 'LogicGridClue.validate_clue' missing type hints
- 🔵 **Line 233**: Method 'LogicGrid.initialize_grid' missing type hints
- 🔵 **Line 310**: Method 'LogicGrid.is_solved' missing type hints
- 🔵 **Line 353**: Method 'LogicGridPuzzle.start_game' missing type hints
- 🔵 **Line 362**: Method 'LogicGridPuzzle.apply_clues' missing type hints
- 🔵 **Line 398**: Method 'LogicGridPuzzle.propagate_constraints' missing type hints
- 🔵 **Line 440**: Method 'LogicGridPuzzle.reset' missing type hints
- 🔵 **Line 459**: Method 'LogicGridPuzzleDefinition.create_game' missing type hints

### src/haive/games/single_player/sudoku/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition
- 🔵 **Line 67**: Method 'SudokuGame.validate_game' missing type hints
- 🔵 **Line 201**: Method 'SudokuGame.get_hint' missing type hints
- 🔵 **Line 247**: Method 'SudokuGame.toggle_candidates' missing type hints
- 🔵 **Line 251**: Method 'SudokuGame.restart' missing type hints
- 🔵 **Line 267**: Method 'SudokuGame.get_elapsed_time' missing type hints
- 🔵 **Line 277**: Method 'SudokuGame.get_status' missing type hints
- 🔵 **Line 294**: Method 'SudokuGame.undo_move' missing type hints

### src/haive/games/single_player/towers_of_hanoi/base.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 40**: Method 'Game.start_game' missing type hints
- 🔵 **Line 55**: Method 'Game.end_game' missing type hints
- 🔵 **Line 61**: Method 'Game.move_count' missing type hints
- 🔵 **Line 65**: Method 'Game.reset' missing type hints
- 🔵 **Line 121**: Method 'PegPosition.display_coords' missing type hints
- 🔵 **Line 192**: Method 'PegSpace.peg_number' missing type hints
- 🔵 **Line 198**: Method 'PegSpace.level' missing type hints
- 🔵 **Line 275**: Method 'HanoiBoard.initialize_board' missing type hints
- 🔵 **Line 317**: Method 'HanoiBoard.is_solved' missing type hints
- 🔵 **Line 349**: Method 'HanoiGame.calculate_min_moves' missing type hints
- 🔵 **Line 355**: Method 'HanoiGame.start_game' missing type hints
- 🔵 **Line 414**: Method 'HanoiGame.is_optimal' missing type hints
- 🔵 **Line 418**: Method 'HanoiGame.reset' missing type hints
- 🔵 **Line 457**: Method 'Peg.remove_top_disk' missing type hints
- 🔵 **Line 465**: Method 'Peg.top_disk' missing type hints

### src/haive/games/single_player/towers_of_hanoi/ui.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 26**: Method 'HanoiUI.run' missing type hints
- 🔵 **Line 51**: Method 'HanoiUI.play_game' missing type hints
- 🔵 **Line 88**: Method 'HanoiUI.create_display' missing type hints
- 🔵 **Line 126**: Method 'HanoiUI.format_moves' missing type hints
- 🔵 **Line 140**: Method 'HanoiUI.ai_move' missing type hints
- 🔵 **Line 155**: Method 'HanoiUI.manual_move' missing type hints
- 🔵 **Line 173**: Method 'HanoiUI.auto_play' missing type hints
- 🔵 **Line 186**: Function 'main' missing type hints

### src/haive/games/single_player/towers_of_hanoi/postiition.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/games/single_player/towers_of_hanoi/move.py

- 🔵 **Line 17**: Method 'HanoiMoveModel.validate_from_peg' missing docstring
- 🔵 **Line 24**: Method 'HanoiMoveModel.validate_to_peg' missing docstring

### src/haive/games/single_player/towers_of_hanoi/container.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/games/single_player/towers_of_hanoi/position.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 30**: Method 'PegPosition.display_coords' missing type hints

### src/haive/games/single_player/towers_of_hanoi/promopts.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/games/single_player/towers_of_hanoi/piece.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/games/single_player/twenty_fourty_eight/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/games/single_player/twenty_fourty_eight/game.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 68**: Method 'NumberTile.reset_merge_status' missing type hints
- 🔵 **Line 115**: Method 'TwentyFortyEightGame.validate_game' missing type hints
- 🔵 **Line 123**: Method 'TwentyFortyEightGame.new_game' missing type hints
- 🔵 **Line 179**: Method 'TwentyFortyEightGame.restart' missing type hints
- 🔵 **Line 190**: Method 'TwentyFortyEightGame.get_status' missing type hints

### src/haive/games/single_player/crossword_puzzle/base.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 49**: Method 'CrosswordCell.is_block' missing type hints
- 🔵 **Line 55**: Method 'CrosswordCell.is_letter_cell' missing type hints
- 🔵 **Line 61**: Method 'CrosswordCell.current_letter' missing type hints
- 🔵 **Line 69**: Method 'CrosswordCell.is_filled' missing type hints
- 🔵 **Line 102**: Method 'CrosswordClue.end_position' missing type hints
- 🔵 **Line 124**: Method 'CrosswordWord.validate_word' missing type hints
- 🔵 **Line 157**: Method 'CrosswordGame.start_game' missing type hints
- 🔵 **Line 261**: Method 'CrosswordGame.check_all' missing type hints
- 🔵 **Line 305**: Method 'CrosswordGame.reset' missing type hints
- 🔵 **Line 335**: Method 'CrosswordTemplate.create_game' missing type hints

### src/haive/games/single_player/word_search/base.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/games/single_player/testing/base.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/games/single_player/testing/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition
- 🔵 **Line 51**: Method 'AnswerableProtocol.check_answer' missing docstring
- 🔵 **Line 52**: Method 'AnswerableProtocol.clear_answer' missing docstring
- 🔵 **Line 52**: Method 'AnswerableProtocol.clear_answer' missing type hints
- 🔵 **Line 53**: Method 'AnswerableProtocol.get_points' missing docstring
- 🔵 **Line 53**: Method 'AnswerableProtocol.get_points' missing type hints
- 🔵 **Line 61**: Method 'ScoringProtocol.calculate_score' missing docstring
- 🔵 **Line 61**: Method 'ScoringProtocol.calculate_score' missing type hints
- 🔵 **Line 62**: Method 'ScoringProtocol.get_completion_percentage' missing docstring
- 🔵 **Line 62**: Method 'ScoringProtocol.get_completion_percentage' missing type hints
- 🔵 **Line 110**: Method 'Question.is_answered' missing type hints
- 🔵 **Line 143**: Method 'Question.clear_answer' missing type hints
- 🔵 **Line 147**: Method 'Question.get_points' missing type hints
- 🔵 **Line 162**: Method 'MultipleChoiceQuestion.validate_choices' missing type hints
- 🔵 **Line 222**: Method 'MatchingQuestion.validate_matching' missing type hints
- 🔵 **Line 244**: Method 'FillInBlankQuestion.validate_blanks' missing type hints
- 🔵 **Line 282**: Method 'Section.question_count' missing type hints
- 🔵 **Line 288**: Method 'Section.max_points' missing type hints
- 🔵 **Line 294**: Method 'Section.total_time' missing type hints
- 🔵 **Line 308**: Method 'Section.calculate_score' missing type hints
- 🔵 **Line 312**: Method 'Section.get_completion_percentage' missing type hints
- 🔵 **Line 363**: Method 'Test.question_count' missing type hints
- 🔵 **Line 369**: Method 'Test.max_points' missing type hints
- 🔵 **Line 375**: Method 'Test.total_time' missing type hints
- 🔵 **Line 391**: Method 'Test.is_completed' missing type hints
- 🔵 **Line 397**: Method 'Test.calculate_score' missing type hints
- 🔵 **Line 401**: Method 'Test.get_completion_percentage' missing type hints
- 🔵 **Line 412**: Method 'Test.is_passing' missing type hints
- 🔵 **Line 427**: Method 'Test.grade' missing type hints
- 🔵 **Line 491**: Method 'TestSession.start' missing type hints
- 🔵 **Line 498**: Method 'TestSession.complete' missing type hints
- 🔵 **Line 505**: Method 'TestSession.timeout' missing type hints

### src/haive/games/single_player/mine_sweeper/base.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 45**: Method 'MinesweeperCell.place_mine' missing type hints
- 🔵 **Line 51**: Method 'MinesweeperCell.is_mine' missing type hints
- 🔵 **Line 55**: Method 'MinesweeperCell.is_revealed' missing type hints
- 🔵 **Line 59**: Method 'MinesweeperCell.is_flagged' missing type hints
- 🔵 **Line 63**: Method 'MinesweeperCell.is_questioned' missing type hints
- 🔵 **Line 67**: Method 'MinesweeperCell.reveal' missing type hints
- 🔵 **Line 79**: Method 'MinesweeperCell.toggle_flag' missing type hints
- 🔵 **Line 102**: Method 'MinesweeperCell.get_display_value' missing type hints
- 🔵 **Line 388**: Method 'MinesweeperBoard.is_game_won' missing type hints
- 🔵 **Line 393**: Method 'MinesweeperBoard.get_board_state' missing type hints
- 🔵 **Line 403**: Method 'MinesweeperBoard.get_mine_locations' missing type hints
- 🔵 **Line 413**: Method 'MinesweeperBoard.reveal_all_mines' missing type hints
- 🔵 **Line 421**: Method 'MinesweeperBoard.get_remaining_mines' missing type hints
- 🔵 **Line 438**: Method 'MinesweeperGame.validate_game' missing type hints
- 🔵 **Line 564**: Method 'MinesweeperGame.restart' missing type hints
- 🔵 **Line 590**: Method 'MinesweeperGame.get_elapsed_time' missing type hints
- 🔵 **Line 600**: Method 'MinesweeperGame.get_status' missing type hints

### src/haive/games/single_player/mine_sweeper/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/games/single_player/logic_grid/game/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/games/single_player/sudoku/game/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/games/single_player/sudoku/game/board.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 18**: Method 'SudokuBoard.initialize_board' missing type hints
- 🔵 **Line 143**: Method 'SudokuBoard.update_all_candidates' missing type hints
- 🔵 **Line 204**: Method 'SudokuBoard.is_complete' missing type hints
- 🔵 **Line 213**: Method 'SudokuBoard.is_valid' missing type hints
- 🔵 **Line 236**: Method 'SudokuBoard.is_solved' missing type hints
- 🔵 **Line 240**: Method 'SudokuBoard.get_puzzle_state' missing type hints
- 🔵 **Line 250**: Method 'SudokuBoard.get_candidates_state' missing type hints
- 🔵 **Line 260**: Method 'SudokuBoard.autosolve_step' missing type hints

### src/haive/games/single_player/sudoku/game/cell.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 15**: Method 'SudokuCell.value' missing type hints
- 🔵 **Line 21**: Method 'SudokuCell.is_fixed' missing type hints
- 🔵 **Line 50**: Method 'SudokuCell.clear' missing type hints

### src/haive/games/single_player/sudoku/game/piece.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/games/single_player/twenty_fourty_eight/game/**init**.py

- 🟡 **Line 1**: **init**.py missing **all** definition

### src/haive/games/single_player/twenty_fourty_eight/game/board.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 10**: Method 'TwentyFortyEightBoard.initialize_board' missing type hints
- 🔵 **Line 18**: Method 'TwentyFortyEightBoard.spawn_random_tile' missing type hints
- 🔵 **Line 158**: Method 'TwentyFortyEightBoard.has_valid_moves' missing type hints
- 🔵 **Line 205**: Method 'TwentyFortyEightBoard.get_max_tile' missing type hints
- 🔵 **Line 213**: Method 'TwentyFortyEightBoard.clear' missing type hints
- 🔵 **Line 219**: Method 'TwentyFortyEightBoard.get_board_state' missing type hints

### src/haive/games/single_player/twenty_fourty_eight/game/piece.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/games/single_player/crossword_puzzle/game/board.py

- 🟡 **Line 1**: Module missing docstring
- 🔵 **Line 9**: Method 'CrosswordBoard.initialize_grid' missing type hints
- 🔵 **Line 187**: Method 'CrosswordBoard.is_complete' missing type hints

### src/haive/games/single_player/crossword_puzzle/game/cell.py

- 🟡 **Line 1**: Module missing docstring

### src/haive/games/single_player/crossword_puzzle/game/piece.py

- 🟡 **Line 1**: Module missing docstring
