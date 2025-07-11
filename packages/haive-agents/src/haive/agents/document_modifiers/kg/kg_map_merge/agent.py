import logging
from typing import Any

from haive.core.engine.agent.agent import Agent, AgentConfig, register_agent
from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.documents import Document
from langgraph.constants import Send
from langgraph.graph import END, START
from langgraph.types import Send
from pydantic import BaseModel, Field

from haive.agents.document_modifiers.kg.kg_base.models import GraphTransformer
from haive.agents.document_modifiers.kg.kg_map_merge.engines import (
    create_parallel_kg_transformer_configs,
)

# Import models and engines
from haive.agents.document_modifiers.kg.kg_map_merge.models import (
    EntityNode,
    EntityRelationship,
    KnowledgeGraph,
)
from haive.agents.document_modifiers.kg.kg_map_merge.state import KnowledgeGraphState

logger = logging.getLogger(__name__)


class ParallelKGTransformerConfig(AgentConfig):
    """Configuration for the Parallel Knowledge Graph Transformer."""

    name: str = "ParallelKGTransformer"
    contents: list[Document]
    state_schema: KnowledgeGraphState = Field(
        default=KnowledgeGraphState,
        description="The state of the knowledge graph transformer.",
    )
    engines: dict[str, AugLLMConfig] = Field(
        default_factory=create_parallel_kg_transformer_configs,
        description="Configurations for different stages of graph transformation",
    )
    checkpoint_mode: str = Field(
        default="async", description="The checkpoint mode for the iterative summarizer."
    )


@register_agent(ParallelKGTransformerConfig)
class ParallelKGTransformer(Agent[ParallelKGTransformerConfig]):
    """An agent that builds a knowledge graph by extracting
    nodes and relationships in parallel across multiple documents.
    """

    def __init__(self, config: ParallelKGTransformerConfig):
        # Prepare graph transformer
        config.engines.get("graph_transformer")
        self.llm_graph_transformer = GraphTransformer()
        # Prepare extractors from engines
        self.node_extractor = config.engines["node_extractor"].create_runnable()
        self.relationship_extractor = config.engines[
            "relationship_extractor"
        ].create_runnable()
        self.graph_merger = config.engines["graph_merger"].create_runnable()

        super().__init__(config)

    def setup_workflow(self):
        self.graph.add_node("map_graph_documents", self.map_graph_documents)
        self.graph.add_node("collect_graph_documents", self.collect_graph_documents)
        self.graph.add_node("map_nodes", self.map_nodes)
        self.graph.add_node("collect_nodes", self.collect_nodes)
        self.graph.add_node("map_relationships", self.map_relationships)
        self.graph.add_node("collect_relationships", self.collect_relationships)
        self.graph.add_node("merge_graphs", self.merge_graphs)

        # ✅ Replace this line:
        # ✅ With this:

        self.graph.add_conditional_edges(
            START, self.map_graph_documents, ["collect_graph_documents"]
        )

        # ✅ Same idea for this conditional multi-send step

        self.graph.add_edge("collect_graph_documents", "map_nodes")

        self.graph.add_conditional_edges(
            "map_nodes",
            lambda state: "collect_nodes",
            {"collect_nodes": "collect_nodes"},
        )

        self.graph.add_edge("collect_nodes", "map_relationships")

        self.graph.add_conditional_edges(
            "map_relationships",
            lambda state: "collect_relationships",
            {"collect_relationships": "collect_relationships"},
        )

        self.graph.add_edge("collect_relationships", "merge_graphs")
        self.graph.add_edge("merge_graphs", END)

    def map_graph_documents(self, state: KnowledgeGraphState):
        return [
            Send("collect_graph_documents", {"content": doc, "index": i})
            for i, doc in enumerate(state.contents)
        ]

    async def collect_graph_documents(
        self, state: KnowledgeGraphState | dict[str, Any], **kwargs
    ):
        content = state["content"]
        # At this point, `content` is a Document object
        if isinstance(content, Document | dict):
            context = content
        elif isinstance(content, BaseModel):
            context = str(content)
        else:
            logger.error(
                f"Invalid content type for graph document extraction: {type(content)}"
            )
            return {}

        if not context:
            logger.warning("Empty context for graph document extraction")
            return {}

        graph_docs = await self.llm_graph_transformer.atransform_documents(
            documents=[context],
            strict_mode=True,
            ignore_tool_usage=True,
        )

        return {"graph_documents": graph_docs}

    def map_nodes(self, state: KnowledgeGraphState):
        """Map node extraction across documents."""
        if state.index >= len(state.contents):
            return {"index": state.index}

        # Create a Send for the current document
        return {
            "sends": [
                Send(
                    "collect_nodes",
                    {"content": state.contents[state.index], "index": state.index},
                )
            ],
            "index": state.index,
        }

    async def collect_nodes(
        self,
        state: KnowledgeGraphState,
        content: Document | dict | BaseModel | None = None,
        index: int | None = None,
    ):
        try:
            if isinstance(content, Document):
                context = content.page_content
            elif isinstance(content, dict):
                context = content.get("page_content", "")
            elif isinstance(content, BaseModel):
                context = str(content)
            else:
                logger.warning(
                    f"Invalid content type for node extraction: {type(content)}"
                )
                return {"index": 1}

            nodes = await self.node_extractor.ainvoke({"context": context})

            return {
                "nodes": nodes if isinstance(nodes, list) else [nodes],
                "index": 1,
            }

        except Exception as e:
            logger.exception(f"Error in collect_nodes: {e}")
            return {"index": 1}

    def map_relationships(self, state: KnowledgeGraphState):
        """Map relationship extraction across documents and nodes."""
        # If no documents or nodes left, proceed to next stage
        if not state.contents and not state.nodes:
            return {"sends": [Send("merge_graphs", {})]}

        # Create sends for processing
        sends = []

        # Process remaining documents
        if state.index < len(state.contents):
            sends.append(
                Send(
                    "collect_relationships",
                    {
                        "content": state.contents[state.index],
                        "index": state.index,
                        "context_type": "document",
                    },
                )
            )

        # Process nodes
        if state.nodes:
            sends.append(
                Send(
                    "collect_relationships",
                    {"nodes": state.nodes, "context_type": "nodes"},
                )
            )

        return {"sends": sends, "index": state.index}

    async def collect_relationships(
        self,
        state: KnowledgeGraphState,
        content: Document | dict | BaseModel | None = None,
        nodes: list[EntityNode] | None = None,
        index: int | None = None,
        context_type: str = "document",
    ):
        try:
            if context_type == "document":
                if isinstance(content, Document):
                    context = content.page_content
                elif isinstance(content, dict):
                    context = content.get("page_content", "")
                elif isinstance(content, BaseModel):
                    context = str(content)
                else:
                    logger.warning(
                        f"Invalid content type for relationship extraction: {type(content)}"
                    )
                    return {"index": 1}

                extractor_input = {"context": context}

            elif context_type == "nodes":
                if not nodes:
                    logger.warning("No nodes provided for relationship extraction")
                    return {"index": 1}

                context = "\n".join(
                    [
                        f"Entity {node.id}: {node.type} with properties {node.properties}"
                        for node in nodes
                    ]
                )
                extractor_input = {"context": context}

            else:
                logger.warning(f"Invalid context_type: {context_type}")
                return {"index": 1}

            relationships = await self.relationship_extractor.ainvoke(extractor_input)

            return {
                "relationships": (
                    relationships
                    if isinstance(relationships, list)
                    else [relationships]
                ),
                "index": 1,
            }

        except Exception as e:
            logger.exception(f"Error in collect_relationships: {e}")
            return {"index": 1}

    def merge_graphs(self, state: KnowledgeGraphState):
        """Merge extracted graph documents, nodes, and relationships."""
        try:
            # Create a KnowledgeGraph from extracted components
            kg = KnowledgeGraph()

            # Add nodes from graph documents
            for graph_doc in state.graph_documents:
                for node in graph_doc.nodes:
                    kg.add_node(EntityNode.from_graph_node(node))

            # Add nodes directly extracted
            for node in state.nodes:
                kg.add_node(node)

            # Add relationships from graph documents
            for graph_doc in state.graph_documents:
                for rel in graph_doc.relationships:
                    kg.add_relationship(EntityRelationship.from_graph_relationship(rel))

            for doc in state.graph_documents:
                for rel in doc.relationships:
                    kg.add_relationship(
                        EntityRelationship(
                            source=rel.source.id,
                            target=rel.target.id,
                            type=rel.type,
                            confidence_score=getattr(rel, "confidence_score", None),
                        )
                    )

            # Prepare context for graph merger
            graph_context = (
                "Nodes:\n"
                + "\n".join([f"- {node.id} (Type: {node.type})" for node in kg.nodes])
                + "\n\nRelationships:\n"
                + "\n".join(
                    [
                        f"- {rel.source} --({rel.type})--> {rel.target}"
                        for rel in kg.relationships
                    ]
                )
            )

            # Refine the graph using graph merger
            refined_graph = self.graph_merger.invoke({"graph_contexts": graph_context})

            return {
                "final_knowledge_graph": refined_graph,
                "graph_documents": [],
                "nodes": [],
                "relationships": [],
                "knowledge_graphs": [],
            }

        except Exception:

            # Fallback: use the created knowledge graph without LLM refinement
            return {
                "final_knowledge_graph": kg,
                "graph_documents": [],
                "nodes": [],
                "relationships": [],
                "knowledge_graphs": [],
            }


