# src/haive/agents/person_research/state.py

import operator
from typing import Annotated, Any

from pydantic import BaseModel, Field

# Define extraction schema
DEFAULT_EXTRACTION_SCHEMA = {
    "type": "object",
    "required": [
        "years_experience",
        "current_company",
        "role",
        "prior_companies",
    ],
    "properties": {
        "role": {"type": "string", "description": "Current role of the person."},
        "years_experience": {
            "type": "number",
            "description": "How many years of full time work experience (excluding internships) does this person have.",
        },
        "current_company": {
            "type": "string",
            "description": "The name of the current company the person works at.",
        },
        "prior_companies": {
            "type": "array",
            "items": {"type": "string"},
            "description": "List of previous companies where the person has worked",
        },
    },
    "description": "Person information",
    "title": "Person",
}


# Person model
class Person(BaseModel):
    """A class representing a person to research."""

    name: str | None = None
    """The name of the person."""
    company: str | None = None
    """The current company of the person."""
    linkedin: str | None = None
    """The Linkedin URL of the person."""
    email: str
    """The email of the person."""
    role: str | None = None
    """The current title of the person."""


# Input state
class PersonResearchInputState(BaseModel):
    """Input state defines the interface between the graph and the user (external API)."""

    person: Person = Field(description="Person to research.")
    extraction_schema: dict[str, Any] = Field(
        default_factory=lambda: DEFAULT_EXTRACTION_SCHEMA,
        description="The json schema defines the information the agent is tasked with filling out.",
    )
    user_notes: dict[str, Any] | None = Field(
        default=None,
        description="Any notes from the user to start the research process.",
    )


# Overall state
class PersonResearchState(BaseModel):
    """Overall state for the person research workflow."""

    person: Person = Field(description="Person to research provided by the user.")
    extraction_schema: dict[str, Any] = Field(
        default_factory=lambda: DEFAULT_EXTRACTION_SCHEMA,
        description="The json schema defines the information the agent is tasked with filling out.",
    )
    user_notes: str | None = Field(
        default=None,
        description="Any notes from the user to start the research process.",
    )
    search_queries: list[str] | None = Field(
        default=None,
        description="List of generated search queries to find relevant information",
    )
    completed_notes: Annotated[list[str], operator.add] = Field(
        default_factory=list,
        description="Notes from completed research related to the schema",
    )
    info: dict[str, Any] | None = Field(
        default=None,
        description="A dictionary containing the extracted and processed information.",
    )
    is_satisfactory: bool | None = Field(
        default=None,
        description="True if all required fields are well populated, False otherwise",
    )
    reflection_steps_taken: int = Field(
        default=0, description="Number of times the reflection node has been executed"
    )


# Output state
class PersonResearchOutputState(BaseModel):
    """The response object for the end user."""

    info: dict[str, Any] = Field(
        description="A dictionary containing the extracted and processed information."
    )


# Agent configuration
class PersonResearchAgentConfig(BaseModel):
    """Configuration settings for person research agent."""

    max_search_queries: int = Field(
        default=3, description="Maximum number of search queries per person"
    )
    max_search_results: int = Field(
        default=3, description="Maximum number of search results per query"
    )
    max_reflection_steps: int = Field(
        default=0, description="Maximum number of reflection steps"
    )
