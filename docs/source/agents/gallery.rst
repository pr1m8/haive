Agent Gallery & Examples
========================

This gallery showcases practical examples of using various Haive agents for real-world tasks.

Simple Agent Examples
---------------------

Basic Conversation
~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from haive.agents.simple import SimpleAgent
    from haive.core.engine import AugLLMConfig

    # Create a simple conversational agent
    agent = SimpleAgent(
    name="assistant",
    engine=AugLLMConfig(
    temperature=0.7,
    system_message="You are a helpful AI assistant."
    )
    )

    # Single turn conversation
    import asyncio

    async def run_conversation():
    response = await agent.arun("What's the capital of France?")
    print(response)

    # Multi-turn conversation with state
    config = {"configurable": {"thread_id": "conv-123"}}

    await agent.arun("My name is Alice", config=config)
    response = await agent.arun("What's my name?", config=config)
    print(response)  # Will remember "Alice"

    asyncio.run(run_conversation())

    Structured Output
    ~~~~~~~~~~~~~~~~~

.. code-block:: python

    from haive.agents.simple.structured import StructuredSimpleAgent
    from pydantic import BaseModel

    class MovieReview(BaseModel):
    title: str
    rating: float
    summary: str
    pros: list[str]
    cons: list[str]

    agent = StructuredSimpleAgent(
    name="reviewer",
    output_schema=MovieReview
    )

    import asyncio

    async def get_review():
    review = await agent.arun(
    "Review the movie 'Inception' directed by Christopher Nolan"
    )
    print(review.rating)  # Structured output
    return review

    review = asyncio.run(get_review())

    ReAct Agent Examples
    --------------------

    Web Research
    ~~~~~~~~~~~~

.. code-block:: python

    from haive.agents.react import ReactAgent
    from haive.tools import WebSearchTool, WikipediaTool, CalculatorTool

    # Create research agent with tools
    agent = ReactAgent(
    name="researcher",
    tools=[
    WebSearchTool(),
    WikipediaTool(),
    CalculatorTool()
    ],
    max_iterations=5,
    verbose=True
    )

    # Research task with reasoning
    import asyncio

    async def run_research():
    result = await agent.arun(
    "What is the population density of Tokyo? "
    "Compare it to New York City and explain the difference."
    )
    # Access reasoning trace
    print(agent.get_reasoning_trace())
    return result

    result = asyncio.run(run_research())

    Code Analysis
    ~~~~~~~~~~~~~

.. code-block:: python

    from haive.agents.react import ReactAgent
    from haive.tools.code import CodeAnalyzer, GitTool

    agent = ReactAgent(
    name="code_analyst",
    tools=[CodeAnalyzer(), GitTool()],
    system_message="You are an expert code reviewer."
    )

    import asyncio

    async def analyze_code():
    analysis = await agent.arun(
    "Analyze the code quality of the main.py file "
    "and suggest improvements"
    )
    return analysis

    analysis = asyncio.run(analyze_code())

    RAG Agent Examples
    ------------------

    Document Q&A
    ~~~~~~~~~~~~

.. code-block:: python

    from haive.agents.rag.simple import SimpleRAGAgent
    from haive.core.retrieval import VectorRetriever
    from haive.core.embeddings import OpenAIEmbeddings

    # Setup retriever
    retriever = VectorRetriever(
    collection="product_docs",
    embeddings=OpenAIEmbeddings(),
    top_k=5
    )

    # Create RAG agent
    agent = SimpleRAGAgent(
    name="doc_assistant",
    retriever=retriever,
    llm_config={"temperature": 0.3}
    )

    # Ask questions about documents
    import asyncio

    async def get_answer():
    answer = await agent.arun(
    "What are the key features of the Pro plan?"
    )
    # Get source documents
    sources = agent.get_source_documents()
    for doc in sources:
    print(f"Source: {doc.metadata['source']}")
    return answer

    answer = asyncio.run(get_answer())

    Adaptive RAG
    ~~~~~~~~~~~~

.. code-block:: python

    from haive.agents.rag.adaptive_rag import AdaptiveRAGAgent

    # Adaptive RAG that chooses retrieval strategy
    agent = AdaptiveRAGAgent(
    name="adaptive_qa",
    strategies=["simple", "multi_query", "hyde", "fusion"],
    retriever=retriever
    )

    # Complex question requiring adaptive strategy
    import asyncio

    async def run_adaptive():
    result = await agent.arun(
    "Compare and contrast the different pricing tiers, "
    "focusing on enterprise features"
    )
    # See which strategy was used
    print(f"Strategy used: {agent.last_strategy}")
    return result

    result = asyncio.run(run_adaptive())

    Conversation Agent Examples
    ---------------------------

    Debate Simulation
    ~~~~~~~~~~~~~~~~~

.. code-block:: python

    from haive.agents.conversation.debate import DebateConversation

    # Create a debate on AI ethics
    debate = DebateConversation.create_simple_debate(
    topic="Should AI systems be required to explain their decisions?",
    position_a=("Alice", "Pro-transparency: All AI decisions should be explainable"),
    position_b=("Bob", "Pro-efficiency: Some AI systems work better as black boxes"),
    enable_judge=True,
    arguments_per_side=3
    )

    # Run the debate
    import asyncio

    async def run_debate():
    result = await debate.arun()
    # Visualize the debate flow
    debate.visualize_graph("debate_graph.png")
    return result

    result = asyncio.run(run_debate())

    Collaborative Problem Solving
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from haive.agents.conversation.collaberative import CollaborativeConversation
    from haive.agents.simple import SimpleAgent

    # Create specialized agents
    analyst = SimpleAgent(
    name="analyst",
    system_message="You are a data analyst expert."
    )

    engineer = SimpleAgent(
    name="engineer", 
    system_message="You are a software engineer."
    )

    designer = SimpleAgent(
    name="designer",
    system_message="You are a UX designer."
    )

    # Create collaborative conversation
    collab = CollaborativeConversation(
    name="product_team",
    participant_agents={
    "analyst": analyst,
    "engineer": engineer,
    "designer": designer
    },
    task="Design a new dashboard for data visualization"
    )

    import asyncio

    async def run_collaboration():
    solution = await collab.arun()
    return solution

    solution = asyncio.run(run_collaboration())

    Multi-Agent Examples
    --------------------

    Research Pipeline
    ~~~~~~~~~~~~~~~~~

