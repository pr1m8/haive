"""Graph Memory Agent with LLMGraphTransformer, TNT, and Graph RAG.

This implementation combines:
1. Graph transformation for structured knowledge extraction
2. Text-to-Neo4j (TNT) capabilities for direct graph database storage
3. Graph RAG for intelligent querying of the knowledge graph
"""

import json
import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any

from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.graphs import Neo4jGraph
from langchain_community.vectorstores import Neo4jVector
from langchain_core.documents import Document
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_neo4j.chains.graph_qa.cypher import GraphCypherQAChain
from langchain_neo4j.graphs.graph_document import GraphDocument

# Optional imports - GraphMemoryAgent will work with basic functionality even if these fail
try:
    from haive.agents.document_modifiers.kg.kg_base.models import GraphTransformer

    HAS_GRAPH_TRANSFORMER = True
except ImportError:
    GraphTransformer = None
    HAS_GRAPH_TRANSFORMER = False

try:
    from haive.agents.rag.db_rag.graph_db.agent import GraphDBRAGAgent
    from haive.agents.rag.db_rag.graph_db.config import GraphDBConfig, GraphDBRAGConfig

    HAS_GRAPH_DB_RAG = True
except ImportError:
    GraphDBRAGAgent = None
    GraphDBRAGConfig = None
    GraphDBConfig = None
    HAS_GRAPH_DB_RAG = False
from haive.core.engine.aug_llm import AugLLMConfig

logger = logging.getLogger(__name__)


class GraphMemoryMode(str, Enum):
    """Modes of operation for the graph memory agent."""

    EXTRACT_ONLY = "extract_only"  # Only extract entities/relationships
    STORE_ONLY = "store_only"  # Store in graph DB without extraction
    EXTRACT_AND_STORE = "extract_and_store"  # Extract and store
    QUERY_ONLY = "query_only"  # Only query existing graph
    FULL = "full"  # All capabilities


@dataclass
class GraphMemoryConfig:
    """Configuration for GraphMemoryAgent."""

    # Neo4j connection
    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_username: str = "neo4j"
    neo4j_password: str = "password"
    database_name: str = "neo4j"

    # Graph transformation settings
    allowed_nodes: list[str] = field(
        default_factory=lambda: [
            "Person",
            "Organization",
            "Location",
            "Event",
            "Concept",
            "Product",
            "Technology",
            "Date",
            "Skill",
            "Topic",
        ]
    )
    allowed_relationships: list[tuple[str, str, str]] = field(
        default_factory=lambda: [
            ("Person", "WORKS_FOR", "Organization"),
            ("Person", "KNOWS", "Person"),
            ("Person", "LOCATED_IN", "Location"),
            ("Person", "PARTICIPATED_IN", "Event"),
            ("Person", "HAS_SKILL", "Skill"),
            ("Organization", "LOCATED_IN", "Location"),
            ("Event", "OCCURRED_AT", "Location"),
            ("Event", "ON_DATE", "Date"),
            ("Person", "INTERESTED_IN", "Topic"),
            ("Concept", "RELATED_TO", "Concept"),
        ]
    )

    # Extraction settings
    extract_properties: bool = True
    node_properties: list[str] = field(
        default_factory=lambda: [
            "role",
            "description",
            "date",
            "importance",
            "confidence",
        ]
    )
    relationship_properties: list[str] = field(
        default_factory=lambda: ["since", "until", "strength", "context"]
    )

    # Memory settings
    user_id: str = "default_user"
    mode: GraphMemoryMode = GraphMemoryMode.FULL

    # LLM settings
    llm_config: AugLLMConfig | None = None

    # RAG settings
    enable_vector_index: bool = True
    embedding_model: str = "openai"

    def __post_init__(self):
        if self.llm_config is None:
            self.llm_config = AugLLMConfig(temperature=0.7)


