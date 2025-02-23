Welcome to Haive
================

.. raw:: html

    <div class="hero">
        <h1>Multi-Agent AI Orchestration Framework</h1>
        <p class="subtitle">Build intelligent, extensible, and scalable AI-driven workflows</p>
        
        <div class="action-buttons">
            <a href="installation.html" class="action-button primary">Quick Start 🚀</a>
            <a href="examples.html" class="action-button secondary">View Examples 💡</a>
        </div>
    </div>

📦 Explore Haive
----------------

.. grid:: 2 2 2 3
    :gutter: 3
    :padding: 4
    :class-container: feature-grid

    .. grid-item-card:: 🤖 Agents
        :link: agents/index
        :link-type: doc
        :class-card: feature-card

        Build autonomous AI agents with different reasoning strategies:  
        **ReAct, Reflexion, Tree of Thought, and more.**

    .. grid-item-card:: 🧠 Core Framework
        :link: core/index
        :link-type: doc
        :class-card: feature-card

        Access **LLMs, vector stores, retrieval systems, and memory**  
        with our powerful core infrastructure.

    .. grid-item-card:: 📊 FLSTAESR Pipeline
        :link: flstaesr/index
        :link-type: doc
        :class-card: feature-card

        Process and structure data efficiently with **document loaders,  
        retrieval-augmented generation, and embedding strategies.**

    .. grid-item-card:: 🔌 Integrations
        :link: integrations/index
        :link-type: doc
        :class-card: feature-card

        Connect with popular AI services, **vector databases, APIs,  
        and retrieval tools.**

    .. grid-item-card:: 📈 Visualization
        :link: visualization/index
        :link-type: doc
        :class-card: feature-card

        Monitor and debug agent workflows using **graph-based  
        visualization tools.**

    .. grid-item-card:: 🛠️ Tools & Utilities
        :link: tools/index
        :link-type: doc
        :class-card: feature-card

        Extend functionality with our **growing collection of modular tools**.

🚀 Why Haive?
------------

.. grid:: 1 1 2 3
    :gutter: 3
    :class-container: why-grid

    .. grid-item-card:: 🌐 Graph-Based Execution
        :class-card: why-card

        Design **flexible AI workflows** using our **graph-based execution engine**,  
        enabling **dynamic routing and complex decision trees.**

    .. grid-item-card:: 🛠 State Management
        :class-card: why-card

        Maintain agent state with **short-term and long-term memory** systems,  
        ensuring context tracking across multiple interactions.

    .. grid-item-card:: ⚡ Real-Time Processing
        :class-card: why-card

        Enable **streaming responses** and **parallel execution**  
        for highly efficient AI workflows.

📝 Quick Example
---------------

Create your first AI agent in minutes:

.. code-block:: python
    :caption: Creating a Simple Agent
    :class: with-copy
    :emphasize-lines: 4,7

    from haive.agents import SummarizerAgent
    from haive.core.config import Config

    # Configure the agent
    config = Config(model="gpt-4")

    # Initialize and run
    agent = SummarizerAgent(config)
    result = agent.summarize("Your text to summarize...")

    print(result)

🔍 Explore Our Modules
----------------------

.. tab-set::

    .. tab-item:: 🤖 Agents
        :sync: agents

        Build autonomous AI agents with different reasoning strategies:

        - **ReAct Agent**: Reasoning and Acting framework
        - **Tree of Thought**: Advanced decision-making
        - **Supervisor**: Monitor and control other agents
        - **Web Navigation**: Browse and extract web content
        - **And many more...**

        🔗 **Learn more in the** [Agents Documentation](agents/index)

    .. tab-item:: 🧠 Core
        :sync: core

        Access essential AI infrastructure:

        - **LLM Management**
        - **Vector Stores & Retrieval**
        - **Memory Systems**
        - **Tool Integration**
        - **State Management**

        🔗 **Explore Core Components** [here](core/index)

    .. tab-item:: 📊 FLSTAESR
        :sync: flstaesr

        Process and structure your data:

        - **Document Loading**
        - **Text Splitting**
        - **Embedding Generation**
        - **Vector Storage**
        - **Semantic Retrieval**

        🔗 **Full FLSTAESR Guide** [available here](flstaesr/index)

🔧 Getting Started
------------------

1️⃣ **Install Haive**:

   .. code-block:: bash

       pip install haive

2️⃣ **Create your first agent**:

   .. code-block:: python

       from haive.agents import ReActAgent
       
       agent = ReActAgent()
       result = agent.run("Your task here...")

3️⃣ **Explore our** :doc:`Examples <examples/index>` **and** :doc:`Documentation <usage>`.

📖 Documentation Navigation
---------------------------

.. toctree::
   :maxdepth: 2
   :caption: 📚 Documentation
   :hidden:

   installation
   tutorials/index
   usage
   contributing/index
   reference/index

.. toctree::
   :maxdepth: 1
   :caption: 🤖 Agents
   :hidden:

   agents/index

.. toctree::
   :maxdepth: 1
   :caption: 🧠 Core Framework
   :hidden:

   core/index

.. toctree::
   :maxdepth: 1
   :caption: 📊 FLSTAESR Pipeline
   :hidden:

   flstaesr/index

.. toctree::
   :maxdepth: 1
   :caption: 🛠 Development
   :hidden:

   contributing/guide
   contributing/development
   contributing/docs
   changelog
