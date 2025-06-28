# Implementation Plan: Dynamic Routing System for Haive Nodes

## Executive Summary

This document outlines a comprehensive plan to implement automatic dynamic routing across all Haive nodes, eliminating the need for hardcoded `Literal` types and enabling runtime-determined routing based on state values. This system will automatically wrap `Command` and `Send` objects with proper routing logic.

## Critical Requirements from Analysis

### 1. **Consistent Engine Reference Pattern**

All nodes that need an engine should follow the same pattern:

- Take `engine_name` as a parameter (not direct engine reference)
- Look up engine from `state.engines[engine_name]` at runtime
- This ensures consistency and allows engine swapping

```python
class NodeWithEngine(DynamicRoutingNode):
    engine_name: str = Field(default="main")

    def execute(self, input_data: Dict[str, Any], config=None) -> Any:
        # Always get engine from state, not stored reference
        engines = input_data.get("engines", {})
        engine = engines.get(self.engine_name)

        if not engine:
            raise ValueError(f"Engine '{self.engine_name}' not found in state")

        # Use engine...
```

### 2. **State Processing Pipeline**

The correct order of operations for state handling:

```python
class StateProcessingPipeline:
    """Defines the complete state processing flow."""

    def process(self, state: Any, node: NodeConfig) -> Command:
        # 1. State Transformation (optional)
        transformed_state = state
        if node.state_transformer:
            transformed_state = node.state_transformer(state)

        # 2. Field Extraction with Type Validation
        input_data = node.extract_fields_from_state(transformed_state)

        # 3. Input Schema Validation
        if node.input_schema:
            validated_input = node.input_schema(**input_data)
        else:
            validated_input = input_data

        # 4. Pre-processing (optional)
        if node.pre_process:
            validated_input = node.pre_process(validated_input)

        # 5. Execution
        result = node.execute(validated_input, config)

        # 6. Post-processing (optional)
        if node.post_process:
            result = node.post_process(result)

        # 7. Output Schema Validation
        if node.output_schema:
            if isinstance(result, dict):
                validated_result = node.output_schema(**result)
            else:
                validated_result = node.output_schema(value=result)
        else:
            validated_result = result

        # 8. Result to State Mapping
        state_update = node.map_result_to_state(validated_result)

        # 9. Route Determination
        route = node.determine_route(state, validated_result)

        # 10. Command Creation
        return node.create_command(state_update, route)
```

### 3. **Dynamic Route Values from State**

The core problem: routes can be dynamic values from state (like `tool_routes`), not just literals.

```python
class DynamicValueRouting(RoutingStrategy):
    """Routes based on dynamic values in state."""

    values_source: str  # Path to values in state (e.g., "engines.main.tool_routes")
    value_type: Literal["dict_values", "dict_keys", "list", "set"] = "dict_values"

    def get_possible_values(self, state: Any) -> List[str]:
        """Extract possible route values from state."""
        source = get_nested_attr(state, self.values_source)

        if source is None:
            return []

        if self.value_type == "dict_values":
            return list(set(source.values())) if isinstance(source, dict) else []
        elif self.value_type == "dict_keys":
            return list(source.keys()) if isinstance(source, dict) else []
        elif self.value_type == "list":
            return source if isinstance(source, list) else []
        elif self.value_type == "set":
            return list(source) if isinstance(source, set) else []

        return []

    def determine_route(self, state: Any, result: Any, node: Any) -> str:
        """Determine route based on dynamic values."""
        # Implementation specific to the node type
        pass
```

## Problem Statement

### Current Issues

1. **Static Route Definitions**: Currently, routes must be defined at compile time using `Literal` types
2. **Inflexible Tool Routing**: Tool routes (e.g., `tool_routes` in engines) cannot dynamically determine graph flow
3. **Manual Command/Send Wrapping**: Each node must manually handle routing logic
4. **State-Route Mismatch**: No automatic way to map state values to routing decisions
5. **Inconsistent State Handling**: Some nodes get full state, others get pre-extracted values
6. **No I/O Schema Validation**: Input/output types aren't validated or documented
7. **Inconsistent Engine References**: Some nodes take engine_name, others take engine directly

### Example of Current Problem

```python
# Current approach - routes are hardcoded
def route_tool(state) -> Literal["parser", "tool_node", "retriever"]:
    # Cannot dynamically add new routes without changing this signature
    tool_name = state.messages[-1].tool_calls[0].name
    # What if engine.tool_routes has "new_handler" as a value?
    # This would fail at runtime!
    return state.engines.main.tool_routes[tool_name]
```

## Proposed Solution

### Core Architecture with I/O Schemas

