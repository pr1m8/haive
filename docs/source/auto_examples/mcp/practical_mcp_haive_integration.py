#!/usr/bin/env python3
"""Practical MCP + Haive Agent Integration Example

This example demonstrates:
1. Searching for MCP tools by query
2. Creating a haive agent with discovered tool capabilities
3. Using the agent to perform tasks
"""

import asyncio
import json
from pathlib import Path
from typing import Any

from haive.agents.react import ReactAgent

# Haive imports
from haive.agents.simple import SimpleAgent
from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.tools import Tool


class MCPToolDemo:
    """Demonstrates MCP tool integration with haive agents"""

    def __init__(self):
        # Correct path to MCP data
        self.data_path = (
            Path(__file__).parent.parent
            / "data"
            / "mcp_servers"
            / "ALL_MCP_SERVERS_COMPLETE.json"
        )
        self.servers_data = self.load_mcp_data()

    def load_mcp_data(self) -> list[dict[str, Any]]:
        """Load MCP servers data"""
        if not self.data_path.exists():
            print(f"❌ MCP data not found at: {self.data_path}")
            return []

        with open(self.data_path) as f:
            data = json.load(f)
            return data.get("all_servers", [])

    def search_tools(self, query: str) -> list[dict[str, Any]]:
        """Simple search for MCP tools"""
        query_lower = query.lower()
        results = []

        for server in self.servers_data:
            name = server.get("name", "").lower()
            desc = server.get("description", "").lower()
            category = server.get("category", "").lower()
            tools = [t.lower() for t in server.get("tools", [])]

            # Simple matching
            if (
                query_lower in name
                or query_lower in desc
                or query_lower in category
                or any(query_lower in tool for tool in tools)
            ):
                results.append(server)

        # Sort by stars
        results.sort(key=lambda x: x.get("stars", 0) or 0, reverse=True)

        return results[:5]  # Top 5 results

    def create_mcp_tool_wrapper(self, server_info: dict[str, Any]) -> Tool:
        """Create a tool wrapper for an MCP server"""
        server_name = server_info.get("name", "unknown")
        description = server_info.get("description", "MCP tool")

        # This is a mock implementation - in reality, you would:
        # 1. Connect to the actual MCP server
        # 2. Use the MCP protocol to communicate
        # 3. Return real results

        def tool_function(input: str) -> str:
            """Mock MCP tool function"""
            return f"[MCP Tool '{server_name}'] Processed: {input}"

        return Tool(
            name=server_name.replace("-", "_").replace(" ", "_"),
            description=description[:100],  # Limit description length
            func=tool_function,
        )


async def demo_calculator_agent():
    """Demo: Create an agent with calculator capabilities"""
    print("\n📊 Demo 1: Calculator Agent")
    print("=" * 50)

    demo = MCPToolDemo()

    # Search for calculator tools
    print("🔍 Searching for calculator tools...")
    results = demo.search_tools("calculator")

    if results:
        print(f"✅ Found {len(results)} calculator tools:")
        for i, server in enumerate(results[:3], 1):
            print(f"\n{i}. {server.get('name', 'Unknown')}")
            print(f"   Stars: {server.get('stars', 0)} ⭐")
            print(f"   Description: {server.get('description', 'N/A')[:60]}...")

        # Use the first result
        selected = results[0]
        print(f"\n🎯 Using: {selected.get('name')}")

        # Create tool wrapper
        calc_tool = demo.create_mcp_tool_wrapper(selected)

        # Create agent with the tool
        agent = SimpleAgent(
            name="calculator_agent",
            engine=AugLLMConfig(
                temperature=0.7,
                system_message="You are a helpful assistant with access to a calculator tool.",
            ),
            tools=[calc_tool],
        )

        # Test the agent
        print("\n🤖 Testing agent with calculator tool:")
        result = await agent.arun("Calculate 42 * 17")
        print(f"Agent response: {result}")
    else:
        print("❌ No calculator tools found")