class GraphMemoryAgent:
    """Agent that manages memory using a knowledge graph.

    This agent provides:
    - Entity and relationship extraction from text
    - Direct storage to Neo4j (TNT - Text to Neo4j)
    - Graph-based retrieval using Cypher queries
    - Vector similarity search on graph nodes
    - Complex graph traversal for memory retrieval
    """

    def __init__(self, config: GraphMemoryConfig):
        self.config = config
        self.logger = logger

        # Initialize Neo4j connection
        self._init_neo4j()

        # Initialize graph transformer
        self._init_graph_transformer()

        # Initialize RAG components if not query-only mode
        if config.mode != GraphMemoryMode.QUERY_ONLY:
            self._init_rag_components()

        # Initialize vector index if enabled
        if config.enable_vector_index:
            self._init_vector_index()

    def _init_neo4j(self):
        """Initialize Neo4j connection."""
        try:
            self.graph = Neo4jGraph(
                url=self.config.neo4j_uri,
                username=self.config.neo4j_username,
                password=self.config.neo4j_password,
                database=self.config.database_name,
            )

            # Create constraints for better performance
            self._create_graph_constraints()

            self.logger.info(f"Connected to Neo4j at {self.config.neo4j_uri}")
        except Exception as e:
            self.logger.error(f"Failed to connect to Neo4j: {e}")
            raise

    def _create_graph_constraints(self):
        """Create constraints and indexes for the graph."""
        try:
            # Create uniqueness constraints for common node types
            for node_type in ["Person", "Organization", "Location", "Event"]:
                self.graph.query(
                    f"CREATE CONSTRAINT IF NOT EXISTS FOR (n:{node_type}) "
                    f"REQUIRE n.id IS UNIQUE"
                )

            # Create indexes for better query performance
            self.graph.query("CREATE INDEX IF NOT EXISTS FOR (n:Person) ON (n.name)")
            self.graph.query(
                "CREATE INDEX IF NOT EXISTS FOR (n:Organization) ON (n.name)"
            )

            # Create user index for multi-user support
            self.graph.query("CREATE INDEX IF NOT EXISTS FOR (n:Memory) ON (n.user_id)")
        except Exception as e:
            self.logger.warning(f"Error creating constraints: {e}")

    def _init_graph_transformer(self):
        """Initialize the graph transformer for entity extraction."""
        if HAS_GRAPH_TRANSFORMER:
            self.graph_transformer = GraphTransformer()
        else:
            self.graph_transformer = None
            self.logger.warning(
                "GraphTransformer not available - graph extraction limited to LangChain LLMGraphTransformer"
            )

        # Always initialize LangChain's LLMGraphTransformer as fallback
        llm = self.config.llm_config.instantiate()
        self.llm_graph_transformer = LLMGraphTransformer(
            llm=llm,
            allowed_nodes=self.config.allowed_nodes,
            allowed_relationships=self.config.allowed_relationships,
            node_properties=(
                self.config.node_properties if self.config.extract_properties else False
            ),
            relationship_properties=(
                self.config.relationship_properties
                if self.config.extract_properties
                else False
            ),
            strict_mode=False,
        )

    def _init_rag_components(self):
        """Initialize Graph RAG components."""
        if HAS_GRAPH_DB_RAG:
            # Create GraphDBRAGConfig
            graph_db_config = GraphDBConfig(
                graph_db_uri=self.config.neo4j_uri,
                graph_db_user=self.config.neo4j_username,
                graph_db_password=self.config.neo4j_password,
                graph_db_database=self.config.database_name,
            )

            rag_config = GraphDBRAGConfig(
                domain_name="memory",
                domain_categories=["personal", "knowledge", "events"],
                graph_db_config=graph_db_config,
                llm_config=self.config.llm_config,
            )

            # Create Graph RAG agent
            self.graph_rag_agent = GraphDBRAGAgent(rag_config)
        else:
            self.graph_rag_agent = None
            self.logger.warning(
                "GraphDBRAGAgent not available - using basic Cypher chain only"
            )

        # Create Cypher QA chain for direct queries
        llm = self.config.llm_config.instantiate()
        self.cypher_chain = GraphCypherQAChain.from_llm(
            llm=llm,
            graph=self.graph,
            verbose=True,
            validate_cypher=True,
            return_intermediate_steps=True,
        )

    def _init_vector_index(self):
        """Initialize vector index for semantic search on graph."""
        try:
            embeddings = OpenAIEmbeddings()

            # Create vector index on Person nodes
            self.person_vector_index = Neo4jVector.from_existing_graph(
                embeddings,
                url=self.config.neo4j_uri,
                username=self.config.neo4j_username,
                password=self.config.neo4j_password,
                database=self.config.database_name,
                index_name="person_embeddings",
                node_label="Person",
                text_node_properties=["name", "description"],
                embedding_node_property="embedding",
            )

            # Create vector index on Concept nodes
            self.concept_vector_index = Neo4jVector.from_existing_graph(
                embeddings,
                url=self.config.neo4j_uri,
                username=self.config.neo4j_username,
                password=self.config.neo4j_password,
                database=self.config.database_name,
                index_name="concept_embeddings",
                node_label="Concept",
                text_node_properties=["name", "description"],
                embedding_node_property="embedding",
            )

            self.logger.info("Vector indexes created successfully")
        except Exception as e:
            self.logger.warning(f"Failed to create vector indexes: {e}")
            self.config.enable_vector_index = False

    async def extract_graph_from_text(
        self, text: str, metadata: dict[str, Any] | None = None
    ) -> list[GraphDocument]:
        """Extract entities and relationships from text.

        Args:
            text: Input text to process
            metadata: Optional metadata to attach

        Returns:
            List of GraphDocument objects
        """
        # Create document
        doc = Document(
            page_content=text,
            metadata=metadata
            or {
                "user_id": self.config.user_id,
                "timestamp": datetime.now().isoformat(),
                "source": "memory_extraction",
            },
        )

        # Use Haive's GraphTransformer if available, otherwise fall back to LangChain
        if self.graph_transformer is not None:
            graph_docs = self.graph_transformer.transform_documents(
                documents=[doc],
                llm_config=self.config.llm_config,
                allowed_nodes=self.config.allowed_nodes,
                allowed_relationships=self.config.allowed_relationships,
                node_properties=self.config.node_properties,
                relationship_properties=self.config.relationship_properties,
                additional_instructions="Extract all entities and relationships that represent memories, facts, and connections.",
            )
        else:
            # Fall back to LangChain LLMGraphTransformer
            graph_docs = self.llm_graph_transformer.convert_to_graph_documents([doc])

        return graph_docs

    async def store_graph_documents(
        self, graph_documents: list[GraphDocument], merge_nodes: bool = True
    ) -> dict[str, Any]:
        """Store graph documents in Neo4j (TNT - Text to Neo4j).

        Args:
            graph_documents: Graph documents to store
            merge_nodes: Whether to merge with existing nodes

        Returns:
            Storage statistics
        """
        nodes_created = 0
        relationships_created = 0
        errors = []

        for graph_doc in graph_documents:
            try:
                # Store nodes
                for node in graph_doc.nodes:
                    # Add user_id and timestamp
                    node_props = node.properties or {}
                    node_props.update(
                        {
                            "user_id": self.config.user_id,
                            "created_at": datetime.now().isoformat(),
                            "id": f"{node.type}_{node.id}_{self.config.user_id}",
                        }
                    )

                    if merge_nodes:
                        query = f"""
                        MERGE (n:{node.type} {{id: $id}})
                        SET n += $properties
                        SET n.name = $name
                        RETURN n
                        """
                    else:
                        query = f"""
                        CREATE (n:{node.type})
                        SET n = $properties
                        SET n.name = $name
                        SET n.id = $id
                        RETURN n
                        """

                    self.graph.query(
                        query,
                        {
                            "id": node_props["id"],
                            "name": node.id,
                            "properties": node_props,
                        },
                    )
                    nodes_created += 1

                # Store relationships
                for rel in graph_doc.relationships:
                    rel_props = rel.properties or {}
                    rel_props.update(
                        {
                            "user_id": self.config.user_id,
                            "created_at": datetime.now().isoformat(),
                        }
                    )

                    query = f"""
                    MATCH (a {{id: $source_id}})
                    MATCH (b {{id: $target_id}})
                    CREATE (a)-[r:{rel.type}]->(b)
                    SET r = $properties
                    RETURN r
                    """

                    source_id = (
                        f"{rel.source.type}_{rel.source.id}_{self.config.user_id}"
                    )
                    target_id = (
                        f"{rel.target.type}_{rel.target.id}_{self.config.user_id}"
                    )

                    self.graph.query(
                        query,
                        {
                            "source_id": source_id,
                            "target_id": target_id,
                            "properties": rel_props,
                        },
                    )
                    relationships_created += 1

            except Exception as e:
                errors.append(str(e))
                self.logger.error(f"Error storing graph document: {e}")

        # Also store as Memory node for tracking
        memory_query = """
        CREATE (m:Memory {
            id: $id,
            user_id: $user_id,
            content: $content,
            timestamp: $timestamp,
            nodes_created: $nodes_created,
            relationships_created: $relationships_created
        })
        RETURN m
        """

        self.graph.query(
            memory_query,
            {
                "id": f"memory_{datetime.now().timestamp()}_{self.config.user_id}",
                "user_id": self.config.user_id,
                "content": (
                    graph_documents[0].source.page_content if graph_documents else ""
                ),
                "timestamp": datetime.now().isoformat(),
                "nodes_created": nodes_created,
                "relationships_created": relationships_created,
            },
        )

        return {
            "nodes_created": nodes_created,
            "relationships_created": relationships_created,
            "errors": errors,
            "success": len(errors) == 0,
        }

    async def query_graph(
        self, query: str, query_type: str = "natural", include_context: bool = True
    ) -> dict[str, Any]:
        """Query the graph using natural language or Cypher.

        Args:
            query: Query string (natural language or Cypher)
            query_type: "natural" or "cypher"
            include_context: Include surrounding context in results

        Returns:
            Query results with optional context
        """
        if query_type == "natural":
            # Use Graph RAG agent for natural language queries if available
            if self.graph_rag_agent is not None:
                result = self.graph_rag_agent.invoke({"question": query})

                if include_context and result.get("cypher_statement"):
                    # Get additional context using the generated Cypher
                    context = self._get_query_context(result["cypher_statement"])
                    result["context"] = context

                return result
            # Fall back to Cypher chain for natural language queries
            try:
                result = self.cypher_chain.invoke({"query": query})

                if include_context:
                    context = self._get_query_context(query)
                    result["context"] = context

                return result
            except Exception as e:
                return {"error": str(e), "query": query, "fallback_used": True}

        elif query_type == "cypher":
            # Direct Cypher query
            try:
                results = self.graph.query(query)

                if include_context:
                    context = self._get_query_context(query)
                    return {
                        "results": results,
                        "context": context,
                        "cypher_statement": query,
                    }

                return {"results": results, "cypher_statement": query}

            except Exception as e:
                return {"error": str(e), "cypher_statement": query}

        else:
            return {"error": f"Unknown query type: {query_type}"}

    def _get_query_context(self, cypher_query: str) -> dict[str, Any]:
        """Get additional context around query results."""
        # Extract node references from the query
        # This is a simplified version - could be enhanced with proper parsing
        context_query = """
        // Get recently accessed nodes
        MATCH (n)
        WHERE n.user_id = $user_id
        RETURN n
        ORDER BY n.created_at DESC
        LIMIT 10
        """

        recent_nodes = self.graph.query(context_query, {"user_id": self.config.user_id})

        return {
            "recent_nodes": recent_nodes,
            "user_id": self.config.user_id,
            "timestamp": datetime.now().isoformat(),
        }

    async def search_similar_memories(
        self, query: str, node_type: str | None = None, k: int = 5
    ) -> list[dict[str, Any]]:
        """Search for similar memories using vector similarity.

        Args:
            query: Search query
            node_type: Optional node type to search (Person, Concept, etc.)
            k: Number of results

        Returns:
            Similar memories with scores
        """
        if not self.config.enable_vector_index:
            return []

        results = []

        # Search in appropriate indexes
        if node_type == "Person" or node_type is None:
            if hasattr(self, "person_vector_index"):
                person_results = self.person_vector_index.similarity_search_with_score(
                    query, k=k
                )
                results.extend(
                    [
                        {"type": "Person", "content": doc.page_content, "score": score}
                        for doc, score in person_results
                    ]
                )

        if node_type == "Concept" or node_type is None:
            if hasattr(self, "concept_vector_index"):
                concept_results = (
                    self.concept_vector_index.similarity_search_with_score(query, k=k)
                )
                results.extend(
                    [
                        {"type": "Concept", "content": doc.page_content, "score": score}
                        for doc, score in concept_results
                    ]
                )

        # Sort by score
        results.sort(key=lambda x: x["score"], reverse=True)

        return results[:k]

    async def get_memory_subgraph(
        self,
        entity_name: str,
        max_depth: int = 2,
        relationship_types: list[str] | None = None,
    ) -> dict[str, Any]:
        """Get a subgraph centered around an entity.

        Args:
            entity_name: Name of the central entity
            max_depth: Maximum traversal depth
            relationship_types: Optional filter for relationship types

        Returns:
            Subgraph data
        """
        rel_filter = ""
        if relationship_types:
            rel_types = "|".join(relationship_types)
            rel_filter = f":{rel_types}"

        query = f"""
        MATCH path = (n {{name: $name, user_id: $user_id}})-[{rel_filter}*1..{max_depth}]-(m)
        RETURN path
        LIMIT 100
        """

        paths = self.graph.query(
            query, {"name": entity_name, "user_id": self.config.user_id}
        )

        # Extract unique nodes and relationships
        nodes = set()
        relationships = set()

        for _path in paths:
            # Process path to extract nodes and relationships
            # This would need proper path parsing based on Neo4j return format
            pass

        return {
            "central_entity": entity_name,
            "nodes": list(nodes),
            "relationships": list(relationships),
            "depth": max_depth,
        }

    async def consolidate_memories(
        self, time_window: str | None = "1 day", min_connections: int = 2
    ) -> dict[str, Any]:
        """Consolidate related memories into higher-level concepts.

        Args:
            time_window: Time window for consolidation
            min_connections: Minimum connections for consolidation

        Returns:
            Consolidation results
        """
        # Find highly connected components
        query = """
        MATCH (n)-[r]-(m)
        WHERE n.user_id = $user_id AND m.user_id = $user_id
        WITH n, count(DISTINCT m) as connections
        WHERE connections >= $min_connections
        RETURN n, connections
        ORDER BY connections DESC
        LIMIT 20
        """

        candidates = self.graph.query(
            query, {"user_id": self.config.user_id, "min_connections": min_connections}
        )

        # Create concept nodes for highly connected entities
        concepts_created = 0
        for _candidate in candidates:
            # Create a concept that represents the cluster

            # Generate concept from candidate
            # This is simplified - would use LLM to generate meaningful concept
            concepts_created += 1

        return {
            "concepts_created": concepts_created,
            "candidates_analyzed": len(candidates),
            "timestamp": datetime.now().isoformat(),
        }

    async def run(
        self,
        input_text: str,
        mode: GraphMemoryMode | None = None,
        auto_store: bool = True,
    ) -> dict[str, Any]:
        """Main entry point for the agent.

        Args:
            input_text: Input text to process
            mode: Override default mode
            auto_store: Automatically store extracted graph

        Returns:
            Processing results
        """
        mode = mode or self.config.mode
        results = {
            "input": input_text,
            "mode": mode.value,
            "timestamp": datetime.now().isoformat(),
        }

        if mode in [
            GraphMemoryMode.EXTRACT_ONLY,
            GraphMemoryMode.EXTRACT_AND_STORE,
            GraphMemoryMode.FULL,
        ]:
            # Extract graph from text
            graph_docs = await self.extract_graph_from_text(input_text)
            results["extracted_graph"] = {
                "documents": len(graph_docs),
                "total_nodes": sum(len(doc.nodes) for doc in graph_docs),
                "total_relationships": sum(
                    len(doc.relationships) for doc in graph_docs
                ),
            }

            if auto_store and mode != GraphMemoryMode.EXTRACT_ONLY:
                # Store in Neo4j
                storage_result = await self.store_graph_documents(graph_docs)
                results["storage"] = storage_result

        if mode in [GraphMemoryMode.QUERY_ONLY, GraphMemoryMode.FULL]:
            # Also query for relevant memories
            query_result = await self.query_graph(
                f"What do we know about: {input_text}", query_type="natural"
            )
            results["query_result"] = query_result

        return results

    @classmethod
    def as_tool(cls, config: GraphMemoryConfig):
        """Convert to a LangChain tool for use in other agents."""
        from langchain_core.tools import tool

        instance = cls(config)

        @tool
        async def graph_memory_tool(text: str, operation: str = "full") -> str:
            """Process text with graph memory. Operations: extract, store, query, full."""
            mode_map = {
                "extract": GraphMemoryMode.EXTRACT_ONLY,
                "store": GraphMemoryMode.STORE_ONLY,
                "query": GraphMemoryMode.QUERY_ONLY,
                "full": GraphMemoryMode.FULL,
            }

            mode = mode_map.get(operation, GraphMemoryMode.FULL)
            result = await instance.run(text, mode=mode)

            return json.dumps(result, indent=2)

        return graph_memory_tool


