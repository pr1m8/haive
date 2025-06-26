# Haive Games: Among Us Module

## Overview

The Among Us module provides an AI-native implementation of a social deduction game inspired by the popular game "Among Us." It enables AI agents to engage in complex social dynamics, including deception, evidence evaluation, cooperation, and reasoning about other agents' knowledge and intentions. This game serves as both an engaging demonstration of multi-agent interaction and a challenging benchmark for social reasoning capabilities.

## Key Features

- **Social Deduction**: Complex reasoning about truth, deception, and evidence
- **Hidden Roles**: Crew members and impostors with asymmetric information
- **Simulated Environments**: Task-based gameplay in a virtual environment
- **Voting and Discussion**: Structured discussion and voting mechanics
- **Strategic Depth**: Multiple strategies for both crews and impostors
- **Observability**: Customizable observability settings for game information
- **Multi-Agent Coordination**: Opportunities for coordinated actions
- **Visualization**: Clear representation of game state and agent observations

## Installation

This module is part of the `haive-games` package. Install the full package with:

```bash
pip install haive-games
```

## Quick Start

```python
from haive.games.among_us import AmongUsAgent, AmongUsConfig
from haive.core.engine.aug_llm import AugLLMConfig

# Configure the game
config = AmongUsConfig(
    num_players=8,
    num_impostors=2,
    map_name="skeld",
    emergency_meetings=1,
    kill_cooldown=30,
    discussion_time=120,
    llm_config=AugLLMConfig(
        system_message="You are playing a social deduction game. Observe carefully, communicate strategically, and try to identify the impostors.",
        temperature=0.7  # Higher temperature for more varied social behavior
    )
)

# Create and run the game
agent = AmongUsAgent(config)
result = agent.run()

# View results
print(f"Winner: {result.winner}")  # 'crew' or 'impostors'
print(f"Game length: {result.num_rounds} rounds")
print(f"Final vote counts: {result.vote_history[-1]}")
```

## Components

### AmongUsAgent

Main agent class that orchestrates the Among Us game.

```python
from haive.games.among_us import AmongUsAgent, AmongUsConfig

# Create a custom configuration
config = AmongUsConfig(
    num_players=10,
    num_impostors=2,
    player_names=["Red", "Blue", "Green", "Yellow", "Orange", "Pink", "Black", "White", "Purple", "Brown"],
    vision_range=5,
    kill_distance=1,
    task_count=8,
    emergency_cooldown=15
)

# Create the agent
agent = AmongUsAgent(config)

# Run a full game
result = agent.run()
```

### AmongUsState

Game state representation for Among Us.

```python
from haive.games.among_us import AmongUsState, Player, Location, Task

# Examine a game state
state = AmongUsState(
    players=[
        Player(id="p1", name="Red", role="impostor", location=Location(5, 10), alive=True),
        Player(id="p2", name="Blue", role="crew", location=Location(8, 12), alive=True),
        # ...more players...
    ],
    tasks=[
        Task(id="t1", name="Fix Wiring", location=Location(10, 15), assigned_to="p2", completed=False),
        Task(id="t2", name="Empty Garbage", location=Location(20, 5), assigned_to="p3", completed=True),
        # ...more tasks...
    ],
    round=3,
    phase="discussion",  # Options: tasks, discussion, voting
    reported_body=None,
    emergency_caller=None,
    voting={},
    kill_cooldowns={"p1": 10},  # Seconds until impostor can kill again
    game_over=False,
    winner=None
)

# Check if a player can see another
can_see = state.can_player_see(player_id="p1", target_id="p2")
```

### AmongUsStateManager

Handles game logic, state transitions, and rule enforcement.

