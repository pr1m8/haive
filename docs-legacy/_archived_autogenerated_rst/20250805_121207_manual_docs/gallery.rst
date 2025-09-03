🖼️ Example Gallery



Welcome to the Haive Example Gallery! Here you'll find comprehensive examples showcasing the capabilities of each package.

.. note::


   Grid layout removed due to sphinx_design incompatibility.


    .. grid-item-card:: 🤖 Agent Examples

        :class-card: showcase-card

        Explore agent examples from SimpleAgent to ReactAgent to complex multi-agent workflows.

        +++

        .. button-ref:: auto_examples_agents/index
            :expand:
            :color: primary
            :click-parent:

            View Agent Gallery

    .. grid-item-card:: 🛠️ Tool Examples

        :class-card: showcase-card

        Discover how to create custom tools and integrate them with agents.

        +++

        .. button-ref:: auto_examples_tools/index
            :expand:
            :color: secondary
            :click-parent:

            View Tool Gallery

    .. grid-item-card:: 🎮 Game Examples

        :class-card: showcase-card

        See AI agents in action playing games like Tic-Tac-Toe, Chess, and more.

        +++

        .. button-ref:: auto_examples_games/index
            :expand:
            :color: success
            :click-parent:

            View Game Gallery

    .. grid-item-card:: 🔌 MCP Examples

        :class-card: showcase-card

        Learn how to integrate with external tools and services via MCP.

        +++

        .. button-ref:: auto_examples_mcp/index
            :expand:
            :color: warning
            :click-parent:

            View MCP Gallery

Featured Examples



.. note::


   Grid layout removed due to sphinx_design incompatibility.


    .. grid-item-card:: 🎯 Tic-Tac-Toe AI Battle

        :class-card: featured-card

        Watch two AI agents battle it out in a strategic game of Tic-Tac-Toe.

        - Strategic vs Creative AI personalities
        - Real-time game state display
        - Move-by-move decision tracking

    .. grid-item-card:: 🔧 Custom Tool Creation

        :class-card: featured-card

        Learn to build powerful custom tools for your agents.

        - Type-safe tool definitions
        - Pydantic model integration
        - Error handling patterns

Gallery Contents



All examples in this gallery are:

✅ **Fully Runnable** - Complete working code you can execute
✅ **Well Documented** - Clear explanations and inline comments
✅ **Best Practices** - Following Haive's coding standards
✅ **Real Components** - No mocks, using actual LLMs and tools

Getting Started



To run any example:

1. **Install Haive** with the relevant extras:

.. code-block:: bash



       poetry install --extras "agents tools games mcp"

       2. **Set Environment Variables** (if needed):

.. code-block:: bash



       export OPENAI_API_KEY="your-api-key"
       export ANTHROPIC_API_KEY="your-api-key"

       3. **Run the Example**:

.. code-block:: bash



       poetry run python packages/haive-agents/examples/simple_agent_example.py

       .. toctree::


       :hidden:
       :maxdepth: 2

       auto_examples_agents/index
       auto_examples_tools/index
       auto_examples_games/index
       auto_examples_mcp/index
