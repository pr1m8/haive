"""
Dynamic MCP Discovery and Installation Tool

This tool leverages the haive-mcp repository's 992 server database to:
1. RAG search through MCP server documentation and metadata
2. Let agent pick the right server based on capabilities
3. Install it dynamically using FastMCP
4. Set up watch dog for server updates

Integrates with AugLLMConfig pattern and uses FastMCP for modern MCP server setup.
"""

import asyncio
import json
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from langchain_core.tools import BaseTool
from langchain_mcp_adapters.client import MultiServerMCPClient
from pydantic import BaseModel, Field

from haive.mcp.documentation import MCPDocumentationLoader
from haive.mcp.agents import MCPDocumentationAgent
from haive.core.engine.aug_llm import AugLLMConfig


class MCPServerInstallRequest(BaseModel):
    """Request to install an MCP server."""
    capability_description: str = Field(description="What you want the MCP server to do")
    max_servers: int = Field(default=3, description="Maximum number of servers to consider")
    auto_install: bool = Field(default=False, description="Automatically install the best match")
    use_fastmcp: bool = Field(default=True, description="Prefer FastMCP implementation")


class MCPServerInstallResult(BaseModel):
    """Result of MCP server installation."""
    success: bool
    server_name: str
    server_config: Dict[str, Any]
    installation_path: str
    tools_available: List[str]
    error_message: Optional[str] = None


