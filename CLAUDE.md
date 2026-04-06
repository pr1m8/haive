# CLAUDE.md - Haive Agent Framework

**Version**: 5.0
**Last Updated**: 2026-04-06

## Project Context

- **Directory**: `/home/will/Projects/haive`
- **Branch**: `final-refactor`
- **Structure**: Monorepo with Git submodules (7 packages)
- **Core Rules**:
  - Always use `poetry run` prefix for ALL Python commands
  - Real components only - NO MOCKS EVER in tests
  - Always use explicit imports: `from haive.core.*`
  - Be EXTREMELY careful with submodules - each is its own repo

## Guides & Documentation

### Agent Design (NEW — 2026-04-06)

- **@project_docs/guides/agent/AGENT_DESIGN_PATTERNS.md** — How to build agents around BaseGraph, state schemas, SimpleAgent/ReactAgent/MultiAgent patterns, anti-patterns
- **@project_docs/guides/agent/MULTIAGENT_STATE_DESIGN.md** — Complex state schemas for multi-agent systems, sequential/parallel/conditional patterns
- **@project_docs/guides/agent/CUSTOM_NODES_AND_GRAPHS.md** — Custom nodes, graph patterns (branching, parallel, reflection loops), NodeConfig types
- **@project_docs/guides/agent/MEMORY_AGENT_GUIDE.md** — Memory + KG integration, Neo4j Cypher, store namespaces, docker-compose
- **@project_docs/guides/agent/STATE_SCHEMA_NOTES.md** — State flow research, engine injection fix, schema hierarchy

### Architecture

- **@project_docs/active/architecture/state_schema_engine_gap.md** — How engines flow through state (FIXED)
- **@project_docs/active/architecture/multi_agent_meta_agent_memory_hub.md** — Multi-agent architecture decisions
- **@project_docs/active/architecture/agent_as_tool_pattern.md** — Agent-as-tool composition
- **@project_docs/guides/TOOL_ROUTING_REFACTOR.md** — Tool routing: pydantic_model vs pydantic_tool vs parse_output

### Standards

- **@project_docs/active/standards/coding/PYDANTIC_PATTERNS.md** — Pydantic best practices
- **@project_docs/active/standards/testing/philosophy.md** — No-mocks testing
- **@project_docs/active/standards/git/workflow.md** — Git safety protocol

## Quick Reference

### Essential Imports

```python
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.schema.prebuilt.llm_state import LLMState
from haive.agents.simple.agent import SimpleAgent
from haive.agents.react.agent import ReactAgent
from haive.agents.multi.agent import MultiAgent
from haive.agents.memory import create_memory_agent
from haive.agents.utils.trace import run_traced
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage
```

### Agent Patterns (the 4 you need)

```python
# 1. SimpleAgent — conversation, no tools
agent = SimpleAgent(name="writer", engine=AugLLMConfig(
    temperature=0.8, system_message="You are a writer."
))

# 2. ReactAgent — tools + reasoning loop
@tool
def search(query: str) -> str:
    '''Search.'''
    return f"Results for {query}"

agent = ReactAgent(name="researcher", engine=AugLLMConfig(
    tools=[search], system_message="Use search tool."
), max_iterations=3)

# 3. MultiAgent — compose agents
pipeline = MultiAgent(name="pipeline",
    agents=[researcher, writer], execution_mode="sequential")

# 4. MemoryAgent — persistent memory + KG
agent = create_memory_agent(name="assistant", user_id="user123",
    connection_string="postgresql://haive:haive@localhost/haive")
```

### Debug & Trace

```python
from haive.agents.utils.trace import run_traced
result = run_traced(agent, "Hello", save_to="traces/")
```

## Critical Rules

