# Sphinx Documentation Issues and Solutions

**Date**: 2025-08-06
**Status**: Active Investigation

## 🎯 Overview

This document consolidates findings on Sphinx documentation issues including:
1. Duplicate object description warnings (Pydantic models)
2. MCP package documentation structure
3. autodoc-pydantic integration
4. Reference target warnings

## 🔍 Issue 1: Duplicate Object Description Warnings

### Problem
When building documentation, getting warnings like:
```
WARNING: duplicate object description of haive.agents.planning.enhanced_plan_execute_v5.planner.models.TaskPlan.milestones
```

### Root Cause
AutoAPI is documenting Pydantic model fields multiple times:
- Once as class attributes
- Once as instance attributes
- Possibly once through autodoc-pydantic if installed

### Solution Options

#### Option 1: Use autodoc-pydantic Extension
```python
# Add to conf.py extensions
extensions = [
    "autoapi.extension",  # Keep first
    # ... other extensions ...
    "sphinxcontrib.autodoc_pydantic",  # Add this
]

# Configure autodoc-pydantic
autodoc_pydantic_model_show_json = False
autodoc_pydantic_model_show_config_summary = True
autodoc_pydantic_model_show_validator_members = False
autodoc_pydantic_field_show_constraints = True
autodoc_pydantic_field_doc_policy = "description"  # Only show field descriptions
```

#### Option 2: Update autoapi_skip_member Function
```python
def autoapi_skip_member(app, what, name, obj, skip, options):
    """Skip duplicate Pydantic field documentation."""
    
    # Skip duplicate Pydantic fields
    if what == "attribute" and "." in name:
        parts = name.split(".")
        if len(parts) >= 2:
            field_name = parts[-1]
            class_name = parts[-2]
            
            # Known Pydantic fields that get duplicated
            pydantic_fields = [
                "model_config", "model_fields", "model_computed_fields",
                "milestones", "risk_factors", "available_tools", 
                "time_constraints", "constraints", "dependencies"
            ]
            
            if field_name in pydantic_fields:
                # Skip if it's being documented as an attribute
                return True
    
    return skip
```

## 📚 Issue 2: MCP Package Documentation Not Rendering

### Problem
The `packages/haive-mcp/data/documentation/servers/` folder contains hundreds of .rst files but they're not included in the built documentation.

### Root Cause
AutoAPI only processes Python source files (.py), not static documentation files (.rst/.md) in the data directory.

### Solution

#### Add Explicit TOC Entries
Create `docs/source/haive-mcp.rst`:
```rst
Haive MCP Documentation
=======================

.. toctree::
   :maxdepth: 2
   :caption: MCP Server Documentation
   :glob:

   ../../packages/haive-mcp/data/documentation/servers/academic/*
   ../../packages/haive-mcp/data/documentation/servers/ai/*
   ../../packages/haive-mcp/data/documentation/servers/analytics/*
   ../../packages/haive-mcp/data/documentation/servers/automation/*
   ../../packages/haive-mcp/data/documentation/servers/cloud/*
   ../../packages/haive-mcp/data/documentation/servers/code/*
   ../../packages/haive-mcp/data/documentation/servers/communication/*
   ../../packages/haive-mcp/data/documentation/servers/data/*
   ../../packages/haive-mcp/data/documentation/servers/design/*
   ../../packages/haive-mcp/data/documentation/servers/developer-tools/*
   ../../packages/haive-mcp/data/documentation/servers/file/*
   ../../packages/haive-mcp/data/documentation/servers/finance/*
   ../../packages/haive-mcp/data/documentation/servers/game/*
   ../../packages/haive-mcp/data/documentation/servers/iot/*
   ../../packages/haive-mcp/data/documentation/servers/knowledge/*
   ../../packages/haive-mcp/data/documentation/servers/media/*
   ../../packages/haive-mcp/data/documentation/servers/monitoring/*
   ../../packages/haive-mcp/data/documentation/servers/productivity/*
   ../../packages/haive-mcp/data/documentation/servers/security/*
   ../../packages/haive-mcp/data/documentation/servers/system/*
   ../../packages/haive-mcp/data/documentation/servers/web/*
```

