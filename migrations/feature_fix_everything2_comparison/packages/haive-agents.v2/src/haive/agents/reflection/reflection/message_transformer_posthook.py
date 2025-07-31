"""Message Transformer Reflection Post-Hook Pattern.

This implements the correct reflection pattern using message transformation
as a POST-HOOK following the insights from 2025-01-18:

1. Don't fight the message-only interface - use prompt engineering instead
2. Structured data flows through prompt configuration, not messages
3. Message transformation + prompt partials = powerful combination
4. The flow: Main Agent → Response → Convert to prompt partial → Message Transform → Reflection

This follows the pattern documented in:
- project_docs/memory_index/by_date/2025-01-18/reflection_pattern_insights.md
- project_docs/sessions/active/hook_pattern_conceptual_exploration.md
"""

import asyncio
from typing import Any, TypeVar

from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel

from haive.agents.simple.agent import SimpleAgent

# Import message transformation safely
try:
    from haive.core.graph.node.message_transformation_v2 import (
        TransformationType,
        create_reflection_transformer,
    )

    MESSAGE_TRANSFORMER_AVAILABLE = True
except (ImportError, AttributeError):
    MESSAGE_TRANSFORMER_AVAILABLE = False

    # Fallback transformer
    class SimpleTransformer:
        def __init__(self, preserve_first=True):
            self.preserve_first_message = preserve_first

        def _apply_transformation(
            self, messages: list[BaseMessage]
        ) -> list[BaseMessage]:
            if not messages:
                return []
            transformed = []
            start_idx = 1 if self.preserve_first_message and messages else 0
            if self.preserve_first_message and messages:
                transformed.append(messages[0])

            for msg in messages[start_idx:]:
                if isinstance(msg, AIMessage):
                    transformed.append(
                        HumanMessage(
                            content=msg.content,
                            additional_kwargs=getattr(msg, "additional_kwargs", {}),
                        )
                    )
                elif isinstance(msg, HumanMessage):
                    transformed.append(
                        AIMessage(
                            content=msg.content,
                            additional_kwargs=getattr(msg, "additional_kwargs", {}),
                        )
                    )
                else:
                    transformed.append(msg)
            return transformed


from .models import Critique

T = TypeVar("T", bound=BaseModel)


class MessageTransformerPostHook:
    """Post-hook that applies message transformation for reflection.

    This follows the correct pattern:
    1. Agent produces response (messages)
    2. Extract structured data from messages
    3. Convert to prompt partial (NOT message!)
    4. Apply message transformation
    5. Feed to reflection agent with grade in prompt context
    """

    def __init__(
        self,
        reflection_agent: SimpleAgent,
        transform_type: str = "reflection",
        preserve_first_message: bool = True,
    ):
        """Initialize the post-hook.

        Args:
            reflection_agent: Agent that will do the reflection
            transform_type: Type of message transformation to apply
            preserve_first_message: Whether to preserve first message
        """
        self.reflection_agent = reflection_agent
        self.transform_type = transform_type

        # Create message transformer
        if MESSAGE_TRANSFORMER_AVAILABLE and transform_type == "reflection":
            self.transformer = create_reflection_transformer(
                preserve_first_message=preserve_first_message
            )
        else:
            self.transformer = SimpleTransformer(preserve_first_message)

    async def __call__(
        self,
        agent_result: dict[str, Any],
        original_input: Any = None,
        structured_data: BaseModel | None = None,
    ) -> dict[str, Any]:
        """Apply message transformation and reflection.

        Args:
            agent_result: Result from the main agent
            original_input: Original input to the agent
            structured_data: Optional structured data to inject into prompt

        Returns:
            Enhanced result with reflection applied
        """
        if not isinstance(agent_result, dict) or "messages" not in agent_result:
            return agent_result

        original_messages = agent_result["messages"]

        # Step 1: Apply message transformation
        transformed_messages = self.transformer._apply_transformation(original_messages)

        # Step 2: Prepare reflection prompt with optional structured data
        reflection_input = {"messages": transformed_messages}

        # Step 3: Add structured data as prompt context (NOT as messages)
        if structured_data:
            # Convert structured data to prompt partial context
            if hasattr(structured_data, "model_dump"):
                data_dict = structured_data.model_dump()
            else:
                data_dict = dict(structured_data) if structured_data else {}

            # Add as separate fields for prompt template
            reflection_input.update(data_dict)

        if original_input:
            reflection_input["original_input"] = str(original_input)

        # Step 4: Run reflection agent
        reflection_result = await self.reflection_agent.arun(reflection_input)

        # Step 5: Combine results
        enhanced_result = agent_result.copy()
        enhanced_result.update(
            {
                "original_messages": original_messages,
                "transformed_messages": transformed_messages,
                "reflection_result": reflection_result,
                "transformation_applied": self.transform_type,
                "post_hook_applied": True,
            }
        )

        return enhanced_result


