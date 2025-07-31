"""Dynamic React Agent with Tool Loading Capabilities.

This module provides DynamicReactAgent, an enhanced ReactAgent that can
dynamically discover, load, and activate tools based on task requirements
using the Dynamic Activation Pattern.

Based on:
- @project_docs/active/patterns/dynamic_activation_pattern.md
- @notebooks/tool_loader.ipynb pattern for tool loading
- @packages/haive-agents/examples/supervisor/advanced/dynamic_activation_example.py
"""

from typing import Any

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.registry import RegistryItem
from haive.core.schema.prebuilt.dynamic_activation_state import DynamicActivationState
from haive.core.schema.prebuilt.meta_state import MetaStateSchema
from langchain_core.tools import BaseTool
from pydantic import Field, PrivateAttr

from haive.agents.discovery.component_discovery_agent import ComponentDiscoveryAgent
from haive.agents.react.agent import ReactAgent


class DynamicToolState(DynamicActivationState):
    """Specialized state for dynamic tool management.

    Extends DynamicActivationState with tool-specific functionality
    for ReactAgent tool loading and management.

    Args:
        tool_categories: Categorization of tools by type
        tool_usage_stats: Usage statistics for each tool
        last_tool_discovery: Timestamp of last tool discovery
        discovery_queries: History of discovery queries

    Examples:
        Basic tool state usage::

            state = DynamicToolState()

            # Track tool categories
            state.tool_categories = {
                "math": ["calculator", "statistics"],
                "web": ["search", "scraper"],
                "file": ["reader", "writef"]
            }

            # Track tool usage
            state.tool_usage_stats = {
                "calculator": 5,
                "search": 3,
                "reader": 2
            }

        Get active tools::

            active_tools = state.get_active_tools()
            for tool in active_tools:
                print(f"Active tool: {tool.name}")
    """

    # Tool-specific fields
    tool_categories: dict[str, list[str]] = Field(
        default_factory=dict, description="Categorization of tools by type"
    )

    tool_usage_stats: dict[str, int] = Field(
        default_factory=dict, description="Usage statistics for each tool"
    )

    last_tool_discovery: str | None = Field(
        default=None, description="Timestamp of last tool discovery"
    )

    discovery_queries: list[str] = Field(
        default_factory=list, description="History of discovery queries"
    )

    def get_active_tools(self) -> list[BaseTool]:
        """Get all active tools as LangChain tools.

        Returns:
            List of active BaseTool instances

        Examples:
            Get active tools for agent::

                tools = state.get_active_tools()
                agent_tools = [tool for tool in tools if isinstance(tool, BaseTool)]
        """
        tools = []

        for item_id in self.registry.active_items:
            item = self.registry.items[item_id]
            component = item.component

            # Check if component is a tool
            if isinstance(component, BaseTool):
                tools.append(component)
            elif hasattr(component, "as_tool"):
                # Component can be converted to tool
                tool = component.as_tool()
                if isinstance(tool, BaseTool):
                    tools.append(tool)

        return tools

    def track_tool_usage(self, tool_name: str) -> None:
        """Track usage of a specific tool.

        Args:
            tool_name: Name of the tool that was used

        Examples:
            Track tool usage::

                state.track_tool_usage("calculator")
                state.track_tool_usage("search")

                # Check usage stats
                print(f"Calculator used {state.tool_usage_stats['calculator']} times")
        """
        if tool_name in self.tool_usage_stats:
            self.tool_usage_stats[tool_name] += 1
        else:
            self.tool_usage_stats[tool_name] = 1

    def get_tool_usage_stats(self) -> dict[str, int]:
        """Get tool usage statistics.

        Returns:
            Dictionary of tool name to usage count

        Examples:
            Get usage statistics::

                stats = state.get_tool_usage_stats()
                most_used = max(stats.items(), key=lambda x: x[1])
                print(f"Most used tool: {most_used[0]} ({most_used[1]} times)")
        """
        return self.tool_usage_stats.copy()

    def categorize_tool(self, tool_name: str, category: str) -> None:
        """Categorize a tool by type.

        Args:
            tool_name: Name of the tool
            category: Category to assign the tool to

        Examples:
            Categorize tools::

                state.categorize_tool("calculator", "math")
                state.categorize_tool("web_search", "web")
                state.categorize_tool("file_reader", "file")
        """
        if category not in self.tool_categories:
            self.tool_categories[category] = []

        if tool_name not in self.tool_categories[category]:
            self.tool_categories[category].append(tool_name)

    def get_tools_by_category(self, category: str) -> list[str]:
        """Get tools in a specific category.

        Args:
            category: Category to get tools for

        Returns:
            List of tool names in the category

        Examples:
            Get math tools::

                math_tools = state.get_tools_by_category("math")
                print(f"Math tools: {', '.join(math_tools)}")
        """
        return self.tool_categories.get(category, [])


