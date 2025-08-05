Collaborative Conversation Examples
===================================

Collaborative conversations enable agents to work together toward shared goals, building on each other's ideas and reaching consensus through natural dialogue flow.

Problem Solving Session
-----------------------

A team collaboratively solving a technical challenge.

**Full Example Code:*

.. literalinclude:: ../../../../../packages/haive-agents/src/haive/agents/conversation/collaborative/example.py

   :language: python
   :pyobject: example_problem_solving
   :caption: Collaborative Problem Solving

**Running the Example:*

.. code-block:: bash

    poetry run python packages/haive-agents/src/haive/agents/conversation/collaborative/example.py

    **Sample Output:*

.. code-block:: text

    === Collaborative Problem Solving ===

    Topic: Optimizing Database Performance for High-Traffic Application

    DBA: I've noticed our query response times increasing during peak hours.
    The main bottleneck seems to be complex JOIN operations on our user_activity
    table, which has grown to 50 million rows.

    Backend Dev: That makes sense. I've been seeing timeout errors in our logs.
    What if we implement query result caching for frequently accessed data? We
    could use Redis with a 5-minute TTL for user dashboards.

    DevOps: Good idea on caching! I can also help by setting up read replicas
    to distribute the query load. We could route all analytical queries to
    replicas while keeping transactional queries on the primary.

    DBA: Excellent suggestions! Building on the caching idea, we should also
    consider partitioning the user_activity table by date. Queries usually
    only need recent data, so this would significantly reduce scan times.

    Backend Dev: Partitioning would help a lot. I'll also refactor our ORM
    queries to use more efficient eager loading and eliminate N+1 query
    problems I've identified in the codebase.

    System Architect: These are all great tactical solutions. For long-term
    scalability, should we consider event sourcing for user activities? We
    could stream events to a data warehouse for analytics, keeping our
    transactional database lean.

    DBA: Event sourcing is interesting! As an immediate step, I'll create
    indexes on the most common query patterns and archive data older than
    6 months. This should give us breathing room to implement the bigger
    architectural changes.

    DevOps: I'll set up monitoring dashboards for query performance and
    cache hit rates. This way we can measure the impact of each optimization
    and identify any new bottlenecks that emerge.

    Backend Dev: Perfect! Let's implement these changes incrementally. I'll
    start with the caching layer and query optimizations while DBA works on
    partitioning. We can sync up daily on progress.

    System Architect: Agreed. I'll draft the event sourcing architecture
    proposal. Let's aim to have the immediate fixes in production by next
    week and the architectural changes planned for next quarter.

    Creative Design Session
    -----------------------

    A design team collaborating on a new product feature.

    **Full Example Code:*

    .. literalinclude:: ../../../../../packages/haive-agents/src/haive/agents/conversation/collaborative/example.py

    :language: python
    :pyobject: example_design_collaboration
    :caption: Design Team Collaboration

    **Sample Output:*

.. code-block:: text

    === Design Collaboration Session ===

    Topic: Designing an AI-Powered Personal Assistant Feature

    UX Designer: I envision the AI assistant as a friendly companion that
    learns user preferences over time. It should have a conversational
    interface but not feel intrusive. Maybe a subtle icon that expands
    when needed?

    UI Designer: I love the companion concept! For the visual design, we
    could use soft, organic shapes and gentle animations. The icon could
    pulse softly when it has suggestions, like a gentle breathing effect.

    Product Manager: These ideas align well with user feedback. Users want
    help but not interruptions. What if the assistant only appears when
    users seem stuck? We could detect patterns like repeated actions or
    long pauses.

    UX Researcher: Based on our user studies, people are concerned about
    privacy with AI assistants. The design should clearly show when the AI
    is active and what data it's using. Maybe a privacy indicator?

    UI Designer: Great point! I can design a small status indicator that
    shows data usage. We could use color coding - green for local processing,
    blue for cloud. The breathing animation could match these colors.

    UX Designer: Building on the privacy theme, let's give users granular
    controls. They could choose which features the AI can access. The
    onboarding should emphasize user control and transparency.

    Product Manager: I'm seeing a cohesive vision emerging. The assistant
    is helpful but respectful, visually subtle but clear about its actions.
    How about adding a learning mode where users can explicitly teach it?

    UX Researcher: Users would love that! In testing, people wanted to
    correct AI mistakes and see it improve. A simple thumbs up/down on
    suggestions could train it while keeping the interaction lightweight.

    UI Designer: For the teaching interaction, we could use micro-animations
    showing the AI "learning" - maybe the icon briefly transforms or sparkles
    when receiving feedback. It makes the learning process visible and
    satisfying.

    UX Designer: Perfect! Let's prototype this flow: subtle icon → contextual
    appearance → clear privacy indicators → easy feedback mechanism. The
    whole experience should feel like a helpful friend, not a surveillance tool.

    Research Collaboration
    ----------------------

    Researchers collaborating on analyzing findings.

    **Example Code:*

.. code-block:: python

    # Code example here

    from haive.agents.conversation.collaborative import CollaborativeConversation
    from haive.agents.simple import SimpleAgent

    def example_research_collaboration():
    """Research team analyzing experimental results."""

    researchers = [
    SimpleAgent(
    name="DataScientist",
    engine=AugLLMConfig(
    system_message="You analyze data patterns and statistical significance."
    )
    ),
    SimpleAgent(
    name="DomainExpert",
    engine=AugLLMConfig(
    system_message="You provide field-specific insights and interpret findings."
    )
    ),
    SimpleAgent(
    name="Methodologist",
    engine=AugLLMConfig(
    system_message="You ensure research methodology is sound and suggest improvements."
    )
    ),
    ]

    collaboration = CollaborativeConversation(
    agents=researchers,
    topic="Analyzing Climate Change Impact on Crop Yields",
    shared_goal="Develop actionable insights from our 5-year study data",
    consensus_threshold=0.8,
    max_turns=15
    )

    result = collaboration.run({})