```python
from haive.games.among_us import AmongUsStateManager, AmongUsConfig, PlayerAction

# Create a state manager
config = AmongUsConfig(num_players=8, num_impostors=2)
state_manager = AmongUsStateManager(config)

# Initialize a new game
state = state_manager.initialize_state()

# Process a player action
action = PlayerAction(
    player_id="p1",
    action_type="move",
    target_location=Location(15, 20)
)
new_state = state_manager.apply_action(state, action)

# Process a kill action
kill_action = PlayerAction(
    player_id="p1",  # Impostor
    action_type="kill",
    target_player="p3"
)
new_state = state_manager.apply_action(new_state, kill_action)

# Check for game over
is_game_over, winner = state_manager.check_game_over(new_state)
```

## Game Structure

An Among Us game follows this structure:

1. **Setup**:
   - Assign roles (crew or impostor) to players
   - Distribute tasks to crew members
   - Place players in starting locations

2. **Task Phase Loop**:
   - Players move around the map
   - Crew members complete tasks
   - Impostors can kill crew members
   - Players can report dead bodies or call emergency meetings

3. **Discussion Phase**:
   - Players share observations and suspicions
   - Impostors try to deflect suspicion
   - Crew members try to identify impostors

4. **Voting Phase**:
   - Players vote to eject someone
   - Player with most votes is ejected
   - Check for win conditions

5. **Game End**:
   - Crew wins if all tasks are completed or all impostors ejected
   - Impostors win if they equal/outnumber crew members

## Usage Patterns

### Custom Agent Strategies

```python
from haive.games.among_us import AmongUsAgent, PlayerRole
from haive.core.engine.aug_llm import AugLLMConfig, compose_runnable

class StrategyAmongUsAgent(AmongUsAgent):
    def __init__(self, config):
        super().__init__(config)

        # Create specialized engines for different roles
        self.crew_engine = compose_runnable(AugLLMConfig(
            system_message="""
            You are a crew member in a social deduction game. Your goals:
            1. Complete assigned tasks efficiently
            2. Observe other players' behavior and movements
            3. Report suspicious activity
            4. Identify impostors through logical deduction
            5. Convince others of your findings through clear communication

            Be methodical and thorough in your observations and reasoning.
            """,
            temperature=0.3
        ))

        self.impostor_engine = compose_runnable(AugLLMConfig(
            system_message="""
            You are an impostor in a social deduction game. Your goals:
            1. Eliminate crew members when unobserved
            2. Blend in by pretending to do tasks
            3. Create alibis for yourself
            4. Cast suspicion on innocent crew members
            5. Defend yourself convincingly when accused

            Be strategic about when and where you act. Avoid being seen during kills.
            """,
            temperature=0.7
        ))

    def get_player_decision(self, state, player_id):
        # Get player's role
        player_role = self.get_player_role(state, player_id)

        # Choose engine based on role
        if player_role == PlayerRole.CREW:
            engine = self.crew_engine
        else:
            engine = self.impostor_engine

        # Create observation for the player
        observation = self.create_player_observation(state, player_id)

        # Get decision from engine
        response = engine.invoke(self.format_observation(observation))

        # Parse decision
        return self.parse_decision(response, observation)
```

### Custom Discussion System

