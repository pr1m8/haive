# Development Workflow - Haive Framework

**Version**: 1.0  
**Purpose**: Comprehensive development workflow and methodology  
**Last Updated**: 2025-01-09

## 🔄 Memory-Driven Development Process

### 1. Context Loading (Session Start)
```bash
# Read current context
cat CLAUDE.md                          # Main routing
cat project_docs/claude_sessions/current_issues.md  # Active issues
cat project_docs/progress_tracking/current_sprint.md  # Sprint status

# Load package-specific memory
cat project_docs/{package_name}/README.md

# Check git state
git status && git diff
```

### 2. Work Planning
```python
# Use TodoWrite for task management
from haive.core.utils.todo import TodoWrite

TodoWrite(todos=[
    {"content": "Specific task description", "status": "pending", "priority": "high"},
    {"content": "Another task", "status": "pending", "priority": "medium"}
])
```

### 3. Execution Standards
- **Apply Standards**: Follow @project_docs/CODING_STYLE_GUIDE.md
- **Document Decisions**: Update session memory in real-time
- **Test Continuously**: Use real components, no mocks
- **Update Progress**: Mark todos complete as you finish

### 4. Quality Assurance
```bash
# Before committing
poetry run pytest                      # All tests pass
poetry run ruff check                  # Code style
poetry run mypy                        # Type checking
```

## 🎯 Package Development Workflow

### Creating New Agents
```bash
# 1. Create module structure
mkdir -p packages/haive-agents/src/haive/agents/new_agent_type
touch packages/haive-agents/src/haive/agents/new_agent_type/{__init__.py,agent.py,config.py,state.py,example.py}

# 2. Run tests as you develop
poetry run pytest packages/haive-agents/tests/test_new_agent_type/ -v --lf

# 3. Check type safety
poetry run mypy packages/haive-agents/src/haive/agents/new_agent_type/
```

### Implementation Pattern
```python
# Step 1: Define State Schema
from haive.core.schema import StateSchema
from pydantic import Field
from typing import List, Dict, Any

class MyAgentState(StateSchema):
    """State schema for custom agent."""
    messages: List[str] = Field(default_factory=list)
    context: Dict[str, Any] = Field(default_factory=dict)
    custom_field: str = Field(default="")

# Step 2: Create Agent Class
from haive.agents.base import Agent
from haive.core.graph import BaseGraph

class MyCustomAgent(Agent[MyAgentState]):
    """Custom agent implementation."""

    def setup_agent(self) -> None:
        """Initialize agent components."""
        self._sync_fields_from_engine()
        self._setup_schemas()
        self._build_initial_graph()

    def build_graph(self) -> BaseGraph:
        """Define agent workflow."""
        graph = BaseGraph()
        graph.add_node("process", self._process_input)
        graph.add_node("respond", self._generate_response)
        graph.add_edge("process", "respond")
        graph.set_entry_point("process")
        return graph.compile()
```

## 🧪 Testing Workflow

### Test-First Development
```python
# 1. Write test first
def test_new_agent_processes_user_input():
    """Test new agent processes user input correctly."""
    agent = MyCustomAgent(name="test")
    result = agent.process("Hello world")
    assert result.response
    assert result.success

# 2. Implement to make test pass
# 3. Refactor while keeping tests green
```

### Real Component Testing
```python
# ALWAYS use real components
def test_react_agent_with_real_llm_and_tools():
    """Test ReactAgent with actual LLM and real tools."""
    agent = ReactAgent(
        name="test_agent",
        model="gpt-4",                      # Real LLM
        tools=["calculator", "web_search"]  # Real tools
    )

    result = agent.process("Calculate 15 * 23")
    assert "345" in str(result.response)
    assert result.conversation_history  # Real state saved
```

## 📊 Quality Metrics Tracking

### Code Quality
```bash
# Coverage tracking
poetry run pytest --cov=haive --cov-report=html

# Type coverage
poetry run mypy packages/ --strict

# Style compliance
poetry run ruff check packages/ --fix
```

