from haive.core.engine.agent.agent import AgentConfig
from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from pydantic import Field


class ParallelKGTransformerConfig(AgentConfig):
    """Configuration for the Parallel Knowledge Graph Transformer."""

    contents: list[Document]
    graph_extraction_config: AugLLMConfig = Field(
        default_factory=lambda: AugLLMConfig(
            name="graph_extractor",
            prompt_template=ChatPromptTemplate.from_messages(
                [
                    (
                        "system",
                        """Extract and refine the knowledge graph from the given text.
                Focus on identifying key entities and their relationships.
                Provide a comprehensive and accurate representation.""",
                    ),
                    ("human", "Extract knowledge graph from this text:\n{context}"),
                ]
            ),
        )
    )
    graph_merge_config: AugLLMConfig = Field(
        default_factory=lambda: AugLLMConfig(
            name="graph_merger",
            prompt_template=ChatPromptTemplate.from_messages(
                [
                    (
                        "system",
                        """Merge and reconcile multiple knowledge graphs.
                Identify consistent relationships, resolve conflicts,
                and create a comprehensive knowledge representation.""",
                    ),
                    (
                        "human",
                        """Merge these knowledge graphs:
                {graph_contexts}

                Provide a unified and refined knowledge graph.""",
                    ),
                ]
            ),
        )
    )
    checkpoint_mode: str = Field(
        default="async", description="The checkpoint mode for the iterative summarizer."
    )
