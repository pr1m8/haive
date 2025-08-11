"""Complete MCP Example with Self-Query Retriever, HITL, and Live Server
Testing.

This example demonstrates:
1. Setting up a self-query retriever for the MCP server database
2. Using AutoTree for hierarchical categorization
3. Installing the highest-ranked GitHub MCP server with HITL approval
4. Actually starting the server and testing tools, resources, and prompts
"""

import asyncio
import json
import tempfile
from typing import Any, Union

from haive.core.common.structures.tree import AutoTree
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.engine.retriever.providers.SelfQueryRetrieverConfig import (
    SelfQueryRetrieverConfig,
)
from haive.core.engine.vectorstore.providers.ChromaVectorStoreConfig import (
    ChromaVectorStoreConfig,
)
from haive.mcp.documentation import MCPDocumentationLoader
from langchain_core.documents import Document
from langchain_mcp_adapters.client import MultiServerMCPClient
from pydantic import BaseModel, Field

# Haive imports

# LangChain imports

# Pydantic models


# === MODELS FOR MCP SERVER HIERARCHY ===


class MCPCapability(BaseModel):
    """Individual capability of an MCP server."""

    name: str
    category: str = "general"
    description: str | None = None


class MCPServer(BaseModel):
    """MCP server with metadata."""

    name: str
    repository_url: str
    description: str
    category: str
    stars: int | None = None
    capabilities: list[str] = Field(default_factory=list)
    install_command: str | None = None
    transport_types: list[str] = Field(default_factory=list)


class MCPCategory(BaseModel):
    """Category of MCP servers."""

    name: str
    description: str
    servers: list[Union[MCPServer, "MCPCategory"]] = Field(default_factory=list)


MCPCategory.model_rebuild()  # Enable self-referential model


# === HITL APPROVAL SYSTEM ===


class HITLApprovalRequest(BaseModel):
    """Request for human approval."""

    action: str
    target: str
    risk_level: str = "medium"
    description: str
    metadata: dict[str, Any] = Field(default_factory=dict)


class HITLApprovalSystem:
    """Simple HITL approval system for dangerous operations."""

    def __init__(self, auto_approve_low_risk: bool = True):
        self.auto_approve_low_risk = auto_approve_low_risk
        self.approval_history: list[HITLApprovalRequest] = []

    async def request_approval(self, request: HITLApprovalRequest) -> bool:
        """Request human approval for an action."""
        self.approval_history.append(request)

        # Auto-approve low risk
        if self.auto_approve_low_risk and request.risk_level == "low":
            return True

        # Display request

        if request.metadata:
            for _key, _value in request.metadata.items():
                pass

        # Get user input
        while True:
            response = input("Approve? (y/n/details): ").lower().strip()
            if response == "y":
                return True
            if response == "n":
                return False
            if response == "details":
                pass
            else:
                pass


# === COMPLETE MCP SYSTEM ===


