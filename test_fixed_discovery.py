#!/usr/bin/env python
"""Test the fixed discovery APIs."""

import asyncio
import sys
from pathlib import Path

# Add path for imports
sys.path.insert(0, str(Path(__file__).parent / "packages" / "haive-dataflow" / "src"))


async def test_fixed_apis():
    """Test all three fixed discovery APIs."""
    
    print("🧪 Testing Fixed Discovery APIs\n")
    
    # Test 1: Agent Discovery
    print("🤖 Testing Agent Discovery API...")
    try:
        from haive.dataflow.api.routes.agent_discovery_routes_fixed import list_agents
        
        response = await list_agents()
        print(f"  ✅ Found {response.count} agents")
        print(f"     - v1 agents: {response.v1_count}")
        print(f"     - v2 agents: {response.v2_count}")
        print(f"     - Discovery method: {response.discovery_method}")
        
        if response.agents:
            print(f"     - Sample agent: {response.agents[0].name} ({response.agents[0].agent_type})")
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    # Test 2: Tool Discovery
    print("\n📦 Testing Tool Discovery API...")
    try:
        from haive.dataflow.api.routes.tools_routes_fixed import list_tools
        
        response = await list_tools()
        print(f"  ✅ Found {response.count} tools")
        print(f"     - Individual tools: {response.tool_count}")
        print(f"     - Toolkits: {response.toolkit_count}")
        print(f"     - Discovery method: {response.discovery_method}")
        
        if response.tools:
            print(f"     - Sample tool: {response.tools[0].name} ({response.tools[0].type})")
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    # Test 3: Game Discovery
    print("\n🎮 Testing Game Discovery...")
    try:
        from haive.dataflow.api.game_router_fixed import discover_game_agents, game_agents
        
        # Clear and discover
        game_agents.clear()
        discover_game_agents()
        
        print(f"  ✅ Found {len(game_agents)} games")
        if game_agents:
            games_list = list(game_agents.keys())[:5]  # First 5 games
            print(f"     - Games: {', '.join(games_list)}")
            
            # Show details of first game
            first_game = games_list[0]
            game_info = game_agents[first_game]
            print(f"     - {first_game} module: {game_info['module']}")
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    print("\n✅ All tests completed!")


if __name__ == "__main__":
    # Run the async tests
    asyncio.run(test_fixed_apis())