```python
# Base class that ALL nodes will inherit from
class DynamicRoutingNode(NodeConfig):
    """Base node with automatic dynamic routing support."""

    # Engine reference (consistent pattern)
    engine_name: Optional[str] = Field(default=None)

    # I/O Schema Configuration
    input_schema: Optional[Type[BaseModel]] = Field(default=None)
    output_schema: Optional[Type[BaseModel]] = Field(default=None)

    # State field extraction
    extract_fields: Optional[Union[List[str], Dict[str, str]]] = Field(default=None)

    # Result field mapping
    result_fields: Optional[Union[str, List[str], Dict[str, str]]] = Field(default=None)

    # State transformation
    state_transformer: Optional[Callable[[Any], Any]] = Field(default=None)

    # Routing configuration
    routing_strategy: RoutingStrategy = Field(default=StateFieldRouting())
    auto_wrap_commands: bool = Field(default=True)

    # Pre/post processing
    pre_process: Optional[Callable] = Field(default=None)
    post_process: Optional[Callable] = Field(default=None)

    def __call__(self, state: Any, config: Optional[Dict] = None) -> Any:
        """Process state through complete pipeline."""
        try:
            # 1. Transform state if needed
            working_state = state
            if self.state_transformer:
                working_state = self.state_transformer(state)

            # 2. Extract input based on configuration
            input_data = self._extract_input(working_state)

            # 3. Always include engines if engine_name is specified
            if self.engine_name and "engines" not in input_data:
                engines = self._get_state_value(working_state, "engines", {})
                input_data["engines"] = engines

            # 4. Validate input schema
            if self.input_schema:
                try:
                    validated_input = self.input_schema(**input_data)
                    # Convert back to dict for execution
                    input_data = validated_input.model_dump()
                except Exception as e:
                    logger.warning(f"Input validation failed: {e}")

            # 5. Pre-process if needed
            if self.pre_process:
                input_data = self.pre_process(input_data)

            # 6. Execute node logic
            result = self.execute(input_data, config)

            # 7. Post-process if needed
            if self.post_process:
                result = self.post_process(result)

            # 8. Validate output schema
            if self.output_schema:
                try:
                    if isinstance(result, dict):
                        validated_result = self.output_schema(**result)
                    else:
                        # Wrap non-dict results
                        validated_result = self.output_schema(value=result)
                    # Keep as model or convert based on preference
                    result = validated_result
                except Exception as e:
                    logger.warning(f"Output validation failed: {e}")

            # 9. Determine routing
            route = self.routing_strategy.determine_route(state, result, self)

            # 10. Auto-wrap in Command/Send
            if self.auto_wrap_commands:
                return self._wrap_with_routing(result, route, state)

            return result

        except Exception as e:
            logger.error(f"Error in node {self.name}: {e}")
            return self._handle_error(e, state)
```

### Command and Send Wrapping

```python
class CommandWrapper:
    """Handles automatic wrapping of results in Command/Send objects."""

    @staticmethod
    def wrap(
        result: Any,
        route: Union[str, List[str]],
        state: Any,
        node: DynamicRoutingNode
    ) -> Union[Command, Send, List[Send]]:
        """Intelligently wrap results based on routing decision."""

        # 1. Create state update from result
        state_update = node._create_state_update(result, state)

        # 2. Handle different routing scenarios
        if isinstance(route, list):
            # Multiple routes = parallel execution
            if len(route) == 0:
                # No routes, go to END
                return Command(update=state_update, goto=END)

            elif len(route) == 1:
                # Single route, use Command
                return Command(update=state_update, goto=route[0])

            else:
                # Multiple routes, use Send for parallel execution
                return [Send(node=r, arg=state_update) for r in route]

        elif route is None:
            # No route specified, use default
            return Command(update=state_update, goto=node.command_goto or END)

        else:
            # Single route string
            return Command(update=state_update, goto=route)

class DynamicRoutingNode(NodeConfig):
    """Enhanced with sophisticated command wrapping."""

    # Control wrapping behavior
    wrap_commands: bool = Field(default=True)
    enable_send: bool = Field(default=True)
    send_strategy: Literal["parallel", "sequential"] = Field(default="parallel")

    def _wrap_with_routing(
        self,
        result: Any,
        route: Union[str, List[str]],
        state: Any
    ) -> Union[Command, Send, List[Send]]:
        """Wrap result with appropriate command type."""

        # Allow node to customize wrapping
        if hasattr(self, "custom_wrap"):
            return self.custom_wrap(result, route, state)

        # Use standard wrapper
        return CommandWrapper.wrap(result, route, state, self)

    def _create_state_update(self, result: Any, state: Any) -> Dict[str, Any]:
        """Create state update from result based on configuration."""

        # 1. Handle None result
        if result is None:
            return {}

        # 2. Use result_fields configuration if specified
        if self.result_fields is not None:
            return self._apply_result_mapping(result)

        # 3. Auto-detect update format
        if isinstance(result, Command):
            # Result is already a Command, extract update
            return result.update or {}

        elif isinstance(result, dict):
            # Direct dictionary update
            return result

        elif isinstance(result, BaseModel):
            # Pydantic model - convert to dict
            return result.model_dump()

        elif isinstance(result, list):
            # List result - use node name as key
            return {f"{self.name}_results": result}

        else:
            # Single value - use node name as key
            return {f"{self.name}_result": result}

    def _apply_result_mapping(self, result: Any) -> Dict[str, Any]:
        """Apply configured result field mapping."""

        if isinstance(self.result_fields, str):
            # Single field name
            return {self.result_fields: result}

        elif isinstance(self.result_fields, list):
            # Extract specific fields from result
            if isinstance(result, dict):
                return {
                    field: result.get(field)
                    for field in self.result_fields
                    if field in result
                }
            elif isinstance(result, BaseModel):
                result_dict = result.model_dump()
                return {
                    field: result_dict.get(field)
                    for field in self.result_fields
                    if field in result_dict
                }
            else:
                # Can't extract fields from non-dict
                return {self.result_fields[0]: result}

        elif isinstance(self.result_fields, dict):
            # Map result fields to state fields
            update = {}
            result_dict = self._normalize_to_dict(result)

            for result_field, state_field in self.result_fields.items():
                if result_field in result_dict:
                    update[state_field] = result_dict[result_field]

            return update

        return {}
```

### Advanced Send Patterns

