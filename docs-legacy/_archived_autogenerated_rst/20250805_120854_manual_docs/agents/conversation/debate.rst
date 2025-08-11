:orphan:

Debate Conversation Examples



The Debate conversation type enables structured argumentation between agents holding opposing positions, with optional judges evaluating arguments based on logic, evidence, and persuasiveness.

Formal Debate Example



A formal debate on AI regulation with opening statements, rebuttals, and closing arguments.

**Full Example Code:**

.. literalinclude:: ../../../../../packages/haive-agents/src/haive/agents/conversation/debate/example.py

   :language: python
   :pyobject: example_formal_debate
   :caption: Formal Debate Implementation

**Running the Example:**

.. code-block:: bash

    poetry run python packages/haive-agents/src/haive/agents/conversation/debate/example.py

    **Sample Output:**

.. code-block:: text

    === Formal Debate: Should AI Development Be Heavily Regulated?
==================================================================

    Moderator: Welcome to today's debate. The motion is: "AI development
    should be heavily regulated by government oversight." Speaking for the
    motion is RegulationAdvocate, against is InnovationDefender.

    --- Opening Statements
--------------------------

    RegulationAdvocate: Thank you. AI represents unprecedented risks to
    society - from job displacement to existential threats. Without regulation,
    we've seen biased algorithms deny loans, surveillance systems oppress
    minorities, and autonomous weapons development. The EU's AI Act shows
    regulation is both possible and necessary. We regulate nuclear technology,
    genetic engineering, and pharmaceuticals - AI deserves the same scrutiny
    to protect humanity while enabling beneficial development.

    InnovationDefender: Regulation stifles innovation when we need it most.
    AI is solving climate change, discovering new medicines, and democratizing
    education. Heavy regulation would entrench big tech monopolies who can
    afford compliance while killing startups. The internet flourished without
    early regulation. Current laws already cover AI harms - we don't need
    new bureaucracy. Innovation happens globally; over-regulation just pushes
    development to countries with fewer safeguards.

    --- Rebuttal Round
----------------------

    RegulationAdvocate: My opponent conflates any regulation with "heavy"
    regulation. Smart regulation enables innovation by creating trust and
    standards. The internet's "wild west" period led to misinformation
    epidemics and privacy violations we're still fixing. Waiting for harm
    before regulating is like allowing untested drugs - the damage is
    irreversible. Risk-based regulation lets beneficial AI flourish while
    preventing harmful applications.

    InnovationDefender: Current "smart regulation" proposals are anything
    but. The EU's AI Act has 100+ pages of requirements that even lawyers
    can't interpret consistently. Small teams can't afford compliance officers
    and legal reviews for every model update. My opponent's pharmaceutical
    analogy fails - drugs directly enter human bodies, while AI is a tool.
    We should focus on outcome-based accountability, not prescriptive rules
    that become obsolete before implementation.

    --- Cross-Examination
-------------------------

    RegulationAdvocate: You mention outcome-based accountability. How do
    we ensure accountability without any oversight framework? Who determines
    if an AI system caused harm after the fact?

    InnovationDefender: Existing legal frameworks - product liability,
    negligence, consumer protection - already provide accountability. Courts
    and expert witnesses can assess harm. Preemptive regulation assumes
    all AI is dangerous. Do you really want innovation committees approving
    every ChatGPT update?

    RegulationAdvocate: You're creating a false dichotomy. Risk-based
    regulation only scrutinizes high-risk applications like medical diagnosis
    or criminal justice. Can you name one industry where waiting for disasters
    before regulating worked well?

    InnovationDefender: The software industry itself. We don't pre-approve
    every app, yet harmful ones get removed and developers face consequences.
    But let me ask - who decides what's "high-risk"? Today's chatbot is
    tomorrow's therapy assistant. Your regulatory framework can't keep pace
    with AI's evolution.

    --- Closing Arguments
-------------------------

    RegulationAdvocate: This debate isn't about stopping innovation - it's
    about responsible development. My opponent admits we need accountability
    but offers only reactive measures. By then, biased hiring algorithms have
    destroyed careers, and autonomous systems have made irreversible decisions.
    Regulation provides certainty for developers and protection for society.
    We can't afford to treat AI like social media - learning from disasters
    after they happen. Vote for thoughtful oversight, not reckless development.

    InnovationDefender: Regulation sounds protective until it becomes
    protectionist. Every requirement my opponent proposes adds months of
    delays and millions in costs. While we debate paperwork, China advances
    AI without such constraints. Current proposals don't make AI safer
