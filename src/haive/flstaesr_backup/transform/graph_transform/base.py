from typing import List, Tuple, Union, Optional
from langchain_core.documents import Document, BaseDocumentTransformer
from langchain_core.prompts import ChatPromptTemplate
from langchain_neo4j.graphs.graph_document import GraphDocument
from langchain_experimental.graph_transformers import LLMGraphTransformer
from src.haive.core.models.llm.base import LLMConfig, AzureLLMConfig
# ASYNC MODES.

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
        ignore_tool_usage: bool = True,
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
    

    

