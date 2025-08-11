{{ fullname }}
{{ underline }}

.. currentmodule:: {{ module }}

.. autoclass:: {{ objname }}

   :members:
   :show-inheritance:
   :inherited-members:
   :special-members: __init__

   .. rubric:: Examples

   {% if fullname.endswith('SimpleAgent') %}

.. code-block:: python

    # Code example here

    from {{ module }} import {{ objname }}
    from haive.core.engine import AugLLMConfig

    # Create a simple conversational agent
    agent = {{ objname }}(
    name="assistant",
    engine=AugLLMConfig(temperature=0.7),
    system_message="You are a helpful assistant."
    )

    # Run the agent
    response = await agent.arun("What is the weather like?")
    print(response)
    {% endif %}

    {% if fullname.endswith('ReactAgent') %}
.. code-block:: python

    # Code example here

    from {{ module }} import {{ objname }}
    from haive.tools import SearchTool, CalculatorTool

    # Create a ReAct agent with tools
    agent = {{ objname }}(
    name="researcher",
    tools=[SearchTool(), CalculatorTool()],
    max_iterations=5
    )

    # Run with reasoning and tool use
    result = await agent.arun(
    "Find the population of Tokyo and calculate its density"
    )
    {% endif %}

    {% if 'RAG' in fullname %}
.. code-block:: python

    # Code example here

    from {{ module }} import {{ objname }}
    from haive.core.retrieval import VectorRetriever

    # Create a RAG agent
    agent = {{ objname }}(
    name="rag_assistant",
    retriever=VectorRetriever(collection="docs"),
    llm_config={"temperature": 0.3}
    )

    # Query with retrieval
    answer = await agent.arun(
    "What are the main features of the product?"
    )
    {% endif %}

    {% if 'Conversation' in fullname or 'Debate' in fullname %}
.. code-block:: python

    # Code example here

    from {{ module }} import {{ objname }}

    # Create a conversation/debate agent
    agent = {{ objname }}(
    topic="AI Ethics",
    participants=["Alice", "Bob", "Charlie"],
    max_rounds=5
    )

    # Start the conversation
    result = await agent.arun({
    "initial_prompt": "Should AI be regulated?"
    })
    {% endif %}

    .. rubric:: Graph Visualization

    {% if objname != 'Agent' and objname != 'GenericAgent' %}
    To visualize this agent's execution graph:

.. code-block:: python

    # Code example here

    # Visualize the agent's graph
    agent.visualize_graph("{{ objname.lower() }}_graph.png")

    # Or get the graph object
    graph = agent.graph
    graph.view()  # Opens in default viewer
    {% endif %}

    .. rubric:: Configuration Options

    This agent supports various configuration options through its constructor
    and runtime config. See the parameters section above for details.

    .. rubric:: Related Examples

    {% set example_path = module.replace('.', '/').replace('haive/', 'packages/haive-agents/src/haive/') + '/example.py' %}
    {% if example_path %}
    For more detailed examples, see the example file in the source code.
    {% endif %}
