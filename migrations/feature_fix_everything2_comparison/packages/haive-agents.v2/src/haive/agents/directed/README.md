# Directed Conversation

Mention-based multi-agent dialogue with targeted responses and natural conversation flow.

## Overview

The Directed Conversation agent implements a natural conversation pattern where participants respond to mentions, questions, and contextual cues. Unlike round-robin conversations, speakers engage only when addressed or when the context naturally calls for their input. This creates more organic, purposeful discussions similar to real-world meetings, classrooms, or collaborative sessions.

## Architecture

```
DirectedConversation (extends BaseConversationAgent)
├── Mention Detection System
│   ├── Direct Mentions (@name)
│   ├── Name References (name, name:)
│   └── Question Targeting
├── Structured Speaker Selection
│   ├── Mention-based Priority
│   ├── Fallback Strategies
│   └── Least-Active Selection
├── Interaction Tracking
│   ├── Speaker Relationships
│   ├── Mention Patterns
│   └── Engagement Metrics
└── Context-Aware Response Generation
```

## Key Features

- **Natural mention detection** - Multiple patterns for detecting when someone is addressed
- **Structured output models** - Type-safe mention and selection tracking
- **Flexible fallback strategies** - Round-robin or least-active when no mentions
- **Interaction tracking** - Monitor who talks to whom and how often
- **Context-aware responses** - Agents know why they're speaking
- **Self-mention prevention** - Avoid speakers selecting themselves
- **Configurable patterns** - Customize mention detection for your use case
- **Priority-based selection** - Different mention types have different weights

## Installation

This module is part of the `haive-agents` package. Install it using:

```bash
pip install haive-agents[conversation]
```

## Quick Start

### Basic Directed Conversation

```python
from haive.agents.conversation import DirectedConversation
from haive.agents.simple import SimpleAgent

# Create participants
manager = SimpleAgent(name="Manager", role="facilitator")
developer = SimpleAgent(name="Developer", role="technical")
designer = SimpleAgent(name="Designer", role="creative")

# Create directed conversation
meeting = DirectedConversation(
    participants=[manager, developer, designer],
    topic="New Feature Planning",
    max_rounds=5
)

# Start with manager directing questions
result = await meeting.arun(
    "Manager: Let's discuss the new dashboard feature. "
    "@Developer, what's the technical feasibility?"
)
```

### Classroom-Style Discussion

```python
from haive.agents.conversation import DirectedConversation

# Use the classroom factory
classroom = DirectedConversation.create_classroom(
    teacher_name="Ms. Johnson",
    student_names=["Alice", "Bob", "Charlie", "Diana"],
    topic="The American Revolution",
    max_rounds=4
)

# Run the discussion
result = await classroom.arun()
```

## Mention Detection Patterns

The system recognizes several mention patterns:

### 1. Direct Mentions (@name)

- **Pattern**: `@Alice`
- **Priority**: Highest
- **Example**: "Great point! @Alice, what's your perspective?"

### 2. Name References

- **Pattern**: `Alice,` or `Alice:`
- **Priority**: High
- **Example**: "Alice, could you elaborate on that?"

### 3. Question Targets

- **Pattern**: Questions directed at specific people
- **Priority**: High
- **Examples**:
  - "What do you think, Bob?"
  - "How about you, Charlie?"
  - "Diana, what's your opinion?"

### 4. Custom Patterns

```python
from haive.agents.conversation.directed import DirectedConversationConfig

config = DirectedConversationConfig(
    mention_patterns=[
        "@{name}",
        "{name},",
        "{name}:",
        "ask {name}",
        "cc: {name}",
        "{name}, please"
    ]
)

conversation = DirectedConversation(
    participants=agents,
    config=config
)
```

## Configuration Options

### Core Configuration

```python
from haive.agents.conversation.directed import DirectedConversationConfig

config = DirectedConversationConfig(
    mention_patterns=["@{name}", "{name},"],     # Patterns to detect
    fallback_to_round_robin=True,                 # Use round-robin if no mentions
    max_silence_turns=3,                          # Force someone to speak after silence
    allow_self_selection=True,                    # Let agents volunteer
    avoid_self_mentions=True,                     # Prevent self-selection
    prioritize_least_active=True                  # Encourage quiet participants
)
```

### Advanced Parameters

```python
conversation = DirectedConversation(
    participants=agents,
    topic="Project Planning",
    max_rounds=10,
    config={
        "mention_confidence_threshold": 0.8,      # Min confidence for mentions
        "track_interaction_patterns": True,       # Monitor who talks to whom
        "balance_participation": True,            # Encourage equal participation
        "context_window_size": 50,               # Chars around mention for context
        "multi_mention_strategy": "queue"        # How to handle multiple mentions
    }
)
```

## State Management

The DirectedState extends ConversationState with mention-specific tracking:

```python
class DirectedState(ConversationState):
    # Mention tracking
    mentioned_speakers: List[str]        # Who was mentioned in last message
    pending_speakers: List[str]          # Queue of speakers to go next

    # Interaction tracking
    interaction_count: Dict[str, Dict[str, int]]  # Who mentions whom
    silence_count: int                   # Turns without mentions

    # Participation metrics
    last_spoke: Dict[str, int]          # When each speaker last talked
    response_times: Dict[str, List[float]]  # Response latencies
```

## Advanced Usage

### Custom Mention Detection

```python
class CustomDirectedConversation(DirectedConversation):
    """Extended with domain-specific mention patterns."""

    def _extract_structured_mentions(self, state) -> List[SpeakerMention]:
        """Add custom mention detection logic."""
        mentions = super()._extract_structured_mentions(state)

        # Add role-based mentions
        content = state.messages[-1].content
        for speaker, role in self.speaker_roles.items():
            if f"the {role}" in content.lower():
                mentions.append(
                    SpeakerMention(
                        speaker_name=speaker,
                        mention_type=MentionType.ROLE_REFERENCE,
                        confidence=0.7
                    )
                )

        return mentions
```