### Performance Monitoring
```python
import time
from contextlib import asynccontextmanager

@asynccontextmanager
async def performance_monitor(operation_name: str):
    """Monitor operation performance."""
    start_time = time.time()
    try:
        yield
    finally:
        duration = time.time() - start_time
        logger.info(f"{operation_name} took {duration:.2f}s")
```

## 🔧 Common Development Tasks

### Debugging Schema Issues
```python
# Debug schema generation
from haive.core.schema import SchemaComposer

composer = SchemaComposer(base_state_schema=MyAgentState)
schema = composer.compose_state([engine1, engine2])
print(schema.schema())  # View full schema

# Check field conflicts
for field_name, field_info in schema.__fields__.items():
    print(f"{field_name}: {field_info.type_}")
```

### Tool Integration
```python
# Pattern 1: Direct tool assignment
from haive.core.tools import tool

@tool
def calculate(expression: str) -> float:
    """Calculate mathematical expression."""
    return eval(expression)  # Simplified example

# Pattern 2: Tool routing
tool_routes = {
    "calculate": "calculator_engine",
    "search": "search_engine",
    "default": "main_engine"
}
```

## 📝 Documentation Workflow

### Module Documentation
```python
"""Module summary in one line.

Detailed module description explaining purpose, main classes,
and usage patterns.

Examples:
    Basic usage::

        from mymodule import MyClass
        instance = MyClass(param="value")
        result = instance.method()
"""
```

### Function Documentation
```python
def process_data(data: List[Dict], threshold: float = 0.5) -> ProcessedResult:
    """Process input data using specified threshold.
    
    Args:
        data: List of dictionaries containing raw data points
        threshold: Minimum confidence score for filtering
        
    Returns:
        ProcessedResult: Object containing filtered data and metadata
        
    Raises:
        ValueError: If data is empty or malformed
        
    Examples:
        Basic processing::
        
            data = [{'value': 0.8, 'timestamp': '2023-01-01'}]
            result = process_data(data)
    """
```

## 🚨 Error Prevention

### Pre-commit Checklist
- [ ] All tests pass with real components
- [ ] No print statements (use logger.debug)
- [ ] Type hints on all public functions
- [ ] Docstrings in Google format
- [ ] No hardcoded secrets
- [ ] Explicit imports (from haive.core.*)
- [ ] Memory documentation updated

### Common Pitfalls
```python
# ❌ WRONG - Generic imports
from utils import helper
from engine import BaseEngine

# ✅ CORRECT - Explicit imports
from haive.core.utils import validate_input
from haive.core.engine import BaseEngine

# ❌ WRONG - Print statements
print("Debug info")

# ✅ CORRECT - Structured logging
logger.debug("Debug info", extra={"context": "value"})
```

## 🔄 Session Memory Management

### Session Creation
```bash
# Create new session workspace
session_id="claude_$(date +%Y%m%d_%H%M%S)_{purpose}"
mkdir -p "project_docs/claude_sessions/$session_id"/{memory,references}
```

### Progress Tracking
```markdown
# In session memory
## Current Focus
- Working on: [specific component]
- Issues encountered: [list]
- Decisions made: [list]
- Next steps: [list]

## Key Insights
- Pattern discovered: [description]
- Performance finding: [metrics]
- Integration challenge: [solution]
```

### Session Completion
```bash
# Archive completed session
mv "project_docs/claude_sessions/$session_id" "project_docs/claude_sessions/archive/"

# Update progress tracking
echo "Completed: $session_id" >> project_docs/progress_tracking/completed_sessions.md
```

## 📈 Continuous Improvement

### Learning Capture
- Document patterns that work
- Record solutions to common problems
- Update methodology based on experience
- Share insights across sessions

### Workflow Optimization
- Monitor task completion times
- Identify bottlenecks in development
- Refine testing strategies
- Improve memory organization

---

**Remember**: Consistent workflow leads to consistent quality. Follow the process, document your work, and continuously improve.