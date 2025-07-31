"""Dynamic Tool Discovery Supervisor with multiple discovery sources.

This module provides DynamicToolDiscoverySupervisor, an advanced supervisor that can
dynamically discover and load tools from multiple sources during runtime, then distribute
them to appropriate agents for task execution.

The supervisor supports multiple discovery modes:
- Component Discovery: Framework-based tool discovery
- RAG Discovery: Document-based tool discovery using RAG agents
- MCP Discovery: External tool discovery via MCP framework
- Hybrid: Combines all discovery methods

Example:
    Basic usage with tool discovery::

        from haive.agents.supervisor.dynamic_tool_discovery_supervisor import (
            DynamicToolDiscoverySupervisor,
            ToolDiscoveryMode
        )
        from haive.agents.simple.agent import SimpleAgent
        from haive.agents.react.agent import ReactAgent
        from haive.core.engine.aug_llm import AugLLMConfig

        # Create supervisor with agents
        config = AugLLMConfig(temperature=0.1)
        agents = {
            "analyzer": SimpleAgent(name="analyzer", engine=config),
            "executor": ReactAgent(name="executor", engine=config, tools=[])
        }

        supervisor = DynamicToolDiscoverySupervisor(
            name="tool_supervisor",
            agents=agents,
            engine=config,
            discovery_mode=ToolDiscoveryMode.HYBRID
        )

        # Run task - supervisor will discover needed tools
        result = await supervisor.arun("Calculate compound interest and analyze the results")

    Using factory method with discovery sources::

        supervisor = DynamicToolDiscoverySupervisor.create_with_discovery(
            name="discovery_supervisof",
            agents=agents,
            engine=config,
            discovery_mode=ToolDiscoveryMode.HYBRID,
            component_discovery_config={"registry_path": "./components"},
            rag_documents_path="/path/to/tool/docs",
            mcp_config={"endpoint": "http://localhost:8000"}
        )

    With initial tools and agents::

        supervisor = DynamicToolDiscoverySupervisor.create_with_agents_and_tools(
            name="configured_supervisof",
            agent_configs=[
                {"type": "SimpleAgent", "name": "worker1"},
                {"type": "ReactAgent", "name": "worker2"}
            ],
            engine=config,
            initial_tools=[calculator_tool, search_tool],
            discovery_mode=ToolDiscoveryMode.COMPONENT_DISCOVERY
        )

Note:
    This supervisor requires async execution. All main methods return awaitable objects.
    Tool discovery happens automatically based on task analysis, but can also be
    triggered manually using the built-in discover_and_load_tools tool.

See Also:
    - :class:`haive.agents.supervisor.base_supervisor.BaseSupervisor`
    - :class:`haive.agents.supervisor.dynamic_activation_supervisor.DynamicActivationSupervisor`
    - :class:`haive.agents.react.dynamic_react_agent.DynamicReactAgent`
"""

from enum import Enum
from typing import Any

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.embeddings import OpenAIEmbeddings
from haive.core.models.vectorstore import InMemoryVectorStore
from haive.core.types import Name
from haive.tools.utility.document_loaders import DirectoryLoader
from langchain_core.messages import HumanMessage
from langchain_core.tools import Tool, tool
from pydantic import ConfigDict, Field, field_validator, model_validator

from haive.agents.base.base_agent import BaseAgent
from haive.agents.react.agent import ReactAgent
from haive.agents.react.dynamic_activation_supervisor import ComponentDiscoveryAgent
from haive.agents.simple.agent import SimpleAgent
from haive.agents.supervisor.base_supervisor import BaseSupervisor
from haive.agents.supervisor.types import (
    SupervisorDecision,
    SupervisorState,
)


class ToolDiscoveryMode(str, Enum):
    """Enumeration of available tool discovery modes.

    Attributes:
        COMPONENT_DISCOVERY: Use ComponentDiscoveryAgent for framework-based discovery
        RAG_DISCOVERY: Use RAG agent for document-based discovery
        MCP_DISCOVERY: Use MCP framework for external tool discovery
        HYBRID: Combine all discovery methods

    Example:
        Setting discovery mode::

            supervisor = DynamicToolDiscoverySupervisor(
                name="supervisor",
                agents=agents,
                engine=config,
                discovery_mode=ToolDiscoveryMode.RAG_DISCOVERY
            )
    """

    COMPONENT_DISCOVERY = "component_discovery"
    RAG_DISCOVERY = "rag_discovery"
    MCP_DISCOVERY = "mcp_discovery"
    HYBRID = "hybrid"


