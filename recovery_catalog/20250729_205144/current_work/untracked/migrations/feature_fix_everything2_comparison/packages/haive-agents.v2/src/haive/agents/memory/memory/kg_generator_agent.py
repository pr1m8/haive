"""Knowledge Graph Generator Agent for Memory System.

This agent specializes in extracting and maintaining knowledge graphs from memories,
building entity relationships and semantic connections across the memory system.
"""

import logging
from datetime import datetime
from typing import Any

from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, ConfigDict, Field

from haive.agents.document_modifiers.kg.kg_base.models import GraphTransformer
from haive.agents.memory.core.classifier import MemoryClassifier
from haive.agents.memory.core.stores import MemoryStoreManager
from haive.agents.memory.core.types import MemoryType
from haive.agents.simple.agent import SimpleAgent

logger = logging.getLogger(__name__)


class KnowledgeGraphNode(BaseModel):
    """Represents a node (entity) in the knowledge graph.

    A knowledge graph node encapsulates an entity extracted from memory content,
    including its type, properties, and references to the memories that mention it.

    Attributes:
        id: Unique identifier for the node, typically generated from name and type
        type: Entity type classification (person, organization, concept, etc.)
        name: Human-readable display name of the entity
        properties: Dictionary of additional properties and attributes
        memory_references: List of memory IDs that reference this entity
        confidence: Confidence score in entity existence and accuracy (0.0-1.0)
        created_at: UTC timestamp when the entity was first created
        last_updated: UTC timestamp of the last update to this entity

    Examples:
        Creating a person entity::

            person = KnowledgeGraphNode(
                id="person_alice_smith",
                type="person",
                name="Alice Smith",
                properties={"role": "engineer", "company": "TechCorp"},
                memory_references=["mem_123", "mem_456"],
                confidence=0.95
            )

        Creating a concept entity::

            concept = KnowledgeGraphNode(
                id="concept_machine_learning",
                type="concept",
                name="Machine Learning",
                properties={"category": "technology", "complexity": "high"},
                confidence=0.9
            )
    """

    id: str = Field(..., description="Unique node identifier")
    type: str = Field(..., description="Entity type (person, place, concept, etc.)")
    name: str = Field(..., description="Display name of the entity")
    properties: dict[str, Any] = Field(
        default_factory=dict, description="Node properties"
    )
    memory_references: list[str] = Field(
        default_factory=list, description="Memory IDs that reference this entity"
    )
    confidence: float = Field(
        default=1.0, ge=0.0, le=1.0, description="Confidence in entity existence"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow, description="Creation timestamp"
    )
    last_updated: datetime = Field(
        default_factory=datetime.utcnow, description="Last update timestamp"
    )


class KnowledgeGraphRelationship(BaseModel):
    """Represents a relationship (edge) in the knowledge graph.

    A knowledge graph relationship connects two entities with a typed relationship,
    capturing semantic connections discovered from memory content.

    Attributes:
        id: Unique identifier for the relationship, typically generated from source, target, and type
        source_id: ID of the source entity in the relationship
        target_id: ID of the target entity in the relationship
        relationship_type: Type of relationship (works_at, knows, uses, etc.)
        properties: Dictionary of additional relationship properties
        memory_references: List of memory IDs that reference this relationship
        confidence: Confidence score in relationship existence and accuracy (0.0-1.0)
        created_at: UTC timestamp when the relationship was first created
        last_updated: UTC timestamp of the last update to this relationship

    Examples:
        Creating a work relationship::

            work_rel = KnowledgeGraphRelationship(
                id="person_alice_smith_works_at_organization_techcorp",
                source_id="person_alice_smith",
                target_id="organization_techcorp",
                relationship_type="works_at",
                properties={"role": "senior_engineer", "start_date": "2020-01-15"},
                memory_references=["mem_123"],
                confidence=0.9
            )

        Creating a knowledge relationship::

            knows_rel = KnowledgeGraphRelationship(
                id="person_alice_smith_knows_concept_machine_learning",
                source_id="person_alice_smith",
                target_id="concept_machine_learning",
                relationship_type="knows",
                properties={"proficiency": "expert", "years_experience": 5},
                confidence=0.85
            )
    """

    id: str = Field(..., description="Unique relationship identifier")
    source_id: str = Field(..., description="Source entity ID")
    target_id: str = Field(..., description="Target entity ID")
    relationship_type: str = Field(..., description="Type of relationship")
    properties: dict[str, Any] = Field(
        default_factory=dict, description="Relationship properties"
    )
    memory_references: list[str] = Field(
        default_factory=list, description="Memory IDs that reference this relationship"
    )
    confidence: float = Field(
        default=1.0, ge=0.0, le=1.0, description="Confidence in relationship"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow, description="Creation timestamp"
    )
    last_updated: datetime = Field(
        default_factory=datetime.utcnow, description="Last update timestamp"
    )


