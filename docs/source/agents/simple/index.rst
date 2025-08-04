.. title:: SimpleAgent - Basic Conversational Agent
.. _simple-agent:

💬 SimpleAgent Documentation
=============================

.. raw:: html

   .. raw:: html

   <div class="agent-hero-section">

.. raw:: html

   <div class="hero-content">
   <h2>💬 Basic Conversational Agent</h2>
   <p class="hero-description">
   SimpleAgent is the foundation for conversational AI in Haive. Perfect for straightforward interactions,
   question-answering, and basic task completion with full memory and context management.
   </p>
   </div>

.. raw:: html

   </div>

Overview
--------

SimpleAgent is designed to be the most straightforward agent implementation while still providing powerful conversational capabilities. It's ideal for:

- General conversation and chat applications
- Question-answering systems
- Simple task automation
- Building blocks for more complex agents
- Quick prototyping and testing

.. raw:: html

   .. raw:: html

   <div class="showcase-section">

.. raw:: html

   <div class="showcase-header">
   <h2>✨ Key Features</h2>
   </div>

.. raw:: html

   <div class="api-grid">

.. raw:: html

   <div class="api-section">
   <h4>🧠 Core Capabilities</h4>
   <ul>
   <li>Natural language understanding</li>
   <li>Context-aware responses</li>
   <li>Conversation history tracking</li>
   <li>Customizable system prompts</li>
   </ul>
   </div>

.. raw:: html

   <div class="api-section">
   <h4>💾 Memory Management</h4>
   <ul>
   <li>Short-term conversation memory</li>
   <li>Long-term state persistence</li>
   <li>Context window optimization</li>
   <li>Memory retrieval patterns</li>
   </ul>
   </div>

.. raw:: html

   <div class="api-section">
   <h4>🔧 Configuration</h4>
   <ul>
   <li>Temperature control</li>
   <li>Response length limits</li>
   <li>Custom prompt templates</li>
   <li>Model selection</li>
   </ul>
   </div>

.. raw:: html

   </div>
   </div>

Quick Start
-----------

.. raw:: html

   .. raw:: html

   <div class="code-example-section">
   <h4>🚀 Basic Usage</h4>

.. code-block:: python

   from haive.agents.simple import SimpleAgent
   from haive.core.engine.aug_llm import AugLLMConfig

   # Create a simple conversational agent
   agent = SimpleAgent(
   name="assistant",
   engine=AugLLMConfig(
   temperature=0.7,
   max_tokens=1000,
   system_message="You are a helpful AI assistant."
   )
   )

   # Synchronous usage
   response = agent.run("What's the weather like today?")
   print(response)

   # Asynchronous usage
   async def chat():
   response = await agent.arun("Tell me a joke about programming")
   print(response)

   # Conversation with context
   agent.run("My name is Alice")
   response = agent.run("What's my name?")
   # Response will remember "Alice"

   .. raw:: html

   </div>

   Advanced Configuration
   ----------------------

   .. raw:: html

   .. raw:: html

   <div class="custom-section">
   <h3>⚙️ Configuration Options</h3>

.. code-block:: python

   from haive.agents.simple import SimpleAgent
   from haive.core.engine.aug_llm import AugLLMConfig
   from langchain_core.prompts import ChatPromptTemplate

   # Custom prompt template
   custom_prompt = ChatPromptTemplate.from_messages([
   ("system", """You are an expert {domain} assistant.
   Always provide accurate, helpful information.
   Use a {tone} tone in your responses."""),
   ("human", "{input}")
   ])

   # Advanced configuration
   agent = SimpleAgent(
   name="expert_assistant",
   engine=AugLLMConfig(
   model="gpt-4",                    # Specific model
   temperature=0.3,                  # Lower for consistency
   max_tokens=2000,                  # Longer responses
   presence_penalty=0.6,             # Encourage variety
   frequency_penalty=0.3,            # Reduce repetition
   top_p=0.95,                       # Nucleus sampling
   system_message="Expert assistant"
   ),
   prompt_template=custom_prompt,
   prompt_variables={
   "domain": "Python programming",
   "tone": "professional but friendly"
   }
   )

   # Using with structured output
   from pydantic import BaseModel

   class AnalysisResult(BaseModel):
   summary: str
   key_points: list[str]
   sentiment: str
   confidence: float

   structured_agent = SimpleAgent(
   name="analyzer",
   engine=AugLLMConfig(),
   structured_output_model=AnalysisResult
   )

   result = await structured_agent.arun(
   "Analyze this customer feedback: The product is great but shipping was slow."
   )
   # result is now an AnalysisResult instance

   .. raw:: html

   </div>

   Memory and State Management
   ---------------------------

   .. raw:: html

   .. raw:: html

   <div class="showcase-section">

   .. raw:: html

   <div class="showcase-header">
   <h2>🧠 Memory Patterns</h2>
   </div>

