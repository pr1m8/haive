# Haive Integration Guide for ooai (macOS)

A practical guide to getting the Haive AI Agent Framework running inside the **ooai** project on Mac.

---

## 1. Prerequisites

| Requirement | Minimum | Check |
|---|---|---|
| Python | 3.12+ | `python3 --version` |
| Poetry | 1.7+ | `poetry --version` |
| Git | 2.x | `git --version` |
| OpenAI API Key | any valid key | `echo $OPENAI_API_KEY` |

Optional but recommended:
- **Anthropic API Key** (`ANTHROPIC_API_KEY`) for Claude models
- **Ollama** (`brew install ollama`) for local models

---

## 2. Installation on Mac

### 2a. Clone with submodules

Haive is a monorepo with 8 Git submodules. You **must** use `--recurse-submodules`:

```bash
git clone --recurse-submodules https://github.com/pr1m8/haive.git
cd haive
```

If you already cloned without submodules:

```bash
git submodule update --init --recursive
```

### 2b. Install Poetry

```bash
pip install poetry
# or via pipx (preferred on modern macOS)
pipx install poetry
```

### 2c. Install all packages

```bash
poetry install --all-extras
```

This installs all 8 packages (`haive-core`, `haive-agents`, `haive-tools`, `haive-games`, `haive-mcp`, `haive-prebuilt`, `haive-dataflow`, `haive-hap`) plus their dependencies into a single virtualenv.

### 2d. Set up environment variables

Create a `.env` file in the repo root:

```bash
cp .env.example .env
```

Edit `.env` and fill in at minimum:

```
OPENAI_API_KEY=sk-...
```

Other useful keys (optional):

```
ANTHROPIC_API_KEY=sk-ant-...
OLLAMA_BASE_URL=http://localhost:11434
TAVILY_API_KEY=tvly-...
```

Haive automatically loads `.env` via `python-dotenv` at import time.

---

## 3. Quick Verification

Run these to confirm everything is wired up:

```bash
# Core engine
poetry run python -c "from haive.core.engine.aug_llm import AugLLMConfig; print('core OK')"

# Agents
poetry run python -c "from haive.agents.simple.agent import SimpleAgent; print('agents OK')"

# Games
poetry run python -c "from haive.games.chess.agent import ChessAgent; print('games OK')"

# MCP
poetry run python -c "from haive.mcp.discovery.server_discovery import ServerDiscovery; print('mcp OK')"

# Full smoke test with a real LLM call (requires OPENAI_API_KEY)
poetry run python -c "
from haive.core.engine.aug_llm import AugLLMConfig
config = AugLLMConfig()
runnable = config.create_runnable()
result = runnable.invoke('Say hello in one word')
print(f'LLM responded: {result}')
"
```

---

## 4. Running the UI Dashboard

Haive ships with a Streamlit dashboard for agent demos, game playback, and observability.

```bash
cd /path/to/haive
poetry run streamlit run tools/haive-ui/src/haive_ui/app.py \
  --server.port 8501 \
  --server.headless true
```

