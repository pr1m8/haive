from haive.core.engine.agent.agent import AgentConfig
from haive.core.engine.aug_llm import AugLLMConfig
from pydantic import Field

from haive.agents.document_modifiers.summarizer.map_branch.engines import (
    map_aug_llm_config,
    reduce_augllm_config,
)
from haive.agents.document_modifiers.summarizer.map_branch.state import (
    InputState,
    OutputState,
    SummaryState,
)


class SummarizerAgentConfig(AgentConfig):
    name: str = "map_reduce_summarizer_agent"
    engines: dict[str, AugLLMConfig] = Field(
        default_factory=lambda: {
            "map_chain": map_aug_llm_config,
            "reduce_chain": reduce_augllm_config,
        },
        description="The configuration for the LLM",
    )
    token_max: int = Field(
        default=1000,
        description="The maximum number of tokens to use for the summarizer",
    )
    state_schema: SummaryState = Field(default=SummaryState)
    input_schema: InputState = Field(default=InputState)
    output_schema: OutputState = Field(default=OutputState)
    # should_visualize_graph: bool = True
    visualize: bool = True
    checkpoint_mode: str = Field(
        default="async", description="The checkpoint mode for the summarizer."
    )

    # visualize_graph_output_name: str = "summarizer_agent_graph.png"
    def build_agent(self):
        from haive.agents.document_modifiers.summarizer.map_branch.agent import (
            SummarizerAgent,
        )

        return SummarizerAgent(self)
