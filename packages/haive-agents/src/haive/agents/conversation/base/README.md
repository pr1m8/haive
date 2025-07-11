# Base Conversation Agent

Core foundation classes for conversation agents that orchestrate multi-agent interactions with automatic state tracking, phase-based management, and extensible graph-based conversation flow.

## Overview

The base conversation system provides the foundation for all conversation agent types in the Haive framework. It implements robust multi-agent conversation orchestration with reducer-based automatic state tracking, computed properties for conversation analysis, and seamless integration with the Haive core systems.

## Architecture

```
BaseConversationAgent (Abstract)
├── Speaker Selection Logic
├── Agent Execution & Error Handling
├── Extension Hooks for Customization
└── Graph-Based Workflow Integration

ConversationState (Extends MessagesState)
├── Automatic Turn & Round Tracking
├── Speaker History Management
├── Computed Progress Properties
└── Reducer-Based State Updates
```

## Key Features

- **Multi-agent orchestration** with automatic turn management
- **Reducer-based state tracking** for rounds and speaker history
- **Phase-based conversation management** with customizable flow control
- **Message routing and agent execution** with comprehensive error handling
- **Extensible graph-based workflow** for complex conversation patterns
- **Computed properties** for real-time conversation progress analysis
- **Seamless integration** with Haive core schema and graph systems

## Installation

This module is part of the `haive-agents` package. Install it using:

```bash
pip install haive-agents[conversation]
```

## Quick Start

### Basic Usage

```python
from haive.agents.conversation.base import ConversationState, create_conversation_state
from haive.agents.simple import SimpleAgent

# Create conversation state with automatic tracking
state = create_conversation_state(
    participants=[
        SimpleAgent(name="Alice"),
        SimpleAgent(name="Bob"),
        SimpleAgent(name="Charlie")
    ],
    topic="Future of AI",
    max_rounds=5
)

# State automatically tracks progress
print(f"Round {state.round_number}, Turn {state.turn_count}")
print(f"Progress: {state.conversation_progress:.1%}")
print(f"Remaining speakers: {state.remaining_speakers_this_round}")
```

### Extending BaseConversationAgent

```python
from haive.agents.conversation.base import BaseConversationAgent, ConversationState
from typing import Optional

class CustomConversationAgent(BaseConversationAgent[ConversationState]):
    """Custom conversation agent with specialized behavior."""

    def select_next_speaker(self, state: ConversationState) -> Optional[str]:
        """Custom speaker selection logic."""
        # Simple round-robin selection
        if state.remaining_speakers_this_round:
            return state.remaining_speakers_this_round[0]
        return None

    def should_end_conversation(self, state: ConversationState) -> bool:
        """Custom termination conditions."""
        return (
            state.should_end_by_rounds or
            len(state.messages) > 50 or
            state.conversation_ended
        )

# Use the custom agent
async def run_custom_conversation():
    agent = CustomConversationAgent(
        name="custom_conversation",
        participants=[alice, bob, charlie],
        initial_state=state
    )

    result = await agent.arun("Let's discuss the future of AI")
    return result
```

## State Management

### ConversationState Fields

```python
class ConversationState(MessagesState):
    # Core conversation tracking
    current_speaker: Optional[str]           # Currently active speaker
    speakers: List[str]                      # All participant names
    turn_count: int                          # Auto-incremented via reducer
    speaker_history: List[str]               # Auto-appended via reducer

    # Configuration
    max_rounds: int                          # Round limit
    topic: Optional[str]                     # Conversation topic
    conversation_ended: bool                 # Termination flag
    mode: str                               # Conversation mode identifier

    # Computed properties (automatic)
    round_number: int                        # Current round (calculated)
    current_round_speakers: List[str]        # Speakers in current round
    remaining_speakers_this_round: List[str] # Remaining speakers
    should_end_by_rounds: bool              # Round limit reached
    turns_per_round: int                    # Expected turns per round
    conversation_progress: float            # Progress percentage (0.0-1.0)
```

### Reducer Functions

The state uses reducer functions for automatic updates:

```python
__reducer_fields__ = {
    "messages": add_messages,        # Inherited from MessagesState
    "turn_count": operator.add,      # Auto-increment turns
    "speaker_history": operator.add, # Append speaker history
}

# Example state update
new_state = state.model_copy(update={
    "turn_count": 1,                 # Automatically increments
    "speaker_history": ["Alice"],    # Automatically appends
})
```

## Utility Functions

### Creating Conversation States

```python
from haive.agents.conversation.base import create_conversation_state

# Basic conversation state
state = create_conversation_state(
    participants=[alice, bob, charlie],
    topic="Climate change solutions",
    max_rounds=8
)

# With custom configuration
state = create_conversation_state(
    participants=[expert1, expert2],
    topic="Technical discussion",
    mode="expert_panel",
    config={
        "timeout_seconds": 300,
        "enable_progress_tracking": True
    }
)
```

### Validating Participants

```python
from haive.agents.conversation.base import validate_conversation_participants

try:
    validate_conversation_participants([alice, bob, charlie])
    print("✓ All participants valid")
except ValueError as e:
    print(f"✗ Validation failed: {e}")
```

### Progress Tracking

```python
from haive.agents.conversation.base import get_conversation_progress

progress_info = get_conversation_progress(state)
print(f"Round: {progress_info['round_number']}")
print(f"Progress: {progress_info['progress_percentage']:.1f}%")
print(f"Messages: {progress_info['total_messages']}")
print(f"Should end: {progress_info['should_end']}")
```

## Examples

See the `examples/` directory for comprehensive usage examples:

- [Basic State Management](examples/basic_state_management.py)
- [Custom Agent Implementation](examples/custom_agent_implementation.py)
- [Progress Tracking](examples/progress_tracking.py)
- [Error Handling](examples/error_handling.py)

## API Reference

For detailed API documentation, see the [API Reference](../../../../docs/source/api/haive/agents/conversation/base/index.rst).

## See Also

- [Round Robin Conversation](../round_robin/README.md) - Sequential turn-taking
- [Debate Conversation](../debate/README.md) - Structured argumentative dialogue
- [Directed Conversation](../directed/README.md) - Moderator-controlled flow
- [Collaborative Conversation](../collaberative/README.md) - Team-based problem solving
- [Social Media Conversation](../social_media/README.md) - Platform-style interactions