**Sample Output:*

.. code-block:: text

    DataScientist: Our regression analysis shows a -2.3% yield decrease per
    degree Celsius increase, with p<0.001. The effect is most pronounced in
    wheat (-3.1%) and least in sorghum (-0.8%). Interesting regional variations too.

    DomainExpert: These findings align with crop physiology. Wheat is
    temperature-sensitive during grain filling. The sorghum resilience makes
    sense - it's originally from hot climates. What about precipitation interactions?

    DataScientist: Great question! When we include precipitation, the model
    improves significantly (R²=0.76). Low rainfall amplifies temperature
    effects. Areas with >800mm annual rainfall show 40% less temperature
    impact on yields.

    Methodologist: We should verify these interactions aren't just capturing
    irrigation differences. Did we control for irrigation infrastructure?
    Also, 5 years might not capture long-term adaptation effects.

    DomainExpert: Valid concern. Farmers do adapt - switching cultivars,
    adjusting planting dates. Our study areas have minimal irrigation, so
    that's controlled. But yes, adaptation is a limitation we should acknowledge.

    DataScientist: I can separate short-term weather effects from long-term
    trends using panel data methods. Preliminary results suggest 30% of the
    impact is offset by adaptation within 3 years. Still significant net negative effect.

    Methodologist: That's a crucial finding! For actionable insights, we should
    model specific adaptation strategies. Which practices show the most promise
    for yield recovery in our data?

    DomainExpert: From field observations, successful farms shifted planting
    dates earlier and adopted drought-resistant varieties. We could quantify
    these effects and create region-specific recommendations.

    DataScientist: I'll run that analysis. Initial results: 15 days earlier
    planting recovers 1.2% yield, drought varieties add 1.8%. Combined with
    optimal fertilization, we can offset up to 60% of climate impact.

    Key Features Demonstrated
    -------------------------

    1. **Natural Flow*: Agents join the conversation when they have relevant input
    2. **Building Ideas*: Each contribution builds on previous statements
    3. **Shared Goals*: All agents work toward the same objective
    4. **Consensus Building*: Group works toward agreement on solutions
    5. **Emergent Leadership*: Natural conversation flow without fixed order

    Configuration Options
    ---------------------

.. code-block:: python

    # Code example here

    CollaborativeConversation(
    agents=agent_list,                    # List of participating agents
    topic="Collaboration Topic",          # Topic of discussion
    shared_goal="What we want to achieve", # Common objective
    max_turns=20,                         # Maximum total turns
    consensus_threshold=0.75,             # Agreement level needed
    allow_thinking_time=True,             # Agents can "pause to think"
    encourage_building=True,              # Prompt agents to build on ideas
    track_contributions=True,             # Monitor each agent's input
    )

    Best Practices

--------------

    1. **Complementary Skills*: Use agents with different but complementary expertise
    2. **Clear Goals*: Define specific shared objectives for focus
    3. **Encourage Building*: System prompts should encourage "yes, and..." thinking
    4. **Monitor Participation*: Ensure all agents contribute meaningfully
    5. **Convergence*: Guide toward actionable outcomes, not endless discussion

    Common Use Cases
    ----------------

    - **Problem Solving*: Technical challenges, debugging, optimization
    - **Design*: Product features, user experiences, architecture
    - **Research*: Data analysis, hypothesis forming, paper writing
    - **Planning*: Project planning, strategy development, roadmapping
    - **Creative*: Storytelling, content creation, brainstorming

    Advanced Example: Startup Ideation
    ----------------------------------

.. code-block:: python

    # Code example here

    def example_startup_ideation():
    """Collaborative session for new startup ideas."""

    team = [
    SimpleAgent(name="TechFounder", expertise="technology and scalability"),
    SimpleAgent(name="BusinessFounder", expertise="market and revenue models"),
    SimpleAgent(name="DesignFounder", expertise="user experience and branding"),
    SimpleAgent(name="Advisor", expertise="startup strategy and funding"),
    ]

    ideation = CollaborativeConversation(
    agents=team,
    topic="EdTech Startup for Personalized Learning",
    shared_goal="Define MVP features and go-to-market strategy",
    phases=[
    "Problem Definition",
    "Solution Brainstorming",
    "MVP Feature Selection",
    "Go-to-Market Strategy"
    ],
    phase_max_turns=5
    )

    result = ideation.run({})

    # Extract key decisions
    mvp_features = extract_decisions(result, "MVP features")
    strategy = extract_decisions(result, "go-to-market")

    Tracking Collaboration Metrics

------------------------------

.. code-block:: python

    # Code example here

    # After running collaboration
    metrics = collaboration.get_metrics()

    print(f"Total turns: {metrics['total_turns']}")
    print(f"Unique contributors: {metrics['unique_contributors']}")
    print(f"Ideas generated: {metrics['idea_count']}")
    print(f"Consensus reached: {metrics['consensus_score']}")
    print(f"Most active: {metrics['most_active_agent']}")

    # Visualize contribution balance
    collaboration.plot_contribution_chart()

    # Export conversation with annotations
    collaboration.export_annotated_transcript("collaboration_results.md")

    See Also

--------

    - :doc:`conversation_directed - Structured conversations with direction`
    - :doc:`conversation_round_robin - Equal participation in fixed order`
    - :doc:`conversation_debate - Opposing viewpoints and argumentation`
    - :doc:`../../api/index - Full API documentation`
