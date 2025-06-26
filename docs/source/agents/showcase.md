# 🤖 Haive Agent Showcase

Welcome to the comprehensive showcase of Haive's intelligent agent ecosystem! This showcase presents **234 agents** across **18 categories**, demonstrating the full breadth and power of the Haive framework.

## 📊 Agent Ecosystem Overview

### 📈 Quick Stats

| Metric | Value |
|--------|-------|
| **Total Agents** | 234 |
| **Categories** | 18 |
| **Packages** | 3 |
| **Complex Agents** | 106 |

### 🏷️ Top Agent Categories

| Category | Agents | Primary Package |
|----------|--------|----------------|
| **Games** | 40 | `haive-games` |
| **ReAct & Tool Use** | 32 | `haive-agents` |
| **RAG & Retrieval** | 28 | `haive-agents` |
| **Specialized Agents** | 21 | `haive-agents` |
| **Reasoning & Critique** | 20 | `haive-agents` |
| **Document Processing** | 18 | `haive-agents` |
| **Multi-Agent Systems** | 11 | `haive-agents` |
| **Prebuilt Solutions** | 11 | `haive-prebuilt` |
| **Classic Games** | 9 | `haive-games` |
| **Research & Information** | 6 | `haive-agents` |
| *...and 8 more categories* | | |


## 🚀 Getting Started

### Quick Start Guide

1. **Choose Your Agent Type**
   - 🌟 **New to Haive?** Start with Foundation Agents (SimpleAgent, ReactAgent)
   - 🎯 **Building Apps?** Check out Prebuilt Solutis  
   - 🎮 **Want Fun?** Explore Game Agents
   - 🧠 **Advanced Use?** Try Reasoning & Critique agents

2. **Install & Import**
   ```bash
   pip install haive[agents]    # Core agents
   pip install haive[games]     # Game agents
   pip install haive[prebuilt]  # Business solutions
   ```

3. **Basic Usage Pattern**
   ```python
   from haive.agents.simple import SimpleAgent

   # Create agent
   agent = SimpleAgent(
       name="my_agent",
       model="gpt-4"
   )

   # Use agent
   result = agent.invoke({"query": "Your task here"})
   ```

## 📚 Complete Agent Catalog

### Games

**40 agents** | **Packages:** haive-games