```python
class ParallelExecutionNode(DynamicRoutingNode):
    """Node that fans out to multiple destinations."""

    parallel_destinations: List[str] = Field(default_factory=list)

    # Custom routing that returns multiple routes
    routing_strategy: RoutingStrategy = Field(
        default_factory=lambda: MultiRouteStrategy()
    )

    def execute(self, input_data: Dict[str, Any], config=None) -> Dict[str, Any]:
        """Prepare data for parallel execution."""
        # Add any preprocessing for parallel execution
        return {
            "prepared_data": input_data,
            "fanout_timestamp": datetime.now().isoformat(),
            "parallel_id": str(uuid.uuid4())
        }

class ConditionalSendNode(DynamicRoutingNode):
    """Node that conditionally sends to multiple destinations."""

    def execute(self, input_data: Dict[str, Any], config=None) -> Dict[str, Any]:
        """Analyze and prepare conditional sends."""
        score = input_data.get("relevance_score", 0)

        # Return metadata that routing strategy will use
        return {
            "score": score,
            "should_parallelize": score > 0.5,
            "destinations": self._determine_destinations(score)
        }

    def _determine_destinations(self, score: float) -> List[str]:
        """Determine which nodes should receive the data."""
        destinations = []

        if score > 0.8:
            destinations.extend(["high_quality_processor", "fast_track"])
        elif score > 0.5:
            destinations.append("standard_processor")
        else:
            destinations.extend(["improvement_needed", "retry_with_enhancement"])

        return destinations

class SendAggregatorNode(DynamicRoutingNode):
    """Node that aggregates results from parallel Send operations."""

    aggregation_strategy: Literal["all", "any", "majority"] = Field(default="all")

    def execute(self, input_data: Dict[str, Any], config=None) -> Dict[str, Any]:
        """Aggregate results from parallel executions."""
        # In LangGraph, this would receive results from multiple Send operations
        parallel_results = input_data.get("parallel_results", {})

        if self.aggregation_strategy == "all":
            # All must succeed
            success = all(r.get("success", False) for r in parallel_results.values())
        elif self.aggregation_strategy == "any":
            # Any can succeed
            success = any(r.get("success", False) for r in parallel_results.values())
        else:
            # Majority must succeed
            successes = sum(1 for r in parallel_results.values() if r.get("success", False))
            success = successes > len(parallel_results) / 2

        return {
            "aggregated_success": success,
            "individual_results": parallel_results,
            "aggregation_method": self.aggregation_strategy
        }
```

### Routing Strategies with Send Support

```python
class MultiDestinationRouting(RoutingStrategy):
    """Routing strategy that can return multiple destinations."""

    def determine_route(self, state: Any, result: Any, node: Any) -> Union[str, List[str]]:
        """Determine one or more routes."""
        # Check result for destination hints
        if isinstance(result, dict):
            # Explicit destinations in result
            if "destinations" in result:
                dests = result["destinations"]
                if isinstance(dests, list):
                    return dests
                elif isinstance(dests, str):
                    return [dests]

            # Conditional routing based on flags
            if result.get("should_parallelize", False):
                return self._get_parallel_routes(state, result)

        # Default single route
        return node.command_goto or END

    def _get_parallel_routes(self, state: Any, result: Any) -> List[str]:
        """Get routes for parallel execution."""
        # Could read from state, result, or have predefined routes
        available_processors = state.get("available_processors", [])

        if available_processors:
            return available_processors[:3]  # Limit parallelism

        return ["processor_1", "processor_2", "processor_3"]

class DynamicFanOutRouting(RoutingStrategy):
    """Route to multiple destinations based on state configuration."""

    fanout_config_path: str = "routing_config.fanout_destinations"

    def determine_route(self, state: Any, result: Any, node: Any) -> Union[str, List[str]]:
        """Determine routes from state configuration."""
        # Get fanout configuration from state
        fanout_dests = get_nested_attr(state, self.fanout_config_path, [])

        if isinstance(fanout_dests, list) and fanout_dests:
            return fanout_dests

        # Fallback to single route
        return node.command_goto or END
```

### Graph Builder Support for Send Commands

```python
class EnhancedGraphBuilder:
    """Graph builder with Send command support."""

    def __init__(self):
        self.graph = StateGraph(GraphState)
        self.nodes_with_send = set()
        self.parallel_aggregators = {}

    def add_node(self, node: Union[NodeConfig, Callable], name: Optional[str] = None):
        """Add node and track Send capabilities."""
        if isinstance(node, DynamicRoutingNode):
            name = name or node.name
            self.graph.add_node(name, node)

            # Track nodes that might use Send
            if node.enable_send:
                self.nodes_with_send.add(name)

                # Check if this is an aggregator
                if hasattr(node, "aggregation_strategy"):
                    # Find which nodes send to this aggregator
                    for other_name, other_node in self.graph.nodes.items():
                        if hasattr(other_node, "routing_strategy"):
                            routes = other_node.routing_strategy.get_possible_routes()
                            if name in routes:
                                self.parallel_aggregators[name] = self.parallel_aggregators.get(name, [])
                                self.parallel_aggregators[name].append(other_name)

    def compile(self) -> CompiledGraph:
        """Compile with Send support."""
        # For nodes that use Send, we need to ensure the graph
        # can handle the parallel execution properly

        for node_name in self.nodes_with_send:
            node = self.graph.nodes[node_name]

            # Add conditional edges that can handle Send returns
            self.graph.add_conditional_edges(
                node_name,
                self._create_send_handler(node),
                self._get_all_possible_destinations(node)
            )

        return self.graph.compile()

    def _create_send_handler(self, node: DynamicRoutingNode):
        """Create a handler for Send commands."""
        def handler(state):
            # This is simplified - LangGraph handles Send internally
            # but we need to ensure routes are available
            return state.get("next_route", END)

        return handler
```

### Example: Complete RAG with Parallel Processing

