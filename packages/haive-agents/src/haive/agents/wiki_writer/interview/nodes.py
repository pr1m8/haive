import json

from agents.wiki_writer.interview.aug_llms import (
    gen_qn_aug_llm_config,
    gen_queries_chain,
)
from agents.wiki_writer.interview.state import InterviewState
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.tools.search_tools import tavily_search_tool
from haive.core.utils.message_utils import swap_roles, tag_with_name
from langchain_core.messages import AIMessage, ToolMessage
from langchain_core.runnables import RunnableConfig, RunnableLambda, chain
from langchain_core.tools import BaseTool, StructuredTool
from langgraph.types import Command


@chain
async def generate_question(
    state: InterviewState,
    aug_llm_config: AugLLMConfig = gen_qn_aug_llm_config,
    # gen_qn_prompt: ChatPromptTemplate=gen_qn_prompt,
):
    editor = state["editor"]
    gn_chain = (
        RunnableLambda(swap_roles).bind(name=editor.name)
        | aug_llm_config
        | RunnableLambda(tag_with_name).bind(name=editor.name)
    )
    result = await gn_chain.ainvoke(state)
    return Command(update={"messages": [result]})


async def gen_answer(
    state: InterviewState,
    config: RunnableConfig | None = None,
    name: str = "Subject_Matter_Expert",
    max_str_len: int = 15000,
    search_engine: BaseTool | StructuredTool = tavily_search_tool,
):
    swapped_state = swap_roles(state, name)  # Convert all other AI messages
    queries = await gen_queries_chain.ainvoke(swapped_state)

    query_results = await search_engine.abatch(
        queries["parsed"].queries, config, return_exceptions=True
    )
    # query_results = [

    successful_results = [
        res for res in query_results if not isinstance(res, Exception)
    ]
    all_query_results = {
        res["url"]: res["content"] for results in successful_results for res in results
    }
    # We could be more precise about handling max token length if we wanted to here
    dumped = json.dumps(all_query_results)[:max_str_len]
    ai_message: AIMessage = queries["raw"]
    tool_call = queries["raw"].tool_calls[0]
    tool_id = tool_call["id"]
    tool_message = ToolMessage(tool_call_id=tool_id, content=dumped)
    swapped_state["messages"].extend([ai_message, tool_message])
    # Only update the shared state with the final answer to avoid
    # polluting the dialogue history with intermediate messages
    generated = await gen_answer_chain.ainvoke(swapped_state)
    cited_urls = set(generated["parsed"].cited_urls)
    # Save the retrieved information to a the shared state for future reference
    cited_references = {k: v for k, v in all_query_results.items() if k in cited_urls}
    formatted_message = AIMessage(name=name, content=generated["parsed"].as_str)
    return {"messages": [formatted_message], "references": cited_references}
