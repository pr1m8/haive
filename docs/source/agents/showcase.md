# 🤖 Haive Agent Showcase

Welcome to the comprehensive showcase of Haive's intelligent agent ecosystem! This showcase presents **348 agents** across **18 categories**, demonstrating the full breadth and power of the Haive framework.

## 📊 Agent Ecosystem Overview

### 📈 Quick Stats

| Metric | Value |
|--------|-------|
| **Total Agents** | 348 |
| **Categories** | 18 |
| **Packages** | 3 |
| **Complex Agents** | 155 |

### 🏷️ Top Agent Categories

| Category | Agents | Primary Package |
|----------|--------|----------------|
| **RAG & Retrieval** | 132 | `haive-agents` |
| **Games** | 40 | `haive-games` |
| **ReAct & Tool Use** | 32 | `haive-agents` |
| **Specialized Agents** | 27 | `haive-agents` |
| **Reasoning & Critique** | 20 | `haive-agents` |
| **Document Processing** | 19 | `haive-agents` |
| **Multi-Agent Systems** | 13 | `haive-agents` |
| **Prebuilt Solutions** | 11 | `haive-prebuilt` |
| **Classic Games** | 9 | `haive-games` |
| **Foundation Agents** | 6 | `haive-agents` |
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

### RAG & Retrieval

**132 agents** | **Packages:** haive-agents