| Agent | Complexity | Features | Description |
|-------|------------|----------|-------------|
| **BattleshipAgent** | 🔴 Complex | planning, memory | Battleship game agent with LLM-powered players. |
| **DebateAgent** | 🔴 Complex | structured_output | Agent for facilitating debates and structured discussions. |
| **DominoesAgent** | 🔴 Complex | Basic | Agent for playing dominoes. |
| **FoxAndGeeseAgent** | 🔴 Complex | Basic | Agent for playing Fox and Geese. |
| **GameAgent** | 🔴 Complex | tools | Base game agent that implements common workflow patterns. |
| **GameAgent** | 🔴 Complex | tools | Base game agent that implements common workflow patterns. |
| **HoldemPlayerAgent** | 🔴 Complex | planning | Player agent for Texas Hold'em poker games. |
| **MancalaAgent** | 🔴 Complex | Basic | Agent for playing Mancala. |
| **MastermindAgent** | 🔴 Complex | Basic | Agent for playing Mastermind. |
| **MultiPlayerGameAgent** | 🔴 Complex | tools, structured_output | Base game agent for multi-player games. |
| **MultiPlayerGameAgent** | 🔴 Complex | tools, structured_output | Base game agent for multi-player games. |
| **MultiPlayerGameConfig** | 🔴 Complex | structured_output | Configuration for multi-player game agents. |
| **MultiPlayerGameConfig** | 🔴 Complex | structured_output | Configuration for multi-player game agents. |
| **NimAgent** | 🔴 Complex | Basic | Agent for playing Nim. |
| **ReversiAgent** | 🔴 Complex | Basic | Agent for playing Reversi/Othello. |
| **SinglePlayerGameAgent** | 🔴 Complex | tools | Base agent for single-player games. |
| **Connect4Agent** | 🟡 Medium | Basic | Agent for playing Connect 4. |
| **FlowFreeAgent** | 🟡 Medium | Basic | Agent for playing Flow Free puzzle game. |
| **MonopolyPlayerAgent** | 🟡 Medium | Basic | Player agent for making individual decisions in Monopoly. |
| **RubiksCubeAgent** | 🟡 Medium | Basic | Rubik's Cube game agent. |
| **TicTacToeAgent** | 🟡 Medium | structured_output | Agent for playing Tic Tac Toe using structured game flow and LLM inference. |
| **BasePlayerAgent** | 🟢 Simple | Basic | No description available |
| **BasePlayerAgent** | 🟢 Simple | Basic | Base class for player agents. |
| **BattleshipAgentConfig** | 🟢 Simple | structured_output | Configuration class for Battleship game agents. |
| **ClueAgent** | 🟢 Simple | Basic | Agent for playing Clue. |
| **Connect4AgentConfig** | 🟢 Simple | Basic | Configuration class for Connect4 game agents. |
| **DebateAgentConfig** | 🟢 Simple | Basic | Configuration for debate agents. |
| **DominoesAgentConfig** | 🟢 Simple | Basic | Configuration for the dominoes agent. |
| **FixedFoxAndGeeseAgent** | 🟢 Simple | Basic | Fixed Fox and Geese agent that handles state directly. |
| **GameAgentConfig** | 🟢 Simple | Basic | Base configuration for game agents. |
| **GameAgentFactory** | 🟢 Simple | structured_output | Factory for creating game agents using a flexible, composable pattern. |
| **GameAgentFactory** | 🟢 Simple | structured_output | Factory for creating game agents using a flexible, composable pattern. |
| **GameConfig** | 🟢 Simple | structured_output | Base configuration for game agents. |
| **GameConfig** | 🟢 Simple | structured_output | Base configuration for game agents. |
| **HoldemPlayerAgentConfig** | 🟢 Simple | Basic | Configuration for Hold'em player agent. |
| **MonopolyGameAgentConfig** | 🟢 Simple | structured_output | Configuration class for monopoly game agents. |
| **MonopolyGameAgentConfig** | 🟢 Simple | structured_output | Configuration class for monopoly game agents. |
| **MonopolyPlayerAgentConfig** | 🟢 Simple | Basic | Configuration for monopoly player decision agent. |
| **MonopolyPlayerAgentConfig** | 🟢 Simple | Basic | Configuration for monopoly player decision agent. |
| **WordConnectionsAgentConfig** | 🟢 Simple | Basic | Configuration for Word Connections agent. |

### ReAct & Tool Use

**32 agents** | **Packages:** haive-agents