```python
# Build a RAG pipeline with parallel document processing
def build_parallel_rag():
    builder = EnhancedGraphBuilder()

    # 1. Retriever fans out to multiple graders
    retriever = RetrieverNode(
        engine_name="retriever",
        routing_strategy=DynamicFanOutRouting(
            fanout_config_path="grader_nodes"
        )
    )

    # 2. Multiple graders process in parallel
    grader1 = create_node_from_function(
        grade_by_relevance,
        name="relevance_grader",
        routing_strategy=StaticRouting("aggregator")
    )

    grader2 = create_node_from_function(
        grade_by_quality,
        name="quality_grader",
        routing_strategy=StaticRouting("aggregator")
    )

    grader3 = create_node_from_function(
        grade_by_recency,
        name="recency_grader",
        routing_strategy=StaticRouting("aggregator")
    )

    # 3. Aggregator combines results
    aggregator = SendAggregatorNode(
        name="grade_aggregator",
        aggregation_strategy="majority",
        routing_strategy=ConditionalRouting([
            (lambda s, r: r.get("aggregated_success"), "generator"),
            (lambda s, r: True, "web_search")
        ])
    )

    # Add all nodes
    builder.add_node(retriever)
    builder.add_node(grader1)
    builder.add_node(grader2)
    builder.add_node(grader3)
    builder.add_node(aggregator)

    return builder.compile()

# Usage
state = GraphState(
    query="Complex query needing parallel analysis",
    grader_nodes=["relevance_grader", "quality_grader", "recency_grader"],
    engines={"retriever": retriever_engine}
)

app = build_parallel_rag()
result = app.invoke(state.model_dump())
```

### Key Benefits of Automatic Command/Send Wrapping

1. **Nodes Don't Worry About Commands**: Just return dicts or objects
2. **Routing Logic Separated**: Routing strategies determine destinations
3. **Automatic Parallelization**: Multiple routes automatically use Send
4. **State Updates Handled**: Result mapping to state is automatic
5. **Flexible Patterns**: Easy to switch between Command and Send

This automatic wrapping is crucial because it:

- Removes boilerplate from every node
- Ensures consistent behavior
- Makes parallel execution transparent
- Allows routing changes without node changes

### Looping Support

```python
class LoopingMixin:
    """Mixin for nodes that process collections."""

    loop_over_field: Optional[str] = Field(default=None)
    loop_result_field: Optional[str] = Field(default=None)
    parallel_loop: bool = Field(default=False)

    def execute_with_loop(self, input_data: Any, config: Optional[Dict] = None) -> Any:
        """Execute with looping support."""
        if not self.loop_over_field or self.loop_over_field not in input_data:
            # No looping needed
            return self.execute(input_data, config)

        collection = input_data[self.loop_over_field]
        results = []

        for i, item in enumerate(collection):
            # Prepare loop input
            loop_input = {
                **input_data,
                "current_item": item,
                "item_index": i,
                "total_items": len(collection)
            }

            # Execute for this item
            try:
                result = self.execute(loop_input, config)
                results.append(result)
            except Exception as e:
                logger.error(f"Error in loop iteration {i}: {e}")
                results.append({"error": str(e), "item_index": i})

        # Return results
        if self.loop_result_field:
            return {self.loop_result_field: results}
        return results

class CallableNodeConfig(DynamicRoutingNode, LoopingMixin):
    """Node that can execute callables with loop support."""

    callable_func: Callable = Field(...)

    def __call__(self, state: Any, config: Optional[Dict] = None) -> Any:
        """Override to add loop support."""
        if self.loop_over_field:
            # Use loop-aware execution
            input_data = self._extract_input(state)
            result = self.execute_with_loop(input_data, config)
            route = self.routing_strategy.determine_route(state, result, self)
            return self._wrap_with_routing(result, route, state)

        # Standard execution
        return super().__call__(state, config)
```

### Input/Output Field Extraction

```python
class EnhancedNodeConfig(DynamicRoutingNode):
    """Enhanced node with smart I/O handling."""

    def _extract_input(self, state: Any) -> Any:
        """Extract input from state based on configuration."""
        # Always receive full state, extract what's needed
        if self.extract_fields is None:
            # No extraction - convert to dict if Pydantic
            if isinstance(state, BaseModel):
                return state.model_dump()
            return state

        extracted = {}

        if isinstance(self.extract_fields, list):
            # Extract listed fields
            for field in self.extract_fields:
                value = self._get_state_value(state, field)
                if value is not None:
                    extracted[field] = value

        elif isinstance(self.extract_fields, dict):
            # Map state fields to input fields
            for state_field, input_field in self.extract_fields.items():
                value = self._get_state_value(state, state_field)
                if value is not None:
                    extracted[input_field] = value

        # Validate with input schema if provided
        if self.input_schema:
            try:
                return self.input_schema(**extracted)
            except Exception as e:
                logger.warning(f"Input validation failed: {e}")
                return extracted

        return extracted

    def _create_state_update(self, result: Any, state: Any) -> Dict[str, Any]:
        """Create state update from result based on configuration."""
        if self.result_fields is None:
            # Auto-detect update format
            if isinstance(result, dict):
                return result
            elif isinstance(result, BaseModel):
                return result.model_dump()
            else:
                return {f"{self.name}_result": result}

        if isinstance(self.result_fields, str):
            # Single field mapping
            return {self.result_fields: result}

        elif isinstance(self.result_fields, list):
            # Extract specific fields from result
            if isinstance(result, dict):
                return {field: result.get(field) for field in self.result_fields if field in result}
            elif isinstance(result, BaseModel):
                result_dict = result.model_dump()
                return {field: result_dict.get(field) for field in self.result_fields if field in result_dict}

        elif isinstance(self.result_fields, dict):
            # Map result fields to state fields
            update = {}
            result_dict = self._normalize_result(result)

            for result_field, state_field in self.result_fields.items():
                if result_field in result_dict:
                    update[state_field] = result_dict[result_field]

            return update

        return {}
```

### Routing Strategies