class DynamicReactAgent(ReactAgent):
    """ReactAgent with dynamic tool loading capabilities.

    This agent extends ReactAgent with the ability to dynamically discover,
    load, and activate tools based on task requirements. It uses the Dynamic
    Activation Pattern with MetaStateSchema for component tracking.

    Key Features:
        - Dynamic tool discovery using ComponentDiscoveryAgent
        - Automatic tool loading from documentation
        - Tool activation and deactivation management
        - Usage tracking and statistics
        - Recompilation support for new tools
        - MetaStateSchema integration for tracking

    Args:
        name: Agent name
        engine: AugLLMConfig for the agent
        state_schema: DynamicToolState (set automatically)

    Private Attributes:
        _discovery_agent: ComponentDiscoveryAgent for finding tools
        _meta_self: MetaStateSchema wrapper for self-tracking
        _tool_loader: Tool loader for actual tool instantiation

    Examples:
        Basic dynamic tool loading::

            from haive.agents.react.dynamic_react_agent import DynamicReactAgent
            from haive.core.engine.aug_llm import AugLLMConfig

            # Create agent with discovery
            agent = DynamicReactAgent.create_with_discovery(
                name="dynamic_react",
                document_path="@haive-tools",
                engine=AugLLMConfig()
            )

            # Task that needs specific tools
            result = await agent.arun("Calculate compound interest and create a chart")

            # Agent automatically discovers and loads needed tools
            active_tools = agent.get_active_tool_names()
            print(f"Tools used: {', '.join(active_tools)}")

        Manual tool discovery::

            # Discover tools for specific task
            tools = await agent.discover_and_load_tools("data visualization")
            print(f"Loaded {len(tools)} tools for visualization")

            # Use agent with newly loaded tools
            result = await agent.arun("Create a bar chart from this data")

        Tool management::

            # Get tool usage statistics
            stats = agent.get_tool_usage_stats()
            print(f"Most used tool: {max(stats, key=stats.get)}")

            # Categorize tools
            agent.categorize_tool("calculator", "math")
            agent.categorize_tool("chart_maker", "visualization")
    """

    # Set state schema to DynamicToolState
    state_schema: type[DynamicToolState] = DynamicToolState

    # Initial tools to register (used during factory creation)
    tools_to_register: list[dict[str, Any]] | None = Field(default=None, exclude=True)

    # Tool discovery agents (part of agent's persistent state)
    discovery_agent: ComponentDiscoveryAgent | None = Field(default=None, exclude=True)
    rag_tool_agent: Any | None = Field(
        default=None, exclude=True
    )  # BaseRAGAgent for tool discovery

    # Private attributes for internal state (not serialized)
    _meta_self: MetaStateSchema | None = PrivateAttr(default=None)
    _tool_loader: Any | None = PrivateAttr(default=None)

    def setup_agent(self) -> None:
        """Setup the dynamic React agent.

        This method is called during agent initialization to set up
        the agent's internal state and discovery capabilities.
        """
        # Set state schema before parent setup
        if not hasattr(self, "state_schema") or self.state_schema is None:
            self.state_schema = DynamicToolState

        # Call parent setup
        super().setup_agent()

        # Initialize discovery agent if config is provided
        if hasattr(self, "_discovery_config"):
            self.discovery_agent = ComponentDiscoveryAgent(
                document_path=self._discovery_config["document_path"]
            )

        # Initialize RAG tool agent if config is provided
        if hasattr(self, "_rag_config"):
            self._setup_rag_tool_agent()

        # Initialize tool loader
        self._setup_tool_loader()

        # Add the dynamic tool discovery tool to the agent
        self._add_dynamic_tool_discovery_tool()

        # Register tools if they were provided during creation
        if hasattr(self, "tools_to_registef") and self.tools_to_register is not None:
            self._register_initial_tools(self.tools_to_register)
            self.tools_to_register = None  # Clean up after registration

        # Wrap self in MetaStateSchema for recompilation support
        self._meta_self = MetaStateSchema(
            agent=self,
            agent_state={"dynamic_tools": True},
            graph_context={
                "recompilation_enabled": True,
                "tool_discovery": True,
                "agent_type": "dynamic_react",
            },
        )

    @classmethod
    def create_with_discovery(
        cls,
        name: str,
        document_path: str,
        engine: AugLLMConfig,
        use_mcp: bool = False,
        **kwargs,
    ) -> "DynamicReactAgent":
        """Factory method to create agent with discovery capabilities.

        Args:
            name: Agent name
            document_path: Path to documentation for tool discovery
            engine: AugLLMConfig for the agent
            use_mcp: Whether to use MCP (Model Context Protocol) for tools
            **kwargs: Additional arguments for agent

        Returns:
            DynamicReactAgent with discovery capabilities

        Examples:
            Create with Haive tools::

                agent = DynamicReactAgent.create_with_discovery(
                    name="haive_react",
                    document_path="@haive-tools",
                    engine=AugLLMConfig()
                )

            Create with custom tools and MCP::

                agent = DynamicReactAgent.create_with_discovery(
                    name="custom_react",
                    document_path="/path/to/custom/tools",
                    engine=AugLLMConfig(temperature=0.3),
                    use_mcp=True
                )
        """
        # Create agent instance
        agent = cls(name=name, engine=engine, **kwargs)

        # Set discovery configuration (used in setup_agent)
        agent._discovery_config = {"document_path": document_path, "use_mcp": use_mcp}

        return agent

    @classmethod
    def create_with_rag_tooling(
        cls,
        name: str,
        engine: AugLLMConfig,
        rag_documents: list[str],
        tool_documents: list[str] | None = None,
        use_mcp: bool = False,
        **kwargs,
    ) -> "DynamicReactAgent":
        """Factory method to create agent with RAG-based tool discovery.

        This creates a DynamicReactAgent that can request tools from a RAG agent
        based on document content. The agent will have both reasoning capabilities
        and the ability to discover and use tools dynamically.

        Args:
            name: Agent name
            engine: AugLLMConfig for the agent
            rag_documents: List of documents for RAG knowledge base
            tool_documents: Optional separate documents for tool discovery
            use_mcp: Whether to use MCP (Model Context Protocol) for tools
            **kwargs: Additional arguments for agent

        Returns:
            DynamicReactAgent with RAG-based tool discovery

        Examples:
            Create with RAG knowledge and tool discovery::

                documents = [
                    "Python programming guide with examples",
                    "Data analysis techniques and tools",
                    "Machine learning algorithms overview"
                ]

                agent = DynamicReactAgent.create_with_rag_tooling(
                    name="rag_react",
                    engine=AugLLMConfig(),
                    rag_documents=documents
                )

            Create with separate tool discovery documents::

                knowledge_docs = ["Domain knowledge documents..."]
                tool_docs = ["Tool documentation and examples..."]

                agent = DynamicReactAgent.create_with_rag_tooling(
                    name="specialized_react",
                    engine=AugLLMConfig(),
                    rag_documents=knowledge_docs,
                    tool_documents=tool_docs,
                    use_mcp=True
                )
        """
        # Create agent instance
        agent = cls(name=name, engine=engine, **kwargs)

        # Set RAG configuration (used in setup_agent)
        agent._rag_config = {
            "rag_documents": rag_documents,
            "tool_documents": tool_documents or rag_documents,
            "use_mcp": use_mcp,
        }

        return agent

    @classmethod
    def create_with_tools(
        cls, name: str, tools: list[dict[str, Any]], engine: AugLLMConfig, **kwargs
    ) -> "DynamicReactAgent":
        """Factory method to create agent with pre-registered tools.

        Args:
            name: Agent name
            tools: List of tool dictionaries to register
            engine: AugLLMConfig for the agent
            **kwargs: Additional arguments for agent

        Returns:
            DynamicReactAgent with pre-registered tools

        Examples:
            Create with specific tools::

                from langchain_core.tools import tool

                @tool
                def calculator(expression: str) -> float:
                    '''Calculate mathematical expression.'''
                    return eval(expression)

                tools = [
                    {
                        "id": "calc",
                        "name": "Calculator",
                        "description": "Mathematical calculations",
                        "component": calculator,
                        "category": "math"
                    }
                ]

                agent = DynamicReactAgent.create_with_tools(
                    name="tool_react",
                    tools=tools,
                    engine=AugLLMConfig()
                )
        """
        # Set tools config before creating agent so it's available during setup
        kwargs["tools_to_register"] = tools

        # Create agent instance
        agent = cls(name=name, engine=engine, **kwargs)

        return agent

    def _setup_tool_loader(self) -> None:
        """Setup tool loader for dynamic tool instantiation.

        This sets up the tool loading mechanism based on the pattern
        from @notebooks/tool_loader.ipynb.
        """
        try:
            # Import tool loading functionality
            from haive.core.utils.haive_discovery import HaiveComponentDiscovery

            # Setup tool loader if discovery agent is available
            if self.discovery_agent and hasattr(
                self.discovery_agent, "_haive_discovery"
            ):
                self._tool_loader = self.discovery_agent._haive_discovery
            else:
                # Fallback: create basic tool loader
                haive_root = "/home/will/Projects/haive/backend/haive"
                self._tool_loader = HaiveComponentDiscovery(haive_root)

        except ImportError:
            # Fallback: no tool loader available
            self._tool_loader = None
        except Exception:
            # Any other error - fallback to None
            self._tool_loader = None

    def _register_initial_tools(self, tools: list[dict[str, Any]]) -> None:
        """Register initial tools during agent setup.

        This method registers tools that were provided during agent creation
        through the factory method. It's called during setup_agent() after
        the agent's state schema is properly initialized.

        Args:
            tools: List of tool dictionaries to register
        """
        from langchain_core.tools import BaseTool

        # Add tools to the engine using the proper method
        for tool_data in tools:
            component = tool_data["component"]
            if isinstance(component, BaseTool):
                # Use the engine's add_tool method to properly register the tool
                self.engine.add_tool(component)

        # Store tools for future state access (when state is available during runtime)
        if not hasattr(self, "_pending_tools"):
            self._pending_tools = []
        self._pending_tools.extend(tools)

    def _setup_rag_tool_agent(self) -> None:
        """Setup RAG-based tool discovery agent.

        This creates a BaseRAGAgent that can search through tool documentation
        to find and suggest appropriate tools for tasks.
        """
        try:
            from haive.core.engine.retriever import BaseRetrieverConfig
            from langchain_core.documents import Document

            from haive.agents.rag.base.agent import BaseRAGAgent

            # Get configuration
            rag_config = self._rag_config
            tool_documents = rag_config.get("tool_documents", [])

            # Convert strings to Document objects if needed
            documents = []
            for doc in tool_documents:
                if isinstance(doc, str):
                    documents.append(
                        Document(
                            page_content=doc,
                            metadata={
                                "source": "tool_docs",
                                "type": "tool_documentation",
                            },
                        )
                    )
                else:
                    documents.append(doc)

            # Create retriever configuration
            retriever_config = BaseRetrieverConfig(
                name="tool_discovery_retriever", documents=documents
            )

            # Create RAG agent for tool discovery
            self.rag_tool_agent = BaseRAGAgent(
                name=f"{self.name}_tool_discovery", engine=retriever_config
            )

        except Exception:
            self.rag_tool_agent = None

    def _add_dynamic_tool_discovery_tool(self) -> None:
        """Add the dynamic tool discovery tool to the agent.

        This tool allows the agent to search for and request new tools
        dynamically based on task requirements.
        """
        from langchain_core.tools import tool

        @tool
        def discover_and_load_tools(task_description: str) -> str:
            """Discover and load tools needed for a specific task.

            Args:
                task_description: Description of the task that needs tools

            Returns:
                Description of tools that were discovered and loaded
            """
            try:
                # Use discovery agent if available
                if self.discovery_agent:
                    # Use the existing discover_and_load_tools method
                    import asyncio

                    async def _discover():
                        return await self.discover_and_load_tools(task_description)

                    # Run async function
                    try:
                        loop = asyncio.get_event_loop()
                        tools = loop.run_until_complete(_discover())
                    except RuntimeError:
                        # No event loop, create one
                        tools = asyncio.run(_discover())

                    if tools:
                        tool_names = [
                            tool.name if hasattr(tool, "name") else str(tool)
                            for tool in tools
                        ]
                        return f"Discovered and loaded {len(tools)} tools: {', '.join(tool_names)}"
                    return "No suitable tools found for this task"

                # Use RAG tool agent if available
                if self.rag_tool_agent:
                    # Query RAG agent for tool suggestions
                    query = f"What tools are available for: {task_description}"

                    import asyncio

                    async def _rag_discover():
                        return await self.rag_tool_agent.arun(query)

                    try:
                        loop = asyncio.get_event_loop()
                        result = loop.run_until_complete(_rag_discover())
                    except RuntimeError:
                        result = asyncio.run(_rag_discover())

                    return f"RAG tool suggestions: {result}"

                return "No tool discovery system available"

            except Exception as e:
                return f"Error discovering tools: {e!s}"

        # Add the tool to the engine
        self.engine.add_tool(discover_and_load_tools)

    async def discover_and_load_tools(self, task: str) -> list[BaseTool]:
        """Discover and load tools for a specific task.

        Args:
            task: Task description to find tools for

        Returns:
            List of loaded BaseTool instances

        Examples:
            Discover tools for calculation::

                tools = await agent.discover_and_load_tools("mathematical calculations")
                print(f"Loaded {len(tools)} math tools")

            Discover tools for data processing::

                tools = await agent.discover_and_load_tools("data analysis and visualization")
                for tool in tools:
                    print(f"Loaded tool: {tool.name}")
        """
        loaded_tools = []

        # Try discovery agent first
        if self.discovery_agent:
            try:
                # Discover tools using RAG
                discovery_query = f"tools needed for: {task}"
                tool_docs = await self.discovery_agent.discover_components(
                    discovery_query
                )

                # Track discovery query
                self.state.discovery_queries.append(discovery_query)

                for doc in tool_docs:
                    # Load tool from document
                    tool = await self._load_tool_from_document(doc)
                    if tool:
                        loaded_tools.append(tool)

            except Exception as e:
                import logging

                logger = logging.getLogger(__name__)
                logger.exception(f"Discovery agent failed for task '{task}': {e}")

        # Try RAG tool agent if discovery agent didn't work or found nothing
        if not loaded_tools and self.rag_tool_agent:
            try:
                # Query RAG agent for tool suggestions
                query = f"Find tools and methods for: {task}"
                rag_result = await self.rag_tool_agent.arun(query)

                # Parse RAG result to find tool suggestions
                # This is a simplified approach - you might want more sophisticated parsing
                tool_suggestions = self._parse_rag_tool_suggestions(rag_result, task)

                for suggestion in tool_suggestions:
                    # Try to load the suggested tool
                    tool = await self._load_tool_from_suggestion(suggestion)
                    if tool:
                        loaded_tools.append(tool)

            except Exception as e:
                import logging

                logger = logging.getLogger(__name__)
                logger.exception(f"RAG tool agent failed for task '{task}': {e}")

        # Register loaded tools
        for tool in loaded_tools:
            try:
                # Register in state
                item = RegistryItem(
                    id=getattr(tool, "name", str(tool)),
                    name=getattr(tool, "name", "Unknown Tool"),
                    description=getattr(tool, "description", ""),
                    component=tool,
                    metadata={"source": "dynamic_discovery", "task": task},
                )

                # Add to registry (this will be available when state is accessible)
                if hasattr(self, "_pending_tools"):
                    self._pending_tools.append(
                        {
                            "id": item.id,
                            "name": item.name,
                            "description": item.description,
                            "component": tool,
                            "metadata": item.metadata,
                        }
                    )

                # Add to engine immediately
                self.engine.add_tool(tool)

                # Categorize tool based on task
                category = self._infer_tool_category(
                    task, {"name": item.name, "description": item.description}
                )
                if category and hasattr(self, "state"):
                    self.state.categorize_tool(item.name, category)

            except Exception as e:
                import logging

                logger = logging.getLogger(__name__)
                logger.exception(f"Failed to register tool {tool}: {e}")

        # Mark for recompilation if tools were loaded
        if loaded_tools and self._meta_self:
            self._meta_self.mark_for_recompile(
                f"Added {len(loaded_tools)} new tools for task: {task}"
            )

            # Trigger recompilation
            await self._recompile_with_new_tools(loaded_tools)

        return loaded_tools

    def _parse_rag_tool_suggestions(
        self, rag_result: str, task: str
    ) -> list[dict[str, Any]]:
        """Parse RAG result to extract tool suggestions.

        Args:
            rag_result: Result from RAG agent
            task: Original task description

        Returns:
            List of tool suggestions with metadata
        """
        suggestions = []

        # Simple parsing - look for tool names and descriptions
        # This is a basic implementation - you might want more sophisticated NLP
        lines = rag_result.split("\n")

        for line in lines:
            line = line.strip()
            if any(
                key in line.lower() for key in ["tool", "function", "method", "api"]
            ):
                # Extract potential tool information
                suggestion = {
                    "name": self._extract_tool_name(line),
                    "description": line,
                    "source": "rag_suggestion",
                    "task": task,
                }
                if suggestion["name"]:
                    suggestions.append(suggestion)

        return suggestions

    def _extract_tool_name(self, line: str) -> str:
        """Extract tool name from a line of text.

        Args:
            line: Line of text containing tool information

        Returns:
            Extracted tool name or empty string
        """
        # Simple extraction - look for patterns like "tool_name" or "ToolName"
        import re

        # Look for quoted strings
        quoted_match = re.search(r'"([^"]+)"', line)
        if quoted_match:
            return quoted_match.group(1)

        # Look for words that might be tool names
        words = line.split()
        for word in words:
            if (word.islower() and "_" in word) or (
                word[0].isupper() and len(word) > 3
            ):
                return word

        return ""

    async def _load_tool_from_suggestion(
        self, suggestion: dict[str, Any]
    ) -> BaseTool | None:
        """Load a tool from a RAG suggestion.

        Args:
            suggestion: Tool suggestion from RAG parsing

        Returns:
            Loaded tool instance or None
        """
        try:
            # This is a placeholder - you would implement actual tool loading logic
            # based on your tool registry or discovery system

            tool_name = suggestion.get("name", "")
            description = suggestion.get("description", "")

            # For now, create a simple placeholder tool
            from langchain_core.tools import tool

            @tool
            def suggested_tool(input_text: str) -> str:
                f"""Tool suggested by RAG: {tool_name}
                Description: {description}
                """
                return f"Executed {tool_name} with input: {input_text}"

            # Set the tool name and description
            suggested_tool.name = tool_name
            suggested_tool.description = description

            return suggested_tool

        except Exception as e:
            import logging

            logger = logging.getLogger(__name__)
            logger.exception(f"Failed to load tool from suggestion {suggestion}: {e}")
            return None

    async def discover_and_load_tools_legacy(self, task: str) -> list[BaseTool]:
        """Legacy version of discover_and_load_tools for backward compatibility."""
        loaded_tools = []

        if not self.discovery_agent:
            return loaded_tools

        try:
            # Discover tools using RAG
            discovery_query = f"tools needed for: {task}"
            tool_docs = await self.discovery_agent.discover_components(discovery_query)

            # Track discovery query
            self.state.discovery_queries.append(discovery_query)

            for doc in tool_docs:
                # Load tool from document
                tool = await self._load_tool_from_document(doc)
                if tool:
                    # Register in state
                    item = RegistryItem(
                        id=doc.get("id", doc.get("name", "unknown")),
                        name=doc.get("name", "Unknown Tool"),
                        description=doc.get("description", ""),
                        component=tool,
                        metadata=doc.get("metadata", {}),
                    )
                    self.state.registry.register(item)

                    # Activate tool
                    meta_state = self.state.activate_component(item.id)
                    if meta_state:
                        loaded_tools.append(tool)

                        # Categorize tool based on task
                        category = self._infer_tool_category(task, doc)
                        if category:
                            self.state.categorize_tool(item.name, category)

            # Update discovery timestamp
            from datetime import datetime

            self.state.last_tool_discovery = str(datetime.now())

            # Mark for recompilation if tools were loaded
            if loaded_tools and self._meta_self:
                self._meta_self.mark_for_recompile(
                    f"Added {len(loaded_tools)} new tools for task: {task}"
                )

                # Trigger recompilation
                await self._recompile_with_new_tools(loaded_tools)

        except Exception as e:
            import logging

            logger = logging.getLogger(__name__)
            logger.exception(
                f"Failed to discover and load tools for task '{task}': {e}"
            )

        return loaded_tools

    async def _load_tool_from_document(
        self, tool_doc: dict[str, Any]
    ) -> BaseTool | None:
        """Load actual tool instance from tool document.

        Args:
            tool_doc: Tool document from discovery

        Returns:
            Loaded BaseTool instance or None
        """
        if not self._tool_loader:
            return None

        try:
            # Use the tool loading pattern from notebooks/tool_loader.ipynb
            # This is a simplified version - the actual implementation would
            # need to handle different tool types and module loading

            tool_doc.get("module_path", "")
            tool_doc.get("name", "")

            # For now, return the tool document as a placeholder
            # In a real implementation, this would load the actual tool
            return tool_doc.get("component")

        except Exception as e:
            import logging

            logger = logging.getLogger(__name__)
            logger.exception(f"Failed to load tool from document: {e}")
            return None

    def _infer_tool_category(self, task: str, tool_doc: dict[str, Any]) -> str | None:
        """Infer tool category based on task and tool documentation.

        Args:
            task: Task description
            tool_doc: Tool document

        Returns:
            Inferred category or None
        """
        task_lower = task.lower()
        tool_name = tool_doc.get("name", "").lower()
        tool_desc = tool_doc.get("description", "").lower()

        # Simple category inference
        if any(word in task_lower for word in ["math", "calculate", "compute"]):
            return "math"
        if any(word in task_lower for word in ["search", "web", "lookup"]):
            return "web"
        if any(word in task_lower for word in ["file", "read", "write"]):
            return "file"
        if any(word in task_lower for word in ["chart", "plot", "visualize"]):
            return "visualization"
        if any(word in task_lower for word in ["data", "process", "analyze"]):
            return "data"

        # Check tool name/description for category hints
        if any(word in tool_name + tool_desc for word in ["math", "calc"]):
            return "math"
        if any(word in tool_name + tool_desc for word in ["search", "web"]):
            return "web"
        if any(word in tool_name + tool_desc for word in ["file", "io"]):
            return "file"
        if any(word in tool_name + tool_desc for word in ["chart", "plot"]):
            return "visualization"
        if any(word in tool_name + tool_desc for word in ["data", "process"]):
            return "data"

        return None

    async def _recompile_with_new_tools(self, new_tools: list[BaseTool]) -> None:
        """Recompile agent graph with new tools.

        Args:
            new_tools: List of new tools to add
        """
        try:
            # Update engine tools
            if hasattr(self.engine, "tools"):
                # Add new tools to engine
                current_tools = getattr(self.engine, "tools", [])
                self.engine.tools = current_tools + new_tools

            # Mark for recompilation
            if hasattr(self, "mark_for_recompile"):
                self.mark_for_recompile(f"Added {len(new_tools)} new tools")

            # Trigger recompilation if available
            if hasattr(self, "recompile") and callable(self.recompile):
                await self.recompile()

        except Exception as e:
            import logging

            logger = logging.getLogger(__name__)
            logger.exception(f"Failed to recompile with new tools: {e}")

    def get_active_tool_names(self) -> list[str]:
        """Get names of all active tools.

        Returns:
            List of active tool names

        Examples:
            List active tools::

                tool_names = agent.get_active_tool_names()
                print(f"Active tools: {', '.join(tool_names)}")
        """
        active_items = self.state.registry.get_active_items()
        return [item.name for item in active_items]

    def get_tool_usage_stats(self) -> dict[str, int]:
        """Get tool usage statistics.

        Returns:
            Dictionary of tool name to usage count

        Examples:
            Get usage statistics::

                stats = agent.get_tool_usage_stats()
                most_used = max(stats.items(), key=lambda x: x[1])
                print(f"Most used tool: {most_used[0]} ({most_used[1]} times)")
        """
        return self.state.get_tool_usage_stats()

    def categorize_tool(self, tool_name: str, category: str) -> None:
        """Categorize a tool by type.

        Args:
            tool_name: Name of the tool
            category: Category to assign the tool to

        Examples:
            Categorize tools::

                agent.categorize_tool("calculator", "math")
                agent.categorize_tool("web_search", "web")
        """
        self.state.categorize_tool(tool_name, category)

    def get_tools_by_category(self, category: str) -> list[str]:
        """Get tools in a specific category.

        Args:
            category: Category to get tools for

        Returns:
            List of tool names in the category

        Examples:
            Get math tools::

                math_tools = agent.get_tools_by_category("math")
                print(f"Math tools: {', '.join(math_tools)}")
        """
        return self.state.get_tools_by_category(category)

    async def activate_tool_by_name(self, tool_name: str) -> bool:
        """Activate a tool by name.

        Args:
            tool_name: Name of tool to activate

        Returns:
            True if activation succeeded

        Examples:
            Activate specific tool::

                success = await agent.activate_tool_by_name("calculator")
                if success:
                    print("Calculator activated successfully")
        """
        # Find tool by name
        for item_id in self.state.registry.list_components():
            item = self.state.registry.get_item(item_id)
            if item and item.name.lower() == tool_name.lower():
                meta_state = self.state.activate_component(item_id)
                if meta_state:
                    # Update engine tools if needed
                    if hasattr(self.engine, "tools") and isinstance(
                        item.component, BaseTool
                    ):
                        current_tools = getattr(self.engine, "tools", [])
                        if item.component not in current_tools:
                            self.engine.tools = [*current_tools, item.component]

                    return True

        return False

    def deactivate_tool_by_name(self, tool_name: str) -> bool:
        """Deactivate a tool by name.

        Args:
            tool_name: Name of tool to deactivate

        Returns:
            True if deactivation succeeded

        Examples:
            Deactivate specific tool::

                success = agent.deactivate_tool_by_name("calculator")
                if success:
                    print("Calculator deactivated successfully")
        """
        # Find tool by name
        for item_id in self.state.registry.list_components():
            item = self.state.registry.get_item(item_id)
            if item and item.name.lower() == tool_name.lower():
                success = self.state.deactivate_component(item_id)
                if success:
                    # Remove from engine tools if needed
                    if hasattr(self.engine, "tools") and isinstance(
                        item.component, BaseTool
                    ):
                        current_tools = getattr(self.engine, "tools", [])
                        if item.component in current_tools:
                            self.engine.tools = [
                                t for t in current_tools if t != item.component
                            ]

                    return True

        return False

    def get_registry_stats(self) -> dict[str, Any]:
        """Get statistics about the tool registry.

        Returns:
            Dictionary with registry statistics

        Examples:
            Show registry status::

                stats = agent.get_registry_stats()
                print(f"Total tools: {stats['total_components']}")
                print(f"Active tools: {stats['active_components']}")
                print(f"Most used: {stats['most_used_component']}")
        """
        return self.state.get_activation_stats()
