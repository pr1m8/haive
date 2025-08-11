#!/usr/bin/env python3
"""Real MCP Server Test - Actually install and run an MCP server.

This demonstrates the complete workflow without haive imports:
1. Install a real MCP server
2. Start the server
3. Communicate with it using MCP protocol
4. Show how it would integrate with haive agents
"""

import asyncio
import json
import subprocess


class MCPServerRunner:
    """Actually run MCP servers and communicate with them."""

    def __init__(self):
        self.running_processes = {}

    async def install_filesystem_server(self) -> bool:
        """Install the filesystem MCP server."""
        try:
            # Install the filesystem server
            process = await asyncio.create_subprocess_shell(
                "npm install -g @modelcontextprotocol/server-filesystem",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            stdout, stderr = await process.communicate()

            return process.returncode == 0

        except Exception:
            return False

    async def start_filesystem_server(self) -> subprocess.Popen:
        """Start the filesystem MCP server."""
        try:
            # Start the server with /tmp as root (safe directory)
            process = subprocess.Popen(
                ["npx", "@modelcontextprotocol/server-filesystem", "/tmp"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            # Give it a moment to start
            await asyncio.sleep(3)

            # Check if process is still running
            if process.poll() is None:
                self.running_processes["filesystem"] = process
                return process
            stdout, stderr = process.communicate()
            return None

        except Exception:
            return None

    async def test_mcp_communication(self, process: subprocess.Popen) -> bool:
        """Test actual MCP protocol communication."""
        try:
            # Initialize the MCP connection
            init_request = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {},
                    "clientInfo": {"name": "haive-test", "version": "1.0.0"},
                },
            }

            process.stdin.write(json.dumps(init_request) + "\n")
            process.stdin.flush()

            # Read response
            response_line = process.stdout.readline()
            if response_line.strip():
                json.loads(response_line)

                # Send initialized notification
                initialized = {"jsonrpc": "2.0", "method": "notifications/initialized"}

                process.stdin.write(json.dumps(initialized) + "\n")
                process.stdin.flush()

                # List available tools
                tools_request = {"jsonrpc": "2.0", "id": 2, "method": "tools/list"}

                process.stdin.write(json.dumps(tools_request) + "\n")
                process.stdin.flush()

                # Read tools response
                tools_response = process.stdout.readline()
                if tools_response.strip():
                    tools = json.loads(tools_response)

                    # Try to call a tool
                    if tools.get("result", {}).get("tools"):
                        tool_name = tools["result"]["tools"][0]["name"]

                        call_request = {
                            "jsonrpc": "2.0",
                            "id": 3,
                            "method": "tools/call",
                            "params": {"name": tool_name, "arguments": {}},
                        }

                        process.stdin.write(json.dumps(call_request) + "\n")
                        process.stdin.flush()

                        call_response = process.stdout.readline()
                        if call_response.strip():
                            json.loads(call_response)
                            return True

        except Exception:
            pass

        return False

    def cleanup(self):
        """Stop all running servers."""
        for _name, process in self.running_processes.items():
            try:
                process.terminate()
                process.wait(timeout=5)
            except:
                process.kill()


async def demo_haive_integration_pattern():
    """Show how this would integrate with haive agents."""


async def main():
    """Run the complete real MCP server test."""
    runner = MCPServerRunner()

    try:
        # Install filesystem server
        installed = await runner.install_filesystem_server()

        if not installed:
            return

        # Start the server
        process = await runner.start_filesystem_server()

        if not process:
            return

        # Test communication
        success = await runner.test_mcp_communication(process)

        if success:
            pass
        else:
            pass

        # Show integration pattern
        await demo_haive_integration_pattern()

    finally:
        # Always cleanup
        runner.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
