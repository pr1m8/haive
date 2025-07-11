# examples/conversation/debate_example.py
"""Examples for structured debate conversations."""

import logging

from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.messages import AIMessage, SystemMessage

from haive.agents.conversation.debate.agent import DebateConversation
from haive.agents.conversation.debate.state import DebateState
from haive.agents.simple.agent import SimpleAgent

# Set logging
logging.getLogger("haive").setLevel(logging.WARNING)


def example_simple_debate():
    """Simple two-sided debate on AI regulation."""

    # Create debate
    debate = DebateConversation.create_simple_debate(
        topic="Should AI development be regulated by governments?",
        position_a=(
            "ProRegulation",
            "AI development needs strict government oversight and regulation",
        ),
        position_b=(
            "AntiRegulation",
            "AI development should remain free from government interference",
        ),
        arguments_per_side=2,
        enable_opening_statements=True,
        enable_closing_statements=True,
        max_rounds=3,
    )

    # Run debate
    result = debate.run(
        {}, config={"configurable": {"recursion_limit": 50}}, debug=True
    )

    # Display debate highlights

    # Extract key moments
    for msg in result.get("messages", []):
        if isinstance(msg, AIMessage) and hasattr(msg, "name"):
            content = msg.content
            # Show opening statements, closing statements, and strong arguments
            if any(
                keyword in str(content).lower()
                for keyword in ["opening statement", "closing", "in conclusion"]
            ):
        elif isinstance(msg, SystemMessage):
            pass


# examples/conversation/debate_example.py
def example_panel_debate():
    """Multi-participant panel debate - FIXED VERSION."""

    # Create participant agents with proper state schema
    participants = {
        "TechOptimist": SimpleAgent(
            name="TechOptimist_agent",
            engine=AugLLMConfig(
                name="optimist_engine",
                system_message=(
                    "You are a technology optimist debating about social media's impact. "
                    "Your position: Social media has been overwhelmingly positive for society. "
                    "Make ONE concise argument. Keep it under 100 words."
                ),
                temperature=0.7,
            ),
            state_schema=DebateState,
        ),
        "DigitalWellbeing": SimpleAgent(
            name="DigitalWellbeing_agent",
            engine=AugLLMConfig(
                name="wellbeing_engine",
                system_message=(
                    "You are a digital wellbeing advocate. "
                    "Your position: Social media needs reform to protect mental health. "
                    "Make ONE concise argument. Keep it under 100 words."
                ),
                temperature=0.7,
            ),
            state_schema=DebateState,
        ),
        "PrivacyAdvocate": SimpleAgent(
            name="PrivacyAdvocate_agent",
            engine=AugLLMConfig(
                name="privacy_engine",
                system_message=(
                    "You are a privacy rights advocate. "
                    "Your position: Social media companies violate user privacy and need strict regulation. "
                    "Make ONE concise argument. Keep it under 100 words."
                ),
                temperature=0.7,
            ),
            state_schema=DebateState,
        ),
    }

    debate = DebateConversation(
        name="PanelDebate",
        participant_agents=participants,
        topic="The Impact of Social Media on Society",
        debate_positions={
            "TechOptimist": "Social media is a net positive",
            "DigitalWellbeing": "Social media needs mental health reforms",
            "PrivacyAdvocate": "Social media violates privacy rights",
        },
        arguments_per_side=1,  # Only 1 argument per participant
        enable_opening_statements=False,  # Skip opening statements
        enable_closing_statements=False,  # Skip closing statements
        enable_judge=False,  # No judge phase
        max_rounds=2,  # Only one round!
        state_schema=DebateState,
    )

    # Run debate with MUCH lower recursion limit
    result = debate.run(
        {}, config={"configurable": {"recursion_limit": 50}}, debug=False
    )

    # Show debate summary

    # Show the actual arguments made
    messages = result.get("messages", [])
    for msg in messages:
        if isinstance(msg, AIMessage) and hasattr(msg, "name"):