```python
from abc import ABC, abstractmethod

class RoutingStrategy(ABC):
    """Base strategy for determining routes."""

    @abstractmethod
    def determine_route(self, state: Any, result: Any, node: Any) -> Union[str, List[str]]:
        """Determine the next route based on state and result."""
        pass

class StateFieldRouting(RoutingStrategy):
    """Route based on a field in state (most common)."""

    field_path: str = "next_route"
    clear_after_read: bool = True

    def determine_route(self, state: Any, result: Any, node: Any) -> str:
        route = get_nested_attr(state, self.field_path)

        # Clear the route field if requested
        if self.clear_after_read and isinstance(result, dict):
            # Add clearing instruction to result
            set_nested_attr(result, self.field_path, None)

        return route or node.command_goto or END

class EngineToolRouting(RoutingStrategy):
    """Route based on tool_routes in engine."""

    engine_path: str = "engines.main"
    tool_extractor: Callable = extract_last_tool_name
    route_mapping: Optional[Dict[str, str]] = None

    def determine_route(self, state: Any, result: Any, node: Any) -> str:
        engine = get_nested_attr(state, self.engine_path)
        tool_name = self.tool_extractor(state)

        if hasattr(engine, "tool_routes") and tool_name:
            route = engine.tool_routes.get(tool_name, "unknown")

            # Apply mapping if provided
            if self.route_mapping:
                route = self.route_mapping.get(route, route)

            return route

        return node.command_goto or END

class ParallelRouting(RoutingStrategy):
    """Route to multiple destinations in parallel."""

    routes: List[str]
    condition: Optional[Callable] = None

    def determine_route(self, state: Any, result: Any, node: Any) -> Union[str, List[str]]:
        if self.condition and not self.condition(state, result):
            return node.command_goto or END

        return self.routes

class ConditionalRouting(RoutingStrategy):
    """Route based on conditions."""

    conditions: List[Tuple[Callable, str]]
    default: str = END

    def determine_route(self, state: Any, result: Any, node: Any) -> str:
        for condition, route in self.conditions:
            if condition(state, result):
                return route

        return self.default
```

### Send Command Support

```python
class EnhancedCommandWrapper:
    """Enhanced command wrapping with Send support."""

    @staticmethod
    def wrap(result: Any, route: Union[str, List[str]], state: Any, node: Any) -> Union[Command, Send, List[Send]]:
        """Wrap result in appropriate command type."""
        # Create state update
        update = node._create_state_update(result, state)

        # Handle multiple routes with Send
        if isinstance(route, list):
            if len(route) == 1:
                # Single route - use Command
                return Command(update=update, goto=route[0])
            else:
                # Multiple routes - use Send
                return [Send(node=r, arg=update) for r in route]

        # Single route
        return Command(update=update, goto=route)

class DynamicRoutingNode(NodeConfig):
    """Updated with Send support."""

    enable_send: bool = Field(default=True)

    def _wrap_with_routing(self, result: Any, route: Union[str, List[str]], state: Any) -> Union[Command, Send, List[Send]]:
        """Wrap with routing support."""
        if not self.enable_send and isinstance(route, list):
            # Force single route if Send disabled
            route = route[0] if route else END

        return EnhancedCommandWrapper.wrap(result, route, state, self)
```

## Implementation Details

### Step 1: Update Base Node Classes

```python
# haive/core/graph/node/base_config.py

class NodeConfig(BaseModel):
    """Enhanced base configuration with routing support."""

    # Existing fields...
    name: str
    node_type: NodeType
    command_goto: Optional[str] = END

    # New routing fields
    routing_strategy: Optional[RoutingStrategy] = None
    routing_enabled: bool = True
    wrap_commands: bool = True

    # I/O configuration
    input_schema: Optional[Type[BaseModel]] = None
    output_schema: Optional[Type[BaseModel]] = None
    extract_fields: Optional[Union[List[str], Dict[str, str]]] = None
    result_fields: Optional[Union[str, List[str], Dict[str, str]]] = None

    # Processing hooks
    pre_process: Optional[Callable] = None
    post_process: Optional[Callable] = None

    def __call__(self, state: Any, config: Optional[Dict] = None) -> Any:
        """Execute with automatic routing."""
        if not self.routing_enabled:
            # Legacy behavior
            return self._execute_legacy(state, config)

        # Modern routing behavior
        try:
            # 1. Extract input
            input_data = self._extract_input(state)

            # 2. Pre-process
            if self.pre_process:
                input_data = self.pre_process(input_data)

            # 3. Execute
            result = self.execute(input_data, config)

            # 4. Post-process
            if self.post_process:
                result = self.post_process(result)

            # 5. Determine route
            route = self._determine_route(state, result)

            # 6. Wrap result
            if self.wrap_commands:
                return self._wrap_with_routing(result, route, state)

            return result

        except Exception as e:
            logger.error(f"Error in node {self.name}: {e}")
            return self._handle_error(e, state)
```

### Updated Node Examples with Consistent Patterns

#### ValidationNodeConfig - Correct Pattern

