# Setup Scripts

**Installation and setup scripts for haive-mcp**

## 🚀 Available Scripts

### Installation Scripts

- **`install.py`** - Main installation script for haive-mcp
- **`setup_all.py`** - Complete setup including dependencies and MCP servers
- **`setup_integrated_mcp.sh`** - Shell script for integrated MCP setup

### Usage

```bash
# Basic installation
python scripts/setup/install.py

# Complete setup (Python + Node.js + MCP servers)
python scripts/setup/setup_all.py

# Integrated setup (shell script)
bash scripts/setup/setup_integrated_mcp.sh
```

## 📋 What These Scripts Do

1. **Install Dependencies**: Python packages and Node.js MCP servers
2. **Configure Environment**: Set up environment variables and config files
3. **Validate Installation**: Test that everything is working correctly
4. **Setup Examples**: Prepare example configurations and data

## 🎯 Choose Your Setup

- **`install.py`**: Basic Python package installation only
- **`setup_all.py`**: Full setup for development environment
- **`setup_integrated_mcp.sh`**: Production-ready setup with all components