class ReflectionWithGradePostHook(MessageTransformerPostHook):
    """Post-hook that combines grading + message transformation + reflection.

    This implements the exact pattern from the 2025-01-18 insights:
    Main Agent → Response → GradingResult → Convert to prompt partial →
    Message Transform → Reflection Agent (with grade in prompt context)
    """

    def __init__(
        self,
        grading_agent: SimpleAgent,
        reflection_agent: SimpleAgent,
        preserve_first_message: bool = True,
    ):
        """Initialize graded reflection post-hook.

        Args:
            grading_agent: Agent that produces structured grading
            reflection_agent: Agent that does reflection with grade context
            preserve_first_message: Whether to preserve first message
        """
        super().__init__(reflection_agent, "reflection", preserve_first_message)
        self.grading_agent = grading_agent

        # Create reflection prompt that accepts grade context
        self.reflection_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "You are a reflection specialist that improves responses."),
                (
                    "human",
                    """Please improve this response:

{response}

{grade_context}

Provide an enhanced version that addresses any feedback.""",
                ),
            ]
        )

        # Update reflection agent's prompt template
        self.reflection_agent.engine.prompt_template = self.reflection_prompt

    async def __call__(
        self, agent_result: dict[str, Any], original_input: Any = None
    ) -> dict[str, Any]:
        """Apply grading → message transform → reflection with grade context.

        Args:
            agent_result: Result from the main agent
            original_input: Original input to the agent

        Returns:
            Enhanced result with grading and reflection applied
        """
        if not isinstance(agent_result, dict) or "messages" not in agent_result:
            return agent_result

        # Step 1: Extract response content from agent result
        response_content = ""
        for msg in reversed(agent_result["messages"]):
            if hasattr(msg, "content") and msg.content:
                response_content = msg.content
                break

        # Step 2: Grade the response (produces structured output)
        grade_input = {
            "response": response_content,
            "original_query": str(original_input) if original_input else "",
        }

        grade_result = await self.grading_agent.arun(grade_input)

        # Step 3: Extract grading result (assume it's structured)
        grade_data = None
        if isinstance(grade_result, dict) and "messages" in grade_result:
            # Look for structured output in tool calls
            for msg in reversed(grade_result["messages"]):
                if hasattr(msg, "tool_calls") and msg.tool_calls:
                    for tool_call in msg.tool_calls:
                        if isinstance(tool_call, dict) and tool_call.get("args"):
                            grade_data = tool_call["args"]
                            break

        # Step 4: Convert grade to prompt partial (NOT message!)
        grade_context = ""
        if grade_data:
            grade_context = f"""Grade Feedback:
- Score: {grade_data.get('score', 'N/A')}/100
- Letter Grade: {grade_data.get('letter_grade', 'N/A')}
- Strengths: {', '.join(grade_data.get('strengths', []))}
- Weaknesses: {', '.join(grade_data.get('weaknesses', []))}
- Suggestions: {', '.join(grade_data.get('suggestions', []))}"""

        # Step 5: Apply message transformation
        original_messages = agent_result["messages"]
        transformed_messages = self.transformer._apply_transformation(original_messages)

        # Step 6: Run reflection with grade context as prompt partial
        reflection_input = {
            "messages": transformed_messages,
            "response": response_content,
            "grade_context": grade_context,
        }

        reflection_result = await self.reflection_agent.arun(reflection_input)

        # Step 7: Combine all results
        enhanced_result = agent_result.copy()
        enhanced_result.update(
            {
                "original_messages": original_messages,
                "transformed_messages": transformed_messages,
                "grade_result": grade_result,
                "grade_data": grade_data,
                "grade_context": grade_context,
                "reflection_result": reflection_result,
                "transformation_applied": "reflection_with_grade",
                "post_hook_applied": True,
            }
        )

        return enhanced_result


