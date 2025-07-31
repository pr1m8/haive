.. title:: ReactAgent - Reasoning and Acting Agent
.. _react-agent:

🧠 ReactAgent Documentation
============================

.. raw:: html

   <div class="agent-hero-section">
      <div class="hero-content">
         <h2>🧠 Reasoning and Acting Agent</h2>
         <p class="hero-description">
            ReactAgent combines reasoning with action through tool usage. It thinks step-by-step, 
            uses tools to gather information, and produces well-reasoned responses based on real data.
         </p>
      </div>
   </div>

Overview
--------

ReactAgent implements the ReAct (Reasoning and Acting) paradigm, allowing agents to:

- Break down complex problems into steps
- Use tools to gather information
- Reason about tool outputs
- Self-correct and retry when needed
- Provide transparent reasoning chains

.. raw:: html

   <div class="showcase-section">
      <div class="showcase-header">
         <h2>✨ Key Features</h2>
      </div>
      <div class="api-grid">
         <div class="api-section">
            <h4>🔧 Tool Integration</h4>
            <ul>
               <li>Dynamic tool selection</li>
               <li>Parallel tool execution</li>
               <li>Tool output interpretation</li>
               <li>Error recovery</li>
            </ul>
         </div>
         
         <div class="api-section">
            <h4>🤔 Reasoning Capabilities</h4>
            <ul>
               <li>Step-by-step planning</li>
               <li>Multi-hop reasoning</li>
               <li>Self-reflection</li>
               <li>Chain-of-thought</li>
            </ul>
         </div>
         
         <div class="api-section">
            <h4>🎯 Advanced Features</h4>
            <ul>
               <li>Retry mechanisms</li>
               <li>Context preservation</li>
               <li>Tool composition</li>
               <li>Reasoning traces</li>
            </ul>
         </div>
      </div>
   </div>

Quick Start
-----------

.. raw:: html

   <div class="code-example-section">
      <h4>🚀 Basic Usage with Tools</h4>

.. code-block:: python

   from haive.agents.react import ReactAgent
   from haive.core.engine.aug_llm import AugLLMConfig
   from langchain_core.tools import tool

   # Define custom tools
   @tool
   def calculator(expression: str) -> str:
       """Evaluate mathematical expressions."""
       try:
           result = eval(expression, {"__builtins__": {}}, {})
           return str(result)
       except Exception as e:
           return f"Error: {e}"

   @tool
   def web_search(query: str) -> str:
       """Search the web for information."""
       # Simulated search results
       return f"Search results for '{query}': [relevant information]"

   @tool
   def weather_api(location: str) -> str:
       """Get current weather for a location."""
       # Simulated weather data
       return f"Weather in {location}: Sunny, 72°F"

   # Create ReactAgent with tools
   agent = ReactAgent(
       name="research_assistant",
       engine=AugLLMConfig(
           temperature=0.7,
           system_message="You are a helpful research assistant."
       ),
       tools=[calculator, web_search, weather_api],
       max_iterations=5,  # Maximum reasoning steps
       return_intermediate_steps=True  # Show reasoning
   )

   # Use the agent
   result = await agent.arun(
       "What's the weather in Tokyo and how many hours of daylight "
       "does it have if sunrise is at 5:30 AM and sunset at 6:45 PM?"
   )

   # The agent will:
   # 1. Use weather_api to get Tokyo weather
   # 2. Use calculator to compute daylight hours
   # 3. Combine results into final answer

.. raw:: html

   </div>

Tool Management
---------------

.. raw:: html

   <div class="custom-section">
      <h3>🔧 Working with Tools</h3>

