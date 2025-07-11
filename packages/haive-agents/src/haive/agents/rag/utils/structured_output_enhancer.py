"""Structured Output Enhancer for RAG Agents.

This utility enables any agent to be enhanced with structured output by appending
a SimpleAgent with the appropriate prompt template and Pydantic model. This follows
the pattern of keeping prompts focused on generation while parsers handle structure.
"""

from typing import Any, Dict, List, Optional, Type

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import LLMConfig
from haive.core.utils.pydantic_utils.base_model_to_prompt import (
    PromptGenerator,
    PromptStyle,
)
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel

from haive.agents.simple.agent import SimpleAgent


class StructuredOutputEnhancer:
    """Utility for enhancing any agent with structured output capabilities.

    This class provides a clean pattern for appending structured output processing
    to any existing agent, following the principle that prompts focus on generation
    while parsers handle structure.

    Example:
        >>> from haive.agents.rag.models import HyDEResult
        >>>
        >>> # Enhance any agent with HyDE structured output
        >>> enhancer = StructuredOutputEnhancer(HyDEResult)
        >>> structured_agent = enhancer.create_enhancement_agent(
        ...     llm_config=llm_config,
        ...     context_prompt="Based on the retrieved documents, generate a hypothetical document analysis"
        ... )
        >>>
        >>> # Or enhance an existing agent pipeline
        >>> enhanced_pipeline = enhancer.enhance_agent_sequence([base_agent, retrieval_agent], llm_config)
    """

    def __init__(
        self,
        output_model: type[BaseModel],
        prompt_style: PromptStyle = PromptStyle.DESCRIPTIVE,
        structured_output_version: str = "v1",
    ):
        """Initialize the enhancer with a Pydantic output model.

        Args:
            output_model: Pydantic model for structured output
            prompt_style: Style for generating format instructions
            structured_output_version: v1 (parser-based) or v2 (tool-based)
        """
        self.output_model = output_model
        self.prompt_style = prompt_style
        self.structured_output_version = structured_output_version
        self.prompt_generator = PromptGenerator(style=prompt_style)

    def create_format_instructions(self) -> str:
        """Generate format instructions for the output model."""
        return PromptGenerator.create_format_instructions(self.output_model)

    def create_enhancement_prompt(
        self, context_prompt: str, include_state_context: bool = True
    ) -> ChatPromptTemplate:
        """Create a prompt template for structured output enhancement.

        Args:
            context_prompt: The main instruction for what to generate
            include_state_context: Whether to include previous state context

        Returns:
            ChatPromptTemplate configured for structured output
        """
        format_instructions = self.create_format_instructions()

        system_message = f"""You are an expert at analyzing and structuring information.

{context_prompt}

Please provide your analysis in the following structured format:
{format_instructions}"""

        messages = [("system", system_message)]

        if include_state_context:
            # Include context from previous processing steps
            messages.append(
                (
                    "human",
                    """Based on the previous processing:

Query: {query}
Context: {context}
Retrieved Documents: {retrieved_documents}

{additional_context}

Please provide your structured analysis.""",
                )
            )
        else:
            messages.append(("human", "{query}"))

        return ChatPromptTemplate.from_messages(messages)

    def create_enhancement_agent(
        self,
        llm_config: LLMConfig,
        context_prompt: str,
        agent_name: str | None = None,
        include_state_context: bool = True,
        **engine_kwargs,
    ) -> SimpleAgent:
        """Create a SimpleAgent for structured output enhancement.

        Args:
            llm_config: LLM configuration
            context_prompt: Main instruction for what to generate
            agent_name: Name for the enhancement agent
            include_state_context: Whether to include previous state context
            **engine_kwargs: Additional arguments for AugLLMConfig

        Returns:
            SimpleAgent configured for structured output
        """
        prompt_template = self.create_enhancement_prompt(
            context_prompt=context_prompt, include_state_context=include_state_context
        )

        output_key = f"{self.output_model.__name__.lower()}_result"

        return SimpleAgent(
            engine=AugLLMConfig(
                llm_config=llm_config,
                prompt_template=prompt_template,
                structured_output_model=self.output_model,
                structured_output_version=self.structured_output_version,
                output_key=output_key,
                **engine_kwargs,
            ),
            name=agent_name or f"{self.output_model.__name__} Enhancer",
        )

    def enhance_agent_sequence(
        self,
        agents: list[Any],
        llm_config: LLMConfig,
        context_prompt: str | None = None,
        **kwargs,
    ) -> list[Any]:
        """Enhance a sequence of agents by appending structured output processing.

        Args:
            agents: List of existing agents
            llm_config: LLM configuration
            context_prompt: Custom context prompt (auto-generated if None)
            **kwargs: Additional arguments for the enhancement agent

        Returns:
            List of agents with structured output enhancement appended
        """
        if context_prompt is None:
            context_prompt = (
                f"Analyze the processing results and provide a structured "
                f"{self.output_model.__name__} summary."
            )

        enhancement_agent = self.create_enhancement_agent(
            llm_config=llm_config, context_prompt=context_prompt, **kwargs
        )

        return [*agents, enhancement_agent]


