"""Pre/Post Agent Processing Mixin.

This mixin generalizes the pre/post agent pattern from the reflection agents
to the enhanced base agent, allowing any agent to have pre-processing and
post-processing stages with message transformation support.

The pattern supports:
- Optional pre-processing agent
- Main agent processing
- Optional post-processing agent
- Message transformation between stages
- Hook integration for monitoring

Examples:
    Basic usage with reflection::

        class MyReflectionAgent(Agent, PrePostAgentMixin):
            def setup_agent(self):
                # Set up main agent
                self.main_agent = SimpleAgent(name="writer", engine=config)

                # Set up post-processing with reflection
                self.post_agent = SimpleAgent(name="reflector", engine=reflection_config)
                self.use_post_transform = True
                self.post_transform_type = "reflection"

    Graded reflection pattern::

        class MyGradedAgent(Agent, PrePostAgentMixin):
            def setup_agent(self):
                self.pre_agent = SimpleAgent(name="grader", engine=grading_config)
                self.main_agent = SimpleAgent(name="responder", engine=main_config)
                self.post_agent = SimpleAgent(name="improver", engine=reflection_config)

                self.use_pre_transform = False
                self.use_post_transform = True

    Factory pattern::

        agent = create_reflection_agent(
            main_agent=SimpleAgent(name="writer", engine=config),
            reflection_type="graded"
        )
"""

import logging
from typing import Any, Dict, Generic, List, Optional, TypeVar

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from pydantic import BaseModel, Field

from haive.agents.base.hooks import HookContext, HookEvent

logger = logging.getLogger(__name__)

# Generic type variables for agents
TPreAgent = TypeVar("TPreAgent", bound="Agent")
TMainAgent = TypeVar("TMainAgent", bound="Agent")
TPostAgent = TypeVar("TPostAgent", bound="Agent")


class MessageTransformer:
    """Simple message transformer for reflection patterns."""

    def __init__(
        self, transformation_type: str = "reflection", preserve_first: bool = True
    ):
        """Initialize transformer.

        Args:
            transformation_type: Type of transformation ("reflection", "ai_to_human", etc.)
            preserve_first: Whether to preserve the first message
        """
        self.transformation_type = transformation_type
        self.preserve_first = preserve_first

    def transform_messages(self, messages: List[BaseMessage]) -> List[BaseMessage]:
        """Transform messages according to the transformation type.

        Args:
            messages: Input messages to transform

        Returns:
            Transformed messages
        """
        if not messages:
            return []

        transformed = []
        start_idx = 1 if self.preserve_first and messages else 0

        # Preserve first message if requested
        if self.preserve_first and messages:
            transformed.append(messages[0])

        # Transform remaining messages
        for msg in messages[start_idx:]:
            if self.transformation_type == "reflection":
                # AI -> Human transformation for reflection
                if isinstance(msg, AIMessage):
                    transformed.append(
                        HumanMessage(
                            content=msg.content,
                            additional_kwargs=getattr(msg, "additional_kwargs", {}),
                        )
                    )
                else:
                    transformed.append(msg)
            elif self.transformation_type == "ai_to_human":
                # Simple AI to Human conversion
                if isinstance(msg, AIMessage):
                    transformed.append(HumanMessage(content=msg.content))
                else:
                    transformed.append(msg)
            else:
                # No transformation, pass through
                transformed.append(msg)

        return transformed


