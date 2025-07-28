#!/usr/bin/env python3
"""Automated Discovery Agent Example

This example shows how to use our MCPDocumentationAgent to automatically
discover new MCP servers and other ecosystem resources, then implement
agents that can use them.

Usage:
    poetry run python examples/automated_discovery_agent.py
"""

import asyncio
import json
from typing import Any

from haive.core.engine import AugLLMConfig

from haive.mcp.agents import MCPDocumentationAgent


class EnhancedMCPDiscoveryAgent(MCPDocumentationAgent):
    """Agent that discovers new MCP servers and updates our database."""

    def __init__(self, engine):
        super().__init__(engine=engine, name="mcp_discovery_agent")
        self.discovered_servers = []
        self.awesome_repos = [
            "wong2/awesome-mcp-servers",
            "punkpeye/awesome-mcp-servers",
            "appcypher/awesome-mcp-servers",
            "modelcontextprotocol/servers",
        ]

    async def discover_from_awesome_lists(self) -> list[dict[str, Any]]:
        """Scan awesome-mcp-servers repositories for new entries."""
        print("🔍 Discovering MCP servers from awesome lists...")

        discovery_prompt = f"""
        I need to find new MCP servers from GitHub repositories. Please help me:
        
        1. Search these repositories for MCP server listings:
           {", ".join(self.awesome_repos)}
        
        2. For each repository, extract:
           - Server names and descriptions
           - GitHub repository URLs
           - Installation instructions
           - Capabilities mentioned
        
        3. Look for patterns like:
           - npm packages starting with @modelcontextprotocol/
           - Repositories with "mcp" in the name
           - Servers with tool/resource descriptions
        
        4. Return a structured list of any servers not in our current database
        
        Focus on finding servers that might be missing from our 992-server collection.
        """

        result = await self.arun(
            {"messages": [{"role": "user", "content": discovery_prompt}]}
        )

        # Parse the result to extract new servers
        return await self._parse_discovery_result(result)

    async def discover_from_npm_search(self) -> list[dict[str, Any]]:
        """Search npm for MCP-related packages."""
        print("📦 Searching npm for MCP packages...")

        npm_search_prompt = """
        Search npm registry for Model Context Protocol related packages.
        
        Search terms to use:
        - "mcp-server"
        - "model-context-protocol" 
        - "@modelcontextprotocol"
        - "fastmcp"
        - packages with "mcp" in name
        
        For each package found, extract:
        1. Package name and version
        2. Description
        3. GitHub repository URL (if available)
        4. Installation command
        5. Usage examples from README
        
        Focus on packages that appear to be MCP servers or tools.
        """

        result = await self.arun(
            {"messages": [{"role": "user", "content": npm_search_prompt}]}
        )

        return await self._parse_npm_result(result)

    async def discover_from_github_search(self) -> list[dict[str, Any]]:
        """Use GitHub search to find new MCP implementations."""
        print("🐙 Searching GitHub for MCP repositories...")

        github_search_prompt = """
        Search GitHub for Model Context Protocol related repositories.
        
        Search queries to use:
        - "mcp server language:typescript"
        - "model context protocol server"
        - "fastmcp"
        - "@modelcontextprotocol"
        - "mcp client"
        - repos with recent commits containing "mcp"
        
        For each repository found, analyze:
        1. Repository name and description
        2. README content
        3. Package.json or setup files
        4. What type of MCP server it implements
        5. Tools and resources it provides
        
        Look for repositories that might be missing from our current collection.
        """

        result = await self.arun(
            {"messages": [{"role": "user", "content": github_search_prompt}]}
        )

        return await self._parse_github_result(result)

    async def _parse_discovery_result(self, result) -> list[dict[str, Any]]:
        """Parse the LLM result into structured server data."""
        parse_prompt = f"""
        Parse this discovery result into a JSON list of MCP servers:
        
        {result}
        
        Return a JSON array where each server has:
        {{
            "name": "server-name",
            "description": "what it does",
            "repository": "github-url",
            "installation": "install command",
            "capabilities": ["list", "of", "features"],
            "category": "database|filesystem|api|etc"
        }}
        
        Only return valid JSON, no other text.
        """

        parsed_result = await self.arun(
            {"messages": [{"role": "user", "content": parse_prompt}]}
        )

        try:
            return json.loads(parsed_result)
        except json.JSONDecodeError:
            print(f"⚠️  Failed to parse discovery result: {parsed_result[:200]}...")
            return []

    async def _parse_npm_result(self, result) -> list[dict[str, Any]]:
        """Parse npm search results."""
        # Similar parsing logic for npm results
        return await self._parse_discovery_result(result)

    async def _parse_github_result(self, result) -> list[dict[str, Any]]:
        """Parse GitHub search results."""
        # Similar parsing logic for GitHub results
        return await self._parse_discovery_result(result)

    async def run_full_discovery(self) -> dict[str, Any]:
        """Run complete discovery process."""
        print("🚀 Starting comprehensive MCP server discovery...")

        all_discovered = []

        # Discover from different sources
        awesome_servers = await self.discover_from_awesome_lists()
        npm_servers = await self.discover_from_npm_search()
        github_servers = await self.discover_from_github_search()

        all_discovered.extend(awesome_servers)
        all_discovered.extend(npm_servers)
        all_discovered.extend(github_servers)

        # Deduplicate and analyze
        unique_servers = await self._deduplicate_servers(all_discovered)

        print(f"✅ Discovery complete! Found {len(unique_servers)} new servers")

        return {
            "total_discovered": len(all_discovered),
            "unique_servers": len(unique_servers),
            "servers": unique_servers,
            "sources": {
                "awesome_lists": len(awesome_servers),
                "npm_search": len(npm_servers),
                "github_search": len(github_servers),
            },
        }

    async def _deduplicate_servers(
        self, servers: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        """Remove duplicates and analyze quality."""
        seen_repos = set()
        unique_servers = []

        for server in servers:
            repo = server.get("repository", "")
            if repo and repo not in seen_repos:
                seen_repos.add(repo)
                unique_servers.append(server)

        return unique_servers


class EcosystemDiscoveryAgent(MCPDocumentationAgent):
    """Agent that can discover resources in other ecosystems."""

    def __init__(self, engine, ecosystem_type: str):
        super().__init__(engine=engine, name=f"{ecosystem_type}_discovery_agent")
        self.ecosystem_type = ecosystem_type

    async def discover_langchain_tools(self) -> list[dict[str, Any]]:
        """Discover LangChain tools and integrations."""
        print("🦜 Discovering LangChain tools...")

        langchain_prompt = """
        Analyze the LangChain ecosystem to find tools and integrations:
        
        1. Search the langchain-ai/langchain repository
        2. Look for tool implementations in langchain/tools/
        3. Find integration packages for external services
        4. Analyze documentation for setup patterns
        
        For each tool/integration found, extract:
        - Tool name and purpose
        - Installation requirements
        - Configuration needed
        - Usage examples
        - What external services it connects to
        
        Focus on tools that could be useful for AI agents.
        """

        result = await self.arun(
            {"messages": [{"role": "user", "content": langchain_prompt}]}
        )

        return await self._parse_ecosystem_result(result, "langchain_tool")

    async def discover_huggingface_models(self) -> list[dict[str, Any]]:
        """Discover useful Hugging Face models."""
        print("🤗 Discovering Hugging Face models...")

        hf_prompt = """
        Analyze the Hugging Face Hub to find useful models:
        
        1. Look for models with good documentation
        2. Focus on models useful for agents:
           - Text generation models
           - Code generation models  
           - Tool-use models
           - Specialized domain models
        3. Extract model capabilities from model cards
        4. Find setup and usage patterns
        
        For each model, extract:
        - Model name and description
        - Capabilities and use cases
        - Hardware requirements
        - Setup instructions
        - Example usage code
        
        Focus on models that would enhance agent capabilities.
        """

        result = await self.arun({"messages": [{"role": "user", "content": hf_prompt}]})

        return await self._parse_ecosystem_result(result, "huggingface_model")

    async def _parse_ecosystem_result(
        self, result: str, resource_type: str
    ) -> list[dict[str, Any]]:
        """Parse ecosystem discovery results."""
        parse_prompt = f"""
        Parse this {resource_type} discovery result into JSON:
        
        {result}
        
        Return a JSON array where each resource has:
        {{
            "name": "resource-name",
            "type": "{resource_type}",
            "description": "what it does", 
            "setup_instructions": "how to install/configure",
            "capabilities": ["list", "of", "features"],
            "usage_example": "code example",
            "requirements": ["dependencies"]
        }}
        
        Only return valid JSON.
        """

        parsed_result = await self.arun(
            {"messages": [{"role": "user", "content": parse_prompt}]}
        )

        try:
            return json.loads(parsed_result)
        except json.JSONDecodeError:
            print(f"⚠️  Failed to parse {resource_type} result")
            return []


async def main():
    """Run automated discovery examples."""
    print("🤖 Starting Automated Discovery Agent Demo")
    print("=" * 50)

    # Create engine for agents
    engine = AugLLMConfig(name="discovery_engine")

    # Example 1: Enhanced MCP Discovery
    print("\n1️⃣  MCP Server Discovery")
    mcp_agent = EnhancedMCPDiscoveryAgent(engine)
    await mcp_agent.setup()

    # Run discovery (this would actually search for new servers)
    discovery_results = await mcp_agent.run_full_discovery()

    print("📊 Discovery Results:")
    print(f"   Total found: {discovery_results['total_discovered']}")
    print(f"   Unique servers: {discovery_results['unique_servers']}")
    print(f"   From awesome lists: {discovery_results['sources']['awesome_lists']}")
    print(f"   From npm search: {discovery_results['sources']['npm_search']}")
    print(f"   From GitHub search: {discovery_results['sources']['github_search']}")

    # Example 2: LangChain Tools Discovery
    print("\n2️⃣  LangChain Tools Discovery")
    langchain_agent = EcosystemDiscoveryAgent(engine, "langchain")
    await langchain_agent.setup()

    langchain_tools = await langchain_agent.discover_langchain_tools()
    print(f"🦜 Found {len(langchain_tools)} LangChain tools")

    # Example 3: Hugging Face Models Discovery
    print("\n3️⃣  Hugging Face Models Discovery")
    hf_agent = EcosystemDiscoveryAgent(engine, "huggingface")
    await hf_agent.setup()

    hf_models = await hf_agent.discover_huggingface_models()
    print(f"🤗 Found {len(hf_models)} useful HF models")

    print("\n✅ Automated discovery complete!")
    print("\n💡 Next steps:")
    print("   - Generate agents that can use discovered resources")
    print("   - Update databases with new findings")
    print("   - Create automated integration workflows")


if __name__ == "__main__":
    asyncio.run(main())
