# Conversation Agent Examples

Real examples and outputs from the conversation agent.

## conversation_README

**Source**: `packages/haive-agents/src/haive/agents/conversation/collaberative/README.md`

# Collaborative Conversation

Structured multi-agent collaboration for building shared documents, plans, and creative content.

## Overview

The Collaborative Conversation agent orchestrates multiple participants working together to create shared content in a structured, section-based format. Unlike free-form conversations, this agent guides participants through defined sections, ensures balanced contributions, and compiles a cohesive final document. It's ideal for brainstorming sessions, code reviews, project planning, and any scenario requiring structured collaborative output.

## Architecture

```
CollaborativeConversation (extends BaseConversationAgent)
├── Document Structure Management
│   ├── Section Definition & Ordering
│   ├── Progress Tracking
│   └── Document Compilation
├── Contribution System
│   ├── Per-Section Tracking
│   ├── Balanced Participation
│   └── Attribution Management
├── Output Formatting
│   ├── Markdown
│   ├── Code
│   ├── Outline
│   └── Report
└── Review & Approval (Optional)
    ├── Section Completion
    ├── Revision Support
    └── Final Approval
```

## Key Features

- **Structured sections** - Organize collaboration into defined sections
- **Balanced contributions** - Ensure everyone participates in each section
- **Multiple output formats** - Markdown, code, outline, or report styles
- **Attribution tracking** - Know who contributed what
- **Progress monitoring** - Track completion of sections and contributions
- **Flexible workflows** - Support for revisions and approvals
- **Document compilation** - Automatic assembly of final output
- **Smart speaker selection** - Prioritize those who haven't contributed to current section

## Installation

This module is part of the `haive-agents` package. Install it using:

```bash
pip install haive-agents[conversation]
```

## Quick Start

### Basic Collaborative Document

```python
from haive.agents.conversation import CollaborativeConversation
from haive.agents.simple import SimpleAgent

... (truncated)


---

## conversation_README

**Source**: `packages/haive-agents/src/haive/agents/conversation/base/README.md`

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
    max_roun

... (truncated)


---

## conversation_README

**Source**: `packages/haive-agents/src/haive/agents/conversation/round_robin/README.md`

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
result = await conv

... (truncated)


---

## conversation_README

**Source**: `packages/haive-agents/src/haive/agents/conversation/debate/README.md`

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

#

... (truncated)


---

## conversation_README

**Source**: `packages/haive-agents/src/haive/agents/conversation/directed/README.md`

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
d

... (truncated)


---

## conversation_README

**Source**: `packages/haive-agents/src/haive/agents/conversation/social_media/README.md`

# Social Media Conversation

Platform-style multi-agent conversations with engagement mechanics, viral dynamics, and social interactions.

## Overview

The Social Media Conversation agent simulates realistic social media interactions across different platforms (Twitter, Instagram, TikTok, LinkedIn). It includes engagement mechanics like likes, shares, and replies, along with viral dynamics and trending topics. This creates authentic platform-specific conversations with natural social behaviors and engagement patterns.

## Architecture

```
SocialMediaConversation (extends BaseConversationAgent)
├── Platform Configuration
│   ├── Twitter (280 chars, retweets)
│   ├── Instagram (visual, hashtags)
│   ├── TikTok (short, trendy)
│   └── Generic (customizable)
├── Engagement System
│   ├── Likes & Reactions
│   ├── Shares & Retweets
│   ├── Reply Threads
│   └── Follower Dynamics
├── Viral Mechanics
│   ├── Engagement Tracking
│   ├── Viral Threshold
│   └── Trending Topics
└── Social Tools
    ├── Like Tool
    ├── Reply Tool
    └── Share Tool
```

## Key Features

- **Platform-specific behavior** - Authentic Twitter, Instagram, TikTok, LinkedIn styles
- **Engagement mechanics** - Likes, shares, replies with social dynamics
- **Viral system** - Posts can go viral based on engagement
- **Character limits** - Platform-appropriate content length
- **Trending topics** - Dynamic hashtag tracking and trends
- **Social tools** - Agents can like, reply, and share posts
- **Weighted selection** - Popular users get more engagement
- **Organic growth** - Natural engagement simulation

## Installation

This module is part of the `haive-agents` package. Install it using:

```bash
pip install haive-agents[conversation]
```

## Quick Start

### Basic Social Media Conversation

```python
from haive.agents.conversation import SocialMediaConversation
from haive.agents.simple import SimpleAgent

# Create social media personalities
influencer = SimpleAgent(name="TechGuru", followers=10000

... (truncated)


---

