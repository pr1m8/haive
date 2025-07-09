# Corrected LTM Conditional Edges & Flow Design

## Overview

After analyzing the actual Haive agent patterns, particularly the SimpleAgent's implementation, I need to correct my understanding of conditional edges and design a proper LTM workflow that follows LangGraph conventions.

## Key Insights from SimpleAgent Analysis

### 1. **Actual Conditional Edge Pattern**

```python
# From SimpleAgent - lines 405-407
graph.add_conditional_edges(
    "agent_node",
    has_tool_calls,          # Condition function
    {True: "validation", False: END}  # Route mapping
)
```

### 2. **Simple Condition Functions**

```python
# From SimpleAgent - lines 26-37
def has_tool_calls(state) -> bool:
    """Check if the last AI message has tool calls."""
    if not hasattr(state, "messages") or not state.messages:
        return False

    last_msg = state.messages[-1]
    if not isinstance(last_msg, AIMessage):
        return False

    tool_calls = getattr(last_msg, "tool_calls", None)
    return bool(tool_calls)
```

### 3. **Validation Node Pattern**

```python
# From SimpleAgent - lines 424
graph.add_conditional_edges("validation", validation_config, routing_map)
```

## Corrected LTM Conditional Edge Design

### 1. **LTM State Schema**

```python
from typing import List, Dict, Any, Optional
from langchain_core.messages import AnyMessage
from pydantic import BaseModel

class LTMState(BaseModel):
    """LTM Agent State following Haive patterns."""

    # Core message state (required by LangGraph)
    messages: List[AnyMessage] = []

    # Processing control
    processing_stage: str = "extract"  # extract -> kg -> categorize -> consolidate -> store -> tools
    processing_complete: bool = False

    # Memory data
    extracted_memories: List[Dict[str, Any]] = []
    knowledge_graph: Optional[Dict[str, Any]] = None
    categories: List[str] = []
    consolidated_memories: List[Dict[str, Any]] = []

    # Processing results
    processing_errors: List[str] = []
    tool_calls_needed: bool = False
    reflection_scheduled: bool = False

    # Quality metrics
    extraction_quality: float = 0.0
    processing_quality: float = 0.0

    # Configuration
    enable_kg_processing: bool = True
    enable_categorization: bool = True
    enable_consolidation: bool = True
    enable_reflection: bool = True
```

### 2. **Simple Condition Functions (Following SimpleAgent Pattern)**

```python
def needs_kg_processing(state: LTMState) -> bool:
    """Check if KG processing is needed."""
    return (
        state.enable_kg_processing and
        bool(state.extracted_memories) and
        not state.knowledge_graph and
        len(state.extracted_memories) >= 2
    )

def needs_categorization(state: LTMState) -> bool:
    """Check if categorization is needed."""
    return (
        state.enable_categorization and
        bool(state.extracted_memories) and
        not state.categories and
        len(state.extracted_memories) >= 3
    )

def needs_consolidation(state: LTMState) -> bool:
    """Check if consolidation is needed."""
    return (
        state.enable_consolidation and
        bool(state.extracted_memories) and
        len(state.extracted_memories) >= 5
    )

def has_processing_errors(state: LTMState) -> bool:
    """Check if there are critical processing errors."""
    return len(state.processing_errors) > 0

def needs_tool_activation(state: LTMState) -> bool:
    """Check if memory tools should be activated."""
    return state.tool_calls_needed

def extraction_succeeded(state: LTMState) -> bool:
    """Check if memory extraction succeeded."""
    return bool(state.extracted_memories)

def processing_complete(state: LTMState) -> bool:
    """Check if all processing is complete."""
    return state.processing_complete
```

### 3. **LTM Graph with Proper Conditional Edges**

