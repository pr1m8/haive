# 📚 Complete Agent Index

Alphabetical listing of all agents in the Haive ecosystem.

## A

**ActiveRetrievalAgent** (🔴 Complex)
_RAG & Retrieval | haive-agents_
Agent that performs active retrieval based on FLARE plans.
**Features:** planning, retrieval
**Module:** `haive.agents.rag.flare.agent`

**AdaptiveGradedRAGAgent** (🔴 Complex)
_RAG & Retrieval | haive-agents_
Adaptive Graded RAG - adjusts grading thresholds based on query complexity
**Features:** retrieval
**Module:** `haive.agents.rag.multi_agent_rag.graded_rag_workflows`

**AdaptiveHyDEGenerator** (🟢 Simple)
_RAG & Retrieval | haive-agents_
Generator that adapts its prompt based on query analysis.
**Features:** Basic
**Module:** `haive.agents.rag.hyde.enhanced_agent_v2`

**AdaptiveQueryDecomposerAgent** (🔴 Complex)
_RAG & Retrieval | haive-agents_
Adaptive query decomposition that selects best strategy.
**Features:** planning
**Module:** `haive.agents.rag.query_decomposition.agent`

**AdaptiveRAGAgent** (🟢 Simple)
_RAG & Retrieval | haive-agents_
RAG Workflow Factory
**Features:** Basic
**Module:** `haive.agents.rag.factories.rag_workflow_factory`

**AdaptiveRAGAgent** (🔴 Complex)
_RAG & Retrieval | haive-agents_
Adaptive RAG that routes queries based on complexity.
**Features:** retrieval
**Module:** `haive.agents.rag.adaptive.agent`

**AdaptiveRAGAgent** (🔴 Complex)
_RAG & Retrieval | haive-agents_
Adaptive RAG with complexity-based routing.
**Features:** retrieval
**Module:** `haive.agents.rag.multi_agent_rag.complete_rag_workflows`

**AdaptiveRAGMultiAgent** (🔴 Complex)
_RAG & Retrieval | haive-agents_
Advanced RAG system that adapts its strategy based on query complexity and results.
**Features:** planning, retrieval
**Module:** `haive.agents.rag.multi_agent_rag.multi_rag`

**AdaptiveThresholdRAGAgent** (🟢 Simple)
_RAG & Retrieval | haive-agents_
Adaptive Threshold RAG - dynamically adjusts retrieval thresholds
**Features:** retrieval
**Module:** `haive.agents.rag.multi_agent_rag.specialized_workflows`

**AdaptiveThresholdRAGAgentV2** (🟢 Simple)
_RAG & Retrieval | haive-agents_
Adaptive Threshold RAG V2 - Configuration in AdaptiveThresholdRAGState
**Features:** retrieval
**Module:** `haive.agents.rag.multi_agent_rag.specialized_workflows_v2`

**AdaptiveToolsRAGAgent** (🟢 Simple)
_RAG & Retrieval | haive-agents_
Complete Adaptive RAG agent with tools integration and ReAct patterns.
**Features:** retrieval, tools
**Module:** `haive.agents.rag.adaptive_tools.agent`

**AdvancedHallucinationGraderAgent** (🔴 Complex)
_RAG & Retrieval | haive-agents_
Advanced hallucination grading with detailed analysis.
**Features:** Basic
**Module:** `haive.agents.rag.hallucination_grading.agent`

**AdvancedReactAgent** (🔴 Complex)
_ReAct & Tool Use | haive-agents_
Advanced React agent with specialized tool routing.
**Features:** tools
**Module:** `haive.agents.react_class.react_agent2.advanced_agent3`

**AdvancedReactAgentConfig** (🔴 Complex)
_ReAct & Tool Use | haive-agents_
Extended configuration for the Advanced React Agent.
**Features:** tools
**Module:** `haive.agents.react_class.react_agent2.advanced_agent3`

**Agent** (🔴 Complex)
_Specialized Agents | haive-agents_
Universal base class for all agent types in the Haive framework.
**Features:** reasoning, tools
**Module:** `haive.agents.base.universal_agent`

**Agent** (🔴 Complex)
_Foundation Agents | haive-agents_
Base class for LLM-based reasoning agents.
**Features:** reasoning, tools, memory, +1 more
**Module:** `haive.agents.base.simple_agent_base`

**Agent** (🔴 Complex)
_Specialized Agents | haive-agents_
Abstract base agent class that extends InvokableEngine with execution and state management.
**Features:** memory, structured_output
**Module:** `haive.agents.base.agent`

**Agent** (🟢 Simple)
_Specialized Agents | haive-agents_
Complete agent protocol combining all capabilities.
**Features:** Basic
**Module:** `haive.agents.base.types`

**Agent** (🔴 Complex)
_Specialized Agents | haive-agents_
Abstract base agent class with automatic graph building and proper inheritance.
**Features:** Basic
**Module:** `haive.agents.base..ipynb_checkpoints.__init__-checkpoint`

**AgentAction** (🔴 Complex)
_Prebuilt Solutions | haive-prebuilt_
Model representing an agent's action decision.
**Features:** reasoning, retrieval, tools
**Module:** `haive.prebuilt.gtla.models`

**AgentCompatibilityReport** (🟢 Simple)
_RAG & Retrieval | haive-agents_
Comprehensive compatibility report for agent pairs.
**Features:** Basic
**Module:** `haive.agents.rag.multi_agent_rag.compatibility`

**AgentDebugger** (🟡 Medium)
_Specialized Agents | haive-agents_
Rich UI debugger for agent execution.
**Features:** Basic
**Module:** `haive.agents.base.debug_utils`

**AgentDecision** (🔴 Complex)
_Classic Games | haive-games_
Agent's decision in the game.
**Features:** reasoning, planning
**Module:** `haive.games.poker.models`

**AgentDecisionSchema** (🔴 Complex)
_Classic Games | haive-games_
Schema for LLM decision output.
**Features:** reasoning, planning, structured_output
**Module:** `haive.games.poker.models`

**AgentInput** (🟢 Simple)
_Specialized Agents | haive-agents_
Default input schema for agents.
**Features:** structured_output
**Module:** `haive.agents.base.types`

**AgentMetadata** (🟢 Simple)
_Prebuilt Solutions | haive-prebuilt_
Metadata about agent contributions to content generation.
**Features:** tools
**Module:** `haive.prebuilt.startup.pitchdeck.models`

**AgentOutput** (🟢 Simple)
_Specialized Agents | haive-agents_
Default output schema for agents.
**Features:** structured_output
**Module:** `haive.agents.base.types`

**AgentOutput** (🟢 Simple)
_Prebuilt Solutions | haive-prebuilt_
Model representing the output from an agent's action.
**Features:** structured_output
**Module:** `haive.prebuilt.gtla.models`

**AgentRegistry** (🔴 Complex)
_Specialized Agents | haive-agents_
Manages agent lifecycle and routing model synchronization.
**Features:** Basic
**Module:** `haive.agents.supervisor.registry`

**AgentState** (🟢 Simple)
_Specialized Agents | haive-agents_
Default state schema for agents.
**Features:** structured_output
**Module:** `haive.agents.base.types`

**AgentState** (🟢 Simple)
_Academic & Research | haive-prebuilt_
No description available
**Features:** Basic
**Module:** `haive.prebuilt.systemic_review_of_scientific_articles.state`

**AgenticGraphRAGAgent** (🔴 Complex)
_RAG & Retrieval | haive-agents_
Agentic Graph RAG - combines graph reasoning with agentic routing
**Features:** reasoning, planning, retrieval
**Module:** `haive.agents.rag.multi_agent_rag.advanced_workflows`

**AgenticRAGAgent** (🔴 Complex)
_RAG & Retrieval | haive-agents_
Agentic RAG agent combining ReAct reasoning with intelligent retrieval.
**Features:** reasoning, retrieval, tools, +1 more
**Module:** `haive.agents.rag.agentic.agent`

**AgenticRAGRouterAgent** (🔴 Complex)
_RAG & Retrieval | haive-agents_
Complete Agentic RAG Router with ReAct patterns and autonomous decision-making.
**Features:** planning, retrieval
**Module:** `haive.agents.rag.agentic_router.agent`

**AgenticRAGRouterAgent** (🔴 Complex)
_RAG & Retrieval | haive-agents_
Agentic RAG Router - intelligently routes queries to different RAG strategies
**Features:** retrieval
**Module:** `haive.agents.rag.multi_agent_rag.advanced_workflows`

**AgenticRAGRouterV2** (🟢 Simple)
_RAG & Retrieval | haive-agents_
Agentic RAG Router using proper conditional routing.
**Features:** retrieval
**Module:** `haive.agents.rag.agentic_router.agent_v2`

**AgenticRAGState** (🔴 Complex)
_RAG & Retrieval | haive-agents_
RAG state for agentic routing and planning
**Features:** planning, retrieval
**Module:** `haive.agents.rag.multi_agent_rag.advanced_workflows`

**AgenticRAGState** (🟢 Simple)
_RAG & Retrieval | haive-agents_
State schema for agentic RAG with retrieval metadata.
**Features:** retrieval, structured_output
**Module:** `haive.agents.rag.agentic.agent`

**AgenticRouterResult** (🟢 Simple)
_RAG & Retrieval | haive-agents_
Complete result from agentic RAG routing.
**Features:** retrieval
**Module:** `haive.agents.rag.agentic_router.agent`

**AmongUsAgent** (🔴 Complex)
_Strategy Games | haive-games_
Agent implementation for the Among Us game.
**Features:** Basic
**Module:** `haive.games.among_us.agent`

**AmongUsAgentConfig** (🟢 Simple)
_Strategy Games | haive-games_
Configuration for Among Us game agent.
**Features:** Basic
**Module:** `haive.games.among_us.config`

**AutoTypedAgent** (🟢 Simple)
_Specialized Agents | haive-agents_
Generic Agent Base Class with Enhanced Typing and Auto-Configuration
**Features:** Basic
**Module:** `haive.agents.base.generic_agent`

## B

**BaseConversationAgent** (🔴 Complex)
_Conversation & Multi-Agent | haive-agents_
Base conversation agent that orchestrates multi-agent conversations.
**Features:** tools, conversation
**Module:** `haive.agents.conversation.base.agent`

**BaseGameConfig** (🔴 Complex)
_Games | haive-games_
Base configuration for all configurable games.
**Features:** retrieval
**Module:** `haive.games.core.config.base`

**BasePlayerAgent** (🟢 Simple)
_Games | haive-games_
No description available
**Features:** Basic
**Module:** `haive.games.framework.core.agent`

**BasePlayerAgent** (🟢 Simple)
_Games | haive-games_
Base class for player agents.
**Features:** Basic
**Module:** `haive.games.core.players.agent`