| Agent | Complexity | Features | Description |
|-------|------------|----------|-------------|
| **ActiveRetrievalAgent** | 🔴 Complex | retrieval, planning | Agent that performs active retrieval based on FLARE plans. |
| **AdaptiveGradedRAGAgent** | 🔴 Complex | retrieval | Adaptive Graded RAG - adjusts grading thresholds based on query complexity |
| **AdaptiveQueryDecomposerAgent** | 🔴 Complex | planning | Adaptive query decomposition that selects best strategy. |
| **AdaptiveRAGAgent** | 🔴 Complex | retrieval | Adaptive RAG that routes queries based on complexity. |
| **AdaptiveRAGAgent** | 🔴 Complex | retrieval | Adaptive RAG with complexity-based routing. |
| **AdaptiveRAGMultiAgent** | 🔴 Complex | retrieval, planning | Advanced RAG system that adapts its strategy based on query complexity and resul... |
| **AdvancedHallucinationGraderAgent** | 🔴 Complex | Basic | Advanced hallucination grading with detailed analysis. |
| **AgenticGraphRAGAgent** | 🔴 Complex | planning, retrieval +1 | Agentic Graph RAG - combines graph reasoning with agentic routing |
| **AgenticRAGAgent** | 🔴 Complex | tools, reasoning +2 | Agentic RAG agent combining ReAct reasoning with intelligent retrieval. |
| **AgenticRAGRouterAgent** | 🔴 Complex | retrieval, planning | Complete Agentic RAG Router with ReAct patterns and autonomous decision-making. |
| **AgenticRAGRouterAgent** | 🔴 Complex | retrieval | Agentic RAG Router - intelligently routes queries to different RAG strategies |
| **AgenticRAGState** | 🔴 Complex | retrieval, planning | RAG state for agentic routing and planning |
| **BaseRAGMultiAgent** | 🔴 Complex | conversation, retrieval | Base multi-agent RAG system with retrieve -> grade -> generate workflow. |
| **CompositeGradingAgent** | 🔴 Complex | Basic | Combines multiple grading components for comprehensive evaluation |
| **ConditionalRAGMultiAgent** | 🔴 Complex | conversation, retrieval | Conditional multi-agent RAG system with smart routing based on document quality. |
| **DebateRAGAgent** | 🔴 Complex | retrieval, reasoning | Debate RAG - multiple agents with different perspectives debate |
| **DomainAnalysisAgent** | 🔴 Complex | Basic | Analyzes queries to determine relevant domains for multi-domain generation. |
| **DynamicRAGAgent** | 🔴 Complex | retrieval, planning | Dynamic RAG with add/remove retrievers - adapts retrieval strategy |
| **EnhancedHyDERAGAgentV2** | 🔴 Complex | retrieval | Enhanced HyDE RAG Agent with advanced prompt selection and multi-document genera... |
| **EnhancedRAGParallelAgent** | 🔴 Complex | retrieval, structured_output | RAG parallel agent with built-in compatibility checking for consensus building. |
| **EnsembleHyDERetriever** | 🔴 Complex | retrieval | Retriever that handles multiple documents for ensemble retrieval. |
| **FLAREPlannerAgent** | 🔴 Complex | retrieval, planning | Agent that creates FLARE plans for iterative generation and active retrieval. |
| **GraphDBRAGAgent** | 🔴 Complex | tools, retrieval +1 | Graph Database RAG Agent for natural language querying of Neo4j databases. |
| **GraphRAGAgent** | 🔴 Complex | retrieval, reasoning | Graph RAG - uses knowledge graph construction and traversal |
| **HypothesisGeneratorAgent** | 🔴 Complex | reasoning | Agent that generates multiple hypotheses for speculative reasoning. |
| **IterativePlannerAgent** | 🔴 Complex | planning | Agent that creates iterative processing plans. |
| **IterativeRAGMultiAgent** | 🔴 Complex | conversation, retrieval | Multi-agent RAG system with iterative document processing. |
| **MultiAgentCompatibilityReport** | 🔴 Complex | Basic | Compatibility report for multiple agents in a workflow. |
| **MultiAgentRAGState** | 🔴 Complex | conversation, retrieval +1 | Comprehensive state schema for multi-agent RAG systems. |
| **MultiCriteriaGradedRAGAgent** | 🔴 Complex | retrieval | Multi-Criteria Graded RAG - uses multiple grading criteria and perspectives |
| **MultiCriteriaGradedRAGAgentV2** | 🔴 Complex | retrieval, structured_output | Multi-Criteria Graded RAG V2 - Configuration stored in state schema. |
| **MultiDomainHyDERetriever** | 🔴 Complex | Basic | Retriever that handles documents from multiple domains. |
| **MultiQueryRAGAgent** | 🔴 Complex | retrieval | Multi-Query RAG - generates multiple diverse queries and retrieves documents |
| **MultiQueryRAGAgent** | 🔴 Complex | retrieval | Multi-Query RAG with query expansion for improved recall. |
| **MultiQueryRetrievalAgent** | 🔴 Complex | retrieval, structured_output | Agent that uses a callable node for multi-query retrieval - proper Pydantic appr... |
| **MultiRetrievalAgent** | 🔴 Complex | retrieval | Agent that performs parallel retrieval with multiple queries. |
| **MultiStrategyRAGAgent** | 🔴 Complex | retrieval | RAG agent with multiple retrieval strategies. |
| **ParallelRAGMultiAgent** | 🔴 Complex | conversation, retrieval | Parallel multi-agent RAG system for consensus-based processing. |
| **QueryDecompositionRAGAgent** | 🔴 Complex | retrieval | Query Decomposition RAG - breaks complex queries into simpler sub-questions, |
| **QueryPlanningAgenticRAGAgent** | 🔴 Complex | planning, retrieval +1 | Query Planning Agentic RAG - creates detailed execution plans |
| **QueryPlanningRAGAgent** | 🔴 Complex | planning, retrieval +1 | Query Planning RAG agent with structured decomposition and execution. |
| **RAGFusionAgent** | 🔴 Complex | retrieval | RAG Fusion - combines multiple retrieval strategies and fuses results |
| **ReciprocalRankFusionAgent** | 🔴 Complex | retrieval | Agent that performs reciprocal rank fusion on multiple retrieval results. |
| **ReflexiveGradedRAGAgent** | 🔴 Complex | planning, retrieval +1 | Reflexive Graded RAG - uses grading feedback to improve its own performance |
| **SQLRAGAgent** | 🔴 Complex | tools, retrieval +1 | SQL RAG Agent for querying SQL databases with natural language. |
| **SelfCorrectiveRAGAgent** | 🔴 Complex | retrieval | RAG agent with self-correction capabilities. |
| **SelfRAGAgent** | 🔴 Complex | retrieval, reasoning | Self-RAG with reflection tokens - determines whether retrieval is needed |
| **SelfRAGAgent** | 🔴 Complex | retrieval, reasoning | Self-RAG with reflection tokens and adaptive retrieval. |
| **SelfRAGAgent** | 🔴 Complex | retrieval, reasoning | Self-RAG agent with reflection tokens and adaptive retrieval. |
| **SelfReflectiveAgenticRAGAgent** | 🔴 Complex | retrieval, reasoning | Self-Reflective Agentic RAG - continuously reflects on and improves |
| **SelfReflectiveRAGAgent** | 🔴 Complex | retrieval, reasoning | Self-Reflective RAG agent with iterative improvement capabilities. |
| **SelfRouteRAGAgent** | 🔴 Complex | retrieval, reasoning | Self-Route RAG - dynamically routes itself to different reasoning |
| **SelfRouteRAGAgent** | 🔴 Complex | planning, retrieval +1 | Complete Self-Route RAG agent with structured analysis and iterative planning. |
| **SimpleRAGAgent** | 🔴 Complex | tools, conversation +1 | Simple RAG agent that retrieves documents and provides basic answers. |
| **SimpleRAGWithMemoryAgent** | 🔴 Complex | conversation, memory +1 | Simple RAG with Memory - incorporates conversation history and previous queries |
| **SpeculativeRAGAgent** | 🔴 Complex | retrieval | Speculative RAG - generates multiple possible answer hypotheses |
| **StepBackQueryGeneratorAgent** | 🔴 Complex | reasoning | Agent that generates step-back queries for abstract reasoning. |
| **StepBackRAGAgent** | 🔴 Complex | retrieval, reasoning | Complete Step-Back RAG agent with abstract reasoning. |
| **DocumentGradingAgent** | 🟡 Medium | Basic | Document grading agent that evaluates document relevance. |
| **DynamicRAGAgent** | 🟡 Medium | retrieval | Implements a dynamic RAG pipeline that routes queries to appropriate data source... |
| **FilteredRAGAgent** | 🟡 Medium | retrieval | RAG agent with document filtering capabilities. |
| **TypedRAGAgent** | 🟡 Medium | retrieval | Implements Typed-RAG that classifies queries and routes to specialized handlers. |
| **AdaptiveHyDEGenerator** | 🟢 Simple | Basic | Generator that adapts its prompt based on query analysis. |
| **AdaptiveRAGAgent** | 🟢 Simple | Basic | RAG Workflow Factory |
| **AdaptiveThresholdRAGAgent** | 🟢 Simple | retrieval | Adaptive Threshold RAG - dynamically adjusts retrieval thresholds |
| **AdaptiveThresholdRAGAgentV2** | 🟢 Simple | retrieval | Adaptive Threshold RAG V2 - Configuration in AdaptiveThresholdRAGState |
| **AdaptiveToolsRAGAgent** | 🟢 Simple | tools, retrieval | Complete Adaptive RAG agent with tools integration and ReAct patterns. |
| **AgentCompatibilityReport** | 🟢 Simple | Basic | Comprehensive compatibility report for agent pairs. |
| **AgenticRAGRouterV2** | 🟢 Simple | retrieval | Agentic RAG Router using proper conditional routing. |
| **AgenticRAGState** | 🟢 Simple | retrieval, structured_output | State schema for agentic RAG with retrieval metadata. |
| **AgenticRouterResult** | 🟢 Simple | retrieval | Complete result from agentic RAG routing. |
| **BaseRAGAgent** | 🟢 Simple | tools, retrieval | Simple base RAG agent with retrieve and generate functionality. |
| **BaseRAGAgent** | 🟢 Simple | retrieval | Base RAG agent that performs retrieval. |
| **BaseRAGConfig** | 🟢 Simple | retrieval | Configuration for a basic RAG agent. |
| **CompatibleAdaptiveRAG** | 🟢 Simple | Basic | Compatible RAG Workflow Factory |
| **ConditionalCallableAgent** | 🟢 Simple | Basic | Agent with conditional routing based on callable results. |
| **ContextualQueryDecomposerAgent** | 🟢 Simple | Basic | Context-aware query decomposition agent. |
| **CorrectiveRAGAgent** | 🟢 Simple | retrieval | Full Corrective RAG implementation with web search fallback. |
| **CorrectiveRAGAgent** | 🟢 Simple | retrieval | Corrective RAG (CRAG) with automatic requerying and web search fallback. |
| **CorrectiveRAGAgent** | 🟢 Simple | retrieval | Corrective RAG with self-correcting retrieval. |
| **CorrectiveRAGAgentV2** | 🟢 Simple | retrieval | Corrective RAG with proper self-correcting retrieval. |
| **DebateRAGAgentV2** | 🟢 Simple | retrieval | Debate RAG V2 - Configuration in DebateRAGState |
| **DocumentGradingAgent** | 🟢 Simple | Basic | Agent that iterates over documents and grades each one. |
| **DocumentGradingAgent** | 🟢 Simple | Basic | Agent that grades retrieved documents for relevance. |
| **DocumentGradingAgent** | 🟢 Simple | Basic | Agent that grades retrieved documents for relevance. |
| **DocumentGradingRAGAgent** | 🟢 Simple | retrieval | RAG with document grading and filtering. |
| **DualRetrievalAgent** | 🟢 Simple | retrieval | Agent that performs both original and step-back retrieval. |
| **DynamicRAGAgentV2** | 🟢 Simple | retrieval | Dynamic RAG V2 - Configuration in DynamicRAGState |
| **EnhancedHyDERAGAgent** | 🟢 Simple | tools, retrieval +1 | Enhanced HyDE RAG Agent using the structured output enhancement pattern. |
| **EnhancedHyDERetriever** | 🟢 Simple | structured_output | Enhanced retriever that handles both enhancement pattern and traditional outputs... |
| **EnhancedHyDERetrieverV2** | 🟢 Simple | Basic | Enhanced retriever with better state handling and fallback mechanisms. |
| **EnhancedRAGConditionalAgent** | 🟢 Simple | retrieval | RAG conditional agent with built-in compatibility checking and smart routing. |
| **EnhancedRAGSequentialAgent** | 🟢 Simple | retrieval | RAG sequential agent with built-in compatibility checking. |
| **EnsembleDocumentParser** | 🟢 Simple | structured_output | Parses ensemble document output into individual documents. |
| **FLAREAgent** | 🟢 Simple | retrieval | Forward-Looking Active REtrieval (FLARE) - generates text while actively |
| **FLAREAgentV2** | 🟢 Simple | Basic | FLARE V2 - Configuration stored in FLAREState |
| **FLAREAgentV2Example** | 🟢 Simple | structured_output | FLARE Agent V2 example using enhanced state schema |
| **FLARERAGAgent** | 🟢 Simple | retrieval | Complete FLARE RAG agent with forward-looking active retrieval. |
| **FullyGradedRAGAgent** | 🟢 Simple | retrieval | Fully Graded RAG - comprehensive grading at every step of the RAG pipeline. |
| **FullyGradedRAGAgentV2** | 🟢 Simple | retrieval, structured_output | Fully Graded RAG V2 - Uses enhanced state schema with configuration support. |
| **GenericCallableAgent** | 🟢 Simple | tools | Generic agent that executes a sequence of callable functions. |
| **GraphDBRAGConfig** | 🟢 Simple | retrieval, structured_output | Main configuration for the Graph Database RAG Agent. |
| **HYDERAGAgent** | 🟢 Simple | retrieval | Enhanced HYDE RAG with hypothesis generation. |
| **HYDERAGAgent** | 🟢 Simple | retrieval | HYDE RAG agent that generates hypothetical documents before retrieval. |
| **HallucinationGraderAgent** | 🟢 Simple | Basic | Basic hallucination grading agent. |
| **HierarchicalQueryDecomposerAgent** | 🟢 Simple | Basic | Hierarchical query decomposition agent. |
| **HyDEAgentConfig** | 🟢 Simple | retrieval | Configuration for Enhanced HyDE RAG Agent. |
| **HyDEDocumentAnalyzer** | 🟢 Simple | structured_output | Analyzes generated hypothetical documents and extracts structured information. |
| **HyDERAGAgentV2** | 🟢 Simple | retrieval | HyDE RAG using hypothetical document generation for better retrieval. |
| **HyDERetrieverAgent** | 🟢 Simple | retrieval | Custom retriever that uses hypothetical document for enhanced retrieval. |
| **IterativeDocumentGradingAgent** | 🟢 Simple | Basic | Specialized grading agent that processes documents one by one. |
| **LLMRAGAgent** | 🟢 Simple | retrieval | LLM-enhanced RAG agent that retrieves documents and generates answers. |
| **MemoryAwareRAGAgent** | 🟢 Simple | memory, retrieval | Complete Memory-Aware RAG agent with persistent learning. |
| **MemoryRetrievalAgent** | 🟢 Simple | Basic | Agent that retrieves relevant memories for context enhancement. |
| **ParallelVerificationAgent** | 🟢 Simple | Basic | Agent that performs parallel hypothesis verification. |
| **QueryAnalysisAgent** | 🟢 Simple | Basic | Agent that analyzes queries and selects appropriate prompt types. |
| **QueryAnalyzerAgent** | 🟢 Simple | structured_output | Agent that performs structured query analysis for routing. |
| **QueryDecomposerAgent** | 🟢 Simple | Basic | Basic query decomposition agent. |
| **RAGFusionAgent** | 🟢 Simple | retrieval | Complete RAG Fusion agent with query expansion and RRF. |
| **RealtimeHallucinationGraderAgent** | 🟢 Simple | Basic | Fast hallucination checker for real-time applications. |
| **RequeryDecisionAgent** | 🟢 Simple | Basic | Agent that decides if requerying is needed based on document grades. |
| **RequeryDecisionAgent** | 🟢 Simple | Basic | Agent that decides if requerying is needed based on document grades. |
| **RoutingDecisionAgent** | 🟢 Simple | Basic | Agent that makes final routing decisions. |
| **SQLRAGConfig** | 🟢 Simple | retrieval, structured_output | Configuration for the SQL RAG Agent. |
| **SearchIntegrationAgent** | 🟢 Simple | tools, retrieval | Agent that integrates external search tools. |
| **SimpleCorrectiveRAGAgent** | 🟢 Simple | retrieval | Simple Corrective RAG implementation using sequential processing. |
| **SimpleHYDERAGAgent** | 🟢 Simple | retrieval | Simple HYDE RAG agent that generates hypothetical documents before retrieval. |
| **SimpleRAGAgent** | 🟢 Simple | retrieval | Simple RAG workflow: Retrieval → Answer Generation |
| **SimpleRAGAnswerAgent** | 🟢 Simple | retrieval, structured_output | RAG answer generation agent that creates responses from retrieved documents. |
| **SpeculativeRAGAgent** | 🟢 Simple | retrieval | Complete Speculative RAG agent with parallel hypothesis processing. |
| **StepBackPromptingRAGAgent** | 🟢 Simple | retrieval | Step-Back Prompting RAG - asks broader conceptual questions before |
| **ToolSelectionAgent** | 🟢 Simple | tools | Agent that selects optimal tools based on query analysis. |

