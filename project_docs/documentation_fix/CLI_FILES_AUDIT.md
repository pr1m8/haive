# CLI Files Audit - User-Facing Interfaces Worth Documenting

**Date**: 2025-07-27
**Purpose**: Evaluate CLI and main files currently ignored for documentation value
**Status**: Found several high-value user-facing interfaces

## 🎯 **HIGH VALUE CLI Files (Should Document)**

### 1. **MCP CLI Tool** ⭐⭐⭐ HIGH PRIORITY

- **File**: `packages/haive-mcp/src/haive/mcp/cli.py`
- **Purpose**: Command-line interface for MCP server selection and configuration
- **User Value**: Very High - Essential for MCP setup
- **Usage Examples**:
  ```bash
  python -m haive.mcp.cli list-servers                    # List all available servers
  python -m haive.mcp.cli filter --prefix "anthropic/"    # Filter by prefix
  python -m haive.mcp.cli recommend "analyze GitHub repo" # Get recommendations
  python -m haive.mcp.cli select                         # Interactive selection
  python -m haive.mcp.cli auto-config "my task"          # Auto-configure for task
  ```
- **Documentation Value**: Essential for users setting up MCP integration
- **Recommendation**: **REMOVE FROM IGNORE LIST** - Document immediately

### 2. **Research Agent CLI** ⭐⭐⭐ HIGH PRIORITY

- **File**: `packages/haive-agents/src/haive/agents/research/open_perplexity/cli.py`
- **Purpose**: CLI tool for running research tasks with open_perplexity agent
- **User Value**: Very High - Research automation interface
- **Features**:
  - Load research questions from text files
  - Configure research parameters
  - Generate research reports
  - Visualize research states
- **Documentation Value**: Critical for users wanting to run research workflows
- **Recommendation**: **REMOVE FROM IGNORE LIST** - Document immediately

## 🚀 **MEDIUM VALUE Application Entry Points (Consider Documenting)**

### 3. **Dataflow Server Main** ⭐⭐ MEDIUM PRIORITY

- **File**: `packages/haive-dataflow/src/haive/dataflow/main.py`
- **Purpose**: FastAPI server entry point for dataflow operations
- **User Value**: Medium - Deployment and server setup
- **Features**:
  - Uvicorn server configuration
  - Rich console logging
  - Environment variable configuration
- **Documentation Value**: Useful for deployment and server setup
- **Recommendation**: **CONSIDER DOCUMENTING** - Deployment guide value

### 4. **Dataflow API Main** ⭐⭐ MEDIUM PRIORITY

- **File**: `packages/haive-dataflow/src/haive/dataflow/api/main.py`
- **Purpose**: API endpoint definitions for dataflow services
- **User Value**: Medium - API integration
- **Documentation Value**: Useful for API consumers
- **Recommendation**: **CONSIDER DOCUMENTING** - API reference value

### 5. **Registry Main Files** ⭐ LOW-MEDIUM PRIORITY

- **Files**:
  - `packages/haive-dataflow/src/haive/dataflow/registry/main.py`
  - `packages/haive-dataflow/src/haive/dataflow/registries/main.py`
  - `packages/haive-dataflow/src/haive/dataflow/registry/registries/main.py`
- **Purpose**: Registry service entry points
- **User Value**: Lower - Internal service management
- **Documentation Value**: Moderate for advanced users
- **Recommendation**: **LOWER PRIORITY** - Document if comprehensive coverage desired

## 📊 **Current Impact of Ignoring These Files**

### User Experience Impact

- **MCP Setup**: Users have no documentation for MCP CLI tool setup
- **Research Workflows**: No guidance for automated research tasks
- **Deployment**: Limited documentation for server deployment
- **API Integration**: Missing API endpoint documentation

### Documentation Gaps

- **CLI Usage**: No command-line interface documentation
- **Server Setup**: Missing deployment guides
- **Integration Examples**: No practical usage examples
- **Troubleshooting**: No CLI-specific troubleshooting guides

## ✅ **Recommended Actions**

### Immediate (High Priority)

1. **Remove MCP CLI from ignore list**:

   ```python
   # In conf.py, remove or comment out:
   # "**/cli.py",
   # Or be more specific:
   "**/debug/cli.py",  # Keep ignoring debug CLIs
   "**/test*/cli.py",  # Keep ignoring test CLIs
   ```

2. **Remove Research CLI from ignore list**:
   - Same approach - be more specific about which CLIs to ignore

3. **Test documentation generation** for these specific files

### Short Term (Medium Priority)

1. **Evaluate main.py files individually**:

   ```python
   # Instead of blanket ignore:
   # "**/main.py",
   # Be specific:
   "**/test*/main.py",
   "**/debug/main.py",
   "**/example*/main.py",
   ```

2. **Document high-value entry points** for deployment guides

### Long Term (Lower Priority)

1. **Create CLI documentation section** in main docs
2. **Add deployment guides** using main.py files
3. **Integrate CLI examples** into user guides

## 🔧 **Implementation Plan**

### Phase 1: Update Ignore Patterns

```python
# Current (TOO BROAD):
"**/cli.py",
"**/main.py",

# Proposed (MORE SPECIFIC):
"**/test*/cli.py",
"**/debug*/cli.py",
"**/example*/cli.py",
"**/test*/main.py",
"**/debug*/main.py",
"**/example*/main.py",
# Remove blanket ignores, allow valuable CLIs
```

### Phase 2: Test Selective Documentation

1. Update ignore patterns in conf.py
2. Test documentation generation
3. Verify HTML output quality
4. Check for any build errors

### Phase 3: Enhance Documentation

1. Add CLI usage examples to generated docs
2. Create deployment guides using main.py files
3. Add cross-references between CLI and API docs

## 🎯 **Expected Benefits**

### For Users

- **Clear CLI guidance** for MCP setup and research workflows
- **Deployment documentation** for dataflow services
- **Complete API reference** including entry points
- **Practical examples** of command-line usage

### For Documentation Quality

- **Increased completeness** - more comprehensive coverage
- **Better user experience** - practical usage information
- **Professional appearance** - complete interface documentation
- **Reduced support burden** - self-service CLI documentation

## 📋 **Files to Update**

1. **docs/source/conf.py** - Update ignore patterns to be more specific
2. **Test documentation build** - Verify quality of CLI documentation
3. **Create CLI examples** - Add practical usage examples
4. **Update user guides** - Reference CLI documentation

## 🚨 **Risks and Mitigation**

### Potential Risks

- **Build time increase** - More files to process
- **Documentation noise** - Internal implementation details exposed
- **Maintenance burden** - More documentation to maintain

### Mitigation Strategies

- **Selective inclusion** - Only include high-value CLIs
- **Good docstrings** - Ensure CLI files have quality documentation
- **Usage examples** - Focus on practical user value
- **Regular review** - Periodically evaluate CLI documentation value

## 🎯 **Priority Recommendation**

**Start with MCP CLI and Research CLI** - these provide immediate user value and are well-documented with clear usage examples. Test the impact on build time and documentation quality before expanding to other files.

**Next Step**: Update conf.py ignore patterns to be more specific, allowing high-value CLI documentation while still filtering out debug/test/example CLIs.
