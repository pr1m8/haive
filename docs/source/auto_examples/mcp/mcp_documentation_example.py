"""Example demonstrating MCP Documentation Agent for setting up MCP servers.

This example shows how to:
1. Load MCP server documentation
2. Generate setup instructions
3. Create MCP configurations
4. Build implementation guides
"""

import asyncio
import json

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import LLMConfig

from haive.mcp.agents.documentation_agent import MCPDocumentationAgent


async def example_process_single_server():
    """Example: Process documentation for a single MCP server."""
    print("=== Processing Single MCP Server Documentation ===\n")

    # Create documentation agent
    doc_agent = MCPDocumentationAgent.create_for_mcp_setup()

    # Process filesystem MCP server
    result = await doc_agent.process_mcp_server(
        "modelcontextprotocol/server-filesystem",
        fetch_latest=False,  # Use cached docs for demo
    )

    print(f"Server: {result['server_name']}")
    print(f"Capabilities: {result['capabilities']}")
    print("\nSetup Instructions:")
    for instruction in result["setup_instructions"]:
        print(f"  {instruction}")

    if result["mcp_config"]:
        print("\nGenerated MCP Config:")
        print(json.dumps(result["mcp_config"].model_dump(), indent=2))


async def example_find_by_capability():
    """Example: Find MCP servers by capability."""
    print("\n=== Finding MCP Servers by Capability ===\n")

    # Create documentation agent
    doc_agent = MCPDocumentationAgent.create_for_mcp_research()

    # Find servers with file operation capabilities
    servers = await doc_agent.find_servers_by_capability("file", limit=5)

    print(f"Found {len(servers)} servers with 'file' capability:\n")

    for server in servers:
        print(f"- {server['server_name']}")
        if server["setup_instructions"]:
            print(f"  Setup: {server['setup_instructions'][0]}")


async def example_generate_implementation():
    """Example: Generate complete implementation guide."""
    print("\n=== Generating Implementation Guide ===\n")

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

    print(f"Implementation Guide for {guide['agent_type']} agent:\n")

    # Show combined configuration
    if guide["combined_config"]:
        print("Combined MCP Configuration:")
        print(json.dumps(guide["combined_config"].model_dump(), indent=2))

    # Show implementation code
    if guide["implementation_code"]:
        print("\nImplementation Code:")
        print("```python")
        print(guide["implementation_code"])
        print("```")

    # Show usage examples
    if guide["usage_examples"]:
        print(f"\nFound {len(guide['usage_examples'])} usage examples")


async def example_batch_documentation():
    """Example: Process documentation for multiple servers."""
    print("\n=== Batch Documentation Processing ===\n")

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

    print("Processing documentation for popular MCP servers:\n")

    for server_name in popular_servers:
        try:
            result = await doc_agent.process_mcp_server(server_name, fetch_latest=False)

            if result["mcp_config"]:
                print(f"✓ {server_name}")
                print(f"  Category: {result['mcp_config'].category}")
                print(f"  Transport: {result['mcp_config'].transport}")
                if result["setup_instructions"]:
                    print(f"  Install: {result['setup_instructions'][0]}")
            else:
                print(f"✗ {server_name} - No documentation found")

        except Exception as e:
            print(f"✗ {server_name} - Error: {e}")

        print()


async def example_create_custom_setup():
    """Example: Create custom setup for specific use case."""
    print("\n=== Creating Custom MCP Setup ===\n")

    # Create documentation agent
    doc_agent = MCPDocumentationAgent.create_for_mcp_setup()

    # Find servers for a research assistant
    print("Finding servers for a research assistant...\n")

    # Search for different capabilities
    search_servers = await doc_agent.find_servers_by_capability("search", limit=3)
    file_servers = await doc_agent.find_servers_by_capability("file", limit=2)
    web_servers = await doc_agent.find_servers_by_capability("web", limit=2)

    all_servers = []

    print("Selected servers:")
    for servers, capability in [
        (search_servers, "Search"),
        (file_servers, "File"),
        (web_servers, "Web"),
    ]:
        print(f"\n{capability} capability:")
        for server in servers:
            if server["server_name"]:
                print(f"  - {server['server_name']}")
                all_servers.append(server["server_name"])

    # Generate combined setup
    if all_servers:
        guide = await doc_agent.generate_implementation_guide(
            server_names=all_servers[:5],  # Limit to 5 servers
            target_agent_type="research_assistant",
        )

        print("\n\nGenerated Research Assistant Configuration:")
        print("=" * 50)

        if guide["combined_config"]:
            # Show summary
            config = guide["combined_config"]
            print(f"Total servers: {len(config.servers)}")
            print(f"Enabled: {config.enabled}")
            print("\nServers:")
            for name, server in config.servers.items():
                print(f"  - {name}: {server.description[:50]}...")


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
