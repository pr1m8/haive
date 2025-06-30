# Haive Framework - Centralized Orchestrator

## What is Haive?

Haive is a comprehensive AI agent framework that provides everything you need to build, test, and deploy intelligent AI systems. With 50+ pre-built agents, 40+ game environments, 110+ integrated tools, and a powerful orchestration layer, Haive is the most complete solution for agent-based AI development.

## Core Purpose

The Haive orchestrator serves as the central nervous system for:

1. **Agent Orchestration**: Coordinate complex multi-agent workflows
2. **Dynamic Composition**: Build and modify AI systems at runtime
3. **Unified Interface**: Single entry point to a vast ecosystem of capabilities

## Key Features at a Glance

- **50+ Pre-built Agents**: From simple chatbots to complex research systems
- **40+ Game Environments**: Test and train agents in competitive scenarios
- **110+ Tool Integrations**: Connect to any API or service
- **100+ MCP Servers**: Direct integration with Model Context Protocol
- **Dynamic Architecture**: Everything can be composed and modified at runtime
- **Full Serialization**: Save and restore complete agent states
- **Production Ready**: Built for scale with proper monitoring and persistence

## What Haive Does

### 1. Dynamic Agent Orchestration

Haive allows you to create and modify AI agents on the fly. Unlike traditional frameworks where agent behavior is fixed at design time, Haive agents can:

- **Adapt their behavior** based on context or requirements
- **Add or remove capabilities** during execution
- **Share state and knowledge** between different agent instances
- **Serialize and restore** their complete state for persistence

**Example Use Case**: An agent that starts as a simple chatbot but dynamically adds research capabilities when it detects the user needs in-depth information.

### 2. Graph-Based Workflow Management

Every Haive agent is built on a graph architecture where:

- **Nodes** represent distinct processing steps (LLM calls, tool usage, decision points)
- **Edges** define the flow between steps
- **Conditions** enable dynamic routing based on results

This allows complex workflows like:
- Multi-stage reasoning with checkpoints
- Parallel processing with synchronization points
- Conditional flows based on intermediate results
- Human-in-the-loop interactions

### 3. Intelligent Tool Integration

Haive provides a sophisticated tool system where:

- Tools can be **dynamically bound** to agents
- The framework **automatically routes** requests to appropriate tools
- Tools can have **structured inputs/outputs** with validation
- **Tool selection** can be forced or left to agent discretion

### 4. Game-Based Testing Environments

Unique to Haive is the concept of "agent games" - competitive environments where:

- Agents can be tested against each other
- Performance metrics are automatically tracked
- Strategies can be evolved through gameplay
- Real-world scenarios can be simulated safely

## Key Capabilities

### Runtime Composition

```python
# Start with a basic agent
agent = haive.create_agent("analyzer")

# Dynamically add capabilities
agent.add_tool(WebSearchTool())
agent.add_engine(DataAnalysisEngine())

# Modify behavior on the fly
agent.set_temperature(0.2)  # Make it more focused
agent.enable_streaming()    # Enable real-time output
```

### State Management

```python
# Full state serialization
state = agent.save_state()

# Restore later or on different machine
restored_agent = haive.load_agent(state)

# Continue exactly where you left off
restored_agent.continue_conversation()
```

### Multi-Agent Coordination

```python
# Create specialized agents
researcher = haive.create_agent("researcher", tools=[WebSearch, PDFReader])
writer = haive.create_agent("writer", model="gpt-4")
critic = haive.create_agent("critic", temperature=0.1)

# Orchestrate them together
haive.run_workflow([
    researcher.research(topic),
    writer.draft(researcher.output),
    critic.review(writer.output),
    writer.revise(critic.feedback)
])
```

## Why Use Haive?

### 1. **Flexibility Without Complexity**
- Build simple agents quickly
- Scale to complex multi-agent systems when needed
- No need to rebuild when requirements change

### 2. **Production-Ready Features**
- Built-in persistence and state management
- Comprehensive logging and monitoring
- Error handling and retry mechanisms
- Resource management and cleanup

### 3. **Extensible Architecture**
- Add custom engines for new LLM providers
- Create domain-specific tools
- Build custom agent types
- Implement new graph patterns

### 4. **Developer Experience**
- Type-safe with Pydantic v2
- Rich debugging capabilities
- Clear error messages
- Extensive documentation

## Comprehensive Agent Library

Haive includes 50+ pre-built agent architectures organized by capability:

