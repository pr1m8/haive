# Debate Agent Examples

Real examples and outputs from the debate agent.

## debate_README

**Source**: `packages/haive-games/src/haive/games/debate/README.md`

# Debate

Structured debate and argumentation platform with LLM-powered participants and sophisticated scoring.

## Overview

The Debate module provides a comprehensive platform for structured discussions and formal debates, featuring AI participants that can engage in sophisticated argumentation, evidence presentation, and logical reasoning. Built on the Haive framework, it supports multiple debate formats and advanced judging mechanisms.

**Key Features:**

- **Multiple Debate Formats**: Parliamentary, Oxford-style, Lincoln-Douglas, and custom formats
- **AI Debaters**: LLM-powered participants with distinct arguing styles and expertise
- **Structured Phases**: Opening statements, rebuttals, cross-examination, and closing arguments
- **Intelligent Judging**: AI judges that evaluate arguments based on logic, evidence, and rhetoric
- **Topic Research**: Automated fact-checking and evidence gathering for debate topics
- **Real-time Scoring**: Dynamic evaluation of argument strength and debate performance
- **Rich Moderation**: AI moderators that enforce rules and guide discussion flow

**Debate Mechanics:**

- **Argument Structure**: Claims, evidence, warrants, and impact analysis
- **Rebuttal System**: Point-by-point refutation and counter-arguments
- **Time Management**: Configurable speaking times and turn enforcement
- **Evidence Validation**: Fact-checking and source verification
- **Flow Tracking**: Comprehensive argument mapping and progression

## Architecture

The debate system follows multi-participant game architecture:

```
DebateAgent
├── Configuration (DebateAgentConfig)
├── State Management (DebateStateManager)
├── Participants (debaters, judges, moderator)
├── Debate Flow (phases, timing, rules)
├── Scoring System (argument evaluation)
└── Workflow (LangGraph-based debate management)
```

### Core Components

- **DebateAgent**: Main debate controller managing flow and participants
- **DebateState**: Complete debate state with arguments, scores, and ph

... (truncated)


---