```python
from haive.games.among_us import AmongUsAgent, AmongUsState
from haive.core.engine.aug_llm import AugLLMConfig, compose_runnable

class EnhancedDiscussionAgent(AmongUsAgent):
    def __init__(self, config):
        super().__init__(config)

        # Create discussion engine
        self.discussion_engine = compose_runnable(AugLLMConfig(
            system_message="""
            You are moderating a discussion in a social deduction game.
            Generate realistic and dynamic dialogue between players based on
            their observations, suspicions, and the current game state.
            """,
            temperature=0.7
        ))

    def run_discussion_phase(self, state):
        """Run an enhanced discussion phase with multiple rounds of dialogue."""
        # Create new state for discussion phase
        discussion_state = state.model_copy(deep=True)
        discussion_state.phase = "discussion"

        # Get observations for all players
        player_observations = {
            player.id: self.create_player_observation(state, player.id)
            for player in state.players if player.alive
        }

        # Initial statements
        statements = {}
        for player_id, observation in player_observations.items():
            statements[player_id] = self.get_player_statement(
                discussion_state, player_id, observation, []
            )

        # Multiple rounds of discussion
        for round_num in range(3):  # 3 rounds of back-and-forth
            # Format all previous statements
            discussion_history = self.format_discussion_history(statements)

            # Get responses to previous statements
            new_statements = {}
            for player_id, observation in player_observations.items():
                # Each player responds to what others have said
                new_statements[player_id] = self.get_player_response(
                    discussion_state, player_id, observation, discussion_history
                )

            # Update statements with new round
            for player_id, statement in new_statements.items():
                statements[player_id].append(statement)

        # Return discussion results
        return {
            "discussion_state": discussion_state,
            "statements": statements
        }

    def get_player_statement(self, state, player_id, observation, previous_statements):
        """Get a player's statement based on their observations."""
        player = next(p for p in state.players if p.id == player_id)

        prompt = f"""
        You are {player.name} in a social deduction game.

        Your observations:
        {self.format_observation(observation)}

        Previous statements: {previous_statements}

        What do you want to share with the group? Consider your role, what you've seen,
        and what strategy would benefit you most.
        """

        response = self.get_player_engine(state, player_id).invoke(prompt)
        return response
```

### Game Visualization and Analysis

```python
from haive.games.among_us import AmongUsAgent, AmongUsConfig
from haive.games.among_us.ui import AmongUsVisualizer

# Run a game
config = AmongUsConfig(num_players=10, num_impostors=2)
agent = AmongUsAgent(config)
result = agent.run()

# Create a visualizer
visualizer = AmongUsVisualizer()

# Generate game summary
summary = visualizer.generate_game_summary(result)
print(summary)

# Visualize the map at a specific point
map_viz = visualizer.visualize_map(result.state_history[10])
print(map_viz)

# Generate player movement heatmaps
heatmaps = visualizer.generate_player_heatmaps(result)
visualizer.save_heatmaps(heatmaps, "heatmaps/")

# Analyze impostor strategy
impostor_analysis = visualizer.analyze_impostor_strategy(result)
print(impostor_analysis)

# Analyze voting patterns
voting_analysis = visualizer.analyze_voting_patterns(result)
print(voting_analysis)
```

## Google-Style Docstrings

Here are examples of Google-style docstrings used in the module:

```python
def can_player_see(self, player_id: str, target_id: str) -> bool:
    """Determines if one player can see another player.

    This method calculates whether the player with player_id can see the player
    with target_id based on their locations, the map layout, vision range, and
    line of sight mechanics.

    Args:
        player_id: The ID of the observing player.
        target_id: The ID of the potentially visible player.

    Returns:
        True if the target player is visible to the observing player, False otherwise.

    Raises:
        ValueError: If either player_id or target_id is not found in the state.

    Examples:
        >>> state = AmongUsState(...)
        >>> state.can_player_see("player1", "player2")
        True
        >>> state.can_player_see("player1", "player3")  # Too far or blocked
        False
    """
    # Implementation...
```

```python
class PlayerAction:
    """Represents an action taken by a player in the Among Us game.

    This class encapsulates various actions a player can take during the game,
    including movement, task completion, killing, reporting, and voting.

    Attributes:
        player_id: The ID of the player taking the action.
        action_type: The type of action (move, kill, report, task, vote, etc.).
        target_location: The location to move to (for move actions).
        target_player: The player to target (for kill or vote actions).
        target_task: The task to interact with (for task actions).

    Examples:
        >>> # Create a movement action
        >>> move_action = PlayerAction(
        ...     player_id="player1",
        ...     action_type="move",
        ...     target_location=Location(x=10, y=15)
        ... )
        >>>
        >>> # Create a kill action
        >>> kill_action = PlayerAction(
        ...     player_id="impostor1",
        ...     action_type="kill",
        ...     target_player="crew3"
        ... )
    """

    def __init__(
        self,
        player_id: str,
        action_type: str,
        target_location: Optional[Location] = None,
        target_player: Optional[str] = None,
        target_task: Optional[str] = None
    ):
        """Initializes a PlayerAction.

        Args:
            player_id: The ID of the player taking the action.
            action_type: The type of action being taken.
            target_location: The location to move to (for move actions).
            target_player: The player to target (for kill or vote actions).
            target_task: The task to interact with (for task actions).
        """
        # Implementation...
```

