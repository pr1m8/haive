Conversation Agents
===================

Multi-agent conversation systems enable rich dialogues between AI agents for various purposes including collaboration, debate, education, and problem-solving.

Overview
--------

The Haive conversation system provides several conversation patterns, each optimized for different interaction styles:

   .. card::

      :link: directed
      :link-type: doc

      Orchestrated discussions with @mentions and targeted responses.
      Perfect for panels, meetings, and classroom settings.

   .. card::

      :link: round_robin
      :link-type: doc

      Equal participation in fixed order. Ideal for standups,
      brainstorming, and status updates.

   .. card::

      :link: collaborative
      :link-type: doc

      Free-flowing cooperation toward shared goals. Great for
      problem-solving and creative work.

   .. card::

      :link: debate
      :link-type: doc

      Structured argumentation with opposing positions. Useful for
      decision-making and exploring ideas.

   .. card::

      :link: social_media
      :link-type: doc

      Simulates online discussions with posts, comments, and
      viral dynamics.

   .. card::

      :link: custom_patterns
      :link-type: doc

      Build your own conversation patterns for specialized needs.

Quick Start
-----------

**Basic Conversation Setup**

.. code-block:: python

    from haive.agents.conversation.directed import DirectedConversation
    from haive.agents.simple import SimpleAgent

    # Create agents
    moderator = SimpleAgent(name="Moderator")
    experts = [
    SimpleAgent(name="Expert1", expertise="AI"),
    SimpleAgent(name="Expert2", expertise="Ethics"),
    SimpleAgent(name="Expert3", expertise="Policy")
    ]

    # Create conversation
    panel = DirectedConversation(
    moderator=moderator,
    participants=experts,
    topic="AI Governance"
    )

    # Run conversation
    result = await panel.run(max_rounds=5)

    Choosing a Conversation Type
    ----------------------------

    .. list-table:: Conversation Type Selection Guide

    :header-rows: 1
    :widths: 25 25 50

    * - Type*

     - Best For
     - Key Features

    * - Directed*

     - Panels, meetings, Q&A
     - @mentions, orchestration, role-based

    * - Round Robin*

     - Standups, reviews, brainstorming
     - Equal turns, predictable flow

    * - Collaborative  *

     - Problem solving, design, research
     - Emergent discussion, consensus building

    * - Debate*

     - Decision making, exploration
     - Opposing views, scoring, evidence

    * - Social Media*

     - Simulations, viral content
     - Async posts, reactions, metrics

    Common Patterns
    ---------------

    **1. Expert Panel Discussion**

.. code-block:: python

    panel = DirectedConversation.create_panel(
    moderator_name="Host",
    expert_names=["AI_Expert", "Ethicist", "Engineer"],
    topic="Responsible AI Development",
    rounds=3
    )

    **2. Team Problem Solving**

.. code-block:: python

    team_session = CollaborativeConversation(
    agents=team_members,
    shared_goal="Optimize system performance",
    phases=["Identify Issues", "Propose Solutions", "Plan Implementation"],
    consensus_required=True
    )

    **3. Decision Analysis**

.. code-block:: python

    decision_debate = DebateConversation(
    topic="Should we migrate to microservices?",
    positions={"Pro": pro_agent, "Con": con_agent},
    judge=neutral_evaluator,
    evidence_required=True
    )

    Architecture
    ------------

    .. mermaid::

    graph TD

       A[Conversation Manager] --> B[Turn Management]
       A --> C[Message History]
       A --> D[Agent Coordination]

       B --> E[Speaker Selection]
       B --> F[Time Control]

       C --> G[Context Window]
       C --> H[Summarization]

       D --> I[@Mention Detection]
       D --> J[Role Assignment]
       D --> K[Consensus Tracking]

    Key Components
    --------------

    1. **Base Conversation Class**


    - Message management
    - Turn orchestration
    - History tracking
    - Context building

    2. **Agent Integration**


    - Any Haive agent can participate
    - Agents maintain individual context
    - System messages guide behavior

    3. **Conversation Flow**


    - Configurable turn patterns
    - Dynamic speaker selection
    - Termination conditions

    4. **Output Formats**


    - Full transcript
    - Summary generation
    - Metrics and analytics
    - Structured outcomes

    Best Practices
    --------------

    **1. Agent Preparation**

.. code-block:: python

    # Give agents clear roles
    agent = SimpleAgent(
    name="DataAnalyst",
    system_message="""You are a data analyst in a team meeting.
    Focus on metrics and evidence. Ask clarifying questions.
    Build on others' ideas with data-driven insights."""
    )

    **2. Conversation Configuration**

.. code-block:: python

    # Set appropriate limits
    conversation = ConversationType(
    max_turns=20,        # Prevent infinite loops
    max_time=10_minutes, # Time bounds
    min_participation=2, # Ensure all speak
    summary_interval=5   # Periodic summaries
    )

    **3. Error Handling**

.. code-block:: python

    try:
    result = await conversation.run()
    except TurnLimitExceeded:
    result = conversation.get_partial_result()
    except AgentTimeout:
    result = conversation.continue_without_agent(failed_agent)

    Advanced Features
    -----------------

    **Dynamic Agent Addition**

.. code-block:: python

    # Add expert when specific topic arises
    conversation.add_agent_when(
    condition=lambda msg: "quantum" in msg.content.lower(),
    agent=quantum_expert,
    introduction="I'm here to explain the quantum aspects..."
    )

    **Conversation Branching**

.. code-block:: python

    # Split into subgroups for parallel discussion
    main_conv.branch_into_subgroups(
    groups=[["Agent1", "Agent2"], ["Agent3", "Agent4"]],
    topics=["Technical Details", "Business Impact"],
    merge_after_turns=10
    )

    **Memory and Context**

.. code-block:: python

    # Use persistent memory across conversations
    memory = ConversationMemory(redis_url="...")

    conversation = ConversationType(
    agents=agents,
    memory=memory,
    context_window=50,  # Recent messages
    use_summary=True    # Compress old context
    )

    Examples by Use Case
    --------------------

    .. toctree::

    :maxdepth: 1
    :caption: Conversation Types

    directed
    round_robin
    collaborative
    debate
    social_media
    custom_patterns

    .. toctree::

    :maxdepth: 1
    :caption: Use Cases

    examples/education
    examples/business
    examples/research
    examples/creative
    examples/support

    Performance Considerations
    --------------------------

    - **Token Usage**: Conversations can consume many tokens quickly
    - **Context Management**: Use sliding windows and summarization
    - **Parallel Processing**: Some patterns allow concurrent agent thinking
    - **Caching**: Cache agent responses for similar prompts
    - **Monitoring**: Track participation, quality, and outcomes

    See Also
    --------

    - :doc:`/guides/building_agents` - Create custom agents
    - :doc:`/api/haive-agents` - Full agents API reference
    - :doc:`/guides/multi_agent_systems` - Advanced multi-agent patterns
    - :doc:`/examples/index` - More code examples
