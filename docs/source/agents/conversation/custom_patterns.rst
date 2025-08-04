Custom Conversation Patterns
============================

Learn how to create your own conversation patterns tailored to specific needs by extending the base conversation classes.

Creating a Custom Conversation Type
-----------------------------------

Basic Template
~~~~~~~~~~~~~~

**Step 1: Inherit from BaseConversation**

.. code-block:: python

    from haive.agents.conversation.base import BaseConversation
    from typing import Dict, List, Optional
    import random

    class CustomConversation(BaseConversation):
    """Your custom conversation pattern."""

    def __init__(
    self,
    agents: List[Agent],
    custom_param: str,
    **kwargs**
    ):
    super().__init__(agents=agents, **kwargs)**
    self.custom_param = custom_param
    self.custom_state = {}

    async def select_next_speaker(self) -> Optional[Agent]:
    """Implement your speaker selection logic."""
    # Example: Random selection with weights
    weights = [self.get_agent_weight(agent) for agent in self.agents]
    return random.choices(self.agents, weights=weights)[0]

    def get_agent_weight(self, agent: Agent) -> float:
    """Calculate speaking probability for agent."""
    # Your custom logic here
    return 1.0

    async def should_end_conversation(self) -> bool:
    """Determine when conversation should end."""
    if self.turn_count >= self.max_turns:
    return True
    # Add your custom ending conditions
    return False

    async def process_message(self, message: Message) -> None:
    """Process messages with custom logic."""
    await super().process_message(message)
    # Add your custom processing
    self.update_custom_state(message)

    Example: Socratic Dialogue Pattern
    ----------------------------------

    A conversation pattern where one agent guides another through questions.

.. code-block:: python

    class SocraticDialogue(BaseConversation):
    """Socratic method conversation between teacher and student."""

    def __init__(
    self,
    teacher: Agent,
    student: Agent,
    topic: str,
    learning_objective: str,
    **kwargs**
    ):
    super().__init__(
    agents=[teacher, student],
    topic=topic,
    **kwargs**
    )
    self.teacher = teacher
    self.student = student
    self.learning_objective = learning_objective
    self.understanding_level = 0.0
    self.questions_asked = []

    async def select_next_speaker(self) -> Agent:
    """Alternate between teacher questions and student answers."""
    last_message = self.get_last_message()

    # First turn or after student answer -> teacher asks
    if not last_message or last_message.speaker == self.student.name:
    return self.teacher
    # After teacher question -> student answers
    else:
    return self.student

    async def generate_teacher_prompt(self) -> str:
    """Create prompts for Socratic questioning."""
    base_prompt = f"""You are using the Socratic method to help a student understand {self.topic}.
    Learning objective: {self.learning_objective}
    Questions asked so far: {len(self.questions_asked)}
    Student understanding: {self.understanding_level:.0%}

    Ask a thought-provoking question that guides discovery, don't give answers directly."""

    if self.understanding_level < 0.3:
    return base_prompt + "\nStart with fundamental concepts."
    elif self.understanding_level < 0.7:
    return base_prompt + "\nBuild on their basic understanding."
    else:
    return base_prompt + "\nChallenge them with edge cases."

    async def process_message(self, message: Message) -> None:
    """Track understanding progress."""
    await super().process_message(message)

    if message.speaker == self.teacher.name:
    # Extract and store question
    self.questions_asked.append(message.content)
    else:
    # Evaluate student response
    self.understanding_level = await self.evaluate_understanding(
    message.content
    )

    async def evaluate_understanding(self, response: str) -> float:
    """Assess student's understanding from response."""
    # Simple heuristic - in practice, use NLP/LLM
    indicators = [
    "I understand",
    "that makes sense", 
    "I see now",
    "because",
    "therefore"
    ]
    score = sum(ind in response.lower() for ind in indicators)
    return min(self.understanding_level + (score * 0.1), 1.0)*

    async def should_end_conversation(self) -> bool:
    """End when objective is reached or max turns."""
    if self.understanding_level >= 0.8:
    await self.add_system_message(
    "Learning objective achieved! Well done."
    )
    return True
    return await super().should_end_conversation()

    **Usage Example:**

