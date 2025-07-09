"""Engine detection and base class determination for schema composition."""

import logging
from typing import Any, List, Type

logger = logging.getLogger(__name__)


class EngineDetectorMixin:
    """Mixin that handles engine detection and base class selection.

    This mixin analyzes components to determine:
    - What type of engines are present
    - Whether tools or messages are needed
    - Which base class to use (StateSchema, MessagesState, ToolState)
    """

    def __init__(self, *args, **kwargs):
        """Initialize detection flags."""
        super().__init__(*args, **kwargs)

        # Detection flags
        self.has_messages = False
        self.has_tools = False
        self.detected_base_class = None
        self.base_class_fields = set()

    def _detect_base_class_requirements(self, components: List[Any] = None) -> None:
        """Detect what base class is needed based on components.

        Args:
            components: Optional list of components to analyze
        """
        logger.debug("Detecting base class requirements")

        # Check current fields first
        if "messages" in self.fields or self.has_messages:
            self.has_messages = True

        if "tools" in self.fields or self.has_tools:
            self.has_tools = True

        # Enhanced component analysis - prioritize engine type detection
        if components:
            for component in components:
                if component is None:
                    continue

                # PRIORITY 1: Check for AugLLM engines specifically
                if hasattr(component, "engine_type"):
                    engine_type_value = getattr(
                        component.engine_type, "value", component.engine_type
                    )
                    engine_type_str = str(engine_type_value).lower()

                    if engine_type_str == "llm":
                        logger.debug(
                            f"Found AugLLM engine: {getattr(component, 'name', 'unnamed')}"
                        )
                        self.has_messages = True

                        # Check if this AugLLM has tools
                        if hasattr(component, "tools") and component.tools:
                            logger.debug("AugLLM has tools - will use ToolState")
                            self.has_tools = True

                # PRIORITY 2: Check for agent-like components
                elif hasattr(component, "agent") or getattr(
                    component, "__class__", None
                ).__name__.lower().endswith("agent"):
                    logger.debug(
                        f"Found agent component: {getattr(component, 'name', getattr(component, '__class__', {}).get('__name__', 'unnamed'))}"
                    )
                    self.has_messages = True

                    # Check if agent has tools
                    if hasattr(component, "tools") and component.tools:
                        logger.debug("Agent has tools - will use ToolState")
                        self.has_tools = True

                # PRIORITY 3: Check for standalone tools
                elif hasattr(component, "tools") and component.tools:
                    logger.debug("Found component with tools")
                    self.has_tools = True

                # PRIORITY 4: Check for messages in engine I/O
                if hasattr(component, "get_input_fields") and callable(
                    component.get_input_fields
                ):
                    try:
                        input_fields = component.get_input_fields()
                        if "messages" in input_fields:
                            self.has_messages = True
                            logger.debug("Found 'messages' in input fields")
                    except Exception:
                        pass

                if hasattr(component, "get_output_fields") and callable(
                    component.get_output_fields
                ):
                    try:
                        output_fields = component.get_output_fields()
                        if "messages" in output_fields:
                            self.has_messages = True
                            logger.debug("Found 'messages' in output fields")
                    except Exception:
                        pass

        # Determine base class with proper priority
        if self.has_tools:
            from haive.core.schema.prebuilt.tool_state import ToolState

            base_class = ToolState
            logger.debug("Using ToolState as base class (found tools)")
        elif self.has_messages:
            from haive.core.schema.prebuilt.messages_state import MessagesState

            base_class = MessagesState
            logger.debug("Using MessagesState as base class (found messages)")
        else:
            from haive.core.schema.state_schema import StateSchema

            base_class = StateSchema
            logger.debug("Using StateSchema as base class (default)")

        self.detected_base_class = base_class

        # Extract fields from base class to avoid duplicates
        if hasattr(base_class, "model_fields"):
            self.base_class_fields = set(base_class.model_fields.keys())
            logger.debug(f"Base class provides fields: {self.base_class_fields}")
        else:
            self.base_class_fields = set()

    def get_detected_base_class(self) -> Type:
        """Get the detected base class.

        Returns:
            The base class that should be used for schema generation
        """
        if self.detected_base_class is None:
            self._detect_base_class_requirements()
        return self.detected_base_class

    def requires_messages(self) -> bool:
        """Check if the schema requires message handling."""
        return self.has_messages

    def requires_tools(self) -> bool:
        """Check if the schema requires tool handling."""
        return self.has_tools
