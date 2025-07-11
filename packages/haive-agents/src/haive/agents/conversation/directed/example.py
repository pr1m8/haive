# examples/conversation/directed_example.py
"""Examples for directed conversation patterns with mentions and targeted responses."""

import logging

from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from haive.agents.conversation.directed.agent import DirectedConversation
from haive.agents.simple.agent import SimpleAgent

# Set logging
logging.getLogger("haive").setLevel(logging.WARNING)


def example_classroom_discussion():
    """Classroom-style directed conversation."""
    classroom = DirectedConversation.create_classroom(
        teacher_name="Ms. Johnson",
        student_names=["Alex", "Sarah", "Mike", "Emma"],
        topic="The Water Cycle and Climate Change",
        max_rounds=3,
    )

    result = classroom.run(
        {}, debug=True, config={"configurable": {"recursion_limit": 50}}
    )

    # Display conversation
    for msg in result.get("messages", []):
        if isinstance(msg, AIMessage) and hasattr(msg, "name"):
            pass


def example_team_meeting():
    """Team meeting with directed questions and responses."""
    participants = {
        "Manager": SimpleAgent(
            name="Manager",
            engine=AugLLMConfig(
                system_message=(
                    "You are the team manager. Ask specific team members about their progress. "
                    "Use @mentions to direct questions. Keep it professional and brief."
                ),
                temperature=0.6,
            ),
        ),
        "Developer": SimpleAgent(
            name="Developer",
            engine=AugLLMConfig(
                system_message=(
                    "You are a software developer. Answer questions about technical progress. "
                    "You can ask the Designer about UI/UX needs."
                ),
                temperature=0.7,
            ),
        ),
        "Designer": SimpleAgent(
            name="Designer",
            engine=AugLLMConfig(
                system_message=(
                    "You are the UI/UX designer. Discuss design progress and needs. "
                    "You can ask the Developer about technical constraints."
                ),
                temperature=0.7,
            ),
        ),
        "QA": SimpleAgent(
            name="QA",
            engine=AugLLMConfig(
                system_message=(
                    "You are the QA engineer. Report on testing status and issues found. "
                    "Ask team members about specific features when needed."
                ),
                temperature=0.7,
            ),
        ),
    }

    meeting = DirectedConversation(
        participant_agents=participants,
        topic="Sprint Progress Update",
        max_rounds=3,
        fallback_to_round_robin=True,
        max_silence_turns=2,
    )

    result = meeting.run(
        {
            "messages": [
                HumanMessage(
                    content="Let's start our sprint update meeting. Manager, please begin."
                )
            ]
        },
        debug=True,
    )

    # Display key interactions
    for msg in result.get("messages", []):
        if isinstance(msg, AIMessage) and hasattr(msg, "name"):
            # Highlight mentions
            content = msg.content
            for participant in participants:
                if f"@{participant}" in content:
                    content = str(content).replace(
                        f"@{participant}", f"**@{participant}**"
                    )


def example_customer_support():
    """Customer support scenario with directed escalation."""
    support_team = {
        "Bot": SimpleAgent(
            name="SupportBot",
            engine=AugLLMConfig(
                system_message=(
                    "You are a customer support bot. Try to help with basic issues. "
                    "If the issue is complex, mention @Agent for human support."
                ),
                temperature=0.5,
            ),
        ),
        "Agent": SimpleAgent(
            name="Agent",
            engine=AugLLMConfig(
                system_message=(
                    "You are a human support agent. Handle escalated issues. "
                    "If technical, mention @TechLead for expertise."
                ),
                temperature=0.6,
            ),
        ),
        "TechLead": SimpleAgent(
            name="TechLead",
            engine=AugLLMConfig(
                system_message=(
                    "You are the technical lead. Provide expert technical solutions. "
                    "Work with @Agent to resolve complex issues."
                ),
                temperature=0.6,
            ),
        ),
    }

    support_conv = DirectedConversation(
        participant_agents=support_team,
        topic="Customer Issue: Application Crashing",
        max_rounds=3,
        mention_patterns=["@{name}", "escalate to {name}", "transfer to {name}"],
        fallback_to_round_robin=False,
    )

    result = support_conv.run(
        {
            "messages": [
                HumanMessage(
                    content="Customer: My application keeps crashing when I try to export data. This is urgent!"
                ),
                AIMessage(
                    content="I'll help you with that. Let me check...",
                    name="SupportBot",
                ),
            ]
        },
        debug=True,
    )

    # Display support flow
    for msg in result.get("messages", []):
        if isinstance(msg, AIMessage) and hasattr(msg, "name"):
            pass


def example_interactive_story():
    """Interactive storytelling with character interactions."""
    characters = {
        "Narrator": SimpleAgent(
            name="Narrator",
            engine=AugLLMConfig(
                system_message=(
                    "You are the story narrator. Set scenes and direct characters to interact. "
                    "Use @mentions to prompt specific characters to speak or act."
                ),
                temperature=0.8,
            ),
        ),
        "Hero": SimpleAgent(
            name="Hero",
            engine=AugLLMConfig(
                system_message=(
                    "You are the brave hero of the story. Respond when addressed or when "
                    "the situation calls for heroic action. You can interact with other characters."
                ),
                temperature=0.7,
            ),
        ),
        "Wizard": SimpleAgent(
            name="Wizard",
            engine=AugLLMConfig(
                system_message=(
                    "You are a wise wizard. Offer magical solutions and ancient knowledge. "
                    "Respond to requests for help or when magic is needed."
                ),
                temperature=0.8,
            ),
        ),
        "Villain": SimpleAgent(
            name="Villain",
            engine=AugLLMConfig(
                system_message=(
                    "You are the cunning villain. Create conflict and challenge the heroes. "
                    "Respond to confrontations and taunt the @Hero."
                ),
                temperature=0.8,
            ),
        ),
    }

    story = DirectedConversation(
        participant_agents=characters,
        topic="The Quest for the Crystal of Power",
        max_rounds=3,
        mention_patterns=["@{name}", "{name} speaks:", "turning to {name}"],
        allow_self_selection=True,
    )

    result = story.run({}, debug=True)

    # Display story
    for msg in result.get("messages", []):
        if isinstance(msg, AIMessage) and hasattr(msg, "name"):
            if msg.name == "Narrator":
                pass
            else:
                pass


if __name__ == "__main__":
    example_classroom_discussion()
