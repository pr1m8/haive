# Node is modularized

from langchain_core.prompt_values import ChatPromptValue
from langchain_core.runnables import RunnableConfig
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder,PromptTemplate

from langchain_core.output_parsers.openai_tools import JsonOutputToolsParser
from src.config.settings import *
from langchain_openai import AzureOpenAI
from typing import TypedDict
from src.haive.agents.lats.node import Node
from collections import defaultdict
from typing import Literal
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph, START

from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.utilities.tavily_search import TavilySearchAPIWrapper
from langgraph.prebuilt import ToolNode
from langchain_core.messages import AIMessage
# Difference with using Search API Wrapper vs search? 
search = TavilySearchAPIWrapper()
tavily_tool = TavilySearchResults(api_wrapper=search, max_results=5)
# https://langchain-ai.github.io/langgraph/tutorials/lats/lats/#reflection

from src.haive.core.engine.agent.agent import AgentArchitecture, AgentArchitectureConfig

from src.haive.agents.lats.state import TreeState

class LATSConfig(AgentArchitectureConfig):
    """LATS Agent Configuration"""
    llm_config: AugLLMConfig = Field(default=AugLLMConfig(name="lats_llm",llm_config=AzureLLMConfig(model="gpt-4o",parameters={"temperature": 0.7})),description="The configuration for the LLM")
    reflection_llm_config: AugLLMConfig = Field(default=AugLLMConfig(name="reflection_llm",llm_config=AzureLLMConfig(model="gpt-4o",parameters={"temperature": 0.7})),description="The configuration for the reflection LLM")

def should_loop(state: TreeState,num_levels: int):
    """Determine whether to continue the tree search."""
    root = state["root"]
    if root.is_solved:
        return END
    if root.height > num_levels:
        return END
    return "expand"

@as_runnable
def reflection_chain(inputs) -> Reflection:
    reflection_llm_chain = compose_runnable(reflection_aug_llm_config)
    tool_choices = reflection_llm_chain.invoke(inputs)
    reflection = tool_choices[0]
    if not isinstance(inputs["candidate"][-1], AIMessage):
        reflection.found_solution = False
    return reflection

