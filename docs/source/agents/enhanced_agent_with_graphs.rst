Enhanced Agent Showcase with Graph Visualization
================================================

This page demonstrates the full capabilities of Haive agents with interactive graph visualization, state history tracking, and execution traces.

   <div class="agent-showcase stagger-animation">

   <!-- Climate Research Agent with Full Visualization -->

   <div class="agent-card" data-agent-type="research">

   <div class="agent-header">

   <div class="agent-icon">🌍</div>

   <div>
   <h3 class="agent-title">Climate Research Agent</h3>
   <p class="agent-subtitle">Advanced Environmental Analysis with ReAct</p>
   </div>

   </div>



   <p class="agent-description">

                Sophisticated AI agent that conducts comprehensive climate research using the ReAct (Reasoning + Acting) methodology.
                Watch how the agent iteratively gathers data, reasons about findings, and takes action to build comprehensive reports.
   </p>



   <div class="agent-features">

   <div class="agent-feature">ReAct Workflow</div>

   <div class="agent-feature">Multi-Source Data</div>

   <div class="agent-feature">Iterative Reasoning</div>

   <div class="agent-feature">Visual Tracking</div>
   </div>

   <!-- Agent Graph Visualization -->

   <div id="climate-agent-graph"
   class="agent-graph-container"
   data-agent-graph='{
   "nodes": [
   {"id": "start", "type": "start", "label": "START"},
   {"id": "agent_node", "type": "agent", "label": "Climate Agent", "description": "Main reasoning and planning node"},
   {"id": "tool_node", "type": "tool", "label": "Research Tools", "description": "Access to climate databases, APIs, and web search"},
   {"id": "validation", "type": "validation", "label": "Validate Data", "description": "Check data quality and relevance"},
   {"id": "end", "type": "end", "label": "END"}
   ],
   "edges": [
   {"source": "start", "target": "agent_node"},
   {"source": "agent_node", "target": "validation", "type": "conditional"},
   {"source": "validation", "target": "tool_node"},
   {"source": "tool_node", "target": "agent_node"},
   {"source": "agent_node", "target": "end"}
   ],
   "executionTrace": [
   {"nodeId": "start", "timestamp": "2025-01-08T10:00:00Z"},
   {"nodeId": "agent_node", "fromNodeId": "start", "timestamp": "2025-01-08T10:00:01Z"},
   {"nodeId": "validation", "fromNodeId": "agent_node", "timestamp": "2025-01-08T10:00:02Z"},
   {"nodeId": "tool_node", "fromNodeId": "validation", "timestamp": "2025-01-08T10:00:03Z"},
   {"nodeId": "agent_node", "fromNodeId": "tool_node", "timestamp": "2025-01-08T10:00:05Z"},
   {"nodeId": "end", "fromNodeId": "agent_node", "timestamp": "2025-01-08T10:00:06Z"}
   ]
   }'>
   </div>

   <!-- State History Visualization -->

   <div id="climate-agent-state"
   class="state-history-container"
   data-state-history='[
   {
   "timestamp": "2025-01-08T10:00:00Z",
   "action": "Initialize Agent",
   "description": "Agent initialized with climate research configuration",
   "duration": 100,
   "state": {
   "messages": [],
   "research_scope": "global_warming_trends",
   "data_sources": ["nasa", "noaa", "ipcc"],
   "iteration_count": 0
   }
   },
   {
   "timestamp": "2025-01-08T10:00:01Z",
   "action": "Plan Research",
   "description": "Agent formulated research plan and identified data sources",
   "duration": 500,
   "state": {
   "messages": [{"role": "system", "content": "Plan: Gather temperature data from NASA, analyze trends"}],
   "research_scope": "global_warming_trends",
   "data_sources": ["nasa", "noaa", "ipcc"],
   "iteration_count": 1,
   "current_plan": "Gather NASA temperature data for last decade"
   }
   },
   {
   "timestamp": "2025-01-08T10:00:03Z",
   "action": "Execute Research",
   "description": "Agent gathered temperature data from NASA API",
   "duration": 2000,
   "state": {
   "messages": [
   {"role": "system", "content": "Plan: Gather temperature data from NASA, analyze trends"},
   {"role": "tool", "content": "Retrieved 120 months of global temperature anomaly data"}
   ],
   "research_scope": "global_warming_trends",
   "data_sources": ["nasa", "noaa", "ipcc"],
   "iteration_count": 2,
   "current_plan": "Analyze temperature trends and patterns",
   "collected_data": {
   "nasa_temperature": "120 data points",
   "time_range": "2014-2024"
   }
   }
   },
   {
   "timestamp": "2025-01-08T10:00:06Z",
   "action": "Analyze Findings",
   "description": "Agent analyzed data and generated insights",
   "duration": 1500,
   "state": {
   "messages": [
   {"role": "system", "content": "Plan: Gather temperature data from NASA, analyze trends"},
   {"role": "tool", "content": "Retrieved 120 months of global temperature anomaly data"},
   {"role": "assistant", "content": "Analysis shows 0.8°C warming trend over the decade"}
   ],
   "research_scope": "global_warming_trends",
   "data_sources": ["nasa", "noaa", "ipcc"],
   "iteration_count": 3,
   "current_plan": "Generate comprehensive report",
   "collected_data": {
   "nasa_temperature": "120 data points",
   "time_range": "2014-2024"
   },
   "analysis_results": {
   "warming_trend": "0.8°C per decade",
   "confidence": "95%",
   "statistical_significance": "p < 0.001"
   }
   }
   }
   ]'>
   </div>

   <!-- Execution Trace -->

   <div id="climate-agent-trace"
   class="execution-trace"
   data-execution-trace='[
   {
   "type": "agent",
   "action": "Initialize Research",
   "node": "agent_node",
   "duration": 100,
   "input": {
   "query": "Analyze global temperature trends for the last decade",
   "config": {"research_scope": "global_warming_trends"}
   },
   "output": {
   "plan": "Multi-step research approach using NASA, NOAA, and IPCC data sources",
   "next_action": "tool_call"
   }
   },
   {
   "type": "tool",
   "action": "NASA API Call",
   "node": "tool_node",
   "duration": 2000,
   "input": {
   "api": "nasa_climate",
   "endpoint": "/temperature/global",
   "parameters": {"start_year": 2014, "end_year": 2024}
   },
   "output": {
   "data_points": 120,
   "format": "monthly_anomalies",
   "status": "success"
   }
   },
   {
   "type": "agent",
   "action": "Analyze Data",
   "node": "agent_node",
   "duration": 1500,
   "input": {
   "raw_data": "120 monthly temperature anomaly readings",
   "analysis_type": "trend_detection"
   },
   "output": {
   "trend": "0.8°C warming per decade",
   "confidence": "95%",
   "methodology": "linear regression with error bounds"
   }
   },
   {
   "type": "validation",
   "action": "Validate Results",
   "node": "validation",
   "duration": 300,
   "input": {
   "results": {"trend": "0.8°C warming per decade"},
   "validation_criteria": ["statistical_significance", "data_quality"]
   },
   "output": {
   "validation_status": "passed",
   "quality_score": 0.94,
   "recommendations": "Results are statistically significant and reliable"
   }
   }
   ]'>
   </div>

   <div class="agent-code-preview">

   <div class="agent-code-header">
   <span>Complete Example</span>
   <span class="badge">Python</span>
   </div>

   <div class="agent-code-content">
   from haive.agents.research import ClimateResearchAgent

   # Initialize the agent with ReAct workflow
   agent = ClimateResearchAgent(

       name="climate_researcher",
       research_scope="global_warming_trends",
       data_sources=["nasa", "noaa", "ipcc"],
       max_iterations=5,
       enable_visualization=True

   )

   # Execute research with full tracing
   results = await agent.arun(

       "Analyze global temperature trends for the last decade",
       trace_execution=True,
       save_state_history=True

   )

   # Access execution details
   print(f"Research completed in {results.total_time}ms")
   print(f"Data sources used: {results.sources_accessed}")
   print(f"Key finding: {results.main_conclusion}")

   # Export visualizations
   agent.export_graph("climate_agent_workflow.svg")
   agent.export_state_history("climate_agent_states.json")

   </div>

   </div>



   <div class="agent-actions">
   <a href="/api/haive/agents/research/climate" class="agent-button">
   <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
   <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
   <polyline points="14,2 14,8 20,8"></polyline>
   <line x1="16" y1="13" x2="8" y2="13"></line>
   <line x1="16" y1="17" x2="8" y2="17"></line>
   <polyline points="10,9 9,9 8,9"></polyline>
   </svg>
   View Full API Docs
   </a>
   <a href="/examples/climate_research_notebook.ipynb" class="agent-button agent-button-secondary">
   <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
   <polyline points="16 18 22 12 16 6"></polyline>
   <polyline points="8 6 2 12 8 18"></polyline>
   </svg>
   Interactive Notebook
   </a>
   <a href="/examples/climate_research_live_demo" class="agent-button agent-button-secondary">
   <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
   <circle cx="12" cy="12" r="10"></circle>
   <polygon points="10,8 16,12 10,16 10,8"></polygon>
   </svg>
   Live Demo
   </a>
   </div>

   </div>

   <!-- Supervisor Agent Multi-Agent Coordination -->

   <div class="agent-card" data-agent-type="supervisor">

   <div class="agent-header">

   <div class="agent-icon">👑</div>

   <div>
   <h3 class="agent-title">Supervisor Agent</h3>
   <p class="agent-subtitle">Multi-Agent Coordination & Routing</p>
   </div>

   </div>



   <p class="agent-description">

                Advanced supervisor agent that coordinates multiple specialized agents. Watch how it routes tasks,
                manages conversations, and synthesizes results from different expert agents working together.
   </p>



   <div class="agent-features">

   <div class="agent-feature">Task Routing</div>

   <div class="agent-feature">Agent Coordination</div>

   <div class="agent-feature">Result Synthesis</div>

   <div class="agent-feature">Conversation Management</div>
   </div>

   <!-- Multi-Agent Graph Visualization -->

   <div id="supervisor-agent-graph"
   class="agent-graph-container"
   data-agent-graph='{
   "nodes": [
   {"id": "start", "type": "start", "label": "START"},
   {"id": "supervisor", "type": "agent", "label": "Supervisor", "description": "Main coordination and routing agent"},
   {"id": "routing", "type": "validation", "label": "Route Task", "description": "Determine which specialist agent to use"},
   {"id": "research_agent", "type": "agent", "label": "Research Agent", "description": "Specialized research capabilities"},
   {"id": "analysis_agent", "type": "agent", "label": "Analysis Agent", "description": "Data analysis and insights"},
   {"id": "writing_agent", "type": "agent", "label": "Writing Agent", "description": "Report generation and summarization"},
   {"id": "synthesis", "type": "validation", "label": "Synthesize", "description": "Combine results from multiple agents"},
   {"id": "end", "type": "end", "label": "END"}
   ],
   "edges": [
   {"source": "start", "target": "supervisor"},
   {"source": "supervisor", "target": "routing"},
   {"source": "routing", "target": "research_agent", "type": "conditional"},
   {"source": "routing", "target": "analysis_agent", "type": "conditional"},
   {"source": "routing", "target": "writing_agent", "type": "conditional"},
   {"source": "research_agent", "target": "supervisor"},
   {"source": "analysis_agent", "target": "supervisor"},
   {"source": "writing_agent", "target": "supervisor"},
   {"source": "supervisor", "target": "synthesis"},
   {"source": "synthesis", "target": "end"}
   ],
   "executionTrace": [
   {"nodeId": "start", "timestamp": "2025-01-08T10:00:00Z"},
   {"nodeId": "supervisor", "fromNodeId": "start", "timestamp": "2025-01-08T10:00:01Z"},
   {"nodeId": "routing", "fromNodeId": "supervisor", "timestamp": "2025-01-08T10:00:02Z"},
   {"nodeId": "research_agent", "fromNodeId": "routing", "timestamp": "2025-01-08T10:00:03Z"},
   {"nodeId": "supervisor", "fromNodeId": "research_agent", "timestamp": "2025-01-08T10:00:08Z"},
   {"nodeId": "routing", "fromNodeId": "supervisor", "timestamp": "2025-01-08T10:00:09Z"},
   {"nodeId": "analysis_agent", "fromNodeId": "routing", "timestamp": "2025-01-08T10:00:10Z"},
   {"nodeId": "supervisor", "fromNodeId": "analysis_agent", "timestamp": "2025-01-08T10:00:13Z"},
   {"nodeId": "synthesis", "fromNodeId": "supervisor", "timestamp": "2025-01-08T10:00:14Z"},
   {"nodeId": "end", "fromNodeId": "synthesis", "timestamp": "2025-01-08T10:00:15Z"}
   ]
   }'>
   </div>

   <div class="agent-code-preview">

   <div class="agent-code-header">
   <span>Multi-Agent Setup</span>
   <span class="badge">Python</span>
   </div>

   <div class="agent-code-content">
   from haive.agents.supervisor import SupervisorAgent
   from haive.agents.research import ResearchAgent
   from haive.agents.analysis import AnalysisAgent
   from haive.agents.writing import WritingAgent

   # Initialize specialist agents
   research_agent = ResearchAgent(name="researcher")
   analysis_agent = AnalysisAgent(name="analyst")
   writing_agent = WritingAgent(name="writer")

   # Create supervisor with registered agents
   supervisor = SupervisorAgent(

       name="coordinator",
       registered_agents={
           "research": research_agent,
           "analysis": analysis_agent,
           "writing": writing_agent
       },
       enable_graph_visualization=True

   )

   # Execute complex multi-step task
   result = await supervisor.arun(

       "Research climate change, analyze the data, and write a summary report"

   )

   </div>

   </div>



   <div class="agent-actions">
   <a href="/api/haive/agents/supervisor" class="agent-button">
   <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
   <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
   <polyline points="14,2 14,8 20,8"></polyline>
   <line x1="16" y1="13" x2="8" y2="13"></line>
   <line x1="16" y1="17" x2="8" y2="17"></line>
   <polyline points="10,9 9,9 8,9"></polyline>
   </svg>
   Supervisor Docs
   </a>
   <a href="/examples/multi_agent_coordination.py" class="agent-button agent-button-secondary">
   <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
   <polyline points="16 18 22 12 16 6"></polyline>
   <polyline points="8 6 2 12 8 18"></polyline>
   </svg>
   Multi-Agent Examples
   </a>
   </div>

   </div>

   </div>