| Agent | Complexity | Features | Description |
|-------|------------|----------|-------------|
| **AdvancedReactAgent** | 🔴 Complex | tools | Advanced React agent with specialized tool routing. |
| **AdvancedReactAgentConfig** | 🔴 Complex | tools | Extended configuration for the Advanced React Agent. |
| **ReactAgent** | 🔴 Complex | reasoning, tools +1 | A tool-using agent implementing the ReAct pattern. |
| **ReactAgent** | 🔴 Complex | reasoning, tools +1 | A React agent implementing the Reasoning-Action-Observation pattern. |
| **ReactAgent** | 🔴 Complex | reasoning, tools | A React agent implementation using LangGraph. |
| **ReactAgent** | 🔴 Complex | reasoning, tools | React Agent implementation that extends SimpleAgent. |
| **ReactAgent** | 🔴 Complex | reasoning, tools | A React agent that enhances SimpleAgent with tool-using capabilities. |
| **ReactAgentConfig** | 🔴 Complex | reasoning, tools | Configuration for a ReAct agent with tool integration. |
| **ReactAgentConfig** | 🔴 Complex | reasoning, tools +1 | Configuration for a React agent that can use tools. |
| **ReactAgentConfig** | 🔴 Complex | reasoning, tools | Configuration for a React agent, extending SimpleAgentConfig. |
| **ReactAgentConfig** | 🔴 Complex | reasoning, tools | Configuration for React Agent, extending SimpleAgentConfig. |
| **ReactAgentConfig** | 🔴 Complex | reasoning, tools | Configuration for a React agent that can use tools and follow ReAct reasoning pa... |
| **ReactAgentState** | 🔴 Complex | reasoning, tools +1 | State for React Agent, extending SimpleAgentState. |
| **ReactManyToolsAgent** | 🔴 Complex | tools, retrieval | React Agent implementation that can handle many tools efficiently. |
| **DynamicReactAgent** | 🟡 Medium | tools | A React agent with dynamic tool selection. |
| **ReactAgent** | 🟡 Medium | Basic | No description available |
| **ReactAgentState** | 🟡 Medium | tools, structured_output +1 | State for React agents with tool usage. |
| **DynamicReactAgentConfig** | 🟢 Simple | tools | Configuration for a React agent with dynamic tool selection. |
| **DynamicReactAgentState** | 🟢 Simple | tools, structured_output | Extended schema for dynamic tool selection. |
| **ReactAgent** | 🟢 Simple | Basic | ReAct agent with looping behavior. |
| **ReactAgent** | 🟢 Simple | tools | ReAct agent implementation with tool usage and routing capabilities. |
| **ReactAgentConfig** | 🟢 Simple | tools | Configuration for the React Agent. |
| **ReactAgentConfig** | 🟢 Simple | tools | Configuration for the ReAct agent. |
| **ReactAgentConfig** | 🟢 Simple | tools | Configuration for a React agent that follows the ReAct pattern: |
| **ReactAgentConfig** | 🟢 Simple | tools | No description available |
| **ReactAgentSchema** | 🟢 Simple | tools, structured_output | Schema for React Agent State, extending SimpleAgentSchema. |
| **ReactAgentSchemaWithStructuredResponse** | 🟢 Simple | structured_output | Schema for React Agent with structured response. |
| **ReactAgentState** | 🟢 Simple | tools, structured_output | State schema for ReAct agent. |
| **ReactAgentState** | 🟢 Simple | Basic | The state of the agent. |
| **ReactAgentState** | 🟢 Simple | tools, structured_output | State schema for React agent. |
| **ReactManyToolsConfig** | 🟢 Simple | tools, retrieval | Configuration for React Agent with many tools. |
| **ReactManyToolsState** | 🟢 Simple | tools, retrieval | State for React Agent with many tools. |

### RAG & Retrieval

**28 agents** | **Packages:** haive-agents

