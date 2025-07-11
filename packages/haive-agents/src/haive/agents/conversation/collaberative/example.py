# examples/conversation/collaborative_example.py
"""Examples for collaborative conversation patterns where participants build shared content."""

import logging

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig
from langchain_core.messages import AIMessage, SystemMessage

from haive.agents.conversation.collaberative.agent import CollaborativeConversation
from haive.agents.simple.agent import SimpleAgent

# Set logging
logging.getLogger("haive").setLevel(logging.WARNING)


def example_brainstorming_session():
    """Collaborative brainstorming for a new product."""

    # Create brainstorming session
    session = CollaborativeConversation.create_brainstorming_session(
        topic="Eco-friendly smart home device ideas",
        participants=["ProductManager", "Designer", "Engineer", "Marketer"],
        sections=[
            "Problem Statement",
            "Product Ideas",
            "Key Features",
            "Target Market",
            "Next Steps",
        ],
        min_contributions_per_section=1,
        max_rounds=2,
    )

    # Run session
    result = session.run(
        {}, config={"configurable": {"recursion_limit": 100}}, debug=True
    )

    # Display final document
    if "shared_document" in result:
        pass

    # Show contribution summary
    for speaker, count in result.get("contribution_count", {}).items():
        pass


def example_code_review():
    """Collaborative code review session."""

    # Create code review
    review = CollaborativeConversation.create_code_review(
        code_description="New authentication microservice using JWT tokens and Redis caching",
        reviewers={
            "SecurityExpert": "security specialist",
            "BackendLead": "backend architecture expert",
            "DevOpsEngineer": "deployment and infrastructure specialist",
        },
        min_contributions_per_section=1,
        max_rounds=3,
    )

    # Run review
    result = review.run(
        {}, config={"configurable": {"recursion_limit": 100}}, debug=True
    )

    # Display code review document
    if "shared_document" in result:
        pass


def example_project_planning():
    """Collaborative project planning session."""

    # Create project planning team
    team = {
        "ProjectManager": SimpleAgent(
            name="ProjectManager",
            engine=AugLLMConfig(
                name="pm_engine",
                system_message=(
                    "You are the project manager. Focus on timelines, deliverables, and coordination. "
                    "Be specific about milestones and dependencies."
                ),
                temperature=0.6,
            ),
        ),
        "TechLead": SimpleAgent(
            name="TechLead",
            engine=AugLLMConfig(
                name="tech_engine",
                system_message=(
                    "You are the technical lead. Focus on technical requirements, architecture, and risks. "
                    "Provide realistic estimates and identify technical challenges."
                ),
                temperature=0.6,
            ),
        ),
        "UXDesigner": SimpleAgent(
            name="UXDesigner",
            engine=AugLLMConfig(
                name="ux_engine",
                system_message=(
                    "You are the UX designer. Focus on user experience, design requirements, and user research needs. "
                    "Think about user journeys and interface design."
                ),
                temperature=0.7,
            ),
        ),
        "QALead": SimpleAgent(
            name="QALead",
            engine=AugLLMConfig(
                name="qa_engine",
                system_message=(
                    "You are the QA lead. Focus on testing strategy, quality metrics, and acceptance criteria. "
                    "Consider edge cases and testing timelines."
                ),
                temperature=0.6,
            ),
        ),
    }

    planning = CollaborativeConversation(
        participant_agents=team,  # type: ignore
        topic="Mobile Banking App Redesign Project",
        document_title="Project Plan: Mobile Banking App Redesign",
        sections=[
            "Project Overview",
            "Technical Requirements",
            "Design Requirements",
            "Timeline & Milestones",
            "Testing Strategy",
            "Risks & Mitigation",
        ],
        output_format="report",
        min_contributions_per_section=1,
        include_attribution=True,
        max_rounds=3,
    )

    result = planning.run(
        {}, config={"configurable": {"recursion_limit": 100}}, debug=True
    )

    # Display project plan
    if "shared_document" in result:
        pass


