# src/haive/agents/base/hooks.py

"""Hook system for agent lifecycle events.

This module provides a flexible hook system that allows users to inject
custom logic at various points in agent execution.

The hook system supports the following event types:
- Lifecycle: setup, graph building
- Execution: before/after run and arun
- Node execution: before/after individual nodes
- Error handling: errors and retries
- State management: state updates

Examples:
    Basic hook usage::

        from haive.agents.simple import SimpleAgent
        from haive.agents.base.hooks import HookEvent, logging_hook

        agent = SimpleAgent(name="my_agent")

        # Add logging hook
        agent.add_hook(HookEvent.BEFORE_RUN, logging_hook)

        # Add custom hook
        def my_hook(context):
            print(f"Starting {context.agent_name}")

        agent.add_hook(HookEvent.BEFORE_RUN, my_hook)

    Using decorators::

        agent = SimpleAgent(name="my_agent")

        @agent.before_run
        def log_start(context):
            print(f"Starting execution of {context.agent_name}")

        @agent.after_run
        def log_end(context):
            print(f"Completed: {context.output_data}")

    Error handling::

        @agent.on_error
        def handle_error(context):
            logger.error(f"Error in {context.agent_name}: {context.error}")
            # Could send alerts, retry, etc.

Note:
    Hooks are executed in the order they were added. Hook errors are caught
    and logged but don't interrupt agent execution. Use hooks for monitoring,
    logging, metrics, validation, and other cross-cutting concerns.
"""

import logging
from collections.abc import Callable
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class HookEvent(str, Enum):
    """Events where hooks can be attached."""

    # Lifecycle hooks
    BEFORE_SETUP = "before_setup"
    AFTER_SETUP = "after_setup"
    BEFORE_BUILD_GRAPH = "before_build_graph"
    AFTER_BUILD_GRAPH = "after_build_graph"

    # Execution hooks
    BEFORE_RUN = "before_run"
    AFTER_RUN = "after_run"
    BEFORE_ARUN = "before_arun"
    AFTER_ARUN = "after_arun"

    # Node execution hooks
    BEFORE_NODE = "before_node"
    AFTER_NODE = "after_node"

    # Error hooks
    ON_ERROR = "on_error"
    ON_RETRY = "on_retry"

    # State hooks
    BEFORE_STATE_UPDATE = "before_state_update"
    AFTER_STATE_UPDATE = "after_state_update"

    # Pre/Post processing hooks
    PRE_PROCESS = "pre_process"
    POST_PROCESS = "post_process"
    
    # Message transformation hooks
    BEFORE_MESSAGE_TRANSFORM = "before_message_transform"
    AFTER_MESSAGE_TRANSFORM = "after_message_transform"
    
    # Reflection and critique hooks
    BEFORE_REFLECTION = "before_reflection"
    AFTER_REFLECTION = "after_reflection"
    BEFORE_GRADING = "before_grading"
    AFTER_GRADING = "after_grading"
    
    # Structured output hooks
    BEFORE_STRUCTURED_OUTPUT = "before_structured_output"
    AFTER_STRUCTURED_OUTPUT = "after_structured_output"


class HookContext(BaseModel):
    """Context passed to hook functions."""

    model_config = {"arbitrary_types_allowed": True}

    event: HookEvent = Field(..., description="The hook event")
    agent_name: str = Field(..., description="Name of the agent")
    agent_type: str = Field(..., description="Type of the agent")

    # Optional fields depending on event
    input_data: Any | None = Field(default=None, description="Input data")
    output_data: Any | None = Field(default=None, description="Output data")
    error: Exception | None = Field(default=None, description="Error if any")
    node_name: str | None = Field(default=None, description="Current node name")
    state: dict[str, Any] | None = Field(default=None, description="Current state")
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata"
    )
    
    # Additional fields for enhanced hook patterns
    messages: list[Any] | None = Field(default=None, description="Messages being processed")
    transformed_messages: list[Any] | None = Field(default=None, description="Transformed messages")
    original_messages: list[Any] | None = Field(default=None, description="Original messages before transformation")
    structured_data: Any | None = Field(default=None, description="Structured data from processing")
    grade_data: dict[str, Any] | None = Field(default=None, description="Grading results")
    reflection_data: dict[str, Any] | None = Field(default=None, description="Reflection results")
    transformation_type: str | None = Field(default=None, description="Type of message transformation applied")
    pre_agent_result: Any | None = Field(default=None, description="Result from pre-processing agent")
    post_agent_result: Any | None = Field(default=None, description="Result from post-processing agent")


