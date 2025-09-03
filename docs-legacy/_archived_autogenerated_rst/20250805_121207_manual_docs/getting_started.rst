.. _getting-started:

#################
Getting Started
###############

   <div class="hero-section">

   <div class="hero-content">
   <h2>Build Your First AI Agent in 5 Minutes</h2>
   <p class="hero-description">
   From installation to your first intelligent agent - we'll guide you every step of the way.

   </p>

   <div class="quick-stats">

   <div class="stat">

   <div class="stat-icon">⏱️</div>

   <div class="stat-text">
   <strong>5 min</strong>
   <span>to first agent</span>
   </div>

   </div>

   <div class="stat">

   <div class="stat-icon">📝</div>

   <div class="stat-text">
   <strong>10 lines</strong>
   <span>of code</span>
   </div>

   </div>

   <div class="stat">

   <div class="stat-icon">🔧</div>

   <div class="stat-text">
   <strong>Zero</strong>
   <span>configuration</span>
   </div>

   </div>
   </div>
   </div>
   </div>

   <style>

     .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 16px;
        padding: 3rem 2rem;
        margin: 2rem 0;
        color: white;
        text-align: center;
     }
     .hero-content h2 {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        font-weight: 700;
     }
     .hero-description {
        font-size: 1.2rem;
        max-width: 600px;
        margin: 0 auto 2rem;
        opacity: 0.95;
     }
     .quick-stats {
        display: flex;
        justify-content: center;
        gap: 3rem;
        flex-wrap: wrap;
     }
     .stat {
        display: flex;
        align-items: center;
        gap: 1rem;
     }
     .stat-icon {
        font-size: 2.5rem;
     }
     .stat-text {
        text-align: left;
     }
     .stat-text strong {
        display: block;
        font-size: 1.5rem;
     }
     .stat-text span {
        opacity: 0.9;
        font-size: 0.9rem;
     }

   </style>

****************
📦 Installation
**************

Choose Your Installation Method



**🎯 Basic Install** (Recommended) Get started with core functionality:

.. code-block:: bash

   pip install haive-core haive-agents

**🎨 Full Install** (All Features) Includes tools, games, and extras:

.. code-block:: bash

   pip install haive-core haive-agents haive-tools haive-games

**🛠️ Development Install** (Contributors) For contributing to Haive:

.. code-block:: bash

   git clone https://github.com/yourusername/haive.git
   cd haive
   poetry install --all-extras

System Requirements



-  🐍 **Python 3.9+**
-  📦 **pip or poetry**
-  🔑 **API keys** (optional)
-  💾 **2GB free space**

*********************
🎯 Quick Start Guide
*******************

1. Create Your First Agent



Start with a simple conversational agent:

.. code-block:: python

    # Code example here

   # first_agent.py
   from haive.agents.simple import SimpleAgent
   from haive.core.engine.aug_llm import AugLLMConfig
   import os

   def create_my_first_agent():
       """Create a simple conversational agent."""
       # Get API key from environment
       api_key = os.getenv("OPENAI_API_KEY")
       if not api_key:
           raise ValueError("Please set OPENAI_API_KEY environment variable")

       # Create agent with configuration
       agent = SimpleAgent(
           name="My First Agent",
           engine=AugLLMConfig(
               model="gpt-4",
               temperature=0.7,
               api_key=api_key
           ),
           description="A helpful assistant"
       )
       return agent

   def main():
       """Demo function."""
       try:
           # Create the agent
           print("🚀 Creating your first Haive agent...")
           agent = create_my_first_agent()

           # Example 1: Simple question
           response = agent.invoke("What is the capital of France?")
           print(f"Agent: {response}")

           # Example 2: Complex reasoning
           response = agent.invoke(
               "Compare the populations of Tokyo, New York, and London."
           )
           print(f"Agent: {response}")

       except Exception as e:
           print(f"❌ Error: {e}")
           print("💡 Tip: Set your OPENAI_API_KEY environment variable")

   if __name__ == "__main__":
       main()

2. Run Your Agent



.. code-block:: bash

   # Set your API key
   export OPENAI_API_KEY="your-api-key-here"

   # Run the script
   python first_agent.py

Expected Output:

.. code-block:: text

   🚀 Creating your first Haive agent...
   Agent: The capital of France is Paris.
   Agent: Tokyo has the largest population at approximately 37 million...

3. Next Steps



Now that you have your first agent running, explore:

-  **Multi-Agent Systems**: :doc:`guides/multi_agents`

`
-  **RAG Agents**: :doc`:`guides/rag_agents`

`
-  **Tool Integration**: :doc`:`guides/tools`

`
-  **Game Environments**: :doc`:`games/index`

`

****************
🔗 Useful Links
**************

-  **API Reference**: :doc`:`api/index`

`
-  **Examples Gallery**: :doc`:`examples/index`

`
-  **Agent Showcase**: :doc`:`agents/index`

`
-  **Tools Catalog**: :doc`:`tools/index`

`

************
Need Help?
**********

-  Check our :doc`:`guides/index for detailed tutorials`

`
-  Browse :doc`:`examples/index for working code samples`

`
-  Review the :doc`:`api/index for complete API documentation`

`

.. note::


   🔑 **API Key Setup**: Most examples require an OpenAI API key. Set it
   with:

   .. code-block:: bash

      export OPENAI_API_KEY="your-api-key-here"
`
