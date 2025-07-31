"""Knowledge Graph Memory Agent with Graph Database Integration.

This agent extends the existing KG transformer capabilities with:
1. Graph database upload and storage (Neo4j, Neptune, etc.)
2. Memory-specific knowledge graph construction
3. Time-weighted graph retrieval
4. Configurable storage backends

Based on existing ParallelKGTransformer but optimized for memory workflows.
"""

import logging
from datetime import datetime
from enum import Enum
from typing import Any
from uuid import uuid4

from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.documents import Document
from langchain_core.messages import BaseMessage
from pydantic import BaseModel, ConfigDict, Field

# Import existing KG components
from haive.agents.document_modifiers.kg.kg_base.models import GraphTransformer
from haive.agents.document_modifiers.kg.kg_map_merge.models import (
    EntityNode,
    EntityRelationship,
    KnowledgeGraph,
)

# Import our memory components
from .memory_state_original import (
    EnhancedMemoryItem,
)
from .message_document_converter import MessageDocumentConverter

logger = logging.getLogger(__name__)


class GraphStorageBackend(str, Enum):
    """Supported graph database backends."""

    MEMORY = "memory"  # In-memory storage only
    NEO4J = "neo4j"  # Neo4j graph database
    NEPTUNE = "neptune"  # Amazon Neptune
    ARANGODB = "arango"  # ArangoDB
    FILE = "file"  # File-based storage (JSON/GraphML)