def example_oxford_debate():
    """Oxford-style formal debate."""

    # Create formal debate structure
    motion = "This house believes that artificial general intelligence (AGI) will be achieved within 10 years"

    # Create debaters with proper naming and state schema
    debaters = {
        "FirstProposition": SimpleAgent(
            name="FirstProposition_agent",
            engine=AugLLMConfig(
                name="prop1_engine",
                system_message=(
                    f"You are the first speaker for the proposition in an Oxford debate. "
                    f"Motion: {motion}. "
                    "Make a strong opening case with clear arguments. Be formal and structured."
                ),
                temperature=0.6,
            ),
            state_schema=DebateState,
        ),
        "FirstOpposition": SimpleAgent(
            name="FirstOpposition_agent",
            engine=AugLLMConfig(
                name="opp1_engine",
                system_message=(
                    f"You are the first speaker for the opposition in an Oxford debate. "
                    f"Motion: {motion}. "
                    "Refute the proposition and present counter-arguments. Be formal and structured."
                ),
                temperature=0.6,
            ),
            state_schema=DebateState,
        ),
        "SecondProposition": SimpleAgent(
            name="SecondProposition_agent",
            engine=AugLLMConfig(
                name="prop2_engine",
                system_message=(
                    f"You are the second speaker for the proposition. "
                    f"Motion: {motion}. "
                    "Reinforce your side's arguments and address opposition points."
                ),
                temperature=0.6,
            ),
            state_schema=DebateState,
        ),
        "SecondOpposition": SimpleAgent(
            name="SecondOpposition_agent",
            engine=AugLLMConfig(
                name="opp2_engine",
                system_message=(
                    f"You are the second speaker for the opposition. "
                    f"Motion: {motion}. "
                    "Strengthen opposition case and highlight flaws in proposition arguments."
                ),
                temperature=0.6,
            ),
            state_schema=DebateState,
        ),
    }

    debate = DebateConversation(
        name="OxfordDebate",
        participant_agents=debaters,
        topic=motion,
        debate_positions={
            "FirstProposition": "AGI within 10 years is achievable",
            "FirstOpposition": "AGI within 10 years is unrealistic",
            "SecondProposition": "Supporting AGI timeline",
            "SecondOpposition": "Opposing AGI timeline",
        },
        arguments_per_side=1,
        enable_opening_statements=True,
        enable_closing_statements=True,
        enforce_position_consistency=True,
        debate_format="oxford",
        max_rounds=2,  # Enough for all phases
        state_schema=DebateState,
    )

    # Run debate
    result = debate.run(
        {}, config={"configurable": {"recursion_limit": 100}}, debug=True
    )

    # Display formal structure

    # Show winner if declared
    if hasattr(result, "debate_winner") and result.debate_winner:
        pass


def example_socratic_debate():
    """Socratic method debate with questioning."""

    # Create Socratic dialogue participants
    participants = {
        "Socrates": SimpleAgent(
            name="Socrates_agent",
            engine=AugLLMConfig(
                name="socrates_engine",
                system_message=(
                    "You are Socrates, using the Socratic method. "
                    "Ask probing questions about knowledge and truth. "
                    "Challenge assumptions through questions, don't lecture. "
                    "Keep your responses concise and focused on questioning."
                ),
                temperature=0.7,
            ),
            state_schema=DebateState,
        ),
        "Student": SimpleAgent(
            name="Student_agent",
            engine=AugLLMConfig(
                name="student_engine",
                system_message=(
                    "You are a philosophy student engaged in dialogue with Socrates. "
                    "Try to answer his questions thoughtfully and ask your own questions. "
                    "Your initial position: Knowledge comes from education and books. "
                    "Be humble and open to learning."
                ),
                temperature=0.7,
            ),
            state_schema=DebateState,
        ),
    }

    debate = DebateConversation(
        name="SocraticDialogue",
        participant_agents=participants,
        topic="What is the nature of true knowledge?",
        debate_positions={
            "Socrates": "Knowledge comes from questioning and self-examination",
            "Student": "Knowledge comes from education and learning from others",
        },
        arguments_per_side=1,
        enable_opening_statements=False,  # More natural flow
        enable_closing_statements=False,
        require_evidence=False,  # Philosophical debate
        max_rounds=2,
        state_schema=DebateState,
    )

    # Start with Socratic question
    initial_message = AIMessage(
        content="Tell me, young friend, what do you believe knowledge to be?",
        name="Socrates",
    )

    # Run dialogue
    result = debate.run(
        {"messages": [initial_message]},
        config={"configurable": {"recursion_limit": 50}},
    )

    # Display dialogue
    messages = result.get("messages", [])
    for msg in messages:
        if isinstance(msg, AIMessage) and hasattr(msg, "name"):
            pass
        elif isinstance(msg, SystemMessage):
            pass


if __name__ == "__main__":
    # Run examples
    example_simple_debate()
