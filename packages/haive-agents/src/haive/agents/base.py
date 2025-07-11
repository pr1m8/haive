from haive.core.engine.agent.agent import Agent, AgentConfig, register_agent
from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.documents import Document
from langchain_core.messages import AnyMessage
from pydantic import BaseModel, Field


class ContentsState(BaseModel):
    """The state of the document agent."""

    documents: list[Document | AnyMessage | dict | str] = Field(
        default_factory=list, description="The documents to process."
    )


class DocumentAgentConfig(AgentConfig):
    """The configuration for the document agent."""

    aug_llm_config: AugLLMConfig = Field(default=AugLLMConfig())


@register_agent(DocumentAgentConfig)
class DocumentAgent(Agent[DocumentAgentConfig]):
    def __init__(self, config: DocumentAgentConfig):
        super().__init__(config)

    def run(self, document: Document):
        pass