class PrePostAgentMixin:
    """Mixin that adds pre/post agent processing capabilities.

    This mixin generalizes the PrePostMultiAgent pattern from reflection agents
    to work with any enhanced agent. It provides:

    - Optional pre-processing agent
    - Main agent processing (the agent this mixin is applied to)
    - Optional post-processing agent
    - Message transformation between stages
    - Hook integration for monitoring
    - Configurable transformation types
    """

    # Agent configuration
    pre_agent: Optional["Agent"] = Field(
        default=None, description="Pre-processing agent"
    )
    post_agent: Optional["Agent"] = Field(
        default=None, description="Post-processing agent"
    )

    # Message transformation config
    use_pre_transform: bool = Field(
        default=False, description="Transform messages before main"
    )
    use_post_transform: bool = Field(
        default=False, description="Transform messages before post"
    )
    pre_transform_type: str = Field(
        default="ai_to_human", description="Type of pre-processing transformation"
    )
    post_transform_type: str = Field(
        default="reflection", description="Type of post-processing transformation"
    )

    # Execution config
    skip_pre_if_empty: bool = Field(
        default=True, description="Skip pre-agent if no input"
    )
    skip_post_if_empty: bool = Field(
        default=False, description="Skip post-agent if no output"
    )

    # Processing config
    combine_results: bool = Field(
        default=True, description="Combine pre/main/post results"
    )
    preserve_original: bool = Field(
        default=True, description="Preserve original messages in result"
    )

    def __init__(self, *args, **kwargs):
        """Initialize the mixin."""
        super().__init__(*args, **kwargs)

        # Initialize transformers
        self._pre_transformer = None
        self._post_transformer = None

    def setup_transformers(self) -> None:
        """Set up message transformers based on configuration."""
        if self.use_pre_transform:
            self._pre_transformer = MessageTransformer(
                transformation_type=self.pre_transform_type, preserve_first=True
            )

        if self.use_post_transform:
            self._post_transformer = MessageTransformer(
                transformation_type=self.post_transform_type, preserve_first=True
            )

    async def run_with_pre_post_processing(self, input_data: Any) -> Dict[str, Any]:
        """Execute the agent with pre/post processing stages.

        This method orchestrates the full pre → main → post workflow with
        proper message transformation and hook integration.

        Args:
            input_data: Input for the agent workflow

        Returns:
            Combined results from all processing stages
        """
        # Initialize transformers if not already done
        if not hasattr(self, "_pre_transformer") or self._pre_transformer is None:
            self.setup_transformers()

        # Execute pre-processing hooks
        if hasattr(self, "execute_hooks"):
            self.execute_hooks(
                HookEvent.PRE_PROCESS,
                input_data=input_data,
                metadata={"stage": "pre_processing"},
            )

        # Stage 1: Pre-processing (optional)
        pre_result = None
        current_input = input_data

        if self.pre_agent and not (self.skip_pre_if_empty and not input_data):
            logger.debug(f"Running pre-processing agent: {self.pre_agent.name}")

            # Execute pre-processing hooks
            if hasattr(self, "execute_hooks"):
                self.execute_hooks(
                    (
                        HookEvent.BEFORE_GRADING
                        if "grading" in getattr(self.pre_agent, "name", "")
                        else HookEvent.BEFORE_NODE
                    ),
                    input_data=current_input,
                    agent_name=self.pre_agent.name,
                )

            pre_result = await self.pre_agent.arun(current_input)

            # Execute post pre-processing hooks
            if hasattr(self, "execute_hooks"):
                self.execute_hooks(
                    (
                        HookEvent.AFTER_GRADING
                        if "grading" in getattr(self.pre_agent, "name", "")
                        else HookEvent.AFTER_NODE
                    ),
                    output_data=pre_result,
                    agent_name=self.pre_agent.name,
                )

            # Transform messages if needed
            if self.use_pre_transform and self._pre_transformer:
                if isinstance(pre_result, dict) and "messages" in pre_result:
                    original_messages = pre_result["messages"]

                    # Execute transformation hooks
                    if hasattr(self, "execute_hooks"):
                        self.execute_hooks(
                            HookEvent.BEFORE_MESSAGE_TRANSFORM,
                            messages=original_messages,
                            transformation_type=self.pre_transform_type,
                        )

                    transformed_messages = self._pre_transformer.transform_messages(
                        original_messages
                    )
                    current_input = {"messages": transformed_messages}

                    if hasattr(self, "execute_hooks"):
                        self.execute_hooks(
                            HookEvent.AFTER_MESSAGE_TRANSFORM,
                            original_messages=original_messages,
                            transformed_messages=transformed_messages,
                            transformation_type=self.pre_transform_type,
                        )

        # Stage 2: Main processing (this agent)
        logger.debug(
            f"Running main agent processing: {getattr(self, 'name', 'unknown')}"
        )

        # Use the agent's own arun method
        main_result = (
            await super().arun(current_input)
            if hasattr(super(), "arun")
            else current_input
        )

        # Stage 3: Post-processing (optional)
        post_result = None
        final_result = main_result

        if self.post_agent and not (self.skip_post_if_empty and not main_result):
            logger.debug(f"Running post-processing agent: {self.post_agent.name}")

            current_post_input = main_result

            # Transform messages for post-processing if needed
            if self.use_post_transform and self._post_transformer:
                if isinstance(main_result, dict) and "messages" in main_result:
                    original_messages = main_result["messages"]

                    # Execute transformation hooks
                    if hasattr(self, "execute_hooks"):
                        self.execute_hooks(
                            HookEvent.BEFORE_MESSAGE_TRANSFORM,
                            messages=original_messages,
                            transformation_type=self.post_transform_type,
                        )

                    transformed_messages = self._post_transformer.transform_messages(
                        original_messages
                    )
                    current_post_input = {"messages": transformed_messages}

                    if hasattr(self, "execute_hooks"):
                        self.execute_hooks(
                            HookEvent.AFTER_MESSAGE_TRANSFORM,
                            original_messages=original_messages,
                            transformed_messages=transformed_messages,
                            transformation_type=self.post_transform_type,
                        )

            # Execute post-processing hooks
            if hasattr(self, "execute_hooks"):
                self.execute_hooks(
                    (
                        HookEvent.BEFORE_REFLECTION
                        if "reflection" in getattr(self.post_agent, "name", "")
                        else HookEvent.BEFORE_NODE
                    ),
                    input_data=current_post_input,
                    agent_name=self.post_agent.name,
                )

            post_result = await self.post_agent.arun(current_post_input)

            if hasattr(self, "execute_hooks"):
                self.execute_hooks(
                    (
                        HookEvent.AFTER_REFLECTION
                        if "reflection" in getattr(self.post_agent, "name", "")
                        else HookEvent.AFTER_NODE
                    ),
                    output_data=post_result,
                    agent_name=self.post_agent.name,
                )

        # Stage 4: Combine results
        if self.combine_results:
            combined_result = {
                "main_result": main_result,
                "processing_stages": {
                    "pre_processing": pre_result is not None,
                    "main_processing": True,
                    "post_processing": post_result is not None,
                },
            }

            if pre_result:
                combined_result["pre_result"] = pre_result

            if post_result:
                combined_result["post_result"] = post_result
                # Use post result as final output if available
                final_result = post_result

            # Preserve original messages if requested
            if (
                self.preserve_original
                and isinstance(main_result, dict)
                and "messages" in main_result
            ):
                combined_result["original_messages"] = main_result["messages"]

            # Add transformation metadata
            if self.use_pre_transform or self.use_post_transform:
                combined_result["transformations_applied"] = {
                    "pre_transform": (
                        self.pre_transform_type if self.use_pre_transform else None
                    ),
                    "post_transform": (
                        self.post_transform_type if self.use_post_transform else None
                    ),
                }

            final_result = combined_result

        # Execute final post-processing hooks
        if hasattr(self, "execute_hooks"):
            self.execute_hooks(
                HookEvent.POST_PROCESS,
                output_data=final_result,
                pre_agent_result=pre_result,
                post_agent_result=post_result,
                metadata={"stage": "post_processing"},
            )

        return final_result

    async def arun(self, input_data: Any) -> Any:
        """Override arun to use pre/post processing if agents are configured.

        Args:
            input_data: Input for the agent

        Returns:
            Result from pre/post processing or standard arun
        """
        # If pre or post agents are configured, use pre/post processing
        if self.pre_agent or self.post_agent:
            return await self.run_with_pre_post_processing(input_data)
        else:
            # Standard execution
            return (
                await super().arun(input_data)
                if hasattr(super(), "arun")
                else input_data
            )