| Agent | Complexity | Features | Description |
|-------|------------|----------|-------------|
| **AdaptiveRAGMultiAgent** | 🔴 Complex | planning, retrieval | Advanced RAG system that adapts its strategy based on query complexity and resul... |
| **BaseRAGMultiAgent** | 🔴 Complex | conversation, retrieval | Base multi-agent RAG system with retrieve -> grade -> generate workflow. |
| **ConditionalRAGMultiAgent** | 🔴 Complex | conversation, retrieval | Conditional multi-agent RAG system with smart routing based on document quality. |
| **EnhancedRAGParallelAgent** | 🔴 Complex | structured_output, retrieval | RAG parallel agent with built-in compatibility checking for consensus building. |
| **GraphDBRAGAgent** | 🔴 Complex | tools, structured_output +1 | Graph Database RAG Agent for natural language querying of Neo4j databases. |
| **IterativeRAGMultiAgent** | 🔴 Complex | conversation, retrieval | Multi-agent RAG system with iterative document processing. |
| **MultiAgentCompatibilityReport** | 🔴 Complex | Basic | Compatibility report for multiple agents in a workflow. |
| **MultiAgentRAGState** | 🔴 Complex | structured_output, conversation +1 | Comprehensive state schema for multi-agent RAG systems. |
| **MultiStrategyRAGAgent** | 🔴 Complex | retrieval | RAG agent with multiple retrieval strategies. |
| **ParallelRAGMultiAgent** | 🔴 Complex | conversation, retrieval | Parallel multi-agent RAG system for consensus-based processing. |
| **SQLRAGAgent** | 🔴 Complex | tools, structured_output +1 | SQL RAG Agent for querying SQL databases with natural language. |
| **SelfCorrectiveRAGAgent** | 🔴 Complex | retrieval | RAG agent with self-correction capabilities. |
| **SimpleRAGAgent** | 🔴 Complex | tools, conversation +1 | Simple RAG agent that retrieves documents and provides basic answers. |
| **DynamicRAGAgent** | 🟡 Medium | retrieval | Implements a dynamic RAG pipeline that routes queries to appropriate data source... |
| **FilteredRAGAgent** | 🟡 Medium | retrieval | RAG agent with document filtering capabilities. |
| **TypedRAGAgent** | 🟡 Medium | retrieval | Implements Typed-RAG that classifies queries and routes to specialized handlers. |
| **AgentCompatibilityReport** | 🟢 Simple | Basic | Comprehensive compatibility report for agent pairs. |
| **BaseRAGAgent** | 🟢 Simple | tools, retrieval | Simple base RAG agent with retrieve and generate functionality. |
| **BaseRAGConfig** | 🟢 Simple | retrieval | Configuration for a basic RAG agent. |
| **DocumentGradingAgent** | 🟢 Simple | Basic | Document grading agent that evaluates document relevance. |
| **EnhancedRAGConditionalAgent** | 🟢 Simple | retrieval | RAG conditional agent with built-in compatibility checking and smart routing. |
| **EnhancedRAGSequentialAgent** | 🟢 Simple | retrieval | RAG sequential agent with built-in compatibility checking. |
| **GraphDBRAGConfig** | 🟢 Simple | structured_output, retrieval | Main configuration for the Graph Database RAG Agent. |
| **IterativeDocumentGradingAgent** | 🟢 Simple | Basic | Specialized grading agent that processes documents one by one. |
| **LLMRAGAgent** | 🟢 Simple | retrieval | LLM-enhanced RAG agent that retrieves documents and generates answers. |
| **SQLRAGConfig** | 🟢 Simple | structured_output, retrieval | Configuration for the SQL RAG Agent. |
| **SimpleRAGAgent** | 🟢 Simple | retrieval | Simple RAG agent that performs retrieval. |
| **SimpleRAGAnswerAgent** | 🟢 Simple | structured_output, retrieval | RAG answer generation agent that creates responses from retrieved documents. |

### Specialized Agents

**21 agents** | **Packages:** haive-agents

| Agent | Complexity | Features | Description |
|-------|------------|----------|-------------|
| **Agent** | 🔴 Complex | structured_output, memory | Abstract base agent class that extends InvokableEngine with execution and state ... |
| **Agent** | 🔴 Complex | Basic | Abstract base agent class with automatic graph building and proper inheritance. |
| **ChainAgent** | 🔴 Complex | tools, structured_output | An agent that chains multiple engines together, passing output from one to the n... |
| **ChainAgentConfig** | 🔴 Complex | Basic | Configuration for a chain agent that processes input through multiple engines in... |
| **SequentialAgent** | 🔴 Complex | Basic | Sequential agent that executes multiple agents in sequence. |
| **TaskAnalysisAgent** | 🔴 Complex | planning | Comprehensive task analysis agent that orchestrates multiple analysis engines. |
| **AgentDebugger** | 🟡 Medium | Basic | Rich UI debugger for agent execution. |
| **SequentialAgentConfig** | 🟡 Medium | structured_output | Configuration for a SequentialAgent that connects components linearly. |
| **WebNavAgent** | 🟡 Medium | tools | An interactive web navigation agent using Playwright & LangGraph with integrated... |
| **Agent** | 🟢 Simple | Basic | Complete agent protocol combining all capabilities. |
| **ChainAgentSchema** | 🟢 Simple | structured_output | Schema for chain agents with intermediate results, extending SimpleAgentSchema. |
| **DocumentAgent** | 🟢 Simple | Basic | No description available |
| **DocumentAgentConfig** | 🟢 Simple | Basic | The configuration for the document agent. |
| **InterviewAgent** | 🟢 Simple | Basic | An agent that conducts an interview with a Subject Matter Expert. |
| **InterviewAgentConfig** | 🟢 Simple | Basic | Configuration for the Interview Agent. |
| **RoutingAgent** | 🟢 Simple | Basic | Simple agent with conditional routing capabilities. |
| **RoutingAgentConfig** | 🟢 Simple | Basic | Configuration for a routing agent. |
| **RoutingAgentSchema** | 🟢 Simple | structured_output | Schema for routing agents. |
| **WebNavAgentConfig** | 🟢 Simple | Basic | Configuration for the Web Navigator Agent. |
| **WikiWriterAgent** | 🟢 Simple | Basic | An agent that writes a wiki page. |
| **WikiWriterAgentConfig** | 🟢 Simple | Basic | Configuration for the Wiki Writer Agent. |