.. code-block:: python

   from haive.tools.search import WebSearchTool
   from haive.tools.code import PythonREPLTool
   from haive.tools.math import CalculatorTool
   from haive.agents.react import ReactAgent
   from pydantic import BaseModel, Field
   from typing import List, Dict, Any

   # Using pre-built tools
   search_tool = WebSearchTool()
   python_tool = PythonREPLTool()
   calc_tool = CalculatorTool()

   # Custom tool with structured input
   class DatabaseQuery(BaseModel):
       """Input schema for database queries."""
       table: str = Field(..., description="Table name")
       query: str = Field(..., description="SQL query")
       limit: int = Field(10, description="Result limit")

   @tool(args_schema=DatabaseQuery)
   def query_database(table: str, query: str, limit: int = 10) -> str:
       """Execute database queries safely."""
       # Validate and execute query
       return f"Results from {table}: [data]"

   # Tool with async support
   @tool
   async def fetch_api_data(endpoint: str) -> Dict[str, Any]:
       """Fetch data from external API."""
       import aiohttp
       async with aiohttp.ClientSession() as session:
           async with session.get(f"https://api.example.com/{endpoint}") as resp:
               return await resp.json()

   # Create agent with diverse tools
   agent = ReactAgent(
       name="data_analyst",
       engine=AugLLMConfig(),
       tools=[
           search_tool,
           python_tool,
           calc_tool,
           query_database,
           fetch_api_data
       ],
       tool_choice="auto",  # Let agent choose tools
       verbose=True  # Show tool usage
   )

   # Dynamic tool addition
   @tool
   def new_tool(input: str) -> str:
       """A new tool added dynamically."""
       return f"Processed: {input}"

   agent.add_tool(new_tool)

.. raw:: html

   </div>

Reasoning Patterns
------------------

.. raw:: html

   <div class="showcase-section">
      <div class="showcase-header">
         <h2>🤔 Reasoning Strategies</h2>
      </div>

.. code-block:: python

   # Configure reasoning behavior
   agent = ReactAgent(
       name="reasoner",
       engine=AugLLMConfig(),
       tools=[...],
       # Reasoning configuration
       max_iterations=5,              # Max reasoning steps
       early_stopping_method="force", # How to stop
       return_intermediate_steps=True,# Include reasoning
       handle_parsing_errors=True,    # Recover from errors
       # Custom prompts for reasoning
       system_message="""You are an expert problem solver.
       Always think step by step:
       1. Understand the problem
       2. Plan your approach
       3. Execute with tools
       4. Verify results
       5. Synthesize final answer"""
   )

   # Example: Multi-step reasoning
   result = await agent.arun("""
   I need to plan a trip from New York to Tokyo next month.
   Find:
   1. Current flight prices
   2. Weather forecast
   3. Currency exchange rate
   4. Total estimated cost for 7 days including hotel
   """)

   # Access reasoning trace
   if agent.return_intermediate_steps:
       for step in result["intermediate_steps"]:
           action = step[0]  # Tool and input
           observation = step[1]  # Tool output
           print(f"Tool: {action.tool}")
           print(f"Input: {action.tool_input}")
           print(f"Output: {observation}\n")

   # Custom reasoning loop
   class CustomReactAgent(ReactAgent):
       async def _arun(self, input_data: Dict[str, Any], **kwargs):
           """Custom reasoning implementation."""
           # Initial planning
           plan = await self._plan(input_data)
           
           # Execute plan with tools
           results = []
           for step in plan:
               try:
                   result = await self._execute_tool(step)
                   results.append(result)
               except Exception as e:
                   # Custom error handling
                   result = await self._handle_error(e, step)
                   results.append(result)
           
           # Synthesize results
           final_answer = await self._synthesize(results)
           return final_answer

.. raw:: html

   </div>

Error Handling and Recovery
---------------------------

.. raw:: html

   <div class="warning-section">
      <h3>⚠️ Robust Error Handling</h3>

