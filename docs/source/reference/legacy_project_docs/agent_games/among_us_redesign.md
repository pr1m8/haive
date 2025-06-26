# Among Us Game Redesign

## Core Design Principles

1. **Clean Separation of Concerns**
   - Strict separation between game state, game rules, agent behavior, and UI
   - Clear interfaces between components
   - Consistent use of Pydantic models throughout

2. **Enhanced Game Mechanics**
   - Full sabotage system with resolution mechanics
   - Vent system for impostors with proper navigation
   - Task mini-games for more engaging gameplay
   - Line-of-sight and visibility mechanics
   - Enhanced map with room connections and distances

3. **Flexible Game Flow**
   - Event-driven architecture for game state transitions
   - Support for game variants and custom rules
   - Proper handling of edge cases and unexpected events
   - Mid-game joining/leaving capability

4. **Immersive UI**
   - Rich, animated terminal UI with better map visualization
   - Clear player feedback for important events
   - Support for color schemes and accessibility options
   - Optional web-based UI for better visual experience

5. **Intelligent Agent Behavior**
   - Enhanced context for LLM decision-making
   - Memory of past interactions and suspicions
   - Better parsing of natural language responses
   - Role-specific behavior patterns and strategies

## Architecture Components

### 1. Game Models

#### Core Models

- `Player`: Player state, identity, and attributes
- `Task`: Enhanced task model with mini-game support
- `Room`: Room information with connectivity data
- `Sabotage`: Expanded sabotage model with resolution mechanics
- `GameEvent`: Event model for tracking significant game events

#### State Models

- `GameState`: Top-level game state container
- `RoundState`: State specific to a round of play
- `MeetingState`: Enhanced meeting with discussion tracking
- `VotingState`: Voting with anonymous option and tie mechanics

### 2. Game Engine

#### State Manager

- `StateManager`: Core state manipulation and validation
- `RuleEnforcer`: Enforces game rules and constraints
- `EventManager`: Handles game events and triggers

#### Game Logic

- `TaskManager`: Manages task assignment and completion
- `SabotageManager`: Handles sabotage initiation and resolution
- `KillSystem`: Advanced kill detection with alibi checking
- `VentSystem`: Manages vent navigation for impostors
- `VisibilitySystem`: Handles line-of-sight and visibility

### 3. Agent System

#### Agent Framework

- `AgentDirector`: Coordinates agent behavior and interactions
- `RoleStrategy`: Role-specific behavior strategies
- `MemoryManager`: Tracks knowledge and observations for agents

#### LLM Integration

- `PromptBuilder`: Creates tailored, context-rich prompts
- `ResponseParser`: Enhanced parsing of natural language responses
- `DecisionEngine`: Manages agent decision-making process

### 4. User Interface

#### Terminal UI

- `UIManager`: Core UI management and updates
- `MapRenderer`: Enhanced map visualization
- `PlayerRenderer`: Player visualization with animations
- `EventRenderer`: Visual feedback for game events
- `TaskRenderer`: Task visualization and interaction

#### Optional Web UI

- `WebServer`: Simple web server for UI
- `WebUIState`: State synchronization for web clients
- `WebRenderers`: Web-specific renderers

## Implementation Plan

### Phase 1: Core Models and Engine

- Implement enhanced game models
- Build basic state manager and rule enforcer
- Create event system for game state transitions

### Phase 2: Game Mechanics

- Implement room connectivity and navigation
- Build task system with mini-games
- Create sabotage and resolution mechanics
- Implement vent system for impostors

### Phase 3: Agent Intelligence

- Enhance LLM prompts with better context
- Implement memory system for agents
- Create improved response parser
- Build role-specific strategies

### Phase 4: UI Enhancements

- Implement enhanced terminal UI
- Create animated map visualization
- Build player and event renderers
- Optional: Create basic web UI

### Phase 5: Testing and Refinement

- Comprehensive testing of game mechanics
- Balance adjustments for fair gameplay
- Performance optimization
- Final polishing

## Key Improvements

### Game Mechanics

1. **Enhanced Map System**
   - Rooms with clear connections and travel times
   - Vents with specific connections for impostors
   - Security cameras for surveillance
   - Door locks for strategic play

2. **Task System**
   - Multiple task types with varying completion methods
   - Task dependencies and sequences
   - Visual tasks with clear indicators for other players
   - Task completion affects ship systems

3. **Sabotage System**
   - Multiple sabotage types (communications, oxygen, reactor, lights)
   - Each sabotage has unique resolution mechanics
   - Cascading effects on ship systems
   - Time limits with consequences

4. **Meeting Mechanics**
   - Evidence system for body reports
   - Anonymous voting option
   - Extended discussion with turn-based contributions
   - Tie resolution mechanics

### Agent Intelligence

1. **Memory and Knowledge Base**
   - Agents remember past observations and interactions
   - Track suspicion levels for other players
   - Build and update mental models of the game state
   - Remember alibis and reported locations

2. **Strategic Decision Making**
   - Role-specific strategies (defensive, aggressive, stealthy)
   - Adaptive play based on game state and suspicion levels
   - Coordination between impostor team members
   - Risk assessment for actions

3. **Natural Language Processing**
   - Better understanding of complex instructions
   - More nuanced response parsing
   - Detection of deception in other players' statements
   - Context-aware dialogue generation

4. **Meta-Game Awareness**
   - Understanding of game phase and strategic implications
   - Awareness of time-sensitive objectives
   - Recognition of common play patterns and counter-strategies
   - End-game tactics and win condition analysis

### User Experience

1. **Rich Visual Feedback**
   - Clear indicators for important events
   - Animated transitions between game phases
   - Visual representation of player movements
   - Task completion animations

2. **Information Accessibility**
   - Clear display of game state and player information
   - Streamlined interface for quick decision making
   - Historical view of significant events
   - Role-specific information displays

3. **Customization Options**
   - Adjustable game parameters
   - Support for different play styles
   - Color schemes and accessibility features
   - Game variants with unique rule sets

4. **Interactive Tutorials**
   - Guided introduction to game mechanics
   - Role-specific training scenarios
   - Progressive difficulty for learning players
   - Strategy tips and best practices
