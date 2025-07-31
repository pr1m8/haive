# Round Robin Conversation

Sequential turn-based multi-agent dialogue with automatic round tracking and balanced participation.

## Overview

The Round Robin Conversation agent implements a simple yet effective conversation pattern where participants speak in a fixed, predictable order. Each participant gets exactly one turn per round, ensuring fair and balanced participation across all agents. This conversation type is ideal for panel discussions, structured interviews, and scenarios requiring equal speaking opportunities.

## Architecture

```
RoundRobinConversation (extends BaseConversationAgent)
├── Sequential Speaker Selection
├── Automatic Round Progression
├── Turn Equality Enforcement
└── Progress Tracking & Analytics
```

## Key Features

- **Fixed speaking order** - Participants speak in the same sequence each round
- **Guaranteed turn equality** - Each participant gets exactly one turn per round
- **Automatic round tracking** - Built-in round counting and progress monitoring
- **Simple configuration** - Minimal setup required for basic conversations
- **Flexible round limits** - Configure maximum rounds or let conversations run
- **Progress visualization** - Real-time tracking of conversation advancement
- **Easy integration** - Works seamlessly with any Haive agent type

## Installation

This module is part of the `haive-agents` package. Install it using:

```bash
pip install haive-agents[conversation]
```

## Quick Start

### Basic Usage

```python
from haive.agents.conversation import RoundRobinConversation
from haive.agents.simple import SimpleAgent

# Create participants
alice = SimpleAgent(name="Alice", model="gpt-4o-mini")
bob = SimpleAgent(name="Bob", model="gpt-4o-mini")
charlie = SimpleAgent(name="Charlie", model="gpt-4o-mini")

# Create round-robin conversation
conversation = RoundRobinConversation(
    participants=[alice, bob, charlie],
    topic="The future of renewable energy",
    max_rounds=3
)

# Run the conversation
result = await conversation.arun()

# Access results
messages = result["messages"]
final_state = result["conversation_state"]
```

### Factory Method

```python
from haive.agents.conversation import create_round_robin_conversation

# Quick creation with factory function
conversation = create_round_robin_conversation(
    participants=[alice, bob, charlie],
    topic="AI in healthcare",
    max_rounds=5,
    enable_speaker_announcements=True
)
```

## Configuration Options

### Core Parameters

- `participants` (List[Agent]): List of agents participating in the conversation
- `topic` (str): Conversation topic or subject
- `max_rounds` (int): Maximum number of rounds (default: 10)
- `enable_speaker_announcements` (bool): Announce speaker changes
- `initial_message` (str): Optional opening message to start conversation

### Advanced Configuration

```python
from haive.agents.conversation.round_robin import RoundRobinConversation

conversation = RoundRobinConversation(
    participants=participants,
    topic="Climate change solutions",
    max_rounds=5,
    config={
        "enable_speaker_announcements": True,
        "include_round_context": True,  # Add round info to prompts
        "allow_skip_unavailable": True,  # Skip if agent unavailable
        "min_response_length": 50,       # Minimum words per response
        "save_conversation_history": True # Persist conversation
    }
)
```

## Speaker Selection Logic

The round-robin agent uses a simple modulo-based selection:

```python
def select_next_speaker(self, state: ConversationState) -> Optional[str]:
    """Select next speaker in sequence."""
    if state.remaining_speakers_this_round:
        # Return first remaining speaker (maintains order)
        return state.remaining_speakers_this_round[0]
    return None  # Round complete
```

## Conversation Flow

1. **Initialization**: Set up participants and speaking order
2. **Round Start**: Begin new round with first speaker
3. **Sequential Turns**: Each participant speaks once in order
4. **Round Completion**: Mark round complete after all speak
5. **Progress Check**: Evaluate termination conditions
6. **Repeat or End**: Start new round or conclude conversation

## State Management

The round-robin conversation leverages the base `ConversationState` with automatic tracking:

```python
# State automatically tracks:
- turn_count: Total turns taken (auto-incremented)
- speaker_history: Order of speakers (auto-appended)
- round_number: Current round (computed property)
- remaining_speakers_this_round: Who hasn't spoken yet
- conversation_progress: Percentage complete
```

## Advanced Usage

### Custom Round-Robin Implementation

