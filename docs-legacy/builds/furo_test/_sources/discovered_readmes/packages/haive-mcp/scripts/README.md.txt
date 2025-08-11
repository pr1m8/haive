# Scripts Directory

**Executable scripts for haive-mcp development, setup, and maintenance**

## 📁 Directory Structure

```
scripts/
├── setup/              # Installation and setup scripts
├── utilities/          # Maintenance and utility scripts
├── run.py             # Main application runner
├── run_mcp_agent.sh   # Shell script to run MCP agent
├── run_working_tests.py # Test runner for working tests
└── background_downloader.py # Background data download
```

## 🚀 Quick Start Scripts

### Running the Application

```bash
# Run main application
python scripts/run.py

# Run MCP agent (shell script)
bash scripts/run_mcp_agent.sh

# Run working tests
python scripts/run_working_tests.py
```

### Setup & Installation

```bash
# Complete setup
python scripts/setup/setup_all.py

# Basic installation
python scripts/setup/install.py
```

### Utilities & Maintenance

```bash
# Update server database
python scripts/utilities/get_all_servers.py

# Fix imports
bash scripts/utilities/fix_imports.sh
```

## 📋 Script Categories

### 1. **Setup Scripts** (`setup/`)

- Install dependencies
- Configure environment
- Set up MCP servers
- Validate installation

### 2. **Utility Scripts** (`utilities/`)

- Data management
- Maintenance tasks
- Import fixes
- Database updates

### 3. **Runtime Scripts** (root level)

- Application execution
- Test running
- Background processes

## 🎯 Usage Guidelines

1. **Always use `poetry run`** when executing Python scripts
2. **Check README files** in subdirectories for detailed usage
3. **Use setup scripts** for initial installation
4. **Use utility scripts** for maintenance tasks
5. **Use runtime scripts** for daily development

## 🔧 Development Workflow

```bash
# 1. Initial setup
python scripts/setup/setup_all.py

# 2. Run application
python scripts/run.py

# 3. Run tests
python scripts/run_working_tests.py

# 4. Maintenance (as needed)
python scripts/utilities/get_all_servers.py
```
