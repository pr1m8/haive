Using Tools



Tools are a fundamental building block in Haive that enable agents to interact with external systems,

retrieve information, and perform specific actions. This guide will walk you through how to use

existing tools and toolkits within your Haive agents.

What are Tools?


--------------

In Haive, a tool is a function that:

1. Takes structured input

2. Performs a specific action

3. Returns structured output

Tools can be simple utilities (like generating random numbers) or complex integrations (like querying

APIs, searching the web, or executing code).

Built-in Tools


-------------

Haive comes with several built-in tools:

- **Search Tool*s**: Query search engines, retrieve web content**

-*** *Math Tool**s**: Perform calculations, solve equations
-*** *Code Tool**s**: Execute Python code safely
-*** *Utility Tool**s**: Generate random data, parse content

Using Tools with Agents


----------------------

To use tools with an agent, you need to:

1. Import the desired tools

2. Add them to your agent configuration

3. Enable the agent to access and invoke them

Here's a simple example using the React agent pattern:

.. code-block:: python

    # Code example here

    from haive.agents.react import ReactAgent
    from haive.tools.search import WebSearch
    from haive.tools.math import Calculator

    # Create an agent with tools
    agent = ReactAgent(
    tools=[WebSearch(), Calculator()],
    llm="anthropic/claude-3-sonnet-20240229"
    )

    # Run the agent with tools
    response = agent.run("Calculate the square root of 16 and then find information about that number")

    When to Use Tools



----------------

    Tools are particularly useful when:

    - Your agent needs to access external data (search, API calls)

    - Specialized calculations or operations are required
    - You want to limit an agent to specific capabilities
    - Complex tasks require multiple steps or specific operations

    Working with Tool Outputs




    Tool outputs are structured and can be used:

    1. Directly by the agent in its reasoning

    2. As input to other tools

    3. To update the agent's state
    4. As part of the final response

.. code-block:: python

    # Code example here

    # Example of chaining tool outputs
    search_result = web_search.run("latest Mars rover")
    parsed_data = content_parser.run(search_result)
    final_summary = summarizer.run(parsed_data)

    Next Steps



---------

    Now that you understand how to use tools, you might want to:

    - Learn about :doc:`custom_tools - Create your own specialized tools`

`

    - Explore :doc`:`tool_routing - Advanced patterns for tool selection`

`
    - Check out the :mod`:``haive.tools API reference for complete documentation***`

``
`
