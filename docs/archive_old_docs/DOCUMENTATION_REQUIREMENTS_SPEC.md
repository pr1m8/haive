# Haive Documentation Requirements Specification

**Version**: 1.0  
**Purpose**: Comprehensive specification for achieving 0 warnings and professional documentation  
**Last Updated**: 2025-07-18

## 🎯 Overview

This document specifies EXACTLY what needs to be documented and HOW it should be documented to achieve:

1. **0 Sphinx warnings**
2. **Complete API documentation**
3. **Runnable examples**
4. **Professional developer experience**

---

## 📋 Priority 1: Missing Core Documentation Files

### 1.1 Tool Documentation Structure

**MUST CREATE these files:**

```
docs/source/api/tools/
├── index.rst           # Tool API overview
├── base.rst            # Base tool classes
├── builtin.rst         # Built-in tools
└── toolkits/
    └── index.rst       # Toolkit documentation
```

**Content Requirements for `api/tools/index.rst`:**

```rst
Tool API Reference
==================

.. automodule:: haive.tools
   :members:
   :undoc-members:
   :show-inheritance:

Base Classes
------------

.. toctree::
   :maxdepth: 2

   base
   builtin
   toolkits/index
```

### 1.2 Missing Guide Files

**MUST CREATE:**

- `docs/source/guides/advanced_patterns.rst`
- `docs/source/guides/performance.rst`
- `docs/source/guides/mcp_integration.rst`
- `docs/source/guides/tool_composition.rst`

**Each guide MUST include:**

1. Overview section
2. Prerequisites
3. 3+ code examples
4. Common patterns
5. Troubleshooting
6. API reference links

---

## 📝 Priority 2: Module Documentation Standards

### 2.1 Module-Level Docstrings

**EVERY Python module (`__init__.py`) MUST have:**

```python
"""
Module one-line summary.

Detailed description of what this module provides, its purpose,
and how it fits into the larger system.

Key Components:
    - ComponentA: Brief description
    - ComponentB: Brief description

Example:
    Basic usage example::

        from haive.tools import Calculator
        calc = Calculator()
        result = calc.add(2, 3)

See Also:
    - :mod:`haive.agents`: Agent implementations
    - :mod:`haive.core`: Core functionality

Note:
    Important usage notes or warnings.
"""

from .base import BaseTool
from .calculator import Calculator

__all__ = ["BaseTool", "Calculator"]  # REQUIRED: explicit exports
```

### 2.2 Class Documentation

**EVERY class MUST have:**

```python
class Calculator(BaseTool):
    """Single-line summary of the class.

    Detailed description of the class purpose, behavior,
    and usage patterns. Include design decisions if relevant.

    Args:
        name: Tool identifier used in agent systems
        description: Human-readable description for LLMs
        precision: Number of decimal places (default: 2)

    Attributes:
        operations (List[str]): Supported operations
        history (List[Dict]): Calculation history

    Example:
        Basic usage::

            calc = Calculator(name="math_tool", precision=4)
            result = calc.add(2.5, 3.7)
            print(result)  # 6.2000

        With agent integration::

            agent = SimpleAgent(
                tools=[Calculator(name="calc")]
            )

    Note:
        This tool is stateful and maintains calculation history.

    .. versionadded:: 0.2.0
    .. versionchanged:: 0.3.0
       Added support for complex numbers
    """
```

### 2.3 Method Documentation

**EVERY public method MUST have:**

```python
def calculate(
    self,
    expression: str,
    variables: Optional[Dict[str, float]] = None,
    timeout: float = 5.0
) -> Union[float, complex]:
    """Calculate mathematical expression with variable substitution.

    Evaluates a mathematical expression string with optional variable
    substitution. Supports basic arithmetic, trigonometry, and complex
    numbers.

    Args:
        expression: Mathematical expression to evaluate.
            Supports operators: +, -, *, /, **, %, //
            Functions: sin, cos, tan, log, sqrt, etc.
        variables: Variable name to value mapping.
            Example: {"x": 5, "y": 10}
        timeout: Maximum execution time in seconds.

    Returns:
        Calculated result as float or complex number.

    Raises:
        ValueError: If expression is invalid or contains forbidden operations.
        TimeoutError: If calculation exceeds timeout.
        ZeroDivisionError: If expression contains division by zero.

    Example:
        Simple calculation::

            result = calc.calculate("2 + 2")
            assert result == 4.0

        With variables::

            result = calc.calculate(
                "x**2 + y",
                variables={"x": 3, "y": 5}
            )
            assert result == 14.0

    Warning:
        This method uses eval() internally. Only pre-validated
        expressions should be passed.

    .. seealso::
       :meth:`validate_expression` for expression validation
       :meth:`add`, :meth:`multiply` for simple operations
    """
```

