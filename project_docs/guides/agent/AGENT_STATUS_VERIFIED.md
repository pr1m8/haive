# Agent Status -- Verified 2026-04-06

All 55 agents verified for import. Core agents verified for execution with real LLM calls.

## Foundation Agents

| Agent | Import | Execution | Notes |
|-------|--------|-----------|-------|
| SimpleAgent | OK | OK | Foundation, conversation + structured output |
| ReactAgent | OK | OK | Tools, reasoning loops |
| MultiAgent | OK | OK | Sequential, parallel, dynamic add/remove/create |
| MemoryAgent | OK | OK | Conversation memory persistence |

## Supervisor Agents

| Agent | Import | Execution | Notes |
|-------|--------|-----------|-------|
| DynamicSupervisor | OK | OK | `dynamic_supervisor.agent.DynamicSupervisor` |
| SupervisorAgent | OK | OK | `supervisor.core.supervisor_agent.SupervisorAgent` |
| SimpleSupervisor | OK | OK | `supervisor.core.simple_supervisor.SimpleSupervisor` |

## Conversation Agents

| Agent | Import | Execution | Notes |
|-------|--------|-----------|-------|
| BaseConversationAgent | OK | OK | Foundation for all conversation types |
| CollaborativeConversation | OK | OK | Note: directory is `collaberative` (typo) |
| DebateConversation | OK | OK | Structured debate format |
| DirectedConversation | OK | OK | Moderator-directed flow |
| RoundRobinConversation | OK | OK | Sequential turn-taking |
| SocialMediaConversation | OK | OK | Social media simulation |

## Planning Agents

| Agent | Import | Execution | Notes |
|-------|--------|-----------|-------|
| LLMCompilerAgent | OK | OK | DAG-based parallel task execution |
| ReWOOAgent | OK | OK | Reasoning Without Observation |
| PlanAndExecuteAgent | OK | OK | Plan then execute pattern |

## Reasoning Agents

| Agent | Import | Execution | Notes |
|-------|--------|-----------|-------|
| ReflexionAgent | OK | OK | Self-reflection with memory |
| LATSAgent | OK | OK | Language Agent Tree Search |
| ReflectionAgent | OK | OK | Generate + reflect loop |

## Discovery & Utility Agents

| Agent | Import | Execution | Notes |
|-------|--------|-----------|-------|
| ComponentDiscoveryAgent | OK | N/A | Utility agent, not LLM-based |
| DynamicToolSelector | OK | N/A | Tool selection utility |
| SemanticDiscoveryEngine | OK | N/A | Semantic search utility |
| LongTermMemoryAgent | OK | Legacy | Extends old ReactAgent pattern |

## Chain & Structured Agents

| Agent | Import | Execution | Notes |
|-------|--------|-----------|-------|
| DeclarativeChainAgent | OK | N/A | Declarative chain builder |
| ChainAgent | OK | N/A | Placeholder (temporarily disabled) |
| StructuredOutputAgent | OK | OK | Structured output with validation |
| TaskAnalysisAgent | OK | OK | Task decomposition |

## Document Agents

| Agent | Import | Execution | Notes |
|-------|--------|-----------|-------|
| DocumentLoaderAgent | OK | Legacy | Base document loader |
| FileLoaderAgent | OK | Legacy | File-based loading |
| WebLoaderAgent | OK | Legacy | Web page loading |
| DirectoryLoaderAgent | OK | Legacy | Directory loading |
| DocumentProcessingAgent | OK | Legacy | Document processing pipeline |
| ParallelKGTransformerConfig | OK | Legacy | Knowledge graph extraction config |

## Document Modifier Agents

| Agent | Import | Notes |
|-------|--------|-------|
| MapBranchSummarizer | OK | Legacy, parallel map-reduce summarization |
| IterativeSummarizer | OK | Legacy, iterative refinement summarization |
| ParallelKGTransformer | OK | Legacy, parallel KG extraction + merge |
| KGIterativeRefinement | OK | Legacy, iterative KG refinement |
| ComplexExtractionAgent | OK | Legacy, structured data extraction |
| TNTAgent | OK | Legacy, translate-and-transform |
| GraphTransformer | OK | Legacy, LLMGraphTransformer wrapper for doc→KG |

## RAG Agents (22 total)

| Agent | Import | Notes |
|-------|--------|-------|
| AdaptiveRAGAgent | OK | Adaptive strategy selection |
| AdaptiveToolsRAGAgent | OK | Adaptive tool-based RAG |
| AgenticRAGAgent | OK | ReactAgent with retrieval tools |
| CorrectiveRAGAgent | OK | Self-correcting retrieval |
| DynamicRAGAgent | OK | Multi-source dynamic retrieval |
| FLARERAGAgent | OK | Forward-looking active retrieval |
| RAGFusionAgent | OK | Reciprocal rank fusion |
| HyDERAGAgent | OK | Hypothetical document embeddings |
| LLMRAGAgent | OK | LLM-based RAG |
| MultiQueryRAGAgent | OK | Multiple query variants |
| SelfCorrectiveRAGAgent | OK | Self-correcting |
| SelfReflectiveRAGAgent | OK | Reflective with grading |
| SelfRouteRAGAgent | OK | Query-aware routing |
| SimpleRAGAgent | OK | Basic retriever + answer |
| SpeculativeRAGAgent | OK | Hypothesis + parallel verification |
| StepBackRAGAgent | OK | Abstract query generation |
| DocumentGradingRAGAgent | OK | Document relevance grading |
| HallucinationGraderAgent | OK | Hallucination detection |
| MemoryAwareRAGAgent | OK | RAG with memory context |
| QueryDecomposerAgent | OK | Hierarchical query decomposition |
| FilteredRAGAgent | OK | Filtered retrieval |
| TypedRAGAgent | OK | Typed retrieval |
| MultiStrategyRAGAgent | OK | Multi-strategy |
| QueryPlanningRAGAgent | OK | Query planning |

## Research Agents

| Agent | Import | Notes |
|-------|--------|-------|
| STORMAgentConfig | OK | STORM research pipeline config |

## MultiAgent Verified Capabilities

| Feature | Status | Notes |
|---------|--------|-------|
| Sequential mode | OK | Agents run in order |
| Parallel mode | OK | Agents run concurrently, results combined |
| Dynamic add_agent | OK | Add agent at runtime |
| Dynamic remove_agent | OK | Remove agent at runtime |
| Dynamic create_agent | OK | Create new agent with system_message + temperature |
| get_agent_names | OK | List current agents |
| get_agent | OK | Get agent by name |

## Fixes Applied

1. **chain/__init__.py**: Removed import of missing `examples.py` module, added placeholder stubs
2. **research/storm/__init__.py**: Removed import of missing `example.py` module, added placeholder stub

## Summary

- **Total agents verified**: 62 (55 + 7 document modifiers)
- **All imports passing**: 62/62
- **Fixes applied**: 2 (missing module imports replaced with stubs)
- **No circular import issues found** (discovery agent imports cleanly)
