Directed Conversation Examples



The DirectedConversation agent enables orchestrated multi-agent discussions where a moderator or specific agents can direct questions to others using @mentions.

Classroom Discussion



A teacher-led classroom discussion where the teacher directs questions to specific students.

**Full Example Code:**

.. literalinclude:: ../../../../../packages/haive-agents/src/haive/agents/conversation/directed/example.py

   :language: python
   :pyobject: example_classroom_discussion
   :caption: Classroom Discussion Implementation

**Running the Example:**

.. code-block:: bash

    poetry run python packages/haive-agents/src/haive/agents/conversation/directed/example.py

    **Sample Output:**

.. code-block:: text

    === Classroom Discussion Example
====================================

    Topic: The Water Cycle and Climate Change

    [Setting: Classroom discussion about The Water Cycle and Climate Change]

    Ms. Johnson: Good morning class! Today we're discussing the water cycle
    and its connection to climate change. @Alex, can you start by explaining
    the basic steps of the water cycle?

    Alex: The water cycle has four main steps: evaporation where water turns
    to vapor, condensation forming clouds, precipitation as rain or snow, and
    collection in bodies of water. The sun's energy drives this continuous cycle.

    Ms. Johnson: Excellent explanation, Alex! @Sarah, how do you think climate
    change might affect the evaporation stage of the water cycle?

    Sarah: With rising global temperatures, evaporation rates increase. This
    means more water vapor in the atmosphere, which can lead to more intense
    precipitation events in some areas while causing droughts in others due to
    faster moisture loss from soil.

    Ms. Johnson: Very insightful, Sarah! @Mike, what impacts might these
    changes have on ecosystems?

    Mike: Changed precipitation patterns can disrupt ecosystems significantly.
    Some areas might flood, destroying habitats, while others face drought,
    causing plant die-offs and forcing animal migration. Aquatic ecosystems
    are especially vulnerable to temperature and water level changes.

    Ms. Johnson: Great points about ecosystem impacts! @Emma, can you connect
    this to human activities and what we can do?

    Emma: Human activities like burning fossil fuels accelerate climate change,
    intensifying water cycle disruption. We can help by reducing emissions,
    conserving water, protecting wetlands that regulate water flow, and
    supporting renewable energy to slow global warming's effects on the cycle.

    Team Meeting Example



    A software team sprint meeting with directed updates and cross-functional questions.

    **Full Example Code:**

    .. literalinclude:: ../../../../../packages/haive-agents/src/haive/agents/conversation/directed/example.py

    :language: python
    :pyobject: example_team_meeting
    :caption: Team Meeting Implementation

    **Sample Output:**

.. code-block:: text

    === Team Meeting Example
============================

    Topic: Sprint Progress Update

    Manager: Good morning team! Let's get our sprint update started.
    @Developer, can you share your progress on the API implementation?

    Developer: I've completed the authentication endpoints and user management
    APIs. Currently working on the data export functionality. @Designer, I'll
    need the loading animation designs for the export process by tomorrow.

    Designer: I'll have those loading animations ready by end of day. I've
    finished the dashboard redesign and mobile responsive layouts. @Developer,
    are there any technical constraints I should consider for the new data
    visualization components?

    Developer: Yes, please keep the SVG complexity moderate as we're rendering
    multiple charts simultaneously. Also, avoid animations that require constant
    redraws. Libraries like D3.js work well with our current stack.

    Manager: Thanks for coordinating. @QA, what's the testing status for the
    completed features?

    QA: I've completed testing on the authentication flow - found and logged
    3 edge cases that need fixing. The user management APIs passed all tests.
    @Developer, I noticed the password reset endpoint doesn't handle expired
    tokens properly. Also started mobile testing on the dashboard.

    Developer: Thanks for catching that! I'll fix the token expiration handling
    today. Is it failing gracefully at least, or causing errors?

    QA: It returns a 500 error instead of a proper 401 with an error message.
    I've added details in ticket #234.

    Manager: Good catch. Let's prioritize that fix. @Designer, when can we
    review the mobile layouts together?

    Designer: I have a interactive prototype ready. How about we do a quick
    review after this meeting? The responsive breakpoints are working smoothly
    down to 320px width.

    Panel Discussion Example



    An expert panel with a moderator directing topic flow.

    **Example Code:**

