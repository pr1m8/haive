Quick Start
===========

Your First Agent
-----------------

Let's build a simple conversational agent in just a few lines of code.

Basic Agent
~~~~~~~~~~~

.. code-block:: python

    from haive.agents.simple import SimpleAgent
    from haive.core.engine import create_engine

    # Create an LLM engine
    engine = create_engine("openai", model="gpt-4")

    # Create a simple agent
    agent = SimpleAgent(
    name="assistant",
    engine=engine,
    system_prompt="You are a helpful AI assistant."
    )

    # Run the agent
    response = await agent.arun("Hello! What can you help me with?")
    print(response)

    With Custom State
    ~~~~~~~~~~~~~~~~~

.. code-block:: python

    from haive.agents.base import Agent
    from haive.core.schema import StateSchema
    from pydantic import Field

    # Define custom state
    class ChatState(StateSchema):
    conversation_count: int = Field(default=0)
    topics: list[str] = Field(default_factory=list)

    # Create agent with custom state
    class ChatAgent(Agent[ChatState]):
    def setup_agent(self):
    self._sync_fields_from_engine()
    self._setup_schemas()
    self._build_initial_graph()

    # Use the agent
    agent = ChatAgent(name="chat", engine=engine)
    response = await agent.arun("Let's talk about AI!")

    Multi-Agent Conversation
    ~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from haive.agents.conversation import MultiAgentConversation

    # Create multiple agents
    researcher = SimpleAgent(
    name="researcher", 
    engine=engine,
    system_prompt="You are a research specialist."
    )

    writer = SimpleAgent(
    name="writer",
    engine=engine, 
    system_prompt="You are a technical writer."
    )

    # Create conversation
    conversation = MultiAgentConversation(
    agents=[researcher, writer],
    max_turns=3
    )

    # Run collaborative conversation
    result = await conversation.arun(
    "Research and write about quantum computing"
    )

    Next Steps
    ----------

    Now that you have a basic agent running:

    1. **Explore Examples**: Check out :doc:`../examples/index` for more complex scenarios
    2. **Learn Concepts**: Read :doc:`concepts` to understand the architecture
    3. **Build Tools**: Add custom tools to your agents
    4. **Create Workflows**: Design multi-step agent workflows

    Common Patterns
    ---------------

    **Error Handling**

.. code-block:: python

    try:
    response = await agent.arun(user_input)
    except Exception as e:
    print(f"Agent error: {e}")

    **Streaming Responses**

.. code-block:: python

    async for chunk in agent.astream(user_input):
    print(chunk, end="", flush=True)

    **State Management**

.. code-block:: python

    # Access agent state
    current_state = agent.get_state()

    # Update state
    agent.update_state({"conversation_count": 5})

    **Configuration**

.. code-block:: python

    # Agent with configuration
    agent = SimpleAgent(
    name="configured",
    engine=engine,
    temperature=0.7,
    max_tokens=1000,
    timeout=30.0
    )