# Example usage
async def example_graph_memory():
    """Example of using GraphMemoryAgent."""
    config = GraphMemoryConfig(
        neo4j_uri="bolt://localhost:7687",
        neo4j_username="neo4j",
        neo4j_password="password",
        user_id="alice_smith",
        mode=GraphMemoryMode.FULL,
    )

    agent = GraphMemoryAgent(config)

    # Process a memory
    result = await agent.run(
        "I met John Doe at the AI Conference in San Francisco last week. "
        "He works as a Senior Engineer at TechCorp and specializes in machine learning. "
        "We discussed implementing RAG systems using knowledge graphs."
    )

    print(f"Extraction and storage result: {json.dumps(result, indent=2)}")

    # Query the graph
    query_result = await agent.query_graph("Who did I meet at conferences recently?")
    print(f"Query result: {json.dumps(query_result, indent=2)}")

    # Search similar memories
    similar = await agent.search_similar_memories(
        "machine learning engineers", node_type="Person"
    )
    print(f"Similar memories: {json.dumps(similar, indent=2)}")

    # Get subgraph around John Doe
    subgraph = await agent.get_memory_subgraph("John Doe", max_depth=2)
    print(f"Subgraph: {json.dumps(subgraph, indent=2)}")


if __name__ == "__main__":
    import asyncio

    asyncio.run(example_graph_memory())
