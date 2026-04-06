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

## Critical Development Rules

1. **NO MOCKS EVER**: Test with real LLMs, real tools, real components
2. **Poetry Run Everything**: `poetry run python`, `poetry run pytest` — never run Python directly
3. **Explicit Imports**: `from haive.core.engine import X` not `from engine import X`
4. **Pydantic**: Never override `__init__`, use `model_post_init()` and Field()
5. **Tools in AugLLMConfig**: Pass tools via `AugLLMConfig(tools=[...])`, not `self.tools.append()`
6. **State Schema**: Use `LLMState` when agent has tools (includes engines dict for tool_node)
7. **System Messages**: Go in `AugLLMConfig(system_message=...)`, not ChatPromptTemplate
8. **Agent Composition**: Use MultiAgent, not complex inheritance
9. **Git Safety**: Always diff before commit, commit submodules first, never force push
10. **Async Postgres preferred**: Use PostgresStoreWrapper for production, not InMemoryStore
11. **Research First**: Check existing patterns before implementing — `grep -r "pattern" packages/`
12. **Keep It Simple**: Avoid over-engineering; one line compositions like `MultiAgent([A, B], mode="sequential")`

## Coding Standards

### Python Code Style

```python
# ✅ CORRECT — descriptive names, type hints, early returns
def process_agent_response(
    agent_response: str,
    validation_config: ValidationConfig,
) -> ProcessedResponse:
    """Process agent response with validation."""
    if not agent_response:
        raise ValidationError("Empty response")
    if not validation_config.enabled:
        return ProcessedResponse(content=agent_response, validated=False)
    validated = validate_response(agent_response, validation_config)
    return ProcessedResponse(content=validated, validated=True)

# ❌ WRONG — poor naming, no types, nested logic
def process(resp, config):
    if resp:
        if config:
            if config.enabled:
                return validate_response(resp, config)
```

### Pydantic Model Pattern

```python
from pydantic import BaseModel, Field, ConfigDict, field_validator

class AgentConfig(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra="forbid",
    )

    name: str = Field(..., min_length=1, max_length=50)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    tools: list[str] = Field(default_factory=list)

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        if not v.replace("_", "").isalnum():
            raise ValueError("Name must be alphanumeric with underscores")
        return v

# ❌ NEVER override __init__ — breaks Pydantic validation
# ❌ NEVER use __init__ for setup — use model_post_init() instead
# ✅ Use model_post_init(self, __context) for post-init setup
```

### Error Handling

```python
import logging
logger = logging.getLogger(__name__)

def execute_agent_safely(agent: Agent, input_data: str) -> AgentResponse | None:
    try:
        response = agent.run(input_data)
        if not response:
            logger.warning(f"Agent {agent.name} returned empty response")
            return None
        return response
    except ValidationError as e:
        logger.error(f"Validation error in {agent.name}: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in {agent.name}: {e}")
        raise

# ❌ WRONG — silent failures, print statements
# Never use print() — use logger
# Never silently return None on error without logging
```

### System vs Human Message Pattern

```python
# ✅ System message in AugLLMConfig
engine = AugLLMConfig(
    system_message="You are a helpful assistant.",  # System message HERE
    temperature=0.7,
)

# ✅ Human message via input or ChatPromptTemplate
agent.run("User question here")  # Becomes HumanMessage automatically

# ❌ WRONG — mixing system and human in one template string
```

## Testing Standards — NO MOCKS

```python
# ✅ CORRECT — real components, real execution
def test_react_agent_with_calculator():
    """Test with REAL LLM and tools."""
    @tool
    def calculator(expression: str) -> str:
        """Calculate."""
        return str(eval(expression))

    agent = ReactAgent(
        name="test_calc",
        engine=AugLLMConfig(temperature=0.1, tools=[calculator]),
        max_iterations=3,
    )
    result = agent.run("What is 15 * 23?")
    assert "345" in str(result)

# ❌ WRONG — mocks, fake responses
def test_with_mocks():
    mock_llm = Mock()  # NO MOCKS!
    mock_llm.return_value = "fake"  # Tests nothing real!

# Test file organization:
# packages/haive-{package}/tests/category/test_module.py
# NEVER delete test files — they serve as documentation
```