class LATS(AgentArchitecture):
    def __init__(self,llm=AzureChatOpenAI(model='gpt-4o'),tools=[tavily_tool],
                 system_prompt="You are an AI Assistant",
                 config: RunnableConfig = {'configurable': {'thread_id':'1'}},
                 num_levels: int = 5):
        self.llm = llm
        self.tools = tools
        self.tool_node = ToolNode(tools=tools)
        self.reflection_chain = ReflectionChain(llm)
        self.config = config
        self.num_levels = num_levels
        self.memory = MemorySaver()
        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("user", "{input}"),
                MessagesPlaceholder(variable_name="messages", optional=True),
            ]
        )#.partial(format_instructions=parser.get_format_instructions())
        self.initial_answer_chain = self.prompt_template | self.llm.bind_tools(tools=tools).with_config(
            run_name="GenerateInitialCandidate"
        ) 


        self.json_parser = JsonOutputToolsParser(return_id=True)
        self.expansion_chain = self.prompt_template | self.generate_candidates
        self.graph = self.setup_graph()
        self.app = self.graph.compile(checkpointer=self.memory)
        self.steps=[]
        self.solution_node=None
        self.best_trajectory=None
    
    def generate_candidates(messages: ChatPromptValue, config: RunnableConfig):
        n = config["configurable"].get("N", 5)
        bound_kwargs = llm.bind_tools(tools=tools).kwargs
        chat_result = llm.generate(
            [messages.to_messages()],
            n=n,
            callbacks=config["callbacks"],
            run_name="GenerateCandidates",
            **bound_kwargs,
        )
        return [gen.message for gen in chat_result.generations[0]]
    # Define the node we will add to the graph
    # Define the node we will add to the graph
    def generate_initial_response(self,state: TreeState) -> dict:
        """Generate the initial candidate response."""
        res = self.initial_answer_chain.invoke({"input": state["input"]})
        parsed = self.json_parser.invoke(res)
        tool_responses = [
            tool_node.invoke(
                {
                    "messages": [
                        AIMessage(
                            content="",
                            tool_calls=[
                                {"name": r["type"], "args": r["args"], "id": r["id"]}
                            ],
                        )
                    ]
                }
            )
            for r in parsed
        ]
        output_messages = [res] + [tr["messages"][0] for tr in tool_responses]
        reflection = reflection_chain.invoke(
            {"input": state["input"], "candidate": output_messages}
        )
        root = Node(output_messages, reflection=reflection)
        return {
            **state,
            "root": root,
        }


    def generate_candidates(self,messages: ChatPromptValue, config: RunnableConfig):
        n = config["configurable"].get("N", 5)
        bound_kwargs = self.llm.bind_tools(tools=self.tools).kwargs
        chat_result = self.llm.generate(
            [messages.to_messages()],
            n=n,
            callbacks=config["callbacks"],
            run_name="GenerateCandidates",
            **bound_kwargs,
        )
        return [gen.message for gen in chat_result.generations[0]]
    #review


    from collections import defaultdict


    def select(self,root: Node) -> dict:
        """Starting from the root node a child node is selected at each tree level until a leaf node is reached."""

        if not root.children:
            return root

        node = root
        while node.children:
            max_child = max(node.children, key=lambda child: child.upper_confidence_bound())
            node = max_child

        return node


    def expand(self,state: TreeState, config: RunnableConfig) -> dict:
        """Starting from the "best" node in the tree, generate N candidates for the next step."""
        root = state["root"]
        best_candidate: Node = self.select(root)
        messages = best_candidate.get_trajectory()
        # Generate N candidates from the single child candidate
        new_candidates = self.expansion_chain.invoke(
            {"input": state["input"], "messages": messages}, config
        )
        parsed = self.json_parser.batch(new_candidates)
        flattened = [
            (i, tool_call)
            for i, tool_calls in enumerate(parsed)
            for tool_call in tool_calls
        ]
        tool_responses = [
            (
                i,
                self.tool_node.invoke(
                    {
                        "messages": [
                            AIMessage(
                                content="",
                                tool_calls=[
                                    {
                                        "name": tool_call["type"],
                                        "args": tool_call["args"],
                                        "id": tool_call["id"],
                                    }
                                ],
                            )
                        ]
                    }
                ),
            )
            for i, tool_call in flattened
        ]
        collected_responses = defaultdict(list)
        for i, resp in tool_responses:
            collected_responses[i].append(resp["messages"][0])
        output_messages = []
        for i, candidate in enumerate(new_candidates):
            output_messages.append([candidate] + collected_responses[i])

        # Reflect on each candidate
        # For tasks with external validation, you'd add that here.
        reflections = self.reflection_chain.batch(
            [{"input": state["input"], "candidate": msges} for msges in output_messages],
            config,
        )
        # Grow tree
        child_nodes = [
            Node(cand, parent=best_candidate, reflection=reflection)
            for cand, reflection in zip(output_messages, reflections)
        ]
        best_candidate.children.extend(child_nodes)
        # We have already extended the tree directly, so we just return the state
        return state

    
    def setup_graph(self):
        builder = StateGraph(TreeState)
        builder.add_node("start", self.generate_initial_response)
        builder.add_node("expand", self.expand)
        builder.add_edge(START, "start")

        builder.add_conditional_edges(
            "start",
            lambda state: should_loop(state, self.num_levels),  # Pass arguments via lambda
            ["expand", END],
    )
        builder.add_conditional_edges(
        "expand",
        lambda state: should_loop(state, self.num_levels),  # Pass arguments via lambda
            ["expand", END],
         )

        return builder


    def run(self,input):
        question = "Generate a table with the average size and weight, as well as the oldest recorded instance for each of the top 5 most common birds."
        last_step = None
        for step in self.app.stream({"input": question},config=self.config):
            last_step = step
            step_name, step_state = next(iter(step.items()))
            #print(step_name)
            #print("rolled out: ", step_state["root"].height)
            #print("---")

        self.solution_node = last_step["expand"]["root"].get_best_solution()
        self.best_trajectory = self.solution_node.get_trajectory(include_reflections=True)
        print(self.best_trajectory[-1].content)

base_agent = LATS()
base_agent.run("Generate a table with the average size and weight, as well as the oldest recorded instance for each of the top 5 most common birds.")