### Reasoning & Critique

**20 agents** | **Packages:** haive-agents

| Agent | Complexity | Features | Description |
|-------|------------|----------|-------------|
| **LATSAgent** | 🔴 Complex | reasoning, retrieval | A Look-Ahead Tree Search (LATS) agent that uses tree search to |
| **LATSAgentConfig** | 🔴 Complex | reasoning, tools +1 | Configuration for a Look-Ahead Tree Search (LATS) agent. |
| **ReasoningSystem** | 🔴 Complex | reasoning | Orchestrator agent for comprehensive reasoning analysis. |
| **ReflectionAgent** | 🔴 Complex | reasoning | An agent with self-reflection capabilities that can improve its responses. |
| **ReflectionAgentConfig** | 🔴 Complex | reasoning | Configuration for an agent that uses reflection to improve responses. |
| **ReflectionAgentState** | 🔴 Complex | reasoning, structured_output | State schema for the Reflection agent. |
| **SelfDiscoverAgent** | 🔴 Complex | reasoning, planning +1 | An agent that implements the SelfDiscover methodology with structured output mod... |
| **SelfDiscoverAgentConfig** | 🔴 Complex | reasoning, structured_output | Configuration for a SelfDiscover agent. |
| **TOTAgentConfig** | 🔴 Complex | reasoning, retrieval | Configuration for the Tree of Thoughts agent. |
| **ToTAgent** | 🔴 Complex | reasoning, retrieval | Tree of Thoughts agent implementation. |
| **ToTAgentConfig** | 🔴 Complex | reasoning, retrieval | Configuration for a Tree of Thoughts agent. |
| **ToTAgent** | 🟡 Medium | Basic | No description available |
| **LATSAgentConfig** | 🟢 Simple | tools, retrieval | Configuration for Language Agent Tree Search (LATS) agent. |
| **MCTSAgent** | 🟢 Simple | retrieval | Monte Carlo Tree Search Agent implementation. |
| **MCTSAgentConfig** | 🟢 Simple | tools | Configuration for MCTS Agent. |
| **ReflexionAgent** | 🟢 Simple | Basic | Agent that uses Reflexion to answer questions. |
| **ReflexionConfig** | 🟢 Simple | tools | Configuration for the Reflexion agent. |
| **ReflexionState** | 🟢 Simple | Basic | State for the Reflexion agent. |
| **SelfDiscoverAgent** | 🟢 Simple | Basic | Self Discover Agent |
| **SelfDiscoverAgentConfig** | 🟢 Simple | Basic | Configuration for the Self Discover Agent |

### Document Processing

**18 agents** | **Packages:** haive-agents