### Games

**40 agents** | **Packages:** haive-games

| Agent | Complexity | Features | Description |
|-------|------------|----------|-------------|
| **BattleshipAgent** | 🔴 Complex | memory, planning | Battleship game agent with LLM-powered players. |
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
| **ReactAgent** | 🔴 Complex | tools, reasoning +1 | A tool-using agent implementing the ReAct pattern. |
| **ReactAgent** | 🔴 Complex | tools, reasoning +1 | A React agent implementing the Reasoning-Action-Observation pattern. |
| **ReactAgent** | 🔴 Complex | tools, reasoning | A React agent implementation using LangGraph. |
| **ReactAgent** | 🔴 Complex | tools, reasoning | React Agent implementation that extends SimpleAgent. |
| **ReactAgent** | 🔴 Complex | tools, reasoning | A React agent that enhances SimpleAgent with tool-using capabilities. |
| **ReactAgentConfig** | 🔴 Complex | tools, reasoning | Configuration for a ReAct agent with tool integration. |
| **ReactAgentConfig** | 🔴 Complex | tools, memory +1 | Configuration for a React agent that can use tools. |
| **ReactAgentConfig** | 🔴 Complex | tools, reasoning | Configuration for a React agent, extending SimpleAgentConfig. |
| **ReactAgentConfig** | 🔴 Complex | tools, reasoning | Configuration for React Agent, extending SimpleAgentConfig. |
| **ReactAgentConfig** | 🔴 Complex | tools, reasoning | Configuration for a React agent that can use tools and follow ReAct reasoning pa... |
| **ReactAgentState** | 🔴 Complex | tools, reasoning +1 | State for React Agent, extending SimpleAgentState. |
| **ReactManyToolsAgent** | 🔴 Complex | tools, retrieval | React Agent implementation that can handle many tools efficiently. |
| **DynamicReactAgent** | 🟡 Medium | tools | A React agent with dynamic tool selection. |
| **ReactAgent** | 🟡 Medium | Basic | No description available |
| **ReactAgentState** | 🟡 Medium | tools, memory +1 | State for React agents with tool usage. |
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

