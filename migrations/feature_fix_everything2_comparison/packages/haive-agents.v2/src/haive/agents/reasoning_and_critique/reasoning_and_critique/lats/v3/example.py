"""Example of using LATS v3 with EnhancedMultiAgentV4 orchestration.

This example demonstrates the complete LATS implementation using the
same patterns as TOT v2 and Self-Discover v2.
"""
from __future__ import annotations

import asyncio

from haive.agents.reasoning_and_critique.lats.v3.lats_orchestrator import (
    create_lats_orchestrator, )
from haive.agents.reasoning_and_critique.lats.v3.models.tree_models import LATSNode


async def solve_maze_problem():
    """Example: Solve a maze navigation problem using LATS."""
    problem = 'Navigate through a complex maze to find the treasure chest'
    goal = 'Find the optimal path to the treasure while avoiding traps'

    # Create the LATS orchestrator
    orchestrator = create_lats_orchestrator(
        problem=problem,
        goal=goal,
        name='maze_solver',
        max_iterations=20,
        max_depth=7,
        exploration_weight=1.4,
        num_candidates=3,
    )

    # Run the LATS algorithm
    solution = await orchestrator.solve()

    # Display results

    if solution['best_path']:
        for _i, _node in enumerate(solution['best_path']):
            pass

    if solution['solution']:
        pass
    else:
        pass


async def solve_math_problem():
    """Example: Solve a complex math problem using LATS."""
    problem = """
    A farmer has chickens and cows. The total number of animals is 35.
    The total number of legs is 94. How many chickens and cows does the farmer have?
    """

    goal = 'Find the exact number of chickens and cows'

    # Create LATS orchestrator with custom configuration
    orchestrator = create_lats_orchestrator(
        problem=problem,
        goal=goal,
        name='math_solver',
        max_iterations=15,
        max_depth=5,
        exploration_weight=1.2,  # Lower exploration for math problems
        num_candidates=4,  # More candidates for diverse approaches
    )

    # Solve the problem
    solution = await orchestrator.solve()

    # Show the solution process
    if solution['search_history']:
        for _i, step in enumerate(
                solution['search_history'][:5]):  # Show first 5 steps
            if 'selected_node' in step:
                pass
            if 'action' in step:
                pass
            if 'evaluation' in step:
                pass

    if solution['solution']:
        pass


async def test_lats_components():
    """Test individual LATS components without full orchestration."""
    from haive.agents.reasoning_and_critique.lats.v3.agents.action_generator import (
        ActionGenerator, )
    from haive.agents.reasoning_and_critique.lats.v3.agents.node_selector import (
        NodeSelector, )
    from haive.agents.reasoning_and_critique.lats.v3.agents.reflection_evaluator import (
        ReflectionEvaluator, )

    # Test data
    problem = 'Plan a trip to Japan'
    goal = 'Create a 7-day itinerary'

    # Create test nodes
    nodes = {
        'tokyo':
        LATSNode(
            node_id='tokyo',
            action='Start in Tokyo',
            state_description='Capital city with modern attractions',
            visits=3,
            reward_sum=2.1,
            depth=1,
        ),
        'kyoto':
        LATSNode(
            node_id='kyoto',
            action='Visit Kyoto',
            state_description='Historical city with temples',
            visits=0,  # Unvisited
            reward_sum=0.0,
            depth=1,
        ),
        'osaka':
        LATSNode(
            node_id='osaka',
            action='Explore Osaka',
            state_description='Food capital with vibrant culture',
            visits=1,
            reward_sum=0.8,
            depth=1,
        ),
    }

    # Test NodeSelector
    selector = NodeSelector()
    selection = await selector.select_node(nodes, problem, debug=False)

    # Test ActionGenerator
    generator = ActionGenerator()
    selected_node = nodes[selection.selected_node_id]
    actions = await generator.generate_actions(selected_node, problem)
    for _i, _action in enumerate(actions.candidate_actions[:3], 1):
        pass

    # Test ReflectionEvaluator
    evaluator = ReflectionEvaluator()
    await evaluator.evaluate_actions(
        selected_node,
        actions.candidate_actions,
        problem,
        goal,
    )


async def main():
    """Run all examples."""
    # Test individual components first
    await test_lats_components()

    # Run maze solving example
    await solve_maze_problem()

    # Run math problem example
    await solve_math_problem()


if __name__ == '__main__':
    asyncio.run(main())