.. code-block:: python

   # Memory management example
   agent = SimpleAgent(

       name="memory_agent",
       engine=AugLLMConfig(),
       memory_config={
           "max_history": 20,              # Keep last 20 exchanges
           "summarize_after": 10,          # Summarize after 10 messages
           "persist_to_disk": True,        # Save conversations
           "persistence_path": "./memory"  # Where to save
       }

   )

   # Long conversation management
   for i in range(30):

       response = agent.run(f"Message {i}: Tell me fact #{i} about Python")
       print(f"Exchange {i}: {len(agent.conversation_history)} messages in memory")

   # Access conversation history
   history = agent.get_conversation_history()
   for msg in history[-5:]:  # Last 5 messages

       print(f"{msg.type}: {msg.content[:50]}...")

   # Clear memory
   agent.clear_memory()

   # Load from saved state
   agent.load_memory("conversation_123.json")

   .. raw:: html

   </div>

   Integration Patterns
   --------------------

   .. raw:: html

   .. raw:: html

   <div class="api-grid">

   .. raw:: html

   <div class="api-section">
   <h4>🔗 As a Tool</h4>

.. code-block:: python



      # Convert agent to tool for other agents
      expert_tool = SimpleAgent.as_tool(
          name="python_expert",
          description="Ask Python programming questions",
          engine=AugLLMConfig(
              system_message="You are a Python expert."
          )
      )



      # Use in ReactAgent
      from haive.agents.react import ReactAgent

      react_agent = ReactAgent(
          name="researcher",
          tools=[expert_tool]
      )


      .. raw:: html

      </div>

      .. raw:: html

      <div class="api-section">
      <h4>🌐 In Multi-Agent Systems</h4>

.. code-block:: python



      # Part of multi-agent workflow
      from haive.agents.multi import SequentialAgent



      agents = [
          SimpleAgent(name="greeter", engine=config),
          SimpleAgent(name="helper", engine=config),
          SimpleAgent(name="closer", engine=config)
      ]



      workflow = SequentialAgent(
          name="support_flow",
          agents=agents
      )


      .. raw:: html

      </div>

      .. raw:: html

      </div>

      Best Practices
      --------------

      .. raw:: html

      .. raw:: html

      <div class="best-practices">
      <h3>💡 Best Practices for SimpleAgent</h3>
      <ul>
      <li><strong>Start Simple</strong>: Begin with default configuration and customize as needed</li>
      <li><strong>Manage Context</strong>: Monitor conversation length and summarize when needed</li>
      <li><strong>Use System Messages</strong>: Set clear instructions in system_message for consistent behavior</li>
      <li><strong>Handle Errors</strong>: Implement try-catch blocks for production use</li>
      <li><strong>Test Incrementally</strong>: Test each configuration change separately</li>
      </ul>
      </div>

      Troubleshooting
      ---------------

      .. raw:: html

      .. raw:: html

      <div class="warning-section">
      <h3>⚠️ Common Issues and Solutions</h3>

.. code-block:: python

   # Issue: Agent not remembering context
   # Solution: Check memory configuration
   agent = SimpleAgent(
   name="assistant",
   engine=AugLLMConfig(),
   memory_config={"max_history": 50}  # Increase history
   )

   # Issue: Responses too long/short
   # Solution: Adjust max_tokens
   agent.engine.max_tokens = 500  # Shorter responses

   # Issue: Inconsistent behavior
   # Solution: Lower temperature
   agent.engine.temperature = 0.1  # More deterministic

   # Issue: Rate limiting
   # Solution: Add retry logic
   from tenacity import retry, wait_exponential

   @retry(wait=wait_exponential(multiplier=1, min=4, max=10))
   async def safe_query(agent, query):
   return await agent.arun(query)

   .. raw:: html

   </div>

   API Reference
   -------------

   .. autoclass:: haive.agents.simple.SimpleAgent

   :members:
   :inherited-members:
   :show-inheritance:

   Complete Example
   ----------------

   .. raw:: html

   .. raw:: html

   <div class="code-example-section">
   <h4>🎯 Full Working Example</h4>

