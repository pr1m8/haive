# ReWOO (Reasoning Without Observation)

Evidence-based planning pattern that separates planning from execution for complex reasoning tasks.

## Overview

ReWOO implements a planning approach where:

1. **Plan First**: Create a complete plan with evidence requirements
2. **Collect Evidence**: Systematically gather information based on dependencies
3. **Reason**: Use collected evidence to reach conclusions

This pattern is ideal for multi-step reasoning tasks that require gathering information from multiple sources.

## Key Components

- **Evidence**: Information pieces with dependencies (#E1, #E2, etc.)
- **ReWOOPlan**: Plan containing evidence steps and dependencies
- **ReWOOState**: State extending ToolState with evidence tracking
- **ToolCall**: Smart tool execution with evidence resolution
- **ReWOOToolExecutor**: Executes tools and manages evidence collection

## Installation

This module is part of the `haive-agents` package. Install it using:

```bash
pip install haive-agents
```

## Usage Examples

### Basic Usage

```python
from haive.agents.planning.rewoo import ReWOOState, ReWOOPlan
from haive.agents.planning.rewoo.tool_integration import ReWOOToolExecutor

# Initialize state with tools
state = ReWOOState(
    objective="Research the economic impact of AI",
    tools=[search_tool, analyze_tool]
)

# Create evidence-based plan
plan = ReWOOPlan(
    name="ai_economic_research",
    objective=state.objective
)

# Define evidence steps
plan.add_rewoo_step(
    name="find_studies",
    evidence_id="#E1",
    evidence_description="Recent AI economic studies",
    tool_name="search",
    tool_args={"query": "AI economic impact studies 2024"}
)

plan.add_rewoo_step(
    name="analyze_data",
    evidence_id="#E2",
    evidence_description="Analysis of economic data",
    tool_name="analyze",
    tool_args={"data": "#E1", "method": "summary"},
    depends_on=["#E1"]  # Depends on search results
)

# Execute plan
executor = ReWOOToolExecutor(state)
state.plan = plan

# Collect evidence
while not state.is_evidence_complete:
    for evidence in state.ready_evidence:
        result = await executor.execute_evidence_collection(evidence)

# Get final reasoning
context = state.get_evidence_context()
```

## API Reference

For detailed API documentation, see the [API Reference](../../../docs/source/api/rewoo/index.rst).

## See Also

- [Planning Base Models](../models/base.py)
- [ToolState Documentation](../../../../haive-core/src/haive/core/schema/prebuilt/tool_state.py)
- [LLM Compiler Pattern](../llm_compiler/)
