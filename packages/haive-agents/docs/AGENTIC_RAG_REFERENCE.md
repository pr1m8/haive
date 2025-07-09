# Agentic RAG Reference (LangChain/LangGraph Tutorial)

## Overview

Reference implementation of Agentic RAG from LangChain/LangGraph tutorial. This shows how to build a retrieval agent that can **decide when to retrieve** context from a vectorstore or respond directly to the user.

**Key Components:**

- **Document preprocessing** and vectorstore indexing
- **Retriever tool** creation
- **Agentic decision making** (retrieve vs respond)
- **Document grading** for relevance
- **Question rewriting** for better retrieval
- **Final answer generation**

## Architecture Flow

```
User Query → Generate/Respond Node → Tool Decision
                     ↓
             [Use Retriever Tool?]
                ↙        ↘
        Retrieve Docs    Direct Response
             ↓               ↓
        Grade Documents     END
             ↓
     [Relevant Documents?]
          ↙        ↘
   Generate Answer  Rewrite Question
        ↓               ↓
       END          Loop Back
```

## Implementation Steps

### 1. Document Preprocessing

```python
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Fetch documents
urls = [
    "https://lilianweng.github.io/posts/2024-11-28-reward-hacking/",
    "https://lilianweng.github.io/posts/2024-07-07-hallucination/",
    "https://lilianweng.github.io/posts/2024-04-12-diffusion-video/",
]

docs = [WebBaseLoader(url).load() for url in urls]

# Split into chunks
docs_list = [item for sublist in docs for item in sublist]
text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=100, chunk_overlap=50
)
doc_splits = text_splitter.split_documents(docs_list)
```

### 2. Create Retriever Tool

```python
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain.tools.retriever import create_retriever_tool

# Create vectorstore and retriever
vectorstore = InMemoryVectorStore.from_documents(
    documents=doc_splits, embedding=OpenAIEmbeddings()
)
retriever = vectorstore.as_retriever()

# Create retriever tool
retriever_tool = create_retriever_tool(
    retriever,
    "retrieve_blog_posts",
    "Search and return information about Lilian Weng blog posts.",
)
```

### 3. Generate Query or Respond Node

```python
from langgraph.graph import MessagesState
from langchain.chat_models import init_chat_model

response_model = init_chat_model("openai:gpt-4.1", temperature=0)

def generate_query_or_respond(state: MessagesState):
    """Call the model to generate a response based on the current state.
    Given the question, it will decide to retrieve using the retriever tool,
    or simply respond to the user.
    """
    response = (
        response_model
        .bind_tools([retriever_tool])
        .invoke(state["messages"])
    )
    return {"messages": [response]}
```

### 4. Document Grading

```python
from pydantic import BaseModel, Field
from typing import Literal

GRADE_PROMPT = (
    "You are a grader assessing relevance of a retrieved document to a user question. \\n "
    "Here is the retrieved document: \\n\\n {context} \\n\\n"
    "Here is the user question: {question} \\n"
    "If the document contains keyword(s) or semantic meaning related to the user question, grade it as relevant. \\n"
    "Give a binary score 'yes' or 'no' score to indicate whether the document is relevant to the question."
)

class GradeDocuments(BaseModel):
    """Grade documents using a binary score for relevance check."""
    binary_score: str = Field(
        description="Relevance score: 'yes' if relevant, or 'no' if not relevant"
    )

grader_model = init_chat_model("openai:gpt-4.1", temperature=0)

def grade_documents(
    state: MessagesState,
) -> Literal["generate_answer", "rewrite_question"]:
    """Determine whether the retrieved documents are relevant to the question."""
    question = state["messages"][0].content
    context = state["messages"][-1].content

    prompt = GRADE_PROMPT.format(question=question, context=context)
    response = (
        grader_model
        .with_structured_output(GradeDocuments)
        .invoke([{"role": "user", "content": prompt}])
    )
    score = response.binary_score

    if score == "yes":
        return "generate_answer"
    else:
        return "rewrite_question"
```

### 5. Question Rewriting

```python
REWRITE_PROMPT = (
    "Look at the input and try to reason about the underlying semantic intent / meaning.\\n"
    "Here is the initial question:"
    "\\n ------- \\n"
    "{question}"
    "\\n ------- \\n"
    "Formulate an improved question:"
)

def rewrite_question(state: MessagesState):
    """Rewrite the original user question."""
    messages = state["messages"]
    question = messages[0].content
    prompt = REWRITE_PROMPT.format(question=question)
    response = response_model.invoke([{"role": "user", "content": prompt}])
    return {"messages": [{"role": "user", "content": response.content}]}
```

### 6. Answer Generation

