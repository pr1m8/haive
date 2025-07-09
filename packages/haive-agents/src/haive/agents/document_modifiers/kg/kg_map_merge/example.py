import asyncio

from haive.agents.document_modifiers.kg.kg_map_merge.utils import (
    create_knowledge_graph,
    visualize_graph,
)

if __name__ == "__main__":

    async def main():
        # Import numpy for visualization

        # Example documents
        documents = [
            "Marie Curie, born in 1867, was a Polish and naturalised-French physicist and chemist who conducted pioneering research on radioactivity.",
            "Marie Curie was the first woman to win a Nobel Prize. Her husband, Pierre Curie, was a co-winner of her first Nobel Prize.",
            "Poland is a country in Europe. Poland was first established as a unified state in 966, and its capital is Warsaw.",
            "Warsaw is the capital and largest city of Poland. It is located on the Vistula River.",
            "Marie Curie discovered the elements polonium and radium. She named polonium after her native country Poland.",
            "Pierre Curie was a French physicist who made pioneering contributions to crystallography, magnetism, and radioactivity.",
        ]

        # Create knowledge graph
        print("Creating knowledge graph...")
        graph = await create_knowledge_graph(
            documents=documents,
            allowed_nodes=["Person", "Country", "City", "Award", "Element", "Field"],
            allowed_relationships=[
                "BORN_IN",
                "WON",
                "CAPITAL_OF",
                "LOCATED_IN",
                "DISCOVERED",
                "NAMED_AFTER",
                "CONTRIBUTED_TO",
                "MARRIED_TO",
            ],
        )

        # Print the result
        if graph:
            print(f"\nNodes: {len(graph.nodes)}")
            for node in graph.nodes:
                properties = ", ".join(
                    f"{k}={v}" for k, v in (node.properties or {}).items()
                )
                print(f"  - {node.id} ({node.type}) {properties}")

            print(f"\nRelationships: {len(graph.relationships)}")
            for rel in graph.relationships:
                properties = ", ".join(
                    f"{k}={v}" for k, v in (rel.properties or {}).items()
                )
                print(f"  - {rel.source.id} -{rel.type}-> {rel.target.id} {properties}")

            # Visualize the graph
            await visualize_graph(graph, "knowledge_graph.png")
        else:
            print("No graph was generated.")

    asyncio.run(main())