def example_research_paper():
    """Collaborative research paper writing."""

    # Research team
    researchers = {
        "LeadResearcher": SimpleAgent(
            name="LeadResearcher",
            engine=AugLLMConfig(
                name="lead_engine",
                system_message=(
                    "You are the lead researcher on AI ethics. "
                    "Focus on the main thesis and overall narrative. "
                    "Ensure academic rigor and clarity."
                ),
                temperature=0.6,
            ),
        ),
        "DataScientist": SimpleAgent(
            name="DataScientist",
            engine=AugLLMConfig(
                name="data_engine",
                system_message=(
                    "You are a data scientist. "
                    "Provide empirical evidence, statistics, and data analysis. "
                    "Focus on methodology and results."
                ),
                temperature=0.5,
            ),
        ),
        "EthicsExpert": SimpleAgent(
            name="EthicsExpert",
            engine=AugLLMConfig(
                name="ethics_engine",
                system_message=(
                    "You are an ethics philosopher. "
                    "Provide ethical frameworks and philosophical perspectives. "
                    "Consider implications and moral dimensions."
                ),
                temperature=0.7,
            ),
        ),
    }

    paper = CollaborativeConversation(
        participant_agents=researchers,  # type: ignore
        topic="The Ethical Implications of Large Language Models",
        document_title="Ethical Considerations in LLM Development and Deployment",
        sections=[
            "Abstract",
            "Introduction",
            "Literature Review",
            "Methodology",
            "Findings",
            "Ethical Analysis",
            "Conclusions",
            "Future Work",
        ],
        output_format="markdown",
        min_contributions_per_section=1,
        allow_revisions=True,
        include_attribution=False,  # Clean output for paper
        max_rounds=3,
    )

    result = paper.invoke({}, config={"configurable": {"recursion_limit": 50}})

    # Display research paper
    if "shared_document" in result:
        # Show just first few sections for brevity
        lines = result["shared_document"].split("\n")
        for _i, line in enumerate(lines[:50]):  # First 50 lines
            pass
        if len(lines) > 50:


def example_creative_writing():
    """Collaborative story writing."""

    # Writing team
    writers = {
        "NarrativeWriter": SimpleAgent(
            name="NarrativeWriter",
            engine=AugLLMConfig(
                name="narrative_engine",
                system_message=(
                    "You are a narrative writer focusing on plot and story structure. "
                    "Create engaging storylines and ensure narrative coherence."
                ),
                temperature=0.8,
            ),
        ),
        "CharacterWriter": SimpleAgent(
            name="CharacterWriter",
            engine=AugLLMConfig(
                name="character_engine",
                system_message=(
                    "You are a character development specialist. "
                    "Create vivid characters with depth and compelling dialogue."
                ),
                temperature=0.8,
            ),
        ),
        "WorldBuilder": SimpleAgent(
            name="WorldBuilder",
            engine=AugLLMConfig(
                name="world_engine",
                system_message=(
                    "You are a world-building expert. "
                    "Create rich settings and atmospheric descriptions."
                ),
                temperature=0.9,
            ),
        ),
    }

    story = CollaborativeConversation(
        participant_agents=writers,  # type: ignore
        topic="A mystery set in a futuristic space station",
        document_title="The Osiris Station Mystery",
        sections=[
            "Opening Scene",
            "Character Introductions",
            "The Discovery",
            "Rising Tension",
            "The Investigation",
            "Plot Twist",
            "Climax",
            "Resolution",
        ],
        output_format="markdown",
        min_contributions_per_section=1,
        include_attribution=True,  # See who wrote what
        max_rounds=3,
    )

    result = story.invoke({}, config={"configurable": {"recursion_limit": 50}})

    # Display story
    if "shared_document" in result:
        # Show opening sections
        sections = result["shared_document"].split("\n## ")
        if len(sections) > 1:
            if len(sections) > 2:
                pass  # Second section


if __name__ == "__main__":
    example_brainstorming_session()
