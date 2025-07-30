"""Base supervisor agent implementation.

This module provides the BaseSupervisor class that serves as the foundation
for all supervisor implementations in the Haive framework.

The BaseSupervisor extends ReactAgent to provide:
    - Multi-agent coordination and routing capabilities
    - Dynamic tool creation for agent handoffs
    - Performance tracking and metrics collection
    - Task lifecycle management with history
    - Error handling and recovery patterns

Example:
    Creating a custom supervisor:

    >>> from haive.agents.supervisor_new.base.agent import BaseSupervisor
    >>> from haive.core.engine.aug_llm import AugLLMConfig
    >>>
    >>> class CustomSupervisor(BaseSupervisor):
    ...     def route_to_agent(self, task: str) -> str:
    ...         # Custom routing logic
    ...         if "research" in task.lower():
    ...             return "research_agent"
    ...         return "general_agent"
    >>>
    >>> supervisor = CustomSupervisor(
    ...     name="custom_coordinator",
    ...     engine=AugLLMConfig(temperature=0.3)
    ... )

    Agent registration and execution:

    >>> from haive.agents.simple import SimpleAgent
    >>> research_agent = SimpleAgent(name="researcher", engine=AugLLMConfig())
    >>> supervisor.register_agent("research_agent", research_agent, "Research specialist")
    >>>
    >>> # The supervisor can now route tasks to the research agent
    >>> result = supervisor._execute_agent("research_agent", "Research quantum computing")
    >>> print(f"Task completed: {len(result) > 0}")
    Task completed: True
"""

import logging
import time
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any

from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.messages import HumanMessage

from haive.agents.base.agent import Agent
from haive.agents.react.agent import ReactAgent
from haive.agents.supervisor_new.base.models import (
    AgentInfo,
    SupervisorConfig,
    SupervisorResult,
    SupervisorTask,
)
from haive.agents.supervisor_new.base.prompts import (
    create_system_prompt,
    format_agent_list,
)
from haive.agents.supervisor_new.base.state import BaseSupervisorState
from haive.agents.supervisor_new.base.tools import SupervisorToolFactory

logger = logging.getLogger(__name__)