# Factory functions for common patterns


def create_reflection_agent(
    main_agent: "Agent",
    reflection_agent: Optional["Agent"] = None,
    name: Optional[str] = None,
    **kwargs,
) -> "Agent":
    """Create an agent with reflection post-processing.

    Args:
        main_agent: The primary agent that generates responses
        reflection_agent: Optional custom reflection agent
        name: Name for the enhanced agent
        **kwargs: Additional configuration

    Returns:
        Agent with reflection capabilities
    """
    if not reflection_agent:
        from haive.core.engine.aug_llm import AugLLMConfig

        # Import SimpleAgent locally to avoid circular import
        from haive.agents.simple.agent import SimpleAgent

        reflection_agent = SimpleAgent(
            name=f"{main_agent.name}_reflector",
            engine=AugLLMConfig(
                system_message="You are a reflection agent that analyzes and improves responses.",
                temperature=0.3,
            ),
        )

    # Add pre/post processing to main agent
    if hasattr(main_agent, "__dict__"):
        main_agent.post_agent = reflection_agent
        main_agent.use_post_transform = True
        main_agent.post_transform_type = "reflection"

        if hasattr(main_agent, "setup_transformers"):
            main_agent.setup_transformers()

    return main_agent


def create_graded_reflection_agent(
    main_agent: "Agent",
    grading_agent: Optional["Agent"] = None,
    reflection_agent: Optional["Agent"] = None,
    name: Optional[str] = None,
    **kwargs,
) -> "Agent":
    """Create an agent with grading and reflection processing.

    Args:
        main_agent: The primary agent that generates responses
        grading_agent: Optional custom grading agent
        reflection_agent: Optional custom reflection agent
        name: Name for the enhanced agent
        **kwargs: Additional configuration

    Returns:
        Agent with grading and reflection capabilities
    """
    if not grading_agent:
        from haive.core.engine.aug_llm import AugLLMConfig

        # Import SimpleAgent locally to avoid circular import
        from haive.agents.simple.agent import SimpleAgent

        grading_agent = SimpleAgent(
            name=f"{main_agent.name}_grader",
            engine=AugLLMConfig(
                system_message="You are a grading agent that evaluates response quality.",
                temperature=0.1,
            ),
        )

    if not reflection_agent:
        from haive.core.engine.aug_llm import AugLLMConfig

        # Import SimpleAgent locally to avoid circular import
        from haive.agents.simple.agent import SimpleAgent

        reflection_agent = SimpleAgent(
            name=f"{main_agent.name}_reflector",
            engine=AugLLMConfig(
                system_message="You are a reflection agent that improves responses based on grades.",
                temperature=0.3,
            ),
        )

    # Add pre/post processing to main agent
    if hasattr(main_agent, "__dict__"):
        main_agent.pre_agent = grading_agent
        main_agent.post_agent = reflection_agent
        main_agent.use_pre_transform = False  # No pre-transform for grading
        main_agent.use_post_transform = True
        main_agent.post_transform_type = "reflection"

        if hasattr(main_agent, "setup_transformers"):
            main_agent.setup_transformers()

    return main_agent


def create_structured_output_agent(
    main_agent: "Agent",
    output_model: type[BaseModel],
    name: Optional[str] = None,
    **kwargs,
) -> "Agent":
    """Create an agent with structured output post-processing.

    Args:
        main_agent: The primary agent that generates responses
        output_model: Pydantic model for structured output
        name: Name for the enhanced agent
        **kwargs: Additional configuration

    Returns:
        Agent with structured output capabilities
    """
    from haive.core.engine.aug_llm import AugLLMConfig

    from haive.agents.structured_output.agent import StructuredOutputAgent

    # Create structured output agent
    structured_agent = StructuredOutputAgent(
        name=f"{main_agent.name}_structurer",
        engine=AugLLMConfig(
            system_message="You are a structured output processor.", temperature=0.1
        ),
        output_models=[output_model],
    )

    # Add post-processing to main agent
    if hasattr(main_agent, "__dict__"):
        main_agent.post_agent = structured_agent
        main_agent.use_post_transform = (
            False  # No message transform for structured output
        )

        if hasattr(main_agent, "setup_transformers"):
            main_agent.setup_transformers()

    return main_agent
