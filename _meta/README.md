# Haive — AI Agent Framework

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![CI](https://github.com/pr1m8/haive/actions/workflows/ci.yml/badge.svg)](https://github.com/pr1m8/haive/actions/workflows/ci.yml)

**Production-ready Python framework for building LLM-powered agents.** From simple chatbots to complex multi-agent pipelines with persistent memory, RAG, knowledge graphs, and tool ecosystems.

> 🎯 **53+ working agents** • **22+ RAG variants** • **23 game environments** • **PostgreSQL + Neo4j** • **MCP integration** • **9 PyPI packages**

---

## What is Haive?

Haive is a production-grade framework built on top of LangGraph and LangChain. It fills the gap between raw state machines (LangGraph) and ready-to-use agents — providing a unified abstraction over LLM configuration, tool routing, state management, persistence, and multi-agent composition.

The framework is organized as a monorepo with **9 published PyPI packages**, each focused on a specific concern. You can install just the parts you need.

### Why not just use LangGraph directly?

LangGraph is powerful but low-level. Building production agents on it requires hand-rolling state schemas, tool routing, validation nodes, and persistence. Haive gives you all of this as a library:

- **State schemas with the right fields** — `LLMState`, `MultiAgentState`, etc. that include `engines` for tool execution
- **Automatic tool routing** — `langchain_tool`, `pydantic_model`, `pydantic_tool`, `parse_output` detected and routed correctly
- **Pre-built agent patterns** — SimpleAgent, ReactAgent, MultiAgent, MemoryAgent, 22+ RAG variants
- **Persistence layer** — PostgreSQL + Neo4j with sync and async support
- **Memory + KG extraction** — automatic knowledge graph construction from conversations
- **No mocks testing** — every agent verified end-to-end with real LLMs

### Why not LangChain agents?

LangChain agents are simple but limited. They don't compose well, don't have first-class memory, and don't support multi-agent patterns out of the box. Haive's `MultiAgent` lets you compose any agents into sequential, parallel, or conditional pipelines — and `MemoryAgent` gives you persistent memory with KG extraction in 3 lines of code.

---

## Packages

Haive is published as **9 PyPI packages**, each focused on a specific concern:

| Package | Version | Description | Docs |
|---------|---------|-------------|------|
| [`haive-core`](https://pypi.org/project/haive-core/) | [![PyPI](https://img.shields.io/pypi/v/haive-core.svg)](https://pypi.org/project/haive-core/) | Foundation: engines, graphs, schemas, persistence | [📖](https://pr1m8.github.io/haive-core/) |
| [`haive-agents`](https://pypi.org/project/haive-agents/) | [![PyPI](https://img.shields.io/pypi/v/haive-agents.svg)](https://pypi.org/project/haive-agents/) | 53+ production agents (Simple, React, Multi, Memory, RAG, Research) | [📖](https://pr1m8.github.io/haive-agents/) |
| [`haive-games`](https://pypi.org/project/haive-games/) | [![PyPI](https://img.shields.io/pypi/v/haive-games.svg)](https://pypi.org/project/haive-games/) | 23 LLM-powered game environments | [📖](https://pr1m8.github.io/haive-games/) |
| [`haive-tools`](https://pypi.org/project/haive-tools/) | [![PyPI](https://img.shields.io/pypi/v/haive-tools.svg)](https://pypi.org/project/haive-tools/) | Tool implementations (search, code, web, APIs) | [📖](https://pr1m8.github.io/haive-tools/) |
| [`haive-mcp`](https://pypi.org/project/haive-mcp/) | [![PyPI](https://img.shields.io/pypi/v/haive-mcp.svg)](https://pypi.org/project/haive-mcp/) | Dynamic MCP integration (1,960+ servers) | [📖](https://pr1m8.github.io/haive-mcp/) |
| [`haive-hap`](https://pypi.org/project/haive-hap/) | [![PyPI](https://img.shields.io/pypi/v/haive-hap.svg)](https://pypi.org/project/haive-hap/) | Haive Agent Protocol (workflow orchestration) | [📖](https://pr1m8.github.io/haive-hap/) |
| [`haive-dataflow`](https://pypi.org/project/haive-dataflow/) | [![PyPI](https://img.shields.io/pypi/v/haive-dataflow.svg)](https://pypi.org/project/haive-dataflow/) | Data pipelines & component registry | [📖](https://pr1m8.github.io/haive-dataflow/) |
| [`haive-prebuilt`](https://pypi.org/project/haive-prebuilt/) | [![PyPI](https://img.shields.io/pypi/v/haive-prebuilt.svg)](https://pypi.org/project/haive-prebuilt/) | Pre-configured agent presets | [📖](https://pr1m8.github.io/haive-prebuilt/) |
| [`pydevelop-docs`](https://pypi.org/project/pydevelop-docs/) | [![PyPI](https://img.shields.io/pypi/v/pydevelop-docs.svg)](https://pypi.org/project/pydevelop-docs/) | Universal Sphinx docs generator | [📖](https://pr1m8.github.io/haive-docs/) |

---

## Installation

```bash
# Foundation only
pip install haive-core

# With agents (most common)
pip install haive-agents

# Everything
pip install haive-core haive-agents haive-games haive-tools haive-mcp haive-hap haive-dataflow haive-prebuilt
```

---

## Quick Start

### 1. Simple LLM Agent

```python
from haive.agents.simple.agent import SimpleAgent
from haive.core.engine.aug_llm import AugLLMConfig

writer = SimpleAgent(
    name="writer",
    engine=AugLLMConfig(
        temperature=0.8,
        system_message="You are a creative writer.",
    ),
)
result = writer.run("Write a haiku about quantum computing.")
```

### 2. Tool-Using Agent (ReAct Pattern)

```python
from haive.agents.react.agent import ReactAgent
from langchain_core.tools import tool

@tool
def calculator(expression: str) -> str:
    """Calculate mathematical expressions."""
    return str(eval(expression, {"__builtins__": {}}))

@tool
def search(query: str) -> str:
    """Search the web."""
    return f"Results for {query}"

researcher = ReactAgent(
    name="researcher",
    engine=AugLLMConfig(tools=[calculator, search]),
    max_iterations=5,
)
result = researcher.run("What is 15 * 23 and how does that compare to the speed of light?")
```

### 3. Multi-Agent Pipeline

```python
from haive.agents.multi.agent import MultiAgent

# Sequential: each agent sees previous output
pipeline = MultiAgent(
    name="research_pipeline",
    agents=[researcher, analyzer, writer],
    execution_mode="sequential",
)
result = pipeline.run("Research and write about AI safety")

# Parallel: agents run concurrently
parallel = MultiAgent(
    name="multi_perspective",
    agents=[technical_agent, business_agent, ethical_agent],
    execution_mode="parallel",
)
```

### 4. Memory Agent with Knowledge Graph

```python
from haive.agents.memory import create_memory_agent

# Production setup with PostgreSQL + Neo4j
agent = create_memory_agent(
    name="assistant",
    user_id="alice",
    connection_string="postgresql://haive:haive@localhost/haive",
    neo4j_config=True,  # Enable Cypher KG queries
)

# Have a conversation — agent remembers + extracts KG
agent.run("My name is Alice. I work at DeepMind on RL with PyTorch.")
# Auto-saves: memories + KG triples
# (Alice)-[works_at]->(DeepMind)
# (Alice)-[focuses_on]->(reinforcement_learning)
# (Alice)-[uses]->(PyTorch)

agent.run("What do you know about me?")
# Pre-hook loads relevant memories + KG facts as context
# LLM responds with full recall
```

### 5. Research Agent (Perplexity-Style)

```python
from haive.agents.research import create_research_agent

agent = create_research_agent(name="researcher", max_search_iterations=8)
# Uses Tavily if TAVILY_API_KEY set, mock otherwise

result = agent.run("What are the latest advances in quantum computing in 2025?")
# QueryAnalyzer → Researcher (search + RAG store) → Synthesizer
```

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     haive (parent)                          │
│  Main repo — orchestration, demos, docs, docker-compose    │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│  haive-core  │  ←   │ haive-agents │  ←   │ haive-games  │
│              │      │              │      │              │
│ • AugLLMConfig│     │ • SimpleAgent │      │ • Chess, Go  │
│ • BaseGraph   │     │ • ReactAgent  │      │ • Among Us   │
│ • State schemas│    │ • MultiAgent  │      │ • Mafia, etc │
│ • Persistence │     │ • MemoryAgent │      │              │
│ • Tool routing│     │ • RAG (22+)   │      │              │
└──────────────┘      └──────────────┘      └──────────────┘
                              │
                              ▼
        ┌──────────────┬─────┴────────┬──────────────┐
        ▼              ▼              ▼              ▼
   ┌─────────┐   ┌─────────┐    ┌─────────┐   ┌──────────┐
   │  tools  │   │   mcp   │    │   hap   │   │ dataflow │
   │         │   │  1960+  │    │workflow │   │ETL/regis │
   └─────────┘   └─────────┘    └─────────┘   └──────────┘
```

---

## Features

### 🤖 Agent Catalog (53+ implementations)

- **Foundation**: SimpleAgent, ReactAgent, MultiAgent, DynamicSupervisor, Supervisor
- **Memory**: MemoryAgent (KG extraction + auto-summarize + Neo4j), LongTermMemoryAgent
- **RAG (22+ variants)**: Adaptive, Agentic, Dynamic, FLARE, Fusion, HyDE, Self-Reflective, Self-Route, Speculative, Step-Back, Query Planning, Query Decomposition, Memory-Aware, GraphDB-RAG, SQL-RAG
- **Reasoning**: Reflexion, LATS (tree search), Reflection, Logic, Tree of Thoughts, Self-Discover
- **Planning**: PlanAndExecute, LLMCompiler (DAG), ReWOO
- **Research**: Perplexity-style (3-stage), DeepResearch (5-stage)
- **Conversation**: 6 patterns (Debate, Round Robin, Social Media, Collaborative, Directed)

### 🧠 Memory & Knowledge

- **Persistent memory** — PostgreSQL with pgvector, async support
- **Auto-context** — searches store before each response, injects relevant facts
- **KG extraction** — automatic triple extraction from conversations
- **Neo4j integration** — Cypher queries on the knowledge graph
- **Auto-summarization** — manages context length with rolling summaries
- **GraphDB-RAG** — natural language → Cypher → graph traversal

### 🛠️ Infrastructure

- **Docker Compose** — PostgreSQL (pgvector) + Neo4j (APOC) ready
- **LangSmith tracing** — built-in observability
- **Rich trace utility** — `haive.agents.utils.trace.run_traced(agent, "...")` for clean output
- **80+ demos** — every agent has a runnable demo in `demos/`

### 🔌 Tool Ecosystem

- **Static tools** (`haive-tools`): Tavily, Google, calculators, code execution, APIs
- **Dynamic tools** (`haive-mcp`): Search and integrate from 1,960+ MCP servers at runtime
- **Custom tools**: LangChain `@tool`, Pydantic models, callables — all supported
- **Tool routing**: automatic detection and routing to correct execution path

---

## Documentation

| Resource | Link |
|----------|------|
| 📖 Per-package docs | https://pr1m8.github.io/haive-core/ |
| 🎯 Agent design patterns | [project_docs/guides/agent/AGENT_DESIGN_PATTERNS.md](project_docs/guides/agent/AGENT_DESIGN_PATTERNS.md) |
| 🧠 Memory agent guide | [project_docs/guides/agent/MEMORY_AGENT_GUIDE.md](project_docs/guides/agent/MEMORY_AGENT_GUIDE.md) |
| 🤖 Multi-agent state design | [project_docs/guides/agent/MULTIAGENT_STATE_DESIGN.md](project_docs/guides/agent/MULTIAGENT_STATE_DESIGN.md) |
| 🪢 Custom nodes & graphs | [project_docs/guides/agent/CUSTOM_NODES_AND_GRAPHS.md](project_docs/guides/agent/CUSTOM_NODES_AND_GRAPHS.md) |
| 🔧 State schema notes | [project_docs/guides/agent/STATE_SCHEMA_NOTES.md](project_docs/guides/agent/STATE_SCHEMA_NOTES.md) |
| 🎮 Demos | [demos/agents/](demos/agents/) and [demos/games/](demos/games/) |

---

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
poetry run python demos/agents/50_research_agent.py

# Run a game demo
poetry run python demos/games/14_chess.py
poetry run python demos/games/28_among_us.py
```

### Working with Submodules

Each package is its own Git repo. To work on one:

```bash
cd packages/haive-agents
# Make your changes
git add ... && git commit -m "..." && git push origin main

cd ../..
git add packages/haive-agents
git commit -m "chore: update haive-agents submodule"
git push origin main
```

---

## License

MIT © [pr1m8](https://github.com/pr1m8)
