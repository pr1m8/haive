# Among_Us Agent Examples

Real examples and outputs from the among_us agent.

## among_us_README

**Source**: `packages/haive-games/src/haive/games/among_us/README.md`

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
print(f"Game length: {resu

... (truncated)


---

```