| Agent | Complexity | Features | Description |
|-------|------------|----------|-------------|
| **ComplexExtractionAgent** | 🔴 Complex | structured_output | Agent that extracts complex structured information from text. |
| **ComplexExtractionAgentConfig** | 🔴 Complex | tools, structured_output | Configuration for the complex extraction agent. |
| **DocumentLoaderAgent** | 🔴 Complex | structured_output, retrieval | Document Loader Agent that integrates the document loader engine with the agent ... |
| **ParallelKGTransformer** | 🔴 Complex | retrieval | An agent that builds a knowledge graph by extracting |
| **StructuredKGAgent** | 🔴 Complex | structured_output, retrieval | An agent that builds a knowledge graph using structured output models. |
| **TaxonomyAgent** | 🔴 Complex | conversation, memory | Agent that generates a taxonomy from a conversation history. |
| **TaxonomyAgentConfig** | 🔴 Complex | conversation, memory | Agent configuration for generating a taxonomy from conversation history. |
| **WebLoaderAgent** | 🔴 Complex | planning | Specialized document loader agent for loading documents from web URLs. |
| **SummarizerAgent** | 🟡 Medium | retrieval | SummarizerAgent is a class that summarizes a list of documents. |
| **DirectoryLoaderAgent** | 🟢 Simple | Basic | Specialized document loader agent for loading documents from directories. |
| **FileLoaderAgent** | 🟢 Simple | Basic | Specialized document loader agent for loading documents from files. |
| **IterativeGraphTransformer** | 🟢 Simple | Basic | An agent that transforms a graph document iteratively. |
| **IterativeGraphTransformerConfig** | 🟢 Simple | Basic | The configuration for the iterative graph transformer. |
| **IterativeSummarizer** | 🟢 Simple | Basic | An agent that summarizes a document iteratively. |
| **IterativeSummarizerConfig** | 🟢 Simple | Basic | The configuration for the iterative summarizer. |
| **ParallelKGTransformerConfig** | 🟢 Simple | retrieval | Configuration for the Parallel Knowledge Graph Transformer. |
| **ParallelKGTransformerConfig** | 🟢 Simple | retrieval | Configuration for the Parallel Knowledge Graph Transformer. |
| **SummarizerAgentConfig** | 🟢 Simple | Basic | No description available |

### Multi-Agent Systems

**11 agents** | **Packages:** haive-agents

| Agent | Complexity | Features | Description |
|-------|------------|----------|-------------|
| **CompatibilityEnhancedMultiAgent** | 🔴 Complex | conversation, retrieval | Multi-agent system with built-in compatibility checking and automatic adaptation... |
| **ConditionalAgent** | 🔴 Complex | conversation | Pre-configured conditional multi-agent with branching. |
| **MultiAgent** | 🔴 Complex | planning, tools +3 | Abstract base class for sophisticated multi-agent systems. |
| **MultiAgent** | 🔴 Complex | conversation | Abstract base class for multi-agent systems. |
| **MultiAgent** | 🔴 Complex | structured_output, conversation +1 | Advanced multi-agent system with flexible coordination patterns. |
| **ParallelAgent** | 🔴 Complex | conversation | Pre-configured parallel multi-agent. |
| **SequentialAgent** | 🔴 Complex | structured_output, conversation | Multi-agent system with sequential execution. |
| **SequentialMultiAgent** | 🔴 Complex | structured_output, conversation | Multi-agent system that executes agents sequentially. |
| **CompatibilityEnhancedConditionalAgent** | 🟢 Simple | Basic | Conditional agent with built-in compatibility checking. |
| **CompatibilityEnhancedParallelAgent** | 🟢 Simple | Basic | Parallel agent with built-in compatibility checking. |
| **CompatibilityEnhancedSequentialAgent** | 🟢 Simple | Basic | Sequential agent with built-in compatibility checking. |

### Prebuilt Solutions

**11 agents** | **Packages:** haive-prebuilt