def build_agent(documents: list[Document]) -> ParallelKGTransformer:
    """Build a Parallel Knowledge Graph Transformer agent.

    Args:
        documents (List[Document]): Documents to process

    Returns:
        ParallelKGTransformer: Configured agent
    """
    config = ParallelKGTransformerConfig(contents=documents)
    return ParallelKGTransformer(config)


# Example usage
async def main():
    # Sample documents for testing
    test_docs = [
        Document(
            page_content="Marie Curie, born in 1867, was a Polish and naturalised-French physicist and chemist who conducted pioneering research on radioactivity."
        ),
        Document(
            page_content="Marie Curie was the first woman to win a Nobel Prize. Her husband, Pierre Curie, was a co-winner of her first Nobel Prize."
        ),
        Document(
            page_content="Poland is a country in Europe. Marie Curie was born in Poland and later became a naturalized French citizen."
        ),
        Document(
            page_content="Pierre Curie was a French physicist who made pioneering contributions to crystallography, magnetism, and radioactivity."
        ),
    ]

    # Create and run the agent
    agent = build_agent(test_docs)
    result = await agent.arun(
        {
            "contents": test_docs,
            "graph_documents": [],
            "knowledge_graphs": [],
            "nodes": [],
            "relationships": [],
            "index": 0,
        },
        config=agent.runnable_config,
        debug=True,
    )

    # Print final knowledge graph
    final_graph = result.get("final_knowledge_graph")
    if final_graph:
        for _node in final_graph.nodes:
            pass

        for _rel in final_graph.relationships:
            pass
    else:
        pass


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