**BaseRAGAgent** (🟢 Simple)
_RAG & Retrieval | haive-agents_
Simple base RAG agent with retrieve and generate functionality.
**Features:** retrieval, tools
**Module:** `haive.agents.rag.base.base_agent`

**BaseRAGAgent** (🟢 Simple)
_RAG & Retrieval | haive-agents_
Base RAG agent that performs retrieval.
**Features:** retrieval
**Module:** `haive.agents.rag.base.agent`

**BaseRAGConfig** (🟢 Simple)
_RAG & Retrieval | haive-agents_
Configuration for a basic RAG agent.
**Features:** retrieval
**Module:** `haive.agents.rag.base.config`

**BaseRAGMultiAgent** (🔴 Complex)
_RAG & Retrieval | haive-agents_
Base multi-agent RAG system with retrieve -> grade -> generate workflow.
**Features:** retrieval, conversation
**Module:** `haive.agents.rag.multi_agent_rag.multi_rag`

**BattleshipAgent** (🔴 Complex)
_Games | haive-games_
Battleship game agent with LLM-powered players.
**Features:** planning, memory
**Module:** `haive.games.battleship.agent`

**BattleshipAgentConfig** (🟢 Simple)
_Games | haive-games_
Configuration class for Battleship game agents.
**Features:** structured_output
**Module:** `haive.games.battleship.config`

**BlackjackAgent** (🔴 Complex)
_Card Games | haive-games_
Multi-player Blackjack game agent.
**Features:** Basic
**Module:** `haive.games.cards.standard.blackjack.agent`

**BlackjackAgentConfig** (🔴 Complex)
_Card Games | haive-games_
Configuration for a multi-player Blackjack game agent.
**Features:** structured_output
**Module:** `haive.games.cards.standard.blackjack.config`

**BullshitAgent** (🔴 Complex)
_Card Games | haive-games_
Multi-player Bullshit (BS) card game agent.
**Features:** Basic
**Module:** `haive.games.cards.standard.bs.agent`

**BullshitAgentConfig** (🟢 Simple)
_Card Games | haive-games_
Configuration for a Bullshit (BS) card game agent.
**Features:** structured_output
**Module:** `haive.games.cards.standard.bs.config`

## C

**ChainAgent** (🔴 Complex)
_Specialized Agents | haive-agents_
An agent that chains multiple engines together, passing output from one to the next.
**Features:** tools, structured_output
**Module:** `haive.agents.chain_agent`

**ChainAgent** (🟡 Medium)
_Foundation Agents | haive-agents_
The simplest way to build chains - just list nodes and edges.
**Features:** Basic
**Module:** `haive.agents.chain.chain_agent_simple`

**ChainAgentConfig** (🔴 Complex)
_Specialized Agents | haive-agents_
Configuration for a chain agent that processes input through multiple engines in sequence.
**Features:** Basic
**Module:** `haive.agents.chain_agent`

**ChainAgentSchema** (🟢 Simple)
_Specialized Agents | haive-agents_
Schema for chain agents with intermediate results, extending SimpleAgentSchema.
**Features:** structured_output
**Module:** `haive.agents.chain_agent`

**ChainMultiAgent** (🔴 Complex)
_Multi-Agent Systems | haive-agents_
ChainAgent that works with the multi-agent framework.
**Features:** conversation
**Module:** `haive.agents.chain.multi_integration`

**ChainNodeWrapper** (🔴 Complex)
_Multi-Agent Systems | haive-agents_
Wrapper to make non-agent nodes work in multi-agent framework.
**Features:** conversation
**Module:** `haive.agents.chain.multi_integration`

**CheckersAgent** (🔴 Complex)
_Classic Games | haive-games_
Agent for playing checkers with LLM-based players and rich UI.
**Features:** structured_output
**Module:** `haive.games.checkers.agent`

**CheckersAgentConfig** (🟢 Simple)
_Classic Games | haive-games_
Configuration for checkers game agent.
**Features:** structured_output
**Module:** `haive.games.checkers.config`

**ClueAgent** (🟢 Simple)
_Games | haive-games_
Agent for playing Clue.
**Features:** Basic
**Module:** `haive.games.clue.agent`

**CollaborativeConversation** (🔴 Complex)
_Conversation & Multi-Agent | haive-agents_
Collaborative conversation for building shared content.
**Features:** structured_output, conversation
**Module:** `haive.agents.conversation.collaberative.agent`

**CompatibilityEnhancedConditionalAgent** (🟢 Simple)
_Multi-Agent Systems | haive-agents_
Conditional agent with built-in compatibility checking.
**Features:** Basic
**Module:** `haive.agents.multi.compatibility_enhanced_base`

**CompatibilityEnhancedMultiAgent** (🔴 Complex)
_Multi-Agent Systems | haive-agents_
Multi-agent system with built-in compatibility checking and automatic adaptation.
**Features:** retrieval, conversation
**Module:** `haive.agents.multi.compatibility_enhanced_base`

**CompatibilityEnhancedParallelAgent** (🟢 Simple)
_Multi-Agent Systems | haive-agents_
Parallel agent with built-in compatibility checking.
**Features:** Basic
**Module:** `haive.agents.multi.compatibility_enhanced_base`

**CompatibilityEnhancedSequentialAgent** (🟢 Simple)
_Multi-Agent Systems | haive-agents_
Sequential agent with built-in compatibility checking.
**Features:** Basic
**Module:** `haive.agents.multi.compatibility_enhanced_base`

**CompatibleAdaptiveRAG** (🟢 Simple)
_RAG & Retrieval | haive-agents_
Compatible RAG Workflow Factory
**Features:** Basic
**Module:** `haive.agents.rag.factories.compatible_rag_factory`

**CompiledAgent** (🔴 Complex)
_Specialized Agents | haive-agents_
Agent class based on CompiledStateGraph architecture.
**Features:** reasoning, tools, memory, +1 more
**Module:** `haive.agents.base.compiled_agent`

**ComplexExtractionAgent** (🔴 Complex)
_Document Processing | haive-agents_
Agent that extracts complex structured information from text.
**Features:** structured_output
**Module:** `haive.agents.document_modifiers.complex_extraction.agent`

**ComplexExtractionAgentConfig** (🔴 Complex)
_Document Processing | haive-agents_
Configuration for the complex extraction agent.
**Features:** tools, structured_output
**Module:** `haive.agents.document_modifiers.complex_extraction.config`

**CompositeGradingAgent** (🔴 Complex)
_RAG & Retrieval | haive-agents_
Combines multiple grading components for comprehensive evaluation
**Features:** Basic
**Module:** `haive.agents.rag.multi_agent_rag.grading_components`

**ConditionalAgent** (🔴 Complex)
_Multi-Agent Systems | haive-agents_
Pre-configured conditional multi-agent with branching.
**Features:** conversation
**Module:** `haive.agents.multi.base`

**ConditionalCallableAgent** (🟢 Simple)
_RAG & Retrieval | haive-agents_
Agent with conditional routing based on callable results.
**Features:** Basic
**Module:** `haive.agents.rag.factories.rag_workflow_factory`

**ConditionalRAGMultiAgent** (🔴 Complex)
_RAG & Retrieval | haive-agents_
Conditional multi-agent RAG system with smart routing based on document quality.
**Features:** retrieval, conversation
**Module:** `haive.agents.rag.multi_agent_rag.multi_rag`

**ConfigurableBattleshipConfig** (🟢 Simple)
_Games | haive-games_
Configurable Battleship configuration with dynamic LLM selection.
**Features:** Basic
**Module:** `haive.games.battleship.configurable_config`

**ConfigurableCheckersConfig** (🟢 Simple)
_Classic Games | haive-games_
Configurable Checkers configuration with dynamic LLM selection.
**Features:** Basic
**Module:** `haive.games.checkers.configurable_config`

**ConfigurableConnect4Config** (🟡 Medium)
_Games | haive-games_
Configurable Connect4 agent configuration.
**Features:** retrieval
**Module:** `haive.games.connect4.configurable_config`

**ConfigurableDebateConfig** (🟢 Simple)
_Games | haive-games_
Configurable Debate configuration with dynamic LLM selection.
**Features:** Basic
**Module:** `haive.games.debate.configurable_config`

**ConfigurableDominoesConfig** (🟢 Simple)
_Games | haive-games_
Configurable Dominoes configuration with dynamic LLM selection.
**Features:** Basic
**Module:** `haive.games.dominoes.configurable_config`

**ConfigurableGameAgent** (🟢 Simple)
_Games | haive-games_
Abstract base for game agents with configurable players.
**Features:** Basic
**Module:** `haive.games.core.agent.player_agent`

**ConfigurableHoldemConfig** (🟢 Simple)
_Games | haive-games_
Configurable Hold'em configuration with dynamic LLM selection.
**Features:** Basic
**Module:** `haive.games.hold_em.configurable_config`

**ConfigurableMonopolyConfig** (🟢 Simple)
_Games | haive-games_
Configurable Monopoly configuration with dynamic LLM selection.
**Features:** Basic
**Module:** `haive.games.monopoly.configurable_config`

**ConfigurablePokerConfig** (🟢 Simple)
_Classic Games | haive-games_
Configurable Poker configuration with dynamic LLM selection.
**Features:** Basic
**Module:** `haive.games.poker.configurable_config`

**Connect4Agent** (🟡 Medium)
_Games | haive-games_
Agent for playing Connect 4.
**Features:** Basic
**Module:** `haive.games.connect4.agent`

**Connect4AgentConfig** (🟢 Simple)
_Games | haive-games_
Configuration class for Connect4 game agents.
**Features:** Basic
**Module:** `haive.games.connect4.config`

**ContextualQueryDecomposerAgent** (🟢 Simple)
_RAG & Retrieval | haive-agents_
Context-aware query decomposition agent.
**Features:** Basic
**Module:** `haive.agents.rag.query_decomposition.agent`

**ContractAnalysisAgent** (🟢 Simple)
_Legal & Business | haive-prebuilt_
No description available
**Features:** Basic
**Module:** `haive.prebuilt.contract_analysis.agent`

**ContractAnalysisAgentConfig** (🟢 Simple)
_Legal & Business | haive-prebuilt_
No description available
**Features:** Basic
**Module:** `haive.prebuilt.contract_analysis.agent`

**CorrectiveRAGAgent** (🟢 Simple)
_RAG & Retrieval | haive-agents_
Full Corrective RAG implementation with web search fallback.
**Features:** retrieval
**Module:** `haive.agents.rag.multi_agent_rag.complete_rag_workflows`

**CorrectiveRAGAgent** (🟢 Simple)
_RAG & Retrieval | haive-agents_
Corrective RAG (CRAG) with automatic requerying and web search fallback.
**Features:** retrieval
**Module:** `haive.agents.rag.multi_agent_rag.enhanced_workflows`

