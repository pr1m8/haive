# Debate Conversation

Structured argumentative multi-agent dialogue with formal positions, rebuttals, and optional judging.

## Overview

The Debate Conversation agent implements formal debate structures where participants argue from assigned positions following multi-phase conversational formats. This includes opening statements, main arguments, rebuttals, closing statements, and optional judging with scoring. The system supports multiple debate formats (traditional, Oxford, parliamentary, Lincoln-Douglas) and provides comprehensive argument tracking and evaluation capabilities.

## Architecture

```
DebateConversation (extends BaseConversationAgent)
├── Position Management (Pro/Con/Judge)
├── Phase-Based Flow Control
├── Argument & Rebuttal Tracking
├── Scoring & Evaluation System
└── Multiple Debate Formats
```

## Key Features

- **Multiple debate formats** - Traditional, Oxford, Parliamentary, Lincoln-Douglas, Policy
- **Position-based roles** - Clear assignment of pro/con positions with optional judges
- **Phase management** - Opening, arguments, cross-examination, rebuttals, closing, judging
- **Argument tracking** - Track arguments, counter-arguments, and evidence per position
- **Scoring system** - Optional judging with customizable scoring criteria
- **Time management** - Configurable time limits per phase and speaker
- **Evidence handling** - Support for citations and fact-based arguments
- **Flexible team sizes** - One-on-one or team-based debates

## Installation

This module is part of the `haive-agents` package. Install it using:

```bash
pip install haive-agents[conversation]
```

## Quick Start

### Basic Two-Sided Debate

```python
from haive.agents.conversation import DebateConversation, create_debate
from haive.agents.simple import SimpleAgent

# Create debate participants
pro_agent = SimpleAgent(name="Proponent", role="advocate")
con_agent = SimpleAgent(name="Opponent", role="critic")
judge_agent = SimpleAgent(name="Judge", role="evaluator")

# Create structured debate
debate = create_debate(
    topic="Artificial Intelligence should be regulated by government",
    pro_agents=[pro_agent],
    con_agents=[con_agent],
    judge_agent=judge_agent,
    debate_format="traditional",
    rounds=3
)

# Run the debate
result = await debate.arun()

# Access results
winner = result["debate_winner"]
scores = result["argument_scores"]
summary = result["debate_summary"]
```

### Oxford-Style Team Debate

```python
from haive.agents.conversation import create_oxford_debate

# Create debate teams
pro_team = [ai_researcher, tech_optimist, futurist]
con_team = [ethicist, policy_expert, safety_advocate]

# Create Oxford debate
debate = create_oxford_debate(
    topic="This house believes AI will solve climate change",
    pro_team=pro_team,
    con_team=con_team,
    moderator=debate_moderator
)

# Run with audience voting
result = await debate.arun(enable_audience_voting=True)
```

## Debate Formats

### Traditional Debate

- Opening statements (2 min each)
- Main arguments (3 rounds, 3 min each)
- Rebuttals (2 rounds, 2 min each)
- Closing statements (2 min each)
- Optional judge evaluation

### Oxford Debate

- Motion announcement
- Opening statements by first speakers
- Second speaker arguments
- Third speaker rebuttals
- Summary speeches
- Audience/judge voting

### Parliamentary Debate

- Government vs. Opposition format
- Points of information allowed
- Prime Minister and Leader of Opposition roles
- Whip speeches
- Speaker of the House moderation

### Lincoln-Douglas Debate

- Value-based philosophical arguments
- Affirmative and Negative positions
- Cross-examination periods
- Focus on moral/ethical frameworks
- Individual (not team) format

## Configuration Options

### Core Parameters

