"""Reflection patterns using Message Transformer V2.

This module implements reflection patterns that integrate with the message
transformation system, following the patterns described in:
- project_docs/active/patterns/reflection_agent_pattern.md (lines 565-594)
- packages/haive-core/src/haive/core/graph/node/message_transformation_v2.py

Key difference from structured output: This uses message transformation
to add reflection context to conversations, enabling more natural
reflection flows.
"""

import asyncio
from typing import Any

from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, ToolMessage
from langchain_core.prompts import ChatPromptTemplate

from haive.agents.simple.agent import SimpleAgent

# Import what we can, but handle the missing MESSAGE_TRANSFORMER gracefully
try:
    from haive.core.graph.node.message_transformation_v2 import (
        TransformationType,
        create_reflection_transformer,
    )

    MESSAGE_TRANSFORMER_AVAILABLE = True
except (ImportError, AttributeError):
    MESSAGE_TRANSFORMER_AVAILABLE = False
    # Create basic enum for our use
    from enum import Enum

    class TransformationType(str, Enum):
        REFLECTION = "reflection"
        AI_TO_HUMAN = "ai_to_human"
        CUSTOM = "custom"


class SimpleReflectionTransformer:
    """Simple reflection transformer for when message_transformation_v2 is not available."""

    def __init__(self, preserve_first_message: bool = True):
        self.preserve_first_message = preserve_first_message

    def _apply_transformation(self, messages: list[BaseMessage]) -> list[BaseMessage]:
        """Apply simple reflection transformation: swap AI ↔ Human roles."""
        if not messages:
            return []

        transformed = []

        # Preserve first message if requested
        if self.preserve_first_message and len(messages) > 0:
            transformed.append(messages[0])
            start_idx = 1
        else:
            start_idx = 0

        # Transform remaining messages with role swap
        for msg in messages[start_idx:]:
            if isinstance(msg, AIMessage):
                # AI → Human
                transformed.append(
                    HumanMessage(
                        content=msg.content,
                        additional_kwargs=getattr(msg, "additional_kwargs", {}),
                    )
                )
            elif isinstance(msg, HumanMessage):
                # Human → AI
                transformed.append(
                    AIMessage(
                        content=msg.content,
                        additional_kwargs=getattr(msg, "additional_kwargs", {}),
                    )
                )
            else:
                # Keep other message types unchanged
                transformed.append(msg)

        return transformed


class MessageTransformerReflectionAgent:
    """Reflection agent using message transformer v2 pattern.

    Instead of structured output extraction, this uses message transformation
    to add reflection context directly to conversations, following the
    pattern from reflection_agent_pattern.md lines 565-594.
    """

    def __init__(
        self,
        name: str = "transformer_reflection_agent",
        temperature: float = 0.3,
        preserve_first_message: bool = True,
    ):
        """Initialize message transformer reflection agent.

        Args:
            name: Name for the agent
            temperature: Temperature for LLM generation
            preserve_first_message: Whether to preserve first message in transformation
        """
        self.name = name
        self.preserve_first_message = preserve_first_message

        # Create simplified reflection transformer
        if MESSAGE_TRANSFORMER_AVAILABLE:
            self.reflection_transformer = create_reflection_transformer(
                name=f"{name}_transformer",
                preserve_first_message=preserve_first_message,
            )
        else:
            # Create a simple reflection transformer function
            self.reflection_transformer = SimpleReflectionTransformer(
                preserve_first_message
            )

        # Create reflection analyzer agent
        reflection_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """You are a reflection agent that analyzes conversations and outputs.

Your role is to:
1. Analyze the conversation flow and responses
2. Identify what worked well and what could be improved
3. Provide actionable feedback for future interactions
4. Consider the context and transformation applied to messages

Focus on the conversation dynamics and response quality.""",
                ),
                ("human", "Analyze this conversation and provide reflection insights."),
            ]
        )

        self.analyzer = SimpleAgent(
            name=f"{name}_analyzer",
            engine=AugLLMConfig(
                prompt_template=reflection_prompt, temperature=temperature
            ),
        )

    async def reflect_on_conversation(
        self, messages: list[BaseMessage], original_query: str | None = None
    ) -> dict[str, Any]:
        """Perform reflection analysis using message transformation.

        Args:
            messages: The conversation messages to reflect on
            original_query: Optional original query for context

        Returns:
            Dict containing reflection analysis and transformed messages
        """
        # Apply reflection transformation to messages
        transformed_messages = self.reflection_transformer._apply_transformation(
            messages
        )

        # Create context for analysis
        analysis_input = {"messages": transformed_messages}

        if original_query:
            analysis_input["original_query"] = original_query

        # Run reflection analysis
        analysis_result = await self.analyzer.arun(analysis_input)

        # Extract analysis content
        analysis_content = ""
        if isinstance(analysis_result, dict) and "messages" in analysis_result:
            for msg in reversed(analysis_result["messages"]):
                if hasattr(msg, "content") and msg.content:
                    analysis_content = msg.content
                    break

        return {
            "analysis": analysis_content,
            "transformed_messages": transformed_messages,
            "original_messages": messages,
            "transformation_applied": "reflection",
            "message_count_before": len(messages),
            "message_count_after": len(transformed_messages),
        }


