"""Multi-agent reflection pattern using sequential coordination.

This module implements reflection patterns using the new multi-agent system.
It creates a sequential workflow where:
1. ReactAgent performs initial reasoning and action
2. SimpleAgent performs reflection using message transformer post-hooks

The reflection flow follows the pattern discovered in project documentation:
Main Agent → Response → Convert to prompt partial → Message Transform → Reflection
"""

import logging

from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langchain_core.tools import Tool
from pydantic import BaseModel, Field

from haive.agents.multi.enhanced_multi_agent_v3 import EnhancedMultiAgent
from haive.agents.react.agent import ReactAgent
from haive.agents.simple.agent import SimpleAgent

logger = logging.getLogger(__name__)


class ReflectionGrade(BaseModel):
    """Structured output for reflection grading."""

    quality_score: int = Field(..., ge=1, le=10, description="Quality rating from 1-10")
    reasoning_clarity: int = Field(
        ..., ge=1, le=10, description="How clear the reasoning is"
    )
    action_appropriateness: int = Field(
        ..., ge=1, le=10, description="How appropriate the actions taken were"
    )
    improvements: list[str] = Field(
        default_factory=list, description="Specific areas for improvement"
    )
    strengths: list[str] = Field(default_factory=list, description="What was done well")
    overall_assessment: str = Field(
        ..., description="Overall assessment of the performance"
    )


class ReflectionResult(BaseModel):
    """Result from the reflection multi-agent."""

    initial_response: str = Field(..., description="Original agent response")
    reflection_grade: ReflectionGrade = Field(..., description="Graded reflection")
    improved_response: str | None = Field(
        None, description="Optional improved response"
    )
    reflection_insights: str = Field(..., description="Key insights from reflection")