**CorrectiveRAGAgent** (🟢 Simple)
_RAG & Retrieval | haive-agents_
Corrective RAG with self-correcting retrieval.
**Features:** retrieval
**Module:** `haive.agents.rag.corrective.agent`

**CorrectiveRAGAgentV2** (🟢 Simple)
_RAG & Retrieval | haive-agents_
Corrective RAG with proper self-correcting retrieval.
**Features:** retrieval
**Module:** `haive.agents.rag.corrective.agent_v2`

## D

**DebateAgent** (🔴 Complex)
_Games | haive-games_
Agent for facilitating debates and structured discussions.
**Features:** structured_output
**Module:** `haive.games.debate.agent`

**DebateAgentConfig** (🟢 Simple)
_Games | haive-games_
Configuration for debate agents.
**Features:** Basic
**Module:** `haive.games.debate.config`

**DebateConversation** (🔴 Complex)
_Conversation & Multi-Agent | haive-agents_
Structured debate conversation with positions and formal argumentation.
**Features:** structured_output, conversation
**Module:** `haive.agents.conversation.debate.agent`

**DebateRAGAgent** (🔴 Complex)
_RAG & Retrieval | haive-agents_
Debate RAG - multiple agents with different perspectives debate
**Features:** reasoning, retrieval
**Module:** `haive.agents.rag.multi_agent_rag.specialized_workflows`

**DebateRAGAgentV2** (🟢 Simple)
_RAG & Retrieval | haive-agents_
Debate RAG V2 - Configuration in DebateRAGState
**Features:** retrieval
**Module:** `haive.agents.rag.multi_agent_rag.specialized_workflows_v2`

**DefaultAgentInput** (🟢 Simple)
_Specialized Agents | haive-agents_
Default input schema for generic agents.
**Features:** structured_output
**Module:** `haive.agents.base.generic_agent`

**DefaultAgentOutput** (🟢 Simple)
_Specialized Agents | haive-agents_
Default output schema for generic agents.
**Features:** structured_output
**Module:** `haive.agents.base.generic_agent`

**DefaultAgentState** (🟢 Simple)
_Specialized Agents | haive-agents_
Default state schema for generic agents.
**Features:** structured_output
**Module:** `haive.agents.base.generic_agent`

**DirectedConversation** (🔴 Complex)
_Conversation & Multi-Agent | haive-agents_
Directed conversation where agents respond to mentions and questions.
**Features:** structured_output, conversation
**Module:** `haive.agents.conversation.directed.agent`

**DirectoryLoaderAgent** (🟢 Simple)
_Document Processing | haive-agents_
Specialized document loader agent for loading documents from directories.
**Features:** Basic
**Module:** `haive.agents.document_loader.directory.agent`

**DocumentAgent** (🟢 Simple)
_Specialized Agents | haive-agents_
No description available
**Features:** Basic
**Module:** `haive.agents.base`

**DocumentAgent** (🔴 Complex)
_Document Processing | haive-agents_
Comprehensive Document Processing Agent.
**Features:** planning, retrieval, memory, +1 more
**Module:** `haive.agents.document.agent`

**DocumentAgentConfig** (🟢 Simple)
_Specialized Agents | haive-agents_
The configuration for the document agent.
**Features:** Basic
**Module:** `haive.agents.base`

**DocumentGradingAgent** (🟢 Simple)
_RAG & Retrieval | haive-agents_
Agent that iterates over documents and grades each one.
**Features:** Basic
**Module:** `haive.agents.rag.document_grading.agent`

**DocumentGradingAgent** (🟢 Simple)
_RAG & Retrieval | haive-agents_
Agent that grades retrieved documents for relevance.
**Features:** Basic
**Module:** `haive.agents.rag.multi_agent_rag.enhanced_workflows`

**DocumentGradingAgent** (🟢 Simple)
_RAG & Retrieval | haive-agents_
Agent that grades retrieved documents for relevance.
**Features:** Basic
**Module:** `haive.agents.rag.multi_agent_rag.simple_enhanced_workflows`

**DocumentGradingAgent** (🟡 Medium)
_RAG & Retrieval | haive-agents_
Document grading agent that evaluates document relevance.
**Features:** Basic
**Module:** `haive.agents.rag.multi_agent_rag.agents`

**DocumentGradingRAGAgent** (🟢 Simple)
_RAG & Retrieval | haive-agents_
RAG with document grading and filtering.
**Features:** retrieval
**Module:** `haive.agents.rag.document_grading.agent`

**DocumentLoaderAgent** (🔴 Complex)
_Document Processing | haive-agents_
Document Loader Agent that integrates the document loader engine with the agent framework.
**Features:** retrieval, structured_output
**Module:** `haive.agents.document_loader.base.agent`

**DomainAnalysisAgent** (🔴 Complex)
_RAG & Retrieval | haive-agents_
Analyzes queries to determine relevant domains for multi-domain generation.
**Features:** Basic
**Module:** `haive.agents.rag.hyde.enhanced_agent_v2`

**DominoesAgent** (🔴 Complex)
_Games | haive-games_
Agent for playing dominoes.
**Features:** Basic
**Module:** `haive.games.dominoes.agent`

**DominoesAgentConfig** (🟢 Simple)
_Games | haive-games_
Configuration for the dominoes agent.
**Features:** Basic
**Module:** `haive.games.dominoes.config`

**DualRetrievalAgent** (🟢 Simple)
_RAG & Retrieval | haive-agents_
Agent that performs both original and step-back retrieval.
**Features:** retrieval
**Module:** `haive.agents.rag.step_back.agent`

**DynamicRAGAgent** (🔴 Complex)
_RAG & Retrieval | haive-agents_
Dynamic RAG with add/remove retrievers - adapts retrieval strategy
**Features:** planning, retrieval
**Module:** `haive.agents.rag.multi_agent_rag.specialized_workflows`

**DynamicRAGAgent** (🟡 Medium)
_RAG & Retrieval | haive-agents_
Implements a dynamic RAG pipeline that routes queries to appropriate data sources.
**Features:** retrieval
**Module:** `haive.agents.rag.dynamic.agent`

**DynamicRAGAgentV2** (🟢 Simple)
_RAG & Retrieval | haive-agents_
Dynamic RAG V2 - Configuration in DynamicRAGState
**Features:** retrieval
**Module:** `haive.agents.rag.multi_agent_rag.specialized_workflows_v2`

**DynamicReactAgent** (🟡 Medium)
_ReAct & Tool Use | haive-agents_
A React agent with dynamic tool selection.
**Features:** tools
**Module:** `haive.agents.react_class.react_agent2.dynamic_agent`

**DynamicReactAgentConfig** (🟢 Simple)
_ReAct & Tool Use | haive-agents_
Configuration for a React agent with dynamic tool selection.
**Features:** tools
**Module:** `haive.agents.react_class.react_agent2.dynamic_agent`

**DynamicReactAgentState** (🟢 Simple)
_ReAct & Tool Use | haive-agents_
Extended schema for dynamic tool selection.
**Features:** tools, structured_output
**Module:** `haive.agents.react_class.react_agent2.dynamic_agent`

## E

**EnhancedHyDERAGAgent** (🟢 Simple)
_RAG & Retrieval | haive-agents_
Enhanced HyDE RAG Agent using the structured output enhancement pattern.
**Features:** retrieval, tools, structured_output
**Module:** `haive.agents.rag.hyde.enhanced_agent`

**EnhancedHyDERAGAgentV2** (🔴 Complex)
_RAG & Retrieval | haive-agents_
Enhanced HyDE RAG Agent with advanced prompt selection and multi-document generation.
**Features:** retrieval
**Module:** `haive.agents.rag.hyde.enhanced_agent_v2`

**EnhancedHyDERetriever** (🟢 Simple)
_RAG & Retrieval | haive-agents_
Enhanced retriever that handles both enhancement pattern and traditional outputs.
**Features:** structured_output
**Module:** `haive.agents.rag.hyde.enhanced_agent`

**EnhancedHyDERetrieverV2** (🟢 Simple)
_RAG & Retrieval | haive-agents_
Enhanced retriever with better state handling and fallback mechanisms.
**Features:** Basic
**Module:** `haive.agents.rag.hyde.enhanced_agent_v2`

**EnhancedKYCAgent** (🔴 Complex)
_Academic & Research | haive-prebuilt_
Advanced KYC Agent with comprehensive risk assessment workflow
**Features:** Basic
**Module:** `haive.prebuilt.company_researcher.agent`

**EnhancedRAGConditionalAgent** (🟢 Simple)
_RAG & Retrieval | haive-agents_
RAG conditional agent with built-in compatibility checking and smart routing.
**Features:** retrieval
**Module:** `haive.agents.rag.multi_agent_rag.enhanced_multi_rag`

**EnhancedRAGParallelAgent** (🔴 Complex)
_RAG & Retrieval | haive-agents_
RAG parallel agent with built-in compatibility checking for consensus building.
**Features:** retrieval, structured_output
**Module:** `haive.agents.rag.multi_agent_rag.enhanced_multi_rag`

**EnhancedRAGSequentialAgent** (🟢 Simple)
_RAG & Retrieval | haive-agents_
RAG sequential agent with built-in compatibility checking.
**Features:** retrieval
**Module:** `haive.agents.rag.multi_agent_rag.enhanced_multi_rag`

**EnsembleDocumentParser** (🟢 Simple)
_RAG & Retrieval | haive-agents_
Parses ensemble document output into individual documents.
**Features:** structured_output
**Module:** `haive.agents.rag.hyde.enhanced_agent_v2`

**EnsembleHyDERetriever** (🔴 Complex)
_RAG & Retrieval | haive-agents_
Retriever that handles multiple documents for ensemble retrieval.
**Features:** retrieval
**Module:** `haive.agents.rag.hyde.enhanced_agent_v2`

**EssayGradingAgent** (🟢 Simple)
_Prebuilt Solutions | haive-prebuilt_
No description available
**Features:** Basic
**Module:** `haive.prebuilt.essay_grading.agent`

## F

**FLAREAgent** (🟢 Simple)
_RAG & Retrieval | haive-agents_
Forward-Looking Active REtrieval (FLARE) - generates text while actively
**Features:** retrieval
**Module:** `haive.agents.rag.multi_agent_rag.specialized_workflows`

**FLAREAgentV2** (🟢 Simple)
_RAG & Retrieval | haive-agents_
FLARE V2 - Configuration stored in FLAREState
**Features:** Basic
**Module:** `haive.agents.rag.multi_agent_rag.specialized_workflows_v2`

**FLAREAgentV2Example** (🟢 Simple)
_RAG & Retrieval | haive-agents_
FLARE Agent V2 example using enhanced state schema
**Features:** structured_output
**Module:** `haive.agents.rag.multi_agent_rag.graded_rag_workflows_v2`

