"""Enhanced Memory RAG with ReAct Pattern

RAG system that maintains conversation memory and uses ReAct (Reasoning + Acting)
pattern for complex multi-step queries requiring reasoning and tool use.
"""

import json
from enum import Enum
from typing import Any, Dict, List, Literal, Optional

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig, LLMConfig
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from haive.agents.chain import ChainAgent, flow_with_edges


class MemoryType(str, Enum):
    """Types of memory."""

    SHORT_TERM = "short_term"
    LONG_TERM = "long_term"
    EPISODIC = "episodic"
    SEMANTIC = "semantic"


class ReActStep(str, Enum):
    """ReAct pattern steps."""

    THOUGHT = "thought"
    ACTION = "action"
    OBSERVATION = "observation"
    REFLECTION = "reflection"


class MemoryEntry(BaseModel):
    """Memory entry structure."""

    content: str = Field(description="Memory content")
    memory_type: MemoryType = Field(description="Type of memory")
    timestamp: str = Field(description="When this memory was created")
    relevance_score: float = Field(
        ge=0.0, le=1.0, description="Relevance to current query"
    )
    context_tags: List[str] = Field(default_factory=list, description="Context tags")


class ReActStepResult(BaseModel):
    """Result from a ReAct step."""

    step_type: ReActStep = Field(description="Type of step")
    content: str = Field(description="Step content")
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence in this step")
    next_action: Optional[str] = Field(default=None, description="Next action to take")


class MemoryAnalysis(BaseModel):
    """Memory analysis result."""

    relevant_memories: List[MemoryEntry] = Field(description="Relevant memories found")
    memory_gaps: List[str] = Field(description="Identified knowledge gaps")
    temporal_context: str = Field(description="Temporal context of memories")
    confidence: float = Field(ge=0.0, le=1.0, description="Overall memory confidence")


class EnhancedResponse(BaseModel):
    """Enhanced response with memory integration."""

    answer: str = Field(description="Main answer")
    reasoning_chain: List[ReActStepResult] = Field(description="ReAct reasoning steps")
    memory_used: List[MemoryEntry] = Field(description="Memories used in response")
    new_memories: List[MemoryEntry] = Field(description="New memories to store")
    confidence: float = Field(ge=0.0, le=1.0, description="Response confidence")


