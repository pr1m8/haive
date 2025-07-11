from agents.long_term_memory.models import KnowledgeTriple
from agents.react_agent.state import AgentState
from pydantic import BaseModel, Field


class LongTermMemoryState(AgentState):
    """State for the long term memory agent."""

    memories: list[BaseModel | KnowledgeTriple] = Field(
        default_factory=list, description="List of memories to be used for the agent"
    )
