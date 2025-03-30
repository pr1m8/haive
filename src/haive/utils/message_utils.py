from langchain_core.messages import AIMessage
from typing import Callable, Dict, Any, List, Union
from langchain_core.messages import HumanMessage, SystemMessage
from uuid import uuid4
from langchain_core.messages import AnyMessage

def add_messages(left, right):
    """
    Add two lists of messages together.
    """
    if not isinstance(left, list):
        left = [left]
    if not isinstance(right, list):
        right = [right]
    return left + right

def tag_with_name(ai_message: AIMessage, name: str):
    """
    Tag an AIMessage with a name.
    """
    ai_message.name = name
    return ai_message

def tag_ai_messages_transform(message, kwargs):
    """Adds a tag to AI messages."""
    tag = kwargs.get("tag", "[AI]")  # Default tag if not provided

    if isinstance(message, AIMessage):
        return AIMessage(content=f"{tag} {message.content}", **message.dict(exclude={"content"}))
    
    return message


def transform_messages(
    state: Dict[str, Any], 
    transform_fn: Callable[[Any, Dict[str, Any]], Any], 
    **kwargs
) -> Dict[str, Any]:
    """
    Generalized function to apply a transformation to all messages in state.

    :param state: The state dictionary containing "messages".
    :param transform_fn: A function that transforms each message.
    :param kwargs: Additional keyword arguments for the transform function.
    :return: A new state dictionary with transformed messages.
    """
    return {
        "messages": [
            transform_fn(message, kwargs) for message in state.get("messages", [])
        ]
    }
def swap_roles_transform(message, kwargs):
    """Specific transformation function for swapping AI/Human roles."""
    name = kwargs.get("name")  # Get the "name" argument

    if isinstance(message, AIMessage) and message.name != name:
        return HumanMessage(**message.dict(exclude={"type"}))
    
    return message  # Return unchanged if conditions don't match

def route_messages(
    state: dict, 
    speaker_name: str = "Subject_Matter_Expert",
    max_turns: int = 5, 
    last_question_trigger: str = "Thank you so much for your help!",
    end_route: str = "END",
    continue_route: str = "ask_question",
) -> str:
    messages: List[Union[AIMessage, HumanMessage, SystemMessage]] = state["messages"]

    # Count how many AI messages from this speaker
    num_responses = len(
        [m for m in messages if isinstance(m, AIMessage) and m.name == speaker_name]
    )
    if num_responses >= max_turns:
        return end_route

    # Check if second-to-last message ends with a certain string
    if len(messages) >= 2:
        last_question = messages[-2]
        if last_question.content.endswith(last_question_trigger):
            return end_route

    return continue_route

def reduce_messages(left: list[AnyMessage], right: list[AnyMessage]) -> list[AnyMessage]:
    # assign ids to messages that don't have them
    for message in right:
        if not message.id:
            message.id = str(uuid4())
    # merge the new messages with the existing messages
    merged = left.copy()
    for message in right:
        for i, existing in enumerate(merged):
            # replace any existing messages with the same id
            if existing.id == message.id:
                merged[i] = message
                break
        else:
            # append any new messages to the end
            merged.append(message)
    return merged