async def demo_database_agent():
    """Demo: Create an agent with database query capabilities"""
    print("\n\n🗄️ Demo 2: Database Query Agent")
    print("=" * 50)

    demo = MCPToolDemo()

    # Search for database tools
    print("🔍 Searching for database tools...")
    results = demo.search_tools("database")

    if results:
        print(f"✅ Found {len(results)} database tools:")

        # Filter for Python database tools with high stars
        python_db_tools = [
            s for s in results if s.get("language", "").lower() == "python"
        ]

        if python_db_tools:
            for i, server in enumerate(python_db_tools[:3], 1):
                print(f"\n{i}. {server.get('name', 'Unknown')}")
                print(f"   Language: {server.get('language', 'unknown')}")
                print(f"   Stars: {server.get('stars', 0)} ⭐")
                print(f"   Category: {server.get('category', 'unknown')}")

            # Create multiple tools
            tools = []
            for server in python_db_tools[:2]:  # Use top 2
                tool = demo.create_mcp_tool_wrapper(server)
                tools.append(tool)

            # Create ReactAgent with multiple tools
            agent = ReactAgent(
                name="database_agent",
                engine=AugLLMConfig(
                    temperature=0.5,
                    system_message="You are a database expert with access to various database tools.",
                ),
                tools=tools,
            )

            print(f"\n🤖 Created ReactAgent with {len(tools)} database tools")

            # Test the agent
            result = await agent.arun("Query the user table for active users")
            print(f"Agent response: {result}")
    else:
        print("❌ No database tools found")


async def demo_custom_tool_creation():
    """Demo: Create custom tool wrappers for MCP servers"""
    print("\n\n🛠️ Demo 3: Custom Tool Creation")
    print("=" * 50)

    print(
        """
Example: Creating a real MCP tool wrapper

```python
import subprocess
import json

@tool
def mcp_web_scraper(url: str) -> str:
    \"\"\"Use MCP web scraper to extract content from a URL\"\"\"
    
    # Start MCP server process
    process = subprocess.Popen(
        ['npx', '-y', '@modelcontextprotocol/web-scraper'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Send MCP request
    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": "scrape_url",
            "arguments": {"url": url}
        }
    }
    
    # Write request
    process.stdin.write(json.dumps(request) + '\\n')
    process.stdin.flush()
    
    # Read response
    response_line = process.stdout.readline()
    response = json.loads(response_line)
    
    # Clean up
    process.terminate()
    
    return response.get('result', {}).get('content', 'No content')

# Use in agent
agent = ReactAgent(
    name="web_research_agent",
    engine=AugLLMConfig(),
    tools=[mcp_web_scraper]
)

result = await agent.arun("Scrape the content from https://example.com")
```
"""
    )


async def show_fastmcp_integration():
    """Show FastMCP server integration"""
    print("\n\n🚀 FastMCP Server Integration")
    print("=" * 50)

    print(
        """
For production use with FastMCP servers:

1. Install the integrated system:
   cd packages/haive-mcp
   ./setup_integrated_mcp.sh

2. Launch the web interface:
   poetry run python src/haive/mcp/integrated_launcher.py web

3. Workflow:
   - Search for tools (e.g., "Python calculator")
   - Click "Install" on desired tool
   - Tool is automatically configured in FastMCP
   - Start the server from "Installed" tab
   - Use in your haive agents!

4. Or use CLI:
   # Start an installed MCP server
   python fastmcp_runner.py start calculator-mcp
   
   # Check status
   python fastmcp_runner.py status
   
   # Stop server
   python fastmcp_runner.py stop calculator-mcp
"""
    )


async def main():
    """Run all demos"""
    print("🚀 MCP + Haive Agent Integration Demos")
    print("=" * 70)

    # Check if data exists
    demo = MCPToolDemo()
    if not demo.servers_data:
        print(
            "\n❌ No MCP data found. Please ensure ALL_MCP_SERVERS_COMPLETE.json exists."
        )
        print(f"Expected location: {demo.data_path}")
        return

    print(f"\n✅ Loaded {len(demo.servers_data)} MCP servers")

    # Run demos
    await demo_calculator_agent()
    await demo_database_agent()
    await demo_custom_tool_creation()
    await show_fastmcp_integration()

    print("\n\n✅ All demos complete!")
    print("\nNext steps:")
    print(
        "1. Try the integrated web interface for easy tool discovery and installation"
    )
    print("2. Create custom tool wrappers for your specific MCP servers")
    print("3. Build powerful agents by combining multiple MCP tools")


if __name__ == "__main__":
    asyncio.run(main())