class MemoryKnowledgeGraph(BaseModel):
    """Complete knowledge graph structure extracted from memory system.

    The MemoryKnowledgeGraph represents a comprehensive knowledge graph built from
    memory content, containing entities (nodes) and their relationships (edges).
    It provides methods for managing the graph structure and querying entity neighborhoods.

    Attributes:
        nodes: Dictionary mapping node IDs to KnowledgeGraphNode objects
        relationships: Dictionary mapping relationship IDs to KnowledgeGraphRelationship objects
        metadata: Dictionary containing graph-level metadata and statistics

    Examples:
        Creating and populating a knowledge graph::

            graph = MemoryKnowledgeGraph()

            # Add entities
            person = KnowledgeGraphNode(
                id="person_alice", type="person", name="Alice Smith"
            )
            company = KnowledgeGraphNode(
                id="org_techcorp", type="organization", name="TechCorp"
            )

            graph.add_node(person)
            graph.add_node(company)

            # Add relationship
            works_at = KnowledgeGraphRelationship(
                id="alice_works_at_techcorp",
                source_id="person_alice",
                target_id="org_techcorp",
                relationship_type="works_at"
            )

            graph.add_relationship(works_at)

        Querying the graph::

            # Get connected nodes
            connected = graph.get_connected_nodes("person_alice")

            # Get all relationships for a node
            relationships = graph.get_relationships_for_node("person_alice")
    """

    nodes: dict[str, KnowledgeGraphNode] = Field(
        default_factory=dict, description="Graph nodes by ID"
    )
    relationships: dict[str, KnowledgeGraphRelationship] = Field(
        default_factory=dict, description="Graph relationships by ID"
    )
    metadata: dict[str, Any] = Field(default_factory=dict, description="Graph metadata")

    def add_node(self, node: KnowledgeGraphNode) -> None:
        """Add or update a node in the graph.

        If the node already exists, its properties and memory references are merged
        with the existing node. Otherwise, a new node is added to the graph.

        Args:
            node: The KnowledgeGraphNode to add or update

        Examples:
            Adding a new node::

                graph = MemoryKnowledgeGraph()
                node = KnowledgeGraphNode(
                    id="person_alice", type="person", name="Alice Smith"
                )
                graph.add_node(node)

            Updating an existing node::

                # First addition
                node1 = KnowledgeGraphNode(
                    id="person_alice", type="person", name="Alice Smith",
                    properties={"role": "engineer"}
                )
                graph.add_node(node1)

                # Update with additional properties
                node2 = KnowledgeGraphNode(
                    id="person_alice", type="person", name="Alice Smith",
                    properties={"company": "TechCorp"}
                )
                graph.add_node(node2)
                # Result: node has both "role" and "company" properties
        """
        if node.id in self.nodes:
            # Update existing node
            existing = self.nodes[node.id]
            existing.properties.update(node.properties)
            existing.memory_references.extend(node.memory_references)
            existing.memory_references = list(
                set(existing.memory_references)
            )  # Remove duplicates
            existing.last_updated = datetime.utcnow()
        else:
            # Add new node
            self.nodes[node.id] = node

    def add_relationship(self, relationship: KnowledgeGraphRelationship) -> None:
        """Add or update a relationship in the graph.

        If the relationship already exists, its properties and memory references are merged
        with the existing relationship. Otherwise, a new relationship is added to the graph.

        Args:
            relationship: The KnowledgeGraphRelationship to add or update

        Examples:
            Adding a new relationship::

                graph = MemoryKnowledgeGraph()
                rel = KnowledgeGraphRelationship(
                    id="alice_works_at_techcorp",
                    source_id="person_alice",
                    target_id="org_techcorp",
                    relationship_type="works_at"
                )
                graph.add_relationship(rel)

            Updating an existing relationship::

                # First addition
                rel1 = KnowledgeGraphRelationship(
                    id="alice_works_at_techcorp",
                    source_id="person_alice",
                    target_id="org_techcorp",
                    relationship_type="works_at",
                    properties={"role": "engineer"}
                )
                graph.add_relationship(rel1)

                # Update with additional properties
                rel2 = KnowledgeGraphRelationship(
                    id="alice_works_at_techcorp",
                    source_id="person_alice",
                    target_id="org_techcorp",
                    relationship_type="works_at",
                    properties={"start_date": "2020-01-15"}
                )
                graph.add_relationship(rel2)
                # Result: relationship has both "role" and "start_date" properties
        """
        if relationship.id in self.relationships:
            # Update existing relationship
            existing = self.relationships[relationship.id]
            existing.properties.update(relationship.properties)
            existing.memory_references.extend(relationship.memory_references)
            existing.memory_references = list(
                set(existing.memory_references)
            )  # Remove duplicates
            existing.last_updated = datetime.utcnow()
        else:
            # Add new relationship
            self.relationships[relationship.id] = relationship

    def get_connected_nodes(self, node_id: str) -> list[KnowledgeGraphNode]:
        """Get all nodes connected to a given node.

        Traverses all relationships to find nodes that are directly connected
        to the specified node, regardless of relationship direction.

        Args:
            node_id: The ID of the node to find connections for

        Returns:
            List of KnowledgeGraphNode objects connected to the specified node

        Examples:
            Finding connected nodes::

                graph = MemoryKnowledgeGraph()
                # Assume graph has been populated with nodes and relationships

                connected = graph.get_connected_nodes("person_alice")
                for node in connected:
                    print(f"Connected to: {node.name} ({node.type})")
        """
        connected = []
        for rel in self.relationships.values():
            if rel.source_id == node_id and rel.target_id in self.nodes:
                connected.append(self.nodes[rel.target_id])
            elif rel.target_id == node_id and rel.source_id in self.nodes:
                connected.append(self.nodes[rel.source_id])
        return connected

    def get_relationships_for_node(
        self, node_id: str
    ) -> list[KnowledgeGraphRelationship]:
        """Get all relationships involving a given node.

        Finds all relationships where the specified node is either the source
        or target of the relationship.

        Args:
            node_id: The ID of the node to find relationships for

        Returns:
            List of KnowledgeGraphRelationship objects involving the specified node

        Examples:
            Finding node relationships::

                graph = MemoryKnowledgeGraph()
                # Assume graph has been populated

                relationships = graph.get_relationships_for_node("person_alice")
                for rel in relationships:
                    print(f"Relationship: {rel.relationship_type} "
                          f"({rel.source_id} -> {rel.target_id})")
        """
        return [
            rel
            for rel in self.relationships.values()
            if node_id in (rel.source_id, rel.target_id)
        ]


