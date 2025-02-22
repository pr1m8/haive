Usage
=====

Basic Usage
----------

.. code-block:: python

    from haive.agents import ReActAgent
    from haive.core.config import Config
    
    # Create a configuration
    config = Config()
    config.set("model", "gpt-4")
    
    # Initialize an agent
    agent = ReActAgent(config)
    
    # Run the agent
    result = agent.run("Solve this math problem: If x + 2y = 15 and 2x - y = 5, what are x and y?")
    
    print(result)

Advanced Usage
-------------

.. code-block:: python

    from haive.agents.tot import ToTAgent
    from haive.core.utils import format_response
    
    # Initialize a Tree of Thought agent
    agent = ToTAgent(
        model="gpt-4",
        max_depth=3,
        beam_width=5
    )
    
    # Run the agent with a complex reasoning task
    result = agent.solve(
        "Design an algorithm to find the longest palindromic substring in a string."
    )
    
    # Format the result for display
    # Format the result for display
    formatted = format_response(result)
    
    print(formatted)