.. code-block:: python

   import asyncio
   from haive.agents.simple import SimpleAgent
   from haive.core.engine.aug_llm import AugLLMConfig
   from pydantic import BaseModel
   from typing import List

   # Define structured output
   class ConversationSummary(BaseModel):
   topic: str
   key_points: List[str]
   sentiment: str
   follow_up_questions: List[str]

   async def main():
   # Create agent with all features
   agent = SimpleAgent(
   name="conversation_analyst",
   engine=AugLLMConfig(
   model="gpt-4",
   temperature=0.7,
   system_message="""You are a conversation analyst.
   Provide helpful, accurate analysis of conversations."""
   ),
   memory_config={
   "max_history": 100,
   "persist_to_disk": True
   }
   )

   # Have a conversation
   print("Starting conversation...")

   await agent.arun("Hi! I'm interested in learning Python for data science.")
   await agent.arun("What are the most important libraries I should learn?")
   await agent.arun("How long does it typically take to become proficient?")
   await agent.arun("Can you recommend some good learning resources?")

   # Analyze the conversation
   summary_agent = SimpleAgent(
   name="summarizer",
   engine=AugLLMConfig(temperature=0.3),
   structured_output_model=ConversationSummary
   )

   history = agent.get_conversation_history()
   conversation_text = "\n".join([f"{msg.type}: {msg.content}" for msg in history])

   summary = await summary_agent.arun(
   f"Analyze this conversation:\n{conversation_text}"
   )

   print(f"\nConversation Analysis:")
   print(f"Topic: {summary.topic}")
   print(f"Sentiment: {summary.sentiment}")
   print(f"Key Points:")
   for point in summary.key_points:
   print(f"  - {point}")
   print(f"\nFollow-up Questions:")
   for question in summary.follow_up_questions:
   print(f"  - {question}")

   if __name__ == "__main__":
   asyncio.run(main())

   .. raw:: html

   </div>

   Next Steps
   ----------

   .. raw:: html

   .. raw:: html

   <div class="showcase-section">

   .. raw:: html

   <div class="showcase-header">
   <h2>🚀 Where to Go From Here</h2>
   </div>

   .. raw:: html

   <div class="agent-showcase">

   .. raw:: html

   <div class="agent-card">

   .. raw:: html

   <div class="agent-header">

   .. raw:: html

   <div class="agent-emoji">🧠</div>

   .. raw:: html

   <div>
   <h3 class="agent-title">Upgrade to ReactAgent</h3>
   <p class="agent-subtitle">Add tool usage and reasoning</p>
   </div>

   .. raw:: html

   </div>
   <p class="agent-description">

               When you need agents that can use tools and perform multi-step reasoning, upgrade to ReactAgent.
   .. raw:: html

   </p>
   <a href="../react/index.html" class="agent-link">Learn ReactAgent</a>
   </div>

   .. raw:: html

   <div class="agent-card">

   .. raw:: html

   <div class="agent-header">

   .. raw:: html

   <div class="agent-emoji">🌐</div>

   .. raw:: html

   <div>
   <h3 class="agent-title">Build Multi-Agent Systems</h3>
   <p class="agent-subtitle">Coordinate multiple SimpleAgents</p>
   </div>

   .. raw:: html

   </div>
   <p class="agent-description">

               Combine multiple SimpleAgents to create sophisticated workflows and conversations.
   .. raw:: html

   </p>
   <a href="../multi/index.html" class="agent-link">Multi-Agent Guide</a>
   </div>

   .. raw:: html

   <div class="agent-card">

   .. raw:: html

   <div class="agent-header">

   .. raw:: html

   <div class="agent-emoji">📚</div>

   .. raw:: html

   <div>
   <h3 class="agent-title">Add RAG Capabilities</h3>
   <p class="agent-subtitle">Ground responses in knowledge</p>
   </div>

   .. raw:: html

   </div>
   <p class="agent-description">

               Enhance SimpleAgent with retrieval-augmented generation for knowledge-based responses.
   .. raw:: html

   </p>
   <a href="../rag/index.html" class="agent-link">Explore RAG</a>
   </div>
   </div>
   </div>

   .. seealso::

   - :doc:`../../guides/building_agents` - Complete guide to building custom agents
   - :doc:`../../examples/simple_agent_examples` - More SimpleAgent examples
   - :doc:`../index` - Back to agent overview