```python
GENERATE_PROMPT = (
    "You are an assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer the question. "
    "If you don't know the answer, just say that you don't know. "
    "Use three sentences maximum and keep the answer concise.\\n"
    "Question: {question} \\n"
    "Context: {context}"
)

def generate_answer(state: MessagesState):
    """Generate an answer."""
    question = state["messages"][0].content
    context = state["messages"][-1].content
    prompt = GENERATE_PROMPT.format(question=question, context=context)
    response = response_model.invoke([{"role": "user", "content": prompt}])
    return {"messages": [response]}
```

### 7. Graph Assembly

```python
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition

workflow = StateGraph(MessagesState)

# Define nodes
workflow.add_node(generate_query_or_respond)
workflow.add_node("retrieve", ToolNode([retriever_tool]))
workflow.add_node(rewrite_question)
workflow.add_node(generate_answer)

# Entry point
workflow.add_edge(START, "generate_query_or_respond")

# Decide whether to retrieve
workflow.add_conditional_edges(
    "generate_query_or_respond",
    tools_condition,
    {
        "tools": "retrieve",  # If tool calls → retrieve
        END: END,            # Otherwise → end
    },
)

# After retrieval, grade documents
workflow.add_conditional_edges(
    "retrieve",
    grade_documents,  # Returns "generate_answer" or "rewrite_question"
)

# Connect final nodes
workflow.add_edge("generate_answer", END)
workflow.add_edge("rewrite_question", "generate_query_or_respond")

# Compile
graph = workflow.compile()
```

### 8. Execution Example

```python
for chunk in graph.stream({
    "messages": [{
        "role": "user",
        "content": "What does Lilian Weng say about types of reward hacking?",
    }]
}):
    for node, update in chunk.items():
        print("Update from node", node)
        update["messages"][-1].pretty_print()
        print("\\n\\n")
```

**Sample Output:**

```
Update from node generate_query_or_respond
Tool Calls: retrieve_blog_posts(query="types of reward hacking")

Update from node retrieve
Retrieved relevant content about reward hacking types...

Update from node generate_answer
Lilian Weng categorizes reward hacking into two types: environment or goal misspecification, and reward tampering...
```

## Key Design Patterns

### 1. **Agentic Decision Making**

- LLM decides whether to use retriever tool or respond directly
- Uses `bind_tools()` to give model access to retrieval capability
- `tools_condition` routes based on whether tool calls were made

### 2. **Document Relevance Grading**

- Structured output with `GradeDocuments` Pydantic model
- Binary relevance scoring ("yes"/"no")
- Conditional routing based on relevance

### 3. **Query Improvement Loop**

- Irrelevant documents trigger question rewriting
- Rewritten question goes back to generation node
- Creates feedback loop for better retrieval

### 4. **Clean State Management**

- Uses `MessagesState` with message list
- Each node updates state by appending messages
- Tool calls and responses preserved in message history

## Haive Implementation Considerations

### Using Base Agent Patterns

```python
class AgenticRAGAgent[TInput: BaseModel, TOutput: BaseModel](
    ReActAgent[TInput, TOutput],
    ToolRouteMixin
):
    """Agentic RAG using proper Haive patterns."""

    # Retrieval engine
    retriever_engine: BaseRetrieverConfig = Field(...)

    # Document grader model
    grader_model: Optional[AugLLMConfig] = Field(default=None)

    @model_validator(mode="after")
    def setup_agentic_rag(self) -> "AgenticRAGAgent":
        """Setup agentic RAG with retrieval tools."""
        # Add retriever as tool
        retriever_tool = self.retriever_engine.to_tool(
            name="retrieve_documents",
            description="Search and retrieve relevant documents"
        )

        # Set up tool routing
        self.add_routed_tool(retriever_tool, "retriever")

        # Add document grading tools
        grading_tools = self._create_grading_tools()
        for tool in grading_tools:
            self.add_routed_tool(tool, "function")

        return self

    def _create_grading_tools(self) -> List[BaseTool]:
        """Create document grading and query rewriting tools."""
        def grade_documents(context: str, question: str) -> str:
            """Grade document relevance using structured output."""
            # Use grader_model to assess relevance
            # Return "relevant" or "irrelevant"

        def rewrite_question(original_question: str) -> str:
            """Rewrite question for better retrieval."""
            # Use main LLM to rewrite question

        return [
            StructuredTool.from_function(func=grade_documents, name="grade_docs"),
            StructuredTool.from_function(func=rewrite_question, name="rewrite_query")
        ]
```

### Benefits Over Manual Implementation

1. **Proper Type Safety** - Generic type bounds ensure compatibility
2. **Tool Route Management** - Automatic tool routing and validation
3. **Schema Composition** - Leverages base agent schema derivation
4. **Engine Management** - Multiple engines (LLM + retriever + grader)
5. **Extensibility** - Easy to add more tools and capabilities

This reference shows the power of agentic RAG - combining ReAct reasoning patterns with retrieval capabilities for more intelligent information access.
