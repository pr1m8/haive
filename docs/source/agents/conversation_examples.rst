Conversation Agent Examples
===========================

This page demonstrates the various conversation agent types with runnable examples and sample outputs.

Directed Conversation
---------------------

A directed conversation uses a moderator agent to orchestrate the discussion between participants.

**Example: AI Ethics Panel Discussion**

.. literalinclude:: ../../../../packages/haive-agents/src/haive/agents/conversation/directed/example.py

   :language: python
   :caption: directed_conversation_example.py
   :lines: 1-50

**Sample Output:**

.. code-block:: text

    === AI Ethics Panel Discussion ===

    Moderator: Welcome to our panel on AI Ethics. Let's begin with Expert1,
    can you share your thoughts on the current state of AI safety?

    Expert1 (AI Safety): Thank you. I believe we're at a critical juncture
    where AI capabilities are advancing faster than our safety measures...

    Moderator: Interesting point. Expert2, from an ethics perspective,
    what are your main concerns?

    Expert2 (AI Ethics): Building on what Expert1 said, the ethical
    implications go beyond just safety. We need to consider fairness,
    transparency, and accountability...

    [Discussion continues with directed turns...]

    Round Robin Conversation
    ------------------------

    Agents take turns speaking in a fixed order, ensuring equal participation.

    **Example: Team Standup Meeting**

.. code-block:: python

    from haive.agents.conversation.round_robin import RoundRobinConversation
    from haive.agents.simple import SimpleAgent

    # Create team members
    team = [
    SimpleAgent(name="Alice", role="Frontend Dev"),
    SimpleAgent(name="Bob", role="Backend Dev"),
    SimpleAgent(name="Carol", role="QA Engineer")
    ]

    # Run standup
    async def run_standup():
    standup = RoundRobinConversation(
    agents=team,
    topic="Daily Standup - Sprint 23"
    )

    await standup.run(rounds=2)

    # Run with asyncio
    import asyncio
    asyncio.run(run_standup())

    **Sample Output:**

.. code-block:: text

    === Daily Standup - Sprint 23 ===

    Round 1:
    Alice (Frontend Dev): Yesterday I completed the user dashboard
    component. Today I'll work on integrating it with the API.

    Bob (Backend Dev): I finished the authentication endpoints.
    Currently debugging the rate limiting middleware.

    Carol (QA Engineer): Found 3 bugs in the payment flow which
    I've documented. Will test the new dashboard today.

    Round 2:
    Alice (Frontend Dev): No blockers on my end, but I'll need
    the API documentation updated for the new endpoints.

    Bob (Backend Dev): I can get that documentation done by noon.
    The rate limiting issue was a Redis config problem - now fixed.

    Carol (QA Engineer): Great! I'll also need staging deployed
    with the latest changes for comprehensive testing.

    Collaborative Conversation
    --------------------------

    Agents work together to solve problems or brainstorm ideas.

    **Example: Product Feature Brainstorming**

    .. literalinclude:: ../../../../packages/haive-agents/src/haive/agents/conversation/collaborative/example.py

    :language: python
    :caption: collaborative_brainstorm.py
    :pyobject: run_brainstorming_session

    **Sample Output:**

.. code-block:: text

    === Collaborative Brainstorming: New Mobile App Features ===

    Designer: What if we add a gesture-based navigation system?
    Users could swipe between main sections more intuitively.

    Developer: I like that! We could use the native gesture APIs.
    Building on that, we could add haptic feedback for actions.

    Product Manager: Great ideas! This aligns with our goal of
    improving user engagement. What about accessibility though?

    Designer: Good point! We should ensure all gestures have
    alternative tap-based controls for accessibility.

    Developer: Agreed. I can implement a settings toggle to switch
    between gesture and traditional navigation modes.

    [Collaboration continues with ideas building on each other...]

    Debate Conversation
    -------------------

    Structured debates with opposing positions and scoring.

    **Example: Technology Debate**

.. code-block:: python

    from haive.agents.conversation.debate import DebateAgent, DebateConversation

    # Create debate agents
    pro_agent = DebateAgent(
    name="TechOptimist",
    position="AI will solve climate change",
    debate_style="evidence-based"
    )

    con_agent = DebateAgent(
    name="TechRealist",
    position="AI alone cannot solve climate change",
    debate_style="analytical"
    )

    judge = SimpleAgent(name="Judge", expertise="Critical thinking")

    # Run debate
    async def run_debate():
    debate = DebateConversation(
    agents=[pro_agent, con_agent],
    judge=judge,
    rounds=3,
    time_per_turn=60
    )

    result = await debate.run()
    print(f"Winner: {result.winner}")
    print(f"Score: {result.scores}")

    # Run with asyncio
    import asyncio
    asyncio.run(run_debate())

    **Sample Output:**

