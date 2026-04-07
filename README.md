# Haive — AI Agent Framework

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![CI](https://github.com/pr1m8/haive/actions/workflows/ci.yml/badge.svg)](https://github.com/pr1m8/haive/actions/workflows/ci.yml)

**Production-ready Python framework for building LLM-powered agents.** From simple chatbots to complex multi-agent pipelines with persistent memory, RAG, knowledge graphs, and tool ecosystems.

> 🎯 **53+ working agents** • **22+ RAG variants** • **23 game environments** • **PostgreSQL + Neo4j** • **MCP integration**

## Packages

Haive is a monorepo with 7 published packages on PyPI:

| Package | Version | Description | Docs |
|---------|---------|-------------|------|
| [`haive-core`](https://pypi.org/project/haive-core/) | [![PyPI](https://img.shields.io/pypi/v/haive-core.svg)](https://pypi.org/project/haive-core/) | Foundation: engines, graphs, schemas, persistence | [📖](https://pr1m8.github.io/haive-core/) |
| [`haive-agents`](https://pypi.org/project/haive-agents/) | [![PyPI](https://img.shields.io/pypi/v/haive-agents.svg)](https://pypi.org/project/haive-agents/) | 53+ production agents (Simple, React, Multi, Memory, RAG, Research) | [📖](https://pr1m8.github.io/haive-agents/) |
| [`haive-games`](https://pypi.org/project/haive-games/) | [![PyPI](https://img.shields.io/pypi/v/haive-games.svg)](https://pypi.org/project/haive-games/) | 23 LLM-powered game environments | [📖](https://pr1m8.github.io/haive-games/) |
| [`haive-tools`](https://pypi.org/project/haive-tools/) | [![PyPI](https://img.shields.io/pypi/v/haive-tools.svg)](https://pypi.org/project/haive-tools/) | Tool implementations (search, code, web, APIs) | [📖](https://pr1m8.github.io/haive-tools/) |
| [`haive-mcp`](https://pypi.org/project/haive-mcp/) | [![PyPI](https://img.shields.io/pypi/v/haive-mcp.svg)](https://pypi.org/project/haive-mcp/) | Dynamic MCP integration (1,960+ servers) | [📖](https://pr1m8.github.io/haive-mcp/) |
| [`haive-hap`](https://pypi.org/project/haive-hap/) | [![PyPI](https://img.shields.io/pypi/v/haive-hap.svg)](https://pypi.org/project/haive-hap/) | Haive Agent Protocol (workflow orchestration) | [📖](https://pr1m8.github.io/haive-hap/) |
| [`haive-dataflow`](https://pypi.org/project/haive-dataflow/) | [![PyPI](https://img.shields.io/pypi/v/haive-dataflow.svg)](https://pypi.org/project/haive-dataflow/) | Data pipelines & component registry | [📖](https://pr1m8.github.io/haive-dataflow/) |

## Installation

```bash
# Foundation only
pip install haive-core

# With agents
pip install haive-agents

# Everything
pip install haive-core haive-agents haive-games haive-tools haive-mcp haive-hap haive-dataflow
```

## Quick Start

```python
from haive.agents.simple.agent import SimpleAgent
from haive.agents.react.agent import ReactAgent
from haive.agents.multi.agent import MultiAgent
from haive.agents.memory import create_memory_agent
from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.tools import tool

# 1. Simple LLM agent
writer = SimpleAgent(name="writer", engine=AugLLMConfig(temperature=0.8))

# 2. Tool-using agent
@tool
def search(query: str) -> str:
    """Search the web."""
    return f"Results for {query}"

researcher = ReactAgent(
    name="researcher",
    engine=AugLLMConfig(tools=[search]),
    max_iterations=3,
)

# 3. Compose them
pipeline = MultiAgent(
    name="research_pipeline",
    agents=[researcher, writer],
    execution_mode="sequential",
)
result = pipeline.run("Write about quantum computing")

# 4. Memory agent with persistent KG
memory = create_memory_agent(
    name="assistant",
    user_id="user123",
    connection_string="postgresql://haive:haive@localhost/haive",
)
memory.run("My name is Alice and I work at DeepMind on RL.")
memory.run("What do you know about me?")  # Recalls memories + KG facts
```

## Features

### 🤖 Agents
- **Foundation**: SimpleAgent, ReactAgent, MultiAgent, DynamicSupervisor
- **Memory**: MemoryAgent (KG extraction + auto-summarize + Neo4j)
- **RAG**: 22+ variants — Adaptive, Agentic, FLARE, Fusion, HyDE, Self-Reflective, GraphDB-RAG
- **Reasoning**: Reflexion, LATS, Reflection, Tree of Thoughts
- **Planning**: PlanAndExecute, LLMCompiler, ReWOO
- **Research**: Perplexity-style + Deep Research with Tavily
- **Conversation**: 6 patterns (Debate, Round Robin, Social Media, etc.)

### 🧠 Memory & Knowledge
- Persistent memory with auto-summarization
- Automatic KG triple extraction from conversations
- Neo4j integration with Cypher queries
- PostgreSQL store (sync + async)

### 🛠️ Infrastructure
- Docker Compose: PostgreSQL (pgvector) + Neo4j (APOC)
- LangSmith tracing built-in
- Rich pretty-printer for agent traces
- 80+ demos in `demos/`

## Architecture

```
haive-core (foundation)
    ├── AugLLMConfig — unified LLM configuration
    ├── BaseGraph — graph builder over LangGraph
    ├── State Schemas — LLMState, MultiAgentState, etc.
    └── Persistence — Postgres, Neo4j, InMemory

haive-agents (built on core)
    ├── SimpleAgent / ReactAgent / MultiAgent
    ├── MemoryAgent (memory + KG + Neo4j)
    ├── RAG variants (22+)
    └── Research / Planning / Reasoning

haive-games (built on agents)
    └── 23 LLM-powered game environments

haive-tools / haive-mcp / haive-hap / haive-dataflow
    └── Specialized capabilities
```

## Documentation

| Resource | Link |
|----------|------|
| 📖 Full docs | https://pr1m8.github.io/haive-core/ |
| 🎯 Agent design patterns | [project_docs/guides/agent/AGENT_DESIGN_PATTERNS.md](project_docs/guides/agent/AGENT_DESIGN_PATTERNS.md) |
| 🧠 Memory agent guide | [project_docs/guides/agent/MEMORY_AGENT_GUIDE.md](project_docs/guides/agent/MEMORY_AGENT_GUIDE.md) |
| 🤖 Multi-agent state | [project_docs/guides/agent/MULTIAGENT_STATE_DESIGN.md](project_docs/guides/agent/MULTIAGENT_STATE_DESIGN.md) |
| 🎮 Demos | [demos/agents/](demos/agents/) and [demos/games/](demos/games/) |

## Development

```bash
# Clone with submodules
git clone --recursive https://github.com/pr1m8/haive.git
cd haive

# Install
poetry install

# Start Postgres + Neo4j
docker-compose up -d

# Run an agent demo
poetry run python demos/agents/03_react_agent.py
poetry run python demos/agents/memory_agent_e2e.py

# Run a game demo
poetry run python demos/games/14_chess.py
poetry run python demos/games/28_among_us.py
```

## License

MIT © [pr1m8](https://github.com/pr1m8)