class CompleteMCPSystem:
    """Complete MCP system with retriever, categorization, and live testing."""

    def __init__(self, engine: AugLLMConfig):
        self.engine = engine
        self.doc_loader = MCPDocumentationLoader()
        self.hitl = HITLApprovalSystem(auto_approve_low_risk=True)
        self.retriever = None
        self.server_tree = None
        self.installed_servers: dict[str, dict] = {}

    async def setup_retriever(self) -> None:
        """Set up self-query retriever for MCP servers."""
        # Load all server documents
        all_servers = self.doc_loader.load_all_mcp_documents()

        # Convert to LangChain documents with metadata
        documents = []
        for server_name, server_data in all_servers.items():
            # Create document content
            content = f"""
Server: {server_data.get("name", server_name)}
Description: {server_data.get("description", "No description")}
Capabilities: {", ".join(server_data.get("capabilities", []))}
Category: {server_data.get("category", "general")}
Install: {server_data.get("install_command", "Not specified")}
"""

            # Create metadata for self-query
            metadata = {
                "name": server_data.get("name", server_name),
                "category": server_data.get("category", "general"),
                "stars": server_data.get("stars", 0) or 0,
                "has_install_command": bool(server_data.get("install_command")),
                "transport_type": (
                    server_data.get("transport_types", ["stdio"])[0]
                    if server_data.get("transport_types")
                    else "stdio"
                ),
                "capability_count": len(server_data.get("capabilities", [])),
                "repository_url": server_data.get("repository_url", ""),
            }

            doc = Document(page_content=content, metadata=metadata)
            documents.append(doc)

        # Create vector store
        vs_config = ChromaVectorStoreConfig(
            name="mcp_servers",
            collection_name="mcp_server_docs",
            persist_directory="/tmp/mcp_server_vectorstore",
        )
        vectorstore = vs_config.instantiate()

        # Add documents to vector store
        vectorstore.add_documents(documents)

        # Define metadata fields for self-query
        metadata_fields = [
            {
                "name": "category",
                "description": "The category of the MCP server (filesystem, database, etc.)",
                "type": "string",
            },
            {
                "name": "stars",
                "description": "Number of GitHub stars",
                "type": "integer",
            },
            {
                "name": "has_install_command",
                "description": "Whether the server has an install command",
                "type": "boolean",
            },
            {
                "name": "capability_count",
                "description": "Number of capabilities the server provides",
                "type": "integer",
            },
        ]

        # Create self-query retriever
        retriever_config = SelfQueryRetrieverConfig(
            name="mcp_self_query",
            vectorstore_config=vs_config,
            llm_config=self.engine,
            document_content_description="MCP server documentation including names, descriptions, capabilities, and installation instructions",
            metadata_field_info=metadata_fields,
            k=10,
        )

        self.retriever = retriever_config.instantiate()

    def build_category_tree(self) -> AutoTree:
        """Build hierarchical category tree of MCP servers."""
        # Load comprehensive server data
        all_servers_path = (
            self.doc_loader.mcp_servers_path / "ALL_MCP_SERVERS_COMPLETE.json"
        )
        with open(all_servers_path) as f:
            data = json.load(f)
            servers = data.get("all_servers", [])

        # Create root category
        root = MCPCategory(
            name="All MCP Servers",
            description=f"Complete collection of {len(servers)} MCP servers",
        )

        # Group by category
        categories: dict[str, MCPCategory] = {}

        for server_data in servers:
            category_name = server_data.get("category", "general")

            # Create category if needed
            if category_name not in categories:
                categories[category_name] = MCPCategory(
                    name=category_name.title(),
                    description=f"MCP servers for {category_name}",
                )
                root.servers.append(categories[category_name])

            # Create server model
            server = MCPServer(
                name=server_data.get("name", "Unknown"),
                repository_url=server_data.get("repository_url", ""),
                description=server_data.get("description", ""),
                category=category_name,
                stars=server_data.get("stars"),
                capabilities=server_data.get("capabilities", []),
                install_command=server_data.get("install_command"),
                transport_types=server_data.get("transport_types", ["stdio"]),
            )

            categories[category_name].servers.append(server)

        # Sort categories by server count
        root.servers.sort(key=lambda cat: len(cat.servers), reverse=True)

        # Create tree
        self.server_tree = AutoTree(root)

        # Show summary
        for _cat_name, _cat in categories.items():
            pass

        return self.server_tree

    async def find_and_install_top_server(
        self, query: str = "highest quality github integration"
    ) -> str | None:
        """Find and install the top server matching a query."""
        # Use self-query retriever
        docs = await self.retriever.aget_relevant_documents(query)

        if not docs:
            return None

        # Sort by stars and pick top
        sorted_docs = sorted(
            docs, key=lambda d: d.metadata.get("stars", 0), reverse=True
        )

        top_doc = sorted_docs[0]
        server_name = top_doc.metadata["name"]
        stars = top_doc.metadata.get("stars", 0)

        # Request HITL approval for installation
        approval_request = HITLApprovalRequest(
            action="Install MCP Server",
            target=server_name,
            risk_level="medium",
            description=f"Install MCP server from GitHub with {stars} stars",
            metadata={
                "repository_url": top_doc.metadata.get("repository_url", ""),
                "category": top_doc.metadata.get("category", ""),
                "capabilities": top_doc.metadata.get("capability_count", 0),
            },
        )

        approved = await self.hitl.request_approval(approval_request)

        if not approved:
            return None

        # Install the server
        return await self._install_server(server_name, top_doc.metadata)

    async def _install_server(self, server_name: str, metadata: dict) -> str | None:
        """Install an MCP server."""
        # For this example, we'll create a simple FastMCP server
        # In production, you'd use the actual install command

        server_code = f'''"""
Auto-generated MCP server for {server_name}
Category: {metadata.get("category", "general")}
"""


mcp = FastMCP("{server_name}")

# Example tool
@mcp.tool()
async def hello(name: str = "World") -> str:
    """Say hello to someone."""
    return f"Hello, {{name}}! This is {server_name}."

# Example tool based on category
@mcp.tool()
async def get_info() -> dict:
    """Get server information."""
    return {{
        "server": "{server_name}",
        "category": "{metadata.get("category", "general")}",
        "stars": {metadata.get("stars", 0)},
        "status": "running"
    }}

# Example resource
@mcp.resource("server://info")
async def server_info_resource() -> str:
    """Server information resource."""
    return f"{server_name} - A {metadata.get("category", "general")} MCP server"

# Example prompt
@mcp.prompt()
async def analyze_prompt(topic: str) -> list:
    """Generate analysis prompt."""
    return [{{
        "role": "user",
        "content": f"Please analyze {{topic}} using {server_name} capabilities"
    }}]

if __name__ == "__main__":
    mcp.run(transport="stdio")
'''

        # Write server to temp file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(server_code)
            server_path = f.name

        self.installed_servers[server_name] = {
            "path": server_path,
            "metadata": metadata,
        }

        return server_path

    async def test_server_live(self, server_name: str) -> None:
        """Test a server with live connection."""
        if server_name not in self.installed_servers:
            return

        server_info = self.installed_servers[server_name]
        server_path = server_info["path"]

        # Create MCP client configuration
        client_config = {
            server_name: {
                "command": "python",
                "args": [server_path],
                "transport": "stdio",
            }
        }

        # Connect to server
        client = MultiServerMCPClient(client_config)

        try:
            # Test connection and capabilities
            async with client.session(server_name) as session:
                # List tools
                tools_result = await session.list_tools()
                tools = tools_result.tools if hasattr(tools_result, "tools") else []
                for _tool in tools:
                    pass

                # Test a tool
                if tools:
                    await session.call_tool(
                        tools[0].name,
                        arguments={"name": "Haive"} if tools[0].name == "hello" else {},
                    )

                # List resources
                resources_result = await session.list_resources()
                resources = (
                    resources_result.resources
                    if hasattr(resources_result, "resources")
                    else []
                )
                for _resource in resources:
                    pass

                # Test a resource
                if resources:
                    resource_content = await session.read_resource(resources[0].uri)
                    if resource_content.contents:
                        pass

                # List prompts
                prompts_result = await session.list_prompts()
                prompts = (
                    prompts_result.prompts if hasattr(prompts_result, "prompts") else []
                )
                for _prompt in prompts:
                    pass

                # Test a prompt
                if prompts:
                    prompt_result = await session.get_prompt(
                        prompts[0].name, arguments={"topic": "MCP integration"}
                    )
                    if prompt_result.messages:
                        pass

        except Exception:
            pass

    async def demo_retriever_queries(self) -> None:
        """Demonstrate various self-query retriever queries."""
        queries = [
            "database servers with more than 100 stars",
            "filesystem tools that have install commands",
            "GitHub integration servers",
            "servers with more than 5 capabilities",
            "PostgreSQL or MySQL database servers",
        ]

        for query in queries:
            docs = await self.retriever.aget_relevant_documents(query)
            for _i, _doc in enumerate(docs[:3]):  # Show top 3
                pass


# === MAIN EXECUTION ===


async def main():
    """Run the complete MCP example."""
    # Initialize system
    engine = AugLLMConfig(name="mcp_discovery_engine", model="gpt-4", temperature=0.7)

    system = CompleteMCPSystem(engine)

    # Step 1: Set up retriever
    await system.setup_retriever()

    # Step 2: Build category tree
    system.build_category_tree()

    # Step 3: Demo retriever queries
    await system.demo_retriever_queries()

    # Step 4: Find and install top server
    server_path = await system.find_and_install_top_server(
        "high quality GitHub integration with many stars"
    )

    if server_path:
        # Step 5: Test the server live
        server_name = next(iter(system.installed_servers.keys()))
        await system.test_server_live(server_name)


if __name__ == "__main__":
    asyncio.run(main())