class MultiAgentReflection:
    """Multi-agent reflection system using sequential coordination.

    This class creates a coordinated reflection workflow:
    1. ReactAgent processes the initial request
    2. Reflection agent analyzes and grades the response
    3. Optional improvement agent creates enhanced response

    The pattern follows the documented message transformer post-hook approach:
    Main Agent → Response → GradingResult → Convert to prompt partial →
    Message Transform → Reflection Agent (with grade in prompt context)
    """

    def __init__(
        self,
        name: str = "reflection_system",
        engine_config: AugLLMConfig | None = None,
        tools: list[Tool] | None = None,
        include_improvement: bool = False,
        reflection_temperature: float = 0.3,
        main_temperature: float = 0.7,
    ):
        """Initialize the multi-agent reflection system.

        Args:
            name: Name for the multi-agent system
            engine_config: Base engine configuration (will be customized per agent)
            tools: Tools available to the main ReactAgent
            include_improvement: Whether to include an improvement agent
            reflection_temperature: Temperature for reflection agents (lower for consistency)
            main_temperature: Temperature for main agent
        """
        self.name = name
        self.include_improvement = include_improvement

        # Use default config if not provided
        if engine_config is None:
            engine_config = AugLLMConfig()

        # Create specialized configs
        main_config = engine_config.model_copy(update={"temperature": main_temperature})
        reflection_config = engine_config.model_copy(
            update={"temperature": reflection_temperature}
        )

        # Create the main processing agent
        self.main_agent = ReactAgent(
            name="main_processor",
            engine=main_config,
            tools=tools or [],
            structured_output_model=None,  # Let it respond naturally
        )

        # Create the reflection agent with structured output
        self.reflection_agent = SimpleAgent(
            name="reflection_grader",
            engine=reflection_config,
            structured_output_model=ReflectionGrade,
        )

        # Optional improvement agent
        self.improvement_agent = None
        if include_improvement:
            self.improvement_agent = SimpleAgent(
                name="response_improvef", engine=main_config
            )

        # Create the multi-agent coordinator using EnhancedMultiAgent V3
        agents_dict = {
            "main_processor": self.main_agent,
            "reflection_grader": self.reflection_agent,
        }
        if self.improvement_agent:
            agents_dict["response_improver"] = self.improvement_agent

        self.multi_agent = EnhancedMultiAgent(
            name=name, agents=agents_dict, execution_mode="sequential"
        )

        # Simple message transformation for reflection

    async def reflect_on_task(self, task: str, debug: bool = False) -> ReflectionResult:
        """Perform reflection on a task using the multi-agent system.

        Args:
            task: The task to process and reflect on
            debug: Whether to enable debug output

        Returns:
            ReflectionResult with original response, reflection, and optional improvement
        """
        if debug:
            logger.info(f"Starting multi-agent reflection on task: {task}")

        # Step 1: Main agent processes the task
        if debug:
            logger.info("Step 1: Main agent processing...")

        main_result = await self.main_agent.arun(task, debug=debug)

        if debug:
            logger.info(f"Main agent result: {main_result}")

        # Step 2: Transform the conversation for reflection
        # Get the conversation messages
        main_messages = getattr(self.main_agent, "messages", [])
        if not main_messages:
            # Fallback: create messages from the result
            main_messages = [
                HumanMessage(content=task),
                AIMessage(content=str(main_result)),
            ]

        # Apply simple message transformation (AI_TO_HUMAN pattern for reflection)
        transformed_messages = self._transform_messages_for_reflection(main_messages)

        # Step 3: Create reflection prompt with the transformed conversation
        reflection_prompt = self._create_reflection_prompt(
            original_task=task,
            agent_response=str(main_result),
            transformed_conversation=transformed_messages,
        )

        if debug:
            logger.info("Step 2: Reflection agent analyzing...")
            logger.info(f"Reflection prompt: {reflection_prompt}")

        # Get structured reflection
        reflection_result = await self.reflection_agent.arun(
            reflection_prompt, debug=debug
        )

        if debug:
            logger.info(f"Raw reflection result: {reflection_result}")
            logger.info(f"Reflection result type: {type(reflection_result)}")

        # Handle the case where the agent returns a dict or messages instead of structured output
        if isinstance(reflection_result, dict):
            # Try to extract from the dict structure
            if "messages" in reflection_result:
                messages = reflection_result["messages"]
                if messages and hasattr(messages[-1], "content"):
                    reflection_content = messages[-1].content
                    if debug:
                        logger.info(
                            f"Extracted content from messages: {reflection_content}"
                        )
                    # Try to parse as structured output
                    try:
                        reflection_grade = ReflectionGrade.model_validate_json(
                            reflection_content
                        )
                    except Exception as e:
                        if debug:
                            logger.warning(
                                f"Failed to parse as JSON, creating manual grade: {e}"
                            )
                        # Create a default grade if parsing fails
                        reflection_grade = ReflectionGrade(
                            quality_score=7,
                            reasoning_clarity=7,
                            action_appropriateness=7,
                            improvements=["More detailed analysis needed"],
                            strengths=["Provided response"],
                            overall_assessment=f"Analysis: {reflection_content[:200]}...",
                        )
                else:
                    # Fallback grade
                    reflection_grade = ReflectionGrade(
                        quality_score=6,
                        reasoning_clarity=6,
                        action_appropriateness=6,
                        improvements=["Unable to analyze properly"],
                        strengths=["Attempted response"],
                        overall_assessment="Unable to properly analyze the response",
                    )
            else:
                # Fallback grade for unexpected dict structure
                reflection_grade = ReflectionGrade(
                    quality_score=5,
                    reasoning_clarity=5,
                    action_appropriateness=5,
                    improvements=["Response structure unclear"],
                    strengths=["Provided some output"],
                    overall_assessment="Unexpected response format",
                )
        elif isinstance(reflection_result, ReflectionGrade):
            # Perfect - already structured
            reflection_grade = reflection_result
        else:
            # Handle string or other types
            reflection_grade = ReflectionGrade(
                quality_score=6,
                reasoning_clarity=6,
                action_appropriateness=6,
                improvements=["Response format not as expected"],
                strengths=["Provided response"],
                overall_assessment=f"Raw response: {str(reflection_result)[:200]}...",
            )

        if debug:
            logger.info(f"Final reflection grade: {reflection_grade}")

        # Step 4: Optional improvement
        improved_response = None
        if self.improvement_agent and hasattr(reflection_grade, "quality_score"):
            # Only improve if quality score is below threshold
            if reflection_grade.quality_score < 8:
                if debug:
                    logger.info("Step 3: Creating improved response...")

                improvement_prompt = self._create_improvement_prompt(
                    original_task=task,
                    original_response=str(main_result),
                    reflection_grade=reflection_grade,
                )

                improved_response = await self.improvement_agent.arun(
                    improvement_prompt, debug=debug
                )

                if debug:
                    logger.info(f"Improved response: {improved_response}")

        # Step 5: Extract insights from reflection
        insights = self._extract_insights(reflection_grade)

        return ReflectionResult(
            initial_response=str(main_result),
            reflection_grade=reflection_grade,
            improved_response=str(improved_response) if improved_response else None,
            reflection_insights=insights,
        )

    def _create_reflection_prompt(
        self,
        original_task: str,
        agent_response: str,
        transformed_conversation: list[BaseMessage],
    ) -> str:
        """Create the reflection prompt using transformed conversation context.

        This follows the pattern: structured data flows through prompt configuration,
        not through messages directly.
        """
        # Convert transformed messages to readable format
        conversation_context = "\n".join(
            [
                f"{msg.__class__.__name__}: {msg.content}"
                for msg in transformed_conversation
            ]
        )

        return f"""You are an expert AI system evaluator. Please analyze the following interaction and provide a detailed reflection.

ORIGINAL TASK:
{original_task}

AGENT RESPONSE:
{agent_response}

CONVERSATION CONTEXT (Message Transformed):
{conversation_context}

Please evaluate this interaction and provide scores for:
1. Quality (1-10): Overall quality of the response
2. Reasoning Clarity (1-10): How clear and logical the reasoning was
3. Action Appropriateness (1-10): How well the actions matched the task

Also identify:
- Specific areas for improvement
- What was done well (strengths)
- Overall assessment

Focus on constructive analysis that can help improve future performance."""

    def _create_improvement_prompt(
        self,
        original_task: str,
        original_response: str,
        reflection_grade: ReflectionGrade,
    ) -> str:
        """Create prompt for improvement based on reflection."""
        improvements_text = "\n".join(
            [f"- {imp}" for imp in reflection_grade.improvements]
        )
        strengths_text = "\n".join(
            [f"- {strength}" for strength in reflection_grade.strengths]
        )

        return f"""Based on the reflection analysis, please create an improved response to the original task.

ORIGINAL TASK:
{original_task}

ORIGINAL RESPONSE:
{original_response}

REFLECTION ANALYSIS:
Quality Score: {reflection_grade.quality_score}/10
Assessment: {reflection_grade.overall_assessment}

AREAS FOR IMPROVEMENT:
{improvements_text}

STRENGTHS TO MAINTAIN:
{strengths_text}

Please provide an improved response that addresses the identified improvements while maintaining the strengths. Be specific and actionable."""

    def _extract_insights(self, reflection_grade: ReflectionGrade) -> str:
        """Extract key insights from the reflection grade."""
        insights = []

        if hasattr(reflection_grade, "quality_score"):
            insights.append(f"Quality Score: {reflection_grade.quality_score}/10")

        if hasattr(reflection_grade, "reasoning_clarity"):
            insights.append(
                f"Reasoning Clarity: {reflection_grade.reasoning_clarity}/10"
            )

        if hasattr(reflection_grade, "action_appropriateness"):
            insights.append(
                f"Action Appropriateness: {reflection_grade.action_appropriateness}/10"
            )

        if hasattr(reflection_grade, "improvements") and reflection_grade.improvements:
            insights.append(
                f"Key Improvements: {', '.join(reflection_grade.improvements[:3])}"
            )

        if hasattr(reflection_grade, "overall_assessment"):
            insights.append(f"Assessment: {reflection_grade.overall_assessment}")

        return " | ".join(insights)

    def _transform_messages_for_reflection(
        self, messages: list[BaseMessage]
    ) -> list[BaseMessage]:
        """Simple message transformation for reflection analysis.

        Converts AI messages to human perspective for better reflection analysis.
        This implements a simplified version of the AI_TO_HUMAN transformation.
        """
        transformed = []
        for msg in messages:
            if isinstance(msg, AIMessage):
                # Convert AI message to human perspective for reflection
                transformed_content = f"The assistant responded: {msg.content}"
                transformed.append(HumanMessage(content=transformed_content))
            else:
                # Keep other messages as-is
                transformed.append(msg)
        return transformed


# Factory functions for easy creation


def create_simple_reflection_system(
    tools: list[Tool] | None = None, engine_config: AugLLMConfig | None = None
) -> MultiAgentReflection:
    """Create a simple reflection system with ReactAgent + ReflectionAgent.

    Args:
        tools: Tools for the ReactAgent
        engine_config: Base engine configuration

    Returns:
        MultiAgentReflection system ready for use
    """
    return MultiAgentReflection(
        name="simple_reflection",
        engine_config=engine_config,
        tools=tools,
        include_improvement=False,
    )


def create_full_reflection_system(
    tools: list[Tool] | None = None, engine_config: AugLLMConfig | None = None
) -> MultiAgentReflection:
    """Create a full reflection system with ReactAgent + ReflectionAgent + ImprovementAgent.

    Args:
        tools: Tools for the ReactAgent
        engine_config: Base engine configuration

    Returns:
        MultiAgentReflection system with improvement capability
    """
    return MultiAgentReflection(
        name="full_reflection",
        engine_config=engine_config,
        tools=tools,
        include_improvement=True,
    )