**FLAREPlannerAgent** (🔴 Complex)
_RAG & Retrieval | haive-agents_
Agent that creates FLARE plans for iterative generation and active retrieval.
**Features:** planning, retrieval
**Module:** `haive.agents.rag.flare.agent`

**FLARERAGAgent** (🟢 Simple)
_RAG & Retrieval | haive-agents_
Complete FLARE RAG agent with forward-looking active retrieval.
**Features:** retrieval
**Module:** `haive.agents.rag.flare.agent`

**FileLoaderAgent** (🟢 Simple)
_Document Processing | haive-agents_
Specialized document loader agent for loading documents from files.
**Features:** Basic
**Module:** `haive.agents.document_loader.file.agent`

**FilteredRAGAgent** (🟡 Medium)
_RAG & Retrieval | haive-agents_
RAG agent with document filtering capabilities.
**Features:** retrieval
**Module:** `haive.agents.rag.filtered.agent`

**FixedFoxAndGeeseAgent** (🟢 Simple)
_Games | haive-games_
Fixed Fox and Geese agent that handles state directly.
**Features:** Basic
**Module:** `haive.games.fox_and_geese.fixed_runner`

**FlowFreeAgent** (🟡 Medium)
_Games | haive-games_
Agent for playing Flow Free puzzle game.
**Features:** Basic
**Module:** `haive.games.single_player.flow_free.agent`

**FoxAndGeeseAgent** (🔴 Complex)
_Games | haive-games_
Agent for playing Fox and Geese.
**Features:** Basic
**Module:** `haive.games.fox_and_geese.agent`

**FullyGradedRAGAgent** (🟢 Simple)
_RAG & Retrieval | haive-agents_
Fully Graded RAG - comprehensive grading at every step of the RAG pipeline.
**Features:** retrieval
**Module:** `haive.agents.rag.multi_agent_rag.graded_rag_workflows`

**FullyGradedRAGAgentV2** (🟢 Simple)
_RAG & Retrieval | haive-agents_
Fully Graded RAG V2 - Uses enhanced state schema with configuration support.
**Features:** retrieval, structured_output
**Module:** `haive.agents.rag.multi_agent_rag.graded_rag_workflows_v2`

## G

**GameAgent** (🔴 Complex)
_Games | haive-games_
Base game agent that implements common workflow patterns.
**Features:** tools
**Module:** `haive.games.base.agent`

**GameAgent** (🔴 Complex)
_Games | haive-games_
Base game agent that implements common workflow patterns.
**Features:** tools
**Module:** `haive.games.framework.base.agent`

**GameAgentConfig** (🟢 Simple)
_Games | haive-games_
Base configuration for game agents.
**Features:** Basic
**Module:** `haive.games.core.base.config`

**GameAgentFactory** (🟢 Simple)
_Games | haive-games_
Factory for creating game agents using a flexible, composable pattern.
**Features:** structured_output
**Module:** `haive.games.base.factory`

**GameAgentFactory** (🟢 Simple)
_Games | haive-games_
Factory for creating game agents using a flexible, composable pattern.
**Features:** structured_output
**Module:** `haive.games.framework.base.factory`

**GameConfig** (🟢 Simple)
_Games | haive-games_
Base configuration for game agents.
**Features:** structured_output
**Module:** `haive.games.base.config`

**GameConfig** (🟢 Simple)
_Games | haive-games_
Base configuration for game agents.
**Features:** structured_output
**Module:** `haive.games.framework.base.config`

**GenericAgent** (🔴 Complex)
_Specialized Agents | haive-agents_
Generic agent base class with enhanced typing and auto-configuration.
**Features:** structured_output
**Module:** `haive.agents.base.generic_agent`

**GenericCallableAgent** (🟢 Simple)
_RAG & Retrieval | haive-agents_
Generic agent that executes a sequence of callable functions.
**Features:** tools
**Module:** `haive.agents.rag.factories.rag_workflow_factory`

**GoAgent** (🔴 Complex)
_Classic Games | haive-games_
Go game agent implementation.
**Features:** tools
**Module:** `haive.games.go.agent`

**GoAgentConfig** (🟢 Simple)
_Classic Games | haive-games_
Configuration for the Go game agent.
**Features:** structured_output
**Module:** `haive.games.go.config`

**GraphDBRAGAgent** (🔴 Complex)
_RAG & Retrieval | haive-agents_
Graph Database RAG Agent for natural language querying of Neo4j databases.
**Features:** retrieval, tools, structured_output
**Module:** `haive.agents.rag.db_rag.graph_db.agent`

**GraphDBRAGConfig** (🟢 Simple)
_RAG & Retrieval | haive-agents_
Main configuration for the Graph Database RAG Agent.
**Features:** retrieval, structured_output
**Module:** `haive.agents.rag.db_rag.graph_db.config`

**GraphRAGAgent** (🔴 Complex)
_RAG & Retrieval | haive-agents_
Graph RAG - uses knowledge graph construction and traversal
**Features:** reasoning, retrieval
**Module:** `haive.agents.rag.multi_agent_rag.advanced_workflows`

## H

**HYDERAGAgent** (🟢 Simple)
_RAG & Retrieval | haive-agents_
Enhanced HYDE RAG with hypothesis generation.
**Features:** retrieval
**Module:** `haive.agents.rag.multi_agent_rag.complete_rag_workflows`

**HYDERAGAgent** (🟢 Simple)
_RAG & Retrieval | haive-agents_
HYDE RAG agent that generates hypothetical documents before retrieval.
**Features:** retrieval
**Module:** `haive.agents.rag.multi_agent_rag.enhanced_workflows`

**HallucinationGraderAgent** (🟢 Simple)
_RAG & Retrieval | haive-agents_
Basic hallucination grading agent.
**Features:** Basic
**Module:** `haive.agents.rag.hallucination_grading.agent`

**HierarchicalQueryDecomposerAgent** (🟢 Simple)
_RAG & Retrieval | haive-agents_
Hierarchical query decomposition agent.
**Features:** Basic
**Module:** `haive.agents.rag.query_decomposition.agent`

**HoldemGameAgent** (🔴 Complex)
_Games | haive-games_
Main Texas Hold'em game agent that coordinates the complete poker game.
**Features:** Basic
**Module:** `haive.games.hold_em.game_agent`

**HoldemGameAgentConfig** (🟢 Simple)
_Games | haive-games_
Configuration for the main Hold'em game agent.
**Features:** tools
**Module:** `haive.games.hold_em.game_agent`

**HoldemPlayerAgent** (🔴 Complex)
_Games | haive-games_
Player agent for Texas Hold'em poker games.
**Features:** planning
**Module:** `haive.games.hold_em.player_agent`

**HoldemPlayerAgentConfig** (🟢 Simple)
_Games | haive-games_
Configuration for Hold'em player agent.
**Features:** Basic
**Module:** `haive.games.hold_em.player_agent`

**HyDEAgentConfig** (🟢 Simple)
_RAG & Retrieval | haive-agents_
Configuration for Enhanced HyDE RAG Agent.
**Features:** retrieval
**Module:** `haive.agents.rag.hyde.enhanced_agent_v2`

**HyDEDocumentAnalyzer** (🟢 Simple)
_RAG & Retrieval | haive-agents_
Analyzes generated hypothetical documents and extracts structured information.
**Features:** structured_output
**Module:** `haive.agents.rag.hyde.enhanced_agent_v2`

**HyDERAGAgentV2** (🟢 Simple)
_RAG & Retrieval | haive-agents_
HyDE RAG using hypothetical document generation for better retrieval.
**Features:** retrieval
**Module:** `haive.agents.rag.hyde.agent_v2`

**HyDERetrieverAgent** (🟢 Simple)
_RAG & Retrieval | haive-agents_
Custom retriever that uses hypothetical document for enhanced retrieval.
**Features:** retrieval
**Module:** `haive.agents.rag.hyde.agent_v2`

**HypothesisGeneratorAgent** (🔴 Complex)
_RAG & Retrieval | haive-agents_
Agent that generates multiple hypotheses for speculative reasoning.
**Features:** reasoning
**Module:** `haive.agents.rag.speculative.agent`

## I

**InterviewAgent** (🟢 Simple)
_Specialized Agents | haive-agents_
An agent that conducts an interview with a Subject Matter Expert.
**Features:** Basic
**Module:** `haive.agents.wiki_writer.interview.agent`

**InterviewAgentConfig** (🟢 Simple)
_Specialized Agents | haive-agents_
Configuration for the Interview Agent.
**Features:** Basic
**Module:** `haive.agents.wiki_writer.interview.agent`

**IterativeDocumentGradingAgent** (🟢 Simple)
_RAG & Retrieval | haive-agents_
Specialized grading agent that processes documents one by one.
**Features:** Basic
**Module:** `haive.agents.rag.multi_agent_rag.agents`

**IterativeGraphTransformer** (🟢 Simple)
_Document Processing | haive-agents_
An agent that transforms a graph document iteratively.
**Features:** Basic
**Module:** `haive.agents.document_modifiers.kg.kg_iterative_refinement.agent`

**IterativeGraphTransformerConfig** (🟢 Simple)
_Document Processing | haive-agents_
The configuration for the iterative graph transformer.
**Features:** Basic
**Module:** `haive.agents.document_modifiers.kg.kg_iterative_refinement.config`

**IterativePlannerAgent** (🔴 Complex)
_RAG & Retrieval | haive-agents_
Agent that creates iterative processing plans.
**Features:** planning
**Module:** `haive.agents.rag.self_route.agent`

**IterativeRAGMultiAgent** (🔴 Complex)
_RAG & Retrieval | haive-agents_
Multi-agent RAG system with iterative document processing.
**Features:** retrieval, conversation
**Module:** `haive.agents.rag.multi_agent_rag.multi_rag`

**IterativeSummarizer** (🟢 Simple)
_Document Processing | haive-agents_
An agent that summarizes a document iteratively.
**Features:** Basic
**Module:** `haive.agents.document_modifiers.summarizer.iterative_refinement.agent`

**IterativeSummarizerConfig** (🟢 Simple)
_Document Processing | haive-agents_
The configuration for the iterative summarizer.
**Features:** Basic
**Module:** `haive.agents.document_modifiers.summarizer.iterative_refinement.config`

## K

**KYCAgentConfiguration** (🔴 Complex)
_Academic & Research | haive-prebuilt_
Advanced configuration for KYC Agent with granular control
**Features:** Basic
**Module:** `haive.prebuilt.company_researcher.config`

## L

**LATSAgent** (🔴 Complex)
_Reasoning & Critique | haive-agents_
A Look-Ahead Tree Search (LATS) agent that uses tree search to
**Features:** reasoning, retrieval
**Module:** `haive.agents.reasoning_and_critique.lats.agent`

**LATSAgentConfig** (🟢 Simple)
_Reasoning & Critique | haive-agents_
Configuration for Language Agent Tree Search (LATS) agent.
**Features:** retrieval, tools
**Module:** `haive.agents.reasoning_and_critique.lats.config`