.. code-block:: text

    === Debate: Can AI Solve Climate Change? ===

    Round 1 - Opening Statements:

    TechOptimist: AI is already revolutionizing climate science through
    advanced modeling, optimization of renewable energy, and discovering
    new materials for carbon capture. Examples include DeepMind's work
    on protein folding leading to better carbon-eating enzymes...

    TechRealist: While AI contributes valuable tools, climate change is
    fundamentally a political, economic, and social challenge. No algorithm
    can force policy changes or alter consumption patterns. The IPCC reports
    show we need immediate behavioral and systemic changes...

    Round 2 - Rebuttals:

    TechOptimist: I acknowledge the social aspects, but AI can influence
    behavior through smart city optimization, personalized carbon tracking,
    and making sustainable choices more convenient and cost-effective...

    TechRealist: Those are incremental improvements. The core issue is that
    AI development itself has a massive carbon footprint. Training large
    models emits as much CO2 as several cars over their lifetime...

    Round 3 - Closing Arguments:
    [Arguments continue...]

    Judge's Decision:
    Winner: TechRealist
    Scores:
    - Logic: TechRealist 8/10, TechOptimist 7/10
    - Evidence: TechRealist 9/10, TechOptimist 8/10
    - Persuasiveness: TechRealist 7/10, TechOptimist 8/10

    Judge's Comments: While both debaters made strong points, TechRealist's
    argument about the systemic nature of climate change and the limitations
    of technological solutions was more comprehensive and grounded in current
    climate science consensus.

    Social Media Conversation
    -------------------------

    Simulates social media dynamics with posts, comments, and engagement.

    **Example: Viral Tech News Discussion**

    .. literalinclude:: ../../../../packages/haive-agents/src/haive/agents/conversation/social_media/example.py

    :language: python
    :caption: social_media_simulation.py
    :lines: 1-40

    **Sample Output:**

.. code-block:: text

    === Social Media Feed: Tech News ===

    @TechReporter [Verified]
    BREAKING: Major tech company announces revolutionary quantum computer!
    🚀 Claims 1000x speedup over classical computers for certain tasks.
    ❤️ 1,234  💬 89  🔄 456

    ↳ @QuantumExpert: This is huge if true! But we need to see
    peer-reviewed benchmarks. Quantum supremacy ≠ quantum advantage.
    ❤️ 234  💬 12

    ↳ @TechReporter: Fair point! They're publishing results next month
    in Nature. Early reviews look promising though 👀
    ❤️ 45  💬 3

    ↳ @SkepticalDev: Every year someone claims a quantum breakthrough.
    Wake me up when it can run Doom 😂
    ❤️ 567  💬 23

    ↳ @QuantumEnthusiast: You joke but quantum computers aren't meant
    for gaming! They excel at optimization, cryptography, and simulation.
    ❤️ 123  💬 8

    ↳ @InvestorGuru: Stock price already up 15%! 📈 #ToTheMoon
    ❤️ 89  💬 34

    [Thread continues with more reactions, memes, and discussions...]

    Engagement Analytics:
    - Total Reach: 45,678 users
    - Engagement Rate: 12.3%
    - Sentiment: 68% positive, 23% neutral, 9% negative
    - Top Keywords: quantum, breakthrough, skeptical, investment

    Running the Examples
    --------------------

    All examples can be found in their respective module directories:

.. code-block:: bash

    # Directed conversation
    poetry run python packages/haive-agents/src/haive/agents/conversation/directed/example.py

    # Round robin
    poetry run python packages/haive-agents/src/haive/agents/conversation/round_robin/example.py

    # Collaborative
    poetry run python packages/haive-agents/src/haive/agents/conversation/collaborative/example.py

    # Debate
    poetry run python packages/haive-agents/src/haive/agents/conversation/debate/example.py

    # Social media
    poetry run python packages/haive-agents/src/haive/agents/conversation/social_media/example.py

    Creating Custom Conversations
    -----------------------------

    To create your own conversation agent:

    1. **Inherit from BaseConversation**

.. code-block:: python

    from haive.agents.conversation.base import BaseConversation

    class CustomConversation(BaseConversation):
    def __init__(self, agents, custom_param):
    super().__init__(agents)
    self.custom_param = custom_param

    async def select_next_speaker(self):
    # Your logic for choosing who speaks next
    pass

    async def should_end_conversation(self):
    # Your logic for when to end
    pass

    2. **Implement Turn Management**

.. code-block:: python

    async def run_turn(self, speaker):
    # Get speaker's message
    message = await speaker.generate_message(
    context=self.get_context(),
    conversation_history=self.history
    )

    # Process and store message
    self.history.append(message)

    # Apply any conversation rules
    self.apply_rules(message)

    return message

    3. **Add Specialized Features**

.. code-block:: python

    def add_scoring(self, message):
    # Score messages for quality, relevance, etc.
    score = self.score_message(message)
    self.scores[message.speaker] = score

    def track_topics(self, message):
    # Extract and track discussion topics
    topics = self.extract_topics(message)
    self.topic_history.extend(topics)

    Best Practices
    --------------

    1. **Memory Management**: For long conversations, implement sliding window or summarization
    2. **Turn Limits**: Always set maximum turns to prevent infinite loops
    3. **Error Handling**: Gracefully handle agent failures or timeouts
    4. **Logging**: Use structured logging for debugging conversations
    5. **Testing**: Test with mock agents before using LLM-based agents

    .. seealso::

    - :doc:`/guides/building_agents` - General agent development guide
    - :doc:`/api/haive-agents` - Full agents API reference
    - :doc:`/agents/showcase` - More agent examples and demos
