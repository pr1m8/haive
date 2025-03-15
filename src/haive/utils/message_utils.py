
from typing import List,Dict,Any
from langchain_core.messages import BaseMessage,FunctionMessage,HumanMessage

def _get_observations(messages: List[BaseMessage],additional_kwargs: Dict[str,Any]) -> Dict[int, Any]:
    # Get all previous tool responses
    results = {}
    for message in messages[::-1]:
        if isinstance(message, FunctionMessage):
            results[int(message.additional_kwargs["idx"])] = message.content
    return results

def select_recent_messages(state) -> dict:
    """Select the most recent messages from the state 
    that are not HumanMessage
    """
    messages = state["messages"]
    selected = []
    for msg in messages[::-1]:
        selected.append(msg)
        if isinstance(msg, HumanMessage):
            break
    return {"messages": selected[::-1]}