### Specialized Agents

**27 agents** | **Packages:** haive-agents

| Agent | Complexity | Features | Description |
|-------|------------|----------|-------------|
| **Agent** | 🔴 Complex | memory, structured_output | Abstract base agent class that extends InvokableEngine with execution and state ... |
| **Agent** | 🔴 Complex | Basic | Abstract base agent class with automatic graph building and proper inheritance. |
| **ChainAgent** | 🔴 Complex | tools, structured_output | An agent that chains multiple engines together, passing output from one to the n... |
| **ChainAgentConfig** | 🔴 Complex | Basic | Configuration for a chain agent that processes input through multiple engines in... |
| **GenericAgent** | 🔴 Complex | structured_output | Generic agent base class with enhanced typing and auto-configuration. |
| **SequentialAgent** | 🔴 Complex | Basic | Sequential agent that executes multiple agents in sequence. |
| **TaskAnalysisAgent** | 🔴 Complex | planning | Comprehensive task analysis agent that orchestrates multiple analysis engines. |
| **AgentDebugger** | 🟡 Medium | Basic | Rich UI debugger for agent execution. |
| **SequentialAgentConfig** | 🟡 Medium | structured_output | Configuration for a SequentialAgent that connects components linearly. |
| **WebNavAgent** | 🟡 Medium | tools | An interactive web navigation agent using Playwright & LangGraph with integrated... |
| **Agent** | 🟢 Simple | Basic | Complete agent protocol combining all capabilities. |
| **AutoTypedAgent** | 🟢 Simple | Basic | Generic Agent Base Class with Enhanced Typing and Auto-Configuration |
| **ChainAgentSchema** | 🟢 Simple | structured_output | Schema for chain agents with intermediate results, extending SimpleAgentSchema. |
| **DefaultAgentInput** | 🟢 Simple | structured_output | Default input schema for generic agents. |
| **DefaultAgentOutput** | 🟢 Simple | structured_output | Default output schema for generic agents. |
| **DefaultAgentState** | 🟢 Simple | structured_output | Default state schema for generic agents. |
| **DocumentAgent** | 🟢 Simple | Basic | No description available |
| **DocumentAgentConfig** | 🟢 Simple | Basic | The configuration for the document agent. |
| **InterviewAgent** | 🟢 Simple | Basic | An agent that conducts an interview with a Subject Matter Expert. |
| **InterviewAgentConfig** | 🟢 Simple | Basic | Configuration for the Interview Agent. |
| **RoutingAgent** | 🟢 Simple | Basic | Simple agent with conditional routing capabilities. |
| **RoutingAgentConfig** | 🟢 Simple | Basic | Configuration for a routing agent. |
| **RoutingAgentSchema** | 🟢 Simple | structured_output | Schema for routing agents. |
| **TypedAgent** | 🟢 Simple | Basic | Generic Agent Base Class with Enhanced Typing and Auto-Configuration |
| **WebNavAgentConfig** | 🟢 Simple | Basic | Configuration for the Web Navigator Agent. |
| **WikiWriterAgent** | 🟢 Simple | Basic | An agent that writes a wiki page. |
| **WikiWriterAgentConfig** | 🟢 Simple | Basic | Configuration for the Wiki Writer Agent. |