class AgentWithPostHook:
    """Agent wrapper that applies post-hooks after execution.

    This implements the proper hook pattern where:
    1. Base agent executes normally
    2. Post-hooks transform the result
    3. Enhanced result is returned
    """

    def __init__(
        self,
        base_agent: SimpleAgent,
        post_hooks: list[MessageTransformerPostHook] = None,
    ):
        """Initialize agent with post-hooks.

        Args:
            base_agent: The base agent to wrap
            post_hooks: List of post-hooks to apply
        """
        self.base_agent = base_agent
        self.post_hooks = post_hooks or []

    def add_post_hook(self, hook: MessageTransformerPostHook):
        """Add a post-hook."""
        self.post_hooks.append(hook)

    async def arun(self, input_data: Any) -> dict[str, Any]:
        """Run agent with post-hook processing.

        Args:
            input_data: Input for the base agent

        Returns:
            Result after all post-hooks have been applied
        """
        # Step 1: Run base agent
        result = await self.base_agent.arun(input_data)

        # Step 2: Apply post-hooks in sequence
        for hook in self.post_hooks:
            result = await hook(result, input_data)

        return result


# Factory functions for common patterns
def create_reflection_post_hook(
    reflection_prompt_template: ChatPromptTemplate | None = None,
    temperature: float = 0.3,
) -> MessageTransformerPostHook:
    """Create a basic reflection post-hook."""
    if not reflection_prompt_template:
        reflection_prompt_template = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """You are a reflection agent that analyzes responses.
            
Analyze the conversation and provide constructive feedback on:
1. Quality and accuracy
2. Completeness
3. Clarity and communication
4. Areas for improvement""",
                ),
                ("human", "Analyze this conversation and provide reflection insights."),
            ]
        )

    reflection_agent = SimpleAgent(
        name="reflection_agent",
        engine=AugLLMConfig(
            prompt_template=reflection_prompt_template, temperature=temperature
        ),
    )

    return MessageTransformerPostHook(reflection_agent)


def create_graded_reflection_post_hook(
    grading_model: type[BaseModel], temperature: float = 0.2
) -> ReflectionWithGradePostHook:
    """Create a graded reflection post-hook."""
    # Create grading agent with structured output
    grading_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a grading expert that evaluates response quality."),
            (
                "human",
                """Grade this response to the query:

Query: {original_query}
Response: {response}

Provide a detailed grade with score, strengths, weaknesses, and suggestions.""",
            ),
        ]
    )

    grading_agent = SimpleAgent(
        name="grading_agent",
        engine=AugLLMConfig(
            prompt_template=grading_prompt,
            structured_output_model=grading_model,
            structured_output_version="v2",
            temperature=temperature,
        ),
    )

    # Create reflection agent (will be updated with proper prompt in post-hook)
    reflection_agent = SimpleAgent(
        name="reflection_agent", engine=AugLLMConfig(temperature=0.3)
    )

    return ReflectionWithGradePostHook(grading_agent, reflection_agent)


def create_agent_with_reflection(
    base_agent: SimpleAgent, reflection_type: str = "basic"
) -> AgentWithPostHook:
    """Create an agent with reflection post-hook.

    Args:
        base_agent: The base agent to enhance
        reflection_type: Type of reflection ("basic" or "graded")

    Returns:
        Agent wrapped with reflection post-hook
    """
    if reflection_type == "basic":
        post_hook = create_reflection_post_hook()
    elif reflection_type == "graded":
        # Need to import a grading model
        from .models import Critique  # Use existing Critique model

        post_hook = create_graded_reflection_post_hook(Critique)
    else:
        raise ValueError(f"Unknown reflection type: {reflection_type}")

    return AgentWithPostHook(base_agent, [post_hook])