def create_enhanced_memory_react_rag(
    documents: List[Document],
    llm_config: Optional[LLMConfig] = None,
    name: str = "Enhanced Memory ReAct RAG",
) -> ChainAgent:
    """Create an enhanced memory-aware RAG with ReAct pattern."""

    if not llm_config:
        llm_config = AzureLLMConfig(
            deployment_name="gpt-4",
            azure_endpoint="${AZURE_OPENAI_API_BASE}",
            api_key="${AZURE_OPENAI_API_KEY}",
        )

    # Step 1: Memory retrieval and analysis
    def analyze_memory(state: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze conversation memory for relevant context."""
        query = state.get("query", "")
        messages = state.get("messages", [])

        # Mock memory analysis - in real implementation would use vector search
        mock_memories = (
            [
                MemoryEntry(
                    content="Previous discussion about machine learning algorithms",
                    memory_type=MemoryType.EPISODIC,
                    timestamp="2024-01-01T10:00:00",
                    relevance_score=0.8,
                    context_tags=["machine_learning", "algorithms"],
                ),
                MemoryEntry(
                    content="User preference for detailed technical explanations",
                    memory_type=MemoryType.SEMANTIC,
                    timestamp="2024-01-01T09:00:00",
                    relevance_score=0.6,
                    context_tags=["user_preference", "technical"],
                ),
            ]
            if len(messages) > 1
            else []
        )

        # Identify gaps in knowledge
        memory_gaps = (
            ["missing recent updates", "lacks specific examples"]
            if mock_memories
            else []
        )

        analysis = MemoryAnalysis(
            relevant_memories=mock_memories,
            memory_gaps=memory_gaps,
            temporal_context=(
                "Continuing conversation" if mock_memories else "New conversation"
            ),
            confidence=0.8 if mock_memories else 0.4,
        )

        return {"memory_analysis": analysis}

    # Step 2: ReAct Thought - initial reasoning
    thought_generator = AugLLMConfig(
        llm_config=llm_config,
        prompt_template=ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """You are using the ReAct pattern (Reasoning + Acting).
            Start with THOUGHT: analyze the query and plan your approach.
            Consider: what information do you need? What steps should you take?""",
                ),
                (
                    "human",
                    """Query: {query}
            Memory Analysis: {memory_analysis}
            
            THOUGHT: What should I think about and plan for this query?""",
                ),
            ]
        ),
        structured_output_model=ReActStepResult,
        output_key="thought_result",
    )

    # Step 3: ReAct Action - determine actions needed
    action_planner = AugLLMConfig(
        llm_config=llm_config,
        prompt_template=ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """Based on your thought, decide what ACTION to take.
            Actions can include: retrieve_documents, search_memory, analyze_context, generate_answer""",
                ),
                (
                    "human",
                    """Query: {query}
            Previous Thought: {thought_result}
            Available Documents: {document_context}
            
            ACTION: What action should I take next?""",
                ),
            ]
        ),
        structured_output_model=ReActStepResult,
        output_key="action_result",
    )

    # Step 4: Action executor
    def execute_action(state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the planned action."""
        action_result = state.get("action_result", {})
        action_content = action_result.get("content", "")
        query = state.get("query", "")

        # Mock action execution based on action type
        if "retrieve" in action_content.lower():
            # Retrieve relevant documents
            relevant_docs = [doc.page_content for doc in documents[:3]]
            observation = f"Retrieved {len(relevant_docs)} relevant documents"
            execution_result = {
                "retrieved_context": "\n\n".join(relevant_docs),
                "action_taken": "document_retrieval",
            }
        elif "search_memory" in action_content.lower():
            # Search memory
            memory_analysis = state.get("memory_analysis", {})
            relevant_memories = memory_analysis.get("relevant_memories", [])
            observation = f"Found {len(relevant_memories)} relevant memories"
            execution_result = {
                "memory_context": json.dumps([m.dict() for m in relevant_memories]),
                "action_taken": "memory_search",
            }
        else:
            # Default context analysis
            observation = "Analyzed available context"
            execution_result = {
                "analysis_result": "Context analyzed",
                "action_taken": "context_analysis",
            }

        return {**execution_result, "observation": observation}

    # Step 5: ReAct Observation - observe action results
    observation_analyzer = AugLLMConfig(
        llm_config=llm_config,
        prompt_template=ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """Analyze the OBSERVATION from your action.
            What did you learn? Is this sufficient to answer the query?""",
                ),
                (
                    "human",
                    """Query: {query}
            Action Taken: {action_result}
            Observation: {observation}
            Retrieved Context: {retrieved_context}
            
            OBSERVATION: What did I learn from this action?""",
                ),
            ]
        ),
        structured_output_model=ReActStepResult,
        output_key="observation_result",
    )

    # Step 6: ReAct Reflection - determine if more steps needed
    reflection_engine = AugLLMConfig(
        llm_config=llm_config,
        prompt_template=ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """REFLECTION: Based on your thought, action, and observation, 
            determine if you have enough information to provide a good answer.
            If not, specify what additional steps are needed.""",
                ),
                (
                    "human",
                    """Query: {query}
            Thought: {thought_result}
            Action: {action_result}
            Observation: {observation_result}
            
            REFLECTION: Do I have enough information to answer well?""",
                ),
            ]
        ),
        structured_output_model=ReActStepResult,
        output_key="reflection_result",
    )

    # Step 7: Answer generator with memory integration
    answer_generator = AugLLMConfig(
        llm_config=llm_config,
        prompt_template=ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """Generate a comprehensive answer using all available information.
            Integrate memory context and reasoning chain into your response.""",
                ),
                (
                    "human",
                    """Query: {query}
            
            Memory Analysis: {memory_analysis}
            ReAct Chain:
            - Thought: {thought_result}
            - Action: {action_result} 
            - Observation: {observation_result}
            - Reflection: {reflection_result}
            
            Retrieved Context: {retrieved_context}
            
            Generate a thoughtful, well-reasoned answer.""",
                ),
            ]
        ),
        output_key="generated_answer",
    )

    # Step 8: Memory updater
    def update_memory(state: Dict[str, Any]) -> Dict[str, Any]:
        """Update memory with new information from this interaction."""
        query = state.get("query", "")
        answer = state.get("generated_answer", "")

        # Create new memory entries
        new_memories = [
            MemoryEntry(
                content=f"Q: {query} A: {answer[:100]}...",
                memory_type=MemoryType.EPISODIC,
                timestamp="2024-01-01T12:00:00",
                relevance_score=0.9,
                context_tags=["recent_interaction"],
            )
        ]

        return {"new_memories": new_memories, "memory_updated": True}

    # Step 9: Response synthesizer
    response_synthesizer = AugLLMConfig(
        llm_config=llm_config,
        prompt_template=ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "Create the final user-facing response with transparency about reasoning",
                ),
                (
                    "human",
                    """Query: {query}
            Generated Answer: {generated_answer}
            Reasoning Chain Available: {thought_result}, {action_result}, {observation_result}
            Memory Integration: {memory_analysis}
            
            Provide a clear, comprehensive response that shows your reasoning process.""",
                ),
            ]
        ),
        structured_output_model=EnhancedResponse,
        output_key="enhanced_response",
    )

    # Step 10: Context preparation
    def prepare_document_context(state: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare document context for the chain."""
        context = "\n\n".join([doc.page_content for doc in documents[:5]])
        return {"document_context": context}

    # Build the enhanced memory ReAct chain
    return flow_with_edges(
        [
            analyze_memory,  # 0: Analyze conversation memory
            prepare_document_context,  # 1: Prepare document context
            thought_generator,  # 2: ReAct Thought
            action_planner,  # 3: ReAct Action planning
            execute_action,  # 4: Execute the action
            observation_analyzer,  # 5: ReAct Observation
            reflection_engine,  # 6: ReAct Reflection
            answer_generator,  # 7: Generate answer
            update_memory,  # 8: Update memory
            response_synthesizer,  # 9: Synthesize final response
        ],
        # Sequential flow through the ReAct pattern
        "0->1",  # Memory analysis → context prep
        "1->2",  # Context → thought
        "2->3",  # Thought → action planning
        "3->4",  # Action planning → execution
        "4->5",  # Execution → observation
        "5->6",  # Observation → reflection
        "6->7",  # Reflection → answer generation
        "7->8",  # Answer → memory update
        "8->9",  # Memory update → final synthesis
    )


def create_simple_memory_react_rag(
    documents: List[Document], llm_config: Optional[LLMConfig] = None
) -> ChainAgent:
    """Create a simplified memory-aware ReAct RAG."""

    if not llm_config:
        llm_config = AzureLLMConfig(
            deployment_name="gpt-4",
            azure_endpoint="${AZURE_OPENAI_API_BASE}",
            api_key="${AZURE_OPENAI_API_KEY}",
        )

    # Simplified memory check
    def check_memory(state: Dict[str, Any]) -> Dict[str, Any]:
        messages = state.get("messages", [])
        has_context = len(messages) > 1
        return {"has_memory_context": has_context}

    # Simple ReAct reasoning
    react_reasoner = AugLLMConfig(
        llm_config=llm_config,
        prompt_template=ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """Use ReAct pattern:
            THOUGHT: What do I need to consider?
            ACTION: What should I do?
            OBSERVATION: What did I learn?
            
            Then provide your answer.""",
                ),
                (
                    "human",
                    """Query: {query}
            Memory Context Available: {has_memory_context}
            Context: {context}
            
            Use ReAct reasoning to answer.""",
                ),
            ]
        ),
        output_key="react_response",
    )

    # Memory-aware answerer
    memory_answerer = AugLLMConfig(
        llm_config=llm_config,
        prompt_template=ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "Provide final answer considering memory context and reasoning",
                ),
                (
                    "human",
                    """Query: {query}
            ReAct Reasoning: {react_response}
            Previous Messages: {messages}
            
            Final answer:""",
                ),
            ]
        ),
        output_key="response",
    )

    # Context preparation
    def add_context(state: Dict[str, Any]) -> Dict[str, Any]:
        context = "\n\n".join([doc.page_content for doc in documents[:3]])
        return {"context": context}

    return ChainAgent(
        check_memory,
        add_context,
        react_reasoner,
        memory_answerer,
        name="Simple Memory ReAct RAG",
    )


def create_memory_react_with_tools(
    documents: List[Document], llm_config: Optional[LLMConfig] = None
) -> ChainAgent:
    """Create memory ReAct RAG with tool integration."""

    if not llm_config:
        llm_config = AzureLLMConfig(
            deployment_name="gpt-4",
            azure_endpoint="${AZURE_OPENAI_API_BASE}",
            api_key="${AZURE_OPENAI_API_KEY}",
        )

    # Tool availability checker
    def check_tools(state: Dict[str, Any]) -> Dict[str, Any]:
        # Mock tool availability
        available_tools = ["search", "calculate", "summarize"]
        return {"available_tools": available_tools}

    # ReAct with tools
    react_with_tools = AugLLMConfig(
        llm_config=llm_config,
        prompt_template=ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """Use ReAct pattern with available tools:
            Available tools: {available_tools}
            
            THOUGHT: Analyze the query
            ACTION: Choose tool or information source
            OBSERVATION: What did you find?
            REFLECTION: Is this sufficient?""",
                ),
                (
                    "human",
                    """Query: {query}
            Memory Context: {messages}
            Document Context: {context}
            
            Use ReAct reasoning with tools to answer.""",
                ),
            ]
        ),
        output_key="response",
    )

    # Context prep
    def add_context(state: Dict[str, Any]) -> Dict[str, Any]:
        context = "\n\n".join([doc.page_content for doc in documents[:3]])
        return {"context": context}

    return ChainAgent(
        check_tools, add_context, react_with_tools, name="Memory ReAct RAG with Tools"
    )


# I/O schema
def get_enhanced_memory_react_io_schema() -> Dict[str, List[str]]:
    """Get I/O schema for enhanced memory ReAct RAG."""
    return {
        "inputs": ["query", "messages", "context"],
        "outputs": [
            "memory_analysis",
            "thought_result",
            "action_result",
            "observation_result",
            "reflection_result",
            "generated_answer",
            "new_memories",
            "enhanced_response",
            "response",
            "messages",
        ],
    }