1. **NO MOCKS EVER**: Test with real LLMs, real tools, real components
2. **Poetry Run Everything**: `poetry run python`, `poetry run pytest`
3. **Explicit Imports**: `from haive.core.engine import X` not `from engine import X`
4. **Pydantic**: Never override `__init__`, use `model_post_init()` and Field()
5. **Tools in AugLLMConfig**: Pass tools via `AugLLMConfig(tools=[...])`, not `self.tools.append()`
6. **State Schema**: Use `LLMState` when agent has tools (includes engines dict for tool_node)
7. **System Messages**: Go in `AugLLMConfig(system_message=...)`, not ChatPromptTemplate
8. **Agent Composition**: Use MultiAgent, not complex inheritance
9. **Git Safety**: Always diff before commit, commit submodules first
10. **Async Postgres preferred**: Use PostgresStoreWrapper for production, not InMemoryStore

## Package Structure

```
packages/                          # Each is its own Git repo (submodule)
├── haive-core/     # Foundation: engine, graph, schema, persistence, store
├── haive-agents/   # Agent implementations: simple, react, multi, memory, rag
├── haive-tools/    # Tool implementations
├── haive-games/    # Game environments
├── haive-mcp/      # MCP integration
├── haive-prebuilt/ # Pre-configured agents
└── haive-dataflow/ # Data processing

project_docs/       # Documentation (main repo)
├── active/architecture/   # Architecture decisions
├── guides/agent/          # Agent building guides (NEW)
├── guides/tools/          # Tool guides
└── sessions/              # Working memory

demos/              # Demo scripts
├── agents/         # Agent demos (memory_agent_e2e.py, etc.)
└── games/          # Game demos
```

### Submodule Workflow

```bash
# Work in submodule
cd packages/haive-agents
git add ... && git commit -m "feat: ..." && git push origin final-refactor
cd ../..
git add packages/haive-agents && git commit -m "chore: update submodule"
```

### Import Hierarchy (no circular deps)

```
Core → standard library, third-party
Agents → core, standard library, third-party
Tools → core, standard library, third-party
Games → core, agents, tools, third-party
```

## State Schema Quick Reference

```
StateSchema → engines: dict[str, Engine] (base)
├── MessagesState → messages: list[BaseMessage]
│   └── ToolState → tools, tool_routes, tool_metadata
│       ├── LLMState → full engine mgmt ← DEFAULT for agents with tools
│       │   └── ReactAgentState → iteration, tool_results
│       └── MultiAgentState → agents, agent_states, agent_outputs
```

**Rule**: If agent has tools, state_schema MUST be LLMState or subclass.
The base Agent auto-selects LLMState when `engine.tools` is non-empty.

## Docker (Postgres + Neo4j)

```bash
docker-compose up -d
# Postgres: postgresql://haive:haive@localhost:5432/haive (pgvector)
# Neo4j:    bolt://localhost:7687 (neo4j/haivepass, APOC plugin)
# Neo4j UI: http://localhost:7474
```

## Common Commands

```bash
poetry run python script.py
poetry run pytest packages/haive-agents/tests/ -v
poetry run python -c "from haive.core import *; print('OK')"

# Run memory agent e2e
poetry run python demos/agents/memory_agent_e2e.py
poetry run python demos/agents/memory_agent_e2e.py --neo4j
```

## Recent Work (2026-04-06)

### MemoryAgent Phase 2 Complete
- 4 memory tools: save_memory, search_memory, save_knowledge, search_knowledge
- Auto-context pre-hook: loads memories + KG triples + summaries
- KG extraction post-hook: LLM extracts triples from conversations
- Auto-summarize post-hook: summarizes on token threshold
- Neo4j integration: connect_neo4j() → sync + Cypher queries
- Docker: PostgreSQL (pgvector) + Neo4j (APOC)
- See: @project_docs/guides/agent/MEMORY_AGENT_GUIDE.md

### Base Agent Fixes
- `_setup_schemas()` defaults to LLMState when tools present
- `execution_mixin` injects engines into invoke_input
- `tool_node_config_v2` passes messages directly (not state.dict())
- MultiAgent wrapper passes engines to child agents
- See: @project_docs/active/architecture/state_schema_engine_gap.md

### Agent Trace Utility
- `haive.agents.utils.trace.run_traced(agent, input)` — Rich pretty-print
- Saves traces to JSON for debugging

---

**Keep this file lean. Detailed guides are in `project_docs/guides/agent/`.**