### Reasoning & Critique

**20 agents** | **Packages:** haive-agents

| Agent | Complexity | Features | Description |
|-------|------------|----------|-------------|
| **LATSAgent** | 🔴 Complex | retrieval, reasoning | A Look-Ahead Tree Search (LATS) agent that uses tree search to |
| **LATSAgentConfig** | 🔴 Complex | tools, retrieval +1 | Configuration for a Look-Ahead Tree Search (LATS) agent. |
| **ReasoningSystem** | 🔴 Complex | reasoning | Orchestrator agent for comprehensive reasoning analysis. |
| **ReflectionAgent** | 🔴 Complex | reasoning | An agent with self-reflection capabilities that can improve its responses. |
| **ReflectionAgentConfig** | 🔴 Complex | reasoning | Configuration for an agent that uses reflection to improve responses. |
| **ReflectionAgentState** | 🔴 Complex | reasoning, structured_output | State schema for the Reflection agent. |
| **SelfDiscoverAgent** | 🔴 Complex | planning, reasoning +1 | An agent that implements the SelfDiscover methodology with structured output mod... |
| **SelfDiscoverAgentConfig** | 🔴 Complex | reasoning, structured_output | Configuration for a SelfDiscover agent. |
| **TOTAgentConfig** | 🔴 Complex | retrieval, reasoning | Configuration for the Tree of Thoughts agent. |
| **ToTAgent** | 🔴 Complex | retrieval, reasoning | Tree of Thoughts agent implementation. |
| **ToTAgentConfig** | 🔴 Complex | retrieval, reasoning | Configuration for a Tree of Thoughts agent. |
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