class DynamicToolDiscoverySupervisor(BaseSupervisor):
    """Supervisor with dynamic tool discovery and distribution capabilities.

    This supervisor extends BaseSupervisor with the ability to dynamically discover
    tools from multiple sources and distribute them to appropriate agents. It analyzes
    tasks to determine tool requirements and can discover new tools on-demand.

    The supervisor maintains a registry of discovered tools and can route tasks to
    agents based on their tool capabilities. Tool discovery happens automatically
    during task execution but can also be triggered manually.

    Attributes:
        discovery_mode (ToolDiscoveryMode): Mode for tool discovery (default: HYBRID)
        discovery_agent (Optional[ComponentDiscoveryAgent]): Agent for component discovery
        rag_tool_agent (Optional[BaseRAGAgent]): RAG agent for document-based discovery
        mcp_framework (Optional[Dict[str, Any]]): MCP framework configuration
        discovered_tools (Set[str]): Set of discovered tool names
        tool_registry (Dict[str, Tool]): Registry mapping tool names to Tool instances
        max_discovery_attempts (int): Maximum discovery attempts per task (default: 3)
        tools_to_register (Optional[List[Dict[str, Any]]]): Initial tools for registration

    Example:
        Creating a supervisor with tool discovery::

            from haive.agents.supervisor.dynamic_tool_discovery_supervisor import (
                DynamicToolDiscoverySupervisor,
                ToolDiscoveryMode
            )

            # Basic creation
            supervisor = DynamicToolDiscoverySupervisor(
                name="main_supervisof",
                agents={
                    "worker1": SimpleAgent(...),
                    "worker2": ReactAgent(...)
                },
                engine=AugLLMConfig(),
                discovery_mode=ToolDiscoveryMode.HYBRID
            )

            # Run task - tools will be discovered as needed
            result = await supervisor.arun("Analyze data and create visualizations")

            # Check discovered tools
            print(f"Discovered tools: {supervisor.discovered_tools}")

        Using factory methods::

            # With discovery sources configured
            supervisor = DynamicToolDiscoverySupervisor.create_with_discovery(
                name="advanced_supervisor",
                agents=agents,
                engine=config,
                rag_documents_path="/path/to/docs",
                component_discovery_config={"scan_packages": ["haive.tools"]}
            )

            # With pre-configured agents and tools
            supervisor = DynamicToolDiscoverySupervisor.create_with_agents_and_tools(
                name="preset_supervisof",
                agent_configs=[
                    {"type": "SimpleAgent", "name": "analyst"},
                    {"type": "ReactAgent", "name": "executor"}
                ],
                engine=config,
                initial_tools=[math_tool, search_tool]
            )

    Note:
        - Tool discovery is asynchronous and may take time for large document sets
        - Discovered tools are cached to avoid redundant discovery
        - Tools are distributed only to agents that support dynamic tool addition
        - The supervisor includes a built-in 'discover_and_load_tools' tool

    Raises:
        ValueError: If invalid discovery mode is provided
        RuntimeError: If discovery agents fail to initialize

    See Also:
        - :class:`ToolDiscoveryMode`: Available discovery modes
        - :class:`haive.agents.supervisor.base_supervisor.BaseSupervisor`: Base supervisor class
        - :meth:`create_with_discovery`: Factory method for discovery configuration
        - :meth:`create_with_agents_and_tools`: Factory method for preset configuration
    """

    model_config = ConfigDict(
        str_strip_whitespace=True, validate_assignment=True, extra="forbid"
    )

    # Discovery configuration
    discovery_mode: ToolDiscoveryMode = Field(
        default=ToolDiscoveryMode.HYBRID, description="Mode for tool discovery"
    )

    # Discovery agents (excluded from serialization)
    discovery_agent: ComponentDiscoveryAgent | None = Field(default=None, exclude=True)
    rag_tool_agent: Any | None = Field(default=None, exclude=True)  # BaseRAGAgent
    mcp_framework: dict[str, Any] | None = Field(default=None, exclude=True)

    # Tool management
    discovered_tools: set[str] = Field(
        default_factory=set, description="Set of discovered tool names"
    )
    tool_registry: dict[str, Tool] = Field(default_factory=dict, exclude=True)
    max_discovery_attempts: int = Field(default=3, ge=1, le=10)

    # Initial tools to register (used during factory creation)
    tools_to_register: list[dict[str, Any]] | None = Field(default=None, exclude=True)

    @field_validator("discovery_mode")
    @classmethod
    def validate_discovery_mode(cls, v: str) -> str:
        """Validate discovery mode."""
        if v not in ToolDiscoveryMode.__members__.values():
            raise ValueError(f"Invalid discovery mode: {v}")
        return v

    @model_validator(mode="after")
    @classmethod
    def setup_supervisor(cls) -> "DynamicToolDiscoverySupervisor":
        """Set up supervisor after initialization."""
        # Register initial tools if provided
        if self.tools_to_register:
            for tool_data in self.tools_to_register:
                self._register_tool(tool_data)
            # Clear after registration
            self.tools_to_register = None

        # Add dynamic tool discovery tool
        self._add_discovery_tool()

        return self

    def _register_tool(self, tool_data: dict[str, Any]) -> None:
        """Register a tool in the supervisor's tool registry.

        This method creates a Tool instance from the provided data and registers it
        in both the tool registry and discovered tools set. If agents support dynamic
        tool addition, the tool is also added to them.

        Args:
            tool_data: Dictionary containing tool information with keys:
                - name (str): Tool name (required)
                - description (str): Tool description
                - func (Callable): Tool function (required if not a full tool config)
                - Other Tool configuration parameters

        Example:
            Registering a tool internally::

                tool_data = {
                    "name": "calculator",
                    "description": "Performs calculations",
                    "func": calculator_function
                }
                supervisor._register_tool(tool_data)

        Note:
            This is an internal method. Use factory methods or the discover_and_load_tools
            tool for external tool registration.
        """
        tool_name = tool_data.get("name", "")
        if tool_name and tool_name not in self.tool_registry:
            # Create tool from data
            if "func" in tool_data:
                # Direct tool function
                tool_instance = Tool(
                    name=tool_name,
                    description=tool_data.get("description", ""),
                    func=tool_data["func"],
                )
            else:
                # Tool configuration
                tool_instance = Tool(**tool_data)

            self.tool_registry[tool_name] = tool_instance
            self.discovered_tools.add(tool_name)

            # Add tool to agents if they support it
            for _agent_name, agent in self.agents.items():
                if hasattr(agent, "add_tool") and callable(agent.add_tool):
                    agent.add_tool(tool_instance)

    def _add_discovery_tool(self) -> None:
        """Add the dynamic tool discovery tool."""

        @tool
        def discover_and_load_tools(task_description: str) -> str:
            """Discover and load tools needed for a specific task.

            This tool analyzes the task description and discovers relevant tools
            from configured sources (component discovery, RAG, MCP).

            Args:
                task_description: Description of the task requiring tools

            Returns:
                Description of discovered and loaded tools
            """
            discovered = []

            # Component discovery
            if (
                self.discovery_mode
                in [
                    ToolDiscoveryMode.COMPONENT_DISCOVERY,
                    ToolDiscoveryMode.HYBRID,
                ]
                and self.discovery_agent
            ):
                try:
                    components = self.discovery_agent.discover_components(
                        query=f"tools for: {task_description}",
                        component_type="tool",
                    )
                    for comp in components:
                        if comp["name"] not in self.discovered_tools:
                            self._register_tool(comp)
                            discovered.append(f"Component: {comp['name']}")
                except Exception as e:
                    discovered.append(f"Component discovery error: {e!s}")

            # RAG discovery
            if (
                self.discovery_mode
                in [
                    ToolDiscoveryMode.RAG_DISCOVERY,
                    ToolDiscoveryMode.HYBRID,
                ]
                and self.rag_tool_agent
            ):
                try:
                    # Query RAG agent for tools
                    rag_response = self.rag_tool_agent.run(
                        f"Find tools or functions that can help with: {task_description}"
                    )
                    # Parse response for tool definitions
                    # This is simplified - real implementation would parse structured output
                    if "tool:" in rag_response.lower():
                        discovered.append("RAG: Found tool definitions in documents")
                except Exception as e:
                    discovered.append(f"RAG discovery error: {e!s}")

            # MCP discovery
            if (
                self.discovery_mode
                in [
                    ToolDiscoveryMode.MCP_DISCOVERY,
                    ToolDiscoveryMode.HYBRID,
                ]
                and self.mcp_framework
            ):
                try:
                    # Query MCP framework
                    mcp_tools = self.mcp_framework.get("discover_tools", lambda x: [])(
                        task_description
                    )
                    for tool_def in mcp_tools:
                        if tool_def["name"] not in self.discovered_tools:
                            self._register_tool(tool_def)
                            discovered.append(f"MCP: {tool_def['name']}")
                except Exception as e:
                    discovered.append(f"MCP discovery error: {e!s}")

            if discovered:
                return f"Discovered and loaded tools: {', '.join(discovered)}"
            return "No new tools discovered for this task"

        # Register the discovery tool
        self._register_tool(
            {
                "name": "discover_and_load_tools",
                "description": "Discover and load tools needed for a specific task",
                "func": discover_and_load_tools,
            }
        )

    async def _make_decision(self, state: SupervisorState) -> SupervisorDecision:
        """Make routing decision with tool discovery awareness.

        This method extends the base supervisor's decision-making to consider tool
        availability and discovery needs. It analyzes tasks to determine if tool
        discovery should happen before routing to agents.

        The decision process:
            1. Analyze if the task requires tools based on keywords
            2. Check if tool discovery has been attempted recently
            3. Route to self for tool discovery if needed
            4. Otherwise, make standard routing decision based on agent capabilities

        Args:
            state: Current supervisor state containing messages and agent outputs

        Returns:
            SupervisorDecision containing:
                - next_agent: Name of agent to route to (or self for discovery)
                - reasoning: Explanation of the routing decision
                - confidence: Confidence score (0.0-1.0)
                - suggested_prompt: Optional prompt modification

        Example:
            The method automatically detects tool needs::

                # Task: "Calculate the compound interest"
                # Decision: Routes to self first to discover calculator tools

                # Task: "Write a simple greeting"
                # Decision: Routes directly to appropriate agent

        Note:
            Tool discovery is limited by max_discovery_attempts to prevent
            infinite discovery loops.
        """
        messages = state.messages

        # Check if we should discover tools first
        if len(messages) > 0:
            last_message = messages[-1]
            if isinstance(last_message, HumanMessage):
                # Analyze if task might need new tools
                task_content = str(last_message.content).lower()
                tool_keywords = [
                    "calculate",
                    "search",
                    "analyze",
                    "process",
                    "convert",
                    "translate",
                ]

                if any(key in task_content for key in tool_keywords):
                    # Check if we have attempted discovery recently
                    recent_discovery = any(
                        "discover_and_load_tools" in str(msg.content)
                        for msg in messages[-5:]
                        if hasattr(msg, "content")
                    )

                    if not recent_discovery and len(self.discovered_tools) < 10:
                        # Suggest tool discovery first
                        return SupervisorDecision(
                            next_agent=self.name,  # Route to self for tool discovery
                            reasoning="Task appears to require tools. Discovering available tools first.",
                            confidence=0.9,
                            suggested_prompt=f"discover_and_load_tools for: {last_message.content}",
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

        # Get available agents and their tools
        agent_info = []
        for name, agent in self.agents.items():
            tools = []
            if hasattr(agent, "tools"):
                tools = [t.name for t in agent.tools if hasattr(t, "name")]
            elif hasattr(agent, "tool_registry"):
                tools = list(agent.tool_registry.keys())

            agent_info.append(
                f"- {name}: {agent.__class__.__name__} (tools: {', '.join(tools) or 'none'})"
            )

        # Get discovered tools
        tool_info = f"Discovered tools: {', '.join(self.discovered_tools) or 'none'}"

        prompt = f"""As a supervisor, analyze the conversation and decide which agent should handle the next step.

Conversation history:
{context}

Available agents:
{chr(10).join(agent_info)}

{tool_info}

Consider:
1. Which agent is best suited for the current task?
2. Are there enough tools available or should we discover more?
3. What is the user trying to accomplish?

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

    # Factory methods for different configurations

    @classmethod
    def create_with_discovery(
        cls,
        name: str,
        agents: dict[Name, BaseAgent],
        engine: AugLLMConfig,
        discovery_mode: ToolDiscoveryMode = ToolDiscoveryMode.HYBRID,
        component_discovery_config: dict[str, Any] | None = None,
        rag_documents_path: str | None = None,
        mcp_config: dict[str, Any] | None = None,
        **kwargs,
    ) -> "DynamicToolDiscoverySupervisor":
        """Create supervisor with configured discovery sources.

        This factory method creates a supervisor with specific discovery sources
        configured. It handles the setup of ComponentDiscoveryAgent, RAG agent,
        and MCP framework based on the provided configuration.

        Args:
            name: Unique name for the supervisor
            agents: Dictionary mapping agent names to Agent instances
            engine: LLM configuration for supervisor decision-making
            discovery_mode: Tool discovery mode (default: HYBRID)
            component_discovery_config: Configuration for ComponentDiscoveryAgent:
                - registry_path (str): Path to component registry
                - scan_packages (List[str]): Packages to scan for tools
                - cache_results (bool): Whether to cache discovery results
            rag_documents_path: Path to documents for RAG-based discovery
            mcp_config: MCP framework configuration:
                - endpoint (str): MCP server endpoint
                - auth_token (str): Authentication token
                - timeout (int): Request timeout in seconds
            **kwargs: Additional arguments pass
                    name="full_discovery_supervisof",
                    agents={
                        "analyst": SimpleAgent(name="analyst", engine=config),
                        "executor": ReactAgent(name="executor", engine=config)
                    },
                    engine=AugLLMConfig(temperature=0.1),
                    discovery_mode=ToolDiscoveryMode.HYBRID,
                    component_discovery_config={
                        "registry_path": "./tool_registry",
                        "scan_packages": ["haive.tools", "custom_tools"]
                    },
                    rag_documents_path="/docs/tool_documentation",
                    mcp_config={
                        "endpoint": "http://mcp.example.com",
                        "auth_token": "secret_token"
                    }
                )

            Create with only RAG discovery::

                supervisor = DynamicToolDiscoverySupervisor.create_with_discovery(
                    name="rag_supervisor",
                    agents=agents,
                    engine=config,
                    discovery_mode=ToolDiscoveryMode.RAG_DISCOVERY,
                    rag_documents_path="./tool_docs"
                )

        Note:
            - Component discovery requires valid Python packages in scan_packages
            - RAG discovery creates an in-memory vector store from documents
            - MCP discovery requires a running MCP server at the endpoint
        """
        # Create discovery agent if needed
        discovery_agent = None
        if (
            discovery_mode
            in [
                ToolDiscoveryMode.COMPONENT_DISCOVERY,
                ToolDiscoveryMode.HYBRID,
            ]
            and component_discovery_config
        ):
            discovery_agent = ComponentDiscoveryAgent(**component_discovery_config)

        # Create RAG agent if needed
        rag_tool_agent = None
        if (
            discovery_mode
            in [
                ToolDiscoveryMode.RAG_DISCOVERY,
                ToolDiscoveryMode.HYBRID,
            ]
            and rag_documents_path
        ):
            # Create simple RAG agent for tool discovery
            from haive.core.tools import create_retriever_tool

            # Load documents
            loader = DirectoryLoader(rag_documents_path)
            documents = loader.load()

            # Create vector store
            embeddings = OpenAIEmbeddings()
            vectorstore = InMemoryVectorStore(embedding=embeddings)
            vectorstore.add_documents(documents)

            # Create retriever tool
            retriever_tool = create_retriever_tool(
                retriever=vectorstore.as_retriever(),
                name="search_tool_docs",
                description="Search for tool documentation and definitions",
            )

            # Create RAG agent
            rag_tool_agent = ReactAgent(
                name="rag_tool_discovery", engine=engine, tools=[retriever_tool]
            )

        # Create supervisor
        return cls(
            name=name,
            agents=agents,
            engine=engine,
            discovery_mode=discovery_mode,
            discovery_agent=discovery_agent,
            rag_tool_agent=rag_tool_agent,
            mcp_framework=mcp_config,
            **kwargs,
        )

    @classmethod
    def create_with_agents_and_tools(
        cls,
        name: str,
        agent_configs: list[dict[str, Any]],
        engine: AugLLMConfig,
        initial_tools: list[Tool | dict[str, Any]] | None = None,
        discovery_mode: ToolDiscoveryMode = ToolDiscoveryMode.HYBRID,
        **kwargs,
    ) -> "DynamicToolDiscoverySupervisor":
        """Create supervisor with agents and initial tools.

        Args:
            name: Supervisor name
            agent_configs: List of agent configurations
            engine: LLM configuration
            initial_tools: Initial tools to register
            discovery_mode: Tool discovery mode
            **kwargs: Additional arguments

        Returns:
            Configured supervisor
        """
        # Create agents from configs
        agents = {}
        for config in agent_configs:
            agent_type = config.pop("type", "SimpleAgent")
            agent_name = config.pop("name")

            if agent_type == "SimpleAgent":
                agent = SimpleAgent(name=agent_name, engine=engine, **config)
            elif agent_type == "ReactAgent":
                agent = ReactAgent(name=agent_name, engine=engine, **config)
            else:
                raise ValueError(f"Unknown agent type: {agent_type}")

            agents[agent_name] = agent

        # Prepare tools for registration
        tools_to_register = []
        if initial_tools:
            for tool in initial_tools:
                if isinstance(tool, dict):
                    tools_to_register.append(tool)
                elif hasattr(tool, "name") and hasattr(tool, "func"):
                    tools_to_register.append(
                        {
                            "name": tool.name,
                            "description": getattr(tool, "description", ""),
                            "func": tool.func,
                        }
                    )

        # Create supervisor
        return cls(
            name=name,
            agents=agents,
            engine=engine,
            discovery_mode=discovery_mode,
            tools_to_register=tools_to_register,
            **kwargs,
        )
