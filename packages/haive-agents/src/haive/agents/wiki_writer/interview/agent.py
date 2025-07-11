from agents.wiki_writer.interview.aug_llms import (
    gen_answer_aug_llm_config,
    gen_qn_aug_llm_config,
    gen_queries_aug_llm_config,
)
from agents.wiki_writer.interview.nodes import gen_answer, generate_question
from agents.wiki_writer.interview.state import InterviewState
from haive.core.engine.agent.agent import AgentArchitecture, AgentArchitectureConfig
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.utils.message_utils import route_messages
from langgraph.graph import START
from langgraph.pregel import RetryPolicy
from pydantic import Field


class InterviewAgentConfig(AgentArchitectureConfig):
    """Configuration for the Interview Agent."""

    aug_llm_configs: dict[str, AugLLMConfig] = Field(
        default={
            "gen_qn": gen_qn_aug_llm_config,
            "gen_queries": gen_queries_aug_llm_config,
            "gen_answer": gen_answer_aug_llm_config,
        },
        description="LLM config for Interview",
    )

    state_schema: InterviewState = Field(
        default=InterviewState, description="State schema for the agent"
    )
    # runnable_config: RunnableConfig = Field(
    #  description="Agent runnable config")


class InterviewAgent(AgentArchitecture):
    """An agent that conducts an interview with a Subject Matter Expert."""

    def __init__(self, config: InterviewAgentConfig = InterviewAgentConfig()):
        super().__init__(config)

    def setup_workflow(self):
        """Setup the workflow for the agent."""
        self.graph.add_node(
            "ask_question", generate_question, retry=RetryPolicy(max_attempts=5)
        )
        self.graph.add_node(
            "answer_question", gen_answer, retry=RetryPolicy(max_attempts=5)
        )
        self.graph.add_conditional_edges("answer_question", route_messages)
        self.graph.add_edge("ask_question", "answer_question")

        self.graph.add_edge(START, "ask_question")
