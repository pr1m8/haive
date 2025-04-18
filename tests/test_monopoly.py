from src.haive.games.monopoly.agent import MonopolyAgent
from src.haive.games.monopoly.models import MoveAction, PropertyAction, TurnDecision
from src.haive.games.monopoly.state import MonopolyState


def test_init():
    agent = MonopolyAgent()

    state = MonopolyState()

    initialized_state = agent.initialize_game(state)

    state_obj = MonopolyState(**initialized_state)
    agent.end_player_turn(state_obj)

    return "Basic initialization tests passed"


def test_move():
    agent = MonopolyAgent()
    state = MonopolyState()
    initialized_state = agent.initialize_game(state)
    state_obj = MonopolyState(**initialized_state)

    # Create a move action
    move_action = MoveAction(action_type="roll", reasoning="Testing roll action")

    # Create a turn decision with the move action
    turn_decision = TurnDecision(
        move_action=move_action,
        property_actions=[],
        end_turn=False,
        reasoning="Test roll action",
    )

    # Add turn decision to state
    state_obj.turn_decision = turn_decision

    # Execute move
    agent.execute_move(state_obj)

    return "Move tests passed"


def test_property_management():
    agent = MonopolyAgent()
    state = MonopolyState()
    initialized_state = agent.initialize_game(state)
    state_obj = MonopolyState(**initialized_state)

    # Create a property action
    property_action = PropertyAction(
        action_type="buy",
        property_name="Mediterranean Avenue",
        reasoning="Testing buy property",
    )

    # Create a turn decision with the property action
    turn_decision = TurnDecision(
        move_action=None,
        property_actions=[property_action],
        end_turn=False,
        reasoning="Test property action",
    )

    # Add turn decision to state
    state_obj.turn_decision = turn_decision

    # Move player to property position
    state_obj.players[0].position = 1  # Mediterranean Avenue position

    # Execute property management
    agent.manage_properties(state_obj)

    return "Property management tests passed"


if __name__ == "__main__":
    result1 = test_init()

    result2 = test_move()

    result3 = test_property_management()