.. code-block:: python

   from haive.agents.react import ReactAgent
   from langchain_core.tools import tool
   from tenacity import retry, stop_after_attempt, wait_exponential

   # Tool with built-in error handling
   @tool
   def risky_operation(input: str) -> str:
       """Operation that might fail."""
       import random
       if random.random() < 0.3:  # 30% failure rate
           raise Exception("Operation failed")
       return f"Success: {input}"

   # Agent with retry logic
   agent = ReactAgent(
       name="resilient_agent",
       engine=AugLLMConfig(),
       tools=[risky_operation],
       # Error handling config
       handle_parsing_errors=True,
       max_retries=3,
       retry_delay=1.0
   )

   # Custom error recovery
   @retry(
       stop=stop_after_attempt(3),
       wait=wait_exponential(multiplier=1, min=4, max=10)
   )
   async def robust_query(agent, query):
       try:
           result = await agent.arun(query)
           return result
       except Exception as e:
           # Log error
           print(f"Error: {e}")
           # Try alternative approach
           fallback_query = f"Please try a simpler approach: {query}"
           return await agent.arun(fallback_query)

   # Handle tool failures gracefully
   class RobustReactAgent(ReactAgent):
       async def _handle_tool_error(self, error, tool_name, tool_input):
           """Custom tool error handling."""
           # Log the error
           self.logger.error(f"Tool {tool_name} failed: {error}")
           
           # Try alternative tool
           alternative = self._find_alternative_tool(tool_name)
           if alternative:
               return await self._execute_tool(alternative, tool_input)
           
           # Fallback to reasoning without tool
           return await self._reason_without_tool(tool_input)

.. raw:: html

   </div>

Advanced Patterns
-----------------

.. raw:: html

   <div class="api-grid">
      <div class="api-section">
         <h4>🔄 Iterative Refinement</h4>

.. code-block:: python

   # Self-improving responses
   agent = ReactAgent(
       name="refiner",
       engine=AugLLMConfig(),
       tools=[...],
       enable_reflection=True
   )

   async def iterative_solve(agent, problem, max_iter=3):
       solution = None
       for i in range(max_iter):
           prompt = f"""
           Problem: {problem}
           Current solution: {solution or 'None'}
           
           Improve the solution or indicate if done.
           """
           solution = await agent.arun(prompt)
           
           if "final answer" in solution.lower():
               break
       
       return solution

.. raw:: html

      </div>
      
      <div class="api-section">
         <h4>🌐 Tool Composition</h4>

.. code-block:: python

   # Combine multiple tools
   @tool
   def composite_tool(query: str) -> str:
       """Use multiple tools together."""
       search_results = web_search.invoke(query)
       analysis = analyzer.invoke(search_results)
       summary = summarizer.invoke(analysis)
       return summary

   agent = ReactAgent(
       name="composer",
       tools=[composite_tool]
   )

.. raw:: html

      </div>
   </div>

Performance Optimization
------------------------

.. raw:: html

   <div class="custom-section">
      <h3>⚡ Optimization Strategies</h3>

.. code-block:: python

   # Parallel tool execution
   agent = ReactAgent(
       name="fast_agent",
       engine=AugLLMConfig(),
       tools=[...],
       # Performance settings
       parallel_tool_calls=True,      # Execute tools in parallel
       tool_call_timeout=10.0,        # Timeout per tool
       cache_tool_results=True,       # Cache repeated calls
       max_concurrent_tools=5         # Limit parallelism
   )

   # Batch processing
   async def batch_process(agent, queries):
       import asyncio
       
       # Process queries concurrently
       tasks = [agent.arun(q) for q in queries]
       results = await asyncio.gather(*tasks)
       
       return results

   # Tool result caching
   from functools import lru_cache

   @tool
   @lru_cache(maxsize=100)
   def expensive_computation(input: str) -> str:
       """Cached expensive operation."""
       # Expensive computation here
       return result

   # Streaming responses
   agent = ReactAgent(
       name="streaming_agent",
       engine=AugLLMConfig(streaming=True),
       tools=[...]
   )

   async for chunk in agent.astream("Complex query"):
       print(chunk, end="", flush=True)

.. raw:: html

   </div>

Monitoring and Debugging
------------------------

.. raw:: html

   <div class="showcase-section">
      <div class="showcase-header">
         <h2>🔍 Debugging ReactAgent</h2>
      </div>