def create_reflection_context_transformer(
    messages: list[BaseMessage],
) -> list[BaseMessage]:
    """Create a reflection context transformer function.

    This function adds reflection insights to conversation context,
    following the pattern from reflection_agent_pattern.md.

    Args:
        messages: Input messages to transform

    Returns:
        Messages with reflection context added
    """
    enhanced = []

    for i, msg in enumerate(messages):
        enhanced.append(msg)

        # If AI message, look for reflection context
        if isinstance(msg, AIMessage):
            # Look for subsequent tool messages with reflection data
            for j in range(i + 1, len(messages)):
                if isinstance(messages[j], ToolMessage) and messages[j].name in [
                    "Critique",
                    "ReflectionResult",
                ]:

                    try:
                        import json

                        reflection_data = json.loads(messages[j].content)

                        # Add reflection as context
                        reflection_context = f"""
Previous response reflection:
- Quality assessment: {reflection_data.get('critique', {}).get('overall_quality', 'N/A')}
- Key insights: {reflection_data.get('summary', 'No summary available')}
- Improvement areas: {', '.join(reflection_data.get('critique', {}).get('weaknesses', []))}
"""
                        enhanced.append(HumanMessage(content=reflection_context))
                        break
                    except (json.JSONDecodeError, KeyError):
                        continue

    return enhanced


class ConversationalReflectionAgent:
    """Reflection agent that maintains conversational flow with reflection context.

    This integrates message transformation to create natural reflection
    patterns within conversations, rather than separate analysis steps.
    """

    def __init__(
        self,
        base_agent: SimpleAgent,
        name: str = "conversational_reflection",
        reflection_frequency: int = 3,  # Reflect every N exchanges
    ):
        """Initialize conversational reflection agent.

        Args:
            base_agent: The base agent to add reflection to
            name: Name for the reflection system
            reflection_frequency: How often to inject reflection (every N messages)
        """
        self.base_agent = base_agent
        self.name = name
        self.reflection_frequency = reflection_frequency
        self.message_count = 0

        # Create reflection transformer for context injection
        self.context_transformer = SimpleCustomTransformer(
            create_reflection_context_transformer
        )

    async def run_with_reflection(
        self, input_data: str | dict[str, Any]
    ) -> dict[str, Any]:
        """Run the base agent with reflection context injection.

        Args:
            input_data: Input for the base agent

        Returns:
            Agent result with reflection context applied
        """
        # Run base agent
        result = await self.base_agent.arun(input_data)

        self.message_count += 1

        # Check if we should inject reflection context
        if self.message_count % self.reflection_frequency == 0:
            # Apply reflection transformation to messages
            if isinstance(result, dict) and "messages" in result:
                messages = result["messages"]

                # Transform messages to add reflection context
                transformed_messages = self.context_transformer._apply_transformation(
                    messages
                )

                # Update result with transformed messages
                result["messages"] = transformed_messages
                result["reflection_applied"] = True
                result["transformation_type"] = "reflection_context"

        return result


