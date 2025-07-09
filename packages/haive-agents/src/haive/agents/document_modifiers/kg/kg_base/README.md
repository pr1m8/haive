# KG Base - Knowledge Graph Foundation

Base models and utilities for knowledge graph construction from documents.

## Overview

The KG Base module provides the foundational components for all knowledge graph agents in the Haive framework. It defines the core transformer class that converts documents into graph structures, along with the models and utilities needed for graph representation.

This module serves as the foundation for:

- Document to graph transformation
- Entity and relationship extraction
- Graph document representation
- LLM-based graph construction

Key capabilities:

- **Flexible graph schemas**: Support for custom entity and relationship types
- **LLM integration**: Uses language models for intelligent extraction
- **Property extraction**: Extract properties for both nodes and relationships
- **Validation**: Ensure extracted graphs follow defined schemas
- **Extensibility**: Base classes for custom graph transformers

## Architecture

The module provides a layered approach to graph construction:

1. **Document Input**: Accept various document formats
2. **LLM Processing**: Use language models to identify entities and relationships
3. **Schema Validation**: Ensure extracted elements match allowed types
4. **Graph Construction**: Build structured graph representations
5. **Output Format**: Produce standardized GraphDocument objects

## Key Components

### GraphTransformer

The main transformer class that converts documents into knowledge graphs using LLMs.

```python
class GraphTransformer(BaseDocumentTransformer):
    """A document transformer that transforms a document into a graph."""
```

Key features:

- Configurable LLM backend
- Schema enforcement with allowed nodes and relationships
- Property extraction for rich graph data
- Custom prompt support for specialized domains
- Strict mode for validation

### Models

- **GraphDocument**: Standard representation of a document as a graph
- **Node**: Entity representation with type and properties
- **Relationship**: Connection between entities with type and properties

### Configuration

- **LLMConfig**: Configuration for the language model used in extraction
- **Allowed schemas**: Define permitted entity and relationship types

## Installation

This module is part of the `haive-agents` package. Install it using:

```bash
pip install haive-agents
```

## Usage Examples

### Basic Graph Transformation

```python
from haive.agents.document_modifiers.kg.kg_base.models import GraphTransformer
from haive.core.models.llm.base import LLMConfig
from langchain_core.documents import Document

# Initialize transformer
transformer = GraphTransformer()

# Define allowed graph schema
allowed_nodes = ["Person", "Organization", "Location", "Event"]
allowed_relationships = [
    ("Person", "WORKS_FOR", "Organization"),
    ("Person", "LOCATED_IN", "Location"),
    ("Organization", "HEADQUARTERED_IN", "Location"),
    ("Person", "PARTICIPATED_IN", "Event")
]

# Transform documents
documents = [
    Document(page_content="John Smith works for Acme Corp in New York."),
    Document(page_content="Acme Corp is headquartered in New York City.")
]

graph_documents = transformer.transform_documents(
    documents=documents,
    allowed_nodes=allowed_nodes,
    allowed_relationships=allowed_relationships,
    strict_mode=True  # Enforce schema
)

# Access extracted graph
for graph_doc in graph_documents:
    print(f"Nodes: {len(graph_doc.nodes)}")
    print(f"Relationships: {len(graph_doc.relationships)}")

    for node in graph_doc.nodes:
        print(f"  Entity: {node.id} ({node.type})")

    for rel in graph_doc.relationships:
        print(f"  Relationship: {rel.source} -> {rel.target} ({rel.type})")
```

### Advanced Configuration with Properties

```python
# Enable property extraction
node_properties = ["role", "founded_year", "industry", "population"]
relationship_properties = ["since", "department", "confidence"]

# Custom LLM configuration
llm_config = LLMConfig(
    model="gpt-4",
    temperature=0.1,  # Low temperature for consistency
    max_tokens=2000
)

# Transform with properties
graph_documents = transformer.transform_documents(
    documents=documents,
    llm_config=llm_config,
    allowed_nodes=allowed_nodes,
    allowed_relationships=allowed_relationships,
    node_properties=node_properties,
    relationship_properties=relationship_properties,
    additional_instructions="Extract founding years for organizations and roles for people."
)

# Access properties
for node in graph_documents[0].nodes:
    if node.properties:
        print(f"{node.id} properties: {node.properties}")
```

### Custom Prompt for Domain-Specific Extraction

```python
from langchain_core.prompts import ChatPromptTemplate

# Define custom prompt for medical domain
medical_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a medical knowledge graph extractor. Focus on medical entities and their relationships."),
    ("human", "Extract medical entities and relationships from: {text}")
])

# Medical schema
medical_nodes = ["Disease", "Symptom", "Treatment", "Medication", "Anatomy"]
medical_relationships = [
    ("Disease", "HAS_SYMPTOM", "Symptom"),
    ("Disease", "TREATED_WITH", "Treatment"),
    ("Treatment", "USES_MEDICATION", "Medication"),
    ("Disease", "AFFECTS", "Anatomy")
]

# Transform medical documents
medical_docs = [
    Document(page_content="COVID-19 causes fever and cough. It affects the respiratory system.")
]

medical_graphs = transformer.transform_documents(
    documents=medical_docs,
    allowed_nodes=medical_nodes,
    allowed_relationships=medical_relationships,
    prompt=medical_prompt,
    additional_instructions="Pay special attention to symptom severity and treatment effectiveness."
)
```

