"""Dynamic Agent Discovery Supervisor with multiple discovery sources.

This module provides DynamicAgentDiscoverySupervisor, an advanced supervisor that can
dynamically discover and add new agents from multiple sources during runtime.

The supervisor supports multiple discovery modes:
- Component Discovery: Framework-based agent discovery
- RAG Discovery: Document-based agent discovery using RAG
- MCP Discovery: External agent discovery via MCP framework
- Hybrid: Combines all discovery methods

Example:
    Basic usage with agent discovery::

        from haive.agents.supervisor.dynamic_agent_discovery_supervisor import (
            DynamicAgentDiscoverySupervisor,
            AgentDiscoveryMode
        )
        from haive.core.engine.aug_llm import AugLLMConfig

        # Create supervisor with initial agents
        config = AugLLMConfig(temperature=0.1)
        initial_agents = {
            "basic_assistant": SimpleAgent(name="basic_assistant", engine=config)
        }

        supervisor = DynamicAgentDiscoverySupervisor(
            name="agent_supervisor",
            agents=initial_agents,
            engine=config,
            discovery_mode=AgentDiscoveryMode.HYBRID
        )

        # Run task - supervisor will discover needed agents
        result = await supervisor.arun("I need an expert to analyze financial data")

    Using factory method with discovery sources::

        supervisor = DynamicAgentDiscoverySupervisor.create_with_discovery(
            name="discovery_supervisof",
            agents=initial_agents,
            engine=config,
            discovery_mode=AgentDiscoveryMode.HYBRID,
            component_discovery_config={"registry_path": "./agents"},
            rag_documents_path="/path/to/agent/docs",
            mcp_config={"endpoint": "http://localhost:8000"}
        )

Note:
    This supervisor requires async execution. Agent discovery happens automatically
    based on task analysis, but can also be triggered manually using the built-in
    discover_and_add_agents tool.

See Also:
    - :class:`haive.agents.react.agent.ReactAgent`
    - :class:`haive.agents.supervisor.dynamic_activation_supervisor.DynamicActivationSupervisor`
    - :class:`haive.agents.react.dynamic_react_agent.DynamicReactAgent`
"""

import logging
from enum import Enum
from typing import Any

from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from pydantic import BaseModel, ConfigDict, Field, model_validator

# Using standard typing instead of Name type
from haive.agents.base.agent import Agent

# from haive.agents.research.perplexity_agent import PerplexityStyleAgent
from haive.agents.discovery.component_discovery_agent import ComponentDiscoveryAgent
from haive.agents.react.agent import ReactAgent
from haive.agents.simple.agent import SimpleAgent
from haive.agents.supervisor.agent import SupervisorState
from haive.agents.supervisor.dynamic_state import SupervisorDecision

# from haive.tools.utility.document_loaders import DirectoryLoader
# from haive.core.models.vectorstore import InMemoryVectorStore
# from haive.core.models.embeddings import OpenAIEmbeddings

logger = logging.getLogger(__name__)


class AgentDiscoveryMode(str, Enum):
    """Enumeration of available agent discovery modes.

    Attributes:
        COMPONENT_DISCOVERY: Use ComponentDiscoveryAgent for framework-based discovery
        RAG_DISCOVERY: Use RAG agent for document-based discovery
        MCP_DISCOVERY: Use MCP framework for external agent discovery
        HYBRID: Combine all discovery methods
    """

    COMPONENT_DISCOVERY = "component_discovery"
    RAG_DISCOVERY = "rag_discovery"
    MCP_DISCOVERY = "mcp_discovery"
    HYBRID = "hybrid"


class AgentCapability(BaseModel):
    """Description of an agent's capabilities."""

    name: str = Field(..., description="Agent name")
    agent_type: str = Field(
        ..., description="Type of agent (SimpleAgent, ReactAgent, etc.)"
    )
    description: str = Field(..., description="What this agent can do")
    specialties: list[str] = Field(
        default_factory=list, description="Areas of expertise"
    )
    tools: list[str] = Field(default_factory=list, description="Tools this agent has")
    requirements: dict[str, Any] = Field(
        default_factory=dict, description="Requirements for creation"
    )


