"""Agentic RAG Agent - ReAct + Retrieval with Proper Haive Patterns

This implementation follows the LangChain/LangGraph agentic RAG tutorial but uses
proper Haive base agent infrastructure:
- Inherits from ReActAgent for reasoning/acting patterns
- Uses ToolRouteMixin for automatic tool routing
- Proper Pydantic patterns (no __init__, model validators)
- Generic type safety with bounds
- Multiple engines (LLM + Retriever + Grader)
"""

from typing import Any, Dict, List, Literal, Optional

from haive.core.common.mixins.tool_route_mixin import ToolRouteMixin
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.engine.retriever import BaseRetrieverConfig
from haive.core.graph.node.engine_node import EngineNodeConfig
from haive.core.graph.node.tool_node_config import ToolNodeConfig
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from haive.core.models.llm.base import LLMConfig
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import BaseTool, StructuredTool
from langgraph.graph import END, START
from pydantic import BaseModel, Field, computed_field, model_validator

from haive.agents.react.agent import ReactAgent


# Structured output models for agentic RAG
class DocumentGrade(BaseModel):
    """Grade for document relevance."""
    binary_score: Literal["yes", "no"] = Field(
        description="Relevance score: 'yes' if relevant, 'no' if not relevant"
    )
    reasoning: str = Field(description="Brief explanation of the grading decision")


class QueryRewrite(BaseModel):
    """Rewritten query for better retrieval."""
    rewritten_query: str = Field(description="Improved query for better retrieval")
    changes_made: str = Field(description="What changes were made and why")


# State schema for agentic RAG
class AgenticRAGState(BaseModel):
    """State schema for agentic RAG with retrieval metadata."""
    messages: List[Any] = Field(default_factory=list, description="Conversation messages")
    retrieved_documents: List[Document] = Field(default_factory=list, description="Retrieved documents")
    document_grades: List[DocumentGrade] = Field(default_factory=list, description="Document relevance grades")
    query_rewrites: List[QueryRewrite] = Field(default_factory=list, description="Query rewrite history")
    retrieval_attempts: int = Field(default=0, description="Number of retrieval attempts")
    max_retrieval_attempts: int = Field(default=3, description="Maximum retrieval attempts")


