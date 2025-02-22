Welcome to Haive
===============

.. raw:: html

   <div style="text-align:center; margin-bottom: 2em;">
     <p style="font-size: 1.2em; color: #555;">
       A powerful framework for building AI agents
     </p>
   </div>

.. grid:: 2

    .. grid-item-card:: Getting Started
        :link: installation
        :link-type: doc
        :class-card: sd-border-0

        Start building with Haive quickly.

    .. grid-item-card:: API Reference
        :link: api/index
        :link-type: doc
        :class-card: sd-border-0

        Explore the Haive API documentation.

Key Features
-----------

- **Flexible Agent Architecture**: Build agents with different reasoning strategies
- **State Management**: Track and manage agent state effectively
- **Tool Integration**: Easily connect agents to external tools and services
- **Extensible Design**: Create custom agents for your specific needs

.. code-block:: python
    :caption: Example: Creating a Simple Agent
    :linenos:

    from haive.agents import SummarizerAgent
    
    # Initialize the agent
    agent = SummarizerAgent()
    
    # Process input text
    result = agent.summarize("Your long text to summarize...")
    
    print(result)

.. toctree::
   :maxdepth: 2
   :caption: Contents:
   :hidden:

   installation
   usage
   api/index
   examples
   contributing