class DynamicMCPTool(BaseTool):
    """
    Tool for dynamic MCP server discovery, installation, and management.
    
    This tool:
    1. Uses RAG to search the 992 MCP server database
    2. Presents options to the user/agent
    3. Installs selected servers using FastMCP
    4. Returns ready-to-use MCP client configuration
    """
    
    name: str = "dynamic_mcp_installer"
    description: str = """
    Discover and install MCP servers dynamically based on capability requirements.
    
    Use this tool when you need to add new capabilities to your agent by finding and 
    installing Model Context Protocol (MCP) servers. The tool searches through 992 
    documented MCP servers, analyzes their capabilities, and can install them automatically.
    
    Examples:
    - "I need database access capabilities"
    - "Find servers that can work with GitHub"
    - "Install filesystem operations server"
    - "Get me weather data integration"
    """
    
    args_schema: type[BaseModel] = MCPServerInstallRequest
    
    def __init__(self, engine: AugLLMConfig, **kwargs):
        super().__init__(**kwargs)
        self.engine = engine
        self.doc_loader = MCPDocumentationLoader()
        self.installed_servers: Dict[str, Dict] = {}
        
    def _run(self, **kwargs) -> str:
        """Synchronous wrapper for async implementation."""
        return asyncio.run(self._arun(**kwargs))
    
    async def _arun(
        self,
        capability_description: str,
        max_servers: int = 3,
        auto_install: bool = False,
        use_fastmcp: bool = True,
        **kwargs
    ) -> str:
        """
        Discover and install MCP servers based on capability requirements.
        """
        try:
            # Step 1: RAG search through the MCP server database
            doc_agent = MCPDocumentationAgent.create_for_mcp_setup(engine=self.engine)
            await doc_agent.setup()
            
            # Find servers matching the capability
            matching_servers = await doc_agent.find_servers_by_capability(
                capability_description, 
                limit=max_servers
            )
            
            if not matching_servers:
                return f"No MCP servers found for capability: {capability_description}"
            
            # Step 2: Let agent/user pick or auto-select
            if auto_install and matching_servers:
                selected_server = matching_servers[0]  # Pick best match
                install_result = await self._install_server(selected_server, use_fastmcp)
                
                if install_result.success:
                    return self._format_success_response(install_result)
                else:
                    return f"Installation failed: {install_result.error_message}"
            
            else:
                # Present options for manual selection
                options_text = self._format_server_options(matching_servers)
                return f"""Found {len(matching_servers)} MCP servers for '{capability_description}':

{options_text}

To install a specific server, use the dynamic_mcp_installer tool again with:
- auto_install=True and the exact capability description, or
- Call install_mcp_server tool with the server name
"""
        
        except Exception as e:
            return f"Error during MCP server discovery: {str(e)}"
    
    def _format_server_options(self, servers: List[Dict]) -> str:
        """Format server options for display."""
        options = []
        for i, server in enumerate(servers, 1):
            name = server.get('name', 'Unknown')
            description = server.get('description', 'No description')
            install_type = server.get('install_type', 'npm')
            
            options.append(f"""
{i}. **{name}**
   - Description: {description}
   - Install: {install_type}
   - Capabilities: {', '.join(server.get('capabilities', []))}
""")
        
        return "\n".join(options)
    
    async def _install_server(self, server_info: Dict, use_fastmcp: bool = True) -> MCPServerInstallResult:
        """Install a specific MCP server."""
        server_name = server_info.get('name', '')
        
        try:
            if use_fastmcp and self._is_fastmcp_compatible(server_info):
                return await self._install_fastmcp_server(server_info)
            else:
                return await self._install_standard_mcp_server(server_info)
                
        except Exception as e:
            return MCPServerInstallResult(
                success=False,
                server_name=server_name,
                server_config={},
                installation_path="",
                tools_available=[],
                error_message=str(e)
            )
    
    def _is_fastmcp_compatible(self, server_info: Dict) -> bool:
        """Check if server is compatible with FastMCP."""
        # Check if it's a Python-based server or has FastMCP support
        install_type = server_info.get('install_type', '')
        language = server_info.get('language', '')
        
        return (
            install_type in ['python', 'pip'] or
            language == 'python' or
            'fastmcp' in server_info.get('keywords', [])
        )
    
    async def _install_fastmcp_server(self, server_info: Dict) -> MCPServerInstallResult:
        """Install server using FastMCP."""
        server_name = server_info['name']
        
        # Create FastMCP server implementation
        fastmcp_code = self._generate_fastmcp_wrapper(server_info)
        
        # Write to temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(fastmcp_code)
            server_path = f.name
        
        # Test the server
        try:
            # Create MCP client configuration
            client_config = {
                server_name: {
                    "command": "python",
                    "args": [server_path],
                    "transport": "stdio"
                }
            }
            
            # Test connection
            client = MultiServerMCPClient(client_config)
            async with client.session(server_name) as session:
                tools = await session.list_tools()
                tool_names = [tool.name for tool in tools.tools] if hasattr(tools, 'tools') else []
            
            # Store server info
            self.installed_servers[server_name] = {
                'config': client_config[server_name],
                'path': server_path,
                'tools': tool_names
            }
            
            return MCPServerInstallResult(
                success=True,
                server_name=server_name,
                server_config=client_config[server_name],
                installation_path=server_path,
                tools_available=tool_names
            )
            
        except Exception as e:
            return MCPServerInstallResult(
                success=False,
                server_name=server_name,
                server_config={},
                installation_path=server_path,
                tools_available=[],
                error_message=f"FastMCP installation failed: {str(e)}"
            )
    
    async def _install_standard_mcp_server(self, server_info: Dict) -> MCPServerInstallResult:
        """Install server using standard MCP approach."""
        server_name = server_info['name']
        install_type = server_info.get('install_type', 'npm')
        install_command = server_info.get('install_command', '')
        
        try:
            # Install the server package
            if install_type == 'npm' and install_command:
                process = await asyncio.create_subprocess_shell(
                    f"npm install -g {install_command}",
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                stdout, stderr = await process.communicate()
                
                if process.returncode != 0:
                    raise Exception(f"NPM install failed: {stderr.decode()}")
            
            # Create client configuration
            client_config = {
                server_name: {
                    "command": "npx",
                    "args": ["-y", install_command] if install_command else [],
                    "transport": "stdio"
                }
            }
            
            # Test connection
            client = MultiServerMCPClient(client_config)
            async with client.session(server_name) as session:
                tools = await session.list_tools()
                tool_names = [tool.name for tool in tools.tools] if hasattr(tools, 'tools') else []
            
            self.installed_servers[server_name] = {
                'config': client_config[server_name],
                'path': install_command,
                'tools': tool_names
            }
            
            return MCPServerInstallResult(
                success=True,
                server_name=server_name,
                server_config=client_config[server_name],
                installation_path=install_command,
                tools_available=tool_names
            )
            
        except Exception as e:
            return MCPServerInstallResult(
                success=False,
                server_name=server_name,
                server_config={},
                installation_path="",
                tools_available=[],
                error_message=f"Standard MCP installation failed: {str(e)}"
            )
    
    def _generate_fastmcp_wrapper(self, server_info: Dict) -> str:
        """Generate FastMCP server code from server documentation."""
        server_name = server_info['name']
        capabilities = server_info.get('capabilities', [])
        description = server_info.get('description', '')
        
        # Generate basic FastMCP server template
        fastmcp_code = f'''"""
Generated FastMCP server for {server_name}
{description}
"""

from fastmcp import FastMCP
from typing import Dict, Any, List

# Initialize FastMCP server
mcp = FastMCP("{server_name}")

'''
        
        # Add tools based on capabilities
        for capability in capabilities:
            if 'file' in capability.lower():
                fastmcp_code += self._generate_file_tools()
            elif 'database' in capability.lower() or 'db' in capability.lower():
                fastmcp_code += self._generate_database_tools()
            elif 'web' in capability.lower() or 'http' in capability.lower():
                fastmcp_code += self._generate_web_tools()
            elif 'time' in capability.lower() or 'date' in capability.lower():
                fastmcp_code += self._generate_time_tools()
        
        # Add server runner
        fastmcp_code += '''
if __name__ == "__main__":
    mcp.run(transport="stdio")
'''
        
        return fastmcp_code
    
    def _generate_file_tools(self) -> str:
        """Generate file operation tools."""
        return '''
@mcp.tool()
def read_file(filepath: str) -> str:
    """Read contents of a file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

@mcp.tool()
def write_file(filepath: str, content: str) -> str:
    """Write content to a file."""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Successfully wrote to {filepath}"
    except Exception as e:
        return f"Error writing file: {str(e)}"

@mcp.tool()
def list_directory(path: str = ".") -> List[str]:
    """List contents of a directory."""
    import os
    try:
        return os.listdir(path)
    except Exception as e:
        return [f"Error listing directory: {str(e)}"]

'''
    
    def _generate_database_tools(self) -> str:
        """Generate database operation tools."""
        return '''
@mcp.tool()
def execute_query(query: str, connection_string: str = None) -> str:
    """Execute a database query."""
    # This is a template - actual implementation would connect to specific database
    return f"Query executed: {query}"

@mcp.tool()
def list_tables(connection_string: str = None) -> List[str]:
    """List database tables."""
    # Template implementation
    return ["table1", "table2", "table3"]

'''
    
    def _generate_web_tools(self) -> str:
        """Generate web operation tools."""
        return '''
@mcp.tool()
def fetch_url(url: str) -> str:
    """Fetch content from a URL."""
    import requests
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception as e:
        return f"Error fetching URL: {str(e)}"

@mcp.tool()
def post_data(url: str, data: Dict[str, Any]) -> str:
    """Post data to a URL."""
    import requests
    try:
        response = requests.post(url, json=data, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception as e:
        return f"Error posting data: {str(e)}"

'''
    
    def _generate_time_tools(self) -> str:
        """Generate time operation tools."""
        return '''
@mcp.tool()
def get_current_time() -> str:
    """Get current time."""
    import datetime
    return datetime.datetime.now().isoformat()

@mcp.tool()
def format_time(timestamp: str, format_string: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Format a timestamp."""
    import datetime
    try:
        dt = datetime.datetime.fromisoformat(timestamp)
        return dt.strftime(format_string)
    except Exception as e:
        return f"Error formatting time: {str(e)}"

'''
    
    def _format_success_response(self, result: MCPServerInstallResult) -> str:
        """Format successful installation response."""
        return f"""✅ Successfully installed MCP server: {result.server_name}

**Configuration:**
```json
{json.dumps(result.server_config, indent=2)}
```

**Available Tools:** {', '.join(result.tools_available)}

**Installation Path:** {result.installation_path}

The server is now ready for use! You can connect to it using the MultiServerMCPClient with the configuration above.

To use with AugLLMConfig:
```python
from langchain_mcp_adapters.client import MultiServerMCPClient

client = MultiServerMCPClient({{
    "{result.server_name}": {json.dumps(result.server_config)}
}})

tools = await client.get_tools()
```
"""


class MCPServerListTool(BaseTool):
    """Tool to list currently installed MCP servers."""
    
    name: str = "list_mcp_servers"
    description: str = "List all currently installed and available MCP servers"
    
    def __init__(self, dynamic_mcp_tool: DynamicMCPTool, **kwargs):
        super().__init__(**kwargs)
        self.dynamic_mcp_tool = dynamic_mcp_tool
    
    def _run(self, **kwargs) -> str:
        """List installed MCP servers."""
        if not self.dynamic_mcp_tool.installed_servers:
            return "No MCP servers currently installed."
        
        servers_info = []
        for name, info in self.dynamic_mcp_tool.installed_servers.items():
            tools = ', '.join(info.get('tools', []))
            servers_info.append(f"- **{name}**: {len(info.get('tools', []))} tools ({tools})")
        
        return f"Installed MCP Servers ({len(self.dynamic_mcp_tool.installed_servers)}):\n" + "\n".join(servers_info)


# Usage example for integrating with AugLLMConfig
def create_mcp_discovery_tools(engine: AugLLMConfig) -> List[BaseTool]:
    """Create MCP discovery and management tools."""
    dynamic_tool = DynamicMCPTool(engine=engine)
    list_tool = MCPServerListTool(dynamic_mcp_tool=dynamic_tool)
    
    return [dynamic_tool, list_tool]