class KGGeneratorAgentConfig(BaseModel):
    """Configuration for Knowledge Graph Generator Agent.

    This configuration class defines all parameters needed to create and configure
    a KGGeneratorAgent, including LLM settings, extraction parameters, and entity/relationship
    type specifications.

    Attributes:
        name: Unique identifier for the agent instance
        memory_store_manager: Manager for memory storage and retrieval operations
        memory_classifier: Classifier for analyzing memory content and types
        engine: LLM engine configuration for entity and relationship extraction
        extract_batch_size: Number of memories to process in each batch
        min_confidence_threshold: Minimum confidence score for extracted entities/relationships
        enable_iterative_refinement: Whether to enable iterative graph refinement
        entity_types: List of entity types the agent should extract
        relationship_types: List of relationship types the agent should extract

    Examples:
        Basic configuration::

            config = KGGeneratorAgentConfig(
                name="my_kg_generator",
                memory_store_manager=store_manager,
                memory_classifier=classifier,
                engine=AugLLMConfig(temperature=0.1),
                extract_batch_size=20,
                min_confidence_threshold=0.7
            )

        Advanced configuration with custom types::

            config = KGGeneratorAgentConfig(
                name="custom_kg_generator",
                memory_store_manager=store_manager,
                memory_classifier=classifier,
                engine=AugLLMConfig(
                    model="gpt-4",
                    temperature=0.1,
                    max_tokens=2000
                ),
                extract_batch_size=15,
                min_confidence_threshold=0.8,
                entity_types=[
                    "person", "organization", "technology", "concept",
                    "project", "skill", "tool", "document"
                ],
                relationship_types=[
                    "works_at", "knows", "uses", "creates", "manages",
                    "collaborates_with", "depends_on", "teaches"
                ]
            )
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    name: str = Field(default="kg_generator", description="Agent name")
    memory_store_manager: MemoryStoreManager = Field(
        ..., description="Memory store manager"
    )
    memory_classifier: MemoryClassifier = Field(..., description="Memory classifier")
    engine: AugLLMConfig = Field(
        default_factory=AugLLMConfig, description="LLM engine for extraction"
    )

    # KG extraction configuration
    extract_batch_size: int = Field(
        default=10, description="Number of memories to process in batch"
    )
    min_confidence_threshold: float = Field(
        default=0.6, description="Minimum confidence for entities/relationships"
    )
    enable_iterative_refinement: bool = Field(
        default=True, description="Enable iterative graph refinement"
    )

    # Entity extraction configuration
    entity_types: list[str] = Field(
        default_factory=lambda: [
            "person",
            "organization",
            "location",
            "concept",
            "event",
            "technology",
            "product",
            "service",
            "skill",
            "tool",
            "document",
            "project",
        ],
        description="Types of entities to extract",
    )

    # Relationship types
    relationship_types: list[str] = Field(
        default_factory=lambda: [
            "knows",
            "works_at",
            "located_in",
            "part_of",
            "related_to",
            "created_by",
            "uses",
            "depends_on",
            "collaborates_with",
            "manages",
            "teaches",
            "learns_from",
            "similar_to",
            "opposite_of",
            "causes",
            "prevents",
            "enables",
        ],
        description="Types of relationships to extract",
    )


class KGGeneratorAgent(SimpleAgent):
    """Agent specializing in knowledge graph generation from memory system.

    The KGGeneratorAgent is a specialized memory agent that extracts entities and relationships
    from memory content to build comprehensive knowledge graphs. It uses LLM-powered extraction
    to identify semantic structures and connections across memories.

    This agent extends SimpleAgent with knowledge graph capabilities, providing methods for:
    - Entity extraction with confidence scoring
    - Relationship discovery between entities
    - Incremental graph building and updates
    - Entity neighborhood exploration
    - Graph-based memory analysis

    Attributes:
        memory_store: Manager for memory storage and retrieval operations
        classifier: Classifier for analyzing memory content and types
        knowledge_graph: The maintained knowledge graph structure
        graph_transformer: Transformer for graph processing operations
        extract_batch_size: Number of memories to process in each batch
        min_confidence_threshold: Minimum confidence score for extracted entities/relationships
        enable_iterative_refinement: Whether to enable iterative graph refinement
        entity_types: List of entity types the agent should extract
        relationship_types: List of relationship types the agent should extract
        entity_extraction_prompt: Prompt template for entity extraction
        relationship_extraction_prompt: Prompt template for relationship extraction

    Examples:
        Basic usage::

            # Create configuration
            config = KGGeneratorAgentConfig(
                memory_store_manager=store_manager,
                memory_classifier=classifier,
                engine=AugLLMConfig(temperature=0.1)
            )

            # Create agent
            kg_agent = KGGeneratorAgent(config)

            # Extract knowledge graph from memories
            graph = await kg_agent.extract_knowledge_graph_from_memories()
            print(f"Extracted {len(graph.nodes)} entities and {len(graph.relationships)} relationships")

        Entity extraction::

            # Extract entities with limit
            entities = await kg_agent.extract_entities_from_memories(limit=10)

            for entity in entities:
                print(f"Entity: {entity.name} ({entity.type}) - Confidence: {entity.confidence}")

        Relationship extraction::

            # Extract relationships
            relationships = await kg_agent.extract_relationships_from_memories(limit=10)

            for rel in relationships:
                print(f"Relationship: {rel.relationship_type} "
                      f"({rel.source_id} -> {rel.target_id})")

        Entity exploration::

            # Get entity context with neighborhood
            context = await kg_agent.get_entity_context("Python")

            if "entity" in context:
                entity = context["entity"]
                neighborhood = context["neighborhood"]
                print(f"Entity: {entity.name}")
                print(f"Connected nodes: {neighborhood['total_nodes']}")
                print(f"Relationships: {neighborhood['total_relationships']}")

        Agent execution::

            # Use agent for interactive queries
            response = await kg_agent.run("Extract knowledge graph from recent memories")
            print(response)

            # Get graph statistics
            stats = await kg_agent.run("Show me graph statistics")
            print(stats)
    """

    # KG-specific fields
    memory_store: MemoryStoreManager = Field(..., description="Memory store manager")
    classifier: MemoryClassifier = Field(..., description="Memory classifier")
    knowledge_graph: MemoryKnowledgeGraph = Field(
        default_factory=MemoryKnowledgeGraph, description="Knowledge graph"
    )
    graph_transformer: GraphTransformer = Field(
        default_factory=GraphTransformer, description="Graph transformer"
    )

    # Configuration
    extract_batch_size: int = Field(
        default=10, description="Number of memories to process in batch"
    )
    min_confidence_threshold: float = Field(
        default=0.6, description="Minimum confidence for entities/relationships"
    )
    enable_iterative_refinement: bool = Field(
        default=True, description="Enable iterative graph refinement"
    )
    entity_types: list[str] = Field(
        default_factory=lambda: [
            "person",
            "organization",
            "location",
            "concept",
            "event",
            "technology",
            "product",
            "service",
            "skill",
            "tool",
            "document",
            "project",
        ],
        description="Types of entities to extract",
    )
    relationship_types: list[str] = Field(
        default_factory=lambda: [
            "knows",
            "works_at",
            "located_in",
            "part_of",
            "related_to",
            "created_by",
            "uses",
            "depends_on",
            "collaborates_with",
            "manages",
            "teaches",
            "learns_from",
            "similar_to",
            "opposite_of",
            "causes",
            "prevents",
            "enables",
        ],
        description="Types of relationships to extract",
    )

    # Prompt fields
    entity_extraction_prompt: PromptTemplate = Field(
        default=None, description="Entity extraction prompt"
    )
    relationship_extraction_prompt: PromptTemplate = Field(
        default=None, description="Relationship extraction prompt"
    )

    # Configuration setup - Pydantic handles initialization
    model_config = ConfigDict(arbitrary_types_allowed=True, validate_assignment=True)

    def setup_agent(self) -> None:
        """Setup agent after initialization - Pydantic pattern."""
        # Call parent setup
        super().setup_agent()

        # Setup prompts if not already configured
        if not self.entity_extraction_prompt:
            self._setup_prompts()

    def _setup_prompts(self) -> None:
        """Setup prompts for entity and relationship extraction."""
        self.entity_extraction_prompt = PromptTemplate(
            template="""You are an expert knowledge graph entity extractor. Extract entities from the given memory content.