**LATSAgentConfig** (🔴 Complex)
_Reasoning & Critique | haive-agents_
Configuration for a Look-Ahead Tree Search (LATS) agent.
**Features:** reasoning, retrieval, tools
**Module:** `haive.agents.reasoning_and_critique.lats.agent`

**LLMCompilerAgent** (🔴 Complex)
_Planning & Strategy | haive-agents_
LLM Compiler Agent implementation.
**Features:** planning, structured_output
**Module:** `haive.agents.planning.llm_compiler.agent`

**LLMCompilerAgentConfig** (🟢 Simple)
_Planning & Strategy | haive-agents_
Configuration for the LLM Compiler Agent using AugLLMConfig system.
**Features:** tools
**Module:** `haive.agents.planning.llm_compiler.config`

**LLMRAGAgent** (🟢 Simple)
_RAG & Retrieval | haive-agents_
LLM-enhanced RAG agent that retrieves documents and generates answers.
**Features:** retrieval
**Module:** `haive.agents.rag.llm_rag.agent`

**LTMAgent** (🔴 Complex)
_Specialized Agents | haive-agents_
Long-Term Memory Agent with LangMem integration.
**Features:** retrieval, tools, reasoning, +2 more
**Module:** `haive.agents.ltm.agent`

**LongTermMemoryAgent** (🟢 Simple)
_Memory & Persistence | haive-agents_
Agent for the long term memory.
**Features:** memory
**Module:** `haive.agents.long_term_memory.agent`

**LongTermMemoryAgentConfig** (🟢 Simple)
_Memory & Persistence | haive-agents_
Config for the long term memory agent.
**Features:** memory
**Module:** `haive.agents.long_term_memory.agent`

**LongTermMemoryState** (🟢 Simple)
_Memory & Persistence | haive-agents_
State for the long term memory agent.
**Features:** memory
**Module:** `haive.agents.long_term_memory.state`

## M

**MCTSAgent** (🟢 Simple)
_Reasoning & Critique | haive-agents_
Monte Carlo Tree Search Agent implementation.
**Features:** retrieval
**Module:** `haive.agents.reasoning_and_critique.mcts.agent`

**MCTSAgentConfig** (🟢 Simple)
_Reasoning & Critique | haive-agents_
Configuration for MCTS Agent.
**Features:** tools
**Module:** `haive.agents.reasoning_and_critique.mcts.config`

**MafiaAgent** (🔴 Complex)
_Strategy Games | haive-games_
Agent for playing Mafia.
**Features:** Basic
**Module:** `haive.games.mafia.agent`

**MafiaAgentConfig** (🔴 Complex)
_Strategy Games | haive-games_
Configuration for the Mafia game agent.
**Features:** structured_output
**Module:** `haive.games.mafia.config`

**MancalaAgent** (🔴 Complex)
_Games | haive-games_
Agent for playing Mancala.
**Features:** Basic
**Module:** `haive.games.mancala.agent`

**MastermindAgent** (🔴 Complex)
_Games | haive-games_
Agent for playing Mastermind.
**Features:** Basic
**Module:** `haive.games.mastermind.agent`

**MemoryAgent** (🔴 Complex)
_Memory & Persistence | haive-agents_
Memory Agent implementation that extends ReactAgent.
**Features:** memory, conversation
**Module:** `haive.agents.memory.agent`

**MemoryAgentState** (🟢 Simple)
_Memory & Persistence | haive-agents_
State for Memory Agent, extending ReactAgentState.
**Features:** memory
**Module:** `haive.agents.memory.state`

**MemoryAwareRAGAgent** (🟢 Simple)
_RAG & Retrieval | haive-agents_
Complete Memory-Aware RAG agent with persistent learning.
**Features:** retrieval, memory
**Module:** `haive.agents.rag.memory_aware.agent`

**MemoryRetrievalAgent** (🟢 Simple)
_RAG & Retrieval | haive-agents_
Agent that retrieves relevant memories for context enhancement.
**Features:** Basic
**Module:** `haive.agents.rag.memory_aware.agent`

**MonopolyGameAgent** (🔴 Complex)
_Games | haive-games_
Main game agent for orchestrating Monopoly.
**Features:** Basic
**Module:** `haive.games.monopoly.game_agent`

**MonopolyGameAgentConfig** (🟢 Simple)
_Games | haive-games_
Configuration class for monopoly game agents.
**Features:** structured_output
**Module:** `haive.games.monopoly.player_agent`

**MonopolyGameAgentConfig** (🟢 Simple)
_Games | haive-games_
Configuration class for monopoly game agents.
**Features:** structured_output
**Module:** `haive.games.monopoly.config`

**MonopolyGameAgentConfig** (🟢 Simple)
_Games | haive-games_
Configuration for monopoly game agent.
**Features:** Basic
**Module:** `haive.games.monopoly.game_agent`

**MonopolyPlayerAgent** (🟡 Medium)
_Games | haive-games_
Player agent for making individual decisions in Monopoly.
**Features:** Basic
**Module:** `haive.games.monopoly.player_agent`

**MonopolyPlayerAgentConfig** (🟢 Simple)
_Games | haive-games_
Configuration for monopoly player decision agent.
**Features:** Basic
**Module:** `haive.games.monopoly.player_agent`

**MonopolyPlayerAgentConfig** (🟢 Simple)
_Games | haive-games_
Configuration for monopoly player decision agent.
**Features:** Basic
**Module:** `haive.games.monopoly.config`

**MultiAgent** (🔴 Complex)
_Multi-Agent Systems | haive-agents_
Abstract base class for sophisticated multi-agent systems.
**Features:** retrieval, tools, structured_output, +2 more
**Module:** `haive.agents.multi.base`

**MultiAgent** (🔴 Complex)
_Multi-Agent Systems | haive-agents_
Abstract base class for multi-agent systems.
**Features:** conversation
**Module:** `haive.agents.multi.multi_agent_base (1)`

**MultiAgent** (🔴 Complex)
_Multi-Agent Systems | haive-agents_
Advanced multi-agent system with flexible coordination patterns.
**Features:** retrieval, structured_output, conversation
**Module:** `haive.agents.multi.agent`

**MultiAgentCompatibilityReport** (🔴 Complex)
_RAG & Retrieval | haive-agents_
Compatibility report for multiple agents in a workflow.
**Features:** Basic
**Module:** `haive.agents.rag.multi_agent_rag.compatibility`

**MultiAgentRAGState** (🔴 Complex)
_RAG & Retrieval | haive-agents_
Comprehensive state schema for multi-agent RAG systems.
**Features:** retrieval, structured_output, conversation
**Module:** `haive.agents.rag.multi_agent_rag.state`

**MultiCriteriaGradedRAGAgent** (🔴 Complex)
_RAG & Retrieval | haive-agents_
Multi-Criteria Graded RAG - uses multiple grading criteria and perspectives
**Features:** retrieval
**Module:** `haive.agents.rag.multi_agent_rag.graded_rag_workflows`

**MultiCriteriaGradedRAGAgentV2** (🔴 Complex)
_RAG & Retrieval | haive-agents_
Multi-Criteria Graded RAG V2 - Configuration stored in state schema.
**Features:** retrieval, structured_output
**Module:** `haive.agents.rag.multi_agent_rag.graded_rag_workflows_v2`

**MultiDomainHyDERetriever** (🔴 Complex)
_RAG & Retrieval | haive-agents_
Retriever that handles documents from multiple domains.
**Features:** Basic
**Module:** `haive.agents.rag.hyde.enhanced_agent_v2`

**MultiPlayerGameAgent** (🔴 Complex)
_Games | haive-games_
Base game agent for multi-player games.
**Features:** tools, structured_output
**Module:** `haive.games.multi_player.agent`

**MultiPlayerGameAgent** (🔴 Complex)
_Games | haive-games_
Base game agent for multi-player games.
**Features:** tools, structured_output
**Module:** `haive.games.framework.multi_player.agent`

**MultiPlayerGameConfig** (🔴 Complex)
_Games | haive-games_
Configuration for multi-player game agents.
**Features:** structured_output
**Module:** `haive.games.multi_player.config`

**MultiPlayerGameConfig** (🔴 Complex)
_Games | haive-games_
Configuration for multi-player game agents.
**Features:** structured_output
**Module:** `haive.games.framework.multi_player.config`

**MultiQueryRAGAgent** (🔴 Complex)
_RAG & Retrieval | haive-agents_
Multi-Query RAG - generates multiple diverse queries and retrieves documents
**Features:** retrieval
**Module:** `haive.agents.rag.multi_agent_rag.additional_workflows`

**MultiQueryRAGAgent** (🔴 Complex)
_RAG & Retrieval | haive-agents_
Multi-Query RAG with query expansion for improved recall.
**Features:** retrieval
**Module:** `haive.agents.rag.multi_query.agent`

**MultiQueryRetrievalAgent** (🔴 Complex)
_RAG & Retrieval | haive-agents_
Agent that uses a callable node for multi-query retrieval - proper Pydantic approach.
**Features:** retrieval, structured_output
**Module:** `haive.agents.rag.fusion.agent`

**MultiRetrievalAgent** (🔴 Complex)
_RAG & Retrieval | haive-agents_
Agent that performs parallel retrieval with multiple queries.
**Features:** retrieval
**Module:** `haive.agents.rag.multi_query.agent`

**MultiStrategyRAGAgent** (🔴 Complex)
_RAG & Retrieval | haive-agents_
RAG agent with multiple retrieval strategies.
**Features:** retrieval
**Module:** `haive.agents.rag.multi_strategy.agent`

## N

**NimAgent** (🔴 Complex)
_Games | haive-games_
Agent for playing Nim.
**Features:** Basic
**Module:** `haive.games.nim.agent`

## P

**ParallelAgent** (🔴 Complex)
_Multi-Agent Systems | haive-agents_
Pre-configured parallel multi-agent.
**Features:** conversation
**Module:** `haive.agents.multi.base`

**ParallelKGTransformer** (🔴 Complex)
_Document Processing | haive-agents_
An agent that builds a knowledge graph by extracting
**Features:** retrieval
**Module:** `haive.agents.document_modifiers.kg.kg_map_merge.agent`

**ParallelKGTransformerConfig** (🟢 Simple)
_Document Processing | haive-agents_
Configuration for the Parallel Knowledge Graph Transformer.
**Features:** retrieval
**Module:** `haive.agents.document_modifiers.kg.kg_map_merge.config`

**ParallelKGTransformerConfig** (🟢 Simple)
_Document Processing | haive-agents_
Configuration for the Parallel Knowledge Graph Transformer.
**Features:** retrieval
**Module:** `haive.agents.document_modifiers.kg.kg_map_merge.agent`