----------------------------------------------------------------------
    they make it more expensive and concentrated in big tech. True safety
    comes from open development, security research, and rapid iteration.
    Vote for innovation with accountability, not bureaucracy masquerading
    as protection.

    --- Judge's Decision
------------------------

    Judge: After careful consideration, I award this debate to InnovationDefender.

    Scores:
    - Logic: RegulationAdvocate 7/10, InnovationDefender 8/10
    - Evidence: RegulationAdvocate 8/10, InnovationDefender 7/10
    - Persuasiveness: RegulationAdvocate 7/10, InnovationDefender 9/10
    - Rebuttal: RegulationAdvocate 6/10, InnovationDefender 8/10

    While RegulationAdvocate made strong points about preventing harm and
    cited real examples, InnovationDefender more effectively argued that
    existing frameworks could handle AI accountability without stifling
    innovation. The key winning arguments were the practical challenges
    of implementing regulation and the global competition aspect.

    Panel Debate Example



    A multi-agent panel debate on climate solutions.

    **Full Example Code:**

    .. literalinclude:: ../../../../../packages/haive-agents/src/haive/agents/conversation/debate/example.py

    :language: python
    :pyobject: example_panel_debate
    :caption: Panel Debate Implementation

    **Sample Output:**

.. code-block:: text

    === Panel Debate: Best Approach to Combat Climate Change
============================================================

    Moderator: Our panel will debate different approaches to fighting climate
    change. Each panelist will advocate for their solution.

    TechOptimist: Technology and innovation are our best hope. Renewable
    energy is now cheaper than fossil fuels. Carbon capture, nuclear fusion,
    and geoengineering can reverse damage. We need massive R&D investment,
    not lifestyle changes. Human ingenuity solved past crises - it will
    solve this one.

    PolicyExpert: Technology without policy is insufficient. We need carbon
    pricing, emission standards, and international agreements. Markets fail
    without proper incentives. The Montreal Protocol shows policy works.
    Technology adoption requires regulatory push and economic restructuring.

    Behavioralist: Both miss the root cause - overconsumption. We need
    cultural shift toward sustainability. Individual actions multiply
---------------------------------------------------------------------
    diet changes, transport choices, consumer habits. Bottom-up social
    movements drive policy and technology deployment. Change starts with us.

    TechOptimist: Asking billions to change behavior is unrealistic and
    slow. One breakthrough in fusion power eliminates emissions without
    anyone changing habits. Direct air capture could remove CO2 while
    people live normally. Why choose suffering when innovation offers solutions?

    PolicyExpert: @TechOptimist, your fusion timeline is decades away. We
    have 10 years to halve emissions. @Behavioralist, individual action
    is important but insufficient without systemic change. Policy creates
    the framework for both technology deployment and behavior change at scale.

    Behavioralist: @PolicyExpert, policies fail without public support.
    @TechOptimist, technology won't deploy itself - people must choose it.
    Social movements created political will for past environmental laws.
    We need all three approaches, but behavior change drives the others.

    Academic Debate Format



    A structured academic debate with research citations.

    **Example Code:**

.. code-block:: python

    # Code example here

    def example_academic_debate():
    """Academic debate with evidence and citations."""

    debaters = {
    "Thesis": AcademicDebater(
    name="ThesisDefender",
    position="Universal Basic Income is necessary for future economy",
    research_areas=["economics", "automation", "social policy"]
    ),
    "Antithesis": AcademicDebater(
    name="ThesisChallenger",
    position="UBI would cause economic collapse and social decay",
    research_areas=["behavioral economics", "labor markets", "history"]
    )
    }

    debate = DebateConversation(
    debaters=debaters,
    format="academic",
    evidence_required=True,
    citation_style="APA",
    rounds=[
    "Theoretical Framework",
    "Empirical Evidence",
    "Counterexamples",
    "Future Projections"
    ],
    time_limit=10_minutes
    )

    result = debate.run({})


**Sample Output:**

