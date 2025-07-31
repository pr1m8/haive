# LATS v3 - Language Agent Tree Search Implementation

This is a clean, modular implementation of the Language Agent Tree Search (LATS) algorithm using the Haive framework.

## Overview

LATS is a Monte Carlo Tree Search (MCTS) algorithm adapted for language models. It combines:

- **Upper Confidence Bound (UCB)** selection for node expansion
- **Parallel action generation** for diverse exploration
- **Reflection and evaluation** for scoring actions
- **Backpropagation** for updating tree statistics

## Architecture

### Modular Agent Design

Unlike the monolithic LATS implementation, v3 uses a **composition pattern** with specialized agents:

1. **NodeSelector** - Selects best node for expansion using UCB
2. **ActionGenerator** - Generates diverse candidate actions
3. **ReflectionEvaluator** - Scores and reflects on actions
4. **TreeManager** (TODO) - Manages MCTS tree operations
5. **LATSOrchestrator** (TODO) - Coordinates all agents

### Why Composition Over Inheritance?

- Avoids Pydantic forward reference issues
- Each agent is independently testable
- Clear separation of concerns
- Easy to swap implementations
- Better type safety

## Components

### 1. NodeSelector Agent

```python
from haive.agents.reasoning_and_critique.lats.v3.agents.node_selector import NodeSelector

selector = NodeSelector(
    name="ucb_selector",
    exploration_weight=1.4  # UCB exploration parameter
)

# Select best node for expansion
result = await selector.select_node(nodes, problem_description)
```

**Features:**

- UCB score calculation with configurable exploration weight
- Prioritizes unvisited nodes (infinite UCB)
- Clear reasoning for selections
- Structured output with UCBSelection model

### 2. ActionGenerator Agent

```python
from haive.agents.reasoning_and_critique.lats.v3.agents.action_generator import ActionGenerator

generator = ActionGenerator(
    name="action_gen",
    num_candidates=5,     # Number of actions to generate
    temperature=0.7       # Diversity control
)

# Generate candidate actions
result = await generator.generate_actions(
    current_node,
    problem_description,
    search_history
)
```

**Features:**

- Generates diverse candidate actions
- Each action includes reasoning and confidence
- Considers search history to avoid repetition
- Structured output with ActionGeneration model

### 3. ReflectionEvaluator Agent

```python
from haive.agents.reasoning_and_critique.lats.v3.agents.reflection_evaluator import ReflectionEvaluator

evaluator = ReflectionEvaluator(
    name="reflection_eval",
    temperature=0.3  # Lower for consistent evaluation
)

# Evaluate and score actions
result = await evaluator.evaluate_actions(
    current_node,
    candidate_actions,
    problem_description,
    goal_description,
    reflection_history
)
```

**Features:**

- Scores actions from 0.0 to 1.0
- Provides reasoning for each score
- Strategic evaluation considering goal
- Suggests backtracking if all actions are poor

## Data Models

### Tree Models

```python
class LATSNode:
    node_id: str              # Unique identifier
    parent_id: Optional[str]  # Parent node reference
    depth: int                # Tree depth
    action: str               # Action that led here
    state_description: str    # Current state
    visits: int               # MCTS visit count
    reward_sum: float         # Total rewards
    children_ids: List[str]   # Child nodes
    is_terminal: bool         # End state?
    is_solved: bool           # Solution found?
    reflection_score: float   # Evaluation score
    reflection_reasoning: str # Why this score
```

### Action Models

```python
class CandidateAction:
    action: str               # What to do
    reasoning: str            # Why do it
    expected_outcome: str     # What might happen
    confidence: float         # 0.0-1.0 confidence

class ActionGeneration:
    situation_analysis: str
    candidate_actions: List[CandidateAction]
    selection_criteria: str
    diversity_check: str
```

### Evaluation Models

```python
class ScoredAction:
    action: str
    score: float              # 0.0-1.0 evaluation
    reasoning: str            # Why this score
    strategic_value: str      # Goal alignment

class ReflectionEvaluation:
    scored_actions: List[ScoredAction]
    overall_reflection: str
    best_action_index: int
    should_backtrack: bool
    confidence_distribution: str
```

## Usage Example

```python
import asyncio
from haive.agents.reasoning_and_critique.lats.v3.agents import (
    NodeSelector,
    ActionGenerator,
    ReflectionEvaluator
)
from haive.agents.reasoning_and_critique.lats.v3.models import LATSNode

async def run_lats_iteration():
    # Initialize agents
    selector = NodeSelector()
    generator = ActionGenerator()
    evaluator = ReflectionEvaluator()

    # Current search state
    nodes = {
        "node1": LATSNode(...),
        "node2": LATSNode(...),
    }

    problem = "Navigate maze to find treasure"
    goal = "Reach the center of the maze"

    # 1. Select best node for expansion
    selection = await selector.select_node(nodes, problem)
    selected_node = nodes[selection.selected_node_id]

    # 2. Generate candidate actions
    action_gen = await generator.generate_actions(
        selected_node,
        problem
    )

    # 3. Evaluate and score actions
    evaluation = await evaluator.evaluate_actions(
        selected_node,
        action_gen.candidate_actions,
        problem,
        goal
    )

    # 4. Get best action
    best_action = evaluator.get_best_action(evaluation)

    # 5. Execute action and update tree (TODO: TreeManager)
    print(f"Best action: {best_action.action} (score: {best_action.score})")

# Run the example
asyncio.run(run_lats_iteration())
```

## Testing

Each agent can be tested independently:

```bash
# Test individual agents
poetry run python test_node_selector.py
poetry run python test_action_generator.py
poetry run python test_reflection_evaluator.py

# Run all v3 tests
poetry run pytest tests/reasoning_and_critique/lats/v3/ -v
```

## Key Advantages of v3

1. **Modularity**: Each component is independent and reusable
2. **Type Safety**: Full Pydantic models with validation
3. **Testability**: Each agent tested with real LLMs (no mocks)
4. **Flexibility**: Easy to swap agent implementations
5. **Clarity**: Clear separation of concerns
6. **Extensibility**: Add new agents without modifying existing ones

## TODO

- [ ] Implement TreeManager for MCTS operations
- [ ] Create LATSOrchestrator to coordinate agents
- [ ] Add backpropagation logic
- [ ] Implement parallel action execution
- [ ] Create comprehensive examples
- [ ] Performance benchmarking

## References

- [LATS Paper](https://arxiv.org/abs/2310.04406)
- [LangGraph LATS Tutorial](https://langchain-ai.github.io/langgraph/tutorials/lats/)
- Monte Carlo Tree Search (MCTS) algorithm