**19 agents** | **Packages:** haive-agents

| Agent | Complexity | Features | Description |
|-------|------------|----------|-------------|
| **ComplexExtractionAgent** | 🔴 Complex | structured_output | Agent that extracts complex structured information from text. |
| **ComplexExtractionAgentConfig** | 🔴 Complex | tools, structured_output | Configuration for the complex extraction agent. |
| **DocumentAgent** | 🔴 Complex | conversation, memory +2 | Comprehensive Document Processing Agent. |
| **DocumentLoaderAgent** | 🔴 Complex | retrieval, structured_output | Document Loader Agent that integrates the document loader engine with the agent ... |
| **ParallelKGTransformer** | 🔴 Complex | retrieval | An agent that builds a knowledge graph by extracting |
| **StructuredKGAgent** | 🔴 Complex | retrieval, structured_output | An agent that builds a knowledge graph using structured output models. |
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

**13 agents** | **Packages:** haive-agents

| Agent | Complexity | Features | Description |
|-------|------------|----------|-------------|
| **ChainMultiAgent** | 🔴 Complex | conversation | ChainAgent that works with the multi-agent framework. |
| **ChainNodeWrapper** | 🔴 Complex | conversation | Wrapper to make non-agent nodes work in multi-agent framework. |
| **CompatibilityEnhancedMultiAgent** | 🔴 Complex | conversation, retrieval | Multi-agent system with built-in compatibility checking and automatic adaptation... |
| **ConditionalAgent** | 🔴 Complex | conversation | Pre-configured conditional multi-agent with branching. |
| **MultiAgent** | 🔴 Complex | structured_output, tools +3 | Abstract base class for sophisticated multi-agent systems. |
| **MultiAgent** | 🔴 Complex | conversation | Abstract base class for multi-agent systems. |
| **MultiAgent** | 🔴 Complex | conversation, retrieval +1 | Advanced multi-agent system with flexible coordination patterns. |
| **ParallelAgent** | 🔴 Complex | conversation | Pre-configured parallel multi-agent. |
| **SequentialAgent** | 🔴 Complex | conversation, structured_output | Multi-agent system with sequential execution. |
| **SequentialMultiAgent** | 🔴 Complex | conversation, structured_output | Multi-agent system that executes agents sequentially. |
| **CompatibilityEnhancedConditionalAgent** | 🟢 Simple | Basic | Conditional agent with built-in compatibility checking. |
| **CompatibilityEnhancedParallelAgent** | 🟢 Simple | Basic | Parallel agent with built-in compatibility checking. |
| **CompatibilityEnhancedSequentialAgent** | 🟢 Simple | Basic | Sequential agent with built-in compatibility checking. |

