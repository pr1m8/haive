"""Branch decision functions for taxonomy generation workflow.

This module contains functions that determine the flow of the taxonomy generation process
by making decisions about which branch of the workflow to follow next.

Example:
    Basic usage of branch decision functions::

        state = TaxonomyGenerationState(...)
        next_node = should_review(state)
        # Returns either 'update_taxonomy' or 'review_taxonomy'
"""

from haive.agents.document_modifiers.tnt.state import TaxonomyGenerationState


# from langchain_core.runnables import RunnableConfig
# from langchain_core.tools import Runnable
def should_review(state: TaxonomyGenerationState) -> str:
    """Determines whether to continue refining the taxonomy or proceed to review.

    This function compares the number of taxonomy revisions against the number of
    minibatches to decide if enough iterations have been performed to warrant a
    final review.

    Args:
        state (TaxonomyGenerationState): The current state containing:
            - minibatches: List of document batch indices
            - clusters: List of taxonomy revisions

    Returns:
        str: Next node name in the workflow:
            - 'update_taxonomy': Continue refining if more minibatches need processing
            - 'review_taxonomy': Proceed to final review if all minibatches processed

    Example:
        >>> state = TaxonomyGenerationState(minibatches=[[1,2], [3,4]], clusters=[[...]])
        >>> next_node = should_review(state)
        >>> print(next_node)
        'update_taxonomy'  # Since only one revision exists for two minibatches
    """
    num_minibatches = len(state.minibatches)
    num_revisions = len(state.clusters)
    if num_revisions < num_minibatches:
        return "update_taxonomy"
    return "review_taxonomy"
