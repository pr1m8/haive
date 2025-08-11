"""Complete MCP Integration Example.

This example demonstrates the full MCP integration with haive-agents:
1. Type-checked MCP configuration
2. Resource/prompt/tool transfer between agents
3. Documentation-based setup
4. Dynamic server discovery
"""

import asyncio

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import LLMConfig
from haive.mcp.agents import MCPAgent, MCPDocumentationAgent, TransferableMCPAgent
from haive.mcp.config import MCPConfig, MCPServerConfig


async def example_basic_mcp_integration():
    """Basic MCP integration with type checking."""
    # Create engine with proper types
    engine = AugLLMConfig(
        llm_config=LLMConfig(provider="openai", model="gpt-4o-mini"),
        name="basic_engine",
    )

    # Create type-checked MCP configuration
    mcp_config = MCPConfig(
        enabled=True,
        servers={
            "filesystem": MCPServerConfig(
                name="filesystem",
                transport="stdio",
                command="npx",
                args=["-y", "@modelcontextprotocol/server-filesystem"],
                capabilities=["file_read", "file_write", "directory_list"],
                description="Local filesystem operations",
            )
        },
    )

    # Create MCP agent
    MCPAgent(engine=engine, mcp_config=mcp_config, name="basic_mcp_agent")


async def example_tool_transfer():
    """Demonstrate tool transfer between agents."""
    # Create shared engine
    engine = AugLLMConfig(
        llm_config=LLMConfig(provider="openai", model="gpt-4o-mini"),
        name="shared_engine",
    )

    # Create collaborative agents with shared MCP client
    agents = TransferableMCPAgent.create_collaborative_agents(
        engine=engine,
        mcp_config=MCPConfig(
            enabled=True,
            servers={
                "time": MCPServerConfig(
                    name="time",
                    transport="stdio",
                    command="npx",
                    args=["-y", "@modelcontextprotocol/server-time"],
                    capabilities=["time_queries"],
                )
            },
        ),
        num_agents=2,
        shared_client=True,
    )

    agent1, agent2 = agents

    # Initialize first agent
    await agent1.initialize_mcp()

    # Transfer tools to second agent
    await agent1.transfer_all_tools_to_agent(agent2)

    # Check transfer status
    agent1.get_transfer_status()


async def example_documentation_based_setup():
    """Use documentation to set up MCP servers."""
    # Create documentation agent
    doc_agent = MCPDocumentationAgent.create_for_mcp_setup()

    # Load documentation for popular servers
    servers_to_setup = [
        "modelcontextprotocol/server-filesystem",
        "modelcontextprotocol/server-github",
        "modelcontextprotocol/server-time",
    ]

    all_configs = []

    for server_name in servers_to_setup:
        result = await doc_agent.process_mcp_server(
            server_name,
            fetch_latest=False,  # Use cached docs
        )

        if result["mcp_config"]:
            all_configs.append(result["mcp_config"])

    # Create combined configuration
    if all_configs:
        MCPConfig(enabled=True, servers={config.name: config for config in all_configs})


async def example_capability_discovery():
    """Discover MCP servers by capability."""
    # Create documentation agent
    doc_agent = MCPDocumentationAgent.create_for_mcp_research()

    # Find servers for different capabilities
    capabilities = ["database", "search", "api", "file"]

    for capability in capabilities:
        servers = await doc_agent.find_servers_by_capability(capability, limit=3)

        for server in servers[:2]:  # Show first 2
            if server["server_name"]:
                config = server.get("mcp_config")
                if config:
                    pass


async def example_complete_workflow():
    """Complete workflow: discover, setup, and use MCP servers."""
    # Step 1: Create documentation agent to research servers
    doc_agent = MCPDocumentationAgent.create_for_mcp_research()

    # Step 2: Find servers for a research task
    search_servers = await doc_agent.find_servers_by_capability("search", limit=2)
    file_servers = await doc_agent.find_servers_by_capability("file", limit=1)

    # Collect server names
    selected_servers = []
    for servers in [search_servers, file_servers]:
        for server in servers:
            if server["server_name"] and server["mcp_config"]:
                selected_servers.append(server["server_name"])

    # Step 3: Generate implementation guide
    guide = await doc_agent.generate_implementation_guide(
        server_names=selected_servers, target_agent_type="research"
    )

    # Step 4: Create agent with the configuration
    if guide["combined_config"]:
        engine = AugLLMConfig(
            llm_config=LLMConfig(provider="openai", model="gpt-4o-mini"),
            name="research_engine",
        )

        research_agent = MCPAgent(
            engine=engine,
            mcp_config=guide["combined_config"],
            name="research_mcp_agent",
        )

        # Initialize MCP
        await research_agent.setup()

        # Show final status
        research_agent.get_mcp_status()


async def main():
    """Run all examples."""
    await example_basic_mcp_integration()
    await example_tool_transfer()
    await example_documentation_based_setup()
    await example_capability_discovery()
    await example_complete_workflow()


if __name__ == "__main__":
    asyncio.run(main())
