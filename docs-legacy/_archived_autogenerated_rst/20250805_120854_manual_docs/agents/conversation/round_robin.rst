Round Robin Conversation Examples



Round Robin conversations ensure equal participation by having agents speak in a fixed order. This is ideal for structured discussions, status updates, and brainstorming sessions.

Daily Standup Example



A development team's daily standup meeting where each member shares updates in order.

**Full Example Code:**

.. literalinclude:: ../../../../../packages/haive-agents/src/haive/agents/conversation/round_robin/example.py

   :language: python
   :pyobject: example_daily_standup
   :caption: Daily Standup Implementation

**Running the Example:**

.. code-block:: bash

    poetry run python packages/haive-agents/src/haive/agents/conversation/round_robin/example.py

    **Sample Output:**

.. code-block:: text

    === Daily Standup Meeting
=============================

    Topic: Sprint 23 Daily Standup

    Round 1 - Yesterday's Progress:

    Frontend Dev: Yesterday I completed the user profile component with all
    the responsive breakpoints. Also fixed the navigation menu bug on mobile
    devices that was reported in ticket #156.

    Backend Dev: I finished implementing the new caching layer for the API
    endpoints, which improved response times by 40%. Also reviewed and merged
    3 pull requests from the team.

    QA Engineer: Completed regression testing for the payment module. Found
    2 critical bugs which I've documented with reproduction steps. Also updated
    our test automation suite with new test cases.

    DevOps: Deployed the latest release to staging environment. Set up
    monitoring alerts for the new microservices. Also automated the database
    backup process which now runs every 6 hours.

    Round 2 - Today's Plan:

    Frontend Dev: Today I'll start working on the dashboard analytics
    component. Need to coordinate with backend on the data format for the
    charts. Should have initial implementation by EOD.

    Backend Dev: Planning to implement the new notification service today.
    Will also work on optimizing the database queries that QA identified as
    slow. Targeting completion by tomorrow.

    QA Engineer: I'll be testing the user profile features that Frontend
    completed. Also preparing test scenarios for the upcoming notification
    service. Will start performance testing in the afternoon.

    DevOps: Today I'm implementing the auto-scaling policies for our
    Kubernetes cluster. Also scheduled maintenance window for database
    upgrades this weekend. Will send out notification to the team.

    Round 3 - Blockers:

    Frontend Dev: No major blockers. Just waiting for the final designs
    for the analytics component from the design team. Using placeholder
    data for now.

    Backend Dev: Need access to the new analytics database. Also, the
    third-party API documentation is outdated, might need to contact
    their support.

    QA Engineer: Test environment is running slow, might be related to
    the recent deployments. Could DevOps take a look at the resource
    utilization?

    DevOps: I'll check the test environment right after this meeting.
    No blockers on my end, but I'll need everyone to avoid deployments
    during the maintenance window.

    Brainstorming Session Example



    A creative brainstorming session where team members build on ideas in rounds.

    **Full Example Code:**

    .. literalinclude:: ../../../../../packages/haive-agents/src/haive/agents/conversation/round_robin/example.py

    :language: python
    :pyobject: example_brainstorming
    :caption: Brainstorming Session Implementation

    **Sample Output:**

.. code-block:: text

    === Brainstorming Session
=============================

    Topic: New Features for Mobile App

    Round 1 - Initial Ideas:

    Product Manager: I think we should add a voice command feature. Users
    are increasingly expecting hands-free interaction, especially while
    driving or cooking. This could set us apart from competitors.

    UX Designer: Building on voice interaction, we could implement gesture
    controls too. Imagine swiping in the air to navigate, or using hand
    signals for common actions. Very futuristic and accessible.

    Developer: From a technical perspective, we could add an offline mode
    with smart sync. Users could work without internet and changes would
    sync seamlessly when connected. Great for travelers.

    Marketing: I love these ideas! What about social features? Users could
    share achievements, collaborate on projects, or even have mini-competitions.
    Social proof drives engagement.

    Round 2 - Expanding Ideas:

    Product Manager: The social features could integrate with the voice
    commands - imagine voice messages or collaborative voice notes. We
    could also add AI transcription for accessibility.

    UX Designer: For the offline mode, we need beautiful empty states and
    clear sync status indicators. Maybe a subtle animation showing what's
    syncing. The gesture controls could have a tutorial game to teach users.

    Developer: The social features could use peer-to-peer sharing for
    offline collaboration. For voice commands, we could integrate with
    existing assistants like Siri shortcuts or Google Assistant.

    Marketing: These features create great marketing stories! "Work anywhere"
    for offline mode, "Control without touching" for gestures, "Never work
    alone" for social. Each feature is a campaign.

    Round 3 - Prioritization:

    Product Manager: Based on user feedback, I'd prioritize offline mode
    first. It's our most requested feature. Voice commands second, as
    they're becoming table stakes in our industry.

    UX Designer: Agreed on offline mode. It needs the most design work
    for edge cases. Gesture controls might be too early for our user
    base - maybe next year?

    Developer: Offline mode is definitely 2-3 sprints of work. Voice
    commands could be MVP'd quickly using platform APIs. Social features
    need backend infrastructure we don't have yet.

    Marketing: Let's launch offline mode with the "Work Anywhere" campaign.
    We can tease voice commands as "coming soon" to build anticipation.
    Social features for our 2.0 release?

    Book Club Discussion Example



    A book club where members share thoughts chapter by chapter.

    **Example Code:**

