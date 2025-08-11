"""Example demonstrating MCP Documentation Agent for setting up MCP servers.

This example shows how to:
1. Load MCP server documentation
2. Generate setup instructions
3. Create MCP configurations
4. Build implementation guides
"""

import asyncio

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import LLMConfig
from haive.mcp.agents.documentation_agent import MCPDocumentationAgent


async def example_process_single_server():
    """Example: Process documentation for a single MCP server."""
    # Create documentation agent
    doc_agent = MCPDocumentationAgent.create_for_mcp_setup()

    # Process filesystem MCP server
    result = await doc_agent.process_mcp_server(
        "modelcontextprotocol/server-filesystem",
        fetch_latest=False,  # Use cached docs for demo
    )

    for _instruction in result["setup_instructions"]:
        pass

    if result["mcp_config"]:
        pass


async def example_find_by_capability():
    """Example: Find MCP servers by capability."""
    # Create documentation agent
    doc_agent = MCPDocumentationAgent.create_for_mcp_research()

    # Find servers with file operation capabilities
    servers = await doc_agent.find_servers_by_capability("file", limit=5)

    for server in servers:
        if server["setup_instructions"]:
            pass


async def example_generate_implementation():
    """Example: Generate complete implementation guide."""
    # Create documentation agent with engine
    engine = AugLLMConfig(
        llm_config=LLMConfig(provider="openai", model="gpt-4o-mini"), name="doc_engine"
    )

    doc_agent = MCPDocumentationAgent(engine=engine, name="Implementation Guide Agent")

    # Generate guide for multiple servers
    guide = await doc_agent.generate_implementation_guide(
        server_names=[
            "modelcontextprotocol/server-filesystem",
            "modelcontextprotocol/server-github",
        ],
        target_agent_type="research",
    )

    # Show combined configuration
    if guide["combined_config"]:
        pass

    # Show implementation code
    if guide["implementation_code"]:
        pass

    # Show usage examples
    if guide["usage_examples"]:
        pass


async def example_batch_documentation():
    """Example: Process documentation for multiple servers."""
    # Create documentation agent
    doc_agent = MCPDocumentationAgent.create_for_mcp_setup()

    # List of popular MCP servers
    popular_servers = [
        "modelcontextprotocol/server-filesystem",
        "modelcontextprotocol/server-time",
        "modelcontextprotocol/server-fetch",
        "pierrebarbera/mcp-server-tavily",
        "CheMigui/mcp-server-perplexity",
    ]

    for server_name in popular_servers:
        try:
            result = await doc_agent.process_mcp_server(server_name, fetch_latest=False)

            if result["mcp_config"]:
                if result["setup_instructions"]:
                    pass
            else:
                pass

        except Exception:
            pass


async def example_create_custom_setup():
    """Example: Create custom setup for specific use case."""
    # Create documentation agent
    doc_agent = MCPDocumentationAgent.create_for_mcp_setup()

    # Find servers for a research assistant

    # Search for different capabilities
    search_servers = await doc_agent.find_servers_by_capability("search", limit=3)
    file_servers = await doc_agent.find_servers_by_capability("file", limit=2)
    web_servers = await doc_agent.find_servers_by_capability("web", limit=2)

    all_servers = []

    for servers, _capability in [
        (search_servers, "Search"),
        (file_servers, "File"),
        (web_servers, "Web"),
    ]:
        for server in servers:
            if server["server_name"]:
                all_servers.append(server["server_name"])

    # Generate combined setup
    if all_servers:
        guide = await doc_agent.generate_implementation_guide(
            server_names=all_servers[:5],  # Limit to 5 servers
            target_agent_type="research_assistant",
        )

        if guide["combined_config"]:
            # Show summary
            config = guide["combined_config"]
            for _name, server in config.servers.items():
                pass


async def main():
    """Run all examples."""
    await example_process_single_server()
    await example_find_by_capability()
    await example_generate_implementation()
    await example_batch_documentation()
    await example_create_custom_setup()


if __name__ == "__main__":
    # Run examples
    asyncio.run(main())