**ParallelRAGMultiAgent** (🔴 Complex)
_RAG & Retrieval | haive-agents_
Parallel multi-agent RAG system for consensus-based processing.
**Features:** retrieval, conversation
**Module:** `haive.agents.rag.multi_agent_rag.multi_rag`

**ParallelVerificationAgent** (🟢 Simple)
_RAG & Retrieval | haive-agents_
Agent that performs parallel hypothesis verification.
**Features:** Basic
**Module:** `haive.agents.rag.speculative.agent`

**PersonResearchAgent** (🔴 Complex)
_Research & Information | haive-agents_
Advanced person research agent with iterative information gathering capabilities.
**Features:** reasoning, retrieval, structured_output
**Module:** `haive.agents.research.person.agent`

**PersonResearchAgentConfig** (🟢 Simple)
_Research & Information | haive-agents_
Configuration settings for person research agent.
**Features:** retrieval
**Module:** `haive.agents.research.person.state`

**PersonResearchAgentConfig** (🟢 Simple)
_Research & Information | haive-agents_
Configuration for the Person Research Agent.
**Features:** retrieval
**Module:** `haive.agents.research.person.config`

**PlanAndExecuteAgent** (🟢 Simple)
_Planning & Strategy | haive-agents_
No description available
**Features:** Basic
**Module:** `haive.agents.planning.plan_and_execute.agent`

**PlanAndExecuteConfig** (🟢 Simple)
_Planning & Strategy | haive-agents_
No description available
**Features:** Basic
**Module:** `haive.agents.planning.plan_and_execute.config`

**PlayerAgentConfig** (🟢 Simple)
_Games | haive-games_
Configuration for a player agent.
**Features:** Basic
**Module:** `haive.games.core.agent.player_agent`

**PlayerAgentFactory** (🟢 Simple)
_Games | haive-games_
Factory for creating configurable player agents.
**Features:** Basic
**Module:** `haive.games.core.agent.player_agent`

**PodcastGeneratorAgent** (🟢 Simple)
_Prebuilt Solutions | haive-prebuilt_
No description available
**Features:** Basic
**Module:** `haive.prebuilt.podcast_generator.agent`

**PokerAgent** (🔴 Complex)
_Classic Games | haive-games_
Enhanced agent class for managing a multi-player Texas Hold'em poker game.
**Features:** structured_output
**Module:** `haive.games.poker.agent`

**PokerAgentConfig** (🟢 Simple)
_Classic Games | haive-games_
Configuration class for the poker agent.
**Features:** retrieval, memory, structured_output
**Module:** `haive.games.poker.config`

**ProjectManagerAgent** (🟡 Medium)
_Prebuilt Solutions | haive-prebuilt_
No description available
**Features:** Basic
**Module:** `haive.prebuilt.project_manager.agent`

**ProjectManagerAgentConfig** (🟢 Simple)
_Prebuilt Solutions | haive-prebuilt_
No description available
**Features:** Basic
**Module:** `haive.prebuilt.project_manager.agent`

## Q

**QueryAnalysisAgent** (🟢 Simple)
_RAG & Retrieval | haive-agents_
Agent that analyzes queries and selects appropriate prompt types.
**Features:** Basic
**Module:** `haive.agents.rag.hyde.enhanced_agent_v2`

**QueryAnalyzerAgent** (🟢 Simple)
_RAG & Retrieval | haive-agents_
Agent that performs structured query analysis for routing.
**Features:** structured_output
**Module:** `haive.agents.rag.self_route.agent`

**QueryDecomposerAgent** (🟢 Simple)
_RAG & Retrieval | haive-agents_
Basic query decomposition agent.
**Features:** Basic
**Module:** `haive.agents.rag.query_decomposition.agent`

**QueryDecompositionRAGAgent** (🔴 Complex)
_RAG & Retrieval | haive-agents_
Query Decomposition RAG - breaks complex queries into simpler sub-questions,
**Features:** retrieval
**Module:** `haive.agents.rag.multi_agent_rag.additional_workflows`

**QueryPlanningAgenticRAGAgent** (🔴 Complex)
_RAG & Retrieval | haive-agents_
Query Planning Agentic RAG - creates detailed execution plans
**Features:** reasoning, planning, retrieval
**Module:** `haive.agents.rag.multi_agent_rag.advanced_workflows`

**QueryPlanningRAGAgent** (🔴 Complex)
_RAG & Retrieval | haive-agents_
Query Planning RAG agent with structured decomposition and execution.
**Features:** planning, retrieval, structured_output
**Module:** `haive.agents.rag.query_planning.agent`

## R

**RAGFusionAgent** (🟢 Simple)
_RAG & Retrieval | haive-agents_
Complete RAG Fusion agent with query expansion and RRF.
**Features:** retrieval
**Module:** `haive.agents.rag.fusion.agent`

**RAGFusionAgent** (🔴 Complex)
_RAG & Retrieval | haive-agents_
RAG Fusion - combines multiple retrieval strategies and fuses results
**Features:** retrieval
**Module:** `haive.agents.rag.multi_agent_rag.additional_workflows`

**ReactAgent** (🟢 Simple)
_ReAct & Tool Use | haive-agents_
ReAct agent with looping behavior.
**Features:** Basic
**Module:** `haive.agents.react.agent`

**ReactAgent** (🔴 Complex)
_ReAct & Tool Use | haive-agents_
A tool-using agent implementing the ReAct pattern.
**Features:** reasoning, tools, structured_output
**Module:** `haive.agents.react_class.react_v3.agent`

**ReactAgent** (🟢 Simple)
_ReAct & Tool Use | haive-agents_
ReAct agent implementation with tool usage and routing capabilities.
**Features:** tools
**Module:** `haive.agents.react_class.react_agent2.agent3`

**ReactAgent** (🔴 Complex)
_ReAct & Tool Use | haive-agents_
A React agent implementing the Reasoning-Action-Observation pattern.
**Features:** reasoning, tools, structured_output
**Module:** `haive.agents.react_class.react_agent2.agent`

**ReactAgent** (🔴 Complex)
_ReAct & Tool Use | haive-agents_
A React agent implementation using LangGraph.
**Features:** reasoning, tools
**Module:** `haive.agents.react_class.react_agent2.agent2`

**ReactAgent** (🔴 Complex)
_ReAct & Tool Use | haive-agents_
React Agent implementation that extends SimpleAgent.
**Features:** reasoning, tools
**Module:** `haive.agents.react_class.react.agent`

**ReactAgent** (🟡 Medium)
_ReAct & Tool Use | haive-agents_
No description available
**Features:** Basic
**Module:** `haive.agents.react_class.react_agent.agent`

**ReactAgent** (🔴 Complex)
_ReAct & Tool Use | haive-agents_
A React agent that enhances SimpleAgent with tool-using capabilities.
**Features:** reasoning, tools
**Module:** `haive.agents.react_class.react_v2.agent`

**ReactAgentConfig** (🟢 Simple)
_ReAct & Tool Use | haive-agents_
Configuration for the React Agent.
**Features:** tools
**Module:** `haive.agents.react.config`

**ReactAgentConfig** (🔴 Complex)
_ReAct & Tool Use | haive-agents_
Configuration for a ReAct agent with tool integration.
**Features:** reasoning, tools
**Module:** `haive.agents.react_class.react_v3.config`

**ReactAgentConfig** (🟢 Simple)
_ReAct & Tool Use | haive-agents_
Configuration for the ReAct agent.
**Features:** tools
**Module:** `haive.agents.react_class.react_agent2.agent3`

**ReactAgentConfig** (🟢 Simple)
_ReAct & Tool Use | haive-agents_
Configuration for a React agent that follows the ReAct pattern:
**Features:** tools
**Module:** `haive.agents.react_class.react_agent2.config`

**ReactAgentConfig** (🔴 Complex)
_ReAct & Tool Use | haive-agents_
Configuration for a React agent that can use tools.
**Features:** reasoning, tools, memory
**Module:** `haive.agents.react_class.react_agent2.config2`

**ReactAgentConfig** (🔴 Complex)
_ReAct & Tool Use | haive-agents_
Configuration for a React agent, extending SimpleAgentConfig.
**Features:** reasoning, tools
**Module:** `haive.agents.react_class.react_agent2.agent`

**ReactAgentConfig** (🔴 Complex)
_ReAct & Tool Use | haive-agents_
Configuration for React Agent, extending SimpleAgentConfig.
**Features:** reasoning, tools
**Module:** `haive.agents.react_class.react.config`

**ReactAgentConfig** (🟢 Simple)
_ReAct & Tool Use | haive-agents_
No description available
**Features:** tools
**Module:** `haive.agents.react_class.react_agent.agent`

**ReactAgentConfig** (🔴 Complex)
_ReAct & Tool Use | haive-agents_
Configuration for a React agent that can use tools and follow ReAct reasoning pattern.
**Features:** reasoning, tools
**Module:** `haive.agents.react_class.react_v2.config`

**ReactAgentSchema** (🟢 Simple)
_ReAct & Tool Use | haive-agents_
Schema for React Agent State, extending SimpleAgentSchema.
**Features:** tools, structured_output
**Module:** `haive.agents.react_class.react_agent2.agent`

**ReactAgentSchemaWithStructuredResponse** (🟢 Simple)
_ReAct & Tool Use | haive-agents_
Schema for React Agent with structured response.
**Features:** structured_output
**Module:** `haive.agents.react_class.react_agent2.agent`

**ReactAgentState** (🟢 Simple)
_ReAct & Tool Use | haive-agents_
State schema for ReAct agent.
**Features:** tools, structured_output
**Module:** `haive.agents.react_class.react_agent2.agent3`

**ReactAgentState** (🟡 Medium)
_ReAct & Tool Use | haive-agents_
State for React agents with tool usage.
**Features:** memory, tools, structured_output
**Module:** `haive.agents.react_class.react_agent2.state2`

**ReactAgentState** (🔴 Complex)
_ReAct & Tool Use | haive-agents_
State for React Agent, extending SimpleAgentState.
**Features:** reasoning, tools, structured_output
**Module:** `haive.agents.react_class.react.state`

**ReactAgentState** (🟢 Simple)
_ReAct & Tool Use | haive-agents_
The state of the agent.
**Features:** Basic
**Module:** `haive.agents.react_class.react_agent.state`

**ReactAgentState** (🟢 Simple)
_ReAct & Tool Use | haive-agents_
State schema for React agent.
**Features:** tools, structured_output
**Module:** `haive.agents.react_class.react_v2.state`

**ReactManyToolsAgent** (🔴 Complex)
_ReAct & Tool Use | haive-agents_
React Agent implementation that can handle many tools efficiently.
**Features:** retrieval, tools
**Module:** `haive.agents.react_class.react_many_tools.agent`

**ReactManyToolsConfig** (🟢 Simple)
_ReAct & Tool Use | haive-agents_
Configuration for React Agent with many tools.
**Features:** retrieval, tools
**Module:** `haive.agents.react_class.react_many_tools.config`