```python
class CustomRoundRobinAgent(RoundRobinConversation):
    """Extended round-robin with custom features."""

    def should_skip_speaker(self, speaker: str, state: ConversationState) -> bool:
        """Conditionally skip speakers based on context."""
        # Skip if speaker has been inactive
        if self.is_speaker_inactive(speaker):
            return True

        # Skip if topic expertise doesn't match
        if not self.matches_expertise(speaker, state.topic):
            return True

        return False

    def format_speaker_prompt(self, speaker: str, state: ConversationState) -> str:
        """Customize prompts for each speaker."""
        base_prompt = super().format_speaker_prompt(speaker, state)

        # Add round context
        round_info = f"\n[Round {state.round_number} of {state.max_rounds}]"

        # Add previous speaker context
        if state.speaker_history:
            prev_speaker = state.speaker_history[-1]
            round_info += f"\n[Following {prev_speaker}'s comments]"

        return base_prompt + round_info
```

### With Dynamic Participants

```python
# Start with initial participants
conversation = RoundRobinConversation(
    participants=[alice, bob],
    topic="Technology trends",
    max_rounds=5
)

# Add participant mid-conversation
await conversation.add_participant(charlie, join_next_round=True)

# Remove participant
await conversation.remove_participant("Bob", complete_current_round=True)
```

## Integration Examples

### With Logging and Analytics

```python
import logging
from haive.agents.conversation import RoundRobinConversation

# Configure logging
logging.basicConfig(level=logging.INFO)

class AnalyticsRoundRobin(RoundRobinConversation):
    """Round-robin with conversation analytics."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.turn_times = []
        self.response_lengths = []

    async def execute_agent(self, agent, input_data, state):
        """Track execution metrics."""
        import time

        start_time = time.time()
        response = await super().execute_agent(agent, input_data, state)
        execution_time = time.time() - start_time

        # Record metrics
        self.turn_times.append(execution_time)
        self.response_lengths.append(len(response.split()))

        # Log turn info
        logger.info(
            f"Turn {state.turn_count}: {agent.name} "
            f"({execution_time:.2f}s, {len(response.split())} words)"
        )

        return response

    def get_analytics(self):
        """Get conversation analytics."""
        return {
            "average_turn_time": sum(self.turn_times) / len(self.turn_times),
            "average_response_length": sum(self.response_lengths) / len(self.response_lengths),
            "total_duration": sum(self.turn_times)
        }
```

### With Persistence

```python
from haive.core.persistence import ConversationStore

# Create conversation with persistence
conversation = RoundRobinConversation(
    participants=[alice, bob, charlie],
    topic="Future of work",
    max_rounds=5,
    persistence_config={
        "store": ConversationStore("redis://localhost"),
        "save_frequency": "every_round",
        "conversation_id": "future_work_discussion_001"
    }
)

# Resume later
resumed_conversation = RoundRobinConversation.load_from_store(
    conversation_id="future_work_discussion_001",
    store=ConversationStore("redis://localhost")
)
```

## Best Practices

### 1. Participant Selection

- Choose participants with complementary perspectives
- Ensure agents have distinct personalities or expertise
- Consider participant count vs. round limit

### 2. Topic Framing

- Provide clear, engaging topics
- Include enough context for meaningful discussion
- Consider topic complexity vs. round limit

### 3. Round Configuration

- 3-5 rounds for focused discussions
- 5-10 rounds for exploratory conversations
- Adjust based on participant count

### 4. Response Quality

- Set minimum response lengths if needed
- Provide clear instructions to participants
- Consider adding quality checks

### 5. Error Handling

- Implement fallbacks for agent failures
- Consider skip strategies for unavailable agents
- Log errors without breaking conversation flow

## Common Use Cases

1. **Panel Discussions**
   - Equal speaking time for all panelists
   - Structured exploration of topics
   - Balanced perspective presentation

2. **Educational Scenarios**
   - Student discussion simulations
   - Socratic dialogue patterns
   - Peer learning exercises

3. **Meeting Simulations**
   - Daily standup patterns
   - Round-table discussions
   - Status update meetings

4. **Creative Brainstorming**
   - Idea generation sessions
   - Story continuation games
   - Collaborative problem-solving

## Examples

See the [example.py](example.py) file for a complete working example with:

- Basic round-robin setup
- Progress tracking
- Custom termination conditions
- Analytics integration

## API Reference

For detailed API documentation, see the [API Reference](../../../../docs/source/api/haive/agents/conversation/round_robin/index.rst).

## See Also

- [Base Conversation Agent](../base/README.md) - Core conversation infrastructure
- [Directed Conversation](../directed/README.md) - Moderator-controlled alternative
- [Debate Conversation](../debate/README.md) - Structured argumentative format
- [Collaborative Conversation](../collaberative/README.md) - Team-based problem solving
- [Social Media Conversation](../social_media/README.md) - Platform-style interactions
