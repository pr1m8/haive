"""Taxonomy and Topic (TNT) generation from document collections.

This module implements an advanced taxonomy generation system that processes
document collections through multiple stages to create hierarchical categorizations.
Based on the LangGraph TNT-LLM tutorial, it provides a production-ready implementation
for discovering and organizing topics in unstructured text.

The TNT agent uses a multi-stage approach:
    1. Document summarization - Extract key concepts from each document
    2. Minibatch processing - Group documents for efficient processing
    3. Initial taxonomy generation - Create initial category clusters
    4. Iterative refinement - Improve taxonomy through multiple passes
    5. Final review - Ensure quality and consistency

Key components:
    - :class:`~haive.agents.document_modifiers.tnt.agent.TaxonomyAgent`: Main agent class
    - :class:`~haive.agents.document_modifiers.tnt.state.TaxonomyGenerationState`: State management
    - :mod:`~haive.agents.document_modifiers.tnt.engines`: LLM configurations for each stage
    - :mod:`~haive.agents.document_modifiers.tnt.utils`: Formatting and utility functions

Example:
    Basic taxonomy generation::

        from haive.agents.document_modifiers.tnt import TaxonomyAgent
        from haive.agents.document_modifiers.tnt.config import TaxonomyAgentConfig

        # Configure agent
        config = TaxonomyAgentConfig(
            name="doc_taxonomy",
            visualize=True
        )
        agent = TaxonomyAgent(config)

        # Generate taxonomy from documents
        documents = [
            "Discussion about Python programming",
            "Questions about database design",
            "Machine learning model deployment"
        ]
        result = agent.run({"documents": documents})

        # Access generated taxonomy
        for category in result["final_taxonomy"]:
            print(f"{category['name']}: {category['description']}")

    Processing conversation histories::

        from haive.agents.document_modifiers.tnt.models import Doc

        # Create document objects with metadata
        docs = []
        for i, conv in enumerate(conversation_history):
            doc = Doc(
                id=f"conv_{i}",
                content=conv["text"],
                # Metadata preserved through processing
            )
            docs.append(doc)

        # Generate hierarchical taxonomy
        result = agent.run({"documents": docs})

See Also:
    - `LangGraph TNT Tutorial <https://langchain-ai.github.io/langgraph/tutorials/tnt-llm/tnt-llm/>`_
    - :mod:`haive.agents.document_modifiers.base`: Base document processing
    - :mod:`haive.agents.document_modifiers.kg`: Knowledge graph generation

Note:
    The name "TNT" comes from "Taxonomy and Topic" generation, representing
    the module's core purpose of creating hierarchical topic structures.
"""