.. code-block:: python

    # Code example here

    from haive.agents.conversation.directed.agent import DirectedConversation
    from haive.agents.simple.agent import SimpleAgent

    def example_expert_panel():
    """Expert panel on AI Ethics."""

    experts = {
    "Moderator": SimpleAgent(
    name="Moderator",
    engine=AugLLMConfig(
    system_message="You moderate an AI ethics panel. Direct questions to specific experts using @mentions."
    )
    ),
    "Ethicist": SimpleAgent(
    name="Ethicist",
    engine=AugLLMConfig(
    system_message="You are an AI ethics professor. Discuss ethical implications."
    )
    ),
    "Engineer": SimpleAgent(
    name="Engineer",
    engine=AugLLMConfig(
    system_message="You are an AI engineer. Discuss technical aspects and limitations."
    )
    ),
    "PolicyExpert": SimpleAgent(
    name="PolicyExpert",
    engine=AugLLMConfig(
    system_message="You are a policy expert. Discuss regulation and governance."
    )
    ),
    }

    panel = DirectedConversation(
    participant_agents=experts,
    topic="Responsible AI Development",
    max_rounds=5,
    allow_self_direction=False
    )

    result = panel.run({})


**Sample Output:**

.. code-block:: text

    Moderator: Welcome to our panel on Responsible AI Development. @Ethicist,
    let's start with you. What are the key ethical challenges in current AI
    development?

    Ethicist: The primary challenges include bias in training data leading to
    discriminatory outcomes, lack of transparency in decision-making processes,
    privacy concerns with data collection, and the potential for AI to be used
    in harmful applications like surveillance or autonomous weapons.

    Moderator: Important points. @Engineer, from a technical perspective, how
    can we address the transparency issue mentioned?

    Engineer: We're developing explainable AI techniques like LIME and SHAP
    for model interpretation. However, there's a trade-off between model
    complexity and explainability. We're also working on documentation
    standards and model cards to communicate limitations clearly.

    Moderator: @PolicyExpert, what regulatory frameworks are emerging to
    ensure responsible AI development?

    PolicyExpert: The EU's AI Act is leading the way with risk-based
    categorization. We're seeing requirements for impact assessments,
    transparency obligations, and human oversight. The challenge is
    balancing innovation with protection while ensuring global coordination.

    Key Features Demonstrated



    1. **@Mention System**: Agents can direct messages to specific participants
    2. **Turn Management**: The conversation flows naturally with directed responses
    3. **Role-Based Behavior**: Each agent maintains their role and expertise
    4. **Fallback Mechanisms**: Can fall back to round-robin if no mentions detected
    5. **Silence Handling**: Configurable behavior when agents don't respond

    Configuration Options



.. code-block:: python

    # Code example here

    DirectedConversation(
    participant_agents=agents,          # Dict of agent name to agent
    topic="Discussion Topic",           # Conversation topic
    max_rounds=5,                       # Maximum conversation rounds
    fallback_to_round_robin=True,       # Use round-robin if no mentions
    max_silence_turns=2,                # Turns before forcing participation
    allow_self_direction=False,         # Can agents mention themselves
    mention_prefix="@",                 # Prefix for mentions
    require_mention_response=True       # Must mentioned agent respond
    )

    Best Practices


-------------

    1. **Clear System Messages**: Give agents clear instructions about using mentions
    2. **Topic Focus**: Provide a specific topic to keep conversation on track
    3. **Role Definition**: Define clear roles and expertise for each agent
    4. **Mention Patterns**: Teach agents when and how to use mentions effectively
    5. **Conversation Length**: Set appropriate max_rounds to avoid repetition

    Common Use Cases



    - **Educational**: Classroom discussions, tutoring sessions, Q&A
    - **Business**: Team meetings, project updates, brainstorming
    - **Panels**: Expert panels, interviews, moderated debates
    - **Support**: Multi-tier customer support, technical assistance
    - **Creative**: Collaborative storytelling, script writing

    See Also



    - :doc:`conversation_round_robin - Simple turn-based conversations`

`
    - :doc`:`conversation_debate - Structured debate format`

`
    - :doc`:`conversation_collaborative - Collaborative problem solving`

`
    - :doc`:`../../api/index - Full API documentation`

`
`
