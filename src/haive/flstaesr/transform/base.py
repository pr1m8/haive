from typing import List, Tuple, Union, Optional
from langchain_core.documents import Document, BaseDocumentTransformer
from langchain_core.prompts import ChatPromptTemplate
from langchain_neo4j.graphs.graph_document import GraphDocument
from langchain_experimental.graph_transformers import LLMGraphTransformer
from src.haive.core.models.llm.base import LLMConfig, AzureLLMConfig


class GraphTransformer(BaseDocumentTransformer):
    """
    A document transformer that transforms a document into a graph.
    """

    def transform_documents(
        self,
        documents: List[Document],
        llm_config: LLMConfig = AzureLLMConfig(),
        allowed_nodes: List[str] = [],
        allowed_relationships: Union[List[str], List[Tuple[str, str, str]]] = [],
        prompt: Optional[ChatPromptTemplate] = None,
        strict_mode: bool = True,
        node_properties: Union[bool, List[str]] = [],
        relationship_properties: Union[bool, List[str]] = [],
        ignore_tool_usage: bool = False,
        additional_instructions: str = "",
    ) -> List[GraphDocument]:
        """
        Transform a document into a graph.
        
        Args:
            documents: The documents to transform.
            llm_config: The LLM configuration.
            allowed_nodes: The allowed nodes.
            allowed_relationships: The allowed relationships.
            prompt: The prompt.
            strict_mode: The strict mode.
            node_properties: The node properties.
            relationship_properties: The relationship properties.
            ignore_tool_usage: The ignore tool usage.
            additional_instructions: The additional instructions.
        """
        
        llm = llm_config.instantiate_llm()

        print("DEBUG: Type of allowed_relationships ->", type(allowed_relationships))  # ✅ Debugging statement
        
        if not isinstance(allowed_relationships, list):
            raise TypeError("allowed_relationships must be a list!")

        # ✅ Check if the LLM supports function calling before passing properties
        graph_transformer_kwargs = {
            "llm": llm,
            "allowed_nodes": allowed_nodes,
            "allowed_relationships": allowed_relationships,
            "prompt": prompt,
            "strict_mode": strict_mode,
            "ignore_tool_usage": ignore_tool_usage,
            "additional_instructions": additional_instructions,
        }

        if getattr(llm, "supports_function_calling", False):  # ✅ Only pass if supported
            graph_transformer_kwargs["node_properties"] = node_properties
            graph_transformer_kwargs["relationship_properties"] = relationship_properties

        graph_transformer = LLMGraphTransformer(**graph_transformer_kwargs)

        return graph_transformer.convert_to_graph_documents(documents)


### **✅ Usage Example**
text = """
Marie Curie, born in 1867, was a Polish and naturalised-French physicist and chemist who conducted pioneering research on radioactivity.
She was the first woman to win a Nobel Prize, the first person to win a Nobel Prize twice, and the only person to win a Nobel Prize in two scientific fields.
Her husband, Pierre Curie, was a co-winner of her first Nobel Prize, making them the first-ever married couple to win the Nobel Prize and launching the Curie family legacy of five Nobel Prizes.
She was, in 1906, the first woman to become a professor at the University of Paris.
"""
nstr="""Poland is a country in Europe. Poland was first established in 1919, and its capital is Warsaw."""
documents = [Document(page_content=text),Document(page_content=nstr)]

graph_documents = GraphTransformer().transform_documents(
    documents,
    llm_config=AzureLLMConfig(),
    #allowed_nodes=["Marie Curie", "Pierre Curie"],
    #allowed_relationships=["married"],  # ✅ Now correctly passed as a list
   # node_properties=["name", "born"],  # ✅ Only passed if LLM supports function calling
    #relationship_properties=["married"],  # ✅ Only passed if LLM supports function calling
    ignore_tool_usage=True,
    additional_instructions=""
)

print(graph_documents)  # ✅ Should now work correctly!
import networkx as nx
import matplotlib.pyplot as plt
from langchain_neo4j.graphs.graph_document import GraphDocument


def render_graph(graph_documents: list[GraphDocument], output_filename="graph.png"):
    """
    Renders a GraphDocument as an image and saves it.

    Args:
        graph_documents (list[GraphDocument]): List of graph documents to visualize.
        output_filename (str): Name of the output file to save the graph image.
    """
    G = nx.DiGraph()  # Directed graph

    # Add nodes and edges
    for graph_doc in graph_documents:
        for node in graph_doc.nodes:
            G.add_node(node.id, label=node.type)  # Add nodes with labels
        
        for relationship in graph_doc.relationships:
            G.add_edge(relationship.source.id, relationship.target.id, label=relationship.type)  # Add edges with labels

    # Define graph layout
    pos = nx.spring_layout(G, seed=42)  # Positions for nodes

    # Draw nodes and edges
    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, with_labels=True, node_color="lightblue", edge_color="gray", node_size=3000, font_size=10)

    # Draw edge labels
    edge_labels = {(u, v): d["label"] for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

    # Save image
    plt.savefig(output_filename, format="png")
    plt.show()
    print(f"Graph saved as {output_filename}")


### **✅ Usage Example**
# Assuming `graph_documents` is the list you printed.
render_graph(graph_documents, "marie_curie_graph.png")