.. code-block:: python

    # Create Socratic dialogue
    teacher = SimpleAgent(
    name="Socrates",
    system_message="You are a wise teacher using the Socratic method."
    )

    student = SimpleAgent(
    name="Student",
    system_message="You are a curious student trying to understand concepts."
    )

    dialogue = SocraticDialogue(
    teacher=teacher,
    student=student,
    topic="What is justice?",
    learning_objective="Understand justice isn't simply following laws",
    max_turns=20
    )

    result = await dialogue.run()

    Example: Negotiation Pattern
    ----------------------------

    Multi-party negotiation with offers and counteroffers.

.. code-block:: python

    class NegotiationConversation(BaseConversation):
    """Multi-party negotiation with deal tracking."""

    def __init__(
    self,
    parties: Dict[str, Agent],
    negotiation_subject: str,
    initial_positions: Dict[str, float],
    **kwargs**
    ):
    super().__init__(
    agents=list(parties.values()),
    topic=f"Negotiating {negotiation_subject}",
    **kwargs**
    )
    self.parties = parties
    self.positions = initial_positions.copy()
    self.offers = []
    self.deal_space = self.calculate_deal_space()
    self.agreement = None

    def calculate_deal_space(self) -> tuple:
    """Find potential agreement zone."""
    positions = list(self.positions.values())
    return (max(positions) * 0.8, min(positions) * 1.2)

    async def select_next_speaker(self) -> Agent:
    """Select party furthest from current offer."""
    if not self.offers:
    # Random start
    return random.choice(self.agents)

    last_offer = self.offers[-1]['amount']
    distances = {
    agent: abs(self.positions[agent.name] - last_offer)
    for agent in self.agents
    }
    # Party with most to gain/lose speaks next
    return max(distances, key=distances.get)

    async def process_message(self, message: Message) -> None:
    """Extract and track offers."""
    await super().process_message(message)

    # Parse offer from message
    offer = self.extract_offer(message.content)
    if offer:
    self.offers.append({
    'speaker': message.speaker,
    'amount': offer,
    'turn': self.turn_count
    })

    # Update position based on movement
    self.positions[message.speaker] = offer

    # Check for agreement
    if self.check_agreement(offer):
    self.agreement = offer

    def extract_offer(self, content: str) -> Optional[float]:
    """Extract numerical offer from message."""
    import re
    # Look for currency amounts
    match = re.search(r'\$?([\d,]+)', content)
    if match:
    return float(match.group(1).replace(',', ''))
    return None

    def check_agreement(self, offer: float) -> bool:
    """Check if all parties would accept offer."""
    if len(self.offers) < len(self.agents):
    return False

    # Simple rule: agreement if offer is in deal space
    # and no party objects in next round
    return self.deal_space[0] <= offer <= self.deal_space[1]

    async def should_end_conversation(self) -> bool:
    """End on agreement or deadlock."""
    if self.agreement:
    await self.add_system_message(
    f"Agreement reached at ${self.agreement:,.2f}!"
    )
    return True

    # Detect deadlock
    if len(self.offers) > len(self.agents) * 3:*
    recent_offers = [o['amount'] for o in self.offers[-6:]]
    if len(set(recent_offers)) <= 2:
    await self.add_system_message("Negotiation deadlocked.")
    return True

    return await super().should_end_conversation()

    Example: Progressive Disclosure Pattern
    ---------------------------------------

    Information revealed gradually based on trust/progress.

.. code-block:: python

    class ProgressiveDisclosure(BaseConversation):
    """Gradually reveal information as conversation progresses."""

    def __init__(
    self,
    informant: Agent,
    investigators: List[Agent],
    secret_info: List[str],
    trust_threshold: float = 0.7,
    **kwargs**
    ):
    super().__init__(
    agents=[informant] + investigators,
    **kwargs**
    )
    self.informant = informant
    self.investigators = investigators
    self.secret_info = secret_info
    self.revealed_info = []
    self.trust_level = 0.0
    self.trust_threshold = trust_threshold

    async def generate_informant_prompt(self) -> str:
    """Create prompts based on trust level."""
    base = f"You have sensitive information. Current trust: {self.trust_level:.0%}. "

    if self.trust_level < 0.3:
    return base + "Be very cautious and evasive."
    elif self.trust_level < self.trust_threshold:
    return base + "Give hints but don't reveal details."
    else:
    info_to_reveal = self.get_next_revelation()
    return base + f"Trust established. Reveal: {info_to_reveal}"

    def get_next_revelation(self) -> str:
    """Get next piece of information to reveal."""
    unrevealed = [
    info for info in self.secret_info 
    if info not in self.revealed_info
    ]
    if unrevealed:
    next_info = unrevealed[0]
    self.revealed_info.append(next_info)
    return next_info
    return "All information already shared."

    async def update_trust(self, message: Message) -> None:
    """Update trust based on investigator approach."""
    if message.speaker in [inv.name for inv in self.investigators]:
    # Simple heuristic - real implementation would analyze content
    if any(word in message.content.lower() for word in 
    ["please", "help", "important", "trust", "safe"]):
    self.trust_level = min(self.trust_level + 0.15, 1.0)
    elif any(word in message.content.lower() for word in 
    ["demand", "tell", "now", "must"]):
    self.trust_level = max(self.trust_level - 0.1, 0.0)

    Advanced Patterns
    -----------------

    **1. Parallel Conversations**

