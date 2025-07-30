# Multi-Agent Module Structure

This document describes the reorganized structure of the multi-agent module.

## Current Implementation (Use This)

- **`clean.py`** - The current, clean multi-agent implementation
- **`__init__.py`** - Exports MultiAgent from clean.py

## Directory Structure

```
multi/
├── clean.py                    # ✅ CURRENT IMPLEMENTATION
├── __init__.py                 # ✅ CURRENT EXPORTS
├── README.md                   # General documentation
├── README_STRUCTURE.md         # This file
├── MULTI_AGENT_GUIDE.md       # Comprehensive guide
├── README_COMPREHENSIVE.md    # Detailed documentation
│
├── archive/                    # 📁 OLD IMPLEMENTATIONS
│   ├── agent.py               # Original complex implementation
│   ├── base.py                # Complex base with SequentialAgent, etc.
│   ├── configurable_base.py   # Configurable variant
│   ├── enhanced_base.py       # Enhanced variant
│   └── example.py             # Original examples
│
├── experiments/                # 📁 EXPERIMENTAL WORK
│   ├── implementations/       # Alternative implementations
│   │   ├── clean_base.py      # Clean base attempt
│   │   ├── clean_multi_agent.py # First clean attempt
│   │   ├── proper_base.py     # Proper base attempt
│   │   ├── multi_agent_v2.py  # Version 2 experiment
│   │   ├── compatibility_enhanced_base.py # Compatibility layer
│   │   ├── debug_with_logging.py # Debug version
│   │   ├── simple_debug.py    # Simple debug version
│   │   └── self_discover_state.py # Self-discover state
│   └── test_proper_usage.py   # Usage tests
│
└── sequential/                 # 📁 SEQUENTIAL SPECIFIC
    ├── __init__.py
    ├── agent.py               # Sequential agent implementation
    └── README.md
```

## Usage

Use the clean implementation:

```python
from haive.agents.multi import MultiAgent

# Create multi-agent system
agents = [agent1, agent2, agent3]
multi = MultiAgent(
    name="my_system",
    agents=agents,
    execution_mode="sequential"
)

# Or use the factory method
multi = MultiAgent.create(
    agents=agents,
    name="my_system",
    execution_mode="sequential"
)
```

## Development History

1. **Original Implementation** (`agent.py`, `base.py`) - Complex, feature-rich but difficult to use
2. **Experimental Phase** - Multiple attempts at cleaner implementations
3. **Current Implementation** (`clean.py`) - Simple, focused, working solution

## Migration Notes

- Old imports from `haive.agents.multi.base` will break
- Use `from haive.agents.multi import MultiAgent` instead
- The clean implementation provides simpler configuration
- Complex routing patterns moved to BaseGraph intelligent routing

## Testing

The current implementation has been tested and verified to work with:

- Sequential execution
- Agent list and dict initialization
- Real LLM execution (no mocks)
- Proper state management