| Agent | Complexity | Features | Description |
|-------|------------|----------|-------------|
| **AgentAction** | 🔴 Complex | reasoning, tools +1 | Model representing an agent's action decision. |
| **WeatherDisasterManagementAgent** | 🔴 Complex | Basic | No description available |
| **ProjectManagerAgent** | 🟡 Medium | Basic | No description available |
| **AgentMetadata** | 🟢 Simple | tools | Metadata about agent contributions to content generation. |
| **AgentOutput** | 🟢 Simple | structured_output | Model representing the output from an agent's action. |
| **EssayGradingAgent** | 🟢 Simple | Basic | No description available |
| **PodcastGeneratorAgent** | 🟢 Simple | Basic | No description available |
| **ProjectManagerAgentConfig** | 🟢 Simple | Basic | No description available |
| **TLDRAgentConfig** | 🟢 Simple | Basic | No description available |
| **TaskifierAgent** | 🟢 Simple | Basic | No description available |
| **WeatherDisasterManagerConfig** | 🟢 Simple | tools | No description available |

### Classic Games

**9 agents** | **Packages:** haive-games

| Agent | Complexity | Features | Description |
|-------|------------|----------|-------------|
| **AgentDecision** | 🔴 Complex | reasoning, planning | Agent's decision in the game. |
| **AgentDecisionSchema** | 🔴 Complex | reasoning, planning +1 | Schema for LLM decision output. |
| **CheckersAgent** | 🔴 Complex | structured_output | Agent for playing checkers with LLM-based players and rich UI. |
| **GoAgent** | 🔴 Complex | tools | Go game agent implementation. |
| **PokerAgent** | 🔴 Complex | structured_output | Enhanced agent class for managing a multi-player Texas Hold'em poker game. |
| **PokerAgentTester** | 🔴 Complex | Basic | Test suite for the Poker agent. |
| **CheckersAgentConfig** | 🟢 Simple | structured_output | Configuration for checkers game agent. |
| **GoAgentConfig** | 🟢 Simple | structured_output | Configuration for the Go game agent. |
| **PokerAgentConfig** | 🟢 Simple | structured_output, memory +1 | Configuration class for the poker agent. |

### Research & Information

**6 agents** | **Packages:** haive-agents

| Agent | Complexity | Features | Description |
|-------|------------|----------|-------------|
| **PersonResearchAgent** | 🔴 Complex | reasoning, structured_output +1 | Advanced person research agent with iterative information gathering capabilities... |
| **ResearchAgent** | 🔴 Complex | retrieval | Agent for performing deep research on any topic with dynamic document loader sel... |
| **STORMAgentConfig** | 🟡 Medium | retrieval | Configuration for the STORM agent - an orchestrator that coordinates research, |
| **PersonResearchAgentConfig** | 🟢 Simple | retrieval | Configuration settings for person research agent. |
| **PersonResearchAgentConfig** | 🟢 Simple | retrieval | Configuration for the Person Research Agent. |
| **ResearchAgentConfig** | 🟢 Simple | tools, structured_output +1 | Configuration for open_perplexity research agent. |

### Planning & Strategy

**6 agents** | **Packages:** haive-agents

| Agent | Complexity | Features | Description |
|-------|------------|----------|-------------|
| **LLMCompilerAgent** | 🔴 Complex | planning, structured_output | LLM Compiler Agent implementation. |
| **RewooAgent** | 🔴 Complex | reasoning, tools +2 | ReWOO (Reasoning Without Observation) Agent implementation. |
| **RewooAgentConfig** | 🔴 Complex | tools, planning | Configuration for the ReWOO Agent with automatic prompt formatting. |
| **LLMCompilerAgentConfig** | 🟢 Simple | tools | Configuration for the LLM Compiler Agent using AugLLMConfig system. |
| **PlanAndExecuteAgent** | 🟢 Simple | Basic | No description available |
| **PlanAndExecuteConfig** | 🟢 Simple | Basic | No description available |

### Academic & Research

**6 agents** | **Packages:** haive-prebuilt

| Agent | Complexity | Features | Description |
|-------|------------|----------|-------------|
| **EnhancedKYCAgent** | 🔴 Complex | Basic | Advanced KYC Agent with comprehensive risk assessment workflow |
| **KYCAgentConfiguration** | 🔴 Complex | Basic | Advanced configuration for KYC Agent with granular control |
| **AgentState** | 🟢 Simple | Basic | No description available |
| **ScientificPaperAgent** | 🟢 Simple | Basic | No description available |
| **ScientificPaperAgentState** | 🟢 Simple | retrieval | The state of the agent during the paper research process. |
| **SystemicReviewOfScientificArticlesAgent** | 🟢 Simple | Basic | No description available |