```python
class ValidationNodeConfig(DynamicRoutingNode):
    """Validation node following correct patterns."""

    node_type: NodeType = Field(default=NodeType.VALIDATION)
    engine_name: str = Field(default="main")  # Engine reference, not direct engine

    # Define what we need from state
    extract_fields: List[str] = Field(default=["messages", "engines"])

    # Define our output schema
    class ValidationOutput(BaseModel):
        tool_name: str
        is_valid: bool
        validation_errors: List[str] = []
        metadata: Dict[str, Any] = {}

    output_schema: Type[BaseModel] = Field(default=ValidationOutput)

    # Use engine tool routing with proper mapping
    routing_strategy: RoutingStrategy = Field(
        default_factory=lambda: EngineToolRouting(
            engine_path="engines.main",
            route_mapping={
                "pydantic_model": "parser",
                "langchain_tool": "tool_node",
                "function": "tool_node",
                "retriever": "retriever_node"
            }
        )
    )

    def execute(self, input_data: Dict[str, Any], config: Optional[Dict] = None) -> Dict[str, Any]:
        """Execute validation - input is already extracted and validated."""
        messages = input_data.get("messages", [])
        engines = input_data.get("engines", {})

        # Get engine from engines dict
        engine = engines.get(self.engine_name)
        if not engine:
            return {
                "tool_name": "unknown",
                "is_valid": False,
                "validation_errors": [f"Engine '{self.engine_name}' not found"]
            }

        # Extract tool information
        tool_name = self._extract_last_tool_name(messages)
        if not tool_name:
            return {
                "tool_name": "unknown",
                "is_valid": False,
                "validation_errors": ["No tool calls found in messages"]
            }

        # Validate tool exists
        validation_errors = []
        is_valid = True

        # Check in tools
        if hasattr(engine, "tools") and engine.tools:
            tool_names = [getattr(t, "name", str(t)) for t in engine.tools]
            if tool_name not in tool_names:
                validation_errors.append(f"Tool '{tool_name}' not found in engine tools")
                is_valid = False

        # Check in schemas
        if hasattr(engine, "schemas") and engine.schemas:
            schema_names = [getattr(s, "__name__", str(s)) for s in engine.schemas]
            # Valid if in either tools or schemas
            if tool_name in schema_names:
                is_valid = True
                validation_errors = []  # Clear errors if found in schemas

        return {
            "tool_name": tool_name,
            "is_valid": is_valid,
            "validation_errors": validation_errors,
            "metadata": {
                "engine": self.engine_name,
                "timestamp": datetime.now().isoformat()
            }
        }
```

#### EngineNodeConfig - With Auto I/O Detection

```python
class EngineNodeConfig(DynamicRoutingNode):
    """Engine node with automatic I/O detection."""

    node_type: NodeType = Field(default=NodeType.ENGINE)
    engine_name: str = Field(...)  # Required - which engine to use

    # By default, extract messages and engines
    extract_fields: List[str] = Field(default=["messages", "engines"])

    # Auto-detect I/O requirements from engine
    auto_detect_io: bool = Field(default=True)

    def _extract_input(self, state: Any) -> Dict[str, Any]:
        """Override to auto-detect engine requirements."""
        # First get base extraction
        base_input = super()._extract_input(state)

        if self.auto_detect_io and "engines" in base_input:
            engine = base_input["engines"].get(self.engine_name)

            if engine:
                # Detect engine type and adjust input
                if hasattr(engine, "engine_type"):
                    engine_type = str(engine.engine_type)

                    if engine_type == "retriever":
                        # Retrievers need query
                        query = self._get_state_value(state, "query")
                        if query:
                            base_input["query"] = query
                        # Remove messages if not needed
                        if "messages" in base_input and not self._engine_uses_messages(engine):
                            del base_input["messages"]

                    elif engine_type == "llm":
                        # LLMs mainly need messages
                        # Already have messages from extract_fields
                        pass

                    elif engine_type == "embeddings":
                        # Embeddings need text/query
                        for field in ["query", "text", "content"]:
                            value = self._get_state_value(state, field)
                            if value:
                                base_input[field] = value
                                break

                # Check if engine defines its own input requirements
                if hasattr(engine, "required_inputs"):
                    for field in engine.required_inputs:
                        value = self._get_state_value(state, field)
                        if value is not None:
                            base_input[field] = value

        return base_input

    def execute(self, input_data: Dict[str, Any], config: Optional[Dict] = None) -> Any:
        """Execute engine with prepared input."""
        engines = input_data.get("engines", {})
        engine = engines.get(self.engine_name)

        if not engine:
            raise ValueError(f"Engine '{self.engine_name}' not found")

        # Remove engines from input before passing to engine
        engine_input = {k: v for k, v in input_data.items() if k != "engines"}

        # Special handling based on engine type
        if hasattr(engine, "engine_type"):
            engine_type = str(engine.engine_type)

            if engine_type == "retriever" and "query" in engine_input:
                # Retrievers typically want just the query string
                return engine.invoke(engine_input["query"], config)

        # Default: pass full input dict
        return engine.invoke(engine_input, config)
```

#### ToolNodeConfig - With Proper Engine Reference

```python
class ToolNodeConfig(DynamicRoutingNode):
    """Tool node with proper engine reference pattern."""

    node_type: NodeType = Field(default=NodeType.TOOL)
    engine_name: str = Field(default="main")

    # Extract what we need
    extract_fields: List[str] = Field(default=["messages", "engines"])

    # Tool results go back in messages
    result_fields: str = Field(default="messages")

    # Filter tools by route
    allowed_routes: List[str] = Field(
        default=["langchain_tool", "function", "tool_node"]
    )

    def execute(self, input_data: Dict[str, Any], config: Optional[Dict] = None) -> Any:
        """Execute tools from engine."""
        messages = input_data.get("messages", [])
        engines = input_data.get("engines", {})

        # Get engine
        engine = engines.get(self.engine_name)
        if not engine:
            logger.error(f"Engine '{self.engine_name}' not found")
            return messages  # Return unchanged

        # Collect tools from engine
        all_tools = []
        if hasattr(engine, "tools") and engine.tools:
            all_tools.extend(engine.tools)

        # Filter by allowed routes
        tool_routes = getattr(engine, "tool_routes", {})
        filtered_tools = []

        for tool in all_tools:
            tool_name = getattr(tool, "name", str(tool))
            route = tool_routes.get(tool_name, "langchain_tool")

            if route in self.allowed_routes:
                filtered_tools.append(tool)
                logger.debug(f"Including tool '{tool_name}' with route '{route}'")
            else:
                logger.debug(f"Excluding tool '{tool_name}' with route '{route}'")

        if not filtered_tools:
            logger.warning("No tools match allowed routes")
            return messages

        # Use LangChain's ToolNode
        from langgraph.prebuilt import ToolNode

        tool_node = ToolNode(
            tools=filtered_tools,
            messages_key="messages"
        )

        # Execute and get updated messages
        result = tool_node.invoke({"messages": messages}, config)

        # Return updated messages
        return result.get("messages", messages)
```

