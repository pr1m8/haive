from haive.core.engine.agent.agent import AgentConfig
from haive.core.engine.aug_llm import AugLLMConfig
from pydantic import Field

from haive.agents.document_modifiers.summarizer.iterative_refinement.engines import (
    initial_summary_aug_llm,
    refine_summary_aug_llm,
)
from haive.agents.document_modifiers.summarizer.iterative_refinement.state import (
    IterativeSummarizerInput,
    IterativeSummarizerOutput,
    IterativeSummarizerState,
)


class IterativeSummarizerConfig(AgentConfig):
    """The configuration for the iterative summarizer."""

    input_schema: IterativeSummarizerInput = Field(
        default=IterativeSummarizerInput,
        description="The input of the iterative summarizer.",
    )
    output_schema: IterativeSummarizerOutput = Field(
        default=IterativeSummarizerOutput,
        description="The output of the iterative summarizer.",
    )
    state_schema: IterativeSummarizerState = Field(
        default=IterativeSummarizerState,
        description="The state of the iterative summarizer.",
    )
    engines: dict[str, AugLLMConfig] = Field(
        default={
            "initial_summary": initial_summary_aug_llm,
            "refine_summary": refine_summary_aug_llm,
        },
        description="The configuration for the Augmented LLMs.",
    )
    checkpoint_mode: str = Field(
        default="async", description="The checkpoint mode for the iterative summarizer."
    )
