#!/usr/bin/env python3
"""
Test script for the Monopoly agent.

This script tests various components and functionality of the Monopoly agent
to identify and fix any issues.
"""

import os
import sys
import logging
import time
import traceback
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))

from haive.games.monopoly.config import MonopolyAgentConfig
from haive.games.monopoly.agent import MonopolyAgent
from haive.games.monopoly.state import MonopolyState
from haive.games.monopoly.models import TurnDecision, PropertyAction, MoveAction, PlayerInfo as Player, PropertyInfo as Property, StrategyAnalysis
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("monopoly_test.log", mode="w")
    ]
)

logger = logging.getLogger(__name__)

class MonopolyAgentTester:
    """Test suite for the Monopoly agent."""
    
    def __init__(self, model="gpt-4o", temperature=0.7):
        """Initialize the tester with model parameters."""
        self.model = model
        self.temperature = temperature
        self.successful_tests = 0
        self.failed_tests = 0
        self.issues_found = []
        
        # Create agent with test configuration
        logger.info(f"Initializing Monopoly agent tester with model: {model}")
        
        self.agent = self._create_agent()
    
    def _create_agent(self):
        """Create a Monopoly agent with test configuration."""
        # Create LLM config
        azure_config = AzureLLMConfig(
            model=self.model,
            parameters={"temperature": self.temperature}
        )
        
        # Create AugLLM configs for the different engines
        strategy_engine = AugLLMConfig.from_llm_config(
            llm_config=azure_config,
            name="strategy",
            request_timeout=60
        )
        
        turn_decision_engine = AugLLMConfig.from_llm_config(
            llm_config=azure_config,
            name="turn_decision",
            request_timeout=60
        )
        
        property_engine = AugLLMConfig.from_llm_config(
            llm_config=azure_config,
            name="property",
            request_timeout=60
        )
        
        # Create agent config
        config = MonopolyAgentConfig(
            name="monopoly_test_agent",
            engines={
                "strategy": strategy_engine,
                "turn_decision": turn_decision_engine,
                "property": property_engine
            }
        )
        
        # Create agent
        return MonopolyAgent(config=config)
    
    def _create_test_state(self):
        """Create a test state for the Monopoly game."""
        # Create basic players
        players = [
            Player(
                index=0,
                name="Player 1",
                cash=1500,
                position=0,
                is_in_jail=False,
                properties_owned=["Mediterranean Avenue", "Baltic Avenue"],
                jail_cards=0,
                bankruptcy_status=False,
                total_wealth=1500  # Add total_wealth field
            ),
            Player(
                index=1,
                name="Player 2",
                cash=1500,
                position=10,  # Just Visiting
                is_in_jail=False,
                properties_owned=["Oriental Avenue", "Vermont Avenue", "Connecticut Avenue"],
                jail_cards=1,
                bankruptcy_status=False,
                total_wealth=1500  # Add total_wealth field
            )
        ]
        
        # Create some properties
        properties = {
            "Mediterranean Avenue": Property(
                name="Mediterranean Avenue",
                position=1,
                cost=60,
                rent_values=[2, 10, 30, 90, 160, 250],
                rent=2,
                color="Brown",
                houses=0,
                owner=0,  # Owned by Player 1
                is_mortgaged=False,
                mortgage_value=30
            ),
            "Baltic Avenue": Property(
                name="Baltic Avenue",
                position=3,
                cost=60,
                rent_values=[4, 20, 60, 180, 320, 450],
                rent=4,
                color="Brown",
                houses=0,
                owner=0,  # Owned by Player 1
                is_mortgaged=False,
                mortgage_value=30
            ),
            "Oriental Avenue": Property(
                name="Oriental Avenue",
                position=6,
                cost=100,
                rent_values=[6, 30, 90, 270, 400, 550],
                rent=6,
                color="Light Blue",
                houses=0,
                owner=1,  # Owned by Player 2
                is_mortgaged=False,
                mortgage_value=50
            ),
            "Vermont Avenue": Property(
                name="Vermont Avenue",
                position=8,
                cost=100,
                rent_values=[6, 30, 90, 270, 400, 550],
                rent=6,
                color="Light Blue",
                houses=0,
                owner=1,  # Owned by Player 2
                is_mortgaged=False,
                mortgage_value=50
            ),
            "Connecticut Avenue": Property(
                name="Connecticut Avenue",
                position=9,
                cost=120,
                rent_values=[8, 40, 100, 300, 450, 600],
                rent=8,
                color="Light Blue",
                houses=1,
                owner=1,  # Owned by Player 2
                is_mortgaged=False,
                mortgage_value=60
            ),
            "St. James Place": Property(
                name="St. James Place",
                position=16,
                cost=180,
                rent_values=[14, 70, 200, 550, 750, 950],
                rent=14,
                color="Orange",
                houses=0,
                owner=None,  # Unowned
                is_mortgaged=False,
                mortgage_value=90
            ),
        }
        
        # Create the state
        state = MonopolyState(
            players=players,
            properties=properties,
            current_player_index=0,  # Player 1's turn
            has_rolled=False,
            recent_events=["Game started", "Player 1's turn"],
            dice=None,
            special_cards={},
            community_chest_drawn=None,
            chance_drawn=None
        )
        
        return state
    
    def test_analyze_strategy(self):
        """Test the analyze_strategy method."""
        logger.info("Testing analyze_strategy...")
        test_state = self._create_test_state()
        
        try:
            start_time = time.time()
            result = self.agent.analyze_strategy(test_state.model_dump())
            duration = time.time() - start_time
            
            # Check results
            if not result or not isinstance(result, dict):
                raise ValueError("Invalid result type returned")
            
            if "strategy_analysis" not in result:
                raise ValueError("Strategy analysis not found in result")
            
            # Log success
            logger.info(f"Strategy analysis successful in {duration:.2f}s")
            logger.debug(f"Analysis: {result['strategy_analysis']}")
            self.successful_tests += 1
            return True
            
        except Exception as e:
            logger.error(f"Strategy analysis test failed: {e}")
            logger.error(traceback.format_exc())
            self.failed_tests += 1
            self.issues_found.append({
                "test": "analyze_strategy",
                "error": str(e),
                "traceback": traceback.format_exc()
            })
            return False
    
    def test_decide_turn_actions(self):
        """Test the decide_turn_actions method."""
        logger.info("Testing decide_turn_actions...")
        test_state = self._create_test_state()
        
        # First run analyze_strategy to get a complete state
        try:
            state_with_analysis = self.agent.analyze_strategy(test_state.model_dump())
            
            start_time = time.time()
            result = self.agent.decide_turn_actions(state_with_analysis)
            duration = time.time() - start_time
            
            # Check for Command with valid update
            if not hasattr(result, 'update') or not result.update:
                raise ValueError("Invalid result: no update found")
            
            if "turn_decision" not in result.update:
                raise ValueError("Turn decision not found in result")
            
            # Log success
            logger.info(f"Turn decision successful in {duration:.2f}s")
            logger.debug(f"Decision: {result.update['turn_decision']}")
            self.successful_tests += 1
            return True
            
        except Exception as e:
            logger.error(f"Turn decision test failed: {e}")
            logger.error(traceback.format_exc())
            self.failed_tests += 1
            self.issues_found.append({
                "test": "decide_turn_actions",
                "error": str(e),
                "traceback": traceback.format_exc()
            })
            return False
    
    def test_execute_move(self):
        """Test the execute_move method."""
        logger.info("Testing execute_move...")
        test_state = self._create_test_state()
        
        try:
            # First run analyze_strategy and decide_turn_actions to get move decision
            state_dict = test_state.model_dump()
            state_dict = self.agent.analyze_strategy(state_dict)
            
            # Create a mock turn decision with a roll move
            from haive.games.monopoly.models import MoveAction, TurnDecision
            move_action = MoveAction(action_type="roll", reasoning="Test roll")
            turn_decision = TurnDecision(
                move_action=move_action,
                property_actions=[],
                end_turn=False,
                reasoning="Testing move execution"
            )
            
            # Add the decision to state
            state_dict["turn_decision"] = turn_decision.model_dump()
            
            # Execute the move
            start_time = time.time()
            result = self.agent.execute_move(state_dict)
            duration = time.time() - start_time
            
            # Check results
            result_state = MonopolyState(**result)
            
            # Verify the move happened - position should be updated
            if result_state.players[0].position == test_state.players[0].position:
                raise ValueError("Player position did not change after move")
            
            # Verify dice were rolled
            if not result_state.dice:
                raise ValueError("Dice not recorded in state")
            
            # Verify has_rolled flag is set
            if not result_state.has_rolled:
                raise ValueError("has_rolled flag not set after move")
            
            # Log success
            logger.info(f"Execute move test successful in {duration:.2f}s")
            self.successful_tests += 1
            return True
            
        except Exception as e:
            logger.error(f"Execute move test failed: {e}")
            logger.error(traceback.format_exc())
            self.failed_tests += 1
            self.issues_found.append({
                "test": "execute_move",
                "error": str(e),
                "traceback": traceback.format_exc()
            })
            return False
    
    def test_manage_properties(self):
        """Test the manage_properties method."""
        logger.info("Testing manage_properties...")
        test_state = self._create_test_state()
        
        try:
            # Create a state with a player landed on an unowned property
            state_dict = test_state.model_dump()
            
            # Get Mediterranean Avenue (should be at position 1)
            mediterranean_ave = None
            for prop_name, prop in state_dict["properties"].items():
                if prop["position"] == 1:
                    mediterranean_ave = prop_name
                    break
            
            if not mediterranean_ave:
                raise ValueError("Mediterranean Avenue not found in test state")
            
            # Make sure it's unowned
            state_dict["properties"][mediterranean_ave]["owner"] = None
            
            # Move player to that position
            state_dict["players"][0]["position"] = 1
            
            # Create a property action to buy it
            from haive.games.monopoly.models import PropertyAction, TurnDecision
            property_action = PropertyAction(
                action_type="buy",
                property_name=mediterranean_ave,
                reasoning="Test buying property"
            )
            
            # Create turn decision
            turn_decision = TurnDecision(
                move_action=None,
                property_actions=[property_action],
                end_turn=False,
                reasoning="Testing property management"
            )
            
            # Add to state
            state_dict["turn_decision"] = turn_decision.model_dump()
            
            # Execute property management
            start_time = time.time()
            result = self.agent.manage_properties(state_dict)
            duration = time.time() - start_time
            
            # Check results
            result_state = MonopolyState(**result)
            
            # Verify the property was bought
            if result_state.properties[mediterranean_ave].owner != 0:
                raise ValueError(f"Property {mediterranean_ave} was not purchased by player 0")
            
            # Verify player cash was reduced
            property_cost = test_state.properties[mediterranean_ave].cost
            expected_cash = test_state.players[0].cash - property_cost
            
            if result_state.players[0].cash != expected_cash:
                raise ValueError(f"Player cash not updated correctly after purchase. Expected {expected_cash}, got {result_state.players[0].cash}")
            
            # Log success
            logger.info(f"Property management test successful in {duration:.2f}s")
            self.successful_tests += 1
            return True
            
        except Exception as e:
            logger.error(f"Property management test failed: {e}")
            logger.error(traceback.format_exc())
            self.failed_tests += 1
            self.issues_found.append({
                "test": "manage_properties",
                "error": str(e),
                "traceback": traceback.format_exc()
            })
            return False
    
    def test_game_flow(self):
        """Test the game flow from start to end."""
        logger.info("Testing game flow...")
        test_state = self._create_test_state()
        
        try:
            # Convert to dict
            state_dict = test_state.model_dump()
            
            # Simulate a few turns of game flow
            for _ in range(3):  # Just do a few turns for testing
                # Analyze strategy
                state_dict = self.agent.analyze_strategy(state_dict)
                
                # Decide turn actions
                cmd = self.agent.decide_turn_actions(state_dict)
                if hasattr(cmd, 'update'):
                    # Update state with the command updates
                    state_dict.update(cmd.update)
                    
                    # Get next action from goto
                    next_action = cmd.goto
                    if next_action == "move":
                        state_dict = self.agent.execute_move(state_dict)
                    elif next_action == "manage_properties":
                        state_dict = self.agent.manage_properties(state_dict)
                    elif next_action == "end_turn":
                        state_dict = self.agent.end_player_turn(state_dict)
                    else:
                        logger.info(f"Skipping action: {next_action}")
                else:
                    # If no command with goto, just end the turn
                    state_dict = self.agent.end_player_turn(state_dict)
            
            # Convert back to state object for validation
            final_state = MonopolyState(**state_dict)
            
            # Check results
            if not final_state.players or len(final_state.players) < 2:
                raise ValueError("Game flow resulted in invalid player count")
            
            # Check that game progressed (some events recorded)
            if len(final_state.recent_events) < 5:
                raise ValueError("Game did not progress properly, too few events")
            
            # Log success
            logger.info("Game flow test successful")
            self.successful_tests += 1
            return True
            
        except Exception as e:
            logger.error(f"Game flow test failed: {e}")
            logger.error(traceback.format_exc())
            self.failed_tests += 1
            self.issues_found.append({
                "test": "game_flow",
                "error": str(e),
                "traceback": traceback.format_exc()
            })
            return False
    
    def run_all_tests(self):
        """Run all tests and report results."""
        logger.info("Running all Monopoly agent tests")
        
        # Run each test
        tests = [
            self.test_analyze_strategy,
            self.test_decide_turn_actions,
            self.test_execute_move,
            self.test_manage_properties,
            self.test_game_flow
        ]
        
        for test_func in tests:
            try:
                logger.info(f"Running test: {test_func.__name__}")
                test_func()
            except Exception as e:
                logger.error(f"Test {test_func.__name__} failed: {e}")
                logger.error(traceback.format_exc())
                self.failed_tests += 1
                self.issues_found.append({
                    "test": test_func.__name__,
                    "error": str(e),
                    "traceback": traceback.format_exc()
                })
        
        # Print results
        logger.info(f"Tests completed. Successful: {self.successful_tests}, Failed: {self.failed_tests}")
        
        # Log any issues
        for issue in self.issues_found:
            logger.error(f"Issue in {issue['test']}: {issue['error']}")
        
        return self.successful_tests, self.failed_tests, self.issues_found

def main():
    """Run the Monopoly agent tests."""
    print("Starting Monopoly agent tests...")
    
    # Run with default GPT-4o model
    tester = MonopolyAgentTester(model="gpt-4o", temperature=0.7)
    tester.run_all_tests()

if __name__ == "__main__":
    main() 