Multi-Agent Systems



Coordinate multiple agents to solve complex problems collaboratively.

.. note::



   This is the user guide for multi-agent systems. For API documentation, see :doc:`/api/haive/agents/multi/index.`
`

Overview



Multi-agent systems in Haive enable sophisticated agent coordination patterns:

- **SequentialMultiAgent** - Agents work in sequence, passing results
- **ParallelMultiAgent** - Agents work simultaneously on sub-tasks
- **HierarchicalMultiAgent** - Supervisor agents manage worker agents
- **CollaborativeMultiAgent** - Agents negotiate and reach consensus

Quick Start



.. code-block:: python

    # Code example here

   from haive.agents.multi import SequentialMultiAgent
   from haive.agents.simple import SimpleAgent
   from haive.agents.react import ReactAgent

   # Create individual agents
   researcher = ReactAgent(name="researcher", tools=[search_tool])
   writer = SimpleAgent(name="writer", system_prompt="You are a technical writer")

   # Create multi-agent system
   multi_agent = SequentialMultiAgent(

       name="research_writer",
       agents=[researcher, writer],
       flow_description="Research topic then write article"

   )

   # Execute workflow
   result = await multi_agent.arun(

       "Write an article about quantum computing"

   )

   Coordination Patterns



   .. grid:: 2


   .. grid-item-card:: Sequential

      :text-align: center

      Agents work in order, each building on previous results

   .. grid-item-card:: Parallel

      :text-align: center

      Agents work simultaneously on different aspects

   .. grid-item-card:: Hierarchical

      :text-align: center

      Supervisor delegates tasks to specialized workers

   .. grid-item-card:: Collaborative

      :text-align: center

      Agents discuss and reach consensus

   Examples



   - Research and Writing Pipeline
   - Customer Support Escalation
   - Code Review System
   - Trading Strategy Committee

   See :doc`:`/guides/multi_agent_systems for detailed examples.`

`

   .. toctree::


   :maxdepth: 2
   :hidden:

   sequential
   parallel
   hierarchical
   collaborative
`