#### Alternative: Copy Files During Build
Add to `conf.py` setup():
```python
def setup(app):
    """Setup function with MCP docs copying."""
    
    def copy_mcp_docs(app, env):
        """Copy MCP documentation files to build."""
        import shutil
        from pathlib import Path
        
        mcp_docs = Path(__file__).parent.parent.parent / "packages/haive-mcp/data/documentation"
        target_dir = Path(app.srcdir) / "mcp_docs"
        
        if mcp_docs.exists() and not target_dir.exists():
            shutil.copytree(mcp_docs, target_dir)
            logger.info(f"Copied MCP docs to {target_dir}")
    
    app.connect('env-before-read-docs', copy_mcp_docs)
```

## 🔧 Issue 3: Reference Target Warnings

### Problem
Getting warnings like:
```
WARNING: py:class reference target not found: langchain_core.runnables.RunnableConfig
WARNING: py:class reference target not found: haive.core.engine.base.Engine
```

### Solution

#### Update nitpick_ignore in conf.py
```python
nitpick_ignore.extend([
    # LangChain types
    ("py:class", "langchain_core.runnables.RunnableConfig"),
    ("py:class", "langchain_core.runnables.Runnable"),
    ("py:class", "langchain_core.callbacks.CallbackManagerForLLMRun"),
    
    # Internal references that might not be available
    ("py:class", "haive.core.engine.base.Engine"),
    ("py:obj", "haive.core.common.mixins.tool_route_mixin.ToolRouteMixin"),
    ("py:class", "haive.agents.wiki_writer.utils.update_editor"),
])
```

#### Update intersphinx_mapping
```python
intersphinx_mapping = {
    # ... existing mappings ...
    "langchain_core": ("https://api.python.langchain.com/en/latest/", None),
    "langchain": ("https://python.langchain.com/docs/", None),
}
```

## 🎨 Recommended Configuration

### Complete autodoc-pydantic Setup

1. **Install**:
   ```bash
   poetry add --group docs autodoc-pydantic
   ```

2. **Configure in conf.py**:
   ```python
   extensions = [
       "autoapi.extension",  # First
       # ... other extensions ...
       "sphinxcontrib.autodoc_pydantic",
   ]
   
   # Pydantic-specific configuration
   autodoc_pydantic_model_show_json = False
   autodoc_pydantic_model_show_config_summary = True
   autodoc_pydantic_model_show_validator_members = True
   autodoc_pydantic_field_show_constraints = True
   autodoc_pydantic_field_doc_policy = "description"
   autodoc_pydantic_settings_show_json = False
   ```

3. **Enhanced autoapi_skip_member**:
   ```python
   def autoapi_skip_member(app, what, name, obj, skip, options):
       """Skip problematic members and duplicates."""
       
       # Skip duplicate Pydantic model internals
       if what == "attribute" and name.endswith(("__fields__", "__config__", "model_fields", "model_config")):
           return True
           
       # Skip if autodoc-pydantic is handling it
       if what == "attribute" and hasattr(obj, "__pydantic_model__"):
           return True
           
       return skip
   ```

## 📊 Multi-Level Documentation Structure

### Current Structure
```
docs/source/conf.py          # Main documentation config
packages/*/docs/             # Package-specific docs (not used)
packages/haive-mcp/data/     # Static documentation files
```

### Recommended Approach

1. **Single Source of Truth**: Use only `docs/source/conf.py`
2. **Include Package Docs**: Create explicit includes for static docs
3. **Use AutoAPI for Code**: Let AutoAPI handle Python API docs
4. **Manual TOCs for Static**: Create .rst files to include static documentation

## 🚀 Implementation Steps

1. **Install autodoc-pydantic**:
   ```bash
   poetry add --group docs autodoc-pydantic
   ```

2. **Update conf.py** with autodoc-pydantic extension and configuration

3. **Create MCP documentation index** at `docs/source/mcp_docs.rst`

4. **Update autoapi_skip_member** to handle duplicates

5. **Extend nitpick_ignore** for missing references

6. **Test build**:
   ```bash
   poetry run sphinx-build -b html docs/source docs/build/html -W --keep-going
   ```

## 📝 Notes

- autodoc-pydantic provides better Pydantic model documentation than standard autodoc
- AutoAPI and autodoc-pydantic can work together with proper configuration
- Static .rst files need explicit inclusion in the documentation structure
- Consider using `sphinx-pydantic` as an alternative for JSON schema documentation