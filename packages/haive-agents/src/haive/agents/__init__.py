"""Haive Agents Package - Comprehensive collection of intelligent agents.

This package provides a rich collection of pre-built and configurable agents
for various AI tasks including research, conversation, document processing,
planning, reasoning, and more. Each agent is built on the Haive framework
and designed to be modular, extensible, and production-ready.

The agents are organized into logical categories:

Research Agents:
    - Person Research Agent: Comprehensive person research with multi-source data
    - Open Perplexity Agent: Web search and research capabilities
    - STORM Agent: Structured research methodology

Conversation Agents:
    - Debate Agent: Multi-party debate facilitation
    - Collaborative Agent: Team-based problem solving
    - Social Media Agent: Social media content generation and analysis

Document Processing:
    - Document Loader Agent: Multi-format document ingestion
    - Summarizer Agent: Intelligent document summarization
    - Complex Extraction Agent: Structured data extraction

RAG (Retrieval-Augmented Generation):
    - Adaptive RAG: Dynamic retrieval strategy selection
    - Self-Correcting RAG: Error detection and correction
    - Multi-Strategy RAG: Multiple retrieval approaches

Planning and Reasoning:
    - Plan and Execute Agent: Task planning and execution
    - ReWOO Agent: Reasoning without observation
    - LLM Compiler Agent: Code generation and compilation
    - Reflection Agent: Self-reflective reasoning
    - Tree of Thoughts Agent: Branching reasoning exploration

Multi-Agent Systems:
    - Multi-Agent Base: Coordinated multi-agent workflows
    - Sequential Agent: Sequential task execution

Usage:
    ```python
    from haive.agents.research.person import PersonResearchAgent
    from haive.agents.conversation.debate import DebateAgent
    from haive.agents.rag.adaptive_rag import AdaptiveRAGAgent

    # Create a research agent
    research_agent = PersonResearchAgent(
        name="researcher",
        research_topic="AI Ethics"
    )

    # Create a debate agent
    debate_agent = DebateAgent(
        name="debater",
        topic="The future of AGI",
        num_participants=3
    )

    # Run agents
    research_result = await research_agent.ainvoke({"query": "Recent developments"})
    debate_result = await debate_agent.ainvoke({"motion": "AGI will benefit humanity"})
    ```

Each agent includes:
- Comprehensive configuration options
- State management
- Error handling and recovery
- Extensible hooks and mixins
- Rich output formatting
- Production monitoring capabilities
"""

__version__ = "0.1.0"

# Import key agent base classes
from haive.agents.base import Agent, GenericAgent
from haive.agents.multi.agent import MultiAgent
from haive.agents.rag.base.agent import BaseRAGAgent
from haive.agents.rag.simple.agent import SimpleRAGAgent
from haive.agents.react.agent import ReactAgent

# Import commonly used agents
from haive.agents.simple import SimpleAgent

# from haive.agents.planning.plan_and_execute.agent import PlanAndExecuteAgent

__all__ = [
    # Version
    "__version__",
    # Base classes
    "Agent",
    "GenericAgent",
    # Common agents
    "SimpleAgent",
    "ReactAgent",
    "BaseRAGAgent",
    "SimpleRAGAgent",
    "MultiAgent",
    "PlanAndExecuteAgent",
]