# Hook function type
HookFunction = Callable[[HookContext], Any | None]


class HooksMixin:
    """Mixin that adds hook functionality to agents."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._hooks: dict[HookEvent, list[HookFunction]] = {}

    def add_hook(self, event: HookEvent, hook: HookFunction) -> None:
        """Add a hook function for an event.

        Args:
            event: The event to hook into
            hook: The function to call on the event

        Example:
            agent.add_hook(HookEvent.BEFORE_RUN, lambda ctx: print(f"Running {ctx.agent_name}"))
        """
        if event not in self._hooks:
            self._hooks[event] = []
        self._hooks[event].append(hook)
        logger.debug(
            f"Added hook for {event} on {
                getattr(
                    self,
                    'name',
                    'agent')}"
        )

    def remove_hook(self, event: HookEvent, hook: HookFunction) -> None:
        """Remove a hook function.

        Args:
            event: The event to remove the hook from
            hook: The hook function to remove
        """
        if event in self._hooks and hook in self._hooks[event]:
            self._hooks[event].remove(hook)
            logger.debug(
                f"Removed hook for {event} on {getattr(self, 'name', 'agent')}"
            )

    def clear_hooks(self, event: HookEvent | None = None) -> None:
        """Clear hooks for an event or all events.

        Args:
            event: Specific event to clear hooks for, or None for all events
        """
        if event:
            self._hooks[event] = []
            logger.debug(
                f"Cleared hooks for {event} on {
                    getattr(
                        self,
                        'name',
                        'agent')}"
            )
        else:
            self._hooks.clear()
            logger.debug(
                f"Cleared all hooks on {
                    getattr(
                        self,
                        'name',
                        'agent')}"
            )

    def _execute_hooks(self, event: HookEvent, **context_kwargs) -> list[Any]:
        """Execute all hooks for an event.

        Args:
            event: The event to execute hooks for
            **context_kwargs: Additional context to pass to hooks

        Returns:
            List of results from hook functions
        """
        if event not in self._hooks or not self._hooks[event]:
            return []

        # Create context
        context = HookContext(
            event=event,
            agent_name=getattr(self, "name", "unknown"),
            agent_type=self.__class__.__name__,
            **context_kwargs,
        )

        results = []
        for hook in self._hooks[event]:
            try:
                result = hook(context)
                if result is not None:
                    results.append(result)
            except Exception as e:
                logger.exception(f"Error in hook for {event}: {e}")
                # Don't let hook errors break execution
                continue

        return results

    # ========================================================================
    # HOOK DECORATORS
    # ========================================================================

    def before_setup(self, func: HookFunction) -> HookFunction:
        """Decorator to add a before_setup hook."""
        self.add_hook(HookEvent.BEFORE_SETUP, func)
        return func

    def after_setup(self, func: HookFunction) -> HookFunction:
        """Decorator to add an after_setup hook."""
        self.add_hook(HookEvent.AFTER_SETUP, func)
        return func

    def before_run(self, func: HookFunction) -> HookFunction:
        """Decorator to add a before_run hook."""
        self.add_hook(HookEvent.BEFORE_RUN, func)
        return func

    def after_run(self, func: HookFunction) -> HookFunction:
        """Decorator to add an after_run hook."""
        self.add_hook(HookEvent.AFTER_RUN, func)
        return func

    def on_error(self, func: HookFunction) -> HookFunction:
        """Decorator to add an on_error hook."""
        self.add_hook(HookEvent.ON_ERROR, func)
        return func

    def pre_process(self, func: HookFunction) -> HookFunction:
        """Decorator to add a pre_process hook."""
        self.add_hook(HookEvent.PRE_PROCESS, func)
        return func

    def post_process(self, func: HookFunction) -> HookFunction:
        """Decorator to add a post_process hook."""
        self.add_hook(HookEvent.POST_PROCESS, func)
        return func

    def before_message_transform(self, func: HookFunction) -> HookFunction:
        """Decorator to add a before_message_transform hook."""
        self.add_hook(HookEvent.BEFORE_MESSAGE_TRANSFORM, func)
        return func

    def after_message_transform(self, func: HookFunction) -> HookFunction:
        """Decorator to add an after_message_transform hook."""
        self.add_hook(HookEvent.AFTER_MESSAGE_TRANSFORM, func)
        return func

    def before_reflection(self, func: HookFunction) -> HookFunction:
        """Decorator to add a before_reflection hook."""
        self.add_hook(HookEvent.BEFORE_REFLECTION, func)
        return func

    def after_reflection(self, func: HookFunction) -> HookFunction:
        """Decorator to add an after_reflection hook."""
        self.add_hook(HookEvent.AFTER_REFLECTION, func)
        return func

    def before_grading(self, func: HookFunction) -> HookFunction:
        """Decorator to add a before_grading hook."""
        self.add_hook(HookEvent.BEFORE_GRADING, func)
        return func

    def after_grading(self, func: HookFunction) -> HookFunction:
        """Decorator to add an after_grading hook."""
        self.add_hook(HookEvent.AFTER_GRADING, func)
        return func

    def before_structured_output(self, func: HookFunction) -> HookFunction:
        """Decorator to add a before_structured_output hook."""
        self.add_hook(HookEvent.BEFORE_STRUCTURED_OUTPUT, func)
        return func

    def after_structured_output(self, func: HookFunction) -> HookFunction:
        """Decorator to add an after_structured_output hook."""
        self.add_hook(HookEvent.AFTER_STRUCTURED_OUTPUT, func)
        return func


# ========================================================================
# COMMON HOOK FUNCTIONS
# ========================================================================


def logging_hook(context: HookContext) -> None:
    """Log hook events.

    A general-purpose logging hook that logs event details at appropriate levels.

    Args:
        context: Hook context with event details.

    Note:
        Uses INFO level for events, DEBUG for data, ERROR for errors.
    """
    logger.info(f"Hook {context.event} triggered for {context.agent_name}")
    if context.input_data:
        logger.debug(f"Input: {context.input_data}")
    if context.output_data:
        logger.debug(f"Output: {context.output_data}")
    if context.error:
        logger.error(f"Error: {context.error}")


def timing_hook(context: HookContext) -> None:
    """Track execution time.

    Measures and logs the execution time between BEFORE_RUN/ARUN and AFTER_RUN/ARUN events.

    Args:
        context: Hook context. Uses context.metadata to store start time.

    Note:
        Must be added to both BEFORE and AFTER events to work properly.

    Example:
        agent.add_hook(HookEvent.BEFORE_RUN, timing_hook)
        agent.add_hook(HookEvent.AFTER_RUN, timing_hook)
    """
    import time

    if context.event in (HookEvent.BEFORE_RUN, HookEvent.BEFORE_ARUN):
        context.metadata["start_time"] = time.time()
    elif context.event in (HookEvent.AFTER_RUN, HookEvent.AFTER_ARUN):
        if "start_time" in context.metadata:
            elapsed = time.time() - context.metadata["start_time"]
            logger.info(f"{context.agent_name} execution took {elapsed:.2f}s")


def state_validation_hook(context: HookContext) -> None:
    """Validate state updates."""
    if context.event == HookEvent.BEFORE_STATE_UPDATE and context.state:
        # Add validation logic here
        required_fields = ["messages"]
        for field in required_fields:
            if field not in context.state:
                logger.warning(f"Missing required field in state: {field}")


def retry_limit_hook(max_retries: int = 3) -> HookFunction:
    """Create a hook that limits retries.

    Factory function that creates a hook to limit retry attempts per agent/node.

    Args:
        max_retries: Maximum number of retries allowed per agent/node combination.

    Returns:
        A hook function that tracks and limits retries.

    Raises:
        Exception: When retry limit is exceeded.

    Example:
        agent.add_hook(HookEvent.ON_RETRY, retry_limit_hook(max_retries=5))
    """
    retry_count = {}

    def hook(context: HookContext) -> None:
        if context.event == HookEvent.ON_RETRY:
            key = f"{context.agent_name}:{context.node_name}"
            retry_count[key] = retry_count.get(key, 0) + 1
            if retry_count[key] > max_retries:
                raise Exception(f"Max retries ({max_retries}) exceeded for {key}")

    return hook


def message_transformation_hook(context: HookContext) -> None:
    """Log message transformation events.
    
    Logs details about message transformations including the transformation type
    and number of messages processed.
    
    Args:
        context: Hook context with transformation details.
    """
    if context.event == HookEvent.BEFORE_MESSAGE_TRANSFORM:
        logger.info(f"Starting message transformation for {context.agent_name}")
        if context.messages:
            logger.debug(f"Input messages: {len(context.messages)} messages")
        if context.transformation_type:
            logger.debug(f"Transformation type: {context.transformation_type}")
    
    elif context.event == HookEvent.AFTER_MESSAGE_TRANSFORM:
        logger.info(f"Message transformation completed for {context.agent_name}")
        if context.transformed_messages:
            logger.debug(f"Output messages: {len(context.transformed_messages)} messages")
        if context.original_messages and context.transformed_messages:
            logger.debug(
                f"Messages transformed: {len(context.original_messages)} -> "
                f"{len(context.transformed_messages)}"
            )


def reflection_hook(context: HookContext) -> None:
    """Log reflection events and provide insights.
    
    Tracks reflection processing including grading and improvement suggestions.
    
    Args:
        context: Hook context with reflection details.
    """
    if context.event == HookEvent.BEFORE_REFLECTION:
        logger.info(f"Starting reflection for {context.agent_name}")
        if context.grade_data:
            logger.debug(f"Using grade data for reflection context")
    
    elif context.event == HookEvent.AFTER_REFLECTION:
        logger.info(f"Reflection completed for {context.agent_name}")
        if context.reflection_data:
            logger.debug(f"Reflection insights generated")


def grading_hook(context: HookContext) -> None:
    """Log grading events and track quality metrics.
    
    Monitors grading processes and logs quality assessment results.
    
    Args:
        context: Hook context with grading details.
    """
    if context.event == HookEvent.BEFORE_GRADING:
        logger.info(f"Starting grading for {context.agent_name}")
    
    elif context.event == HookEvent.AFTER_GRADING:
        logger.info(f"Grading completed for {context.agent_name}")
        if context.grade_data and isinstance(context.grade_data, dict):
            score = context.grade_data.get("score")
            if score is not None:
                logger.info(f"Grade score: {score}")


def structured_output_hook(context: HookContext) -> None:
    """Log structured output processing events.
    
    Tracks structural output parsing and validation.
    
    Args:
        context: Hook context with structured output details.
    """
    if context.event == HookEvent.BEFORE_STRUCTURED_OUTPUT:
        logger.info(f"Starting structured output processing for {context.agent_name}")
        if context.input_data:
            logger.debug("Input data available for structuring")
    
    elif context.event == HookEvent.AFTER_STRUCTURED_OUTPUT:
        logger.info(f"Structured output processing completed for {context.agent_name}")
        if context.structured_data:
            data_type = type(context.structured_data).__name__
            logger.debug(f"Structured output type: {data_type}")


def pre_post_processing_hook(context: HookContext) -> None:
    """Log pre/post processing events.
    
    Monitors pre and post processing stages in multi-agent workflows.
    
    Args:
        context: Hook context with processing details.
    """
    if context.event == HookEvent.PRE_PROCESS:
        logger.info(f"Pre-processing started for {context.agent_name}")
        if context.input_data:
            logger.debug("Input data received for pre-processing")
    
    elif context.event == HookEvent.POST_PROCESS:
        logger.info(f"Post-processing completed for {context.agent_name}")
        if context.output_data:
            logger.debug("Output data processed")
        if context.pre_agent_result and context.post_agent_result:
            logger.debug("Both pre and post agent results available")


def comprehensive_workflow_hook(context: HookContext) -> None:
    """Comprehensive hook that logs all workflow events.
    
    A single hook that can handle all types of workflow events for complete
    monitoring and debugging of agent execution.
    
    Args:
        context: Hook context with event details.
    """
    event_type = context.event.value
    
    # Core execution events
    if context.event in (HookEvent.BEFORE_RUN, HookEvent.BEFORE_ARUN):
        logger.info(f"🚀 Starting execution: {context.agent_name}")
        if context.input_data:
            logger.debug(f"Input: {str(context.input_data)[:100]}...")
    
    elif context.event in (HookEvent.AFTER_RUN, HookEvent.AFTER_ARUN):
        logger.info(f"✅ Execution completed: {context.agent_name}")
        if context.output_data:
            logger.debug(f"Output: {str(context.output_data)[:100]}...")
    
    # Message processing events
    elif "message" in event_type:
        message_transformation_hook(context)
    
    # Reflection and grading events
    elif "reflection" in event_type:
        reflection_hook(context)
    elif "grading" in event_type:
        grading_hook(context)
    
    # Structured output events
    elif "structured_output" in event_type:
        structured_output_hook(context)
    
    # Pre/post processing events
    elif context.event in (HookEvent.PRE_PROCESS, HookEvent.POST_PROCESS):
        pre_post_processing_hook(context)
    
    # Error events
    elif context.event == HookEvent.ON_ERROR:
        logger.error(f"❌ Error in {context.agent_name}: {context.error}")
    
    # General events
    else:
        logger.debug(f"Hook event: {event_type} for {context.agent_name}")


def create_multi_stage_hook(stages: list[str]) -> HookFunction:
    """Create a hook that tracks multi-stage agent workflows.
    
    Factory function for creating hooks that monitor complex workflows
    like reflection, grading, and structured output processing.
    
    Args:
        stages: List of stage names to track (e.g., ["grading", "reflection", "improvement"])
        
    Returns:
        A hook function that tracks multi-stage workflows.
        
    Example:
        hook = create_multi_stage_hook(["grading", "reflection", "improvement"])
        agent.add_hook(HookEvent.PRE_PROCESS, hook)
        agent.add_hook(HookEvent.POST_PROCESS, hook)
    """
    stage_data = {}
    
    def hook(context: HookContext) -> None:
        agent_key = context.agent_name
        
        if context.event == HookEvent.PRE_PROCESS:
            stage_data[agent_key] = {
                "stages": stages,
                "current_stage": 0,
                "start_time": __import__("time").time(),
                "stage_results": {}
            }
            logger.info(f"🔄 Multi-stage workflow started for {agent_key}: {' → '.join(stages)}")
        
        elif context.event == HookEvent.POST_PROCESS:
            if agent_key in stage_data:
                workflow_data = stage_data[agent_key]
                elapsed = __import__("time").time() - workflow_data["start_time"]
                logger.info(f"✅ Multi-stage workflow completed for {agent_key} in {elapsed:.2f}s")
                
                # Log stage results
                for stage, result in workflow_data["stage_results"].items():
                    logger.debug(f"  Stage '{stage}': {result}")
                
                # Clean up
                del stage_data[agent_key]
        
        # Track individual stages
        elif context.event in (HookEvent.AFTER_GRADING, HookEvent.AFTER_REFLECTION, 
                              HookEvent.AFTER_STRUCTURED_OUTPUT):
            if agent_key in stage_data:
                stage_name = context.event.value.replace("after_", "")
                if stage_name in stages:
                    stage_data[agent_key]["stage_results"][stage_name] = "completed"
                    logger.debug(f"  ✓ Stage '{stage_name}' completed for {agent_key}")
    
    return hook
