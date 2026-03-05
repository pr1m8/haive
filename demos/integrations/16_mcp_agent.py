"""Demo 16: MCP Agent.

Tests: MCPAgent from haive-mcp
"""

import asyncio
import sys
sys.path.insert(0, ".")

from dotenv import load_dotenv
load_dotenv()

from haive.core.engine.aug_llm import AugLLMConfig


async def main():
    print("=" * 60)
    print("Demo 16: MCP Agent")
    print("=" * 60)

    try:
        from haive.mcp.agents.mcp_agent import MCPAgent
        print("[OK] MCPAgent imported")
    except ImportError as e:
        print(f"[BROKEN] Import failed: {e}")
        return

    try:
        agent = MCPAgent(name="mcp_demo", engine=AugLLMConfig(temperature=0.3))
        print(f"[OK] Instantiated: {agent.name}")
    except Exception as e:
        print(f"[BROKEN] Instantiation failed: {e}")
        return

    print("\n[INFO] MCPAgent requires MCP server connection to run")
    print("       Skipping arun - needs MCP server setup")
    print("\n[OK] MCPAgent demo complete (import + instantiate)")


if __name__ == "__main__":
    asyncio.run(main())