class AgenticRAGAgent[TInput: BaseModel, TOutput: BaseModel](
    ReactAgent[TInput, TOutput],
    ToolRouteMixin
):
    """Agentic RAG agent combining ReAct reasoning with intelligent retrieval.
    
    This agent can:
    - Decide when to retrieve vs respond directly (agentic behavior)
    - Grade retrieved documents for relevance
    - Rewrite queries when documents are not relevant
    - Loop until relevant documents are found or max attempts reached
    
    Key features:
    - Proper Pydantic patterns (no __init__)
    - Multiple engines with proper typing
    - Automatic tool routing via ToolRouteMixin
    - Generic type safety
    """
    
    # Additional engines for agentic RAG
    retriever_engine: BaseRetrieverConfig = Field(
        ..., description="Retrieval engine for document search"
    )
    grader_engine: Optional[AugLLMConfig] = Field(
        default=None, description="Engine for grading document relevance"
    )
    rewriter_engine: Optional[AugLLMConfig] = Field(
        default=None, description="Engine for rewriting queries"
    )
    
    # Agentic RAG configuration
    grade_documents_threshold: float = Field(
        default=0.7, description="Threshold for document relevance grading"
    )
    max_retrieval_attempts: int = Field(
        default=3, description="Maximum attempts to find relevant documents"
    )
    enable_query_rewriting: bool = Field(
        default=True, description="Whether to rewrite queries for better retrieval"
    )
    
    @model_validator(mode="after")
    def setup_agentic_rag(self) -> "AgenticRAGAgent":
        """Setup agentic RAG with multiple engines and tools.
        
        This follows proper Pydantic patterns using model_validator
        instead of __init__ for post-initialization setup.
        """
        # Add all engines to engines dict
        self.engines["llm"] = self.llm_engine
        self.engines["retriever"] = self.retriever_engine
        
        # Setup grader engine (use main LLM if not specified)
        if not self.grader_engine:
            self.grader_engine = AugLLMConfig(
                llm_config=self.llm_engine.llm_config,
                prompt_template=self._create_grading_prompt(),
                structured_output_model=DocumentGrade,
                structured_output_version="v1"
            )
        self.engines["grader"] = self.grader_engine
        
        # Setup rewriter engine (use main LLM if not specified)
        if not self.rewriter_engine:
            self.rewriter_engine = AugLLMConfig(
                llm_config=self.llm_engine.llm_config,
                prompt_template=self._create_rewriting_prompt(),
                structured_output_model=QueryRewrite,
                structured_output_version="v1"
            )
        self.engines["rewriter"] = self.rewriter_engine
        
        # Create and register agentic RAG tools
        self._setup_agentic_tools()
        
        return self
    
    def _setup_agentic_tools(self) -> None:
        """Setup tools for agentic RAG with proper routing."""
        
        # 1. Retrieval tool
        retrieval_tool = self._create_retrieval_tool()
        self.add_routed_tool(retrieval_tool, "retriever")
        
        # 2. Document grading tool
        grading_tool = self._create_grading_tool()
        self.add_routed_tool(grading_tool, "function")
        
        # 3. Query rewriting tool
        if self.enable_query_rewriting:
            rewriting_tool = self._create_rewriting_tool()
            self.add_routed_tool(rewriting_tool, "function")
        
        # 4. Answer generation tool (uses retrieved context)
        answer_tool = self._create_answer_generation_tool()
        self.add_routed_tool(answer_tool, "function")
    
    def _create_retrieval_tool(self) -> BaseTool:
        """Create semantic retrieval tool."""
        def retrieve_documents(query: str) -> str:
            """Search and retrieve relevant documents for the query."""
            try:
                # Use retriever engine to get documents
                result = self.retriever_engine.invoke({"query": query})
                
                # Extract documents from result
                if hasattr(result, "retrieved_documents"):
                    docs = result.retrieved_documents
                elif isinstance(result, dict) and "retrieved_documents" in result:
                    docs = result["retrieved_documents"]
                else:
                    docs = []
                
                if docs:
                    # Combine document content
                    combined_content = "\\n\\n".join([
                        f"Document {i+1}: {doc.page_content}" 
                        for i, doc in enumerate(docs[:5])  # Limit to top 5
                    ])
                    return f"Retrieved {len(docs)} documents:\\n{combined_content}"
                else:
                    return "No relevant documents found for the query."
                    
            except Exception as e:
                return f"Error retrieving documents: {str(e)}"
        
        return StructuredTool.from_function(
            func=retrieve_documents,
            name="retrieve_documents",
            description="Search and retrieve relevant documents for answering questions"
        )
    
    def _create_grading_tool(self) -> BaseTool:
        """Create document grading tool."""
        def grade_document_relevance(context: str, question: str) -> str:
            """Grade whether retrieved documents are relevant to the question."""
            try:
                # Use grader engine to assess relevance
                result = self.grader_engine.invoke({
                    "context": context,
                    "question": question
                })
                
                # Extract grade from structured output
                if hasattr(result, "binary_score"):
                    grade = result
                elif isinstance(result, dict) and "binary_score" in result:
                    grade = DocumentGrade(**result)
                else:
                    return "Could not grade document relevance"
                
                return f"Relevance: {grade.binary_score}. Reasoning: {grade.reasoning}"
                
            except Exception as e:
                return f"Error grading documents: {str(e)}"
        
        return StructuredTool.from_function(
            func=grade_document_relevance,
            name="grade_documents",
            description="Grade whether retrieved documents are relevant to the user question"
        )
    
    def _create_rewriting_tool(self) -> BaseTool:
        """Create query rewriting tool."""
        def rewrite_query(original_query: str, feedback: str = "") -> str:
            """Rewrite the query for better retrieval results."""
            try:
                # Use rewriter engine to improve query
                result = self.rewriter_engine.invoke({
                    "original_query": original_query,
                    "feedback": feedback
                })
                
                # Extract rewrite from structured output
                if hasattr(result, "rewritten_query"):
                    rewrite = result
                elif isinstance(result, dict) and "rewritten_query" in result:
                    rewrite = QueryRewrite(**result)
                else:
                    return f"Could not rewrite query: {original_query}"
                
                return f"Rewritten query: {rewrite.rewritten_query}\\nChanges: {rewrite.changes_made}"
                
            except Exception as e:
                return f"Error rewriting query: {str(e)}"
        
        return StructuredTool.from_function(
            func=rewrite_query,
            name="rewrite_query", 
            description="Rewrite the user query to improve retrieval results"
        )
    
    def _create_answer_generation_tool(self) -> BaseTool:
        """Create answer generation tool using retrieved context."""
        def generate_answer_from_context(question: str, context: str) -> str:
            """Generate a final answer using the retrieved context."""
            answer_prompt = ChatPromptTemplate.from_template(
                "You are an assistant for question-answering tasks. "
                "Use the following retrieved context to answer the question. "
                "If you don't know the answer, say you don't know. "
                "Keep the answer concise and cite the context.\\n\\n"
                "Question: {question}\\n\\n"
                "Context: {context}\\n\\n"
                "Answer:"
            )
            
            try:
                # Use main LLM engine for answer generation
                prompt_text = answer_prompt.format(question=question, context=context)
                result = self.llm_engine.invoke({"query": prompt_text})
                
                if hasattr(result, "response"):
                    return result.response
                elif isinstance(result, dict) and "response" in result:
                    return result["response"]
                else:
                    return str(result)
                    
            except Exception as e:
                return f"Error generating answer: {str(e)}"
        
        return StructuredTool.from_function(
            func=generate_answer_from_context,
            name="generate_answer",
            description="Generate final answer using retrieved context"
        )
    
    @computed_field
    @property
    def state_schema(self) -> type[AgenticRAGState]:
        """Computed property for agentic RAG state schema."""
        return AgenticRAGState
    
    @classmethod
    def from_documents(
        cls,
        documents: List[Document], 
        llm_config: LLMConfig,
        embedding_config: Optional[Any] = None,
        **kwargs
    ) -> "AgenticRAGAgent":
        """Create agentic RAG agent from documents using proper factory pattern.
        
        This follows Pydantic best practices by using a classmethod factory
        instead of complex __init__ logic.
        """
        # Create retriever engine from documents
        retriever_engine = BaseRetrieverConfig.from_documents(
            documents=documents,
            embedding_config=embedding_config,
            name="Agentic RAG Retriever"
        )
        
        # Create main LLM engine with agentic prompting
        llm_engine = AugLLMConfig(
            llm_config=llm_config,
            prompt_template=cls._create_agentic_prompt(),
            name="Agentic RAG LLM"
        )
        
        return cls(
            llm_engine=llm_engine,
            retriever_engine=retriever_engine,
            name=kwargs.get('name', 'Agentic RAG Agent'),
            **kwargs
        )
    
    @staticmethod
    def _create_agentic_prompt() -> ChatPromptTemplate:
        """Create agentic reasoning prompt for deciding when to retrieve."""
        return ChatPromptTemplate.from_messages([
            ("system", """You are an intelligent assistant that can decide when to retrieve information.

You have access to these tools:
- retrieve_documents: Search for relevant documents
- grade_documents: Check if retrieved documents are relevant  
- rewrite_query: Improve queries for better retrieval
- generate_answer: Create final answers from context

For each user question, decide whether to:
1. Retrieve documents if you need more information
2. Respond directly if you can answer without retrieval
3. Grade documents if you've retrieved them
4. Rewrite queries if documents aren't relevant
5. Generate final answers when you have good context

Think step by step about what action to take."""),
            ("human", "{query}")
        ])
    
    @staticmethod
    def _create_grading_prompt() -> ChatPromptTemplate:
        """Create prompt for document relevance grading."""
        return ChatPromptTemplate.from_messages([
            ("system", """You are a document relevance grader. Assess whether retrieved documents are relevant to the user question.

Grade documents as:
- "yes" if they contain information that helps answer the question
- "no" if they are not relevant or don't contain useful information

Provide reasoning for your decision."""),
            ("human", """Question: {question}

Retrieved Context: {context}

Grade the relevance of this context to the question.""")
        ])
    
    @staticmethod  
    def _create_rewriting_prompt() -> ChatPromptTemplate:
        """Create prompt for query rewriting."""
        return ChatPromptTemplate.from_messages([
            ("system", """You are a query rewriting expert. Improve queries to get better retrieval results.

Consider:
- Making queries more specific
- Adding relevant keywords
- Clarifying ambiguous terms
- Focusing on key concepts

Explain what changes you made and why."""),
            ("human", """Original query: {original_query}

Feedback on previous results: {feedback}

Rewrite this query for better document retrieval.""")
        ])


# Convenience factory functions
def create_agentic_rag_agent(
    documents: List[Document],
    llm_config: LLMConfig,
    embedding_config: Optional[Any] = None,
    **kwargs
) -> AgenticRAGAgent:
    """Create agentic RAG agent with sensible defaults."""
    return AgenticRAGAgent.from_documents(
        documents=documents,
        llm_config=llm_config, 
        embedding_config=embedding_config,
        **kwargs
    )


def create_memory_aware_agentic_rag(
    documents: List[Document],
    llm_config: LLMConfig,
    memory_config: Optional[Any] = None,
    **kwargs
) -> AgenticRAGAgent:
    """Create agentic RAG with long-term memory capabilities."""
    agent = create_agentic_rag_agent(documents, llm_config, **kwargs)
    
    # Add memory tools if config provided
    if memory_config:
        # Implementation would add memory store/retrieve tools
        pass
    
    return agent