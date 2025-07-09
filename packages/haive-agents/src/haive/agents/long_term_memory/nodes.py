import tiktoken
from agents.long_term_memory.state import LongTermMemoryState
from agents.long_term_memory.tools import search_recall_memories
from langchain_core.messages import get_buffer_string
from langchain_core.runnables import RunnableConfig

tokenizer = tiktoken.encoding_for_model("gpt-4o")


def load_memories(
    state: LongTermMemoryState, config: RunnableConfig
) -> LongTermMemoryState:
    """Load memories for the current conversation.

    Args:
        state (schemas.State): The current state of the conversation.
        config (RunnableConfig): The runtime configuration for the agent.

    Returns:
        State: The updated state with loaded memories.
    """
    convo_str = get_buffer_string(state["messages"])
    convo_str = tokenizer.decode(tokenizer.encode(convo_str)[:2048])
    recall_memories = search_recall_memories.invoke(convo_str, config)
    return {
        "recall_memories": recall_memories,
    }