### Integration with Graph Databases

```python
# Transform documents for Neo4j import
graph_documents = transformer.transform_documents(
    documents=documents,
    allowed_nodes=allowed_nodes,
    allowed_relationships=allowed_relationships,
    strict_mode=True
)

# Convert to Neo4j-compatible format
def to_neo4j_format(graph_doc):
    """Convert GraphDocument to Neo4j import format."""
    nodes = []
    relationships = []

    for node in graph_doc.nodes:
        nodes.append({
            "id": node.id,
            "labels": [node.type],
            "properties": node.properties or {}
        })

    for rel in graph_doc.relationships:
        relationships.append({
            "source": rel.source,
            "target": rel.target,
            "type": rel.type,
            "properties": rel.properties or {}
        })

    return {"nodes": nodes, "relationships": relationships}

# Prepare for import
neo4j_data = [to_neo4j_format(doc) for doc in graph_documents]
```

## Schema Design Best Practices

### Entity Types

1. **Use clear, singular nouns**

   ```python
   # Good
   allowed_nodes = ["Person", "Company", "Product"]

   # Avoid
   allowed_nodes = ["people", "Companies", "PRODUCTS"]
   ```

2. **Create hierarchical types when appropriate**
   ```python
   allowed_nodes = [
       "Entity",  # Base type
       "Person",  # Subtype of Entity
       "Organization",  # Subtype of Entity
       "Government",  # Subtype of Organization
   ]
   ```

### Relationship Types

1. **Use descriptive, active verbs**

   ```python
   # Good
   ("Person", "WORKS_FOR", "Organization")
   ("Product", "MANUFACTURED_BY", "Company")

   # Avoid
   ("Person", "RELATED_TO", "Organization")  # Too vague
   ```

2. **Include directionality in the type**
   ```python
   ("Parent", "HAS_CHILD", "Child")
   ("Child", "HAS_PARENT", "Parent")
   ```

### Properties

1. **Use consistent property names**

   ```python
   node_properties = ["name", "description", "created_date", "updated_date"]
   ```

2. **Type-specific properties**
   ```python
   person_properties = ["age", "occupation", "nationality"]
   company_properties = ["founded_year", "revenue", "employee_count"]
   ```

## Configuration Options

### GraphTransformer Parameters

- `llm_config`: LLM configuration for extraction
- `allowed_nodes`: List of permitted entity types
- `allowed_relationships`: List of tuples defining valid relationships
- `prompt`: Custom prompt template
- `strict_mode`: Whether to enforce schema strictly
- `node_properties`: Properties to extract for nodes
- `relationship_properties`: Properties to extract for relationships
- `ignore_tool_usage`: Skip tool-based extraction
- `additional_instructions`: Extra guidance for the LLM

## Best Practices

1. **Start with a simple schema**
   - Begin with core entities and relationships
   - Add complexity gradually based on results

2. **Use consistent naming conventions**
   - PascalCase for entity types
   - UPPER_SNAKE_CASE for relationship types
   - lower_snake_case for properties

3. **Validate extracted graphs**
   - Check for orphaned nodes
   - Verify relationship consistency
   - Ensure required properties are present

4. **Optimize for your use case**
   - Use lower temperatures for consistency
   - Adjust chunk sizes for document processing
   - Consider domain-specific prompts

## Troubleshooting

### Common Issues

1. **Missing entities or relationships**

   ```python
   # Solution: Provide more specific instructions
   additional_instructions = """
   Pay special attention to:
   - Job titles and roles
   - Dates and time periods
   - Locations at all levels (city, state, country)
   """
   ```

2. **Inconsistent entity names**

   ```python
   # Solution: Add normalization instructions
   additional_instructions = "Always use full names for people and official names for organizations."
   ```

3. **Too many false relationships**
   ```python
   # Solution: Use strict mode and specific relationship types
   strict_mode = True
   allowed_relationships = [
       ("Person", "DIRECTLY_MANAGES", "Person"),
       # Not just ("Person", "RELATED_TO", "Person")
   ]
   ```

## API Reference

For detailed API documentation, see the [API Reference](../../../../../docs/source/api/document_modifiers/kg/kg_base/index.rst).

## See Also

- [`kg_iterative_refinement`](../kg_iterative_refinement/): Iterative graph building
- [`kg_map_merge`](../kg_map_merge/): Parallel graph construction
- [`langchain.graph_transformers`](https://python.langchain.com/docs/modules/graphs/): LangChain graph utilities
- [`neo4j`](https://neo4j.com/): Graph database integration