Interactive Features
--------------------

   <div class="collapsible-group">

   <div class="collapsible">

   <div class="collapsible-header">
   <h4 class="collapsible-title">🎮 Graph Playback Controls</h4>
   <span class="collapsible-icon">▶</span>
   </div>

   <div class="collapsible-content">
   <p>Interactive graph visualizations with playback controls let you step through agent execution:</p>
   <ul>
   <li><strong>Step Mode:</strong> Click "Step" to advance through each node execution</li>
   <li><strong>Play Mode:</strong> Watch automatic playback of the entire execution flow</li>
   <li><strong>Reset:</strong> Return to the initial state and start over</li>
   <li><strong>Export:</strong> Download the graph as SVG for reports and presentations</li>
   </ul>
   <p>Click on any node in the graph to see detailed information about that step in the process.</p>
   </div>

   </div>

   <div class="collapsible">

   <div class="collapsible-header">
   <h4 class="collapsible-title">📊 State Evolution Tracking</h4>
   <span class="collapsible-icon">▶</span>
   </div>

   <div class="collapsible-content">
   <p>Visual timeline shows how agent state evolves throughout execution:</p>
   <ul>
   <li><strong>Timeline View:</strong> Chronological display of state changes</li>
   <li><strong>Diff Visualization:</strong> See exactly what changed at each step</li>
   <li><strong>Interactive Steps:</strong> Click any timeline item to examine that state</li>
   <li><strong>Performance Metrics:</strong> Duration and timing information for each step</li>
   </ul>
   <p>Green highlights show additions, yellow shows modifications, and red shows removals.</p>
   </div>

   </div>

   <div class="collapsible">

   <div class="collapsible-header">
   <h4 class="collapsible-title">🔍 Execution Trace Analysis</h4>
   <span class="collapsible-icon">▶</span>
   </div>

   <div class="collapsible-content">
   <p>Detailed execution traces provide insight into agent decision-making:</p>
   <ul>
   <li><strong>Input/Output Tracking:</strong> See exactly what data flows between nodes</li>
   <li><strong>Performance Analysis:</strong> Timing and resource usage for each operation</li>
   <li><strong>Error Handling:</strong> Detailed logs of any issues or retries</li>
   <li><strong>Decision Points:</strong> Understand why the agent made specific choices</li>
   </ul>
   <p>Expand any trace step to see the full input and output data for that operation.</p>
   </div>

   </div>

   <div class="collapsible">

   <div class="collapsible-header">
   <h4 class="collapsible-title">🌐 Multi-Agent Coordination</h4>
   <span class="collapsible-icon">▶</span>
   </div>

   <div class="collapsible-content">
   <p>Advanced visualization for multi-agent systems and coordination:</p>
   <ul>
   <li><strong>Agent Communication:</strong> See how agents pass information to each other</li>
   <li><strong>Task Routing:</strong> Understand how the supervisor determines agent assignment</li>
   <li><strong>Parallel Execution:</strong> Visualize concurrent agent operations</li>
   <li><strong>Result Synthesis:</strong> Watch how individual agent outputs are combined</li>
   </ul>
   <p>Each specialist agent maintains its own state while contributing to the shared conversation context.</p>
   </div>

   </div>

   </div>