```python
class LTMAgent(Agent):
    """Long-Term Memory Agent with proper conditional edges."""

    def build_graph(self) -> BaseGraph:
        """Build LTM graph with proper conditional edge patterns."""
        graph = BaseGraph(name=self.name)

        # ============================================================================
        # NODES
        # ============================================================================

        # Memory extraction
        graph.add_node("extract_memories", self.extract_memories_node)

        # Processing nodes
        graph.add_node("process_kg", self.process_kg_node)
        graph.add_node("categorize_memories", self.categorize_memories_node)
        graph.add_node("consolidate_memories", self.consolidate_memories_node)

        # Storage and tools
        graph.add_node("store_memories", self.store_memories_node)
        graph.add_node("memory_tools", self.memory_tools_node)

        # Error handling
        graph.add_node("handle_errors", self.handle_errors_node)

        # ============================================================================
        # EDGES - Following SimpleAgent Pattern
        # ============================================================================

        # Start with extraction
        graph.add_edge(START, "extract_memories")

        # 1. After extraction - route based on success/failure
        graph.add_conditional_edges(
            "extract_memories",
            extraction_succeeded,
            {
                True: "after_extraction_router",
                False: "handle_errors"
            }
        )

        # 2. After extraction router - determine next processing step
        graph.add_node("after_extraction_router", self.after_extraction_router)
        graph.add_conditional_edges(
            "after_extraction_router",
            self.determine_next_step,
            {
                "process_kg": "process_kg",
                "categorize": "categorize_memories",
                "consolidate": "consolidate_memories",
                "store": "store_memories"
            }
        )

        # 3. After KG processing
        graph.add_conditional_edges(
            "process_kg",
            has_processing_errors,
            {
                True: "handle_errors",
                False: "after_kg_router"
            }
        )

        graph.add_node("after_kg_router", self.after_kg_router)
        graph.add_conditional_edges(
            "after_kg_router",
            self.determine_next_after_kg,
            {
                "categorize": "categorize_memories",
                "consolidate": "consolidate_memories",
                "store": "store_memories"
            }
        )

        # 4. After categorization
        graph.add_conditional_edges(
            "categorize_memories",
            has_processing_errors,
            {
                True: "handle_errors",
                False: "after_categorize_router"
            }
        )

        graph.add_node("after_categorize_router", self.after_categorize_router)
        graph.add_conditional_edges(
            "after_categorize_router",
            self.determine_next_after_categorize,
            {
                "consolidate": "consolidate_memories",
                "store": "store_memories"
            }
        )

        # 5. After consolidation
        graph.add_conditional_edges(
            "consolidate_memories",
            has_processing_errors,
            {
                True: "handle_errors",
                False: "store_memories"
            }
        )

        # 6. After storage - check for tool activation
        graph.add_conditional_edges(
            "store_memories",
            needs_tool_activation,
            {
                True: "memory_tools",
                False: END
            }
        )

        # 7. Memory tools to end
        graph.add_edge("memory_tools", END)

        # 8. Error handling
        graph.add_conditional_edges(
            "handle_errors",
            self.can_recover_from_errors,
            {
                "retry_extraction": "extract_memories",
                "skip_to_storage": "store_memories",
                "end": END
            }
        )

        return graph

    # ============================================================================
    # ROUTER NODES (Simple Functions)
    # ============================================================================

    def after_extraction_router(self, state: LTMState) -> Dict[str, Any]:
        """Router after extraction - sets next step."""
        next_step = self.determine_next_step(state)
        return {"processing_stage": next_step}

    def after_kg_router(self, state: LTMState) -> Dict[str, Any]:
        """Router after KG processing."""
        next_step = self.determine_next_after_kg(state)
        return {"processing_stage": next_step}

    def after_categorize_router(self, state: LTMState) -> Dict[str, Any]:
        """Router after categorization."""
        next_step = self.determine_next_after_categorize(state)
        return {"processing_stage": next_step}

    # ============================================================================
    # CONDITION FUNCTIONS (Return Simple String Values)
    # ============================================================================

    def determine_next_step(self, state: LTMState) -> str:
        """Determine next processing step after extraction."""
        if needs_kg_processing(state):
            return "process_kg"
        elif needs_categorization(state):
            return "categorize"
        elif needs_consolidation(state):
            return "consolidate"
        else:
            return "store"

    def determine_next_after_kg(self, state: LTMState) -> str:
        """Determine next step after KG processing."""
        if needs_categorization(state):
            return "categorize"
        elif needs_consolidation(state):
            return "consolidate"
        else:
            return "store"

    def determine_next_after_categorize(self, state: LTMState) -> str:
        """Determine next step after categorization."""
        if needs_consolidation(state):
            return "consolidate"
        else:
            return "store"

    def can_recover_from_errors(self, state: LTMState) -> str:
        """Determine error recovery strategy."""
        if not state.extracted_memories:
            return "retry_extraction"
        elif state.extracted_memories:
            return "skip_to_storage"
        else:
            return "end"
```

