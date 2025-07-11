from agents.react_agent2.many_tools.engines import query_builder_aug_llm_config
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.messages import HumanMessage
from haive.core.models.state import State
from haive.core.models.vectorstore.base import VectorStoreConfig
from langgraph.types import Command


def select_tools_with_repeat(
    state: State,
    vs_config: VectorStoreConfig,
    aug_llm_config: AugLLMConfig = query_builder_aug_llm_config,
):
    """Selects tools based on the last message in the conversation state.

    If the last message is from a human, directly uses the content of the message
    as the query. Otherwise, constructs a query using a system message and invokes
    the LLM to generate tool suggestions.
    """
    last_message = state.messages[-1]
    hack_remove_tool_condition = False  # Simulate an error in the first tool selection

    if isinstance(last_message, HumanMessage):
        query = last_message.content
        hack_remove_tool_condition = True  # Simulate wrong tool selection
    else:
        aug_llm = aug_llm_config.create_runnable()
        query = aug_llm.invoke(state.messages).query

    # Search the tool vector store using the generated query
    vector_store = vs_config.create_vector_store()
    tool_documents = vector_store.similarity_search(query)
    if hack_remove_tool_condition:
        # Simulate error by removing the correct tool from the selection
        selected_tools = [
            document.id
            for document in tool_documents
            if document.metadata["tool_name"] != "Advanced_Micro_Devices"
        ]
    else:
        selected_tools = [document.id for document in tool_documents]
    return Command(update={"selected_tools": selected_tools})


# The select_tools function selects tools based on the user's last message content.
def select_tools(state: State, vs_config: VectorStoreConfig):
    last_user_message = state.messages[-1]
    query = last_user_message.content
    vector_store = vs_config.create_vector_store()
    tool_documents = vector_store.similarity_search(query)
    return Command(
        update={"selected_tools": [document.id for document in tool_documents]}
    )
