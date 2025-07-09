from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig
from langchain_core.prompts import ChatPromptTemplate

# Import the models
from haive.agents.document_modifiers.kg.kg_map_merge.models import (
    EntityNode,
    EntityRelationship,
    KnowledgeGraph,
)


def create_node_extraction_config(
    model: str = "gpt-4o", temperature: float = 0.7
) -> AugLLMConfig:
    """Create an AugLLMConfig for entity node extraction.

    Args:
        model: LLM model to use
        temperature: Sampling temperature for generation

    Returns:
        Configured AugLLMConfig for node extraction
    """
    # LLM Configuration
    llm_config = AzureLLMConfig(model=model, parameters={"temperature": temperature})

    # Prompt Template for Node Extraction
    node_extraction_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are an expert entity extractor. 
        Extract key entities from the given text with precision.
        
        Requirements:
        - Identify unique, meaningful entities
        - Assign accurate and specific types
        - Include relevant properties
        - Ensure high-quality, comprehensive entity representation
        
        Output Format:
        - Each entity should have a unique ID
        - Types should be descriptive but concise
        - Include important contextual properties""",
            ),
            ("human", "Extract entities from this text:\n{context}"),
        ]
    )

    # Create AugLLMConfig
    return AugLLMConfig(
        name="node_extractor",
        llm_config=llm_config,
        prompt_template=node_extraction_prompt,
        structured_output_model=EntityNode,  # Structured output for nodes
    )


def create_relationship_extraction_config(
    model: str = "gpt-4o", temperature: float = 0.7
) -> AugLLMConfig:
    """Create an AugLLMConfig for relationship extraction.

    Args:
        model: LLM model to use
        temperature: Sampling temperature for generation

    Returns:
        Configured AugLLMConfig for relationship extraction
    """
    # LLM Configuration
    llm_config = AzureLLMConfig(model=model, parameters={"temperature": temperature})

    # Prompt Template for Relationship Extraction
    relationship_extraction_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are an expert relationship extractor. 
        Identify and extract meaningful relationships between entities.
        
        Guidelines:
        - Extract clear, verifiable relationships
        - Assign precise relationship types
        - Provide supporting evidence
        - Assess relationship confidence
        - Capture nuanced contextual connections
        
        Output Requirements:
        - Source and target entities must be well-defined
        - Relationship type should be specific and meaningful
        - Include a confidence score (0-1)
        - Provide brief supporting evidence""",
            ),
            (
                "human",
                """Extract relationships from this text. 
        Consider the context and connections between entities:
        {context}""",
            ),
        ]
    )

    # Create AugLLMConfig
    return AugLLMConfig(
        name="relationship_extractor",
        llm_config=llm_config,
        prompt_template=relationship_extraction_prompt,
        structured_output_model=EntityRelationship,  # Structured output for relationships
    )


def create_graph_extraction_config(
    model: str = "gpt-4o", temperature: float = 0.7
) -> AugLLMConfig:
    """Create an AugLLMConfig for comprehensive knowledge graph extraction.

    Args:
        model: LLM model to use
        temperature: Sampling temperature for generation

    Returns:
        Configured AugLLMConfig for graph extraction
    """
    # LLM Configuration
    llm_config = AzureLLMConfig(model=model, parameters={"temperature": temperature})

    # Prompt Template for Graph Extraction
    graph_extraction_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are an expert knowledge graph extractor. 
        Create a comprehensive knowledge graph from the given text.
        
        Comprehensive Requirements:
        - Extract all meaningful entities
        - Identify rich, contextual relationships
        - Ensure high-quality, precise graph representation
        - Capture subtle and explicit connections
        
        Detailed Extraction Process:
        1. Identify unique entities with their types and properties
        2. Discover relationships between these entities
        3. Assess and score relationship confidence
        4. Provide supporting evidence for relationships""",
            ),
            (
                "human",
                "Extract a comprehensive knowledge graph from this text:\n{context}",
            ),
        ]
    )

    # Create AugLLMConfig
    return AugLLMConfig(
        name="graph_extractor",
        llm_config=llm_config,
        prompt_template=graph_extraction_prompt,
        structured_output_model=KnowledgeGraph,  # Structured output for entire graph
    )


def create_graph_merger_config(
    model: str = "gpt-4o", temperature: float = 0.7
) -> AugLLMConfig:
    """Create an AugLLMConfig for merging knowledge graphs.

    Args:
        model: LLM model to use
        temperature: Sampling temperature for generation

    Returns:
        Configured AugLLMConfig for graph merging
    """
    # LLM Configuration
    llm_config = AzureLLMConfig(model=model, parameters={"temperature": temperature})

    # Prompt Template for Graph Merging
    graph_merge_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are an expert knowledge graph reconciliation specialist.
        Merge multiple knowledge graphs with extreme precision.
        
        Merge Objectives:
        - Maintain entity consistency
        - Preserve meaningful relationships
        - Resolve conflicts between graphs
        - Select highest confidence relationships
        - Minimize redundancy
        
        Detailed Merging Process:
        1. Compare entities across graphs
        2. Reconcile conflicting entity properties
        3. Merge relationships with careful confidence scoring
        4. Create a unified, comprehensive knowledge graph""",
            ),
            (
                "human",
                """Merge these knowledge graphs with precision:
        {graph_contexts}
        
        Provide a unified, comprehensive knowledge graph.""",
            ),
        ]
    )

    # Create AugLLMConfig
    return AugLLMConfig(
        name="graph_merger",
        llm_config=llm_config,
        prompt_template=graph_merge_prompt,
        structured_output_model=KnowledgeGraph,  # Structured output for merged graph
    )


def create_parallel_kg_transformer_configs() -> dict:
    """Create a comprehensive set of configurations for the Parallel KG Transformer.

    Returns:
        Dictionary of AugLLMConfigs
    """
    return {
        "node_extractor": create_node_extraction_config(),
        "relationship_extractor": create_relationship_extraction_config(),
        "graph_extractor": create_graph_extraction_config(),
        "graph_merger": create_graph_merger_config(),
    }


# Example usage
def main():
    # Create configurations
    configs = create_parallel_kg_transformer_configs()

    # Demonstrate accessing configs
    for name, config in configs.items():
        print(f"Configuration for {name}:")
        print(f"  Model: {config.llm_config.model}")
        print(
            f"  Temperature: {config.llm_config.parameters.get('temperature', 'N/A')}"
        )
        print(
            f"  Structured Output: {config.structured_output_model.__name__ if config.structured_output_model else 'None'}"
        )
        print()


if __name__ == "__main__":
    main()