### RAG (Retrieval Augmented Generation) Agents
- **Agentic RAG**: Advanced RAG with agent-based decision making
- **Dynamic RAG**: Adapts retrieval strategy based on query complexity
- **Self-Correcting RAG**: Validates and refines retrieved information
- **Multi-Strategy RAG**: Combines multiple retrieval approaches
- **HYDE RAG**: Uses hypothetical document embeddings
- **LLM RAG**: Uses LLM for retrieval decisions
- **DB RAG**: Specialized for database queries (SQL, Graph)
- **Filtered RAG**: Advanced filtering and ranking capabilities

### Reasoning & Critique Agents
- **LATS (Language Agent Tree Search)**: Tree-based reasoning
- **MCTS (Monte Carlo Tree Search)**: Probabilistic decision making
- **Reflection Agent**: Self-evaluates and improves responses
- **Reflexion**: Iterative self-improvement through reflection
- **Self-Discover**: Autonomous capability discovery
- **Tree of Thoughts**: Explores multiple reasoning paths

### Planning & Execution Agents
- **Plan and Execute**: Decomposes and executes complex tasks
- **LLM Compiler**: Optimizes task execution plans
- **ReWoo**: Reduces API calls through smart planning
- **Task Analysis**: Analyzes task complexity and dependencies

### Conversation & Collaboration Agents
- **Collaborative Agents**: Multiple agents working together
- **Debate Agents**: Agents that debate to reach conclusions
- **Directed Conversation**: Goal-oriented dialogues
- **Round Robin**: Turn-based multi-agent conversations
- **Social Media**: Specialized for social platform interactions

### Document Processing Agents
- **Knowledge Graph Extractors**: Build KGs from documents
- **Iterative Refinement**: Progressively improves document analysis
- **Map-Merge**: Parallel document processing with merging
- **Complex Extraction**: Structured data extraction
- **Summarizers**: Multi-strategy summarization

### Research & Analysis Agents
- **Storm**: Systematic research agent
- **Open Perplexity**: Open-source research assistant
- **Person Researcher**: Deep research on individuals
- **Wiki Writer**: Creates Wikipedia-style articles
- **Interview Agent**: Conducts and analyzes interviews

### Specialized Agents
- **ReAct**: Multiple implementations (v1, v2, v3) with tool use
- **Long-Term Memory**: Persistent memory across sessions
- **Dynamic Supervisor**: Orchestrates other agents
- **Self-Healing Code**: Automatically fixes code errors
- **Sequential**: Step-by-step task execution

## Extensive Game Library

Haive includes 40+ game environments for agent testing and development:

### Classic Board Games
- **Chess**: Full chess implementation with analysis
- **Checkers**: Traditional and variant rules
- **Go**: The ancient strategy game
- **Reversi (Othello)**: Territory control game
- **Connect 4**: Classic connection game
- **Mancala**: Ancient counting game

### Card Games
- **Poker**: Texas Hold'em and variants
- **Blackjack**: Casino-style with strategies
- **BS (Bluff)**: Deception and detection game
- **UNO**: Popular card matching game

### Strategy Games
- **Risk**: Territory conquest and diplomacy
- **Battleship**: Naval strategy
- **Clue**: Deduction and reasoning
- **Dominoes**: Pattern matching strategy

### Social Deduction Games
- **Among Us**: Find the impostor
- **Mafia**: Classic social deduction
- **Debate**: Structured argumentation

### Single-Player Puzzles
- **Sudoku**: Logic puzzle solver
- **Crossword**: Language and knowledge
- **Wordle**: Word guessing optimization
- **Minesweeper**: Probability and deduction
- **Logic Grid**: Constraint satisfaction
- **Flow Free**: Path optimization
- **2048**: Tile merging strategy
- **Rubik's Cube**: 3D puzzle solving
- **Towers of Hanoi**: Classic algorithm puzzle
- **Solitaire**: Card arrangement
- **Word Search**: Pattern recognition

### Complex Simulations
- **Monopoly**: Full economic simulation
- **Nim**: Mathematical strategy
- **Mastermind**: Code breaking
- **Fox and Geese**: Asymmetric strategy

## Tool Ecosystem

### 110+ Curated Toolkits
- **Web Tools**: Search, scraping, API interactions
- **Data Tools**: Analysis, transformation, visualization
- **Document Tools**: PDFs, Office files, parsing
- **Code Tools**: Execution, analysis, generation
- **Communication**: Email, Slack, messaging
- **Database**: SQL, NoSQL, vector stores
- **ML/AI Tools**: Model interactions, embeddings
- **Financial**: Market data, calculations
- **Geographic**: Maps, location services