#### ParserNodeConfig - Already Correct Pattern

```python
class ParserNodeConfig(DynamicRoutingNode):
    """Parser node - already follows correct pattern."""

    node_type: NodeType = Field(default=NodeType.PARSER)
    engine_name: str = Field(default="main")

    extract_fields: List[str] = Field(default=["messages", "engines"])

    # Output field for parsed result
    output_key: str = Field(default="parsed_output")

    # Return to agent after parsing
    routing_strategy: RoutingStrategy = Field(
        default_factory=lambda: StaticRouting(route="agent")
    )

    def execute(self, input_data: Dict[str, Any], config: Optional[Dict] = None) -> Dict[str, Any]:
        """Parse tool output using schema from engine."""
        messages = input_data.get("messages", [])
        engines = input_data.get("engines", {})

        # Get engine
        engine = engines.get(self.engine_name)
        if not engine:
            return {"error": f"Engine '{self.engine_name}' not found"}

        # Find last tool message
        tool_message = None
        tool_name = None

        for msg in reversed(messages):
            if hasattr(msg, "name") and hasattr(msg, "content"):
                tool_message = msg
                tool_name = msg.name
                break

        if not tool_message:
            return {"error": "No tool message found"}

        # Find schema in engine
        schema = None

        # Check schemas
        if hasattr(engine, "schemas") and engine.schemas:
            for s in engine.schemas:
                if getattr(s, "__name__", "") == tool_name:
                    schema = s
                    break

        # Check structured_output_model
        if not schema and hasattr(engine, "structured_output_model"):
            model = engine.structured_output_model
            if getattr(model, "__name__", "") == tool_name:
                schema = model

        if not schema:
            return {"error": f"No schema found for tool '{tool_name}'"}

        # Parse content
        try:
            content = tool_message.content

            # Handle different content types
            if isinstance(content, dict):
                parsed = schema(**content)
            elif isinstance(content, str):
                # Try JSON parsing
                import json
                data = json.loads(content)
                parsed = schema(**data)
            else:
                parsed = schema(value=content)

            return {self.output_key: parsed}

        except Exception as e:
            logger.error(f"Failed to parse: {e}")
            return {
                "error": str(e),
                "raw_content": content,
                self.output_key: None
            }
```

### Step 3: Graph Builder Integration

```python
class EnhancedGraphBuilder:
    """Graph builder that understands dynamic routing."""

    def __init__(self):
        self.graph = StateGraph(GraphState)
        self.dynamic_nodes = {}

    def add_node(self, node: Union[NodeConfig, Callable], name: Optional[str] = None) -> None:
        """Add a node with automatic routing support."""
        if isinstance(node, NodeConfig):
            name = name or node.name
            self.graph.add_node(name, node)

            # Track dynamic nodes
            if node.routing_enabled:
                self.dynamic_nodes[name] = node
        else:
            # Legacy callable
            self.graph.add_node(name or node.__name__, node)

    def compile(self) -> CompiledGraph:
        """Compile with dynamic routing support."""
        # Add conditional edges for dynamic nodes
        for name, node in self.dynamic_nodes.items():
            if hasattr(node.routing_strategy, 'is_conditional'):
                # Add conditional routing
                self.graph.add_conditional_edges(
                    name,
                    lambda state: state.get("next_route", END),
                    self._get_possible_routes(node)
                )

        return self.graph.compile()

    def _get_possible_routes(self, node: NodeConfig) -> Dict[str, str]:
        """Get possible routes for a node."""
        # This would be more sophisticated in practice
        return {
            "tool_node": "tool_node",
            "parser": "parser",
            "retriever": "retriever",
            "agent": "agent",
            END: END
        }
```

## Complete Example: Document Processing Pipeline

```python
# Define schemas
class DocumentInput(BaseModel):
    document: Document
    query: str

class DocumentGrade(BaseModel):
    is_relevant: bool
    relevance_score: float
    reasoning: str

# Create grading function
@node_function(
    name="document_grader",
    extract_fields={"documents": "document", "query": "query"},
    result_fields={"is_relevant": "doc_relevant", "relevance_score": "doc_score"},
    routing_strategy=ConditionalRouting(
        conditions=[
            (lambda s, r: r.get("is_relevant", False), "relevant_docs"),
            (lambda s, r: True, "irrelevant_docs")
        ]
    )
)
def grade_document(input_data: DocumentInput) -> DocumentGrade:
    """Grade document relevance."""
    # Scoring logic
    score = calculate_relevance(input_data.document, input_data.query)

    return DocumentGrade(
        is_relevant=score > 0.5,
        relevance_score=score,
        reasoning=f"Document matches {score*100:.1f}% of query terms"
    )

# Create a looping grader for multiple documents
document_batch_grader = CallableNodeConfig(
    name="batch_grader",
    callable_func=grade_document,
    loop_over_field="retrieved_documents",
    loop_result_field="graded_documents",
    extract_fields=["retrieved_documents", "query"],
    routing_strategy=StateFieldRouting()  # Read next_route from state
)

# Build graph
builder = EnhancedGraphBuilder()
builder.add_node(document_batch_grader)
builder.add_node("relevant_docs", process_relevant_docs)
builder.add_node("irrelevant_docs", handle_irrelevant_docs)

graph = builder.compile()
```

## Benefits

### 1. **Simplified Node Development**

- Nodes focus only on their core logic
- No manual routing code needed
- Automatic Command/Send wrapping
- Built-in looping support

### 2. **Dynamic Runtime Routing**