### Foundation Agents

**5 agents** | **Packages:** haive-agents

| Agent | Complexity | Features | Description |
|-------|------------|----------|-------------|
| **SimpleAgent** | 🔴 Complex | tools, structured_output +1 | Simple agent that modifies its engine to include structured output schema. |
| **SimpleAgentState** | 🔴 Complex | conversation, memory | Base state for simple agents. |
| **SimpleAgent** | 🟢 Simple | structured_output | A simple agent with a single node workflow and comprehensive schema handling. |
| **SimpleAgentConfig** | 🟢 Simple | structured_output | Configuration for a simple single-node agent with comprehensive schema handling. |
| **StructuredOutputAgentConfig** | 🟢 Simple | tools, structured_output | Configuration for a structured output agent. |

### Memory & Persistence

**5 agents** | **Packages:** haive-agents

| Agent | Complexity | Features | Description |
|-------|------------|----------|-------------|
| **MemoryAgent** | 🔴 Complex | conversation, memory | Memory Agent implementation that extends ReactAgent. |
| **LongTermMemoryAgent** | 🟢 Simple | memory | Agent for the long term memory. |
| **LongTermMemoryAgentConfig** | 🟢 Simple | memory | Config for the long term memory agent. |
| **LongTermMemoryState** | 🟢 Simple | memory | State for the long term memory agent. |
| **MemoryAgentState** | 🟢 Simple | memory | State for Memory Agent, extending ReactAgentState. |

### Conversation & Multi-Agent

**5 agents** | **Packages:** haive-agents

| Agent | Complexity | Features | Description |
|-------|------------|----------|-------------|
| **BaseConversationAgent** | 🔴 Complex | tools, conversation | Base conversation agent that orchestrates multi-agent conversations. |
| **CollaborativeConversation** | 🔴 Complex | structured_output, conversation | Collaborative conversation for building shared content. |
| **DebateConversation** | 🔴 Complex | structured_output, conversation | Structured debate conversation with positions and formal argumentation. |
| **DirectedConversation** | 🔴 Complex | structured_output, conversation | Directed conversation where agents respond to mentions and questions. |
| **RoundRobinConversation** | 🔴 Complex | conversation | Round-robin conversation where each agent speaks in a fixed order. |

### Strategy Games

**5 agents** | **Packages:** haive-games

| Agent | Complexity | Features | Description |
|-------|------------|----------|-------------|
| **AmongUsAgent** | 🔴 Complex | Basic | Agent implementation for the Among Us game. |
| **MafiaAgent** | 🔴 Complex | Basic | Agent for playing Mafia. |
| **MafiaAgentConfig** | 🔴 Complex | structured_output | Configuration for the Mafia game agent. |
| **RiskAgent** | 🔴 Complex | reasoning, planning +1 | Agent for playing the Risk game. |
| **AmongUsAgentConfig** | 🟢 Simple | Basic | Configuration for Among Us game agent. |

### Card Games

**4 agents** | **Packages:** haive-games

| Agent | Complexity | Features | Description |
|-------|------------|----------|-------------|
| **BlackjackAgent** | 🔴 Complex | Basic | Multi-player Blackjack game agent. |
| **BlackjackAgentConfig** | 🔴 Complex | structured_output | Configuration for a multi-player Blackjack game agent. |
| **BullshitAgent** | 🔴 Complex | Basic | Multi-player Bullshit (BS) card game agent. |
| **BullshitAgentConfig** | 🟢 Simple | structured_output | Configuration for a Bullshit (BS) card game agent. |

### Legal & Business

**2 agents** | **Packages:** haive-prebuilt

| Agent | Complexity | Features | Description |
|-------|------------|----------|-------------|
| **ContractAnalysisAgent** | 🟢 Simple | Basic | No description available |
| **ContractAnalysisAgentConfig** | 🟢 Simple | Basic | No description available |

