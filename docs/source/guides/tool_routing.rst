Tool Routing and Selection
==========================

As your agent's toolset grows, effectively routing and selecting the right tools becomes essential.

This guide covers advanced patterns for tool routing, selection, and orchestration in Haive.

Understanding Tool Routing

--------------------------

Tool routing refers to how an agent decides which tool(s) to use in response to a task. In Haive,

tool routing can be:

1. **LLM-drive*n**: The language model selects tools based on context*

2.*** *Rule-base**d*: Predetermined logic selects tools based on triggers

3.*** *Hybri**d*: Combining LLM decisions with programmatic constraints

LLM-Driven Tool Selection

-------------------------

The most flexible approach lets the LLM choose tools:

.. code-block:: python

    # Code example here

    from haive.agents.react import ReactAgent
    from haive.tools import WebSearch, Calculator, WeatherTool

    agent = ReactAgent(
    tools=[WebSearch(), Calculator(), WeatherTool()],
    llm="anthropic/claude-3-sonnet-20240229"
    )

    # The LLM will decide which tool(s) to use
    response = agent.run("I need to know if I should take an umbrella tomorrow in Seattle")

    Rule-Based Tool Selection


-------------------------

    For more control, implement rules:

.. code-block:: python

    # Code example here

    from haive.core.graph.node import ToolNode
    from haive.core.graph import StateGraph

    def tool_selector(state):
    query = state.query.lower()

    if "weather" in query or "temperature" in query or "umbrella" in query:
    return {"tool": "weather_tool"}

elif "calculate" in query or any(op in query for op in ["+", "-", ***"", "/"]):*
    return {"tool": "calculator"}
    else:
    return {"tool": "web_search"}

    graph = StateGraph()
    graph.add_node("tool_selector", tool_selector)
    graph.add_node("weather_tool", ToolNode(WeatherTool()))
    graph.add_node("calculator", ToolNode(Calculator()))
    graph.add_node("web_search", ToolNode(WebSearch()))

    # Connect nodes
    graph.add_edge("tool_selector", "weather_tool", condition=lambda state: state.tool == "weather_tool")
    graph.add_edge("tool_selector", "calculator", condition=lambda state: state.tool == "calculator")
    graph.add_edge("tool_selector", "web_search", condition=lambda state: state.tool == "web_search")

    Tool Filtering and Constraints

    ------------------------------

    Limiting tool access based on context:

.. code-block:: python

    # Code example here

    class RestrictedToolAgent(ReactAgent):
    def get_available_tools(self, query):
    """Return only relevant tools based on the query."""
    all_tools = self.tools

    # Simple filtering example
    if "code" not in query.lower():
    # Filter out code execution tools for non-code related queries
    return [t for t in all_tools if "code" not in t.name.lower()]

    return all_tools

    Dynamic Tool Loading


--------------------

    Load tools on demand to optimize resource usage:

.. code-block:: python

    # Code example here

    class DynamicToolAgent(ReactAgent):

def __init__(self,* args,* **kwargs):*
    super().__init__***(args,* **kwargs)
    self.tool_registry = {}  # Cache for loaded tools

    def get_tool(self, tool_name):
    # Load tool only when needed
    if tool_name not in self.tool_registry:
    if tool_name == "database_query":
    # Only establish database connection when needed
    self.tool_registry[tool_name] = DatabaseQueryTool()
    elif tool_name == "image_generator":
    # Only load large ML models when needed
    self.tool_registry[tool_name] = ImageGenerationTool()

    return self.tool_registry.get(tool_name)

    Tool Pipelines

    --------------

    Chain tools together for complex workflows:

.. code-block:: python

    # Code example here

    from haive.core.graph import StateGraph
    from haive.core.graph.node import ToolNode, LLMNode

    # Create a pipeline of tools
    graph = StateGraph()

    # Add nodes
    graph.add_node("web_search", ToolNode(WebSearch()))
    graph.add_node("content_filter", ToolNode(ContentFilter()))
    graph.add_node("summarizer", LLMNode(summarize_content))
    graph.add_node("formatter", ToolNode(OutputFormatter()))

    # Connect in sequence
    graph.add_edge("web_search", "content_filter")
    graph.add_edge("content_filter", "summarizer")
    graph.add_edge("summarizer", "formatter")

    Observability and Monitoring


----------------------------

    Track tool usage to optimize performance:

.. code-block:: python

    # Code example here

    class MonitoredAgent(ReactAgent):

def __init__(self,*** args,* **kwargs):
    super().__init__***(args,* **kwargs)
    self.tool_usage = {}

    def run_tool(self, tool_name,*** *kwargs):
    start_time = time.time()
    result = super().run_tool(tool_name,*** *kwargs)
    execution_time = time.time() - start_time

    # Record usage
    if tool_name not in self.tool_usage:
    self.tool_usage[tool_name] = {"count": 0, "total_time": 0}

    self.tool_usage[tool_name]["count"] += 1
    self.tool_usage[tool_name]["total_time"] += execution_time

    return result

    def get_tool_metrics(self):
    return {
    tool: {
    "count": data["count"],
    "avg_time": data["total_time"] / data["count"] if data["count"] > 0 else 0
    }
    for tool, data in self.tool_usage.items()
    }

    Next Steps

    ----------

    To further enhance your tool routing capabilities:

    - Learn about the :mod:``haive.core.graph system for complex routing logic``

    - Explore :doc:`advanced_patterns for sophisticated agent architectures`
    - Check out :doc:`performance for optimizing tool execution***`
