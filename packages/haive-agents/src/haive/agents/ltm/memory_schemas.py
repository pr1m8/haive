# ============================================================================
# LTM MEMORY SCHEMAS
# ============================================================================
"""Memory schemas for LTM agent using LangMem patterns.

These schemas define the structure of memories that will be extracted
and managed by the LTM agent.
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

# ============================================================================
# BASIC MEMORY SCHEMA (from LangMem)
# ============================================================================


class Memory(BaseModel):
    """Basic memory schema following LangMem patterns."""

    content: str = Field(
        description="The memory as a well-written, standalone episode/fact/note/preference/etc."
    )


# ============================================================================
# EXTENDED MEMORY SCHEMAS
# ============================================================================


class UserPreference(BaseModel):
    """User preference memory."""

    category: str = Field(description="Preference category (e.g., food, music, etc.)")
    preference: str = Field(description="The actual preference")
    context: str = Field(description="Context or reasoning behind the preference")
    confidence: float = Field(
        default=0.8, description="Confidence level in this preference (0.0-1.0)"
    )


class FactualMemory(BaseModel):
    """Factual information memory."""

    fact: str = Field(description="The factual information")
    domain: str = Field(description="Domain or category of the fact")
    source: str | None = Field(default=None, description="Source of the information")
    verification_level: str = Field(
        default="stated",
        description="Level of verification: stated, confirmed, verified",
    )


class PersonalContext(BaseModel):
    """Personal context and relationship memory."""

    person: str = Field(description="Person or entity this context relates to")
    relationship: str = Field(description="Relationship to the user")
    context: str = Field(description="Important context about this person/relationship")
    importance: str = Field(
        default="medium", description="Importance level: low, medium, high, critical"
    )


class ConversationalMemory(BaseModel):
    """General conversational memory."""

    content: str = Field(description="The conversational memory content")
    topic: str = Field(description="Main topic or theme")
    emotional_tone: str | None = Field(
        default=None, description="Emotional tone if relevant"
    )
    action_items: list[str] = Field(
        default_factory=list, description="Any action items or follow-ups mentioned"
    )


# ============================================================================
# SCHEMA COLLECTIONS
# ============================================================================

# Default schemas for the LTM agent
DEFAULT_MEMORY_SCHEMAS = [Memory, UserPreference, FactualMemory, ConversationalMemory]

# Extended schemas including personal context
EXTENDED_MEMORY_SCHEMAS = [
    Memory,
    UserPreference,
    FactualMemory,
    PersonalContext,
    ConversationalMemory,
]

# Minimal schemas for basic use cases
MINIMAL_MEMORY_SCHEMAS = [Memory, UserPreference]
