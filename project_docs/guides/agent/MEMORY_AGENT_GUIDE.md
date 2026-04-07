# Memory Agent Guide

**Created**: 2026-04-06
**Status**: Phase 2 complete, e2e verified

## Overview

MemoryAgent is a ReactAgent with persistent memory, automatic KG extraction, and auto-summarization. It stores memories and knowledge graph triples in a LangGraph store (InMemoryStore or PostgresStore), with optional Neo4j for graph traversal.

## Quick Start

```python
from haive.agents.memory import create_memory_agent

# Dev mode (InMemoryStore)
agent = create_memory_agent(name="assistant", user_id="user123")

# Production (PostgreSQL)
agent = create_memory_agent(
    name="assistant",
    connection_string="postgresql://haive:haive@localhost/haive",
    user_id="user123",
)

# With Neo4j KG
agent = create_memory_agent(name="assistant", user_id="user123")
agent.connect_neo4j()  # Uses NEO4J_URI/USER/PASSWORD env vars

# Run
result = agent.run("My name is Alice and I work at DeepMind.")
# → LLM saves memories + KG triples auto-extracted

result = agent.run("What do you know about me?")
# → Recalls memories and KG facts
```

## Architecture

```
create_memory_agent()
  ├── Resolves store: explicit > connection_string > InMemoryStore
  ├── Creates memory tools bound to store + user_id
  ├── Builds AugLLMConfig with tools
  └── Returns MemoryAgent(ReactAgent)

MemoryAgent.run(input)
  ├── PRE-HOOK: _load_memory_context(query)
  │   ├── Search ("user", user_id) → memories
  │   ├── Search ("kg", user_id) → KG triples
  │   └── Search ("summary", user_id) → summaries
  │   → Inject into system message
  ├── EXECUTE: ReactAgent.run()
  │   └── LLM may call: save_memory, search_memory, save_knowledge, search_knowledge
  ├── POST-HOOK 1: _extract_and_store_kg(messages)
  │   ├── SimpleAgent extracts JSON triples from conversation
  │   ├── Store triples in ("kg", user_id) namespace
  │   └── Sync to Neo4j if connected
  └── POST-HOOK 2: Auto-summarize if token_count > threshold
      ├── SimpleAgent summarizes conversation
      └── Store in ("summary", user_id) namespace
```

## Memory Tools

| Tool | Purpose | Args |
|------|---------|------|
| `save_memory` | Save facts/preferences about user | content, importance |
| `search_memory` | Recall past memories | query |
| `save_knowledge` | Save KG triple (structured fact) | subject, predicate, object_ |
| `search_knowledge` | Query KG triples | query |

## Store Namespaces

| Namespace | Content | Example |
|-----------|---------|---------|
| `("user", user_id)` | User memories | "Alice works at DeepMind" |
| `("kg", user_id)` | KG triples | {subject: "Alice", predicate: "works at", object: "DeepMind"} |
| `("summary", user_id)` | Conversation summaries | "Discussed ML research..." |

## Neo4j Integration

```python
# Start Neo4j
# docker-compose up -d neo4j

# Connect
kg = agent.connect_neo4j()

# Sync existing triples from store to Neo4j
agent.sync_kg_to_neo4j()

# Query via graph traversal
triples = agent.query_kg("Alice")
# [{"subject": "Alice", "predicate": "works at", "object": "DeepMind"}, ...]

# Raw Cypher
results = agent.query_kg_cypher(
    "MATCH (s:Entity)-[r:RELATES_TO]->(o:Entity) WHERE s.name = $name RETURN s, r, o",
    params={"name": "Alice"}
)

# Neighborhood (1-2 hops)
neighbors = kg.query_neighborhood("Alice")

# Shortest path
path = kg.query_path("Alice", "Python")
```

### Neo4j Schema

```cypher
-- Nodes
(:Entity {name, type, user_id, created_at})
(:Memory {id, content, importance, user_id, created_at})
(:Summary {id, content, token_count, user_id, created_at})

-- Relationships
(Entity)-[:RELATES_TO {predicate, created_at, source}]->(Entity)
(Entity)-[:MENTIONED_IN]->(Memory)
(Memory)-[:SUMMARIZED_BY]->(Summary)

-- Indexes
CREATE CONSTRAINT entity_name FOR (e:Entity) REQUIRE e.name IS UNIQUE
CREATE INDEX entity_type FOR (e:Entity) ON (e.type)
CREATE INDEX entity_user FOR (e:Entity) ON (e.user_id)
```

## Integration with Other Components

### Document-level KG extraction
```python
# Uses GraphTransformer from document_modifiers
triples = agent.extract_kg_from_document(
    "Alice works at DeepMind on reinforcement learning.",
    allowed_nodes=["Person", "Organization", "Field"]
)
```

### With GraphDBRAG for NL→Cypher
The `rag/db_rag/graph_db/` agent can generate Cypher queries from natural language against the same Neo4j instance.

### With IterativeSummarizer
The `document_modifiers/summarizer/` agents can provide advanced summarization beyond the built-in SimpleAgent summarizer.

## Docker Setup

```bash
# Start PostgreSQL + Neo4j
docker-compose up -d

# Connection strings
# Postgres: postgresql://haive:haive@localhost:5432/haive
# Neo4j:    bolt://localhost:7687 (neo4j/haivepass)
# Neo4j UI: http://localhost:7474
```

## E2E Test

```bash
# Store-only
poetry run python demos/agents/memory_agent_e2e.py

# With Neo4j
poetry run python demos/agents/memory_agent_e2e.py --neo4j
```