.. code-block:: text

    Round 1 - Theoretical Framework:

    ThesisDefender: Economic theory suggests technological unemployment
    will accelerate. Brynjolfsson & McAfee (2014) demonstrate how AI
    automates cognitive tasks. UBI provides income floor enabling market
    participation when labor income becomes sporadic (Standing, 2017).

    ThesisChallenger: Classical economics shows income without productivity
    destroys currency value (Friedman, 1962). Historical examples like
    Speenhamland system (Polanyi, 1944) demonstrate how guaranteed income
    reduces labor participation and creates dependency cycles.

    Round 2 - Empirical Evidence:

    ThesisDefender: Finland's UBI experiment (2017-2018) showed no decrease
    in employment but significant improvements in mental health (Kangas et al.,
    2019). Kenya's GiveDirectly study found increased entrepreneurship and
    no inflation over 3 years (Haushofer & Shapiro, 2021).

    ThesisChallenger: Finland's experiment was limited and politically
    terminated. Alaska's dividend, often cited as UBI, is too small to
    show true effects. Spain's COVID UBI attempt faced massive fraud and
    implementation failures (Gentilini, 2022). No long-term successful example exists.

    Key Features Demonstrated



    1. **Structured Format**: Clear rounds with specific purposes
    2. **Position Advocacy**: Agents strongly defend assigned positions
    3. **Evidence-Based**: Arguments supported by facts and logic
    4. **Dynamic Rebuttals**: Agents respond to opponent's points
    5. **Judged Outcomes**: Optional scoring based on multiple criteria

    Configuration Options



.. code-block:: python

    # Code example here

    DebateConversation(
    debaters=agent_dict,              # Position -> Agent mapping
    topic="Debate topic",             # What to debate
    format="formal",                  # formal, panel, academic, casual
    rounds=["Opening", "Rebuttal"],   # Round structure
    time_limit=5_minutes,             # Time per speech
    judge_config={                    # Judge settings
    "criteria": ["logic", "evidence", "persuasion"],
    "weights": [0.3, 0.4, 0.3],
    "style": "analytical"
    },
    allow_interruptions=False,        # Oxford-style interruptions
    require_evidence=True,            # Must support claims
    )

    Best Practices


-------------

    1. **Clear Positions**: Define specific, opposing stances
    2. **Balanced Agents**: Similar capability levels for fair debate
    3. **Structured Rounds**: Use progressive round structure
    4. **Judgment Criteria**: Define clear scoring criteria
    5. **Time Management**: Set appropriate time limits

    Common Use Cases



    - **Decision Making**: Exploring pros/cons of important decisions
    - **Education**: Teaching critical thinking and argumentation
    - **Research**: Examining different theoretical positions
    - **Policy**: Evaluating policy proposals from multiple angles
    - **Entertainment**: Engaging audiences with intellectual content

    Advanced Example: Multi-Position Debate



.. code-block:: python

    # Code example here

    def example_multi_position_debate():
    """Debate with more than two positions."""

    positions = {
    "Capitalism": "Free markets best allocate resources",
    "Socialism": "Democratic control of economy is fairest",
    "Mixed": "Regulated markets with safety net optimal",
    "PostGrowth": "Abandon growth paradigm for sustainability"
    }

    debate = MultiPositionDebate(
    positions=positions,
    elimination_rounds=True,
    audience_voting=True,
    fact_checking=True
    )

    winner = debate.run_tournament()

    Customizing Debate Styles


------------------------

.. code-block:: python

    # Code example here

    # British Parliamentary style
    bp_debate = DebateConversation(
    format="british_parliamentary",
    teams={"Gov": [...], "Opp": [...]},
    poi_allowed=True  # Points of Information
    )

    # Lincoln-Douglas style
    ld_debate = DebateConversation(
    format="lincoln_douglas",
    value_premise_required=True,
    cross_examination_time=3_minutes
    )

    # Policy debate style
    policy_debate = DebateConversation(
    format="policy",
    evidence_cards=True,
    spreading_allowed=False,
    prep_time=10_minutes
    )

    See Also


-------

    - :doc:`conversation_directed - Orchestrated multi-agent discussions`

`
    - :doc`:`conversation_collaborative - Cooperative problem solving`

`
    - :doc`:`conversation_social_media - Online discussion dynamics`

`
    - :doc`:`../../api/index - Full API documentation`

`
`