class KGMemoryConfig(BaseModel):
    """Configuration for KG Memory Agent."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    # Graph construction settings
    llm_config: AugLLMConfig = Field(default_factory=AugLLMConfig)

    # Memory-specific node types
    memory_node_types: list[str] = Field(
        default=[
            "Person",
            "Organization",
            "Location",
            "Concept",
            "Skill",
            "Project",
            "Technology",
            "Event",
            "Goal",
            "Problem",
            "Solution",
        ]
    )

    # Memory-specific relationships
    memory_relationships: list[str | tuple[str, str, str]] = Field(
        default=[
            ("Person", "WORKS_AT", "Organization"),
            ("Person", "KNOWS", "Person"),
            ("Person", "HAS_SKILL", "Skill"),
            ("Person", "INTERESTED_IN", "Concept"),
            ("Person", "WORKS_ON", "Project"),
            ("Person", "USES", "Technology"),
            ("Person", "ATTENDED", "Event"),
            ("Person", "WANTS", "Goal"),
            ("Person", "FACES", "Problem"),
            ("Problem", "HAS_SOLUTION", "Solution"),
            ("Project", "USES", "Technology"),
            ("Organization", "LOCATED_IN", "Location"),
            ("Concept", "RELATES_TO", "Concept"),
        ]
    )

    # Graph database settings
    storage_backend: GraphStorageBackend = Field(default=GraphStorageBackend.MEMORY)

    # Neo4j connection settings
    neo4j_uri: str | None = Field(default=None)
    neo4j_username: str | None = Field(default=None)
    neo4j_password: str | None = Field(default=None)
    neo4j_database: str = Field(default="neo4j")

    # File storage settings
    file_storage_path: str | None = Field(default="./memory_graphs/")

    # Graph construction settings
    strict_mode: bool = Field(default=False)
    extract_properties: bool = Field(default=True)
    confidence_threshold: float = Field(default=0.7)

    # Memory integration settings
    include_temporal_info: bool = Field(default=True)
    include_importance_weights: bool = Field(default=True)
    include_source_tracking: bool = Field(default=True)


class GraphDatabaseConnector:
    """Abstract connector for graph databases."""

    def __init__(self, config: KGMemoryConfig):
        """Initialize connector with configuration."""
        self.config = config
        self.backend = config.storage_backend
        self._connection = None

    async def connect(self) -> None:
        """Connect to graph database."""
        if self.backend == GraphStorageBackend.NEO4J:
            await self._connect_neo4j()
        elif self.backend == GraphStorageBackend.MEMORY:
            self._connection = {"type": "memory", "graphs": {}}
        elif self.backend == GraphStorageBackend.FILE:
            await self._connect_file_storage()
        else:
            logger.warning(f"Backend {self.backend} not implemented, using memory")
            self._connection = {"type": "memory", "graphs": {}}

    async def _connect_neo4j(self) -> None:
        """Connect to Neo4j database."""
        try:
            from neo4j import AsyncGraphDatabase

            if not all(
                [
                    self.config.neo4j_uri,
                    self.config.neo4j_username,
                    self.config.neo4j_password,
                ]
            ):
                raise ValueError("Neo4j connection details missing")

            driver = AsyncGraphDatabase.driver(
                self.config.neo4j_uri,
                auth=(self.config.neo4j_username, self.config.neo4j_password),
            )

            # Test connection
            async with driver.session(database=self.config.neo4j_database) as session:
                await session.run("RETURN 1")

            self._connection = {
                "type": "neo4j",
                "driver": driver,
                "database": self.config.neo4j_database,
            }
            logger.info(f"Connected to Neo4j at {self.config.neo4j_uri}")

        except ImportError:
            logger.error("Neo4j driver not available. Install with: pip install neo4j")
            raise
        except Exception as e:
            logger.error(f"Failed to connect to Neo4j: {e}")
            raise

    async def _connect_file_storage(self) -> None:
        """Initialize file-based storage."""
        import os

        storage_path = self.config.file_storage_path or "./memory_graphs/"
        os.makedirs(storage_path, exist_ok=True)

        self._connection = {"type": "file", "path": storage_path, "graphs": {}}
        logger.info(f"Initialized file storage at {storage_path}")

    async def store_knowledge_graph(
        self, graph: KnowledgeGraph, graph_id: str, metadata: dict[str, Any] = None
    ) -> bool:
        """Store knowledge graph in configured backend."""
        if not self._connection:
            await self.connect()

        try:
            if self._connection["type"] == "neo4j":
                return await self._store_neo4j(graph, graph_id, metadata)
            if self._connection["type"] == "memory":
                return await self._store_memory(graph, graph_id, metadata)
            if self._connection["type"] == "file":
                return await self._store_file(graph, graph_id, metadata)
            logger.error(f"Unknown connection type: {self._connection['type']}")
            return False

        except Exception as e:
            logger.error(f"Failed to store graph {graph_id}: {e}")
            return False

    async def _store_neo4j(
        self, graph: KnowledgeGraph, graph_id: str, metadata: dict[str, Any]
    ) -> bool:
        """Store graph in Neo4j."""
        driver = self._connection["driver"]
        database = self._connection["database"]

        async with driver.session(database=database) as session:
            # Create nodes
            for node in graph.nodes:
                cypher = """
                MERGE (n:Entity {id: $id})
                SET n.type = $type,
                    n.graph_id = $graph_id,
                    n.created_at = datetime(),
                    n += $properties
                """

                await session.run(
                    cypher,
                    {
                        "id": node.id,
                        "type": node.type,
                        "graph_id": graph_id,
                        "properties": node.properties,
                    },
                )

            # Create relationships
            for rel in graph.relationships:
                cypher = """
                MATCH (a:Entity {id: $source_id}), (b:Entity {id: $target_id})
                MERGE (a)-[r:RELATES {type: $rel_type}]->(b)
                SET r.graph_id = $graph_id,
                    r.confidence = $confidence,
                    r.created_at = datetime(),
                    r += $properties
                """

                await session.run(
                    cypher,
                    {
                        "source_id": rel.source,
                        "target_id": rel.target,
                        "rel_type": rel.type,
                        "graph_id": graph_id,
                        "confidence": rel.confidence_score,
                        "properties": rel.properties,
                    },
                )

            # Store graph metadata
            if metadata:
                cypher = """
                MERGE (g:GraphMetadata {id: $graph_id})
                SET g += $metadata, g.updated_at = datetime()
                """
                await session.run(cypher, {"graph_id": graph_id, "metadata": metadata})

        logger.info(
            f"Stored graph {graph_id} in Neo4j: {len(graph.nodes)} nodes, {len(graph.relationships)} relationships"
        )
        return True

    async def _store_memory(
        self, graph: KnowledgeGraph, graph_id: str, metadata: dict[str, Any]
    ) -> bool:
        """Store graph in memory."""
        self._connection["graphs"][graph_id] = {
            "graph": graph,
            "metadata": metadata,
            "created_at": datetime.now().isoformat(),
        }

        logger.info(
            f"Stored graph {graph_id} in memory: {len(graph.nodes)} nodes, {len(graph.relationships)} relationships"
        )
        return True

    async def _store_file(
        self, graph: KnowledgeGraph, graph_id: str, metadata: dict[str, Any]
    ) -> bool:
        """Store graph in file."""
        import json
        import os

        file_path = os.path.join(self._connection["path"], f"{graph_id}.json")

        # Convert graph to serializable format
        graph_data = {
            "graph_id": graph_id,
            "metadata": metadata or {},
            "created_at": datetime.now().isoformat(),
            "nodes": [
                {"id": node.id, "type": node.type, "properties": node.properties}
                for node in graph.nodes
            ],
            "relationships": [
                {
                    "source": rel.source,
                    "target": rel.target,
                    "type": rel.type,
                    "confidence": rel.confidence_score,
                    "properties": rel.properties,
                    "supporting_evidence": rel.supporting_evidence,
                }
                for rel in graph.relationships
            ],
        }

        with open(file_path, "w") as f:
            json.dump(graph_data, f, indent=2)

        logger.info(f"Stored graph {graph_id} to file {file_path}")
        return True

    async def retrieve_graph(
        self, graph_id: str
    ) -> tuple[KnowledgeGraph, dict[str, Any]] | None:
        """Retrieve knowledge graph by ID."""
        if not self._connection:
            await self.connect()

        try:
            if self._connection["type"] == "memory":
                graph_data = self._connection["graphs"].get(graph_id)
                if graph_data:
                    return graph_data["graph"], graph_data["metadata"]

            elif self._connection["type"] == "file":
                import json
                import os

                file_path = os.path.join(self._connection["path"], f"{graph_id}.json")
                if os.path.exists(file_path):
                    with open(file_path) as f:
                        graph_data = json.load(f)

                    # Reconstruct graph
                    graph = KnowledgeGraph()

                    for node_data in graph_data["nodes"]:
                        node = EntityNode(
                            id=node_data["id"],
                            type=node_data["type"],
                            properties=node_data["properties"],
                        )
                        graph.add_node(node)

                    for rel_data in graph_data["relationships"]:
                        rel = EntityRelationship(
                            source=rel_data["source"],
                            target=rel_data["target"],
                            type=rel_data["type"],
                            confidence_score=rel_data["confidence"],
                            properties=rel_data["properties"],
                            supporting_evidence=rel_data.get("supporting_evidence"),
                        )
                        graph.add_relationship(rel)

                    return graph, graph_data["metadata"]

            # Neo4j retrieval would go here

        except Exception as e:
            logger.error(f"Failed to retrieve graph {graph_id}: {e}")

        return None

    async def close(self) -> None:
        """Close database connection."""
        if self._connection and self._connection.get("type") == "neo4j":
            driver = self._connection.get("driver")
            if driver:
                await driver.close()


class KGMemoryAgent:
    """Knowledge Graph Memory Agent with database integration."""

    def __init__(self, config: KGMemoryConfig):
        """Initialize KG Memory Agent."""
        self.config = config
        self.graph_transformer = GraphTransformer()
        self.db_connector = GraphDatabaseConnector(config)
        self.message_converter = MessageDocumentConverter()

        logger.info(f"Initialized KGMemoryAgent with backend: {config.storage_backend}")

    async def setup(self) -> None:
        """Setup agent and connections."""
        await self.db_connector.connect()

    async def process_memories_to_graph(
        self, memories: list[EnhancedMemoryItem], graph_id: str | None = None
    ) -> tuple[str, KnowledgeGraph]:
        """Process memories into knowledge graph and store.

        Args:
            memories: List of memory items to process
            graph_id: Optional graph ID (generated if not provided)

        Returns:
            Tuple of (graph_id, knowledge_graph)
        """
        if graph_id is None:
            graph_id = f"memory_graph_{uuid4()}"

        # Convert memories to documents
        documents = []
        for memory in memories:
            doc = Document(
                page_content=memory.content,
                metadata={
                    "memory_id": memory.id,
                    "memory_type": memory.memory_type.value,
                    "importance": memory.importance.value,
                    "confidence": memory.confidence,
                    "tags": memory.tags,
                    "created_at": memory.created_at.isoformat(),
                    "source": memory.source,
                },
            )
            documents.append(doc)

        # Transform to knowledge graph
        try:
            graph_docs = await self.graph_transformer.atransform_documents(
                documents=documents,
                allowed_nodes=self.config.memory_node_types,
                allowed_relationships=self.config.memory_relationships,
                strict_mode=self.config.strict_mode,
                node_properties=self.config.extract_properties,
                relationship_properties=self.config.extract_properties,
            )

            # Build unified knowledge graph
            unified_graph = KnowledgeGraph()

            for doc in graph_docs:
                for node in doc.nodes:
                    entity_node = EntityNode.from_graph_node(node)
                    unified_graph.add_node(entity_node)

                for rel in doc.relationships:
                    entity_rel = EntityRelationship.from_graph_relationship(
                        rel, confidence_score=max(self.config.confidence_threshold, 0.8)
                    )
                    unified_graph.add_relationship(entity_rel)

            # Enhance with memory-specific metadata
            metadata = {
                "source": "memory_processing",
                "memory_count": len(memories),
                "memory_types": list(set(m.memory_type.value for m in memories)),
                "importance_levels": list(set(m.importance.value for m in memories)),
                "created_at": datetime.now().isoformat(),
                "confidence_threshold": self.config.confidence_threshold,
            }

            # Store in graph database
            success = await self.db_connector.store_knowledge_graph(
                unified_graph, graph_id, metadata
            )

            if success:
                logger.info(
                    f"Successfully processed {len(memories)} memories into graph {graph_id}"
                )
            else:
                logger.error(f"Failed to store graph {graph_id}")

            return graph_id, unified_graph

        except Exception as e:
            logger.error(f"Failed to process memories to graph: {e}")
            raise

    async def process_conversation_to_graph(
        self, messages: list[BaseMessage], graph_id: str | None = None
    ) -> tuple[str, KnowledgeGraph]:
        """Process conversation messages into knowledge graph.

        Args:
            messages: Conversation messages
            graph_id: Optional graph ID

        Returns:
            Tuple of (graph_id, knowledge_graph)
        """
        if graph_id is None:
            graph_id = f"conversation_graph_{uuid4()}"

        # Convert messages to timestamped documents
        timestamped_docs = self.message_converter.convert_messages(messages)

        # Convert to regular documents for graph transformer
        documents = []
        for ts_doc in timestamped_docs:
            doc = Document(page_content=ts_doc.page_content, metadata=ts_doc.metadata)
            documents.append(doc)

        # Process similar to memories
        try:
            graph_docs = await self.graph_transformer.atransform_documents(
                documents=documents,
                allowed_nodes=self.config.memory_node_types,
                allowed_relationships=self.config.memory_relationships,
                strict_mode=self.config.strict_mode,
            )

            # Build unified graph
            unified_graph = KnowledgeGraph()

            for doc in graph_docs:
                for node in doc.nodes:
                    entity_node = EntityNode.from_graph_node(node)
                    unified_graph.add_node(entity_node)

                for rel in doc.relationships:
                    entity_rel = EntityRelationship.from_graph_relationship(rel)
                    unified_graph.add_relationship(entity_rel)

            # Store with conversation metadata
            metadata = {
                "source": "conversation_processing",
                "message_count": len(messages),
                "conversation_id": self.message_converter.conversation_id,
                "session_id": self.message_converter.session_id,
                "created_at": datetime.now().isoformat(),
            }

            await self.db_connector.store_knowledge_graph(
                unified_graph, graph_id, metadata
            )

            logger.info(
                f"Processed conversation ({len(messages)} messages) into graph {graph_id}"
            )

            return graph_id, unified_graph

        except Exception as e:
            logger.error(f"Failed to process conversation to graph: {e}")
            raise

    async def retrieve_memory_graph(self, graph_id: str) -> KnowledgeGraph | None:
        """Retrieve stored knowledge graph.

        Args:
            graph_id: ID of graph to retrieve

        Returns:
            KnowledgeGraph if found, None otherwise
        """
        result = await self.db_connector.retrieve_graph(graph_id)
        if result:
            graph, metadata = result
            logger.info(
                f"Retrieved graph {graph_id}: {len(graph.nodes)} nodes, {len(graph.relationships)} relationships"
            )
            return graph
        return None

    async def query_graph_by_entity(self, entity_name: str) -> list[dict[str, Any]]:
        """Query graph database for entity and its relationships.

        Args:
            entity_name: Name of entity to query

        Returns:
            List of related entities and relationships
        """
        if (
            self.db_connector._connection
            and self.db_connector._connection["type"] == "neo4j"
        ):
            return await self._query_neo4j_entity(entity_name)
        if (
            self.db_connector._connection
            and self.db_connector._connection["type"] == "memory"
        ):
            return await self._query_memory_entity(entity_name)
        logger.warning("Graph querying not implemented for current backend")
        return []

    async def _query_neo4j_entity(self, entity_name: str) -> list[dict[str, Any]]:
        """Query Neo4j for entity relationships."""
        driver = self.db_connector._connection["driver"]
        database = self.db_connector._connection["database"]

        results = []

        async with driver.session(database=database) as session:
            # Find entity and its relationships
            cypher = """
            MATCH (e:Entity {id: $entity_name})
            OPTIONAL MATCH (e)-[r]-(connected)
            RETURN e, r, connected
            LIMIT 50
            """

            result = await session.run(cypher, {"entity_name": entity_name})

            async for record in result:
                entity = record["e"]
                relationship = record["r"]
                connected = record["connected"]

                if entity:
                    results.append(
                        {
                            "entity": dict(entity),
                            "relationship": (
                                dict(relationship) if relationship else None
                            ),
                            "connected": dict(connected) if connected else None,
                        }
                    )

        return results

    async def _query_memory_entity(self, entity_name: str) -> list[dict[str, Any]]:
        """Query memory storage for entity relationships."""
        results = []

        for graph_id, graph_data in self.db_connector._connection["graphs"].items():
            graph = graph_data["graph"]

            # Find matching nodes
            for node in graph.nodes:
                if entity_name.lower() in node.id.lower():
                    # Find relationships for this node
                    related_rels = [
                        rel
                        for rel in graph.relationships
                        if rel.source == node.id or rel.target == node.id
                    ]

                    results.append(
                        {
                            "graph_id": graph_id,
                            "entity": {
                                "id": node.id,
                                "type": node.type,
                                "properties": node.properties,
                            },
                            "relationships": [
                                {
                                    "source": rel.source,
                                    "target": rel.target,
                                    "type": rel.type,
                                    "confidence": rel.confidence_score,
                                }
                                for rel in related_rels
                            ],
                        }
                    )

        return results

    async def close(self) -> None:
        """Close agent and database connections."""
        await self.db_connector.close()


# ============================================================================
# FACTORY FUNCTIONS
# ============================================================================


def create_memory_kg_agent(
    storage_backend: str = "memory", llm_config: AugLLMConfig = None, **storage_kwargs
) -> KGMemoryAgent:
    """Factory function to create KG Memory Agent.

    Args:
        storage_backend: "memory", "neo4j", "file"
        llm_config: LLM configuration
        **storage_kwargs: Backend-specific settings

    Returns:
        Configured KGMemoryAgent
    """
    if llm_config is None:
        llm_config = AugLLMConfig()

    config = KGMemoryConfig(
        llm_config=llm_config,
        storage_backend=GraphStorageBackend(storage_backend),
        **storage_kwargs,
    )

    return KGMemoryAgent(config)


def create_neo4j_memory_agent(
    uri: str,
    username: str,
    password: str,
    database: str = "neo4j",
    llm_config: AugLLMConfig = None,
) -> KGMemoryAgent:
    """Create KG Memory Agent with Neo4j backend.

    Args:
        uri: Neo4j connection URI
        username: Database username
        password: Database password
        database: Database name
        llm_config: LLM configuration

    Returns:
        KGMemoryAgent configured for Neo4j
    """
    config = KGMemoryConfig(
        llm_config=llm_config or AugLLMConfig(),
        storage_backend=GraphStorageBackend.NEO4J,
        neo4j_uri=uri,
        neo4j_username=username,
        neo4j_password=password,
        neo4j_database=database,
    )

    return KGMemoryAgent(config)