Then open [http://localhost:8501](http://localhost:8501).

The dashboard includes pages for:
- **Home** - Overview and quick actions
- **Agents** - Run and inspect agents interactively
- **Games** - Play LLM-vs-LLM games (chess, poker, etc.)
- **Discovery** - Browse available MCP tools
- **Trace** - Execution trace viewer
- **Demos** - Pre-built demonstration workflows

---

## 5. Architecture Overview

### Package Map

```
packages/
  haive-core/       Foundation: LLM configs, engine, graphs, state schemas
  haive-agents/     Agent implementations (simple, react, RAG, multi-agent, memory)
  haive-tools/      Tool integrations and toolkits
  haive-games/      LLM-vs-LLM game environments (chess, poker, go, risk, ...)
  haive-mcp/        Model Context Protocol server/client integration
  haive-prebuilt/   Ready-to-use agent configurations
  haive-dataflow/   Streaming and data processing pipelines
  haive-hap/        Haive Agent Protocol (multi-agent orchestration protocol)

tools/
  haive-ui/         Streamlit dashboard
  haive-cli/        CLI tooling
  haive-dev/        Developer utilities
  haive-docs/       Documentation build tools
  haive-testing/    Test infrastructure
```

Each package under `packages/` is its own Git submodule with independent history, branches, and releases. They share a single Poetry virtualenv at the root.

### Import Namespaces

All packages live under the `haive` namespace:

```python
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import OpenAILLMConfig, AnthropicLLMConfig, OllamaLLMConfig
from haive.agents.simple.agent import SimpleAgent
from haive.agents.react.agent import ReactAgent
from haive.agents.multi.agent import MultiAgent
from haive.games.chess.agent import ChessAgent
from haive.games.chess.config import ChessConfig
from haive.mcp.discovery.server_discovery import ServerDiscovery
```

---

## 6. Available Components

### Agents (~40+ implementations)

| Category | Examples |
|---|---|
| **Core** | `SimpleAgent`, `ReactAgent`, `StructuredOutputAgent` |
| **RAG** | `BaseRAGAgent`, `AdaptiveRAGAgent`, `CorrectiveRAG`, `SelfReflectiveRAG`, `HyDE`, `FLARE`, `FusionRAG`, `MultiQueryRAG` |
| **Reasoning** | `TreeOfThought`, `LATS`, `MCTS`, `Reflexion`, `SelfDiscover`, `LogicAgent` |
| **Planning** | `PlanAndExecute`, `LLMCompiler`, `ReWOO` |
| **Research** | `StormAgent`, `OpenPerplexity`, `PersonResearch` |
| **Multi-Agent** | `MultiAgent`, `DynamicSupervisor`, `Supervisor` |
| **Conversation** | `DebateAgent`, `RoundRobin`, `Collaborative`, `SocialMedia` |
| **Memory** | `LongTermMemory`, `MemoryAgent`, `QuickSearch`, `ProSearch`, `DeepResearch` |
| **Document** | `DocumentAgent`, `DocumentLoader`, `Summarizer`, `KGMapMerge` |
| **Discovery** | `ComponentDiscovery`, `DynamicToolSelector` |

### Games (21 working environments)

Among Us, Battleship, Checkers, Chess, Clue, Connect4, Debate, Dominoes, Fox & Geese, Go, Hold'em (Texas), Mafia, Mancala, Mastermind, Monopoly, Nim, Poker, Reversi, Risk, Tic-Tac-Toe, plus single-player variants (Wordle).

### MCP Integration

- **Server Discovery** - Scan for installed MCP servers
- **Plugin Registry** - Register and manage MCP tool providers
- **Retrieval** - MCP-based retrieval for RAG pipelines

---

## 7. Integrating into ooai

Choose one of these approaches:

### Option A: Git submodule (recommended for monorepo setups)

```bash
cd /path/to/ooai
git submodule add https://github.com/pr1m8/haive.git packages/haive
cd packages/haive
git submodule update --init --recursive
cd ../..

# Add haive's source paths to your pyproject.toml or PYTHONPATH
```

Then in your `pyproject.toml` add the source directories:

```toml
[tool.pytest.ini_options]
pythonpath = [
  "packages/haive/packages/haive-core/src",
  "packages/haive/packages/haive-agents/src",
  "packages/haive/packages/haive-tools/src",
  "packages/haive/packages/haive-games/src",
  "packages/haive/packages/haive-mcp/src",
  "packages/haive/packages/haive-dataflow/src",
  "packages/haive/packages/haive-prebuilt/src",
  "packages/haive/packages/haive-hap/src",
]
```

### Option B: Install from local path via Poetry

```bash
cd /path/to/ooai
poetry add --editable /path/to/haive
```

Or in `pyproject.toml`:

```toml
[tool.poetry.dependencies]
haive = { path = "../haive", develop = true }
```

### Option C: PYTHONPATH (quick and dirty)

```bash
export PYTHONPATH="/path/to/haive/packages/haive-core/src:\
/path/to/haive/packages/haive-agents/src:\
/path/to/haive/packages/haive-tools/src:\
/path/to/haive/packages/haive-games/src:\
/path/to/haive/packages/haive-mcp/src:\
/path/to/haive/packages/haive-dataflow/src:\
/path/to/haive/packages/haive-prebuilt/src:\
/path/to/haive/packages/haive-hap/src:$PYTHONPATH"
```

Then import directly:

```python
from haive.agents.simple.agent import SimpleAgent
```

---

## 8. Using Agents in Your Code

### Basic Agent (SimpleAgent)

```python
import asyncio
from haive.agents.simple.agent import SimpleAgent
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import OpenAILLMConfig

# Configure with gpt-4o-mini (default) - reads OPENAI_API_KEY from env
config = AugLLMConfig(
    llm_config=OpenAILLMConfig(model="gpt-4o-mini"),
    system_message="You are a helpful assistant for the ooai project."
)

agent = SimpleAgent(name="ooai_assistant", engine=config)

# Async execution
async def main():
    result = await agent.arun({
        "messages": [{"role": "user", "content": "Hello! What can you do?"}]
    })
    print(result)

asyncio.run(main())
```

### ReactAgent with Tools

```python
from haive.agents.react.agent import ReactAgent
from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.tools import tool

@tool
def lookup_user(user_id: str) -> str:
    """Look up a user in the ooai database."""
    return f"User {user_id}: name=Alice, plan=pro"

@tool
def calculate(expression: str) -> str:
    """Evaluate a math expression."""
    return str(eval(expression))

config = AugLLMConfig(
    system_message="You are an ooai support agent.",
    tools=[lookup_user, calculate],
)

agent = ReactAgent(name="support_agent", engine=config)
```

### Structured Output

```python
from pydantic import BaseModel, Field
from haive.agents.simple.agent import SimpleAgent
from haive.core.engine.aug_llm import AugLLMConfig

class SentimentResult(BaseModel):
    sentiment: str = Field(description="positive, negative, or neutral")
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence score")
    summary: str = Field(description="Brief explanation")

config = AugLLMConfig(
    structured_output_model=SentimentResult,
    system_message="Analyze the sentiment of the user's message."
)

agent = SimpleAgent(name="sentiment_analyzer", engine=config)
```

### Multi-Agent Workflow

```python
from haive.agents.simple.agent import SimpleAgent
from haive.agents.multi.agent import MultiAgent
from haive.core.engine.aug_llm import AugLLMConfig

planner = SimpleAgent(
    name="planner",
    engine=AugLLMConfig(system_message="Create a detailed plan for the task.")
)

executor = SimpleAgent(
    name="executor",
    engine=AugLLMConfig(system_message="Execute the plan and produce results.")
)

reviewer = SimpleAgent(
    name="reviewer",
    engine=AugLLMConfig(
        temperature=0.2,
        system_message="Review the results for quality and accuracy."
    )
)

pipeline = MultiAgent(
    name="content_pipeline",
    agents=[planner, executor, reviewer],
    execution_mode="sequential"
)
```

---

## 9. Swapping LLM Providers

All provider configs live in `haive.core.models.llm.base`. Each reads its API key from the corresponding environment variable automatically.

### OpenAI (default)

```python
from haive.core.models.llm.base import OpenAILLMConfig

config = AugLLMConfig(
    llm_config=OpenAILLMConfig(model="gpt-4o")
)
```

Reads `OPENAI_API_KEY` from environment. Default model is `gpt-4o-mini`.

### Anthropic

```python
from haive.core.models.llm.base import AnthropicLLMConfig

config = AugLLMConfig(
    llm_config=AnthropicLLMConfig(model="claude-sonnet-4-20250514")
)
```

Reads `ANTHROPIC_API_KEY` from environment.

### Ollama (local models)

```bash
# Install Ollama on Mac
brew install ollama
ollama serve &
ollama pull llama3
```

```python
from haive.core.models.llm.base import OllamaLLMConfig

config = AugLLMConfig(
    llm_config=OllamaLLMConfig(
        model="llama3",
        base_url="http://localhost:11434"  # default
    )
)
```

No API key required.

### Google Gemini

```python
from haive.core.models.llm.base import GeminiLLMConfig

config = AugLLMConfig(
    llm_config=GeminiLLMConfig(model="gemini-1.5-pro")
)
```

Reads `GOOGLE_API_KEY` from environment.

### Switching at runtime

```python
# Start with OpenAI
config = AugLLMConfig(llm_config=OpenAILLMConfig(model="gpt-4o-mini"))

# Swap to Anthropic later
from haive.core.models.llm.base import AnthropicLLMConfig
config.llm_config = AnthropicLLMConfig(model="claude-sonnet-4-20250514")
```

---

## 10. MCP Setup

MCP (Model Context Protocol) lets agents discover and use external tools dynamically.

### Install MCP servers

```bash
# Filesystem access
claude mcp add haive-files -s user -- \
  npx -y @modelcontextprotocol/server-filesystem /path/to/ooai

# Web search (requires Brave API key)
claude mcp add haive-search -s user -e BRAVE_API_KEY=$BRAVE_API_KEY -- \
  npx -y @modelcontextprotocol/server-brave-search

# GitHub integration
claude mcp add haive-github -s user -e GITHUB_TOKEN=$GITHUB_TOKEN -- \
  npx -y @modelcontextprotocol/server-github

# List configured servers
claude mcp list
```

### Use MCP discovery in code

```python
from haive.mcp.discovery.server_discovery import ServerDiscovery

# Discover installed MCP servers
discovery = ServerDiscovery()
servers = discovery.discover()
for server in servers:
    print(f"Server: {server.name}, Tools: {server.tools}")
```

### Use the dynamic tool selector

```python
from haive.agents.discovery.dynamic_tool_selector import DynamicToolSelector

selector = DynamicToolSelector()
# Automatically selects the best tools for a given task
tools = selector.select_tools("Search for recent AI papers and summarize them")
```

---

## 11. Running Games / Tournaments

### Quick game: Tic-Tac-Toe

```python
from haive.games.tic_tac_toe.agent import TicTacToeAgent
from haive.games.tic_tac_toe.config import TicTacToeConfig
from haive.core.engine.aug_llm import AugLLMConfig

config = TicTacToeConfig(
    player_names=["GPT-4o", "Claude"],
    llm_config=AugLLMConfig(temperature=0.3),
)

game = TicTacToeAgent(config)
game.run()
```

### Chess: OpenAI vs Anthropic

```python
from haive.games.chess.agent import ChessAgent
from haive.games.chess.config import ChessConfig
from haive.games.chess.configurable_config import create_chess_config

# Pit two models against each other
config = create_chess_config(
    white_model="gpt-4o",
    black_model="claude-3-5-sonnet-20240620",
    temperature=0.7,
)

agent = ChessAgent(config)
initial_state = ChessState()
app = agent.app

for step in app.stream(
    initial_state.model_dump(),
    config={"configurable": {"thread_id": "chess_001"}},
    stream_mode="values",
):
    if "game_status" in step:
        print(f"Status: {step['game_status']}")
```

### Running a full tournament

The tournament runner plays all 21 games between two LLM providers:

```bash
cd /path/to/haive
poetry run python packages/haive-games/tournament_tools/scripts/claude_vs_openai_final_tournament.py
```

Available games in the tournament: Among Us, Battleship, Checkers, Chess, Clue, Connect4, Debate, Dominoes, Fox & Geese, Hold'em, Mafia, Mancala, Mastermind, Monopoly, Nim, Poker, Reversi, Risk, Tic-Tac-Toe.

### Available predefined chess configurations

```python
from haive.games.chess.configurable_config import create_chess_config_from_example

# Predefined matchups
config = create_chess_config_from_example("anthropic_vs_openai")
config = create_chess_config_from_example("gpt4_only")
config = create_chess_config_from_example("claude_only")
config = create_chess_config_from_example("mixed_providers")
config = create_chess_config_from_example("budget_friendly")
```

---

## 12. Troubleshooting

### Import errors

**Symptom:** `ModuleNotFoundError: No module named 'haive'`

**Fix:** Make sure you are using `poetry run` or have activated the Poetry virtualenv:

```bash
poetry run python your_script.py
# or
poetry shell
python your_script.py
```

If using PYTHONPATH, ensure all 8 source paths are included (see Section 7, Option C).

### Submodule issues

**Symptom:** Empty `packages/haive-*` directories

**Fix:**

```bash
git submodule update --init --recursive
```

**Symptom:** Submodule is in detached HEAD state

**Fix:**

```bash
cd packages/haive-core
git checkout main
git pull
cd ../..
```

### Missing API keys

**Symptom:** `ValueError: OpenAI API key is required`

**Fix:** Set the key in your `.env` file at the repo root or export it:

```bash
export OPENAI_API_KEY="sk-..."
```

Haive auto-loads `.env` via `python-dotenv`. Make sure the `.env` file is in your working directory or the haive repo root.

### LangChain dependency conflicts

**Symptom:** Version mismatch errors between `langchain-core`, `langchain-openai`, etc.

**Fix:**

```bash
poetry lock --no-update
poetry install --all-extras
```

### Ollama connection refused

**Symptom:** `ConnectionRefusedError` when using `OllamaLLMConfig`

**Fix:** Make sure the Ollama server is running:

```bash
ollama serve
# In another terminal
ollama list  # verify models are downloaded
```

### Poetry virtual environment on macOS

If Poetry is not creating a virtualenv inside the project:

```bash
poetry config virtualenvs.in-project true
poetry install --all-extras
```

This creates `.venv/` inside the repo, making IDE integration easier.

### Slow first import

The first import of haive packages can take a few seconds due to LangChain and transformer model loading. This is normal. Subsequent imports in the same process are fast.

---

## Quick Reference: Common Commands

```bash
# Install / update
poetry install --all-extras
git submodule update --init --recursive

# Run any Python with haive available
poetry run python your_script.py

# Run tests
poetry run pytest packages/haive-agents/tests/ -v
poetry run pytest packages/haive-games/tests/ -v

# Launch UI
poetry run streamlit run tools/haive-ui/src/haive_ui/app.py --server.port 8501

# Run a chess game
poetry run python packages/haive-games/src/haive/games/chess/example.py

# Run the full tournament
poetry run python packages/haive-games/tournament_tools/scripts/claude_vs_openai_final_tournament.py

# Check which LLM config is defaulting to
poetry run python -c "
from haive.core.engine.aug_llm.config import _create_default_llm_config
cfg = _create_default_llm_config()
print(type(cfg).__name__, getattr(cfg, 'model', ''))
"
```
