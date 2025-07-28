#!/usr/bin/env python3
"""Dynamic MCP Agent System

Flow:
1. Agent checks what tools are available vs installed
2. Self-query retrieval to find needed tools
3. Dynamic installation if tool missing
4. Hot-reload tools into agent
5. Agent uses new tool automatically
"""

import asyncio
import json
import subprocess
from dataclasses import dataclass
from pathlib import Path

from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field


@dataclass
class MCPServerInfo:
    """Information about an MCP server"""

    name: str
    description: str
    install_command: str | None
    category: str
    language: str
    tools: list[str]
    stars: int
    is_installed: bool = False
    is_running: bool = False


class ToolNeed(BaseModel):
    """Agent's tool requirement"""

    capability: str = Field(description="What the agent needs to do")
    category: str = Field(description="Tool category needed")
    priority: str = Field(description="high/medium/low")


class DynamicMCPManager:
    """Manages MCP servers dynamically for agents"""

    def __init__(self):
        # Load MCP server database
        data_path = (
            Path(__file__).parent.parent
            / "data"
            / "mcp_servers"
            / "ALL_MCP_SERVERS_COMPLETE.json"
        )
        with open(data_path) as f:
            data = json.load(f)
            self.all_servers = data.get("all_servers", [])

        # Running state
        self.installed_servers: dict[str, MCPServerInfo] = {}
        self.running_processes: dict[str, subprocess.Popen] = {}
        self.available_tools: dict[str, StructuredTool] = {}
        self.request_counters: dict[str, int] = {}

        print(f"📊 Loaded {len(self.all_servers)} MCP servers from database")

    def get_installed_tools(self) -> list[str]:
        """Get list of currently available tools"""
        return list(self.available_tools.keys())

    def search_available_servers(
        self, capability: str, category: str = ""
    ) -> list[MCPServerInfo]:
        """Search for servers that could provide a capability"""
        matches = []
        capability_lower = capability.lower()
        category_lower = category.lower()

        for server_data in self.all_servers:
            name = (server_data.get("name") or "").lower()
            desc = (server_data.get("description") or "").lower()
            cat = (server_data.get("category") or "").lower()
            tools = [t.lower() for t in server_data.get("tools", [])]

            # Check if server matches the capability
            matches_capability = (
                capability_lower in name
                or capability_lower in desc
                or any(capability_lower in tool for tool in tools)
            )

            matches_category = not category_lower or category_lower in cat

            if matches_capability and matches_category:
                server_info = MCPServerInfo(
                    name=server_data.get("name", "unknown"),
                    description=server_data.get("description", "No description"),
                    install_command=server_data.get("install_command"),
                    category=server_data.get("category", "general"),
                    language=server_data.get("language", "unknown"),
                    tools=server_data.get("tools", []),
                    stars=server_data.get("stars", 0) or 0,
                    is_installed=server_data.get("name") in self.installed_servers,
                    is_running=server_data.get("name") in self.running_processes,
                )
                matches.append(server_info)

        # Sort by stars and installation status
        matches.sort(key=lambda x: (x.is_installed, x.stars), reverse=True)
        return matches

    async def assess_tool_needs(self, agent_request: str) -> ToolNeed:
        """Analyze what tool capabilities the agent needs"""
        # Simple keyword-based analysis (could be enhanced with LLM)
        request_lower = agent_request.lower()

        if any(
            word in request_lower
            for word in ["calculate", "math", "compute", "add", "multiply"]
        ):
            return ToolNeed(capability="calculator", category="math", priority="high")
        if any(
            word in request_lower
            for word in ["file", "read", "write", "directory", "folder"]
        ):
            return ToolNeed(capability="filesystem", category="file", priority="high")
        if any(
            word in request_lower
            for word in ["web", "scrape", "url", "website", "html"]
        ):
            return ToolNeed(
                capability="web_scraping", category="web", priority="medium"
            )
        if any(word in request_lower for word in ["database", "sql", "query", "table"]):
            return ToolNeed(capability="database", category="data", priority="high")
        return ToolNeed(capability="general", category="utility", priority="low")

    def find_missing_tools(self, needed: ToolNeed) -> list[MCPServerInfo]:
        """Find what tools we need but don't have"""
        # Check if we already have tools for this capability
        current_tools = self.get_installed_tools()

        # Simple check - could be more sophisticated
        has_capability = any(
            needed.capability in tool.lower() for tool in current_tools
        )

        if has_capability:
            print(f"✅ Already have tools for {needed.capability}")
            return []

        # Search for servers that could provide this capability
        candidates = self.search_available_servers(needed.capability, needed.category)

        # Filter to installable servers
        installable = [
            s for s in candidates if s.install_command and not s.is_installed
        ]

        print(
            f"🔍 Found {len(installable)} installable servers for {needed.capability}"
        )
        return installable[:3]  # Top 3 candidates

    async def install_server(self, server_info: MCPServerInfo) -> bool:
        """Install an MCP server"""
        if not server_info.install_command:
            print(f"❌ No install command for {server_info.name}")
            return False

        print(f"📦 Installing {server_info.name}...")

        try:
            process = await asyncio.create_subprocess_shell(
                server_info.install_command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            stdout, stderr = await process.communicate()

            if process.returncode == 0:
                print(f"✅ Installed {server_info.name}")
                server_info.is_installed = True
                self.installed_servers[server_info.name] = server_info
                return True
            print(f"❌ Installation failed: {stderr.decode()}")
            return False

        except Exception as e:
            print(f"❌ Installation error: {e}")
            return False

    async def start_server(self, server_info: MCPServerInfo) -> bool:
        """Start an MCP server process"""
        if server_info.name in self.running_processes:
            print(f"✅ {server_info.name} already running")
            return True

        # Try different start commands based on server type
        start_commands = [
            f"npx {server_info.name}",
            f"python -m {server_info.name.replace('-', '_')}",
            server_info.name,
        ]

        for cmd in start_commands:
            try:
                print(f"🚀 Starting {server_info.name} with: {cmd}")

                process = subprocess.Popen(
                    cmd.split(),
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )

                await asyncio.sleep(2)

                if process.poll() is None:
                    self.running_processes[server_info.name] = process
                    self.request_counters[server_info.name] = 1

                    if await self._initialize_server(server_info.name):
                        print(f"✅ {server_info.name} started and initialized")
                        server_info.is_running = True
                        return True

            except Exception as e:
                print(f"❌ Failed to start with {cmd}: {e}")
                continue

        return False

    async def _initialize_server(self, server_name: str) -> bool:
        """Initialize MCP server connection"""
        try:
            process = self.running_processes[server_name]

            init_request = {
                "jsonrpc": "2.0",
                "id": self.request_counters[server_name],
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {},
                    "clientInfo": {"name": "dynamic-haive-agent", "version": "1.0.0"},
                },
            }

            process.stdin.write(json.dumps(init_request) + "\n")
            process.stdin.flush()
            self.request_counters[server_name] += 1

            response = process.stdout.readline()
            if response.strip():
                result = json.loads(response)
                if "result" in result:
                    # Send initialized notification
                    notify = {"jsonrpc": "2.0", "method": "notifications/initialized"}
                    process.stdin.write(json.dumps(notify) + "\n")
                    process.stdin.flush()
                    return True

        except Exception as e:
            print(f"❌ Initialization failed for {server_name}: {e}")

        return False

    def create_dynamic_tool(self, server_name: str, tool_name: str) -> StructuredTool:
        """Create a tool dynamically for any MCP server"""

        def execute_mcp_tool(query: str) -> str:
            """Execute any MCP tool dynamically"""
            try:
                process = self.running_processes[server_name]
                request = {
                    "jsonrpc": "2.0",
                    "id": self.request_counters[server_name],
                    "method": "tools/call",
                    "params": {
                        "name": tool_name,
                        "arguments": (
                            {"query": query}
                            if tool_name in ["calculate", "search"]
                            else {"path": query}
                        ),
                    },
                }

                process.stdin.write(json.dumps(request) + "\n")
                process.stdin.flush()
                self.request_counters[server_name] += 1

                response = process.stdout.readline()
                if response.strip():
                    result = json.loads(response)

                    if "result" in result:
                        content = result["result"].get("content", [])
                        if content and content[0].get("type") == "text":
                            return content[0].get("text", str(result["result"]))
                        return str(result["result"])
                    if "error" in result:
                        return f"❌ Error: {result['error']['message']}"

            except Exception as e:
                return f"❌ Tool execution failed: {e}"

            return "❌ No response"

        tool = StructuredTool.from_function(
            func=execute_mcp_tool,
            name=f"{server_name}_{tool_name}",
            description=f"Use {tool_name} from {server_name} MCP server",
        )

        return tool

    async def auto_discover_and_install_tools(
        self, server_info: MCPServerInfo
    ) -> list[StructuredTool]:
        """Automatically discover available tools from a running server and create them"""
        if server_info.name not in self.running_processes:
            print(f"❌ Server {server_info.name} not running")
            return []

        try:
            process = self.running_processes[server_info.name]

            # List available tools
            tools_request = {
                "jsonrpc": "2.0",
                "id": self.request_counters[server_info.name],
                "method": "tools/list",
            }

            process.stdin.write(json.dumps(tools_request) + "\n")
            process.stdin.flush()
            self.request_counters[server_info.name] += 1

            response = process.stdout.readline()
            if response.strip():
                result = json.loads(response)

                if "result" in result and "tools" in result["result"]:
                    available_tools = result["result"]["tools"]
                    created_tools = []

                    for tool_info in available_tools:
                        tool_name = tool_info.get("name")
                        if tool_name:
                            dynamic_tool = self.create_dynamic_tool(
                                server_info.name, tool_name
                            )
                            created_tools.append(dynamic_tool)
                            self.available_tools[dynamic_tool.name] = dynamic_tool
                            print(f"✅ Created tool: {dynamic_tool.name}")

                    return created_tools

        except Exception as e:
            print(f"❌ Tool discovery failed: {e}")

        return []

    async def dynamic_tool_provision(self, agent_request: str) -> list[StructuredTool]:
        """Main method: Dynamically provision tools based on agent needs"""
        print(f"\n🤖 Agent request: {agent_request}")

        # 1. Assess what tools are needed
        needed = await self.assess_tool_needs(agent_request)
        print(f"🎯 Need: {needed.capability} tools (priority: {needed.priority})")

        # 2. Check what's missing
        missing_servers = self.find_missing_tools(needed)

        if not missing_servers:
            print("✅ All needed tools already available")
            return list(self.available_tools.values())

        # 3. Install and setup missing tools
        newly_created_tools = []

        for server_info in missing_servers:
            print(f"\n📦 Setting up {server_info.name}...")

            # Install if needed
            if await self.install_server(server_info):
                # Start the server
                if await self.start_server(server_info):
                    # Auto-discover and create tools
                    tools = await self.auto_discover_and_install_tools(server_info)
                    newly_created_tools.extend(tools)

                    if tools:
                        print(f"🔥 HOT-RELOADED {len(tools)} new tools!")
                        break  # Got what we need

        # 4. Return all available tools (existing + new)
        all_tools = list(self.available_tools.values())
        print(f"\n✅ Total tools available: {len(all_tools)}")

        return all_tools

    def cleanup(self):
        """Stop all running servers"""
        for name, process in self.running_processes.items():
            try:
                process.terminate()
                process.wait(timeout=5)
                print(f"✅ Stopped {name}")
            except:
                process.kill()


