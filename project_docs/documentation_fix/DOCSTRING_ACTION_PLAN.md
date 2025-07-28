# AutoAPI Docstring Fix Action Plan

Prioritized plan for fixing the most critical documentation issues for AutoAPI generation.

## Strategy

1. **Phase 1**: Fix highest-impact core modules (haive-core foundation)
2. **Phase 2**: Fix main user-facing APIs (haive-agents)
3. **Phase 3**: Complete remaining public APIs

## Phase 1: Critical Core Infrastructure (haive-core)

Focus on the foundation that all other packages depend on:

### Top Priority haive-core Issues

#### packages/haive-core/src/haive/core/engine/agent/persistence/base.py (Priority: 118)

- Line 1: module `base` (score: 118)

#### packages/haive-core/src/haive/core/engine/agent/persistence/factory.py (Priority: 118)

- Line 1: module `factory` (score: 118)

#### packages/haive-core/src/haive/core/engine/agent/persistence/handlers.py (Priority: 118)

- Line 1: module `handlers` (score: 118)

#### packages/haive-core/src/haive/core/engine/agent/persistence/integration.py (Priority: 118)

- Line 1: module `integration` (score: 118)

#### packages/haive-core/src/haive/core/engine/agent/persistence/memory_config.py (Priority: 118)

- Line 1: module `memory_config` (score: 118)

#### packages/haive-core/src/haive/core/engine/agent/persistence/mongodb_config.py (Priority: 118)

- Line 1: module `mongodb_config` (score: 118)

#### packages/haive-core/src/haive/core/engine/agent/persistence/postgres_config.py (Priority: 118)

- Line 1: module `postgres_config` (score: 118)

#### packages/haive-core/src/haive/core/engine/agent/persistence/types.py (Priority: 118)

- Line 1: module `types` (score: 118)

#### packages/haive-core/src/haive/core/engine/agent/utils/input_handling.py (Priority: 118)

- Line 1: module `input_handling` (score: 118)

#### packages/haive-core/src/haive/core/engine/document/base/schema.py (Priority: 118)

- Line 1: module `schema` (score: 118)

## Phase 2: Main User APIs (haive-agents)

Focus on the main user-facing agent classes:

#### packages/haive-agents/src/haive/agents/simple/enhanced_simple_minimal.py (Priority: 208)

- Line 14: class `Engine` (score: 104)
- Line 18: class `AugLLMConfig` (score: 104)

#### packages/haive-agents/src/haive/agents/simple/.ipynb_checkpoints/agent-checkpoint.py (Priority: 109)

- Line 1: module `agent-checkpoint` (score: 109)

#### packages/haive-agents/src/haive/agents/simple/agent.py (Priority: 109)

- Line 1: module `agent` (score: 109)

#### packages/haive-agents/src/haive/agents/simple/debug.py (Priority: 109)

- Line 1: module `debug` (score: 109)

#### packages/haive-agents/src/haive/agents/simple/state.py (Priority: 109)

- Line 1: module `state` (score: 109)

#### packages/haive-agents/src/haive/agents/simple/structured/agent.py (Priority: 109)

- Line 1: module `agent` (score: 109)

#### packages/haive-agents/src/haive/agents/simple/structured/config.py (Priority: 109)

- Line 1: module `config` (score: 109)

#### packages/haive-agents/src/haive/agents/simple/v2/graph.py (Priority: 109)

- Line 1: module `graph` (score: 109)

## Package Priority Summary

Total issues by package (sorted by cumulative priority):

- **haive-core**: 4073 issues (total priority: 410939, high-priority: 4073)
- **haive-agents**: 4665 issues (total priority: 366204, high-priority: 4665)
- **haive-games**: 2047 issues (total priority: 90820, high-priority: 277)
- **haive-dataflow**: 640 issues (total priority: 22175, high-priority: 0)
- **haive-mcp**: 397 issues (total priority: 20998, high-priority: 198)
- **haive-prebuilt**: 475 issues (total priority: 12807, high-priority: 0)

## Implementation Guidelines

### Google-Style Docstring Template

Use this template for all new docstrings:

```python
def example_function(param1: str, param2: int = 10) -> bool:
    """One-line summary of what the function does.

    Longer description explaining the purpose, algorithm,
    or implementation details if needed.

    Args:
        param1: Description of param1 and its purpose.
        param2: Description of param2 (default: 10).

    Returns:
        Description of what the function returns.

    Raises:
        ValueError: If param1 is empty.
        TypeError: If param2 is not an integer.

    Examples:
        Basic usage::

            result = example_function("hello", 20)
            assert result is True
    """
```

### Module Docstring Template

```python
"""Module for handling specific functionality.

This module provides classes and functions for [specific purpose].
It is designed to work with [related systems] and supports
[key features].

Key Classes:
    MainClass: Primary interface for [functionality]
    HelperClass: Utility class for [specific tasks]

Key Functions:
    main_function: Primary function for [purpose]
    utility_function: Helper function for [specific task]

Examples:
    Basic usage::

        from module import MainClass
        instance = MainClass()
        result = instance.main_method()
"""
```

### Class Docstring Template

```python
class ExampleClass:
    """One-line summary of the class purpose.

    Detailed description of what the class does,
    its role in the system, and key concepts.

    Attributes:
        attr1: Description of public attribute.
        attr2: Description of another attribute.

    Examples:
        Basic usage::

            instance = ExampleClass(param="value")
            result = instance.method()

    Note:
        Any important notes about usage, thread-safety,
        or integration with other components.
    """
```

## Next Steps

1. **Start with Phase 1** - Fix the top 10 haive-core files
2. **Focus on modules first** - Module docstrings have highest AutoAPI impact
3. **Then classes** - Class docstrings define the main API structure
4. **Finally methods** - Complete the public method documentation
5. **Test AutoAPI generation** - Verify docs build correctly after each phase

Remember: AutoAPI depends heavily on module and class docstrings for navigation and structure!