---

## 🔧 Priority 3: Type Hints Requirements

### 3.1 Complete Type Coverage

**EVERY function/method parameter and return MUST have type hints:**

```python
from typing import (
    Dict, List, Optional, Union, Tuple, Any,
    Callable, TypeVar, Generic, Protocol, Literal,
    overload
)
from typing_extensions import TypedDict, NotRequired
from collections.abc import Sequence, Mapping

T = TypeVar('T')

class ToolResult(TypedDict):
    """Typed dictionary for tool results."""
    success: bool
    output: Any
    error: NotRequired[str]
    metadata: NotRequired[Dict[str, Any]]

@overload
def process_input(data: str) -> str: ...

@overload
def process_input(data: List[str]) -> List[str]: ...

def process_input(
    data: Union[str, List[str]]
) -> Union[str, List[str]]:
    """Process input with overloaded signatures."""
    ...
```

### 3.2 Generic Types

```python
class Store(Generic[T]):
    """Generic store for any type.

    Type Parameters:
        T: The type of items stored
    """

    def add(self, item: T) -> None:
        """Add item of type T."""
        ...

    def get(self, index: int) -> Optional[T]:
        """Get item by index, None if not found."""
        ...
```

---

## 📂 Priority 4: Package Structure Requirements

### 4.1 Package README.md

**EVERY package MUST have `README.md` with:**

````markdown
# haive-tools

Tool implementations for the Haive AI Agent Framework.

## Overview

This package provides tool implementations that agents can use to interact
with external systems, perform calculations, and access APIs.

## Installation

```bash
pip install haive-tools
```
````

## Quick Start

```python
from haive.tools import Calculator, WebSearch, FileReader

# Create tools
calc = Calculator()
search = WebSearch(api_key="...")

# Use with agents
from haive.agents import ReactAgent
agent = ReactAgent(tools=[calc, search])
```

## Available Tools

| Tool       | Description             | Requirements     |
| ---------- | ----------------------- | ---------------- |
| Calculator | Mathematical operations | None             |
| WebSearch  | Internet search         | API key          |
| FileReader | File system access      | File permissions |

## Creating Custom Tools

```python
from haive.tools import BaseTool

class MyTool(BaseTool):
    """Custom tool implementation."""

    def _run(self, input: str) -> str:
        """Tool logic here."""
        return f"Processed: {input}"
```

## API Reference