class DynamicAgent:
    """Agent that can dynamically acquire new tools"""

    def __init__(self, name: str):
        self.name = name
        self.mcp_manager = DynamicMCPManager()
        self.current_tools: list[StructuredTool] = []

    async def process_request(self, user_request: str) -> str:
        """Process user request, dynamically acquiring tools if needed"""
        print(f"\n{'=' * 60}")
        print(f"🤖 {self.name} processing: {user_request}")
        print(f"{'=' * 60}")

        # Get tools (existing + dynamically provisioned)
        all_tools = await self.mcp_manager.dynamic_tool_provision(user_request)

        # Update agent's tool set
        self.current_tools = all_tools

        # Simulate agent using the tools
        print(f"\n🔧 Agent now has {len(self.current_tools)} tools available:")
        for tool in self.current_tools:
            print(f"   - {tool.name}: {tool.description}")

        # In a real implementation, this would use the actual haive agent
        return f"✅ Agent processed '{user_request}' with {len(self.current_tools)} available tools"

    def cleanup(self):
        """Cleanup resources"""
        self.mcp_manager.cleanup()


async def demo_dynamic_mcp_system():
    """Demonstrate the dynamic MCP system"""
    print("🚀 Dynamic MCP Agent System Demo")
    print("=" * 60)

    agent = DynamicAgent("DynamicAssistant")

    try:
        # Test 1: Request that needs filesystem tools
        result1 = await agent.process_request("I need to read a file called config.txt")
        print(f"\nResult: {result1}")

        await asyncio.sleep(2)

        # Test 2: Request that needs calculation tools
        result2 = await agent.process_request("Calculate 15 * 23 + 100")
        print(f"\nResult: {result2}")

        await asyncio.sleep(2)

        # Test 3: Request that needs web scraping
        result3 = await agent.process_request("Scrape the content from a website")
        print(f"\nResult: {result3}")

    finally:
        agent.cleanup()

    print("\n🏆 Dynamic MCP System Demo Complete!")
    print("\n🎯 What happened:")
    print("- Agent analyzed each request")
    print("- Discovered what tools were needed")
    print("- Dynamically installed missing MCP servers")
    print("- Hot-reloaded new tools into the agent")
    print("- Agent continued with expanded capabilities")


if __name__ == "__main__":
    asyncio.run(demo_dynamic_mcp_system())