.. code-block:: python

    # Code example here

    from haive.agents.conversation.round_robin import RoundRobinConversation
    from haive.agents.simple import SimpleAgent

    def example_book_club():
    """Book club discussion with literary analysis."""

    members = [
    SimpleAgent(
    name="Sarah",
    engine=AugLLMConfig(
    system_message="Book club member who focuses on character development and relationships."
    )
    ),
    SimpleAgent(
    name="James",
    engine=AugLLMConfig(
    system_message="Book club member who analyzes themes and symbolism."
    )
    ),
    SimpleAgent(
    name="Maria",
    engine=AugLLMConfig(
    system_message="Book club member who considers historical context and author background."
    )
    ),
    SimpleAgent(
    name="David",
    engine=AugLLMConfig(
    system_message="Book club member who focuses on writing style and literary techniques."
    )
    ),
    ]

    discussion = RoundRobinConversation(
    agents=members,
    topic="Discussing '1984' by George Orwell - Chapters 1-5",
    rounds=3,
    round_names=[
    "Initial Impressions",
    "Deeper Analysis",
    "Predictions and Connections"
    ]
    )

    result = discussion.run({})


**Sample Output:**

.. code-block:: text

    Round 1 - Initial Impressions:

    Sarah: The relationship between Winston and Julia is fascinating but
    feels doomed from the start. Winston's internal rebellion contrasts
    sharply with his outward conformity, showing the deep psychological
    impact of totalitarian control.

    James: The theme of reality control through language manipulation is
    chilling. Newspeak isn't just censorship - it's making certain thoughts
    literally unthinkable. The symbol of Big Brother represents the death
    of individual identity.

    Maria: Orwell wrote this in 1948, reversing the digits to 1984. His
    experience in the Spanish Civil War and observing Stalin's regime clearly
    influenced the portrayal of totalitarianism. The parallels to real
    historical events are unmistakable.

    David: Orwell's prose is deliberately flat and gray, mirroring the
    bleakness of Oceania. The use of paradoxes like "War is Peace" creates
    cognitive dissonance that puts readers in Winston's confused state of mind.

    Key Features Demonstrated



    1. **Fixed Order**: Agents always speak in the same sequence
    2. **Equal Participation**: Every agent speaks exactly once per round
    3. **Round Structure**: Conversations organized into themed rounds
    4. **No Interruptions**: Clean, organized flow of ideas
    5. **Building Ideas**: Later speakers can reference earlier contributions

    Configuration Options



.. code-block:: python

    # Code example here

    RoundRobinConversation(
    agents=agent_list,              # List of agents in speaking order
    topic="Discussion Topic",       # Overall conversation topic
    rounds=3,                       # Number of complete rounds
    round_names=["R1", "R2"],      # Optional names for each round
    allow_passing=False,           # Can agents skip their turn
    summary_after_round=True,      # Summarize after each round
    time_limit_per_turn=None,      # Optional time limit
    )

    Best Practices


-------------

    1. **Clear Roles**: Give each agent a distinct perspective or expertise
    2. **Round Themes**: Use round_names to structure the conversation progression
    3. **Appropriate Rounds**: Usually 2-4 rounds work best to avoid repetition
    4. **Speaking Order**: Consider putting synthesizers/summarizers last
    5. **Topic Clarity**: Provide specific topics or questions for focus

    Common Use Cases



    - **Status Meetings**: Daily standups, weekly syncs, project updates
    - **Brainstorming**: Idea generation, feature planning, problem solving
    - **Reviews**: Code reviews, design reviews, retrospectives
    - **Education**: Student presentations, group discussions, peer review
    - **Creative**: Story building, collaborative writing, improv games

    Advanced Example: Retrospective



.. code-block:: python

    # Code example here

    def example_retrospective():
    """Agile retrospective with structured rounds."""

    team = create_team_agents()  # Create your team agents

    retro = RoundRobinConversation(
    agents=team,
    topic="Sprint 23 Retrospective",
    rounds=4,
    round_names=[
    "What went well?",
    "What could be improved?",
    "What puzzled us?",
    "Action items"
    ],
    summary_after_round=True
    )

    result = retro.run({})

    # Extract action items from final round
    action_items = extract_action_items(result["messages"])
    print(f"\nAction Items: {action_items}")

    See Also


-------

    - :doc:`conversation_directed - Orchestrated conversations with mentions`

`
    - :doc`:`conversation_collaborative - Free-form collaborative discussions`

`
    - :doc`:`conversation_debate - Structured debates with opposing sides`

`
    - :doc`:`../../api/index - Full API documentation`

`
`