class BaseSupervisor(ReactAgent[BaseSupervisorState], ABC):
    """Base supervisor agent providing common functionality.

    This class extends ReactAgent to provide supervisor-specific capabilities
    including agent management, routing, and coordination. All supervisor
    implementations should extend this base class.

    The BaseSupervisor handles:
        - Agent registration and lifecycle management
        - Dynamic tool creation for agent handoffs
        - Task routing and execution coordination
        - Performance monitoring and metrics collection
        - Error handling and recovery mechanisms
        - State management with comprehensive tracking

    Attributes:
        registered_agents (Dict[str, Agent]): Registry of agent instances.
        agent_info (Dict[str, AgentInfo]): Metadata for registered agents.
        tool_factory (Optional[SupervisorToolFactory]): Factory for creating tools.
        config (SupervisorConfig): Configuration for supervisor behavior.

    Examples:
        Creating a custom supervisor implementation:

        >>> from haive.agents.supervisor_new.base.agent import BaseSupervisor
        >>> from haive.core.engine.aug_llm import AugLLMConfig
        >>>
        >>> class MyHierarchicalSupervisor(BaseSupervisor):
        ...     def route_to_agent(self, task: str) -> str:
        ...         # Implement custom routing logic
        ...         if "urgent" in task.lower():
        ...             return "priority_agent"
        ...         elif "research" in task.lower():
        ...             return "research_agent"
        ...         else:
        ...             return "general_agent"
        >>>
        >>> supervisor = MyHierarchicalSupervisor(
        ...     name="hierarchy_coordinator",
        ...     engine=AugLLMConfig(temperature=0.2)
        ... )

        Agent registration and management:

        >>> from haive.agents.simple import SimpleAgent
        >>> research_agent = SimpleAgent(name="researcher", engine=AugLLMConfig())
        >>> supervisor.register_agent(
        ...     name="research_agent",
        ...     agent=research_agent,
        ...     description="Specialized in academic research and analysis",
        ...     capabilities=["literature_review", "data_analysis", "report_writing"]
        ... )
        >>>
        >>> # Check registration
        >>> agents = supervisor.list_agents()
        >>> print(f"Registered: {list(agents.keys())}")
        Registered: ['research_agent']

        Task execution and performance tracking:

        >>> result = supervisor._execute_agent("research_agent", "Research quantum computing trends")
        >>> performance = supervisor._get_performance_stats()
        >>> print(f"Total executions: {performance.get('total_executions', 0)}")
        Total executions: 1

    Note:
        Subclasses must implement the abstract `route_to_agent` method to define
        their specific routing logic. The base class provides all infrastructure
        for agent management, tool creation, and performance tracking.

    Raises:
        NotImplementedError: If `route_to_agent` is not implemented by subclass.
        ValueError: If invalid agent names or configurations are provided.
    """

    def __init__(
        self,
        name: str,
        engine: AugLLMConfig,
        config: SupervisorConfig | None = None,
        initial_agents: dict[str, Agent] | None = None,
        **kwargs,
    ) -> None:
        """Initialize base supervisor with configuration and optional agents.

        Sets up the supervisor with the provided configuration and registers any
        initial agents. Creates the tool factory and initializes state management.

        Args:
            name (str): Unique identifier for this supervisor instance.
            engine (AugLLMConfig): LLM engine configuration for supervisor decisions.
            config (Optional[SupervisorConfig]): Supervisor behavior configuration.
                If None, creates default config with the provided name.
            initial_agents (Optional[Dict[str, Agent]]): Dictionary of agent_name -> Agent
                to register immediately upon initialization.
            **kwargs: Additional keyword arguments passed to ReactAgent parent class.
                Common options include `system_message`, `max_iterations`, `state_schema`.

        Examples:
            Basic supervisor initialization:

            >>> from haive.agents.supervisor_new.base import SupervisorConfig
            >>> from haive.core.engine.aug_llm import AugLLMConfig
            >>>
            >>> config = SupervisorConfig(name="coordinator", max_iterations=8)
            >>> engine = AugLLMConfig(temperature=0.3, max_tokens=1000)
            >>> supervisor = BaseSupervisor(name="coordinator", engine=engine, config=config)

            Initialization with agents:

            >>> from haive.agents.simple import SimpleAgent
            >>> writer = SimpleAgent(name="writer", engine=engine)
            >>> researcher = SimpleAgent(name="researcher", engine=engine)
            >>> initial_agents = {"writer": writer, "researcher": researcher}
            >>> supervisor = BaseSupervisor(
            ...     name="team_lead",
            ...     engine=engine,
            ...     initial_agents=initial_agents
            ... )
            >>> print(f"Registered: {len(supervisor.registered_agents)} agents")
            Registered: 2 agents

        Note:
            The supervisor automatically creates a system prompt based on registered
            agents unless a custom `system_message` is provided in kwargs. The tool
            factory is initialized during `setup_agent()` which is called automatically.

        Raises:
            ValueError: If name is empty or invalid configuration is provided.
            TypeError: If initial_agents contains non-Agent instances.
        """
        # Set up configuration
        self.config = config or SupervisorConfig(name=name)

        # Set up state schema
        kwargs["state_schema"] = kwargs.get("state_schema", BaseSupervisorState)

        # Set max iterations from config
        kwargs["max_iterations"] = kwargs.get(
            "max_iterations", self.config.max_iterations
        )

        # Create system prompt
        if "system_message" not in kwargs:
            agent_list = self._format_initial_agents(initial_agents or {})
            kwargs["system_message"] = create_system_prompt(
                agent_list=agent_list, supervisor_name=name
            )

        # Initialize ReactAgent parent
        super().__init__(name=name, engine=engine, **kwargs)

        # Supervisor-specific attributes
        self.registered_agents: dict[str, Agent] = {}
        self.agent_info: dict[str, AgentInfo] = {}
        self.tool_factory: SupervisorToolFactory | None = None

        # Register initial agents
        if initial_agents:
            for agent_name, agent in initial_agents.items():
                self.register_agent(agent_name, agent)

    def setup_agent(self) -> None:
        """Setup supervisor agent with tools and configuration."""
        super().setup_agent()

        # Create tool factory
        self.tool_factory = SupervisorToolFactory(
            supervisor_name=self.name,
            get_agents_func=self._get_agent_descriptions,
            get_agent_info_func=self._get_agent_info,
            get_stats_func=self._get_performance_stats,
            execute_agent_func=self._execute_agent,
        )

        # Update tools
        self._update_tools()

        # Initialize state
        self._initialize_supervisor_state()

    def _initialize_supervisor_state(self) -> None:
        """Initialize supervisor-specific state."""
        if hasattr(self, "state") and self.state:
            self.state.supervisor_name = self.name
            # Register agent names in state
            for agent_name in self.registered_agents.keys():
                self.state.register_agent_name(agent_name)

    def _format_initial_agents(self, agents: dict[str, Agent]) -> str:
        """Format initial agents for system prompt."""
        if not agents:
            return (
                "No agents currently available. Agents will be registered dynamically."
            )

        descriptions = {}
        for name, agent in agents.items():
            # Try to get description from agent, fall back to class name
            description = getattr(
                agent, "description", f"{agent.__class__.__name__} agent"
            )
            descriptions[name] = description

        return format_agent_list(descriptions)

    def register_agent(
        self,
        name: str,
        agent: Agent,
        description: str | None = None,
        capabilities: list[str] | None = None,
    ) -> None:
        """Register an agent with the supervisor.

        Args:
            name: Agent name
            agent: Agent instance
            description: Optional agent description
            capabilities: Optional list of capabilities
        """
        # Store agent
        self.registered_agents[name] = agent

        # Create agent info
        if description is None:
            description = getattr(
                agent, "description", f"{agent.__class__.__name__} agent"
            )

        self.agent_info[name] = AgentInfo(
            name=name,
            description=description,
            agent_class=agent.__class__.__name__,
            capabilities=capabilities or [],
            created_at=datetime.now(),
        )

        # Update state
        if hasattr(self, "state") and self.state:
            self.state.register_agent_name(name)

        # Update tools
        if self.tool_factory:
            self._update_tools()

        logger.info(f"Registered agent '{name}' with supervisor '{self.name}'")

    def unregister_agent(self, name: str) -> bool:
        """Unregister an agent from the supervisor.

        Args:
            name: Agent name to unregister

        Returns:
            True if agent was unregistered, False if not found
        """
        if name not in self.registered_agents:
            return False

        # Remove from registries
        del self.registered_agents[name]
        del self.agent_info[name]

        # Update state
        if hasattr(self, "state") and self.state:
            self.state.deactivate_agent(name)
            if name in self.state.registered_agent_names:
                self.state.registered_agent_names.remove(name)

        # Update tools
        if self.tool_factory:
            self._update_tools()

        logger.info(f"Unregistered agent '{name}' from supervisor '{self.name}'")
        return True

    def list_agents(self) -> dict[str, str]:
        """List all registered agents.

        Returns:
            Dict mapping agent names to descriptions
        """
        return {
            name: info.description
            for name, info in self.agent_info.items()
            if info.is_active
        }

    def get_agent_info(self, name: str) -> AgentInfo | None:
        """Get information about a registered agent.

        Args:
            name: Agent name

        Returns:
            AgentInfo if found, None otherwise
        """
        return self.agent_info.get(name)

    def activate_agent(self, name: str) -> bool:
        """Activate an agent.

        Args:
            name: Agent name

        Returns:
            True if activated, False if not found
        """
        if name not in self.agent_info:
            return False

        self.agent_info[name].is_active = True

        if hasattr(self, "state") and self.state:
            self.state.activate_agent(name)

        self._update_tools()
        return True

    def deactivate_agent(self, name: str) -> bool:
        """Deactivate an agent.

        Args:
            name: Agent name

        Returns:
            True if deactivated, False if not found
        """
        if name not in self.agent_info:
            return False

        self.agent_info[name].is_active = False

        if hasattr(self, "state") and self.state:
            self.state.deactivate_agent(name)

        self._update_tools()
        return True

    def _update_tools(self) -> None:
        """Update supervisor tools based on current agent registry."""
        if not self.tool_factory:
            return

        # Get active agents
        active_agents = {
            name: info.description
            for name, info in self.agent_info.items()
            if info.is_active
        }

        # Create all tools
        all_tools = self.tool_factory.create_all_tools(active_agents)

        # Update engine tools
        if self.main_engine and hasattr(self.main_engine, "tools"):
            self.main_engine.tools = all_tools
        elif (
            self.main_engine
            and hasattr(self.main_engine, "config")
            and hasattr(self.main_engine.config, "tools")
        ):
            self.main_engine.config.tools = all_tools

    def _get_agent_descriptions(self) -> dict[str, str]:
        """Get active agent descriptions for tools."""
        return {
            name: info.description
            for name, info in self.agent_info.items()
            if info.is_active
        }

    def _get_agent_info(self, name: str) -> AgentInfo | None:
        """Get agent info for tools."""
        return self.agent_info.get(name)

    def _get_performance_stats(self) -> dict[str, Any]:
        """Get performance statistics for tools."""
        if not hasattr(self, "state") or not self.state:
            return {}

        stats = {
            "total_executions": self.state.execution_count,
            "success_rate": self.state.get_total_success_rate(),
            "error_count": self.state.error_count,
            "agent_stats": {},
        }

        # Add per-agent stats
        for agent_name, metrics in self.state.agent_performance.items():
            stats["agent_stats"][agent_name] = {
                "executions": metrics.total_executions,
                "success_rate": metrics.success_rate,
                "avg_time": metrics.average_execution_time,
            }

        return stats

    def _execute_agent(self, agent_name: str, task: str) -> str:
        """Execute an agent with a task.

        Args:
            agent_name: Name of agent to execute
            task: Task to execute

        Returns:
            Result from agent execution
        """
        if agent_name not in self.registered_agents:
            return f"Agent '{agent_name}' not found in registry."

        agent = self.registered_agents[agent_name]

        # Create task
        task_obj = SupervisorTask(
            task_id=f"{agent_name}_{int(time.time())}",
            content=task,
            target_agent=agent_name,
        )

        # Add task to state
        if hasattr(self, "state") and self.state:
            self.state.add_task(task_obj)

        try:
            start_time = time.time()

            # Execute agent
            result = agent.invoke({"messages": [HumanMessage(content=task)]})

            execution_time = time.time() - start_time

            # Extract response
            if isinstance(result, dict) and "messages" in result:
                response = result["messages"][-1].content
            else:
                response = str(result)

            # Update agent info
            if agent_name in self.agent_info:
                self.agent_info[agent_name].usage_count += 1
                self.agent_info[agent_name].last_used = datetime.now()

            # Create result
            result_obj = SupervisorResult(
                task_id=task_obj.task_id,
                agent_used=agent_name,
                result=response,
                execution_time=execution_time,
                success=True,
                completed_at=datetime.now(),
            )

            # Complete task in state
            if hasattr(self, "state") and self.state:
                self.state.complete_task(result_obj)
                self.state.last_agent_used = agent_name
                self.state.clear_error()

            return response

        except Exception as e:
            execution_time = time.time() - start_time
            error_msg = str(e)

            # Create error result
            result_obj = SupervisorResult(
                task_id=task_obj.task_id,
                agent_used=agent_name,
                result="",
                execution_time=execution_time,
                success=False,
                error_message=error_msg,
                completed_at=datetime.now(),
            )

            # Update state with error
            if hasattr(self, "state") and self.state:
                self.state.complete_task(result_obj)
                self.state.set_error(error_msg)

            logger.error(f"Error executing agent {agent_name}: {e}")
            return f"Error executing agent {agent_name}: {error_msg}"

    @abstractmethod
    def route_to_agent(self, task: str) -> str:
        """Route a task to the appropriate agent.

        This method must be implemented by subclasses to define
        their specific routing logic.

        Args:
            task: Task to route

        Returns:
            Name of agent to handle the task
        """

    def create_initial_state(self) -> BaseSupervisorState:
        """Create initial state for supervisor.

        Returns:
            Initial supervisor state
        """
        state = BaseSupervisorState(supervisor_name=self.name)

        # Register agent names
        for agent_name in self.registered_agents.keys():
            state.register_agent_name(agent_name)

        return state