# Example usage functions
async def example_basic_post_hook():
    """Example: Basic message transformer post-hook."""
    print("\n=== Basic Message Transformer Post-Hook Example ===\n")

    # Create base agent
    base_agent = SimpleAgent(
        name="writer",
        engine=AugLLMConfig(
            system_message="You are a helpful writing assistant.", temperature=0.7
        ),
    )

    # Create reflection post-hook
    reflection_hook = create_reflection_post_hook()

    # Wrap agent with post-hook
    enhanced_agent = AgentWithPostHook(base_agent, [reflection_hook])

    # Test query
    query = "Write a brief explanation of quantum computing"

    print(f"Query: {query}")

    # Run with post-hook reflection
    result = await enhanced_agent.arun(query)

    print(f"\n✅ Post-Hook Applied: {result.get('post_hook_applied', False)}")
    print(f"Transformation: {result.get('transformation_applied', 'None')}")

    if "reflection_result" in result:
        refl_result = result["reflection_result"]
        if isinstance(refl_result, dict) and "messages" in refl_result:
            for msg in reversed(refl_result["messages"]):
                if hasattr(msg, "content") and msg.content:
                    print(f"\nReflection Analysis: {msg.content[:200]}...")
                    break


async def example_graded_reflection_post_hook():
    """Example: Graded reflection with message transformation."""
    print("\n\n=== Graded Reflection Post-Hook Example ===\n")

    # Create base agent
    base_agent = SimpleAgent(
        name="explainer",
        engine=AugLLMConfig(
            system_message="You are an educational assistant that explains concepts.",
            temperature=0.6,
        ),
    )

    # Create graded reflection post-hook
    graded_hook = create_graded_reflection_post_hook(Critique)

    # Wrap agent with graded reflection
    enhanced_agent = AgentWithPostHook(base_agent, [graded_hook])

    # Test query
    query = "Explain machine learning in simple terms"

    print(f"Query: {query}")

    # Run with graded reflection
    result = await enhanced_agent.arun(query)

    print(f"\n✅ Post-Hook Applied: {result.get('post_hook_applied', False)}")
    print(f"Transformation: {result.get('transformation_applied', 'None')}")

    # Show grade context
    if "grade_context" in result:
        print("\n📊 Grade Context:")
        print(result["grade_context"])

    # Show reflection result
    if "reflection_result" in result:
        refl_result = result["reflection_result"]
        if isinstance(refl_result, dict) and "messages" in refl_result:
            for msg in reversed(refl_result["messages"]):
                if hasattr(msg, "content") and msg.content:
                    print(f"\nReflection with Grade Context: {msg.content[:300]}...")
                    break


async def example_factory_pattern():
    """Example: Using factory function for quick setup."""
    print("\n\n=== Factory Pattern Example ===\n")

    # Create base agent
    base_agent = SimpleAgent(
        name="summarizer",
        engine=AugLLMConfig(
            system_message="You are a text summarization expert.", temperature=0.4
        ),
    )

    # Use factory to create enhanced agent
    enhanced_agent = create_agent_with_reflection(base_agent, "basic")

    # Test
    long_text = """
    Artificial intelligence (AI) is a broad field of computer science focused on 
    creating systems capable of performing tasks that typically require human 
    intelligence. This includes learning, reasoning, problem-solving, perception, 
    and language understanding. AI systems can be narrow (designed for specific 
    tasks) or general (capable of performing any intellectual task). Machine 
    learning, a subset of AI, enables systems to learn and improve from experience 
    without being explicitly programmed for every scenario.
    """

    query = f"Summarize this text: {long_text}"

    print("Query: Summarize a long text about AI")

    result = await enhanced_agent.arun(query)

    print(f"\n✅ Enhanced with Reflection: {result.get('post_hook_applied', False)}")

    # Show original response
    if "messages" in result:
        for msg in reversed(result["messages"]):
            if hasattr(msg, "content") and msg.content:
                print(f"\nOriginal Summary: {msg.content}")
                break

    # Show reflection
    if "reflection_result" in result:
        refl_result = result["reflection_result"]
        if isinstance(refl_result, dict) and "messages" in refl_result:
            for msg in reversed(refl_result["messages"]):
                if hasattr(msg, "content") and msg.content:
                    print(f"\nReflection Analysis: {msg.content[:250]}...")
                    break


async def main():
    """Run all post-hook examples."""
    await example_basic_post_hook()
    await example_graded_reflection_post_hook()
    await example_factory_pattern()


if __name__ == "__main__":
    asyncio.run(main())