```bash
# Running tests
poetry run pytest packages/haive-agents/tests/ -v
poetry run pytest packages/haive-agents/tests/multi/ -v
poetry run pytest -k "test_react" -v
```

## Git Safety Protocol

```bash
# BEFORE ANY WORK
git status && git diff

# BEFORE COMMITTING
git diff --cached
git add specific_file.py  # NEVER git add . or git add -A
git commit -m "feat(component): clear description"

# SUBMODULE SAFETY — commit submodule first, then main repo
cd packages/haive-agents
git add ... && git commit -m "feat: ..." && git push origin final-refactor
cd ../..
git add packages/haive-agents
git commit -m "chore: update haive-agents submodule"

# RECOVERY
git reflog  # Find lost commits
git branch recovery-branch HEAD@{n}
```

**Key Rules**: Never force push submodules. Always create backups before major changes. Always check status before work. Stage files individually, not with `.` or `-A`.

## File Organization

```
# Test files — mirror source structure
packages/haive-agents/
├── src/haive/agents/memory/agent.py
└── tests/memory/test_agent.py

# Scripts
scripts/
├── maintenance/    # Fix scripts
├── debug/          # Debug utilities
└── docs/           # Doc build scripts

# Documentation
project_docs/
├── active/architecture/   # Architecture decisions
├── guides/agent/          # Agent building guides
└── sessions/              # Working memory
```

```bash
# ALWAYS check if similar file exists before creating
find packages/ -name "*similar_pattern*" -type f

# Files that MUST stay in root: CLAUDE.md, README.md, pyproject.toml, docker-compose.yml
```

## Docstring Standard (Google-style)

```python
def my_function(param: str, config: Config | None = None) -> Result:
    """Brief description of what this does.

    Args:
        param: Description of parameter.
        config: Optional configuration.

    Returns:
        Result object with processed data.

    Raises:
        ValidationError: If response fails validation.

    Examples:
        >>> result = my_function("test")
        >>> print(result.data)
    """
```

## Memory & Persistence Patterns

### MemoryAgent — Persistent Memory + KG

```python
from haive.agents.memory import create_memory_agent

# Dev (InMemoryStore)
agent = create_memory_agent(name="assistant", user_id="user123")

# Production (PostgreSQL — preferred)
agent = create_memory_agent(name="assistant", user_id="user123",
    connection_string="postgresql://haive:haive@localhost/haive")

# With Neo4j KG
agent = create_memory_agent(name="assistant", user_id="user123")
agent.connect_neo4j()  # Uses NEO4J_URI/USER/PASSWORD env vars
agent.sync_kg_to_neo4j()  # Sync existing triples to graph
triples = agent.query_kg("Alice")  # Graph query
```

### Store Namespaces

```python
# Memory agent uses 3 namespaces per user:
("user", user_id)     # Memories (facts, preferences)
("kg", user_id)       # Knowledge graph triples (subject-predicate-object)
("summary", user_id)  # Conversation summaries (auto-generated)

# Store API (positional args — NOT keyword):
store.put(namespace_tuple, key, value_dict)
store.search(namespace_tuple, query=query, limit=5)
```

### Store Configuration

```python
# Always prefer async Postgres for production
from haive.core.persistence.store.factory import StoreFactory
from haive.core.persistence.store.types import StoreConfig, StoreType

config = StoreConfig(
    type=StoreType.POSTGRES_SYNC,  # or POSTGRES_ASYNC
    connection_params={"connection_string": "postgresql://haive:haive@localhost/haive"},
    setup_on_init=True,
)
store = StoreFactory.create(config)

# InMemoryStore for dev ONLY
from langgraph.store.memory import InMemoryStore
store = InMemoryStore()
```