ENTITY TYPES TO EXTRACT:
{entity_types}

MEMORY CONTENT:
{memory_content}

MEMORY METADATA:
- Memory Types: {memory_types}
- Topics: {topics}
- Entities (from classification): {existing_entities}

EXTRACTION RULES:
1. Extract only meaningful entities that represent concrete things, people, concepts, or places
2. Assign appropriate entity types from the provided list
3. Provide confidence scores (0.0-1.0) based on clarity and importance
4. Include key properties that describe the entity
5. Focus on entities that are likely to appear in multiple memories or be referenced later

FORMAT: Return a JSON list of entities with structure:
{{
    "entities": [
        {{
            "name": "entity_name",
            "type": "entity_type",
            "properties": {{"key": "value"}},
            "confidence": 0.95
        }}
    ]
}}

Extract entities now:""",
            input_variables=[
                "memory_content",
                "memory_types",
                "topics",
                "existing_entities",
                "entity_types",
            ],
        )

        self.relationship_extraction_prompt = PromptTemplate(
            template="""You are an expert knowledge graph relationship extractor. Extract relationships between entities from the given memory content.

KNOWN ENTITIES:
{known_entities}

RELATIONSHIP TYPES TO EXTRACT:
{relationship_types}

MEMORY CONTENT:
{memory_content}

