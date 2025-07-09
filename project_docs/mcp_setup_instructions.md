# MCP Screenshot Server Setup Instructions for Agent

## Objective
Set up an MCP (Model Context Protocol) screenshot server that allows Claude Desktop to take screenshots of localhost:8003 documentation pages for visual analysis.

## Prerequisites Check
Before starting, verify these requirements:
- [ ] Claude Desktop app is installed
- [ ] Node.js is installed (`node --version`)
- [ ] NPM is working (`npm --version`)
- [ ] Documentation server is running at localhost:8003

## Step 1: Locate Claude Desktop Configuration

### For macOS Users:
```bash
# Navigate to Claude Desktop config directory
cd ~/Library/Application\ Support/Claude/

# Check if config file exists
ls -la claude_desktop_config.json
```

### For Windows Users:
```bash
# Navigate using Windows Run command (Windows + R)
# Type: %APPDATA%\Claude
# Or use command line:
cd %APPDATA%\Claude

# Check if config file exists
dir claude_desktop_config.json
```

### For Linux Users:
```bash
# Navigate to Claude Desktop config directory
cd ~/.config/Claude/

# Check if config file exists
ls -la claude_desktop_config.json
```

## Step 2: Install MCP Screenshot Server

Choose one of these options:

### Option A: Basic Screenshot Server (Recommended)
```bash
# Install the screenshot MCP server globally
npm install -g @sethbang/mcp-screenshot-server
```

### Option B: Browser-based Screenshot Server (More Features)
```bash
# Install browser automation server
npm install -g browser-use-mcp-server
```

## Step 3: Create/Update Claude Desktop Configuration

Create or edit the `claude_desktop_config.json` file:

### For Basic Screenshot Server:
```json
{
  "mcpServers": {
    "screenshot": {
      "command": "npx",
      "args": [
        "-y",
        "@sethbang/mcp-screenshot-server"
      ],
      "env": {
        "HOST": "localhost"
      }
    }
  }
}
```

### For Browser-based Server:
```json
{
  "mcpServers": {
    "browser": {
      "command": "npx",
      "args": [
        "-y", 
        "browser-use-mcp-server"
      ],
      "env": {
        "HOST": "localhost",
        "PORT": "8000"
      }
    }
  }
}
```

## Step 4: Verify Documentation Server

Ensure the Haive documentation server is running:

```bash
# Navigate to docs directory
cd /home/will/Projects/haive/backend/haive/docs

# Check if server is running
ps aux | grep sphinx-autobuild

# If not running, start it:
poetry run sphinx-autobuild source _build/html --port 8003 --host 0.0.0.0 --ignore "*.pyc" --watch ../packages --open-browser -j auto
```

## Step 5: Restart Claude Desktop

1. **Completely close Claude Desktop**
   - Use Cmd+Q on macOS or Alt+F4 on Windows
   - Or right-click taskbar icon and select "Quit"

2. **Restart Claude Desktop**
   - Launch from Applications (macOS) or Start Menu (Windows)

## Step 6: Verify MCP Integration

1. **Look for MCP indicator**
   - Check for a hammer icon (🔨) in the chat input area
   - Or look for "MCP" indicator in bottom-left corner

2. **Test screenshot functionality**
   - In Claude Desktop, type: "Take a screenshot of localhost:8003"
   - Or: "Show me what localhost:8003 looks like"

## Step 7: Troubleshooting

### If MCP server isn't detected:

1. **Check configuration file syntax**
   ```bash
   # Validate JSON syntax
   python -c "import json; print(json.load(open('claude_desktop_config.json')))"
   ```

2. **Check MCP server installation**
   ```bash
   # Verify screenshot server is installed
   npx @sethbang/mcp-screenshot-server --help
   ```

3. **Check Claude Desktop logs**
   - Look for files named `mcp-server-*.log` in the Claude config directory
   - Check for error messages

4. **Manual server test**
   ```bash
   # Test running the server manually
   npx -y @sethbang/mcp-screenshot-server
   ```

### If localhost:8003 is not accessible:

1. **Verify server is running**
   ```bash
   curl -I http://localhost:8003/
   ```

2. **Check firewall settings**
   - Ensure port 8003 is not blocked

3. **Test from browser**
   - Open http://localhost:8003/ in your browser
   - Verify documentation loads correctly

## Expected Outcome

After successful setup, you should be able to:

1. **See MCP tools available** in Claude Desktop interface
2. **Request screenshots** of localhost:8003 pages
3. **Get visual feedback** about documentation appearance
4. **Ask questions** about the documentation layout and styling

## Usage Examples

Once set up, try these commands in Claude Desktop:

```
"Take a screenshot of localhost:8003"
"Show me how the main documentation page looks"
"Capture the current state of localhost:8003/agents/gallery.html"
"What does the documentation homepage look like right now?"
```

## Security Notes

- MCP servers run with your user permissions
- Only install trusted MCP servers
- The screenshot server only captures what's visible on your local machine
- Localhost access is limited to your machine only

## Success Indicators

✅ Claude Desktop shows MCP tools available  
✅ Can request and receive screenshots of localhost:8003  
✅ Documentation pages are visually accessible through Claude  
✅ Can analyze documentation styling and layout issues  

## Next Steps

After setup, you can:
1. Ask for screenshots of specific documentation pages
2. Get visual feedback on styling changes
3. Identify white-on-white text issues
4. Analyze documentation layout and navigation
5. Compare before/after styling changes

Remember: This setup allows visual analysis of the documentation without needing to share screenshots manually!