### MCP (Model Context Protocol) Integration
- **100+ MCP Servers**: Direct integration with MCP ecosystem
- **Seamless Tool Discovery**: Automatic tool detection
- **Standard Protocols**: Consistent tool interfaces

## Advanced Capabilities

### Dynamic Architectures
- **Dynamic Supervisor**: Runtime agent orchestration
- **Swarm Intelligence**: Coordinated multi-agent systems
- **Meta Agents**: Agents that manage other agents
- **Agents in State**: Agents as part of the state machine

### Memory Systems
- **Long-Term Memory**: Persistent across sessions
- **Graph Memory**: Relationship-based memory
- **Episodic Memory**: Event-based recall
- **Working Memory**: Short-term task focus

### Planning & Parallelization
- **Parallelizable Planning**: Concurrent execution paths
- **Adaptive Planning**: Runtime plan modification
- **Hierarchical Planning**: Multi-level task decomposition

### Dataflow & Integration
- **Persistence Layer**: Full state serialization
- **MCP Integration**: Model Context Protocol support
- **APIs/WebSockets**: Real-time communication
- **Event Streaming**: Reactive architectures

## Prebuilt Domain Solutions

Haive includes 40+ specialized agents for specific domains:

### Business & Startup
- **Company Researcher**: Deep company analysis
- **Startup Suite**: Ideation, market research, pitch decks
- **Business Model Canvas**: Strategic planning
- **Sales Call Analyzer**: Conversation insights
- **Shop Genie**: E-commerce optimization

### Content & Media
- **Blog Writer**: SEO-optimized content
- **Podcast Generator**: Full podcast production
- **GIF Generator**: Animated content creation
- **Business Meme Generator**: Viral content
- **Content Intelligence**: Content strategy

### Professional Services
- **Contract Analysis**: Legal document review
- **EU Green Compliance**: Regulatory compliance
- **Project Manager**: Task coordination
- **Career Assistant**: Job search and planning
- **Customer Support**: Automated assistance

### Academic & Research
- **Academic Task Learning**: Educational support
- **Essay Grading**: Automated assessment
- **Scientific Paper Agent**: Research writing
- **Systematic Review**: Literature analysis
- **Open Researcher**: General research

### Specialized Applications
- **Car Buyer Agent**: Vehicle purchase assistance
- **Travel Planner**: Itinerary optimization
- **Weather Disaster Management**: Emergency response
- **E2E Testing**: Automated testing
- **Prompt Writing**: Prompt engineering

## Getting Started

*Note: Comprehensive documentation is coming soon. For now, here's a quick start guide.*

### Installation

```bash
# Install the orchestrator
pip install haive

# Install specific packages as needed
pip install haive-agents haive-tools
```

### Basic Usage

```python
import haive

# Create a simple agent
agent = haive.create_agent(
    name="assistant",
    model="gpt-4",
    temperature=0.7
)

# Use the agent
response = agent.invoke("Help me plan a trip to Paris")

# Add tools dynamically
agent.add_tool(haive.tools.WebSearch())
agent.add_tool(haive.tools.Calculator())

# Now the agent can search and calculate
response = agent.invoke("What's the weather in Paris and how much would a week cost?")
```

### CLI Usage

```bash
# Start interactive session
haive chat --agent assistant

# Run a specific workflow
haive run workflow.yaml

# Test agents in a game
haive game chess --player1 agent1 --player2 agent2

# Manage agents
haive agent list
haive agent create --template research
haive agent export assistant > assistant.json
```

## Architecture Philosophy

Haive is built on several key principles:

1. **Everything is an Engine**: Uniform interface for all components
2. **Composition over Inheritance**: Build complex behaviors by combining simple ones
3. **Runtime over Compile-time**: Decisions and modifications happen during execution
4. **Explicit over Implicit**: Clear configuration and behavior
5. **Serializable by Default**: Everything can be saved and restored

## Future Roadmap

- **Web UI**: Visual agent builder and monitoring dashboard
- **Cloud Deployment**: Managed Haive instances with scaling
- **Marketplace**: Share and discover agent templates and tools
- **Enhanced Games**: More complex simulation environments
- **Performance Optimizations**: Faster execution and lower latency

## Conclusion

Haive is not just another AI framework - it's a complete ecosystem for building, testing, and deploying intelligent AI systems. Whether you're building a simple chatbot or a complex multi-agent research system, Haive provides the tools and flexibility you need while maintaining clean, maintainable code.

The centralized orchestrator ensures all components work together seamlessly while allowing each piece to evolve independently. This polyrepo approach with namespace packaging means you only use what you need, when you need it.