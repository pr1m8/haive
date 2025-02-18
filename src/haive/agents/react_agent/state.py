from typing_extensions import Annotated, TypedDict,Sequence
from langgraph.graph import add_messages
from langchain_core.messages import BaseMessage


#class AgentState(TypedDict):
#    """ General state for all agents """
#    messages: Annotated[list, add_messages]


# Need to commpare with above
class ReactAgentState(TypedDict):
    """The state of the agent."""

    # add_messages is a reducer
    # See https://langchain-ai.github.io/langgraph/concepts/low_level/#reducers
    messages: Annotated[Sequence[BaseMessage], add_messages]
    #ability_to_execute_tools: Field(default=None,description="The agent's ability to execute tools",)