.. code-block:: python

   import logging
   from haive.agents.react import ReactAgent

   # Enable detailed logging
   logging.basicConfig(level=logging.DEBUG)
   logger = logging.getLogger("haive.agents.react")

   # Debug mode agent
   agent = ReactAgent(
       name="debug_agent",
       engine=AugLLMConfig(),
       tools=[...],
       verbose=True,                   # Print reasoning steps
       return_intermediate_steps=True, # Include all steps
       debug=True                      # Enable debug mode
   )

   # Custom callbacks for monitoring
   class MonitoringCallback:
       def on_tool_start(self, tool_name, tool_input):
           print(f"[TOOL START] {tool_name}: {tool_input}")
       
       def on_tool_end(self, tool_name, tool_output):
           print(f"[TOOL END] {tool_name}: {tool_output[:100]}...")
       
       def on_reasoning_step(self, thought):
           print(f"[REASONING] {thought}")

   agent.callbacks = [MonitoringCallback()]

   # Trace execution
   result = await agent.arun("Complex query", trace=True)

   # Analyze performance
   print(f"Total time: {result['metadata']['total_time']}s")
   print(f"Tool calls: {result['metadata']['tool_calls']}")
   print(f"Tokens used: {result['metadata']['tokens']}")

.. raw:: html

   </div>

Complete Example
----------------

.. raw:: html

   <div class="code-example-section">
      <h4>🎯 Full Research Assistant Example</h4>

.. code-block:: python

   import asyncio
   from haive.agents.react import ReactAgent
   from haive.core.engine.aug_llm import AugLLMConfig
   from haive.tools.search import WebSearchTool
   from haive.tools.code import PythonREPLTool
   from langchain_core.tools import tool
   from pydantic import BaseModel
   from typing import List, Dict

   # Define structured output for research
   class ResearchReport(BaseModel):
       topic: str
       summary: str
       key_findings: List[str]
       data_points: Dict[str, float]
       sources: List[str]
       recommendations: List[str]

   # Custom tools for research
   @tool
   def analyze_data(data: str) -> str:
       """Analyze data and return insights."""
       # Simulated analysis
       return "Key insights: Growth trend observed, 15% increase YoY"

   @tool
   def generate_chart(data: str, chart_type: str = "bar") -> str:
       """Generate visualization from data."""
       return f"Generated {chart_type} chart: [chart_url]"

   async def main():
       # Create comprehensive research agent
       agent = ReactAgent(
           name="research_assistant",
           engine=AugLLMConfig(
               model="gpt-4",
               temperature=0.7,
               system_message="""You are an expert research assistant.
               Always provide thorough, well-researched answers with sources."""
           ),
           tools=[
               WebSearchTool(),
               PythonREPLTool(),
               analyze_data,
               generate_chart
           ],
           max_iterations=10,
           return_intermediate_steps=True
       )

       # Conduct research
       research_query = """
       Research the current state of renewable energy adoption globally.
       I need:
       1. Current statistics and trends
       2. Top 5 countries by renewable energy usage
       3. Cost comparisons with fossil fuels
       4. Future projections for 2030
       5. Key challenges and opportunities
       
       Please create visualizations where appropriate.
       """

       print("Starting research...")
       result = await agent.arun(research_query)
       
       # Process results into structured report
       report_agent = ReactAgent(
           name="report_generator",
           engine=AugLLMConfig(temperature=0.3),
           tools=[],
           structured_output_model=ResearchReport
       )
       
       report = await report_agent.arun(f"""
       Based on this research, create a structured report:
       {result}
       """)
       
       # Display report
       print(f"\n{'='*60}")
       print(f"Research Report: {report.topic}")
       print(f"{'='*60}")
       print(f"\nSummary:\n{report.summary}")
       print(f"\nKey Findings:")
       for i, finding in enumerate(report.key_findings, 1):
           print(f"{i}. {finding}")
       print(f"\nData Points:")
       for key, value in report.data_points.items():
           print(f"  - {key}: {value}")
       print(f"\nRecommendations:")
       for i, rec in enumerate(report.recommendations, 1):
           print(f"{i}. {rec}")
       print(f"\nSources: {len(report.sources)} references used")

   if __name__ == "__main__":
       asyncio.run(main())

.. raw:: html

   </div>

API Reference
-------------

.. autoclass:: haive.agents.react.ReactAgent
   :members:
   :inherited-members:
   :show-inheritance:

.. seealso::

   - :doc:`../../tools/index` - Available tools for ReactAgent
   - :doc:`../../guides/building_react_agents` - Advanced ReactAgent patterns
   - :doc:`../planning/index` - Planning agents that extend ReactAgent