class ReflectionMessageFlow:
    """Manages reflection flow using message transformations.

    This creates a workflow where reflection insights are naturally
    integrated into message flows rather than separate analysis steps.
    """

    def __init__(
        self,
        primary_agent: SimpleAgent,
        reflection_agent: SimpleAgent | None = None,
        name: str = "reflection_flow",
    ):
        """Initialize reflection message flow.

        Args:
            primary_agent: Main agent for primary responses
            reflection_agent: Optional dedicated reflection agent
            name: Name for the flow system
        """
        self.primary_agent = primary_agent
        self.name = name

        # Create reflection agent if not provided
        if not reflection_agent:
            reflection_prompt = ChatPromptTemplate.from_messages(
                [
                    (
                        "system",
                        """You are a reflection partner in this conversation.

When previous responses are shared with you through message transformation,
provide brief, constructive reflection insights that help improve the
ongoing conversation. Focus on:

1. What's working well in the conversation
2. What could be clearer or more helpful
3. Opportunities for better engagement

Keep reflections concise and conversational.""",
                    ),
                    ("human", "Please reflect on this conversation flow."),
                ]
            )

            self.reflection_agent = SimpleAgent(
                name=f"{name}_reflector",
                engine=AugLLMConfig(prompt_template=reflection_prompt, temperature=0.4),
            )
        else:
            self.reflection_agent = reflection_agent

        # Create message transformers for different flows
        self.ai_to_human_transformer = MessageTransformationNodeConfig(
            name=f"{name}_ai_to_human",
            transformation_type=TransformationType.AI_TO_HUMAN,
            preserve_metadata=True,
        )

        self.reflection_transformer = create_reflection_transformer(
            name=f"{name}_reflection", preserve_first_message=True
        )

    async def run_primary_with_reflection(
        self, query: str, include_reflection: bool = True
    ) -> dict[str, Any]:
        """Run primary agent and optionally add reflection insights.

        Args:
            query: Input query
            include_reflection: Whether to include reflection analysis

        Returns:
            Combined results with optional reflection insights
        """
        # Step 1: Primary agent response
        primary_result = await self.primary_agent.arun(query)

        result = {
            "primary_response": primary_result,
            "reflection_included": include_reflection,
        }

        if (
            include_reflection
            and isinstance(primary_result, dict)
            and "messages" in primary_result
        ):
            # Step 2: Transform messages for reflection context
            messages = primary_result["messages"]

            # Apply AI -> Human transformation for reflection agent
            transformed_for_reflection = (
                self.ai_to_human_transformer._apply_transformation(messages)
            )

            # Step 3: Get reflection insights
            reflection_input = {
                "messages": transformed_for_reflection,
                "original_query": query,
            }

            reflection_result = await self.reflection_agent.arun(reflection_input)

            # Step 4: Apply reflection transformation to create enhanced flow
            if isinstance(reflection_result, dict) and "messages" in reflection_result:
                all_messages = messages + reflection_result["messages"]
                final_transformed = self.reflection_transformer._apply_transformation(
                    all_messages
                )

                result.update(
                    {
                        "reflection_response": reflection_result,
                        "enhanced_messages": final_transformed,
                        "transformation_steps": [
                            "primary_response",
                            "ai_to_human_for_reflection",
                            "reflection_analysis",
                            "reflection_transformation",
                        ],
                    }
                )

        return result


# Factory functions for easy creation
def create_message_transformer_reflection_agent(
    name: str = "mt_reflector", temperature: float = 0.3, **kwargs
) -> MessageTransformerReflectionAgent:
    """Create a message transformer reflection agent."""
    return MessageTransformerReflectionAgent(
        name=name, temperature=temperature, **kwargs
    )


def create_conversational_reflection_agent(
    base_agent: SimpleAgent, name: str = "conv_reflector", reflection_frequency: int = 3
) -> ConversationalReflectionAgent:
    """Create a conversational reflection agent."""
    return ConversationalReflectionAgent(
        base_agent=base_agent, name=name, reflection_frequency=reflection_frequency
    )


def create_reflection_message_flow(
    primary_agent: SimpleAgent,
    reflection_agent: SimpleAgent | None = None,
    name: str = "reflection_flow",
) -> ReflectionMessageFlow:
    """Create a reflection message flow system."""
    return ReflectionMessageFlow(
        primary_agent=primary_agent, reflection_agent=reflection_agent, name=name
    )