.. code-block:: python

    class ParallelConversations(BaseConversation):
    """Multiple simultaneous conversation threads."""

    def __init__(self, thread_configs: List[Dict], **kwargs):**
    # Initialize multiple conversation threads
    self.threads = [
    self.create_thread(config) 
    for config in thread_configs
    ]

    async def run_parallel(self):
    """Run all threads concurrently."""
    import asyncio
    results = await asyncio.gather(*[*
    thread.run() for thread in self.threads
    ])
    return self.merge_results(results)

    **2. Hierarchical Conversations**

.. code-block:: python

    class HierarchicalConversation(BaseConversation):
    """Conversations with reporting structure."""

    def __init__(self, hierarchy: Dict[str, List[str]], **kwargs):**
    self.hierarchy = hierarchy
    self.approval_needed = []
    self.decisions = {}

    **3. Time-Based Patterns**

.. code-block:: python

    class TimeBasedConversation(BaseConversation):
    """Conversations with time-sensitive elements."""

    def __init__(self, schedule: Dict[int, str], **kwargs):**
    self.schedule = schedule  # turn -> event
    self.time_pressure = False

    Best Practices for Custom Patterns
    ----------------------------------

    1. **Clear State Management**

   
    - Track conversation-specific state
    - Use dataclasses for complex state
    - Implement state persistence if needed

    2. **Flexible Configuration**

   
    - Use keyword arguments for extensibility
    - Provide sensible defaults
    - Allow runtime configuration changes

    3. **Robust Error Handling**

   
    - Handle agent failures gracefully
    - Implement timeout mechanisms
    - Provide fallback behaviors

    4. **Testing Your Pattern**

.. code-block:: python

    import pytest

    @pytest.mark.asyncio
    async def test_custom_conversation():
    # Create mock agents
    agents = [MockAgent(name=f"Agent{i}") for i in range(3)]

    # Test conversation
    conv = CustomConversation(agents=agents)
    result = await conv.run()

    # Assertions
    assert len(result['messages']) > 0
    assert conv.custom_state['some_metric'] > 0

    5. **Documentation**

.. code-block:: python

    class WellDocumentedConversation(BaseConversation):
    """Brief description of pattern.

    This conversation pattern implements [specific behavior].
    It's useful for [use cases].

    Args:
    agents: List of participating agents
    special_param: Controls [specific feature]

    Example:
    >>> conv = WellDocumentedConversation(
    ...     agents=[agent1, agent2],
    ...     special_param="value"
    ... )
    >>> result = await conv.run()
"""""""""""""""""""""""""""""""""

    Publishing Your Pattern
    -----------------------

    1. **Package Structure**

.. code-block:: text

    haive-conversation-extension/
    ├── src/
    │   └── haive_ext/
    │       └── conversations/
    │           ├── __init__.py
    │           └── my_pattern.py
    ├── tests/
    ├── examples/
    └── README.md

    2. **Registration**

.. code-block:: python

    # In __init__.py
    from haive.agents.conversation import register_pattern
    from .my_pattern import MyCustomConversation

    register_pattern("my_pattern", MyCustomConversation)

    3. **Usage**

.. code-block:: python

    from haive.agents.conversation import create_conversation

    conv = create_conversation(
    pattern="my_pattern",
    agents=agents,
    custom_param="value"
    )

    See Also
    --------

    - :doc:`index` - Conversation patterns overview
    - :doc:`/api/haive-agents` - Base classes documentation
    - :doc:`/guides/building_agents` - Agent development guide
    - :doc:`/guides/testing` - Testing conversational agents
