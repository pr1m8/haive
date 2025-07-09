"""Document transformation and information extraction agents.

This module provides a comprehensive suite of agents for transforming documents
and extracting structured information. It includes agents for building knowledge
graphs, generating taxonomies, summarizing documents, and extracting structured
data with validation.

The module is organized into specialized submodules:
    - :mod:`~haive.agents.document_modifiers.base`: Base classes and shared state
    - :mod:`~haive.agents.document_modifiers.tnt`: Taxonomy and topic generation
    - :mod:`~haive.agents.document_modifiers.complex_extraction`: Structured data extraction
    - :mod:`~haive.agents.document_modifiers.kg`: Knowledge graph construction
    - :mod:`~haive.agents.document_modifiers.summarizer`: Document summarization

Key Features:
    - Schema-based data extraction with validation and retries
    - Multiple knowledge graph construction strategies
    - Map-reduce document summarization for large texts
    - Hierarchical taxonomy generation from conversations
    - Shared document processing state and utilities

Example:
    Basic knowledge graph extraction::

        from haive.agents.document_modifiers.kg.kg_map_merge import ParallelKGTransformer
        from haive.agents.document_modifiers.kg.kg_map_merge.config import ParallelKGTransformerConfig

        # Configure and create agent
        config = ParallelKGTransformerConfig()
        agent = ParallelKGTransformer(config)

        # Extract knowledge graph
        documents = ["Marie Curie won two Nobel Prizes.", "She discovered radium."]
        result = agent.run({"contents": documents})
        graph = result["final_graph"]

    Document summarization::

        from haive.agents.document_modifiers.summarizer.map_branch import SummarizerAgent
        from haive.agents.document_modifiers.summarizer.map_branch.config import SummarizerAgentConfig

        config = SummarizerAgentConfig(token_max=1000)
        agent = SummarizerAgent(config)

        result = agent.run({"contents": ["Long document text..."]})
        summary = result["final_summary"]

See Also:
    :mod:`haive.agents.document_modifiers.tnt`: Taxonomy generation from conversations
    :mod:`haive.agents.document_modifiers.base`: Base document processing utilities
    :mod:`haive.agents.document_modifiers.summarizer`: Advanced summarization strategies
    :mod:`haive.agents.document_modifiers.complex_extraction`: Schema-based data extraction
    :mod:`haive.agents.document_modifiers.kg`: Knowledge graph construction agents

Note:
    All agents in this module process documents asynchronously. Use the
    appropriate async/await patterns when integrating with your application.
"""