**ReactManyToolsState** (🟢 Simple)
_ReAct & Tool Use | haive-agents_
State for React Agent with many tools.
**Features:** retrieval, tools
**Module:** `haive.agents.react_class.react_many_tools.state`

**RealtimeHallucinationGraderAgent** (🟢 Simple)
_RAG & Retrieval | haive-agents_
Fast hallucination checker for real-time applications.
**Features:** Basic
**Module:** `haive.agents.rag.hallucination_grading.agent`

**ReasoningSystem** (🔴 Complex)
_Reasoning & Critique | haive-agents_
Orchestrator agent for comprehensive reasoning analysis.
**Features:** reasoning
**Module:** `haive.agents.reasoning_and_critique.logic.agent`

**ReciprocalRankFusionAgent** (🔴 Complex)
_RAG & Retrieval | haive-agents_
Agent that performs reciprocal rank fusion on multiple retrieval results.
**Features:** retrieval
**Module:** `haive.agents.rag.fusion.agent`

**ReflectionAgent** (🔴 Complex)
_Reasoning & Critique | haive-agents_
An agent with self-reflection capabilities that can improve its responses.
**Features:** reasoning
**Module:** `haive.agents.reasoning_and_critique.reflection.agent`

**ReflectionAgentConfig** (🔴 Complex)
_Reasoning & Critique | haive-agents_
Configuration for an agent that uses reflection to improve responses.
**Features:** reasoning
**Module:** `haive.agents.reasoning_and_critique.reflection.config`

**ReflectionAgentState** (🔴 Complex)
_Reasoning & Critique | haive-agents_
State schema for the Reflection agent.
**Features:** reasoning, structured_output
**Module:** `haive.agents.reasoning_and_critique.reflection.state`

**ReflexionAgent** (🟢 Simple)
_Reasoning & Critique | haive-agents_
Agent that uses Reflexion to answer questions.
**Features:** Basic
**Module:** `haive.agents.reasoning_and_critique.reflexion.agent`

**ReflexionConfig** (🟢 Simple)
_Reasoning & Critique | haive-agents_
Configuration for the Reflexion agent.
**Features:** tools
**Module:** `haive.agents.reasoning_and_critique.reflexion.config`

**ReflexionState** (🟢 Simple)
_Reasoning & Critique | haive-agents_
State for the Reflexion agent.
**Features:** Basic
**Module:** `haive.agents.reasoning_and_critique.reflexion.state`

**ReflexiveGradedRAGAgent** (🔴 Complex)
_RAG & Retrieval | haive-agents_
Reflexive Graded RAG - uses grading feedback to improve its own performance
**Features:** reasoning, planning, retrieval
**Module:** `haive.agents.rag.multi_agent_rag.graded_rag_workflows`

**RequeryDecisionAgent** (🟢 Simple)
_RAG & Retrieval | haive-agents_
Agent that decides if requerying is needed based on document grades.
**Features:** Basic
**Module:** `haive.agents.rag.multi_agent_rag.enhanced_workflows`

**RequeryDecisionAgent** (🟢 Simple)
_RAG & Retrieval | haive-agents_
Agent that decides if requerying is needed based on document grades.
**Features:** Basic
**Module:** `haive.agents.rag.multi_agent_rag.simple_enhanced_workflows`

**ResearchAgent** (🔴 Complex)
_Research & Information | haive-agents_
Agent for performing deep research on any topic with dynamic document loader selection
**Features:** retrieval
**Module:** `haive.agents.research.open_perplexity.agent`

**ResearchAgentConfig** (🟢 Simple)
_Research & Information | haive-agents_
Configuration for open_perplexity research agent.
**Features:** retrieval, tools, structured_output
**Module:** `haive.agents.research.open_perplexity.config`

**ReversiAgent** (🔴 Complex)
_Games | haive-games_
Agent for playing Reversi/Othello.
**Features:** Basic
**Module:** `haive.games.reversi.agent`

**RewooAgent** (🔴 Complex)
_Planning & Strategy | haive-agents_
ReWOO (Reasoning Without Observation) Agent implementation.
**Features:** reasoning, planning, tools, +1 more
**Module:** `haive.agents.planning.rewoo.agent`

**RewooAgentConfig** (🔴 Complex)
_Planning & Strategy | haive-agents_
Configuration for the ReWOO Agent with automatic prompt formatting.
**Features:** planning, tools
**Module:** `haive.agents.planning.rewoo.agent`

**RiskAgent** (🔴 Complex)
_Strategy Games | haive-games_
Agent for playing the Risk game.
**Features:** reasoning, planning, memory
**Module:** `haive.games.risk.agent`

**RoundRobinConversation** (🔴 Complex)
_Conversation & Multi-Agent | haive-agents_
Round-robin conversation where each agent speaks in a fixed order.
**Features:** conversation
**Module:** `haive.agents.conversation.round_robin.agent`

**RoutingAgent** (🟢 Simple)
_Specialized Agents | haive-agents_
Simple agent with conditional routing capabilities.
**Features:** Basic
**Module:** `haive.agents.routing_agent`

**RoutingAgentConfig** (🟢 Simple)
_Specialized Agents | haive-agents_
Configuration for a routing agent.
**Features:** Basic
**Module:** `haive.agents.routing_agent`

**RoutingAgentSchema** (🟢 Simple)
_Specialized Agents | haive-agents_
Schema for routing agents.
**Features:** structured_output
**Module:** `haive.agents.routing_agent`

**RoutingDecisionAgent** (🟢 Simple)
_RAG & Retrieval | haive-agents_
Agent that makes final routing decisions.
**Features:** Basic
**Module:** `haive.agents.rag.self_route.agent`

**RubiksCubeAgent** (🟡 Medium)
_Games | haive-games_
Rubik's Cube game agent.
**Features:** Basic
**Module:** `haive.games.single_player.rubiks.agent`

## S

**SQLRAGAgent** (🔴 Complex)
_RAG & Retrieval | haive-agents_
SQL RAG Agent for querying SQL databases with natural language.
**Features:** retrieval, tools, structured_output
**Module:** `haive.agents.rag.db_rag.sql_rag.agent`

**SQLRAGConfig** (🟢 Simple)
_RAG & Retrieval | haive-agents_
Configuration for the SQL RAG Agent.
**Features:** retrieval, structured_output
**Module:** `haive.agents.rag.db_rag.sql_rag.config`

**STORMAgentConfig** (🟡 Medium)
_Research & Information | haive-agents_
Configuration for the STORM agent - an orchestrator that coordinates research,
**Features:** retrieval
**Module:** `haive.agents.research.storm.config`

**ScientificPaperAgent** (🟢 Simple)
_Academic & Research | haive-prebuilt_
No description available
**Features:** Basic
**Module:** `haive.prebuilt.scientific_paper_agent.agent`

**ScientificPaperAgentState** (🟢 Simple)
_Academic & Research | haive-prebuilt_
The state of the agent during the paper research process.
**Features:** retrieval
**Module:** `haive.prebuilt.scientific_paper_agent.state`

**SearchIntegrationAgent** (🟢 Simple)
_RAG & Retrieval | haive-agents_
Agent that integrates external search tools.
**Features:** retrieval, tools
**Module:** `haive.agents.rag.adaptive_tools.agent`

**SelfCorrectiveRAGAgent** (🔴 Complex)
_RAG & Retrieval | haive-agents_
RAG agent with self-correction capabilities.
**Features:** retrieval
**Module:** `haive.agents.rag.self_corr.agent`

**SelfDiscoverAgent** (🟢 Simple)
_Reasoning & Critique | haive-agents_
Self Discover Agent
**Features:** Basic
**Module:** `haive.agents.reasoning_and_critique.self_discover.agent`

**SelfDiscoverAgent** (🔴 Complex)
_Reasoning & Critique | haive-agents_
An agent that implements the SelfDiscover methodology with structured output models.
**Features:** reasoning, planning, structured_output
**Module:** `haive.agents.reasoning_and_critique.self_discover.agent2`

**SelfDiscoverAgentConfig** (🔴 Complex)
_Reasoning & Critique | haive-agents_
Configuration for a SelfDiscover agent.
**Features:** reasoning, structured_output
**Module:** `haive.agents.reasoning_and_critique.self_discover.config`

**SelfDiscoverAgentConfig** (🟢 Simple)
_Reasoning & Critique | haive-agents_
Configuration for the Self Discover Agent
**Features:** Basic
**Module:** `haive.agents.reasoning_and_critique.self_discover.agent`

**SelfRAGAgent** (🔴 Complex)
_RAG & Retrieval | haive-agents_
Self-RAG with reflection tokens - determines whether retrieval is needed
**Features:** reasoning, retrieval
**Module:** `haive.agents.rag.multi_agent_rag.additional_workflows`

**SelfRAGAgent** (🔴 Complex)
_RAG & Retrieval | haive-agents_
Self-RAG with reflection tokens and adaptive retrieval.
**Features:** reasoning, retrieval
**Module:** `haive.agents.rag.multi_agent_rag.complete_rag_workflows`

**SelfRAGAgent** (🔴 Complex)
_RAG & Retrieval | haive-agents_
Self-RAG agent with reflection tokens and adaptive retrieval.
**Features:** reasoning, retrieval
**Module:** `haive.agents.rag.multi_agent_rag.enhanced_workflows`

**SelfReflectiveAgenticRAGAgent** (🔴 Complex)
_RAG & Retrieval | haive-agents_
Self-Reflective Agentic RAG - continuously reflects on and improves
**Features:** reasoning, retrieval
**Module:** `haive.agents.rag.multi_agent_rag.advanced_workflows`

**SelfReflectiveRAGAgent** (🔴 Complex)
_RAG & Retrieval | haive-agents_
Self-Reflective RAG agent with iterative improvement capabilities.
**Features:** reasoning, retrieval
**Module:** `haive.agents.rag.self_reflective.agent`

**SelfRouteRAGAgent** (🔴 Complex)
_RAG & Retrieval | haive-agents_
Self-Route RAG - dynamically routes itself to different reasoning
**Features:** reasoning, retrieval
**Module:** `haive.agents.rag.multi_agent_rag.advanced_workflows`

**SelfRouteRAGAgent** (🔴 Complex)
_RAG & Retrieval | haive-agents_
Complete Self-Route RAG agent with structured analysis and iterative planning.
**Features:** planning, retrieval, structured_output
**Module:** `haive.agents.rag.self_route.agent`

**SequentialAgent** (🔴 Complex)
_Specialized Agents | haive-agents_
Sequential agent that executes multiple agents in sequence.
**Features:** Basic
**Module:** `haive.agents.sequential.agent`

**SequentialAgent** (🔴 Complex)
_Multi-Agent Systems | haive-agents_
Multi-agent system with sequential execution.
**Features:** structured_output, conversation
**Module:** `haive.agents.multi.base`