Debugging and Development
-------------------------

.. note::

   All visualization components are interactive and provide detailed debugging information. Use these tools during development to understand agent behavior and optimize performance.

.. tip::

   Enable ``trace_execution=True`` when running agents to capture detailed execution information for visualization.`

   <div class="section-nav">
   <h3 class="section-nav-title">
   <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
   <path d="M9 11H5a2 2 0 0 0-2 2v7a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7a2 2 0 0 0-2-2h-4m-2-4v16"></path>
   </svg>
   Development Tools
   </h3>

   <div class="section-nav-grid">
   <a href="/guides/debugging-agents" class="section-nav-item">

   <div class="section-nav-item-title">Debugging Guide</div>

   <div class="section-nav-item-desc">Learn to debug and optimize agent performance</div>
   </a>
   <a href="/guides/custom-visualizations" class="section-nav-item">

   <div class="section-nav-item-title">Custom Visualizations</div>

   <div class="section-nav-item-desc">Create your own visualization components</div>
   </a>
   <a href="/guides/performance-analysis" class="section-nav-item">

   <div class="section-nav-item-title">Performance Analysis</div>

   <div class="section-nav-item-desc">Monitor and optimize agent execution speed</div>
   </a>
   <a href="/guides/state-management" class="section-nav-item">

   <div class="section-nav-item-title">State Management</div>

   <div class="section-nav-item-desc">Best practices for agent state design</div>
   </a>
   </div>

   </div>