```python
debate = DebateConversation(
    topic="Resolution text",
    pro_agents=[...],           # Agents arguing FOR
    con_agents=[...],           # Agents arguing AGAINST
    judge_agent=judge,          # Optional judge/evaluator
    debate_format="oxford",     # Format selection
    config={
        "rounds": 3,                    # Number of argument rounds
        "time_limits": {                # Time per phase (seconds)
            "opening": 120,
            "argument": 180,
            "rebuttal": 120,
            "closing": 120
        },
        "scoring_criteria": [           # Judge evaluation criteria
            "logic_consistency",
            "evidence_quality",
            "persuasiveness",
            "rebuttal_effectiveness"
        ],
        "enable_cross_examination": True,
        "allow_interruptions": False,
        "track_evidence": True
    }
)
```

## State Management

The DebateState extends ConversationState with debate-specific tracking:

```python
class DebateState(ConversationState):
    # Position tracking
    pro_agents: List[str]
    con_agents: List[str]
    judge_agent: Optional[str]

    # Debate phases
    current_phase: DebatePhase
    completed_phases: List[DebatePhase]

    # Argument tracking
    pro_arguments: List[Argument]
    con_arguments: List[Argument]
    rebuttals: Dict[str, List[Rebuttal]]

    # Scoring
    argument_scores: Dict[str, float]
    position_scores: Dict[str, float]
    debate_winner: Optional[str]

    # Evidence tracking
    citations: List[Citation]
    fact_checks: Dict[str, bool]
```

## Advanced Usage

### Custom Scoring System

```python
class CustomScoringDebate(DebateConversation):
    """Debate with custom scoring logic."""

    def score_argument(self, argument: Argument, position: str) -> float:
        """Custom argument scoring based on multiple factors."""
        base_score = 5.0

        # Evidence bonus
        if argument.has_citations:
            base_score += 2.0

        # Length penalty (encourage conciseness)
        if len(argument.content.split()) > 500:
            base_score -= 1.0

        # Logical structure bonus
        if self.has_clear_premises(argument):
            base_score += 1.5

        # Rebuttal consideration
        rebuttal_score = self.calculate_rebuttal_impact(argument)
        base_score -= rebuttal_score

        return max(0, min(10, base_score))

    def determine_winner(self, state: DebateState) -> str:
        """Custom winner determination logic."""
        # Weight different criteria
        weights = {
            "argument_quality": 0.4,
            "rebuttal_effectiveness": 0.3,
            "evidence_strength": 0.2,
            "persuasiveness": 0.1
        }

        pro_score = self.calculate_weighted_score("pro", weights)
        con_score = self.calculate_weighted_score("con", weights)

        return "pro" if pro_score > con_score else "con"
```

### Multi-Judge Panel

```python
# Create multiple judges with different expertise
judges = {
    "logic_judge": SimpleAgent(name="Dr. Logic", expertise="logical_consistency"),
    "evidence_judge": SimpleAgent(name="Prof. Facts", expertise="evidence_quality"),
    "rhetoric_judge": SimpleAgent(name="Ms. Persuasion", expertise="rhetorical_effectiveness")
}

debate = DebateConversation(
    topic="Universal Basic Income is necessary",
    pro_agents=[economist, social_worker],
    con_agents=[business_owner, policy_analyst],
    judge_panel=judges,  # Multiple judges
    scoring_method="weighted_panel"  # Aggregate scores
)
```

### Dynamic Debate Flow

```python
class AdaptiveDebate(DebateConversation):
    """Debate that adapts based on argument quality."""

    def should_extend_phase(self, state: DebateState) -> bool:
        """Extend phase if arguments are particularly engaging."""
        recent_scores = state.argument_scores[-3:]
        avg_score = sum(recent_scores) / len(recent_scores)

        # Extend if high-quality exchange
        return avg_score > 8.0

    def select_next_speaker(self, state: DebateState) -> str:
        """Prioritize speakers who haven't addressed key points."""
        unaddressed_points = self.find_unaddressed_arguments(state)

        if unaddressed_points:
            # Select speaker best suited to address gaps
            return self.match_speaker_to_points(unaddressed_points, state)

        return super().select_next_speaker(state)
```