### 4. **Key Corrections Made**

#### **Pattern Compliance**

- Uses simple boolean functions for conditions (like `has_tool_calls`)
- Router nodes that set state and determine routing
- Clear separation between condition checking and state updates

#### **Simple Condition Functions**

- Return boolean values or simple strings
- No complex logic in condition functions themselves
- State examination only, no state modification

#### **Proper Edge Structure**

- `add_conditional_edges(source, condition_func, route_map)`
- Route maps use simple string keys to node names
- Fallback paths for all conditions

#### **State-Driven Routing**

- All routing decisions based on state attributes
- Clear state progression through `processing_stage`
- Error handling through `processing_errors` list

### 5. **Memory Tool Integration (Following SimpleAgent Tool Pattern)**

```python
def memory_tools_node(self, state: LTMState) -> Dict[str, Any]:
    """Handle memory tool interactions."""

    # Check last message for tool calls (like SimpleAgent)
    if not state.messages:
        return {"tool_calls_needed": False}

    last_msg = state.messages[-1]
    if isinstance(last_msg, AIMessage) and getattr(last_msg, "tool_calls", None):
        # Process tool calls (similar to ToolNode in SimpleAgent)
        # ... tool processing logic ...
        return {"tool_calls_needed": False}

    # If no tool calls, determine if tools are needed
    needs_tools = self.analyze_tool_needs(state)
    return {"tool_calls_needed": needs_tools}

def analyze_tool_needs(self, state: LTMState) -> bool:
    """Analyze if tools are needed (following SimpleAgent validation pattern)."""
    if not state.messages:
        return False

    last_content = state.messages[-1].content.lower()

    # Check for explicit tool requests
    tool_indicators = [
        "search memory", "find memory", "recall", "remember",
        "delete memory", "update memory", "browse memories"
    ]

    return any(indicator in last_content for indicator in tool_indicators)
```

### 6. **Benefits of This Corrected Approach**

#### **Follows Haive Patterns**

- Matches SimpleAgent conditional edge usage exactly
- Uses same validation and routing patterns
- Consistent with existing Haive agent architecture

#### **Simple and Maintainable**

- Clear condition functions that do one thing
- Easy to test and debug individual conditions
- Straightforward flow logic

#### **Robust Error Handling**

- Multiple error check points
- Recovery strategies for different failure modes
- Graceful degradation

#### **Configurable**

- Feature toggles for different processing stages
- Threshold-based routing decisions
- User-controlled behavior

### 7. **Integration with LangMem Components**

```python
# Memory extraction using LangMem patterns
def extract_memories_node(self, state: LTMState) -> Dict[str, Any]:
    """Extract memories using LangMem memory manager."""
    try:
        # Use LangMem memory manager
        memory_manager = self.engines["memory_manager"]

        # Extract memories from conversation
        extracted = memory_manager.invoke({
            "messages": state.messages,
            "max_steps": 3
        })

        return {
            "extracted_memories": extracted,
            "extraction_quality": self.assess_extraction_quality(extracted),
            "processing_stage": "kg"
        }

    except Exception as e:
        return {
            "processing_errors": [f"Extraction failed: {str(e)}"],
            "processing_stage": "error"
        }

# KG processing using Haive components
def process_kg_node(self, state: LTMState) -> Dict[str, Any]:
    """Process knowledge graph using Haive KG extraction."""
    try:
        kg_engine = self.engines["kg_extractor"]

        kg_result = kg_engine.invoke({
            "memories": state.extracted_memories
        })

        return {
            "knowledge_graph": kg_result,
            "processing_stage": "categorize"
        }

    except Exception as e:
        return {
            "processing_errors": state.processing_errors + [f"KG processing failed: {str(e)}"],
            "processing_stage": "categorize"  # Continue despite KG failure
        }
```

This corrected design properly follows LangGraph and Haive patterns while implementing comprehensive LTM functionality. The key insight is that conditional edges should be simple and state-driven, with router nodes handling the complex logic and state updates.
