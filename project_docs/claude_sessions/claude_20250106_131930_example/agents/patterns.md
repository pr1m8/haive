# Reusable Agent Patterns

## Pattern: Basic Agent Structure

```python
from haive.agents.base import Agent
from haive.core.schema import StateSchema
from haive.core.graph import BaseGraph
from pydantic import Field
from typing import List, Dict, Any, Optional

class CustomAgentState(StateSchema):
    """State schema for custom agent."""
    messages: List[str] = Field(default_factory=list)
    context: Dict[str, Any] = Field(default_factory=dict)

class CustomAgent(Agent[CustomAgentState]):
    """Custom agent implementation."""

    def __init__(
        self,
        name: str,
        engine: Any,
        **kwargs
    ) -> None:
        super().__init__(
            name=name,
            state_schema=CustomAgentState,
            **kwargs
        )
        self.engine = engine

    def setup_agent(self) -> None:
        """Initialize agent components."""
        self._sync_fields_from_engine()
        self._setup_schemas()
        self._build_initial_graph()

    def build_graph(self) -> BaseGraph:
        """Define agent workflow."""
        graph = BaseGraph()

        # Add your nodes here
        graph.add_node("start", self._process_input)
        graph.add_node("end", self._generate_output)

        # Define edges
        graph.add_edge("start", "end")
        graph.set_entry_point("start")

        return graph.compile()
```

## Pattern: Multi-Engine Agent

```python
class MultiEngineAgent(Agent[MultiEngineState]):
    """Agent using multiple engines for different tasks."""

    def __init__(
        self,
        name: str,
        main_engine: Any,
        tool_engine: Any,
        **kwargs
    ) -> None:
        super().__init__(name=name, **kwargs)
        self.main_engine = main_engine
        self.tool_engine = tool_engine

        # Register engines
        registry = EngineRegistry.get_instance()
        registry.register(main_engine)
        registry.register(tool_engine)

    def build_graph(self) -> BaseGraph:
        """Build graph with engine routing."""
        graph = BaseGraph()

        # Router node decides which engine
        graph.add_node("router", self._route_request)
        graph.add_node("main", self._use_main_engine)
        graph.add_node("tools", self._use_tool_engine)

        # Conditional routing
        graph.add_conditional_edge(
            "router",
            self._needs_tools,
            {
                True: "tools",
                False: "main"
            }
        )

        return graph.compile()
```

## Pattern: Streaming Agent

```python
class StreamingAgent(Agent[StreamingState]):
    """Agent with streaming response support."""

    async def astream(
        self,
        input_data: str,
        config: Optional[Dict] = None
    ) -> AsyncGenerator[str, None]:
        """Stream responses token by token."""
        # Initialize state
        state = self._prepare_state(input_data, config)

        # Stream from engine
        async for token in self.engine.astream(state):
            # Process token
            processed = self._process_token(token)

            # Yield to caller
            yield processed

            # Update state
            state = self._update_streaming_state(state, token)
```

## Pattern: Error Recovery Agent

```python
class ResilientAgent(Agent[ResilientState]):
    """Agent with error recovery capabilities."""

    async def arun_with_retry(
        self,
        input_data: str,
        max_retries: int = 3,
        backoff: float = 1.0
    ) -> str:
        """Run with automatic retry on failure."""
        last_error = None

        for attempt in range(max_retries):
            try:
                result = await self.arun(input_data)
                return result

            except AgentError as e:
                last_error = e
                if attempt < max_retries - 1:
                    # Log retry
                    logger.warning(
                        f"Attempt {attempt + 1} failed, retrying",
                        extra={"error": str(e), "agent": self.name}
                    )

                    # Exponential backoff
                    await asyncio.sleep(backoff * (2 ** attempt))

                    # Optionally modify approach
                    self._adjust_strategy(e)

        raise AgentError(f"Failed after {max_retries} attempts: {last_error}")
```

## Pattern: Validating Agent

```python
class ValidatingAgent(Agent[ValidatedState]):
    """Agent with input/output validation."""

    def __init__(self, *args, validators: List[Validator], **kwargs):
        super().__init__(*args, **kwargs)
        self.validators = validators

    async def arun(self, input_data: str, config: Optional[Dict] = None) -> str:
        """Run with validation."""
        # Validate input
        for validator in self.validators:
            if not validator.validate_input(input_data):
                raise ValidationError(f"Input failed {validator.name} validation")

        # Process normally
        result = await super().arun(input_data, config)

        # Validate output
        for validator in self.validators:
            if not validator.validate_output(result):
                # Attempt to fix
                result = validator.fix_output(result)

        return result
```

## Pattern: Caching Agent

```python
from functools import lru_cache
import hashlib

class CachingAgent(Agent[CachingState]):
    """Agent with response caching."""

    def __init__(self, *args, cache_size: int = 100, **kwargs):
        super().__init__(*args, **kwargs)
        self._cache = {}
        self._cache_size = cache_size

    def _get_cache_key(self, input_data: str, config: Dict) -> str:
        """Generate cache key from input."""
        key_data = f"{input_data}:{json.dumps(config, sort_keys=True)}"
        return hashlib.md5(key_data.encode()).hexdigest()

    async def arun(self, input_data: str, config: Optional[Dict] = None) -> str:
        """Run with caching."""
        config = config or {}

        # Check cache
        cache_key = self._get_cache_key(input_data, config)
        if cache_key in self._cache:
            logger.info(f"Cache hit for {cache_key}")
            return self._cache[cache_key]

        # Process normally
        result = await super().arun(input_data, config)

        # Update cache
        self._cache[cache_key] = result

        # Evict old entries if needed
        if len(self._cache) > self._cache_size:
            oldest = next(iter(self._cache))
            del self._cache[oldest]

        return result
```
