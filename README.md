# Haive - AI Agent Framework

A powerful, modular framework for building sophisticated AI agents with advanced capabilities including planning, reasoning, tool usage, and multi-agent collaboration.

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/haive.git
cd haive/backend/haive

# Install Poetry (if not installed)
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install --all-extras

# Activate virtual environment
poetry shell

# Run tests to verify installation
poetry run pytest

# Build documentation
poetry run nox -s docs_fast
```

## 📋 Overview

Haive is a comprehensive AI agent framework that provides:

- **🤖 Pre-built Agents**: SimpleAgent, ReactAgent, PlannerAgent, and more
- **🔧 Tool Integration**: Easy integration with external tools and APIs
- **🧠 Advanced Reasoning**: Chain-of-thought, self-reflection, and planning capabilities
- **👥 Multi-Agent Systems**: Coordinate multiple agents for complex workflows
- **💾 State Management**: Persistent state and memory systems
- **🎮 Game Environments**: Built-in game agents and environments
- **📊 Data Processing**: Streaming and batch data processing capabilities

## 🏗️ Architecture

Haive is organized as a monorepo with multiple packages:

```
packages/
├── haive-core/      # Core framework and infrastructure
├── haive-agents/    # Pre-built agent implementations
├── haive-tools/     # Tool integrations and utilities
├── haive-games/     # Game environments and agents
├── haive-dataflow/  # Data processing pipelines
├── haive-mcp/       # Model Context Protocol integration
└── haive-prebuilt/  # Ready-to-use configurations
```

## 💻 Basic Usage

### Simple Agent Example

```python
from haive.agents.simple.agent_v3 import SimpleAgentV3
from haive.core.engine.aug_llm import AugLLMConfig

# Create an agent
agent = SimpleAgentV3(
    name="assistant",
    engine=AugLLMConfig(
        temperature=0.7,
        system_message="You are a helpful assistant."
    )
)

# Execute
result = agent.run("What is the capital of France?")
print(result)
```

### React Agent with Tools

```python
from haive.agents.react.agent import ReactAgent
from langchain_core.tools import tool

@tool
def calculator(expression: str) -> str:
    """Calculate mathematical expressions."""
    return str(eval(expression))

# Create agent with tools
agent = ReactAgent(
    name="math_agent",
    engine=AugLLMConfig(),
    tools=[calculator]
)

# Execute with tool usage
result = agent.run("What is 25 * 37?")
```

### Multi-Agent System

```python
from haive.agents.multi.enhanced_multi_agent_v4 import EnhancedMultiAgentV4

# Create a multi-agent workflow
workflow = EnhancedMultiAgentV4([
    PlannerAgent(name="planner"),
    ResearchAgent(name="researcher"),
    WriterAgent(name="writer")
], mode="sequential")

# Execute complex task
result = workflow.run("Create a report on AI trends")
```

## 📚 Documentation

- **Full Documentation**: Run `poetry run nox -s docs_serve` and visit http://localhost:8000
- **Project Docs**: See `project_docs/` for architecture and design documents
- **Memory Index**: `project_docs/memory_index/` for development patterns and solutions
- **CLAUDE.md**: Central development hub with patterns and guidelines

## 🧪 Testing

```bash
# Run all tests
poetry run pytest

# Run specific package tests
poetry run pytest packages/haive-agents/tests/

# Run with coverage
poetry run pytest --cov=haive --cov-report=html

# Run specific test
poetry run pytest -k "test_simple_agent"
```

## 🛠️ Development

### Environment Setup

```bash
# VS Code users: Automatic setup
./.vscode/setup-environment.sh

# Manual setup
poetry install --all-extras
poetry shell
```

### Code Quality

```bash
# Run linters
poetry run ruff check .

# Type checking
poetry run mypy packages/

# Format code
poetry run black .

# All checks
poetry run nox -s lint
```

### Common Tasks

```bash
# Build documentation
poetry run nox -s docs

# Clean project
poetry run nox -s clean

# Update dependencies
poetry update
```

## 🎯 Key Features

### 1. Flexible Agent Types
- **SimpleAgent**: Basic LLM-powered agent
- **ReactAgent**: Reasoning and tool usage
- **PlannerAgent**: Strategic planning
- **RAGAgent**: Retrieval-augmented generation
- **MultiAgent**: Agent coordination

### 2. Advanced Capabilities
- **Structured Output**: Pydantic model outputs
- **Memory Systems**: Short and long-term memory
- **Tool Integration**: Easy tool creation and usage
- **State Management**: Persistent conversation state
- **Async Support**: Full async/await compatibility

### 3. Production Ready
- **No Mocks Testing**: Real component testing
- **Type Safety**: Full type hints and validation
- **Error Handling**: Comprehensive error management
- **Performance**: Optimized for production use
- **Extensible**: Easy to extend and customize

## 📖 Examples

Find examples in the `examples/` directory:
- `simple_agent_example.py` - Basic agent usage
- `react_agent_tools.py` - Tool integration
- `multi_agent_workflow.py` - Complex workflows
- `rag_agent_example.py` - RAG implementation
- `game_agent_example.py` - Game playing agents

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`poetry run pytest`)
5. Commit your changes (`git commit -m 'feat: add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Development Guidelines
- Follow the coding standards in `project_docs/active/standards/`
- No mock testing - use real components
- Include tests for new features
- Update documentation as needed
- Use conventional commits

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔗 Resources

- **GitHub**: [github.com/yourusername/haive](https://github.com/yourusername/haive)
- **Documentation**: [haive.readthedocs.io](https://haive.readthedocs.io)
- **Issues**: [GitHub Issues](https://github.com/yourusername/haive/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/haive/discussions)

## 🙏 Acknowledgments

Built with:
- [LangChain](https://langchain.com/) - LLM application framework
- [Pydantic](https://pydantic-docs.helpmanual.io/) - Data validation
- [Poetry](https://python-poetry.org/) - Dependency management
- [Sphinx](https://www.sphinx-doc.org/) - Documentation generation

---

**Note**: This is an active development project. APIs may change. Check CHANGELOG.md for updates.