.. code-block:: python

    from haive.agents.multi import MultiAgent
    from haive.agents.research.person import PersonResearchAgent
    from haive.agents.rag.simple import SimpleRAGAgent
    from haive.agents.simple import SimpleAgent

    # Create specialized agents
    researcher = PersonResearchAgent(name="researcher")
    fact_checker = SimpleRAGAgent(
    name="fact_checker",
    retriever=fact_db_retriever
    )
    writer = SimpleAgent(
    name="writer",
    system_message="You are a professional writer."
    )

    # Create multi-agent pipeline
    pipeline = MultiAgent(
    name="research_pipeline",
    agents=[researcher, fact_checker, writer],
    routing_strategy="sequential",
    state_schema=ResearchState
    )

    # Run pipeline
    import asyncio

    async def run_pipeline():
    article = await pipeline.arun({
    "topic": "Recent advances in quantum computing",
    "style": "technical blog post",
    "length": "1500 words"
    })
    return article

    article = asyncio.run(run_pipeline())

    Supervisor Pattern
    ~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from haive.agents.supervisor import SupervisorAgent

    # Create supervisor that delegates tasks
    supervisor = SupervisorAgent(
    name="project_manager",
    team_agents={
    "researcher": research_agent,
    "analyst": analysis_agent,
    "writer": writing_agent
    },
    delegation_strategy="skill_based"
    )

    import asyncio

    async def run_supervisor():
    result = await supervisor.arun(
    "Create a comprehensive market analysis report "
    "for the EV charging industry"
    )
    return result

    result = asyncio.run(run_supervisor())

    Advanced Examples
    -----------------

    Self-Healing Code Agent
    ~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from haive.agents.self_healing_code import SelfHealingCodeAgent

    agent = SelfHealingCodeAgent(
    name="code_fixer",
    language="python",
    test_command="pytest",
    max_attempts=3
    )

    # Fix broken code
    import asyncio

    async def fix_code():
    fixed_code = await agent.arun({
    "code": broken_code,
    "error": error_message,
    "requirements": "Fix the code to pass all tests"
    })
    return fixed_code

    fixed_code = asyncio.run(fix_code())

    Tree of Thoughts Reasoning
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from haive.agents.reasoning_and_critique.tot import TreeOfThoughtsAgent

    agent = TreeOfThoughtsAgent(
    name="problem_solver",
    branch_factor=3,
    max_depth=4,
    evaluation_strategy="value_function"
    )

    import asyncio

    async def solve_problem():
    solution = await agent.arun(
    "Design an algorithm to optimize delivery routes "
    "for a fleet of 50 vehicles across a city"
    )
    # Visualize reasoning tree
    agent.visualize_reasoning_tree("tot_reasoning.png")
    return solution

    solution = asyncio.run(solve_problem())

    Visualization Examples
    ----------------------

    Agent Graph Visualization
    ~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # For any agent, visualize its execution graph
    agent = ReactAgent(name="viz_example", tools=[...])

    # Generate static image
    agent.visualize_graph("agent_graph.png", format="png")

    # Generate interactive HTML
    agent.visualize_graph("agent_graph.html", format="html")

    # Get graph object for custom visualization
    graph = agent.graph
    graph.view()  # Opens in default viewer

    State Flow Visualization
    ~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from haive.agents.multi import MultiAgent

    multi_agent = MultiAgent(agents=[...])

    # Visualize state transitions
    multi_agent.visualize_state_flow(
    "state_flow.png",
    include_conditions=True,
    highlight_path=True
    )

    Performance Monitoring
    ----------------------

.. code-block:: python

    from haive.agents.react import ReactAgent
    from haive.core.monitoring import AgentMonitor

    # Create agent with monitoring
    agent = ReactAgent(
    name="monitored_agent",
    tools=[...],
    enable_monitoring=True
    )

    # Run with performance tracking
    import asyncio

    async def run_with_monitoring():
    with AgentMonitor(agent) as monitor:
    result = await agent.arun("Complex task...")

    # Get performance metrics
    metrics = monitor.get_metrics()
    print(f"Total time: {metrics.total_time}s")
    print(f"Tool calls: {metrics.tool_calls}")
    print(f"Tokens used: {metrics.tokens_used}")
    return result

    result = asyncio.run(run_with_monitoring())

    Best Practices
    --------------

    1. **State Management**: Always use thread_id for conversation continuity
    2. **Error Handling**: Implement proper error handling for production use
    3. **Resource Management**: Set appropriate timeouts and token limits
    4. **Monitoring**: Enable monitoring for production deployments
    5. **Testing**: Write comprehensive tests for custom agents

    Next Steps
    ----------

    - Explore the :doc:`api_reference` for detailed documentation
    - Check out :doc:`showcase` for production examples
    - Read the :doc:`../guides/building_agents` guide to create custom agents