**SequentialAgentConfig** (🟡 Medium)
_Specialized Agents | haive-agents_
Configuration for a SequentialAgent that connects components linearly.
**Features:** structured_output
**Module:** `haive.agents.sequential.config`

**SequentialMultiAgent** (🔴 Complex)
_Multi-Agent Systems | haive-agents_
Multi-agent system that executes agents sequentially.
**Features:** structured_output, conversation
**Module:** `haive.agents.multi.sequential.agent`

**SimpleAgent** (🔴 Complex)
_Foundation Agents | haive-agents_
Simple agent that modifies its engine to include structured output schema.
**Features:** tools, structured_output, conversation
**Module:** `haive.agents.simple.agent`

**SimpleAgent** (🟢 Simple)
_Foundation Agents | haive-agents_
A simple agent with a single node workflow and comprehensive schema handling.
**Features:** structured_output
**Module:** `haive.agents.simple.v2.config`

**SimpleAgentConfig** (🟢 Simple)
_Foundation Agents | haive-agents_
Configuration for a simple single-node agent with comprehensive schema handling.
**Features:** structured_output
**Module:** `haive.agents.simple.config`

**SimpleAgentState** (🔴 Complex)
_Foundation Agents | haive-agents_
Base state for simple agents.
**Features:** memory, conversation
**Module:** `haive.agents.simple.state`

**SimpleCorrectiveRAGAgent** (🟢 Simple)
_RAG & Retrieval | haive-agents_
Simple Corrective RAG implementation using sequential processing.
**Features:** retrieval
**Module:** `haive.agents.rag.multi_agent_rag.simple_enhanced_workflows`

**SimpleHYDERAGAgent** (🟢 Simple)
_RAG & Retrieval | haive-agents_
Simple HYDE RAG agent that generates hypothetical documents before retrieval.
**Features:** retrieval
**Module:** `haive.agents.rag.multi_agent_rag.simple_enhanced_workflows`

**SimpleRAGAgent** (🟢 Simple)
_RAG & Retrieval | haive-agents_
Simple RAG workflow: Retrieval → Answer Generation
**Features:** retrieval
**Module:** `haive.agents.rag.simple.agent`

**SimpleRAGAgent** (🔴 Complex)
_RAG & Retrieval | haive-agents_
Simple RAG agent that retrieves documents and provides basic answers.
**Features:** retrieval, tools, conversation
**Module:** `haive.agents.rag.multi_agent_rag.agents`

**SimpleRAGAnswerAgent** (🟢 Simple)
_RAG & Retrieval | haive-agents_
RAG answer generation agent that creates responses from retrieved documents.
**Features:** retrieval, structured_output
**Module:** `haive.agents.rag.multi_agent_rag.agents`

**SimpleRAGWithMemoryAgent** (🔴 Complex)
_RAG & Retrieval | haive-agents_
Simple RAG with Memory - incorporates conversation history and previous queries
**Features:** retrieval, memory, conversation
**Module:** `haive.agents.rag.multi_agent_rag.additional_workflows`

**SinglePlayerGameAgent** (🔴 Complex)
_Games | haive-games_
Base agent for single-player games.
**Features:** tools
**Module:** `haive.games.single_player.base`

**SpeculativeRAGAgent** (🔴 Complex)
_RAG & Retrieval | haive-agents_
Speculative RAG - generates multiple possible answer hypotheses
**Features:** retrieval
**Module:** `haive.agents.rag.multi_agent_rag.advanced_workflows`

**SpeculativeRAGAgent** (🟢 Simple)
_RAG & Retrieval | haive-agents_
Complete Speculative RAG agent with parallel hypothesis processing.
**Features:** retrieval
**Module:** `haive.agents.rag.speculative.agent`

**StepBackPromptingRAGAgent** (🟢 Simple)
_RAG & Retrieval | haive-agents_
Step-Back Prompting RAG - asks broader conceptual questions before
**Features:** retrieval
**Module:** `haive.agents.rag.multi_agent_rag.additional_workflows`

**StepBackQueryGeneratorAgent** (🔴 Complex)
_RAG & Retrieval | haive-agents_
Agent that generates step-back queries for abstract reasoning.
**Features:** reasoning
**Module:** `haive.agents.rag.step_back.agent`

**StepBackRAGAgent** (🔴 Complex)
_RAG & Retrieval | haive-agents_
Complete Step-Back RAG agent with abstract reasoning.
**Features:** reasoning, retrieval
**Module:** `haive.agents.rag.step_back.agent`

**StructuredKGAgent** (🔴 Complex)
_Document Processing | haive-agents_
An agent that builds a knowledge graph using structured output models.
**Features:** retrieval, structured_output
**Module:** `haive.agents.document_modifiers.kg.kg_map_merge.agent2`

**StructuredOutputAgentConfig** (🟢 Simple)
_Foundation Agents | haive-agents_
Configuration for a structured output agent.
**Features:** tools, structured_output
**Module:** `haive.agents.simple.structured.config`

**SummarizerAgent** (🟡 Medium)
_Document Processing | haive-agents_
SummarizerAgent is a class that summarizes a list of documents.
**Features:** retrieval
**Module:** `haive.agents.document_modifiers.summarizer.map_branch.agent`

**SummarizerAgentConfig** (🟢 Simple)
_Document Processing | haive-agents_
No description available
**Features:** Basic
**Module:** `haive.agents.document_modifiers.summarizer.map_branch.config`

**SupervisorAgent** (🔴 Complex)
_Specialized Agents | haive-agents_
Supervisor agent that manages multiple specialized agents.
**Features:** Basic
**Module:** `haive.agents.supervisor.agent`

**SupervisorAgent** (🔴 Complex)
_Specialized Agents | haive-agents_
ReactAgent-based supervisor with dynamic routing and agent registry.
**Features:** tools
**Module:** `haive.agents.supervisor.agent_v2`

**SystemicReviewOfScientificArticlesAgent** (🟢 Simple)
_Academic & Research | haive-prebuilt_
No description available
**Features:** Basic
**Module:** `haive.prebuilt.systemic_review_of_scientific_articles.agent`

## T

**TLDRAgentConfig** (🟢 Simple)
_Prebuilt Solutions | haive-prebuilt_
No description available
**Features:** Basic
**Module:** `haive.prebuilt.tldr2.agent`

**TOTAgentConfig** (🔴 Complex)
_Reasoning & Critique | haive-agents_
Configuration for the Tree of Thoughts agent.
**Features:** reasoning, retrieval
**Module:** `haive.agents.reasoning_and_critique.tot.config`

**TaskAnalysisAgent** (🔴 Complex)
_Specialized Agents | haive-agents_
Comprehensive task analysis agent that orchestrates multiple analysis engines.
**Features:** planning
**Module:** `haive.agents.task_analysis.agent`

**TaskifierAgent** (🟢 Simple)
_Prebuilt Solutions | haive-prebuilt_
No description available
**Features:** Basic
**Module:** `haive.prebuilt.taskifier.agent`

**TaxonomyAgent** (🔴 Complex)
_Document Processing | haive-agents_
Agent that generates a taxonomy from a conversation history.
**Features:** memory, conversation
**Module:** `haive.agents.document_modifiers.tnt.agent`

**TaxonomyAgentConfig** (🔴 Complex)
_Document Processing | haive-agents_
Agent configuration for generating a taxonomy from conversation history.
**Features:** memory, conversation
**Module:** `haive.agents.document_modifiers.tnt.agent`

**TicTacToeAgent** (🟡 Medium)
_Games | haive-games_
Agent for playing Tic Tac Toe using structured game flow and LLM inference.
**Features:** structured_output
**Module:** `haive.games.tic_tac_toe.agent`

**ToTAgent** (🔴 Complex)
_Reasoning & Critique | haive-agents_
Tree of Thoughts agent implementation.
**Features:** reasoning, retrieval
**Module:** `haive.agents.reasoning_and_critique.tot.agent`

**ToTAgent** (🟡 Medium)
_Reasoning & Critique | haive-agents_
No description available
**Features:** Basic
**Module:** `haive.agents.reasoning_and_critique.tot.modular.agent`

**ToTAgentConfig** (🔴 Complex)
_Reasoning & Critique | haive-agents_
Configuration for a Tree of Thoughts agent.
**Features:** reasoning, retrieval
**Module:** `haive.agents.reasoning_and_critique.tot.modular.config`

**ToolSelectionAgent** (🟢 Simple)
_RAG & Retrieval | haive-agents_
Agent that selects optimal tools based on query analysis.
**Features:** tools
**Module:** `haive.agents.rag.adaptive_tools.agent`

**TypedAgent** (🟢 Simple)
_Specialized Agents | haive-agents_
Generic Agent Base Class with Enhanced Typing and Auto-Configuration
**Features:** Basic
**Module:** `haive.agents.base.generic_agent`

**TypedRAGAgent** (🟡 Medium)
_RAG & Retrieval | haive-agents_
Implements Typed-RAG that classifies queries and routes to specialized handlers.
**Features:** retrieval
**Module:** `haive.agents.rag.typed.agent`

## W

**WeatherDisasterManagementAgent** (🔴 Complex)
_Prebuilt Solutions | haive-prebuilt_
No description available
**Features:** Basic
**Module:** `haive.prebuilt.weather_disaster_management.agent`

**WeatherDisasterManagerConfig** (🟢 Simple)
_Prebuilt Solutions | haive-prebuilt_
No description available
**Features:** tools
**Module:** `haive.prebuilt.weather_disaster_management.config`

**WebLoaderAgent** (🔴 Complex)
_Document Processing | haive-agents_
Specialized document loader agent for loading documents from web URLs.
**Features:** planning
**Module:** `haive.agents.document_loader.web.agent`

**WebNavAgent** (🟡 Medium)
_Specialized Agents | haive-agents_
An interactive web navigation agent using Playwright & LangGraph with integrated tools.
**Features:** tools
**Module:** `haive.agents.agent`

**WebNavAgentConfig** (🟢 Simple)
_Specialized Agents | haive-agents_
Configuration for the Web Navigator Agent.
**Features:** Basic
**Module:** `haive.agents.agent`

**WikiWriterAgent** (🟢 Simple)
_Specialized Agents | haive-agents_
An agent that writes a wiki page.
**Features:** Basic
**Module:** `haive.agents.wiki_writer.agent`

**WikiWriterAgentConfig** (🟢 Simple)
_Specialized Agents | haive-agents_
Configuration for the Wiki Writer Agent.
**Features:** Basic
**Module:** `haive.agents.wiki_writer.agent`

**WordConnectionsAgentConfig** (🟢 Simple)
_Games | haive-games_
Configuration for Word Connections agent.
**Features:** Basic
**Module:** `haive.games.single_player.wordle.config`
