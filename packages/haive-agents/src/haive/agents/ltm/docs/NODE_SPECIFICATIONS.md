# LTM Node Specifications & Implementation Details

## Node Architecture Overview

Each node in the LTM workflow has specific responsibilities, inputs/outputs, and error handling strategies. This document provides detailed specifications for implementing each node type.

## Core Node Categories

### 1. Processing Nodes (EngineNodeConfig)

- Memory extraction
- Knowledge graph processing
- Categorization
- Consolidation

### 2. Storage Nodes (Custom)

- Memory persistence
- Metadata storage
- Cross-reference updates

### 3. Tool Nodes (ToolNodeConfig)

- Memory management tools
- Search tools
- Browse and exploration tools

### 4. Control Nodes (Custom)

- Flow control and routing
- Quality validation
- Error recovery

## Detailed Node Specifications

### 1. Memory Extraction Node

#### Node Configuration

```python
{
    "name": "extract_memories",
    "type": "EngineNodeConfig",
    "engine_name": "memory_extraction",
    "input_transform": "messages_to_extraction_input",
    "output_transform": "extraction_output_to_state",
    "error_handling": "continue_with_empty_memories",
    "timeout": 120  # seconds
}
```

#### Input Schema

```python
class MemoryExtractionInput(BaseModel):
    messages: list[BaseMessage] = Field(description="Conversation messages to process")
    existing_memories: list[dict] = Field(default_factory=list, description="Existing memories for context")
    user_id: str | None = Field(default=None, description="User identifier for personalization")
    session_id: str | None = Field(default=None, description="Session context")
    extraction_mode: Literal["incremental", "full", "update"] = Field(default="incremental")
    max_steps: int = Field(default=3, description="Maximum extraction iterations")
```

#### Output Schema

```python
class MemoryExtractionOutput(BaseModel):
    extracted_memories: list[dict] = Field(description="Newly extracted memory objects")
    updated_memories: list[dict] = Field(default_factory=list, description="Updated existing memories")
    extraction_metadata: dict = Field(description="Processing metadata and statistics")
    confidence_scores: dict[str, float] = Field(description="Confidence in extracted memories")
    processing_time: float = Field(description="Processing duration in seconds")
```

#### Processing Logic

1. **Message Preprocessing**: Clean and format conversation messages
2. **Context Assembly**: Combine messages with existing memories
3. **Schema Selection**: Choose appropriate memory schemas based on content
4. **Iterative Extraction**: Run trustcall extractor for multiple steps
5. **Validation**: Verify extracted memories meet quality thresholds
6. **Deduplication**: Remove or merge duplicate memories

#### Error Handling

- **Extraction Failure**: Return empty list, log error, continue workflow
- **Timeout**: Return partial results, mark as incomplete
- **Schema Validation Error**: Use default schema, log validation issues
- **LLM API Error**: Retry with backoff, fallback to simpler extraction

---

### 2. Knowledge Graph Processing Node

#### Node Configuration

```python
{
    "name": "process_kg",
    "type": "EngineNodeConfig",
    "engine_name": "kg_processing",
    "conditional": "enable_kg_processing",
    "parallel_execution": True,
    "batch_size": 10,
    "timeout": 180
}
```

#### Input Schema

```python
class KGProcessingInput(BaseModel):
    extracted_memories: list[dict] = Field(description="Memories to process for KG extraction")
    existing_kg: dict = Field(default_factory=dict, description="Existing knowledge graph")
    kg_config: dict = Field(description="KG processing configuration")
    allowed_entities: list[str] = Field(default_factory=list, description="Allowed entity types")
    allowed_relationships: list[str] = Field(default_factory=list, description="Allowed relationship types")
```

#### Output Schema

```python
class KGProcessingOutput(BaseModel):
    knowledge_graph: dict = Field(description="Extracted knowledge graph")
    entities: list[dict] = Field(description="Extracted entities with properties")
    relationships: list[dict] = Field(description="Entity relationships with confidence")
    entity_clusters: dict = Field(description="Grouped similar entities")
    kg_statistics: dict = Field(description="KG processing statistics")
    confidence_distribution: dict = Field(description="Confidence score distribution")
```

#### Processing Logic

1. **Document Conversion**: Transform memories into Document objects
2. **Entity Extraction**: Use GraphTransformer to identify entities
3. **Relationship Detection**: Find connections between entities
4. **Confidence Scoring**: Assign confidence levels to entities/relationships
5. **Graph Merging**: Integrate with existing knowledge graph
6. **Consistency Checking**: Validate graph consistency and resolve conflicts

#### Integration Points

- **Haive KG Components**: IterativeGraphTransformer, GraphTransformer
- **Entity Resolution**: Merge similar entities across memories
- **Relationship Validation**: Cross-check relationships for consistency

---

### 3. Categorization Node

#### Node Configuration

```python
{
    "name": "categorize_memories",
    "type": "EngineNodeConfig",
    "engine_name": "categorization",
    "conditional": "enable_categorization",
    "requires_batch": True,
    "min_batch_size": 3,
    "timeout": 240
}
```

#### Input Schema