### Prebuilt Solutions

**11 agents** | **Packages:** haive-prebuilt

| Agent | Complexity | Features | Description |
|-------|------------|----------|-------------|
| **AgentAction** | 🔴 Complex | tools, retrieval +1 | Model representing an agent's action decision. |
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
| **AgentDecision** | 🔴 Complex | planning, reasoning | Agent's decision in the game. |
| **AgentDecisionSchema** | 🔴 Complex | planning, reasoning +1 | Schema for LLM decision output. |
| **CheckersAgent** | 🔴 Complex | structured_output | Agent for playing checkers with LLM-based players and rich UI. |
| **GoAgent** | 🔴 Complex | tools | Go game agent implementation. |
| **PokerAgent** | 🔴 Complex | structured_output | Enhanced agent class for managing a multi-player Texas Hold'em poker game. |
| **PokerAgentTester** | 🔴 Complex | Basic | Test suite for the Poker agent. |
| **CheckersAgentConfig** | 🟢 Simple | structured_output | Configuration for checkers game agent. |
| **GoAgentConfig** | 🟢 Simple | structured_output | Configuration for the Go game agent. |
| **PokerAgentConfig** | 🟢 Simple | memory, retrieval +1 | Configuration class for the poker agent. |

### Foundation Agents

**6 agents** | **Packages:** haive-agents