### Interaction Analytics

```python
class AnalyticsDirectedConversation(DirectedConversation):
    """Track detailed interaction patterns."""

    def get_interaction_report(self) -> Dict[str, Any]:
        """Generate interaction analytics."""
        state = self.get_state()

        # Calculate interaction metrics
        total_mentions = sum(
            sum(targets.values())
            for targets in state.interaction_count.values()
        )

        # Find most active relationships
        relationships = []
        for speaker, targets in state.interaction_count.items():
            for target, count in targets.items():
                relationships.append({
                    "from": speaker,
                    "to": target,
                    "count": count,
                    "strength": count / total_mentions
                })

        # Sort by interaction strength
        relationships.sort(key=lambda x: x["count"], reverse=True)

        return {
            "total_mentions": total_mentions,
            "top_relationships": relationships[:5],
            "participation_balance": self._calculate_balance(state),
            "average_response_time": self._calculate_avg_response_time(state)
        }
```

### Smart Escalation System

```python
# Customer support with intelligent escalation
support_config = DirectedConversationConfig(
    mention_patterns=[
        "@{name}",
        "escalate to {name}",
        "transfer to {name}",
        "need {name}"
    ],
    fallback_to_round_robin=False,  # Don't force participation
    max_silence_turns=1  # Quick escalation if no response
)

support = DirectedConversation(
    participants={
        "Bot": bot_agent,
        "L1_Support": level1_agent,
        "L2_Support": level2_agent,
        "Manager": manager_agent
    },
    topic="Customer Support",
    config=support_config
)
```

## Integration Examples

### With Memory Systems

```python
from haive.memory import ConversationMemory

class MemoryDirectedConversation(DirectedConversation):
    """Directed conversation with memory of past interactions."""

    def __init__(self, *args, memory_store=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.memory = ConversationMemory(store=memory_store)

    def _prepare_agent_input(self, state, agent_name):
        """Add memory context to agent input."""
        base_input = super()._prepare_agent_input(state, agent_name)

        # Retrieve past interactions with current speakers
        if state.mentioned_speakers:
            for mentioned in state.mentioned_speakers:
                past_interactions = self.memory.get_interactions(
                    agent_name, mentioned, limit=3
                )
                if past_interactions:
                    context = f"[Past interactions with {mentioned}: {len(past_interactions)} conversations]"
                    base_input["messages"].insert(0, SystemMessage(content=context))

        return base_input
```

### With Tool Integration

```python
from haive.tools import SearchTool, CalculatorTool

# Technical meeting with tool access
tech_meeting = DirectedConversation(
    participants={
        "Lead": lead_with_search,
        "Engineer": engineer_with_calculator,
        "Analyst": analyst_with_both_tools
    },
    topic="Performance Optimization",
    tools=[SearchTool(), CalculatorTool()],
    config={
        "allow_tool_mentions": True,  # Can mention tools like @SearchTool
        "tool_result_sharing": True   # Share tool results with all
    }
)
```

## Best Practices

### 1. Natural Conversation Flow

- Start with a clear moderator or facilitator
- Use mentions sparingly for natural flow
- Allow organic back-and-forth exchanges
- Don't over-structure the conversation

### 2. Mention Patterns

- Keep patterns simple and intuitive
- Test patterns with your specific use case
- Consider cultural/domain conventions
- Document expected patterns for users

### 3. Participation Balance

- Monitor quiet participants
- Use fallback strategies wisely
- Consider forced participation sparingly
- Track engagement metrics

### 4. Context Management

- Provide clear context for mentions
- Include why someone is being addressed
- Maintain conversation continuity
- Summarize when switching topics

### 5. Error Handling

- Handle missing participants gracefully
- Provide fallbacks for no mentions
- Clear messaging for unclear mentions
- Log interaction patterns for debugging

## Common Use Cases

1. **Team Meetings**
   - Status updates with targeted questions
   - Problem-solving with expert consultation
   - Planning sessions with role-based input
   - Decision-making with stakeholder input

2. **Educational Settings**
   - Classroom discussions with teacher guidance
   - Study groups with peer interaction
   - Tutorials with targeted assistance
   - Q&A sessions with expert panels

3. **Customer Support**
   - Tiered support with escalation
   - Expert consultation on demand
   - Collaborative troubleshooting
   - Handoff between departments

4. **Creative Collaboration**
   - Brainstorming with targeted feedback
   - Story development with character interaction
   - Design reviews with specific critiques
   - Content creation with role-based input

## Performance Considerations

- **Mention Detection**: Regex operations scale with message length
- **Queue Management**: Pending speakers list can grow with mentions
- **Interaction Tracking**: Memory usage increases with conversation length
- **Pattern Matching**: More patterns = more processing per message

## Examples

See the [example.py](example.py) file for complete working examples including:

- Classroom discussions
- Team meetings
- Customer support scenarios
- Interactive storytelling

## API Reference

For detailed API documentation, see the [API Reference](../../../../docs/source/api/haive/agents/conversation/directed/index.rst).

## See Also

- [Base Conversation Agent](../base/README.md) - Core conversation infrastructure
- [Round Robin Conversation](../round_robin/README.md) - Fixed-order alternative
- [Debate Conversation](../debate/README.md) - Structured argumentative format
- [Collaborative Conversation](../collaborative/README.md) - Goal-oriented teamwork
- [Social Media Conversation](../social_media/README.md) - Platform-style interactions