# Convenience functions for common RAG patterns
def create_hyde_enhancer() -> StructuredOutputEnhancer:
    """Create an enhancer for HyDE structured output."""
    from haive.agents.rag.models import HyDEResult

    return StructuredOutputEnhancer(
        output_model=HyDEResult, prompt_style=PromptStyle.DESCRIPTIVE
    )


def create_fusion_enhancer() -> StructuredOutputEnhancer:
    """Create an enhancer for Fusion RAG structured output."""
    from haive.agents.rag.models import FusionResult

    return StructuredOutputEnhancer(
        output_model=FusionResult, prompt_style=PromptStyle.STRUCTURED
    )


def create_speculative_enhancer() -> StructuredOutputEnhancer:
    """Create an enhancer for Speculative RAG structured output."""
    from haive.agents.rag.models import SpeculativeResult

    return StructuredOutputEnhancer(
        output_model=SpeculativeResult, prompt_style=PromptStyle.CONVERSATIONAL
    )


def create_memory_enhancer() -> StructuredOutputEnhancer:
    """Create an enhancer for Memory-aware RAG structured output."""
    from haive.agents.rag.models import MemoryAnalysis

    return StructuredOutputEnhancer(
        output_model=MemoryAnalysis, prompt_style=PromptStyle.DESCRIPTIVE
    )


# Example usage patterns
def demonstrate_enhancement_patterns():
    """Demonstrate various enhancement patterns."""
    from haive.core.models.llm.base import AzureLLMConfig

    # Example LLM config
    llm_config = AzureLLMConfig(
        deployment_name="gpt-4",
        azure_endpoint="${AZURE_OPENAI_API_BASE}",
        api_key="${AZURE_OPENAI_API_KEY}",
    )

    # Pattern 1: Enhance any existing agent with HyDE analysis
    hyde_enhancer = create_hyde_enhancer()
    hyde_analysis_agent = hyde_enhancer.create_enhancement_agent(
        llm_config=llm_config,
        context_prompt="Generate a hypothetical document that would contain the ideal answer to this query",
    )

    # Pattern 2: Add fusion analysis to a pipeline
    fusion_enhancer = create_fusion_enhancer()
    enhanced_agents = fusion_enhancer.enhance_agent_sequence(
        agents=[],  # Your existing agents here
        llm_config=llm_config,
        context_prompt="Analyze the multi-query retrieval results and provide fusion ranking analysis",
    )

    # Pattern 3: Create custom enhancement for any model
    class CustomAnalysis(BaseModel):
        """Custom analysis model."""

        insights: list[str]
        confidence: float
        recommendations: list[str]

    custom_enhancer = StructuredOutputEnhancer(
        output_model=CustomAnalysis, prompt_style=PromptStyle.CONVERSATIONAL
    )

    custom_agent = custom_enhancer.create_enhancement_agent(
        llm_config=llm_config,
        context_prompt="Provide custom insights and recommendations based on the analysis",
    )

    return {
        "hyde_analysis": hyde_analysis_agent,
        "enhanced_pipeline": enhanced_agents,
        "custom_enhancement": custom_agent,
    }


# Integration with existing RAG patterns
class RAGEnhancementFactory:
    """Factory for creating enhanced RAG agents with structured output."""

    @staticmethod
    def enhance_simple_rag(
        llm_config: LLMConfig, enhancement_type: str = "hyde"
    ) -> list[SimpleAgent]:
        """Create a simple RAG with structured output enhancement.

        Args:
            llm_config: LLM configuration
            enhancement_type: Type of enhancement (hyde, fusion, speculative, memory)

        Returns:
            List of agents forming an enhanced RAG pipeline
        """
        enhancer_map = {
            "hyde": create_hyde_enhancer,
            "fusion": create_fusion_enhancer,
            "speculative": create_speculative_enhancer,
            "memory": create_memory_enhancer,
        }

        if enhancement_type not in enhancer_map:
            raise ValueError(f"Unknown enhancement type: {enhancement_type}")

        enhancer = enhancer_map[enhancement_type]()

        # Create base processing steps (these would be actual agents in practice)
        base_agents = []  # Add your base RAG agents here

        # Enhance with structured output
        context_prompts = {
            "hyde": "Generate hypothetical documents and refined queries for enhanced retrieval",
            "fusion": "Analyze multi-query retrieval results and provide reciprocal rank fusion analysis",
            "speculative": "Generate and verify hypotheses about the query requirements",
            "memory": "Analyze conversation context and memory relevance for personalized responses",
        }

        return enhancer.enhance_agent_sequence(
            agents=base_agents,
            llm_config=llm_config,
            context_prompt=context_prompts[enhancement_type],
        )
