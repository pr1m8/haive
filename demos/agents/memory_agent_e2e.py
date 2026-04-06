"""E2E Demo: MemoryAgent with KG extraction, Cypher queries, and Neo4j.

Tests the full memory pipeline:
1. MemoryAgent saves memories via LLM tool calls
2. KG triples auto-extracted from conversations
3. Memories recalled in subsequent turns
4. KG queried (store-based or Neo4j if available)
5. Auto-summarization on context length threshold

Usage:
    # Store-only mode (always works)
    poetry run python demos/agents/memory_agent_e2e.py

    # With Neo4j (requires docker-compose up)
    NEO4J_URI=bolt://localhost:7687 poetry run python demos/agents/memory_agent_e2e.py --neo4j
"""

import argparse
import logging
import sys

sys.path.insert(0, ".")

from dotenv import load_dotenv
load_dotenv()


def test_store_based_memory():
    """Test memory agent with store-only (no Neo4j)."""
    from haive.agents.memory import create_memory_agent

    print("=" * 60)
    print("MemoryAgent E2E Test (Store-based)")
    print("=" * 60)

    agent = create_memory_agent(
        name="mem_e2e",
        user_id="test_user",
        auto_extract_kg=True,
        summarize_threshold=2000,
    )
    print(f"[OK] Agent created: {agent.name}")
    print(f"     Store: {type(agent.get_store()).__name__}")
    print(f"     Tools: {[t.name for t in agent.engine.tools if hasattr(t, 'name')]}")

    # Turn 1: Share info → LLM should save memories + KG extracted
    print("\n--- Turn 1: Share info ---")
    r1 = agent.run("My name is Alice. I'm a data scientist at DeepMind working on reinforcement learning.")
    _print_messages(r1)

    # Turn 2: More info
    print("\n--- Turn 2: More info ---")
    r2 = agent.run("I use PyTorch and JAX for my research. I prefer functional programming.")
    _print_messages(r2)

    # Turn 3: Recall
    print("\n--- Turn 3: Recall ---")
    r3 = agent.run("What do you know about me, my work, and my tools?")
    _print_messages(r3)

    # Check store contents
    print("\n--- Store Contents ---")
    store = agent.get_store()
    _print_store(store, "test_user")

    # Query KG (store-based fallback)
    print("\n--- KG Query (store-based) ---")
    triples = agent.query_kg("Alice")
    for t in triples:
        print(f"  {t['subject']} --{t['predicate']}--> {t['object']}")
    if not triples:
        print("  (no triples found via store search)")

    print("\n[OK] Store-based e2e test complete!")
    return agent


def test_neo4j_integration(agent):
    """Test Neo4j KG integration (requires Neo4j running)."""
    print("\n" + "=" * 60)
    print("MemoryAgent E2E Test (Neo4j KG)")
    print("=" * 60)

    try:
        # Connect to Neo4j
        kg = agent.connect_neo4j()
        print(f"[OK] Neo4j connected")

        # Sync existing KG triples to Neo4j
        synced = agent.sync_kg_to_neo4j()
        print(f"[OK] Synced {synced} triples to Neo4j")

        # Query entity via Neo4j
        print("\n--- Neo4j: Entity query (Alice) ---")
        triples = agent.query_kg("Alice")
        for t in triples:
            print(f"  {t['subject']} --{t['predicate']}--> {t['object']}")

        # Neighborhood query
        print("\n--- Neo4j: Neighborhood ---")
        neighbors = kg.query_neighborhood("Alice")
        for n in neighbors:
            print(f"  {n['center']} -{n['rel1']}-> {n['neighbor']}", end="")
            if n.get("hop2_entity"):
                print(f" -{n['rel2']}-> {n['hop2_entity']}", end="")
            print()

        # Raw Cypher query
        print("\n--- Neo4j: Cypher query ---")
        cypher = "MATCH (e:Entity)-[r:RELATES_TO]->(t:Entity) RETURN e.name, r.predicate, t.name LIMIT 10"
        results = agent.query_kg_cypher(cypher)
        for r in results:
            print(f"  {r}")

        # Stats
        stats = kg.get_stats()
        print(f"\n--- Neo4j Stats ---")
        print(f"  Entities: {stats['entities']}")
        print(f"  Relationships: {stats['relationships']}")

        # Add a turn with Neo4j connected (should auto-sync)
        print("\n--- Turn 4: With Neo4j sync ---")
        r4 = agent.run("Alice also collaborates with Bob on a paper about multi-agent systems.")
        _print_messages(r4)

        # Verify new triples in Neo4j
        print("\n--- Neo4j: Updated triples ---")
        triples = kg.query_entity("Alice")
        for t in triples:
            print(f"  {t['subject']} --{t['predicate']}--> {t['object']}")

        kg.close()
        print("\n[OK] Neo4j e2e test complete!")

    except ImportError as e:
        print(f"[SKIP] Neo4j not available: {e}")
        print("       Install with: pip install neo4j")
    except Exception as e:
        print(f"[SKIP] Neo4j connection failed: {e}")
        print("       Start with: docker-compose up -d neo4j")


def _print_messages(result):
    """Print messages from a result."""
    messages = result.messages if hasattr(result, "messages") else []
    for msg in messages:
        if hasattr(msg, "content") and msg.content:
            tc = getattr(msg, "tool_calls", None)
            if tc:
                print(f"  [{type(msg).__name__}]: tool_calls={[c['name'] for c in tc]}")
            else:
                print(f"  [{type(msg).__name__}]: {msg.content[:200]}")


def _print_store(store, user_id):
    """Print store contents."""
    # Memories
    user_items = store.search(("user", user_id), limit=20)
    print(f"  Memories ({len(user_items)}):")
    for item in user_items:
        v = item.value if hasattr(item, "value") else item
        print(f"    - {v.get('content', str(v))[:80]}")

    # KG triples
    kg_items = store.search(("kg", user_id), limit=20)
    kg_triples = [i for i in kg_items if (i.value if hasattr(i, "value") else i).get("type") == "kg_triple"]
    print(f"  KG Triples ({len(kg_triples)}):")
    for item in kg_triples:
        v = item.value if hasattr(item, "value") else item
        print(f"    - {v['subject']} {v['predicate']} {v['object']}")

    # Summaries
    sum_items = store.search(("summary", user_id), limit=5)
    print(f"  Summaries ({len(sum_items)}):")
    for item in sum_items:
        v = item.value if hasattr(item, "value") else item
        print(f"    - {v.get('content', str(v))[:80]}")


def main():
    parser = argparse.ArgumentParser(description="MemoryAgent E2E Demo")
    parser.add_argument("--neo4j", action="store_true", help="Test Neo4j integration")
    parser.add_argument("--verbose", action="store_true", help="Enable debug logging")
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.WARNING)

    # Always test store-based
    agent = test_store_based_memory()

    # Optionally test Neo4j
    if args.neo4j:
        test_neo4j_integration(agent)

    print("\n" + "=" * 60)
    print("All tests complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
