Agents
======

.. raw:: html

    <div class="module-header">
        <h1>🤖 AI Agents</h1>
        <p class="subtitle">Build and deploy intelligent AI agents with different reasoning strategies</p>
    </div>

Available Agents
--------------

.. grid:: 2 2 2 3
    :gutter: 3
    :padding: 4
    :class-container: agents-grid

    .. grid-item-card:: ReAct Agent
        :link: react_agent/index
        :class-card: agent-card

        Reasoning and Acting framework for iterative task completion.

    .. grid-item-card:: Plan and Execute
        :link: plan_and_execute/index
        :class-card: agent-card

        Hierarchical planning and execution for complex tasks.

    .. grid-item-card:: Tree of Thought
        :link: tot/index
        :class-card: agent-card

        Advanced decision-making with branching reasoning paths.

    .. grid-item-card:: Self Discover
        :link: self_discover/index
        :class-card: agent-card

        Autonomous exploration and learning capabilities.

    .. grid-item-card:: Web Navigation
        :link: web_nav/index
        :class-card: agent-card

        Browse and extract information from web content.

    .. grid-item-card:: Summarizer
        :link: summarizer/index
        :class-card: agent-card

        Efficient text summarization and content distillation.

Agent Components
-------------

.. toctree::
   :maxdepth: 2
   :hidden:

   react_agent/index
   plan_and_execute/index
   tot/index
   self_discover/index
   web_nav/index
   summarizer/index

Base Classes
----------

.. toctree::
   :maxdepth: 1

   base/agent_architecture
   base/agent_config