See the [API documentation](https://haive.readthedocs.io/api/tools).

## Examples

- [Basic Calculator](examples/calculator_basic.py)
- [Advanced Search](examples/search_advanced.py)
- [Custom Tool](examples/custom_tool.py)

## Contributing

See [CONTRIBUTING.md](../../CONTRIBUTING.md)

```

### 4.2 Example Files Structure

**EVERY package MUST have `examples/` directory:**

```

packages/haive-tools/
├── examples/
│ ├── **init**.py
│ ├── README.md
│ ├── calculator_basic.py # Simple example
│ ├── calculator_advanced.py # Complex example
│ ├── integration_agent.py # Integration example
│ └── requirements.txt # Example dependencies

````

**Example File Requirements:**

```python
#!/usr/bin/env python3
"""
Calculator Tool Basic Example

This example demonstrates basic usage of the Calculator tool
for simple mathematical operations.

Requirements:
    - haive-tools >= 0.2.0

Usage:
    python calculator_basic.py

Expected Output:
    Addition: 10.0
    Complex: 14.0
    History: [...]
"""

from haive.tools import Calculator


def main():
    """Run calculator examples."""
    # Create calculator with configuration
    calc = Calculator(
        name="math_helper",
        description="Performs mathematical calculations",
        precision=2
    )

    # Example 1: Simple addition
    print("Example 1: Simple Addition")
    result = calc.add(5, 5)
    print(f"5 + 5 = {result}")

    # Example 2: Complex expression
    print("\nExample 2: Complex Expression")
    result = calc.calculate("2**3 + 6")
    print(f"2^3 + 6 = {result}")

    # Example 3: With variables
    print("\nExample 3: Variables")
    result = calc.calculate(
        "x * y + z",
        variables={"x": 2, "y": 3, "z": 8}
    )
    print(f"x * y + z = {result} (x=2, y=3, z=8)")

    # Show calculation history
    print("\nCalculation History:")
    for entry in calc.history:
        print(f"  - {entry['expression']} = {entry['result']}")


if __name__ == "__main__":
    main()
````

---

## 🧪 Priority 5: Test Documentation

### 5.1 Test Docstrings

**EVERY test MUST have descriptive docstrings:**

```python
class TestCalculator:
    """Test suite for Calculator tool.

    Tests cover basic operations, error handling, and edge cases.
    """

    def test_addition_with_positive_numbers(self):
        """Test addition of two positive numbers returns correct sum."""
        calc = Calculator()
        assert calc.add(2, 3) == 5

    def test_calculate_handles_division_by_zero(self):
        """Test calculate raises ZeroDivisionError for division by zero.

        Validates that:
        1. Exception is raised
        2. Exception message is descriptive
        3. Calculator state remains valid
        """
        calc = Calculator()
        with pytest.raises(ZeroDivisionError) as exc_info:
            calc.calculate("1/0")
        assert "division by zero" in str(exc_info.value)
        assert calc.is_valid  # State not corrupted
```

---

## 🏗️ Priority 6: Sphinx Documentation Structure

### 6.1 Missing RST Files to Create

```
docs/source/
├── api/
│   ├── tools/
│   │   ├── index.rst         # CREATE: Tool API overview
│   │   ├── base.rst          # CREATE: Base classes
│   │   └── toolkits/
│   │       └── index.rst     # CREATE: Toolkit docs
│   └── examples/
│       └── tools/
│           └── index.rst     # CREATE: Tool examples
├── guides/
│   ├── advanced_patterns.rst # CREATE: Advanced usage
│   ├── performance.rst       # CREATE: Performance guide
│   ├── mcp_integration.rst   # CREATE: MCP guide
│   └── tool_composition.rst  # CREATE: Composition patterns
```

### 6.2 Auto-generated Examples Fix

**In `conf.py`, fix Sphinx Gallery configuration:**

```python
sphinx_gallery_conf = {
    "examples_dirs": [
        "../../packages/haive-agents/examples",  # MUST exist
        "../../packages/haive-tools/examples",   # MUST exist
    ],
    "gallery_dirs": [
        "auto_examples/agents",  # Output location
        "auto_examples/tools",
    ],
    "filename_pattern": r"/[^_].*\.py$",  # Exclude _*.py
    "ignore_pattern": r"__init__\.py",
    "download_all_examples": True,
}
```

---

## 📊 Priority 7: API Documentation Generation

### 7.1 AutoAPI Configuration

**Ensure ALL packages are included:**

```python
# conf.py
autoapi_dirs = [
    "../../packages/haive-core/src",
    "../../packages/haive-agents/src",
    "../../packages/haive-tools/src",    # ADD if missing
    "../../packages/haive-games/src",    # ADD if missing
    "../../packages/haive-mcp/src",      # ADD if missing
]

autoapi_options = [
    "members",
    "undoc-members",      # Document even without docstrings
    "show-inheritance",   # Show class inheritance
    "show-module-summary", # Module summaries
    "imported-members",   # Include imported members
    "special-members",    # Include __init__, etc.
]
```

---

## 🎨 Priority 8: Code Quality Standards

### 8.1 Docstring Linting

**Use these tools to enforce standards:**

```bash
# pyproject.toml
[tool.ruff]
select = [
    "D",    # pydocstyle
    "E",    # pycodestyle errors
    "F",    # pyflakes
    "I",    # isort
    "N",    # pep8-naming
    "ANN",  # flake8-annotations
]

[tool.ruff.pydocstyle]
convention = "google"  # Enforce Google style

[tool.mypy]
strict = true
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
```

### 8.2 Pre-commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.5
    hooks:
      - id: ruff
        args: [--fix]

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.7.0
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
```

---

## ✅ Acceptance Criteria

Documentation is complete when:

1. **Sphinx builds with 0 warnings**
2. **All public APIs have docstrings**
3. **All parameters have type hints**
4. **Every package has README.md**
5. **Every package has 3+ examples**
6. **AutoAPI generates for all packages**
7. **All cross-references resolve**
8. **Tests have descriptive names/docstrings**

---

## 🚀 Implementation Order

1. **Fix references** - Create stub files for missing docs
2. **Add type hints** - Start with haive.tools package
3. **Write docstrings** - Focus on public APIs first
4. **Create examples** - One basic example per tool
5. **Update READMEs** - Package-level documentation
6. **Run validation** - `ruff check`, `mypy`, `sphinx-build`

---

## 📚 Resources

- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)
- [Sphinx Napoleon](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html)
- [Type Hints PEP 484](https://peps.python.org/pep-0484/)
- [AutoAPI Documentation](https://sphinx-autoapi.readthedocs.io/)

---

**Remember**: Good documentation is an investment. It reduces support burden, speeds onboarding, and improves code quality.