### KG Extraction & Neo4j

```python
# MemoryAgent auto-extracts KG triples from conversations (post-hook)
# Triples stored in both LangGraph store AND Neo4j (if connected)

# Manual document-level KG extraction:
triples = agent.extract_kg_from_document("Alice works at DeepMind on RL.")

# Raw Cypher queries:
results = agent.query_kg_cypher(
    "MATCH (s:Entity)-[r:RELATES_TO]->(o:Entity) RETURN s.name, r.predicate, o.name"
)

# Neo4j schema: (:Entity {name, type, user_id}) -[:RELATES_TO {predicate}]-> (:Entity)
# See: @project_docs/guides/agent/MEMORY_AGENT_GUIDE.md for full schema
```

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

## Agent Status (2026-04-06)

### Working (30+)

| Agent | Type | Notes |
|-------|------|-------|
| SimpleAgent | Foundation | 1660 lines, BaseGraph, v3 |
| ReactAgent | Foundation | 984 lines, extends SimpleAgent |
| MultiAgent | Foundation | 920 lines, sequential/parallel/conditional |
| DynamicSupervisor | Foundation | 220 lines, dynamic agent mgmt |
| Supervisor | Foundation | 577 lines, multi-supervisor |
| MemoryAgent | Memory | KG extraction, Neo4j, auto-summarize |
| LongTermMemory | Memory | 78 lines, ReactAgent + vector store |
| Conversation (6) | Conversation | Base, Collaborative, Debate, Directed, RoundRobin, SocialMedia |
| LLM Compiler | Planning | 300 lines, DAG plan + join + replan |
| ReWOO | Planning | 254 lines, plan all → execute → solve |
| Reflexion | Reasoning | 271 lines, draft → reflect → revise loop |
| LATS | Reasoning | 265 lines, tree search + backprop |
| Reflection | Reasoning | 473 lines |
| Logic | Reasoning | 140 lines |
| RAG (24 variants) | RAG | Base, Adaptive, Agentic, Dynamic, FLARE, Fusion, HyDE, QueryPlan, SelfReflective, SelfRoute, Speculative, StepBack, + more |
| DocumentLoader (4) | Loader | Base, File, Directory, Web |
| TaskAnalysis | Analysis | Proper Agent inheritance |
| StructuredOutput | Output | Extends SimpleAgent |

### Needs Fix (import path: `haive.core.engine.agent.agent` → `haive.agents.base.agent`)

| Agent | Issue |
|-------|-------|
| Filtered RAG | Wrong import path |
| Self-Corrective RAG | Wrong import, no inheritance |
| DB RAG (Graph + SQL) | Wrong import path (2 files) |
| Summarizer (map + iterative) | Wrong import path |
| KG Extraction (iterative + map) | Wrong import path |
| Person Research | Wrong import, no inheritance |
| Open Perplexity | Wrong import, no inheritance |
| Discovery Agent | Circular import |
| Plan & Execute v2 | No implementation (empty) |

### Broken (need rewrite)

| Agent | Issue |
|-------|-------|
| Complex Extraction | No Agent inheritance |
| TNT | Wrong import, no inheritance |
| Tree of Thoughts | No Agent inheritance (uses DynamicGraph directly) |
| Self-Discover | 79 lines, minimal, agent2.py has better version |
| Storm | Components only, no orchestrator |

### Fix Priority
1. **Import fixes** (15 files) — mechanical: change `from haive.core.engine.agent.agent import Agent` → `from haive.agents.base.agent import Agent`
2. **Missing inheritance** (5 files) — add proper Agent/ReactAgent base class
3. **Incomplete** (3 files) — Plan & Execute, Storm orchestrator, Self-Discover

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
