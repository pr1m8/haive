Core Concepts
=============

Agents
------

Agents are the fundamental building blocks of Haive. They combine:

- **LLM Engine**: The language model that powers reasoning
- **Tools**: External capabilities the agent can use
- **Memory**: State management and conversation history
- **Graph**: Workflow orchestration

Agent Types
^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Agent Type
     - Description
   * - SimpleAgent
     - Basic conversational agent with prompt templates
   * - ReactAgent
     - Reasoning agent that can use tools and plan actions
   * - RAGAgent
     - Retrieval-augmented generation for knowledge-based Q&A
   * - MultiAgent
     - Orchestrates multiple agents working together

State Management
----------------

Haive uses structured state schemas to manage agent data:

- **MessagesState**: Conversation history
- **MetaStateSchema**: Meta-capable agent state
- **Custom States**: Define your own Pydantic models

Tools and Toolkits
------------------

Tools extend agent capabilities:

- **Built-in Tools**: Web search, calculators, file operations
- **Custom Tools**: Create your own with the `@tool` decorator
- **Toolkits**: Collections of related tools