EXISTING RELATIONSHIPS (from memory metadata):
{existing_relationships}

EXTRACTION RULES:
1. Extract only relationships between entities that are clearly mentioned in the content
2. Use relationship types from the provided list
3. Provide confidence scores (0.0-1.0) based on clarity and strength of connection
4. Include properties that describe the relationship (e.g., time, context, strength)
5. Focus on relationships that provide meaningful semantic connections

FORMAT: Return a JSON list of relationships with structure:
{{
    "relationships": [
        {{
            "source_entity": "entity_1",
            "target_entity": "entity_2",
            "relationship_type": "relationship_type",
            "properties": {{"key": "value"}},
            "confidence": 0.9
        }}
    ]
}}

Extract relationships now:""",
            input_variables=[
                "memory_content",
                "known_entities",
                "existing_relationships",
                "relationship_types",
            ],
        )

    async def extract_knowledge_graph_from_memories(
        self,
        memory_ids: list[str] | None = None,
        namespace: tuple[str, ...] | None = None,
        memory_types: list[MemoryType] | None = None,
    ) -> MemoryKnowledgeGraph:
        """Extract knowledge graph from specified memories.

        Processes memories to extract entities and relationships, building a comprehensive
        knowledge graph. Uses LLM-powered extraction to identify semantic structures
        and connections across memory content.

        Args:
            memory_ids: Specific memory IDs to process. If None, processes all memories
                in the specified namespace and types.
            namespace: Memory namespace to process. If None, processes all namespaces.
            memory_types: Specific memory types to process. If None, processes all types.

        Returns:
            Updated MemoryKnowledgeGraph containing extracted entities and relationships
            with metadata about the extraction process.

        Raises:
            ValueError: If no memories are found to process
            RuntimeError: If extraction fails due to LLM or processing errors

        Examples:
            Extract from all memories::

                # Extract from all memories
                graph = await kg_agent.extract_knowledge_graph_from_memories()
                print(f"Extracted {len(graph.nodes)} entities")
                print(f"Extracted {len(graph.relationships)} relationships")

            Extract from specific memories::

                # Extract from specific memory IDs
                memory_ids = ["mem_123", "mem_456", "mem_789"]
                graph = await kg_agent.extract_knowledge_graph_from_memories(
                    memory_ids=memory_ids
                )

            Extract from specific namespace::

                # Extract from user's personal memories
                graph = await kg_agent.extract_knowledge_graph_from_memories(
                    namespace=("user", "personal")
                )

            Extract from specific memory types::

                # Extract only from semantic and episodic memories
                graph = await kg_agent.extract_knowledge_graph_from_memories(
                    memory_types=[MemoryType.SEMANTIC, MemoryType.EPISODIC]
                )

        Note:
            The extraction process runs in batches (controlled by extract_batch_size)
            to manage memory usage and API rate limits. Progress is logged during
            processing.
        """
        try:
            # Get memories to process
            if memory_ids:
                memories = []
                for memory_id in memory_ids:
                    memory = await self.memory_store.get_memory_by_id(memory_id)
                    if memory:
                        memories.append(memory)
            else:
                # Get all memories from store
                memories = await self.memory_store.retrieve_memories(
                    query="",  # Empty query to get all
                    namespace=namespace,
                    memory_types=memory_types,
                    limit=1000,  # Large limit to get all
                )

            logger.info(f"Processing {len(memories)} memories for KG extraction")

            # Process memories in batches
            for i in range(0, len(memories), self.extract_batch_size):
                batch = memories[i : i + self.extract_batch_size]
                await self._process_memory_batch(batch)

            # Update graph metadata
            self.knowledge_graph.metadata.update(
                {
                    "last_updated": datetime.utcnow().isoformat(),
                    "total_memories_processed": len(memories),
                    "total_nodes": len(self.knowledge_graph.nodes),
                    "total_relationships": len(self.knowledge_graph.relationships),
                }
            )

            logger.info(
                f"KG extraction complete: {len(self.knowledge_graph.nodes)} nodes, {len(self.knowledge_graph.relationships)} relationships"
            )

            return self.knowledge_graph

        except Exception as e:
            logger.exception(f"Error extracting knowledge graph: {e}")
            raise

    async def _process_memory_batch(self, memories: list[dict[str, Any]]) -> None:
        """Process a batch of memories for entity and relationship extraction."""
        for memory in memories:
            try:
                await self._extract_entities_from_memory(memory)
                await self._extract_relationships_from_memory(memory)

            except Exception as e:
                logger.exception(
                    f"Error processing memory {memory.get('id', 'unknown')}: {e}"
                )
                continue

    async def _extract_entities_from_memory(self, memory: dict[str, Any]) -> None:
        """Extract entities from a single memory."""
        memory_content = memory.get("content", "")
        memory_id = memory.get("id", "")
        metadata = memory.get("metadata", {})

        # Prepare prompt inputs
        prompt_input = {
            "memory_content": memory_content,
            "memory_types": metadata.get("memory_types", []),
            "topics": metadata.get("topics", []),
            "existing_entities": metadata.get("entities", []),
            "entity_types": ", ".join(self.entity_types),
        }

        # Extract entities using LLM
        try:
            response = await self.llm.ainvoke(
                [
                    SystemMessage(
                        content="You are an expert knowledge graph entity extractor."
                    ),
                    HumanMessage(
                        content=self.entity_extraction_prompt.format(**prompt_input)
                    ),
                ]
            )

            # Parse response
            entities_data = self._parse_json_response(response.content)

            if entities_data and "entities" in entities_data:
                for entity_data in entities_data["entities"]:
                    # Create entity node
                    entity_id = self._generate_entity_id(
                        entity_data["name"], entity_data["type"]
                    )

                    entity_node = KnowledgeGraphNode(
                        id=entity_id,
                        type=entity_data["type"],
                        name=entity_data["name"],
                        properties=entity_data.get("properties", {}),
                        memory_references=[memory_id],
                        confidence=entity_data.get("confidence", 0.8),
                    )

                    # Add to graph
                    self.knowledge_graph.add_node(entity_node)

        except Exception as e:
            logger.exception(f"Error extracting entities from memory {memory_id}: {e}")

    async def _extract_relationships_from_memory(self, memory: dict[str, Any]) -> None:
        """Extract relationships from a single memory."""
        memory_content = memory.get("content", "")
        memory_id = memory.get("id", "")
        metadata = memory.get("metadata", {})

        # Get known entities for context
        known_entities = [
            f"{node.name} ({node.type})" for node in self.knowledge_graph.nodes.values()
        ]

        # Prepare prompt inputs
        prompt_input = {
            "memory_content": memory_content,
            "known_entities": ", ".join(known_entities),
            "existing_relationships": metadata.get("relationships", []),
            "relationship_types": ", ".join(self.relationship_types),
        }

        # Extract relationships using LLM
        try:
            response = await self.llm.ainvoke(
                [
                    SystemMessage(
                        content="You are an expert knowledge graph relationship extractor."
                    ),
                    HumanMessage(
                        content=self.relationship_extraction_prompt.format(
                            **prompt_input
                        )
                    ),
                ]
            )

            # Parse response
            relationships_data = self._parse_json_response(response.content)

            if relationships_data and "relationships" in relationships_data:
                for rel_data in relationships_data["relationships"]:
                    # Find entity IDs
                    source_id = self._find_entity_id(rel_data["source_entity"])
                    target_id = self._find_entity_id(rel_data["target_entity"])

                    if source_id and target_id:
                        # Create relationship
                        rel_id = self._generate_relationship_id(
                            source_id, target_id, rel_data["relationship_type"]
                        )

                        relationship = KnowledgeGraphRelationship(
                            id=rel_id,
                            source_id=source_id,
                            target_id=target_id,
                            relationship_type=rel_data["relationship_type"],
                            properties=rel_data.get("properties", {}),
                            memory_references=[memory_id],
                            confidence=rel_data.get("confidence", 0.8),
                        )

                        # Add to graph
                        self.knowledge_graph.add_relationship(relationship)

        except Exception as e:
            logger.exception(
                f"Error extracting relationships from memory {memory_id}: {e}"
            )

    def _generate_entity_id(self, name: str, entity_type: str) -> str:
        """Generate unique entity ID."""
        return f"{entity_type}_{name}".lower().replace(" ", "_")

    def _generate_relationship_id(
        self, source_id: str, target_id: str, rel_type: str
    ) -> str:
        """Generate unique relationship ID."""
        return f"{source_id}_{rel_type}_{target_id}".lower().replace(" ", "_")

    def _find_entity_id(self, entity_name: str) -> str | None:
        """Find entity ID by name."""
        entity_name_lower = entity_name.lower()
        for node in self.knowledge_graph.nodes.values():
            if node.name.lower() == entity_name_lower:
                return node.id
        return None

    def _parse_json_response(self, response: str) -> dict[str, Any] | None:
        """Parse JSON response from LLM."""
        try:
            import json

            # Try to find JSON in response
            start_idx = response.find("{")
            end_idx = response.rfind("}") + 1
            if start_idx != -1 and end_idx > start_idx:
                json_str = response[start_idx:end_idx]
                return json.loads(json_str)
        except Exception as e:
            logger.warning(f"Failed to parse JSON response: {e}")
        return None

    async def extract_entities_from_memories(
        self, limit: int | None = None, namespace: tuple[str, ...] | None = None
    ) -> list[KnowledgeGraphNode]:
        """Extract entities from memories and return them as a list.

        Args:
            limit: Maximum number of memories to process
            namespace: Memory namespace to process

        Returns:
            List of extracted knowledge graph nodes (entities)
        """
        try:
            # Extract full knowledge graph first
            await self.extract_knowledge_graph_from_memories(
                namespace=namespace, memory_types=None
            )

            # Return entities as list
            entities = list(self.knowledge_graph.nodes.values())

            # Limit if requested
            if limit and len(entities) > limit:
                entities = entities[:limit]

            return entities

        except Exception as e:
            logger.exception(f"Error extracting entities from memories: {e}")
            return []

    async def extract_relationships_from_memories(
        self, limit: int | None = None, namespace: tuple[str, ...] | None = None
    ) -> list[KnowledgeGraphRelationship]:
        """Extract relationships from memories and return them as a list.

        Args:
            limit: Maximum number of memories to process
            namespace: Memory namespace to process

        Returns:
            List of extracted knowledge graph relationships
        """
        try:
            # Extract full knowledge graph first
            await self.extract_knowledge_graph_from_memories(
                namespace=namespace, memory_types=None
            )

            # Return relationships as list
            relationships = list(self.knowledge_graph.relationships.values())

            # Limit if requested
            if limit and len(relationships) > limit:
                relationships = relationships[:limit]

            return relationships

        except Exception as e:
            logger.exception(f"Error extracting relationships from memories: {e}")
            return []

    async def get_entity_context(self, entity_name: str) -> dict[str, Any]:
        """Get context for an entity by name.

        Args:
            entity_name: Name of the entity to get context for

        Returns:
            Dictionary containing entity context information
        """
        try:
            # Find entity by name
            entity_id = self._find_entity_id(entity_name)

            if not entity_id:
                return {"error": f"Entity '{entity_name}' not found"}

            # Get entity details
            entity = self.knowledge_graph.nodes.get(entity_id)
            if not entity:
                return {"error": f"Entity '{entity_name}' not found in graph"}

            # Get neighborhood
            neighborhood = await self.get_entity_neighborhood(entity_id, depth=2)

            return {
                "entity": entity,
                "neighborhood": neighborhood,
                "entity_name": entity_name,
            }

        except Exception as e:
            logger.exception(f"Error getting entity context: {e}")
            return {"error": str(e)}

    async def get_entity_neighborhood(
        self, entity_id: str, depth: int = 1
    ) -> dict[str, Any]:
        """Get the neighborhood of an entity up to specified depth.

        Args:
            entity_id: The entity to explore
            depth: Maximum depth to traverse

        Returns:
            Dictionary containing entity neighborhood information
        """
        if entity_id not in self.knowledge_graph.nodes:
            return {}

        visited = set()
        current_level = {entity_id}
        neighborhood = {
            "center_entity": self.knowledge_graph.nodes[entity_id],
            "levels": [],
            "total_nodes": 0,
            "total_relationships": 0,
        }

        for level in range(depth):
            if not current_level:
                break

            level_data = {"level": level, "nodes": [], "relationships": []}

            next_level = set()

            for node_id in current_level:
                if node_id in visited:
                    continue

                visited.add(node_id)

                # Get connected nodes
                connected_nodes = self.knowledge_graph.get_connected_nodes(node_id)
                relationships = self.knowledge_graph.get_relationships_for_node(node_id)

                level_data["nodes"].extend(connected_nodes)
                level_data["relationships"].extend(relationships)

                # Add to next level
                for rel in relationships:
                    next_node_id = (
                        rel.target_id if rel.source_id == node_id else rel.source_id
                    )
                    if next_node_id not in visited:
                        next_level.add(next_node_id)

            neighborhood["levels"].append(level_data)
            current_level = next_level

        # Calculate totals
        neighborhood["total_nodes"] = len(visited)
        neighborhood["total_relationships"] = sum(
            len(level["relationships"]) for level in neighborhood["levels"]
        )

        return neighborhood

    async def run(self, user_input: str) -> str:
        """Main execution method for the KG Generator Agent."""
        # Parse user input to understand the request
        if "extract" in user_input.lower() or "build" in user_input.lower():
            # Extract knowledge graph
            await self.extract_knowledge_graph_from_memories()

            return f"Knowledge graph extracted successfully. Found {len(self.knowledge_graph.nodes)} entities and {len(self.knowledge_graph.relationships)} relationships."

        if "explore" in user_input.lower() or "neighborhood" in user_input.lower():
            # Find entity to explore
            words = user_input.lower().split()
            entity_name = None

            for word in words:
                if word in [
                    node.name.lower() for node in self.knowledge_graph.nodes.values()
                ]:
                    entity_name = word
                    break

            if entity_name:
                entity_id = self._find_entity_id(entity_name)
                if entity_id:
                    neighborhood = await self.get_entity_neighborhood(entity_id)
                    return f"Entity '{entity_name}' neighborhood: {neighborhood['total_nodes']} connected nodes, {neighborhood['total_relationships']} relationships"

            return "Please specify an entity to explore."

        if "stats" in user_input.lower() or "statistics" in user_input.lower():
            # Return graph statistics
            return f"Knowledge Graph Statistics:\n- Nodes: {len(self.knowledge_graph.nodes)}\n- Relationships: {len(self.knowledge_graph.relationships)}\n- Last Updated: {self.knowledge_graph.metadata.get('last_updated', 'Never')}"

        return "I can help you extract knowledge graphs from memories, explore entity neighborhoods, or provide graph statistics. What would you like to do?"