- Routes determined from state values
- No compile-time route restrictions
- Easy to add new routes without code changes
- Support for parallel execution with Send

### 3. **Consistency**

- All nodes use the same pattern
- Consistent state handling (always full state)
- Standardized I/O with schemas
- Easier to debug and maintain

### 4. **Flexibility**

- Multiple routing strategies available
- Function wrapping and decorators
- Pre/post processing hooks
- Custom strategies easy to create

### 5. **Better Testing**

- Routing logic separated from business logic
- I/O schemas enable better testing
- Mock strategies for unit tests
- Clear contracts between nodes

## Key Design Principles

### 1. **Always Full State, Smart Extraction**

- Every node receives the full state
- Nodes declare what fields they need via `extract_fields`
- Extraction happens automatically before execution
- This ensures consistency and flexibility

### 2. **Engine Reference Pattern**

- Nodes take `engine_name`, not direct engine references
- Engines are looked up from `state.engines[engine_name]`
- This allows engine swapping and better testing

### 3. **I/O Schema Validation**

- Input schemas validate extracted data before execution
- Output schemas validate results before state updates
- This provides type safety and documentation

### 4. **Routing from State Values**

- Routes are determined from state values at runtime
- No hardcoded Literal types needed
- Tool routes, valid nodes, etc. all come from state

### 5. **Automatic Command Wrapping**

- Nodes return simple dicts or objects
- Base class automatically wraps in Command/Send
- Routing decisions are separate from business logic

## Complete Working Example

```python
# Example: Building a RAG Pipeline with Dynamic Routing

# 1. Define State with Dynamic Routes
class RAGState(BaseModel):
    messages: List[Any] = []
    query: str = ""
    documents: List[Document] = []
    engines: Dict[str, Any] = {}

    # Dynamic routing fields
    next_route: Optional[str] = None
    available_nodes: List[str] = []

    class Config:
        arbitrary_types_allowed = True

# 2. Create Retriever Node
class RetrieverNode(DynamicRoutingNode):
    node_type: NodeType = Field(default=NodeType.ENGINE)
    engine_name: str = Field(default="retriever")

    # Define what we need and produce
    extract_fields: List[str] = Field(default=["query", "engines"])
    result_fields: Dict[str, str] = Field(
        default={"documents": "retrieved_documents"}
    )

    # Route based on document count
    routing_strategy: RoutingStrategy = Field(
        default_factory=lambda: ConditionalRouting(
            conditions=[
                (lambda s, r: len(r.get("documents", [])) > 0, "document_grader"),
                (lambda s, r: True, "query_rewriter")
            ]
        )
    )

    def execute(self, input_data: Dict[str, Any], config=None) -> Dict[str, Any]:
        query = input_data.get("query", "")
        engines = input_data.get("engines", {})

        retriever = engines.get(self.engine_name)
        if not retriever:
            return {"documents": []}

        # Execute retrieval
        docs = retriever.invoke(query, config)
        return {"documents": docs}

# 3. Create Document Grader
@node_function(
    name="document_grader",
    extract_fields=["retrieved_documents", "query"],
    result_fields={"graded_docs": "graded_documents"},
    routing_strategy=ConditionalRouting(
        conditions=[
            (lambda s, r: any(d.get("relevant") for d in r.get("graded_docs", [])), "generator"),
            (lambda s, r: True, "web_search")
        ]
    )
)
def grade_documents(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """Grade document relevance."""
    docs = input_data.get("retrieved_documents", [])
    query = input_data.get("query", "")

    graded = []
    for doc in docs:
        # Simple relevance check
        score = calculate_relevance(doc, query)
        graded.append({
            "document": doc,
            "relevant": score > 0.5,
            "score": score
        })

    return {"graded_docs": graded}

# 4. Build Graph with Dynamic Routing
def build_rag_graph():
    builder = EnhancedGraphBuilder()

    # Create engine configuration
    retriever_engine = RetrieverEngine(name="retriever")
    generator_engine = GeneratorEngine(name="generator")

    # Add nodes - they handle their own routing!
    builder.add_node(RetrieverNode())
    builder.add_node(grade_documents)
    builder.add_node(GeneratorNode(engine_name="generator"))
    builder.add_node(WebSearchNode())
    builder.add_node(QueryRewriterNode())

    # The builder understands dynamic routing
    return builder.compile()

# 5. Use the Graph
initial_state = RAGState(
    query="What is the capital of France?",
    engines={
        "retriever": retriever_engine,
        "generator": generator_engine
    },
    available_nodes=["retriever", "document_grader", "generator", "web_search", "query_rewriter"]
)

app = build_rag_graph()
result = app.invoke(initial_state.model_dump())
```

## Benefits Summary

1. **No More Literal Types**: Routes come from state at runtime
2. **Consistent Patterns**: All nodes follow the same structure
3. **Type Safety**: I/O schemas provide validation and documentation
4. **Separation of Concerns**: Business logic separate from routing
5. **Flexibility**: Easy to add new routes/nodes without code changes
6. **Testing**: Each component can be tested in isolation

## Migration Checklist

- [ ] Update NodeConfig base class with routing support
- [ ] Add routing strategies (StateField, EngineTool, Conditional, etc.)
- [ ] Update ValidationNodeConfig to use engine_name pattern
- [ ] Update ToolNodeConfig to use engine_name pattern
- [ ] Update EngineNodeConfig with auto I/O detection
- [ ] Update ParserNodeConfig (already correct)
- [ ] Add function wrapping support
- [ ] Add looping support for batch operations
- [ ] Update graph builder to handle dynamic routing
- [ ] Create migration guide for existing nodes
- [ ] Add comprehensive tests
- [ ] Update documentation

This implementation provides a complete solution for dynamic routing while maintaining consistency and type safety across the entire Haive framework.