# Example usage functions
async def example_message_transformer_reflection():
    """Example: Reflection using message transformer patterns."""
    print("\n=== Message Transformer Reflection Example ===\n")

    # Create reflection agent using message transformation
    mt_reflector = create_message_transformer_reflection_agent()

    # Create sample conversation messages
    from langchain_core.messages import AIMessage, HumanMessage

    conversation = [
        HumanMessage(content="What is artificial intelligence?"),
        AIMessage(
            content="AI is computer intelligence that can learn and solve problems."
        ),
        HumanMessage(content="Can you explain it in more detail?"),
        AIMessage(content="AI uses algorithms and data to simulate human thinking."),
    ]

    print(f"Original conversation has {len(conversation)} messages")

    # Apply reflection analysis with message transformation
    reflection_result = await mt_reflector.reflect_on_conversation(
        conversation, original_query="What is artificial intelligence?"
    )

    print("\n✅ Reflection Analysis:")
    print(f"Transformation applied: {reflection_result['transformation_applied']}")
    print(f"Messages before: {reflection_result['message_count_before']}")
    print(f"Messages after: {reflection_result['message_count_after']}")
    print(f"\nAnalysis: {reflection_result['analysis'][:200]}...")


async def example_conversational_reflection():
    """Example: Conversational reflection with context injection."""
    print("\n\n=== Conversational Reflection Example ===\n")

    # Create base agent
    base_agent = SimpleAgent(
        name="chat_assistant",
        engine=AugLLMConfig(
            system_message="You are a helpful assistant engaging in conversation.",
            temperature=0.7,
        ),
    )

    # Wrap with conversational reflection
    conv_reflector = create_conversational_reflection_agent(
        base_agent=base_agent, reflection_frequency=2  # Reflect every 2 messages
    )

    # Simulate conversation with reflection
    queries = [
        "Tell me about climate change",
        "What can individuals do to help?",
        "Are there any recent technological solutions?",
    ]

    for i, query in enumerate(queries, 1):
        print(f"\n--- Turn {i}: {query} ---")

        result = await conv_reflector.run_with_reflection(query)

        reflection_applied = result.get("reflection_applied", False)
        print(f"Reflection applied: {reflection_applied}")

        if isinstance(result, dict) and "messages" in result:
            last_message = result["messages"][-1]
            if hasattr(last_message, "content"):
                print(f"Response: {last_message.content[:150]}...")


async def example_reflection_message_flow():
    """Example: Complete reflection message flow system."""
    print("\n\n=== Reflection Message Flow Example ===\n")

    # Create primary agent
    primary_agent = SimpleAgent(
        name="knowledge_assistant",
        engine=AugLLMConfig(
            system_message="You are a knowledgeable assistant providing informative responses.",
            temperature=0.6,
        ),
    )

    # Create reflection flow system
    reflection_flow = create_reflection_message_flow(
        primary_agent=primary_agent, name="knowledge_reflection_flow"
    )

    # Test query
    query = "Explain the concept of machine learning in simple terms"

    print(f"Query: {query}")

    # Run with reflection
    flow_result = await reflection_flow.run_primary_with_reflection(
        query=query, include_reflection=True
    )

    print("\n📊 Flow Results:")
    print(f"Reflection included: {flow_result['reflection_included']}")

    if "transformation_steps" in flow_result:
        print(
            f"Transformation steps: {' → '.join(flow_result['transformation_steps'])}"
        )

    if "enhanced_messages" in flow_result:
        enhanced_messages = flow_result["enhanced_messages"]
        print(f"Enhanced message count: {len(enhanced_messages)}")

        # Show the reflection transformation effect
        print("\n📝 Message Flow with Reflection:")
        for i, msg in enumerate(enhanced_messages):
            msg_type = type(msg).__name__
            content_preview = (
                msg.content[:80] + "..." if len(msg.content) > 80 else msg.content
            )
            print(f"  {i+1}. {msg_type}: {content_preview}")


async def main():
    """Run all message transformer reflection examples."""
    await example_message_transformer_reflection()
    await example_conversational_reflection()
    await example_reflection_message_flow()


if __name__ == "__main__":
    asyncio.run(main())
