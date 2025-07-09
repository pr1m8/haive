# src/haive/agents/conversation/collaborative/agent.py
"""Collaborative conversation agent for building shared content."""

from typing import Any, Literal

from haive.core.logging.rich_logger import LogLevel, get_logger
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langgraph.types import Command
from pydantic import Field

from haive.agents.conversation.base.agent import BaseConversationAgent
from haive.agents.conversation.collaberative.state import CollaborativeState

logger = get_logger(__name__)
logger.set_level(LogLevel.WARNING)


class CollaborativeConversation(BaseConversationAgent):
    """Collaborative conversation for building shared content.

    Features:
    - Structured document building
    - Section-based contributions
    - Review and approval process
    - Version tracking
    - Multiple output formats
    """

    mode: Literal["collaborative"] = Field(default="collaborative")

    # Document structure
    document_title: str = Field(default="Collaborative Document")
    sections: list[str] = Field(
        default_factory=lambda: ["Introduction", "Main Content", "Conclusion"],
        description="Sections to collaborate on",
    )

    # Collaboration settings
    require_approval: bool = Field(
        default=False, description="Require approval before finalizing sections"
    )
    min_contributions_per_section: int = Field(
        default=1, description="Minimum contributions per section"
    )
    allow_revisions: bool = Field(
        default=True, description="Allow revision of completed sections"
    )

    # Output configuration
    output_format: Literal["markdown", "code", "outline", "report"] = Field(
        default="markdown"
    )
    include_attribution: bool = Field(
        default=True, description="Include contributor names in output"
    )

    def get_conversation_state_schema(self) -> type:
        """Use collaborative state schema."""
        return CollaborativeState

    def _custom_initialization(self, state: CollaborativeState) -> dict[str, Any]:
        """Initialize collaborative-specific state."""
        # Initialize document with title
        if self.output_format == "markdown":
            initial_doc = f"# {self.document_title}\n\n"
        elif self.output_format == "code":
            initial_doc = f"# {self.document_title}\n# Collaborative Code\n\n"
        elif self.output_format == "outline":
            initial_doc = f"{self.document_title}\n{'=' * len(self.document_title)}\n\n"
        else:  # report
            initial_doc = f"{self.document_title.upper()}\n\n"

        return {
            "shared_document": initial_doc,
            "sections_order": self.sections,
            "current_section": self.sections[0] if self.sections else None,
            "output_format": self.output_format,
            "document_sections": dict.fromkeys(self.sections, ""),
        }

    def _create_initial_message(self) -> BaseMessage:
        """Create collaborative session introduction."""
        sections_list = "\n".join([f"- {section}" for section in self.sections])

        return HumanMessage(
            content=f"""📝 Collaborative Session: {self.document_title}

Topic: {self.topic}

We'll work together on these sections:
{sections_list}

Format: {self.output_format}
Min contributions per section: {self.min_contributions_per_section}

Let's start with: {self.sections[0] if self.sections else 'open discussion'}"""
        )

    def select_speaker(self, state: CollaborativeState) -> Command:
        """Select speaker based on contribution balance and current section."""
        logger.debug("=== SELECT SPEAKER ===")
        logger.debug(f"Current section: {state.current_section}")
        logger.debug(f"Completed sections: {state.completed_sections}")
        logger.debug(f"Total contributions: {len(state.contributions)}")
        logger.debug(f"Conversation ended: {state.conversation_ended}")

        # Check if we need to move to next section
        section_update = self._check_section_completion(state)
        if section_update:
            logger.debug("Section update triggered")
            return section_update

        # Get current section
        current_section = state.current_section
        if not current_section:
            logger.debug("No current section - ending conversation")
            return Command(update={"conversation_ended": True})

        # Count contributions to current section
        section_contributors = {}
        for contributor, section, _ in state.contributions:
            if section == current_section:
                section_contributors[contributor] = (
                    section_contributors.get(contributor, 0) + 1
                )

        logger.debug(f"Section contributors: {section_contributors}")

        # Find who hasn't contributed enough
        speakers = state.speakers
        min_contributor = None
        min_count = float("inf")

        for speaker in speakers:
            count = section_contributors.get(speaker, 0)
            if count < min_count:
                min_count = count
                min_contributor = speaker

        # If everyone has contributed minimum, pick least active overall
        if min_count >= self.min_contributions_per_section:
            logger.debug(
                f"Everyone has contributed minimum ({self.min_contributions_per_section})"
            )
            return self._select_least_active_overall(state)

        logger.debug(f"Selected speaker: {min_contributor} (count: {min_count})")
        return Command(update={"current_speaker": min_contributor})

    def _check_section_completion(self, state: CollaborativeState) -> Command | None:
        """Check if current section is complete and move to next."""
        current_section = state.current_section
        if not current_section:
            return None

        # Count contributions to current section
        section_contribution_count = sum(
            1 for _, section, _ in state.contributions if section == current_section
        )

        # Check if section has enough contributions
        min_total = self.min_contributions_per_section * len(state.speakers)
        logger.debug(
            f"Section {current_section}: {section_contribution_count}/{min_total} contributions"
        )

        if section_contribution_count >= min_total:
            # Mark section complete
            completed = list(state.completed_sections)
            completed.append(current_section)

            # Find next section
            next_section = None
            for section in state.sections_order:
                if section not in completed:
                    next_section = section
                    break

            if next_section:
                transition_msg = SystemMessage(
                    content=f"✅ Section '{current_section}' complete. "
                    f"Moving to '{next_section}'."
                )
                return Command(
                    update={
                        "completed_sections": completed,
                        "current_section": next_section,
                        "messages": [transition_msg],
                        "current_speaker": (
                            state.speakers[0] if state.speakers else None
                        ),
                    }
                )
            # All sections complete
            logger.debug("All sections complete - finalizing document")
            return self._finalize_document(state)

        return None

    def _select_least_active_overall(self, state: CollaborativeState) -> Command:
        """Select speaker who has contributed least overall."""
        contribution_count = dict(state.contribution_count)

        min_speaker = None
        min_count = float("inf")

        for speaker in state.speakers:
            count = contribution_count.get(speaker, 0)
            if count < min_count:
                min_count = count
                min_speaker = speaker

        return Command(update={"current_speaker": min_speaker})

    def _prepare_agent_input(
        self, state: CollaborativeState, agent_name: str
    ) -> dict[str, Any]:
        """Prepare input with collaboration context."""
        base_input = super()._prepare_agent_input(state, agent_name)

        # Get current section content
        current_section = state.current_section
        section_content = state.document_sections.get(str(current_section), "")

        # Create context message
        context_parts = [
            f"Current Section: {current_section}",
            f"Your total contributions: {state.contribution_count.get(agent_name, 0)}",
            f"Format: {state.output_format}",
        ]

        if section_content:
            context_parts.append(f"\nCurrent content:\n{section_content}")

        context_msg = SystemMessage(content="\n".join(context_parts))

        # Add instruction based on section state
        if section_content:
            instruction = SystemMessage(
                content="Build upon or enhance the existing content. "
                "Be constructive and collaborative."
            )
        else:
            instruction = SystemMessage(
                content=f"Start the '{current_section}' section. "
                "Provide a solid foundation for others to build on."
            )

        messages = [context_msg, instruction] + base_input.get("messages", [])
        base_input["messages"] = messages

        return base_input

    def process_response(self, state: CollaborativeState) -> Command:
        """Process contribution and update document."""
        if not state.current_speaker or not state.messages:
            return Command(update={})

        last_msg = state.messages[-1]
        if not isinstance(last_msg, AIMessage) or not hasattr(last_msg, "name"):
            return Command(update={})

        contributor = last_msg.name
        content = last_msg.content
        current_section = state.current_section

        # Build complete updated values
        # Add new contribution to existing list
        new_contributions = state.contributions + [
            (contributor, current_section, content)
        ]

        # Update contribution count
        new_contribution_count = state.contribution_count.copy()
        new_contribution_count[str(contributor)] = (
            new_contribution_count.get(str(contributor), 0) + 1
        )

        # Update section content
        new_document_sections = state.document_sections.copy()
        if current_section:
            # Add content with attribution if enabled
            if self.include_attribution:
                new_content = f"[{contributor}]: {content}"
            else:
                new_content = str(content)

            # Append to existing section content
            if new_document_sections.get(current_section):
                new_document_sections[current_section] = (
                    new_document_sections[current_section].rstrip() + "\n" + new_content
                )
            else:
                new_document_sections[current_section] = new_content

        # Compile updated document
        new_shared_document = self._compile_document(state, new_document_sections)

        # Return Command with complete updated values
        return Command(
            update={
                "contributions": new_contributions,
                "contribution_count": new_contribution_count,
                "document_sections": new_document_sections,
                "shared_document": new_shared_document,
            }
        )

    def _compile_document(
        self, state: CollaborativeState, sections: dict[str, str]
    ) -> str:
        """Compile sections into final document."""
        # Get title from current document or use default
        if state.shared_document:
            doc_parts = [state.shared_document.split("\n\n")[0]]  # Keep title
        elif self.output_format == "markdown":
            doc_parts = [f"# {self.document_title}"]
        elif self.output_format == "code":
            doc_parts = [f"# {self.document_title}\n# Collaborative Code"]
        elif self.output_format == "outline":
            doc_parts = [f"{self.document_title}\n{'=' * len(self.document_title)}"]
        else:  # report
            doc_parts = [f"{self.document_title.upper()}"]

        for section in state.sections_order:
            if sections.get(section):
                if self.output_format == "markdown":
                    doc_parts.append(f"## {section}\n{sections[section]}")
                elif self.output_format == "outline":
                    doc_parts.append(f"{section}:\n{sections[section]}")
                elif self.output_format == "code":
                    doc_parts.append(f"# {section}\n{sections[section]}")
                else:  # report
                    doc_parts.append(f"{section.upper()}\n\n{sections[section]}")

        return "\n\n".join(doc_parts)

    def _finalize_document(self, state: CollaborativeState) -> Command:
        """Finalize the collaborative document."""
        # Create final summary
        total_contributions = len(state.contributions)
        contributor_summary = []

        for speaker, count in state.contribution_count.items():
            contributor_summary.append(f"- {speaker}: {count} contributions")

        summary_msg = SystemMessage(
            content=f"""📄 Document Complete!

Title: {self.document_title}
Total Contributions: {total_contributions}

Contributors:
{chr(10).join(contributor_summary)}

The final document has been compiled."""
        )

        return Command(update={"messages": [summary_msg], "conversation_ended": True})

    def _check_custom_end_conditions(self, state: CollaborativeState) -> Command | None:
        """Check if all sections are complete."""
        if len(state.completed_sections) >= len(self.sections):
            return self._finalize_document(state)
        return None

    @classmethod
    def create_brainstorming_session(
        cls,
        topic: str,
        participants: list[str],
        sections: list[str] | None = None,
        **kwargs,
    ):
        """Create a brainstorming/ideation session.

        Args:
            topic: Brainstorming topic
            participants: List of participant names
            sections: Optional custom sections
            **kwargs: Additional configuration
        """
        if sections is None:
            sections = ["Problem Statement", "Ideas", "Evaluation", "Action Items"]

        from haive.core.engine.aug_llm import AugLLMConfig

        from haive.agents.simple.agent import SimpleAgent

        agents = {}
        for name in participants:
            engine = AugLLMConfig(
                name=f"{name.lower()}_engine",
                system_message=(
                    f"You are {name}, participating in a brainstorming session. "
                    "Be creative, build on others' ideas, and think outside the box. "
                    "Keep contributions focused and constructive."
                ),
                temperature=0.8,
            )
            agents[name] = SimpleAgent(name=f"{name}_agent", engine=engine)

        # Calculate appropriate max_rounds
        # Each participant needs to contribute min_contributions_per_section times per section
        min_contributions = kwargs.get("min_contributions_per_section", 1)
        total_contributions_needed = (
            len(participants) * len(sections) * min_contributions
        )

        # Add some buffer for conversation flow
        suggested_max_rounds = total_contributions_needed + len(sections) + 5

        # Use the suggested max_rounds if not explicitly provided
        if "max_rounds" not in kwargs:
            kwargs["max_rounds"] = suggested_max_rounds

        return cls(
            participant_agents=agents,
            topic=topic,
            document_title=f"Brainstorming: {topic}",
            sections=sections,
            output_format="outline",
            **kwargs,
        )

    @classmethod
    def create_code_review(
        cls,
        code_description: str,
        reviewers: dict[str, str],  # name -> expertise
        **kwargs,
    ):
        """Create a collaborative code review session.

        Args:
            code_description: Description of code being reviewed
            reviewers: Dictionary mapping reviewer names to expertise
            **kwargs: Additional configuration
        """
        from haive.core.engine.aug_llm import AugLLMConfig

        from haive.agents.simple.agent import SimpleAgent

        agents = {}
        for name, expertise in reviewers.items():
            engine = AugLLMConfig(
                name=f"{name.lower()}_engine",
                system_message=(
                    f"You are {name}, a {expertise} reviewing code. "
                    "Provide constructive feedback on code quality, design, "
                    "performance, and best practices. Be specific and helpful."
                ),
                temperature=0.6,
            )
            agents[name] = SimpleAgent(name=f"{name}_agent", engine=engine)

        # Calculate appropriate max_rounds
        min_contributions = kwargs.get("min_contributions_per_section", 1)
        sections = ["Overview", "Strengths", "Issues", "Suggestions", "Conclusion"]
        total_contributions_needed = len(reviewers) * len(sections) * min_contributions
        suggested_max_rounds = total_contributions_needed + len(sections) + 5

        if "max_rounds" not in kwargs:
            kwargs["max_rounds"] = suggested_max_rounds

        return cls(
            participant_agents=agents,
            topic=code_description,
            document_title="Code Review",
            sections=sections,
            output_format="markdown",
            **kwargs,
        )