| Agent | Complexity | Features | Description |
|-------|------------|----------|-------------|
| **SimpleAgent** | 🔴 Complex | tools, conversation +1 | Simple agent that modifies its engine to include structured output schema. |
| **SimpleAgentState** | 🔴 Complex | conversation, memory | Base state for simple agents. |
| **ChainAgent** | 🟡 Medium | Basic | The simplest way to build chains - just list nodes and edges. |
| **SimpleAgent** | 🟢 Simple | structured_output | A simple agent with a single node workflow and comprehensive schema handling. |
| **SimpleAgentConfig** | 🟢 Simple | structured_output | Configuration for a simple single-node agent with comprehensive schema handling. |
| **StructuredOutputAgentConfig** | 🟢 Simple | tools, structured_output | Configuration for a structured output agent. |

### Research & Information

**6 agents** | **Packages:** haive-agents

| Agent | Complexity | Features | Description |
|-------|------------|----------|-------------|
| **PersonResearchAgent** | 🔴 Complex | reasoning, retrieval +1 | Advanced person research agent with iterative information gathering capabilities... |
| **ResearchAgent** | 🔴 Complex | retrieval | Agent for performing deep research on any topic with dynamic document loader sel... |
| **STORMAgentConfig** | 🟡 Medium | retrieval | Configuration for the STORM agent - an orchestrator that coordinates research, |
| **PersonResearchAgentConfig** | 🟢 Simple | retrieval | Configuration settings for person research agent. |
| **PersonResearchAgentConfig** | 🟢 Simple | retrieval | Configuration for the Person Research Agent. |
| **ResearchAgentConfig** | 🟢 Simple | tools, retrieval +1 | Configuration for open_perplexity research agent. |

### Planning & Strategy

**6 agents** | **Packages:** haive-agents

| Agent | Complexity | Features | Description |
|-------|------------|----------|-------------|
| **LLMCompilerAgent** | 🔴 Complex | planning, structured_output | LLM Compiler Agent implementation. |
| **RewooAgent** | 🔴 Complex | planning, tools +2 | ReWOO (Reasoning Without Observation) Agent implementation. |
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
| **CollaborativeConversation** | 🔴 Complex | conversation, structured_output | Collaborative conversation for building shared content. |
| **DebateConversation** | 🔴 Complex | conversation, structured_output | Structured debate conversation with positions and formal argumentation. |
| **DirectedConversation** | 🔴 Complex | conversation, structured_output | Directed conversation where agents respond to mentions and questions. |
| **RoundRobinConversation** | 🔴 Complex | conversation | Round-robin conversation where each agent speaks in a fixed order. |

### Strategy Games

**5 agents** | **Packages:** haive-games

| Agent | Complexity | Features | Description |
|-------|------------|----------|-------------|
| **AmongUsAgent** | 🔴 Complex | Basic | Agent implementation for the Among Us game. |
| **MafiaAgent** | 🔴 Complex | Basic | Agent for playing Mafia. |
| **MafiaAgentConfig** | 🔴 Complex | structured_output | Configuration for the Mafia game agent. |
| **RiskAgent** | 🔴 Complex | planning, memory +1 | Agent for playing the Risk game. |
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

