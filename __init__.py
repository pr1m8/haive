"""Haive - Advanced AI Agent Framework

Haive is a comprehensive framework for building production-ready AI agents with 
advanced features including conversation persistence, multi-agent coordination,
tool integration, and state management.

Key Features
------------
- **Modular Architecture**: Namespace packages for clean separation of concerns
- **Auto-Persistence**: Automatic conversation persistence with PostgreSQL/Supabase
- **Rich Agent Library**: Pre-built agents for RAG, ReAct, planning, and more
- **Tool Ecosystem**: Extensive collection of integrations and utilities
- **State Management**: Advanced state schemas with reducers and composition
- **LangGraph Integration**: Seamless integration with LangGraph workflows

Packages
--------
- **haive.core**: Core engine, graph, and schema systems
- **haive.agents**: Pre-built agent implementations
- **haive.tools**: Tool library and integrations
- **haive.games**: Game environments and agents
- **haive.dataflow**: Streaming and data processing
- **haive.mcp**: Model Context Protocol integration
- **haive.prebuilt**: Ready-to-use configurations

Quick Start
-----------
>>> from haive.agents import SimpleAgent
>>> from haive.core.engine import AugLLMConfig
>>> 
>>> # Create an agent with auto-persistence
>>> agent = SimpleAgent(
...     engine=AugLLMConfig(model="gpt-4"),
...     name="assistant"
... )
>>> 
>>> # Run with conversation memory
>>> result = agent.run(
...     {"messages": [{"role": "user", "content": "Hello!"}]},
...     config={"configurable": {"thread_id": "conv-123"}}
... )

Environment Variables
--------------------
- POSTGRES_CONNECTION_STRING: Enable auto-persistence
- OPENAI_API_KEY: OpenAI API access
- ANTHROPIC_API_KEY: Anthropic Claude access

Documentation
-------------
Full documentation available at: https://haive.readthedocs.io

License
-------
MIT License - See LICENSE file for details

Copyright (c) 2025 Haive Framework Contributors
"""

__version__ = "0.1.0"

# Re-export key components for convenience
try:
    from haive.core import (
        AugLLM,
        AugLLMConfig,
        DynamicGraph,
        StateGraph,
        BasicAgentState,
    )
    from haive.agents import (
        Agent,
        SimpleAgent,
        ReactAgent,
        BaseRAGAgent,
        MultiAgent,
    )
    
    __all__ = [
        # Core
        "AugLLM",
        "AugLLMConfig", 
        "DynamicGraph",
        "StateGraph",
        "BasicAgentState",
        # Agents
        "Agent",
        "SimpleAgent",
        "ReactAgent",
        "BaseRAGAgent",
        "MultiAgent",
        # Version
        "__version__",
    ]
except ImportError:
    # Packages may not be installed yet
    __all__ = ["__version__"]