"""Module exports."""

# Existing reflection patterns
from haive.agents.reflection.agent import (
    ExpertAgent,
    GradedReflectionMultiAgent,
    GradingAgent,
    PrePostMultiAgent,
    ReflectionAgent,
    ReflectionMultiAgent,
    StructuredOutputMultiAgent,
    ToolBasedReflectionAgent,
    create,
    create_expert_agent,
    create_graded_reflection_agent,
    create_reflection_agent,
    create_tool_based_reflection_agent,
    model_post_init,
)

# New message transformer reflection patterns
from haive.agents.reflection.message_transformer import (
    ConversationalReflectionAgent,
    MessageTransformerReflectionAgent,
    ReflectionMessageFlow,
    create_conversational_reflection_agent,
    create_message_transformer_reflection_agent,
    create_reflection_context_transformer,
    create_reflection_message_flow,
)
from haive.agents.reflection.prompts import (
    create_expert_prompt,
    create_grading_prompt,
    create_improvement_prompt,
    create_reflection_prompt,
)
from haive.agents.reflection.simple_agent import ReflectionAgent, create, enhance_agent
from haive.agents.reflection.state import (
    ReflectionState,
    add_improvement,
    finalize,
    should_continue,
)

# New structured output reflection patterns
from haive.agents.reflection.structured_output import (
    ReflectionLoop,
    StructuredImprovementAgent,
    StructuredReflectionAgent,
    create_improvement_agent,
)
from haive.agents.reflection.structured_output import (
    create_reflection_agent as create_structured_reflection_agent,
)
from haive.agents.reflection.structured_output import (
    create_reflection_loop,
    extract_structured_output,
)

from .models import (  # Add new models
    Critique,
    ExpertiseConfig,
    GradingResult,
    Improvement,
    ImprovementSuggestion,
    QualityScore,
    ReflectionConfig,
    ReflectionOutput,
    ReflectionResult,
    to_prompt,
    validate_grade_matches_score,
)

# Models already imported above

__all__ = [
    # Existing reflection patterns
    "ExpertAgent",
    "ExpertiseConfig",
    "GradedReflectionMultiAgent",
    "GradingAgent",
    "GradingResult",
    "ImprovementSuggestion",
    "PrePostMultiAgent",
    "QualityScore",
    "ReflectionAgent",
    "ReflectionConfig",
    "ReflectionMultiAgent",
    "ReflectionOutput",
    "ReflectionState",
    "StructuredOutputMultiAgent",
    "ToolBasedReflectionAgent",
    "add_improvement",
    "create",
    "create_expert_agent",
    "create_expert_prompt",
    "create_graded_reflection_agent",
    "create_grading_prompt",
    "create_improvement_prompt",
    "create_reflection_agent",
    "create_reflection_prompt",
    "create_tool_based_reflection_agent",
    "enhance_agent",
    "finalize",
    "model_post_init",
    "should_continue",
    "to_prompt",
    "validate_grade_matches_score",
    # New structured output reflection patterns
    "StructuredReflectionAgent",
    "StructuredImprovementAgent",
    "ReflectionLoop",
    "create_structured_reflection_agent",
    "create_improvement_agent",
    "create_reflection_loop",
    "extract_structured_output",
    # New message transformer reflection patterns
    "MessageTransformerReflectionAgent",
    "ConversationalReflectionAgent",
    "ReflectionMessageFlow",
    "create_message_transformer_reflection_agent",
    "create_conversational_reflection_agent",
    "create_reflection_message_flow",
    "create_reflection_context_transformer",
    # Shared models for new patterns
    "Critique",
    "Improvement",
    "ReflectionResult",
]