```python
class CategorizationInput(BaseModel):
    extracted_memories: list[dict] = Field(description="Memories to categorize")
    knowledge_graph: dict = Field(default_factory=dict, description="KG context for categorization")
    existing_taxonomy: dict = Field(default_factory=dict, description="Existing category structure")
    categorization_depth: int = Field(default=3, description="Maximum category hierarchy depth")
    min_category_size: int = Field(default=2, description="Minimum memories per category")
```

#### Output Schema

```python
class CategorizationOutput(BaseModel):
    categories: list[str] = Field(description="Assigned categories")
    category_hierarchy: dict = Field(description="Hierarchical category structure")
    category_confidence: dict[str, float] = Field(description="Confidence in category assignments")
    taxonomy_tree: dict = Field(description="Complete taxonomy structure")
    category_descriptions: dict[str, str] = Field(description="Category descriptions")
    uncategorized_memories: list[dict] = Field(description="Memories that couldn't be categorized")
```

#### Processing Logic

1. **Content Analysis**: Analyze memory content for thematic patterns
2. **Clustering**: Group similar memories using semantic similarity
3. **Taxonomy Generation**: Use TNT to create hierarchical categories
4. **Category Assignment**: Assign memories to appropriate categories
5. **Validation**: Ensure category quality and coherence
6. **Hierarchy Building**: Construct multi-level taxonomy structure

#### Integration Points

- **TNT Components**: TaxonomyAgent for category generation
- **Semantic Clustering**: Group related memories for better categorization
- **Iterative Refinement**: Improve categories based on new memories

---

### 4. Consolidation Node

#### Node Configuration

```python
{
    "name": "consolidate_memories",
    "type": "EngineNodeConfig",
    "engine_name": "consolidation",
    "conditional": "enable_consolidation_and_threshold_met",
    "requires_minimum_memories": 5,
    "timeout": 300
}
```

#### Input Schema

```python
class ConsolidationInput(BaseModel):
    extracted_memories: list[dict] = Field(description="Memories to consolidate")
    categories: list[str] = Field(default_factory=list, description="Memory categories")
    knowledge_graph: dict = Field(default_factory=dict, description="KG context")
    consolidation_strategy: Literal["semantic", "temporal", "categorical"] = Field(default="semantic")
    max_summary_length: int = Field(default=500, description="Maximum summary length")
    preserve_details: bool = Field(default=True, description="Preserve important details")
```

#### Output Schema

```python
class ConsolidationOutput(BaseModel):
    consolidated_summary: str = Field(description="Consolidated memory summary")
    consolidated_memories: list[dict] = Field(description="Merged memory objects")
    consolidation_map: dict[str, list[str]] = Field(description="Mapping of original to consolidated memories")
    preserved_details: list[dict] = Field(description="Important details preserved separately")
    consolidation_metadata: dict = Field(description="Consolidation process metadata")
    quality_metrics: dict = Field(description="Quality assessment of consolidation")
```

#### Processing Logic

1. **Similarity Detection**: Identify related and overlapping memories
2. **Merging Strategy**: Choose appropriate consolidation approach
3. **Summary Generation**: Create comprehensive summaries using IterativeSummarizer
4. **Detail Preservation**: Maintain important specific information
5. **Quality Assessment**: Evaluate consolidation quality
6. **Metadata Tracking**: Record consolidation relationships and provenance

#### Integration Points

- **IterativeSummarizer**: Use Haive's summarization components
- **Semantic Similarity**: Leverage embeddings for memory similarity
- **Incremental Processing**: Support progressive consolidation

---

### 5. Storage Node

#### Node Configuration

```python
{
    "name": "store_memories",
    "type": "StorageNodeConfig",  # Custom node type
    "storage_backend": "haive_persistence",
    "namespace_template": "ltm_user_{user_id}",
    "retry_strategy": "exponential_backoff",
    "timeout": 60
}
```

#### Input Schema

```python
class StorageInput(BaseModel):
    extracted_memories: list[dict] = Field(description="Processed memories to store")
    knowledge_graph: dict = Field(default_factory=dict, description="Associated KG data")
    categories: list[str] = Field(default_factory=list, description="Memory categories")
    consolidated_summary: str = Field(default="", description="Consolidated summary")
    storage_namespace: tuple[str, ...] = Field(description="Storage namespace")
    user_metadata: dict = Field(default_factory=dict, description="User-specific metadata")
```

#### Output Schema

```python
class StorageOutput(BaseModel):
    stored_memory_ids: list[str] = Field(description="IDs of successfully stored memories")
    failed_storage_ids: list[str] = Field(description="IDs that failed to store")
    storage_metadata: dict = Field(description="Storage operation metadata")
    embedding_ids: list[str] = Field(description="Generated embedding IDs")
    cross_references: dict = Field(description="Cross-reference mappings")
    storage_statistics: dict = Field(description="Storage operation statistics")
```

#### Processing Logic

1. **Memory Enhancement**: Enrich memories with processing results
2. **Embedding Generation**: Create vector embeddings for semantic search
3. **Namespace Resolution**: Resolve dynamic namespace templates
4. **Batch Storage**: Store memories efficiently in batches
5. **Cross-Reference Creation**: Build relationships between stored memories
6. **Index Updates**: Update search indices and metadata

