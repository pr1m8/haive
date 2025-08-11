# Haive Agents Examples

**Welcome to the Haive Agents examples!** This directory contains comprehensive examples showing how to build AI agents with the Haive framework.

## 🎯 Quick Start

**New to Haive?** Start here:

1. **[Getting Started](01_getting_started/)** - Your first agents
2. **[Single Agents](02_single_agents/)** - Core agent patterns
3. **[Multi-Agents](03_multi_agents/)** - Agent coordination

## 📚 Learning Path

### Beginner (Start Here!)

```
01_getting_started/
├── simple_agent_basic.py         # Your first agent
├── react_agent_with_tools.py     # Agent with tools
└── structured_output_basics.py   # Structured responses
```

### Intermediate

```
02_single_agents/                  # Single agent patterns
├── agent_with_hooks.py           # Pre/post processing
├── funky_prompt_templates.py     # Creative prompts
└── agent_with_memory.py          # Persistent memory

03_multi_agents/                   # Multi-agent workflows
├── sequential_workflow.py        # A → B → C execution
├── conditional_routing.py        # Smart routing
└── parallel_workflow.py          # Concurrent execution
```

### Advanced

```
04_specialized/                    # Domain-specific agents
├── rag_workflows/                 # Document Q&A
├── planning_agents/               # Strategic planning
└── research_agents/               # Information gathering

05_advanced/                       # Advanced patterns
├── meta_agent_patterns.py        # Self-modifying agents
└── enterprise_workflows.py       # Production patterns
```

## 🎪 Featured Examples

### 🎨 Creative Prompt Templates

**File**: `02_single_agents/funky_prompt_templates.py`

- Recipe generation with complex constraints
- Story writing with emotional arcs
- Code review with pattern matching
- Multi-modal data analysis

### 🌳 Smart Agent Routing

**File**: `03_multi_agents/conditional_routing.py`

- Query classification with confidence scores
- Automatic routing to specialist agents
- Type-safe structured outputs
- Clean branching logic

### 🧠 RAG Workflows

**File**: `04_specialized/rag_workflows/`

- Simple document Q&A
- Agentic RAG with grading
- Multi-agent document processing

## 🚀 Running Examples

All examples are self-contained and runnable:

```bash
# Navigate to examples
cd examples_new/

# Run any example
poetry run python 01_getting_started/simple_agent_basic.py
poetry run python 02_single_agents/funky_prompt_templates.py
poetry run python 03_multi_agents/conditional_routing.py
```

## 🎯 Example Categories

| Category            | Description               | Best For               |
| ------------------- | ------------------------- | ---------------------- |
| **Getting Started** | Basic agent creation      | First-time users       |
| **Single Agents**   | Individual agent patterns | Learning core concepts |
| **Multi-Agents**    | Agent coordination        | Building workflows     |
| **Specialized**     | Domain-specific solutions | Specific use cases     |
| **Advanced**        | Complex patterns          | Production systems     |
| **Integrations**    | External services         | Real-world deployment  |

## 📋 Example Standards

Every example follows these standards:

- **Self-contained**: Runs without external dependencies
- **Well-documented**: Clear comments and docstrings
- **Real LLM usage**: No mocks, actual AI interaction
- **Error handling**: Graceful failure and recovery
- **Logging suppression**: Clean output for demonstrations

## 🔗 Related Resources

- **[Demos](../demos/)** - Complete applications
- **[Tests](../tests/)** - Testing patterns
- **[Experiments](../experiments/)** - Research and exploration
- **[Documentation](../docs/)** - Comprehensive guides

## 🤝 Contributing Examples

Want to add an example? Follow these guidelines:

1. **Choose the right category** based on complexity and purpose
2. **Include comprehensive docstrings** explaining the pattern
3. **Add real LLM integration** - no mocks or fake responses
4. **Test thoroughly** before submitting
5. **Reference related examples** for cross-learning

### Example Template

```python
#!/usr/bin/env python3
"""Short Description - What This Example Demonstrates.

Detailed explanation of the pattern, when to use it, and key concepts.
Explain any prerequisites or background knowledge needed.

Key Features:
- Feature 1 with explanation
- Feature 2 with explanation
- Feature 3 with explanation

Date: Current date
"""

import asyncio
# ... imports

async def main():
    \"\"\"Demonstrate the main pattern.\"\"\"

    print("🎯 Example Name")
    print("=" * 50)

    # Implementation with clear steps

    print("\\n✅ Example completed!")
    print("\\n💡 Key Takeaways:")
    print("1. Takeaway 1")
    print("2. Takeaway 2")

if __name__ == "__main__":
    # Suppress logging for clean demo
    import logging
    import os
    logging.getLogger().setLevel(logging.CRITICAL)
    os.environ["HAIVE_LOG_LEVEL"] = "CRITICAL"

    asyncio.run(main())
```

## 🎨 Example Showcase

### Most Popular Examples

1. **Funky Prompt Templates** - Creative state field usage
2. **Conditional Routing** - Smart agent coordination
3. **Sequential Workflows** - ReactAgent → SimpleAgent patterns

### Recently Added

- Dynamic branching with parallel execution
- Memory-first routing patterns
- Custom validation node examples

### Coming Soon

- Enterprise deployment patterns
- Performance optimization techniques
- Advanced memory management

---

**Happy coding with Haive!** 🚀

Start with `01_getting_started/` and work your way through the examples. Each directory builds on the previous concepts while introducing new patterns and capabilities.
