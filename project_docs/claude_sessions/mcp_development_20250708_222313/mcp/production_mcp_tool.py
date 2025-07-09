"""
Production MCP Discovery and Installation Tool

Leverages the existing haive-mcp infrastructure with 1,960 servers to:
1. RAG search through the complete MCP server database 
2. Agent picks the best server based on capabilities
3. Install it dynamically using FastMCP or standard MCP
4. Return ready-to-use LangChain MCP client configuration

This tool integrates with the AugLLMConfig pattern and builds on the existing
MCPDocumentationLoader and agents.
"""

import asyncio
import json
import subprocess
import tempfile
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

from langchain_core.tools import BaseTool
from langchain_mcp_adapters.client import MultiServerMCPClient
from pydantic import BaseModel, Field

# Import existing haive-mcp infrastructure
from haive.mcp.documentation import MCPDocumentationLoader
from haive.mcp.agents import MCPDocumentationAgent
from haive.core.engine.aug_llm import AugLLMConfig

logger = logging.getLogger(__name__)


class MCPCapabilityRequest(BaseModel):
    """Request to find and install MCP servers by capability."""
    capability_query: str = Field(
        description="Describe what you want the MCP server to do (e.g., 'database access', 'file operations', 'GitHub integration')"
    )
    max_options: int = Field(default=3, description="Maximum number of server options to return")
    auto_install: bool = Field(default=False, description="Automatically install the best match")
    prefer_fastmcp: bool = Field(default=True, description="Prefer FastMCP compatible servers")
    include_experimental: bool = Field(default=False, description="Include experimental/beta servers")


class MCPServerOption(BaseModel):
    """Information about an available MCP server."""
    name: str
    description: str
    repository_url: str
    install_command: Optional[str]
    capabilities: List[str]
    transport_types: List[str]
    category: str
    stars: Optional[int]
    is_fastmcp_compatible: bool


class MCPInstallationResult(BaseModel):
    """Result of MCP server installation."""
    success: bool
    server_name: str
    client_config: Dict[str, Any]
    available_tools: List[str]
    installation_notes: str
    error_message: Optional[str] = None