#### Storage Strategy

- **Primary Storage**: Memory content and metadata in configured backend
- **Vector Storage**: Embeddings for semantic search
- **Graph Storage**: KG entities and relationships
- **Index Storage**: Category and keyword indices for fast lookup

---

### 6. Memory Tools Node

#### Node Configuration

```python
{
    "name": "memory_tools",
    "type": "ToolNodeConfig",
    "tools": ["manage_memory", "search_memory", "browse_categories", "memory_stats"],
    "tool_timeout": 30,
    "max_iterations": 5,
    "streaming_enabled": True
}
```

#### Available Tools

##### 6.1 Manage Memory Tool

```python
class ManageMemoryInput(BaseModel):
    action: Literal["create", "update", "delete"] = Field(description="Memory management action")
    memory_content: str | None = Field(default=None, description="Memory content for create/update")
    memory_id: str | None = Field(default=None, description="Memory ID for update/delete")
    categories: list[str] = Field(default_factory=list, description="Memory categories")
    tags: list[str] = Field(default_factory=list, description="User tags")

class ManageMemoryOutput(BaseModel):
    success: bool = Field(description="Operation success status")
    memory_id: str | None = Field(description="ID of managed memory")
    message: str = Field(description="Human-readable result message")
    affected_memories: list[str] = Field(description="IDs of affected memories")
```

##### 6.2 Search Memory Tool

```python
class SearchMemoryInput(BaseModel):
    query: str = Field(description="Search query")
    search_modes: list[Literal["semantic", "keyword", "category", "graph"]] = Field(
        default=["semantic"], description="Search modes to use"
    )
    limit: int = Field(default=10, description="Maximum results to return")
    filters: dict = Field(default_factory=dict, description="Search filters")
    include_metadata: bool = Field(default=False, description="Include memory metadata")

class SearchMemoryOutput(BaseModel):
    memories: list[dict] = Field(description="Found memories")
    total_results: int = Field(description="Total matching memories")
    search_metadata: dict = Field(description="Search operation metadata")
    related_categories: list[str] = Field(description="Related categories found")
```

##### 6.3 Browse Categories Tool

```python
class BrowseCategoriesInput(BaseModel):
    category_path: list[str] = Field(default_factory=list, description="Category path to browse")
    include_subcategories: bool = Field(default=True, description="Include subcategories")
    include_memory_count: bool = Field(default=True, description="Include memory counts")

class BrowseCategoriesOutput(BaseModel):
    categories: list[dict] = Field(description="Category information")
    hierarchy: dict = Field(description="Category hierarchy structure")
    memory_counts: dict[str, int] = Field(description="Memories per category")
    navigation_hints: list[str] = Field(description="Suggested navigation paths")
```

#### Tool Processing Logic

1. **Input Validation**: Validate tool parameters and permissions
2. **Context Resolution**: Resolve user context and namespace
3. **Operation Execution**: Execute requested memory operations
4. **Result Formatting**: Format results for user consumption
5. **Metadata Collection**: Gather operation metadata for analytics
6. **Error Handling**: Provide helpful error messages and suggestions

---

## Node Orchestration Patterns

### 1. Sequential Processing

```python
# Basic sequential flow
START → extract_memories → process_kg → categorize → consolidate → store → END
```

### 2. Conditional Branching

```python
# Feature-based branching
extract_memories → [kg_enabled? → process_kg] → [cat_enabled? → categorize] → store
```

### 3. Parallel Processing

```python
# Concurrent operations
extract_memories → SPLIT → [process_kg, categorize, generate_embeddings] → MERGE → store
```

### 4. Iterative Refinement

```python
# Quality-based loops
process → quality_check → [acceptable? → continue, unacceptable → refine] → process
```

### 5. Tool Interaction

```python
# User-driven tool usage
store → tools_needed? → [yes → memory_tools → continue?, no → END]
```

## Implementation Guidelines

### Node Development Principles

1. **Single Responsibility**: Each node has one clear purpose
2. **Error Resilience**: Graceful failure handling with partial results
3. **Configuration Driven**: Behavior controlled by agent configuration
4. **Observable**: Comprehensive logging and metrics
5. **Testable**: Clear interfaces for unit and integration testing

### Performance Considerations

1. **Async Processing**: All nodes support async operation
2. **Batch Processing**: Handle multiple memories efficiently
3. **Resource Management**: Monitor memory and compute usage
4. **Caching**: Cache expensive operations (embeddings, LLM calls)
5. **Streaming**: Support streaming for long-running operations

### Integration Requirements

1. **Haive Compatibility**: Follow Haive node configuration patterns
2. **LangMem Integration**: Maintain compatibility with LangMem tools
3. **Storage Backend**: Work with multiple storage backends
4. **Schema Evolution**: Support schema versioning and migration
5. **Monitoring**: Integrate with Haive's monitoring systems

This specification provides the foundation for implementing a robust, scalable, and maintainable LTM workflow that integrates seamlessly with the Haive framework while providing powerful memory management capabilities.