## Integration Examples

### With Research Tools

```python
from haive.tools.search import SearchTool
from haive.tools.fact_check import FactChecker

# Create debate with research capabilities
research_debate = DebateConversation(
    topic="Gene editing will eliminate genetic diseases",
    pro_agents=[scientist_with_search],
    con_agents=[ethicist_with_research],
    tools=[SearchTool(), FactChecker()],
    config={
        "allow_real_time_research": True,
        "fact_check_claims": True,
        "require_citations": True
    }
)
```

### With Audience Interaction

```python
class InteractiveDebate(DebateConversation):
    """Debate with audience participation."""

    def __init__(self, *args, audience_agents=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.audience_agents = audience_agents or []
        self.audience_reactions = []

    async def after_argument(self, argument: Argument, state: DebateState):
        """Collect audience reactions after each argument."""
        reactions = await self.poll_audience(argument)
        self.audience_reactions.append(reactions)

        # Adjust debate flow based on audience engagement
        if reactions["confusion_level"] > 0.7:
            # Request clarification
            state.next_action = "clarification_needed"
```

## Best Practices

### 1. Topic Selection

- Choose clear, debatable resolutions
- Avoid overly broad or narrow topics
- Ensure both sides have viable arguments
- Frame as clear propositions

### 2. Participant Preparation

- Assign clear position instructions
- Provide relevant background knowledge
- Set argument quality expectations
- Define evidence standards

### 3. Format Configuration

- Match format to topic complexity
- Allow sufficient time per phase
- Balance argument and rebuttal time
- Consider audience and purpose

### 4. Scoring Fairness

- Use consistent evaluation criteria
- Weight multiple factors
- Consider argument quality over quantity
- Account for position difficulty

### 5. Evidence Standards

- Require citations for factual claims
- Enable fact-checking when possible
- Track evidence quality
- Penalize unsupported assertions

## Common Use Cases

1. **Educational Debates**
   - Student learning exercises
   - Critical thinking development
   - Perspective exploration
   - Argumentation practice

2. **Policy Analysis**
   - Policy proposal evaluation
   - Impact assessment debates
   - Stakeholder perspective simulation
   - Decision support discussions

3. **Research Debates**
   - Scientific hypothesis discussion
   - Methodology debates
   - Theory comparison
   - Peer review simulation

4. **Business Strategy**
   - Strategic option evaluation
   - Risk/benefit analysis
   - Market approach debates
   - Innovation discussions

## Example Outputs

The module includes several example debate outputs in the `outputs/` directory:

- [Simple Debate](outputs/simple_debate.md) - Basic two-agent debate
- [Oxford Debate](outputs/oxford_debate.md) - Formal Oxford-style team debate
- [Panel Debate](outputs/panel_debate.md) - Multi-participant panel format
- [Socratic Debate](outputs/socratic_debate.md) - Question-driven philosophical debate

## Performance Considerations

- **Token Usage**: Debates can be token-intensive; consider limits
- **Context Windows**: Long debates may exceed context limits
- **Scoring Complexity**: Complex scoring increases computation
- **Real-time Constraints**: Consider time limits for live debates

## Examples

See the [example.py](example.py) file for complete working examples including:

- Basic debate setup
- Oxford-style debates
- Custom scoring systems
- Multi-judge panels
- Advanced debate formats

## API Reference

For detailed API documentation, see the [API Reference](../../../../docs/source/api/haive/agents/conversation/debate/index.rst).

## See Also

- [Base Conversation Agent](../base/README.md) - Core conversation infrastructure
- [Directed Conversation](../directed/README.md) - Moderated discussion alternative
- [Round Robin Conversation](../round_robin/README.md) - Equal participation format
- [Collaborative Conversation](../collaberative/README.md) - Cooperative problem solving
- [Social Media Conversation](../social_media/README.md) - Platform-style discussions