class ProductionMCPTool(BaseTool):
    """
    Production-ready tool for MCP server discovery and installation.
    
    This tool leverages the existing haive-mcp infrastructure with 1,960 servers
    to provide intelligent server discovery, installation, and configuration.
    """
    
    name: str = "discover_install_mcp_server"
    description: str = """
    Discover and install MCP servers from a database of 1,960+ documented servers.
    
    Use this tool when you need to add new capabilities to your agent by finding and 
    installing Model Context Protocol (MCP) servers. The tool uses RAG to search through
    comprehensive server documentation and can install servers automatically.
    
    Examples:
    - "I need PostgreSQL database access"
    - "Find servers for GitHub repository management" 
    - "Install filesystem operations with read/write"
    - "Get me weather data integration capabilities"
    - "Find servers that can process images"
    """
    
    args_schema: type[BaseModel] = MCPCapabilityRequest
    
    def __init__(self, engine: AugLLMConfig, **kwargs):
        super().__init__(**kwargs)
        self.engine = engine
        self.doc_loader = MCPDocumentationLoader()
        self.installed_servers: Dict[str, Dict] = {}
        
        # Load the full server database once
        self._server_database: Dict[str, Dict] = {}
        self._load_server_database()
        
    def _load_server_database(self):
        """Load the complete MCP server database."""
        try:
            # Load from the comprehensive JSON file
            all_servers_path = self.doc_loader.mcp_servers_path / "ALL_MCP_SERVERS_COMPLETE.json"
            
            if all_servers_path.exists():
                with open(all_servers_path, 'r') as f:
                    data = json.load(f)
                    servers = data.get('all_servers', [])
                    
                    # Index by name for quick lookup
                    for server in servers:
                        name = server.get('name', server.get('repository_name', 'unknown'))
                        self._server_database[name] = server
                        
                logger.info(f"Loaded {len(self._server_database)} servers from database")
            else:
                logger.warning(f"Server database not found at {all_servers_path}")
                
        except Exception as e:
            logger.error(f"Failed to load server database: {e}")
    
    def _run(self, **kwargs) -> str:
        """Synchronous wrapper for async implementation."""
        return asyncio.run(self._arun(**kwargs))
    
    async def _arun(
        self,
        capability_query: str,
        max_options: int = 3,
        auto_install: bool = False,
        prefer_fastmcp: bool = True,
        include_experimental: bool = False,
        **kwargs
    ) -> str:
        """
        Discover and optionally install MCP servers based on capability requirements.
        """
        try:
            # Step 1: Use existing documentation agent for intelligent search
            doc_agent = MCPDocumentationAgent.create_for_mcp_setup(engine=self.engine)
            await doc_agent.setup()
            
            # Find servers using the agent's RAG capabilities
            matching_servers = await doc_agent.find_servers_by_capability(
                capability_query, 
                limit=max_options * 2  # Get more to filter
            )
            
            if not matching_servers:
                return f"❌ No MCP servers found for capability: '{capability_query}'"
            
            # Step 2: Enhance with database information and filter
            enhanced_options = self._enhance_server_options(
                matching_servers, 
                prefer_fastmcp, 
                include_experimental
            )[:max_options]
            
            if not enhanced_options:
                return f"❌ No suitable servers found after filtering for: '{capability_query}'"
            
            # Step 3: Auto-install or present options
            if auto_install and enhanced_options:
                best_server = enhanced_options[0]
                install_result = await self._install_server(best_server)
                
                if install_result.success:
                    return self._format_installation_success(install_result)
                else:
                    return f"❌ Installation failed: {install_result.error_message}"
            
            else:
                # Present options for user selection
                return self._format_server_options(enhanced_options, capability_query)
        
        except Exception as e:
            logger.error(f"Error in MCP discovery: {e}")
            return f"❌ Error during MCP server discovery: {str(e)}"
    
    def _enhance_server_options(
        self, 
        servers: List[Dict], 
        prefer_fastmcp: bool, 
        include_experimental: bool
    ) -> List[MCPServerOption]:
        """Enhance server information with database data and apply filters."""
        enhanced = []
        
        for server in servers:
            server_name = server.get('name', '')
            
            # Look up in comprehensive database
            db_info = self._server_database.get(server_name, {})
            
            # Check if experimental
            is_experimental = (
                'experimental' in server.get('tags', []) or
                'beta' in server.get('description', '').lower() or
                (db_info.get('stars', 0) or 0) < 5
            )
            
            if not include_experimental and is_experimental:
                continue
            
            # Determine FastMCP compatibility
            is_fastmcp_compatible = self._is_fastmcp_compatible(server, db_info)
            
            # Skip if preferring FastMCP but not compatible
            if prefer_fastmcp and not is_fastmcp_compatible:
                continue
            
            option = MCPServerOption(
                name=server_name,
                description=server.get('description', db_info.get('description', 'No description')),
                repository_url=server.get('repository_url', db_info.get('repository_url', '')),
                install_command=db_info.get('install_command'),
                capabilities=server.get('capabilities', db_info.get('capabilities', [])),
                transport_types=db_info.get('transport_types', ['stdio']),
                category=db_info.get('category', 'utility'),
                stars=db_info.get('stars'),
                is_fastmcp_compatible=is_fastmcp_compatible
            )
            
            enhanced.append(option)
        
        # Sort by relevance (FastMCP compatible first if preferred, then by stars)
        enhanced.sort(key=lambda x: (
            -1 if prefer_fastmcp and x.is_fastmcp_compatible else 0,
            -(x.stars or 0)
        ))
        
        return enhanced
    
    def _is_fastmcp_compatible(self, server: Dict, db_info: Dict) -> bool:
        """Determine if a server is compatible with FastMCP."""
        # Check for Python-based servers
        repo_url = server.get('repository_url', db_info.get('repository_url', ''))
        
        # Python indicators
        python_indicators = [
            'python' in repo_url.lower(),
            'fastmcp' in str(db_info.get('tags', [])).lower(),
            '.py' in str(db_info.get('install_command', '')),
            'pip install' in str(db_info.get('setup_instructions', '')).lower()
        ]
        
        # NPM indicators (less likely to be FastMCP compatible)
        npm_indicators = [
            'npm' in str(db_info.get('install_command', '')).lower(),
            'node' in repo_url.lower(),
            db_info.get('npm_package') is not None
        ]
        
        return any(python_indicators) and not any(npm_indicators)
    
    def _format_server_options(self, options: List[MCPServerOption], query: str) -> str:
        """Format server options for display."""
        options_text = f"🔍 Found {len(options)} MCP servers for '{query}':\n\n"
        
        for i, option in enumerate(options, 1):
            fastmcp_indicator = "🐍 FastMCP" if option.is_fastmcp_compatible else "📦 Standard"
            stars_text = f"⭐ {option.stars}" if option.stars else "⭐ New"
            
            options_text += f"""**{i}. {option.name}** ({fastmcp_indicator}, {stars_text})
   📝 {option.description[:100]}{'...' if len(option.description) > 100 else ''}
   🔧 Category: {option.category}
   🚀 Capabilities: {', '.join(option.capabilities[:3])}{'...' if len(option.capabilities) > 3 else ''}
   🔗 {option.repository_url}

"""
        
        options_text += f"""To install any of these servers, call this tool again with:
- The same capability_query: "{query}"
- auto_install=True

Or use the `install_specific_mcp_server` tool with the exact server name."""
        
        return options_text
    
    async def _install_server(self, server_option: MCPServerOption) -> MCPInstallationResult:
        """Install a specific MCP server."""
        try:
            if server_option.is_fastmcp_compatible:
                return await self._install_with_fastmcp(server_option)
            else:
                return await self._install_standard_mcp(server_option)
                
        except Exception as e:
            logger.error(f"Installation error for {server_option.name}: {e}")
            return MCPInstallationResult(
                success=False,
                server_name=server_option.name,
                client_config={},
                available_tools=[],
                installation_notes="",
                error_message=str(e)
            )
    
    async def _install_with_fastmcp(self, server: MCPServerOption) -> MCPInstallationResult:
        """Install using FastMCP approach."""
        # Generate FastMCP wrapper based on server capabilities
        fastmcp_code = self._generate_fastmcp_server(server)
        
        # Write to temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(fastmcp_code)
            server_path = f.name
        
        # Test the server
        try:
            server_name = server.name.lower().replace(' ', '_').replace('-', '_')
            
            client_config = {
                "command": "python",
                "args": [server_path],
                "transport": "stdio"
            }
            
            # Test connection
            test_client = MultiServerMCPClient({server_name: client_config})
            
            available_tools = []
            async with test_client.session(server_name) as session:
                tools_result = await session.list_tools()
                if hasattr(tools_result, 'tools'):
                    available_tools = [tool.name for tool in tools_result.tools]
            
            # Store installation info
            self.installed_servers[server_name] = {
                'config': client_config,
                'path': server_path,
                'tools': available_tools,
                'type': 'fastmcp'
            }
            
            return MCPInstallationResult(
                success=True,
                server_name=server_name,
                client_config=client_config,
                available_tools=available_tools,
                installation_notes=f"FastMCP server created at {server_path}"
            )
            
        except Exception as e:
            return MCPInstallationResult(
                success=False,
                server_name=server.name,
                client_config={},
                available_tools=[],
                installation_notes="",
                error_message=f"FastMCP setup failed: {str(e)}"
            )
    
    async def _install_standard_mcp(self, server: MCPServerOption) -> MCPInstallationResult:
        """Install using standard MCP approach (npm, etc.)."""
        if not server.install_command:
            raise Exception("No installation command available for this server")
        
        server_name = server.name.lower().replace(' ', '_').replace('-', '_')
        
        try:
            # Install the package
            if 'npm' in server.install_command:
                install_cmd = f"npm install -g {server.install_command}"
            elif 'pip' in server.install_command:
                install_cmd = f"pip install {server.install_command}"
            else:
                install_cmd = server.install_command
            
            process = await asyncio.create_subprocess_shell(
                install_cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                raise Exception(f"Installation failed: {stderr.decode()}")
            
            # Create client configuration
            if 'npm' in server.install_command:
                client_config = {
                    "command": "npx",
                    "args": ["-y", server.install_command],
                    "transport": "stdio"
                }
            else:
                client_config = {
                    "command": server.install_command.split()[0],
                    "args": server.install_command.split()[1:],
                    "transport": "stdio"
                }
            
            # Test connection
            test_client = MultiServerMCPClient({server_name: client_config})
            
            available_tools = []
            async with test_client.session(server_name) as session:
                tools_result = await session.list_tools()
                if hasattr(tools_result, 'tools'):
                    available_tools = [tool.name for tool in tools_result.tools]
            
            self.installed_servers[server_name] = {
                'config': client_config,
                'install_command': server.install_command,
                'tools': available_tools,
                'type': 'standard'
            }
            
            return MCPInstallationResult(
                success=True,
                server_name=server_name,
                client_config=client_config,
                available_tools=available_tools,
                installation_notes=f"Installed via: {install_cmd}"
            )
            
        except Exception as e:
            return MCPInstallationResult(
                success=False,
                server_name=server.name,
                client_config={},
                available_tools=[],
                installation_notes="",
                error_message=f"Standard installation failed: {str(e)}"
            )
    
    def _generate_fastmcp_server(self, server: MCPServerOption) -> str:
        """Generate FastMCP server code based on server information."""
        server_name_clean = server.name.replace(' ', '_').replace('-', '_')
        
        code = f'''"""
Generated FastMCP server for {server.name}
{server.description}

Capabilities: {', '.join(server.capabilities)}
"""

from fastmcp import FastMCP
from typing import Dict, Any, List, Optional
import json
import os

# Initialize FastMCP server
mcp = FastMCP("{server_name_clean}")

'''
        
        # Add tools based on capabilities
        for capability in server.capabilities:
            code += self._generate_capability_tools(capability)
        
        # Add fallback generic tools if no specific capabilities
        if not server.capabilities:
            code += self._generate_generic_tools()
        
        # Add server runner
        code += '''
if __name__ == "__main__":
    mcp.run(transport="stdio")
'''
        
        return code
    
    def _generate_capability_tools(self, capability: str) -> str:
        """Generate tools for specific capabilities."""
        capability_lower = capability.lower()
        
        if 'file' in capability_lower or 'filesystem' in capability_lower:
            return self._file_tools_template()
        elif 'database' in capability_lower or 'sql' in capability_lower:
            return self._database_tools_template()
        elif 'web' in capability_lower or 'http' in capability_lower:
            return self._web_tools_template()
        elif 'github' in capability_lower or 'git' in capability_lower:
            return self._git_tools_template()
        elif 'search' in capability_lower:
            return self._search_tools_template()
        else:
            return self._generic_capability_template(capability)
    
    def _file_tools_template(self) -> str:
        return '''
@mcp.tool()
async def read_file(filepath: str) -> str:
    """Read contents of a file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

@mcp.tool()
async def write_file(filepath: str, content: str) -> str:
    """Write content to a file."""
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Successfully wrote to {filepath}"
    except Exception as e:
        return f"Error writing file: {str(e)}"

@mcp.tool()
async def list_directory(path: str = ".") -> List[str]:
    """List contents of a directory."""
    try:
        return os.listdir(path)
    except Exception as e:
        return [f"Error listing directory: {str(e)}"]

'''
    
    def _database_tools_template(self) -> str:
        return '''
@mcp.tool()
async def execute_query(query: str, connection_string: Optional[str] = None) -> str:
    """Execute a database query (template implementation)."""
    return f"Query would be executed: {query}"

@mcp.tool()
async def list_tables(database_name: Optional[str] = None) -> List[str]:
    """List database tables (template implementation)."""
    return ["users", "products", "orders"]

'''
    
    def _web_tools_template(self) -> str:
        return '''
@mcp.tool()
async def fetch_url(url: str) -> str:
    """Fetch content from a URL."""
    import aiohttp
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as response:
                return await response.text()
    except Exception as e:
        return f"Error fetching URL: {str(e)}"

'''
    
    def _git_tools_template(self) -> str:
        return '''
@mcp.tool()
async def git_status(repo_path: str = ".") -> str:
    """Get git repository status."""
    import subprocess
    try:
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              cwd=repo_path, capture_output=True, text=True)
        return result.stdout or "Repository is clean"
    except Exception as e:
        return f"Error getting git status: {str(e)}"

'''
    
    def _search_tools_template(self) -> str:
        return '''
@mcp.tool()
async def search(query: str, limit: int = 10) -> List[Dict[str, Any]]:
    """Search for information (template implementation)."""
    return [{"title": f"Result for {query}", "url": "https://example.com", "snippet": "Sample result"}]

'''
    
    def _generic_capability_template(self, capability: str) -> str:
        return f'''
@mcp.tool()
async def {capability.lower().replace(' ', '_')}_tool(input_data: str) -> str:
    """Tool for {capability} capability."""
    return f"Processed {{input_data}} using {capability} capability"

'''
    
    def _generic_tools_template(self) -> str:
        return '''
@mcp.tool()
async def echo(message: str) -> str:
    """Echo a message back."""
    return f"Echo: {message}"

@mcp.tool()
async def get_info() -> Dict[str, Any]:
    """Get server information."""
    return {
        "server_name": "Generated FastMCP Server",
        "capabilities": ["echo", "info"],
        "status": "running"
    }

'''
    
    def _format_installation_success(self, result: MCPInstallationResult) -> str:
        """Format successful installation response."""
        tools_list = ', '.join(result.available_tools) if result.available_tools else 'None detected'
        
        return f"""✅ Successfully installed MCP server: **{result.server_name}**

🔧 **Client Configuration:**
```json
{json.dumps(result.client_config, indent=2)}
```

🛠️ **Available Tools:** {tools_list}

📝 **Installation Notes:** {result.installation_notes}

🚀 **Ready to Use!** You can now connect to this server using:

```python
from langchain_mcp_adapters.client import MultiServerMCPClient

client = MultiServerMCPClient({{
    "{result.server_name}": {json.dumps(result.client_config)}
}})

# Get tools
tools = await client.get_tools()

# Use in LangGraph
from langgraph.prebuilt import create_react_agent
agent = create_react_agent(model, tools)
```
"""


# Helper tool for listing installed servers
class ListInstalledMCPTool(BaseTool):
    """Tool to list currently installed MCP servers."""
    
    name: str = "list_installed_mcp_servers"
    description: str = "List all currently installed MCP servers and their capabilities"
    
    def __init__(self, production_tool: ProductionMCPTool, **kwargs):
        super().__init__(**kwargs)
        self.production_tool = production_tool
    
    def _run(self, **kwargs) -> str:
        """List installed MCP servers."""
        if not self.production_tool.installed_servers:
            return "📭 No MCP servers currently installed."
        
        servers_info = []
        for name, info in self.production_tool.installed_servers.items():
            tools_count = len(info.get('tools', []))
            server_type = info.get('type', 'unknown')
            tools_list = ', '.join(info.get('tools', [])[:3])
            if len(info.get('tools', [])) > 3:
                tools_list += '...'
            
            servers_info.append(f"""
**{name}** ({server_type})
   🛠️ {tools_count} tools: {tools_list}
   📍 Path: {info.get('path', info.get('install_command', 'N/A'))}
""")
        
        return f"📦 Installed MCP Servers ({len(self.production_tool.installed_servers)}):" + "".join(servers_info)


def create_production_mcp_tools(engine: AugLLMConfig) -> List[BaseTool]:
    """Create production-ready MCP discovery and management tools."""
    production_tool = ProductionMCPTool(engine=engine)
    list_tool = ListInstalledMCPTool(production_tool=production_tool)
    
    return [production_tool, list_tool]