class DynamicAgentDiscoverySupervisor(ReactAgent):
    """Supervisor with dynamic agent discovery and registration capabilities.

    This supervisor extends ReactAgent with the ability to dynamically discover
    new agents from multiple sources and add them to its agent registry. It analyzes
    tasks to determine what type of agents are needed and can discover specialists
    on-demand.

    The supervisor maintains a registry of discovered agents and can route tasks to
    newly discovered agents. Agent discovery happens automatically during task
    execution but can also be triggered manually.

    Attributes:
        discovery_mode (AgentDiscoveryMode): Mode for agent discovery (default: HYBRID)
        discovery_agent (Optional[ComponentDiscoveryAgent]): Agent for component discovery
        rag_discovery_agent (Optional[BaseRAGAgent]): RAG agent for document-based discovery
        mcp_framework (Optional[Dict[str, Any]]): MCP framework configuration
        discovered_agents (Set[str]): Set of discovered agent names
        agent_capabilities (Dict[str, AgentCapability]): Registry of agent capabilities
        max_discovery_attempts (int): Maximum discovery attempts per task (default: 3)
        agent_factory (Dict[str, Type[Agent]]): Registry of agent constructors

    Example:
        Creating a supervisor with agent discovery::

            supervisor = DynamicAgentDiscoverySupervisor(
                name="main_supervisof",
                agents={
                    "generalist": SimpleAgent(name="generalist", engine=config)
                },
                engine=AugLLMConfig(),
                discovery_mode=AgentDiscoveryMode.HYBRID
            )

            # Run task - specialist agents will be discovered as needed
            result = await supervisor.arun("Analyze market trends and write a report")

            # Check discovered agents
            print(f"Discovered agents: {supervisor.discovered_agents}")

    Note:
        - Agent discovery is asynchronous and may take time
        - Discovered agents are cached to avoid redundant discovery
        - The supervisor includes a built-in 'discover_and_add_agents' tool
    """

    model_config = ConfigDict(
        str_strip_whitespace=True, validate_assignment=True, extra="forbid"
    )

    # Discovery configuration
    discovery_mode: AgentDiscoveryMode = Field(
        default=AgentDiscoveryMode.HYBRID, description="Mode for agent discovery"
    )

    # Discovery agents (excluded from serialization)
    discovery_agent: ComponentDiscoveryAgent | None = Field(default=None, exclude=True)
    rag_discovery_agent: Any | None = Field(default=None, exclude=True)  # BaseRAGAgent
    mcp_framework: dict[str, Any] | None = Field(default=None, exclude=True)

    # Agent management
    agents: dict[str, Agent] = Field(
        default_factory=dict, description="Registry of available agents"
    )
    discovered_agents: set[str] = Field(
        default_factory=set, description="Set of discovered agent names"
    )
    agent_capabilities: dict[str, AgentCapability] = Field(
        default_factory=dict, exclude=True
    )
    max_discovery_attempts: int = Field(default=3, ge=1, le=10)

    # Agent factory registry
    agent_factory: dict[str, type[Agent]] = Field(default_factory=dict, exclude=True)

    # Initial agents to register (used during factory creation)
    agents_to_register: list[dict[str, Any]] | None = Field(default=None, exclude=True)

    @model_validator(mode="after")
    @classmethod
    def setup_supervisor(cls) -> "DynamicAgentDiscoverySupervisor":
        """Set up supervisor after initialization."""
        # Register default agent types
        self.agent_factory = {
            "SimpleAgent": SimpleAgent,
            "ReactAgent": ReactAgent,
            # "PerplexityStyleAgent": PerplexityStyleAgent,  # Commented out due to import issues
            # Add more agent types as needed
        }

        # Register initial agents if provided
        if self.agents_to_register:
            for agent_data in self.agents_to_register:
                self._register_discovered_agent(agent_data)
            # Clear after registration
            self.agents_to_register = None

        # Add dynamic agent discovery tool
        self._add_discovery_tool()

        return self

    def _register_discovered_agent(self, agent_data: dict[str, Any]) -> bool:
        """Register a discovered agent in the supervisor.

        Args:
            agent_data: Dictionary containing agent information:
                - name: Agent name
                - agent_type: Type of agent to create
                - description: Agent description
                - config: Agent configuration

        Returns:
            True if agent was successfully registered
        """
        agent_name = agent_data.get("name", "")
        agent_type = agent_data.get("agent_type", "SimpleAgent")

        if agent_name and agent_name not in self.agents:
            # Get agent constructor
            agent_class = self.agent_factory.get(agent_type)
            if not agent_class:
                logger.warning(f"Unknown agent type: {agent_type}")
                return False

            try:
                # Create agent configuration
                config = agent_data.get("config", {})
                if "engine" not in config:
                    config["engine"] = self.engine

                # Create agent instance
                agent = agent_class(name=agent_name, **config)

                # Add to supervisor's agents
                self.agents[agent_name] = agent
                self.discovered_agents.add(agent_name)

                # Store capabilities
                capability = AgentCapability(
                    name=agent_name,
                    agent_type=agent_type,
                    description=agent_data.get("description", ""),
                    specialties=agent_data.get("specialties", []),
                    tools=agent_data.get("tools", []),
                )
                self.agent_capabilities[agent_name] = capability

                logger.info(
                    f"Successfully registered agent: {agent_name} ({agent_type})"
                )
                return True

            except Exception as e:
                logger.exception(f"Failed to create agent {agent_name}: {e}")
                return False

        return False

    def _add_discovery_tool(self) -> None:
        """Add the dynamic agent discovery tool."""

        @tool
        def discover_and_add_agents(task_description: str) -> str:
            """Discover and add agents needed for a specific task.

            This tool analyzes the task description and discovers relevant agents
            from configured sources (component discovery, RAG, MCP).

            Args:
                task_description: Description of the task requiring agents

            Returns:
                Description of discovered and added agents
            """
            discovered = []

            # Component discovery
            if (
                self.discovery_mode
                in [
                    AgentDiscoveryMode.COMPONENT_DISCOVERY,
                    AgentDiscoveryMode.HYBRID,
                ]
                and self.discovery_agent
            ):
                try:
                    components = self.discovery_agent.discover_components(
                        query=f"agents for: {task_description}",
                        component_type="agent",
                    )
                    for comp in components:
                        if self._register_discovered_agent(comp):
                            discovered.append(f"Component: {comp['name']}")
                except Exception as e:
                    discovered.append(f"Component discovery error: {e!s}")

            # RAG discovery
            if self.discovery_mode in [
                AgentDiscoveryMode.RAG_DISCOVERY,
                AgentDiscoveryMode.HYBRID,
            ]:
                if self.rag_discovery_agent:
                    try:
                        # Query RAG agent for agent specifications
                        rag_response = self.rag_discovery_agent.run(
                            f"Find agent specifications or experts that can help with: {task_description}"
                        )
                        # Parse response for agent definitions
                        # This is simplified - real implementation would parse structured output
                        if "agent:" in rag_response.lower():
                            discovered.append(
                                "RAG: Found agent specifications in documents"
                            )
                    except Exception as e:
                        discovered.append(f"RAG discovery error: {e!s}")

            # MCP discovery
            if (
                self.discovery_mode
                in [
                    AgentDiscoveryMode.MCP_DISCOVERY,
                    AgentDiscoveryMode.HYBRID,
                ]
                and self.mcp_framework
            ):
                try:
                    # Query MCP framework for available agents
                    mcp_agents = self.mcp_framework.get(
                        "discover_agents", lambda x: []
                    )(task_description)
                    for agent_def in mcp_agents:
                        if self._register_discovered_agent(agent_def):
                            discovered.append(f"MCP: {agent_def['name']}")
                except Exception as e:
                    discovered.append(f"MCP discovery error: {e!s}")

            if discovered:
                return f"Discovered and added agents: {', '.join(discovered)}"
            return "No new agents discovered for this task"

        # Register the discovery tool if supervisor has engine with tools
        if hasattr(self, "engine") and hasattr(self.engine, "tools"):
            self.engine.tools.append(discover_and_add_agents)

    async def _make_decision(self, state: SupervisorState) -> SupervisorDecision:
        """Make routing decision with agent discovery awareness.

        This method extends the base supervisor's decision-making to consider
        available agents and discover new ones if needed for the task.

        Args:
            state: Current supervisor state

        Returns:
            SupervisorDecision with routing information
        """
        messages = state.messages

        # Check if we should discover agents first
        if len(messages) > 0:
            last_message = messages[-1]
            if isinstance(last_message, HumanMessage):
                # Analyze if task might need specialized agents
                task_content = str(last_message.content).lower()
                specialist_keywords = [
                    "expert",
                    "specialist",
                    "analyze",
                    "research",
                    "financial",
                    "medical",
                    "legal",
                    "technical",
                    "advanced",
                    "complex",
                    "professional",
                ]

                if any(key in task_content for key in specialist_keywords):
                    # Check if we have suitable agents
                    has_specialist = any(
                        cap.specialties for cap in self.agent_capabilities.values()
                    )

                    if not has_specialist and len(self.discovered_agents) < 10:
                        # Suggest agent discovery first
                        return SupervisorDecision(
                            next_agent=self.name,  # Route to self for discovery
                            reasoning="Task appears to require specialized agents. Discovering suitable agents first.",
                            confidence=0.9,
                            suggested_prompt=f"discover_and_add_agents for: {last_message.content}",
                        )

        # Standard routing decision
        decision_prompt = self._create_decision_prompt(state)

        # Use supervisor's LLM for decision
        response = await self.engine.ainvoke(decision_prompt)

        # Parse response into decision
        return self._parse_decision_response(response.content, state)

    def _create_decision_prompt(self, state: SupervisorState) -> str:
        """Create prompt for routing decision."""
        # Get conversation context
        context = self._format_conversation_history(state.messages[-10:])

        # Get available agents and their capabilities
        agent_info = []
        for name, agent in self.agents.items():
            capability = self.agent_capabilities.get(name)
            if capability:
                specialties = (
                    f"Specialties: {', '.join(capability.specialties)}"
                    if capability.specialties
                    else ""
                )
                tools = (
                    f"Tools: {', '.join(capability.tools)}" if capability.tools else ""
                )
                info = f"- {name} ({capability.agent_type}): {capability.description}. {specialties} {tools}"
            else:
                info = f"- {name}: {agent.__class__.__name__}"
            agent_info.append(info)

        prompt = f"""As a supervisor, analyze the conversation and decide which agent should handle the next step.

Conversation history:
{context}

Available agents ({len(self.agents)}):
{chr(10).join(agent_info)}

Discovered agents: {', '.join(self.discovered_agents) or 'none yet'}

Consider:
1. Which agent is best suited for the current task?
2. Do we have the right specialist agents or should we discover more?
3. What expertise does the task require?

Respond with:
- AGENT: [agent_name] - The agent to route to
- REASONING: [explanation] - Why this agent was chosen
- CONFIDENCE: [0.0-1.0] - How confident you are
- PROMPT: [optional] - Suggested prompt for the agent"""

        return prompt

    def _parse_decision_response(
        self, response: str, state: SupervisorState
    ) -> SupervisorDecision:
        """Parse LLM response into routing decision."""
        lines = response.strip().split("\n")

        agent = None
        reasoning = ""
        confidence = 0.8
        prompt = None

        for line in lines:
            line = line.strip()
            if line.startswith("AGENT:"):
                agent = line.replace("AGENT:", "").strip()
            elif line.startswith("REASONING:"):
                reasoning = line.replace("REASONING:", "").strip()
            elif line.startswith("CONFIDENCE:"):
                try:
                    confidence = float(line.replace("CONFIDENCE:", "").strip())
                except:
                    confidence = 0.8
            elif line.startswith("PROMPT:"):
                prompt = line.replace("PROMPT:", "").strip()

        # Default to first agent if parsing fails
        if not agent or agent not in self.agents:
            agent = next(iter(self.agents.keys())) if self.agents else self.name

        return SupervisorDecision(
            next_agent=agent,
            reasoning=reasoning or "Routing based on task analysis",
            confidence=confidence,
            suggested_prompt=prompt,
        )

    # Factory methods

    @classmethod
    def create_with_discovery(
        cls,
        name: str,
        agents: dict[str, Agent],
        engine: AugLLMConfig,
        discovery_mode: AgentDiscoveryMode = AgentDiscoveryMode.HYBRID,
        component_discovery_config: dict[str, Any] | None = None,
        rag_documents_path: str | None = None,
        mcp_config: dict[str, Any] | None = None,
        **kwargs,
    ) -> "DynamicAgentDiscoverySupervisor":
        """Create supervisor with configured discovery sources.

        Args:
            name: Supervisor name
            agents: Initial agents dictionary
            engine: LLM configuration
            discovery_mode: Agent discovery mode
            component_discovery_config: Config for component discovery
            rag_documents_path: Path to agent documentation
            mcp_config: MCP framework configuration
            **kwargs: Additional supervisor arguments

        Returns:
            Configured supervisor with discovery capabilities

        Example:
            Create with all discovery sources::

                supervisor = DynamicAgentDiscoverySupervisor.create_with_discovery(
                    name="full_discovery",
                    agents={"generalist": SimpleAgent(...)},
                    engine=config,
                    discovery_mode=AgentDiscoveryMode.HYBRID,
                    component_discovery_config={"registry_path": "./agents"},
                    rag_documents_path="/docs/agent_specs",
                    mcp_config={"endpoint": "http://mcp.example.com"}
                )
        """
        # Create discovery agent if needed
        discovery_agent = None
        if (
            discovery_mode
            in [
                AgentDiscoveryMode.COMPONENT_DISCOVERY,
                AgentDiscoveryMode.HYBRID,
            ]
            and component_discovery_config
        ):
            discovery_agent = ComponentDiscoveryAgent(**component_discovery_config)

        # Create RAG agent if needed
        rag_discovery_agent = None
        if (
            discovery_mode
            in [
                AgentDiscoveryMode.RAG_DISCOVERY,
                AgentDiscoveryMode.HYBRID,
            ]
            and rag_documents_path
        ):
            # Create simple RAG agent for agent discovery
            # TODO: Re-enable when DirectoryLoader and vectorstore imports are fixed
            # from haive.core.tools import create_retriever_tool

            # # Load documents
            # loader = DirectoryLoader(rag_documents_path)
            # documents = loader.load()

            # # Create vector store
            # embeddings = OpenAIEmbeddings()
            # vectorstore = InMemoryVectorStore(embedding=embeddings)
            # vectorstore.add_documents(documents)

            # # Create retriever tool
            # retriever_tool = create_retriever_tool(
            #     retriever=vectorstore.as_retriever(),
            #     name="search_agent_docs",
            #     description="Search for agent specifications and documentation"
            # )

            # # Create RAG agent
            # rag_discovery_agent = ReactAgent(
            #     name="rag_agent_discovery",
            #     engine=engine,
            #     tools=[retriever_tool]
            # )

            # For now, disable RAG discovery until imports are fixed
            logger.warning("RAG discovery disabled due to import issues")
            rag_discovery_agent = None

        # Create supervisor
        return cls(
            name=name,
            agents=agents,
            engine=engine,
            discovery_mode=discovery_mode,
            discovery_agent=discovery_agent,
            rag_discovery_agent=rag_discovery_agent,
            mcp_framework=mcp_config,
            **kwargs,
        )

    @classmethod
    def create_with_agent_specs(
        cls,
        name: str,
        initial_agent_specs: list[dict[str, Any]],
        engine: AugLLMConfig,
        discovery_mode: AgentDiscoveryMode = AgentDiscoveryMode.HYBRID,
        **kwargs,
    ) -> "DynamicAgentDiscoverySupervisor":
        """Create supervisor with initial agent specifications.

        Args:
            name: Supervisor name
            initial_agent_specs: List of agent specifications
            engine: LLM configuration
            discovery_mode: Agent discovery mode
            **kwargs: Additional arguments

        Returns:
            Configured supervisor

        Example:
            Create with agent specs::

                specs = [
                    {
                        "name": "analyst",
                        "agent_type": "ReactAgent",
                        "description": "Data analysis expert",
                        "specialties": ["data", "statistics"],
                        "tools": ["calculator", "data_visualizef"]
                    },
                    {
                        "name": "writer",
                        "agent_type": "SimpleAgent",
                        "description": "Content writing specialist",
                        "specialties": ["writing", "editing"]
                    }
                ]

                supervisor = DynamicAgentDiscoverySupervisor.create_with_agent_specs(
                    name="team_supervisor",
                    initial_agent_specs=specs,
                    engine=config
                )
        """
        # Create initial agents from specs
        agents = {}
        for spec in initial_agent_specs:
            agent_name = spec.get("name")
            agent_type = spec.get("agent_type", "SimpleAgent")

            # Get agent class
            if agent_type == "SimpleAgent":
                agent_class = SimpleAgent
            elif agent_type == "ReactAgent":
                agent_class = ReactAgent
            # elif agent_type == "PerplexityStyleAgent":
            #     agent_class = PerplexityStyleAgent  # Commented out due to import issues
            else:
                logger.warning(f"Unknown agent type: {agent_type}, using SimpleAgent")
                agent_class = SimpleAgent

            # Create agent
            config_dict = spec.get("config", {})
            if "engine" not in config_dict:
                config_dict["engine"] = engine

            agent = agent_class(name=agent_name, **config_dict)
            agents[agent_name] = agent

        # Create supervisor with agents to register
        return cls(
            name=name,
            agents=agents,
            engine=engine,
            discovery_mode=discovery_mode,
            agents_to_register=initial_agent_specs,
            **kwargs,
        )