## Integration with Other Modules

### Integration with Agent Variants

```python
from haive.games.among_us import AmongUsAgent, AmongUsConfig
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm import ChatOpenAI, Claude, GPT4, Gemini

# Create configurations for different agent variants
agent_variants = {
    "baseline": AugLLMConfig(
        system_message="You are playing a social deduction game. Use basic reasoning to complete your objectives.",
        temperature=0.5,
        llm=ChatOpenAI()
    ),
    "strategic": AugLLMConfig(
        system_message="You are playing a social deduction game. Use advanced strategic thinking and careful planning.",
        temperature=0.3,
        llm=GPT4()
    ),
    "deceptive": AugLLMConfig(
        system_message="You are playing a social deduction game. You excel at deception and misdirection.",
        temperature=0.7,
        llm=Claude()
    ),
    "analytical": AugLLMConfig(
        system_message="You are playing a social deduction game. You carefully analyze all evidence and make logical deductions.",
        temperature=0.2,
        llm=Gemini()
    )
}

# Run games with different agent compositions
results = []

for _ in range(5):  # Run 5 trials
    # Randomly assign agent types to players
    import random
    player_configs = random.choices(list(agent_variants.values()), k=10)

    # Create and run game
    config = AmongUsConfig(
        num_players=10,
        num_impostors=2,
        player_llm_configs=player_configs
    )

    agent = AmongUsAgent(config)
    result = agent.run()
    results.append(result)

# Analyze results
win_rates = {"crew": 0, "impostors": 0}
for result in results:
    win_rates[result.winner] += 1

print(f"Win rates: Crew {win_rates['crew']/len(results)*100}%, Impostors {win_rates['impostors']/len(results)*100}%")
```

### Integration with Metrics System

```python
from haive.games.among_us import AmongUsAgent, AmongUsConfig
from haive.games.metrics import MetricsCollector

# Create metrics collector
metrics = MetricsCollector()

# Create and run game with metrics
config = AmongUsConfig(num_players=8, num_impostors=2)
agent = AmongUsAgent(config)

# Register metrics to track
metrics.register_metric("task_completion_rate", "Percentage of tasks completed")
metrics.register_metric("correct_suspicion_rate", "Rate of correct suspicions during discussions")
metrics.register_metric("kill_efficiency", "Kills per opportunity for impostors")
metrics.register_metric("deception_success", "Rate at which impostors avoid suspicion")
metrics.register_metric("voting_accuracy", "Percentage of votes that target impostors")

# Run game with metrics
result = agent.run(metrics=metrics)

# Analyze metrics
metrics_report = metrics.generate_report()
print(metrics_report)

# Generate visualizations
metrics.plot_metrics("among_us_metrics.png")
```

## Best Practices

- **Map Design**: Create maps with strategic choke points and visibility constraints
- **Role Balance**: Adjust number of impostors based on player count (1:4-5 ratio)
- **Task Distribution**: Distribute tasks across the map for strategic movement
- **Information Flow**: Control information visibility for balanced gameplay
- **Discussion Prompting**: Design discussion prompts to elicit strategic reasoning
- **AI Persona**: Create consistent AI personalities across game phases
- **Social Dynamics**: Encourage alliances, suspicion, and social interaction
- **Memory Management**: Ensure agents can recall and use past observations

## API Reference

For full API details, see the [documentation](https://docs.haive.ai/games/among_us).

## Related Modules

- **haive.games.framework**: Core framework used by the Among Us implementation
- **haive.games.debate**: Discussion mechanisms shared with debate games
- **haive.core.engine**: Engine components used by Among Us agents
