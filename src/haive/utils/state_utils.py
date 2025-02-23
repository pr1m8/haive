from typing import Any,Dict,Union

from langchain_core.messages import AnyMessage
from pydantic import BaseModel


def get_messages(x: Union[Dict,BaseModel],field:str="messages") -> list[AnyMessage]:
    """Get the messages from the state."""
    if isinstance(x,BaseModel):
        x = x.model_dump()
    return x[field]



def count_messages(state: Union[Dict,BaseModel],field:str="messages") -> dict:
    """Count the number of messages in the state."""
    if isinstance(state,BaseModel):
        state = state.model_dump()
    return {"initial_num_messages": len(state.get(field, []))}

def select_generated_messages(select_messages:list[AnyMessage],state: Union[Dict,BaseModel],field:str="messages") -> list:
    """Select only the messages generated within this loop."""
    if isinstance(state,BaseModel):
        state = state.model_dump()
    selected = state[field][state["initial_num_messages"] :]
    return [select_messages(selected)]