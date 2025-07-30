"""Branches graph module.

This module provides branches functionality for the Haive framework.
"""

from haive.core.graph.branches import Branch
from langgraph.graph import END

# Define the Guardrails Branch
guardrails_branch = Branch(
    key="next_action",
    destinations={"end": "generate_final_answer", "movie": "generate_cypher"},
    default=END,  # Default to ending if no match
)

# Define the Cypher Validation Branch
validate_cypher_branch = Branch(
    key="next_action",
    destinations={
        "end": "generate_final_answer",
        "correct_cypher": "correct_cypher",
        "execute_cypher": "execute_cypher",
    },
    default=END,  # Default to ending if no match
)
