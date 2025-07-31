# Quick Reference - Haive Documentation Patterns

**Updated**: 2025-07-18
**Purpose**: Fast access to common documentation patterns and solutions

## 🎨 **Sphinx Jinja2 Template Processing**

### **Quick Setup**

```bash
# Install extension
poetry add sphinx-jinja2 --group=docs

# Add to conf.py extensions
"sphinx_jinja2",
```

### **Configuration Pattern**

```python
# conf.py
jinja2_contexts = {
    'agent_demo': {
        'get_agent_context': get_agent_context,
        'available_agents': AVAILABLE_AGENTS,
    }
}
jinja2_debug = False  # IMPORTANT: Disable for production
```

### **Template Usage**

```rst
.. jinja:: agent_demo
   :ctx: {"agent_id": "simple"}

   {% set agent_data = get_agent_context(agent_id) %}
   {{ agent_data.agent_name }} Demo
   {{ '=' * (agent_data.agent_name|length + 5) }}
```

### **Common Issues**

- **Duplicate Output**: Set `jinja2_debug = False`
- **Missing Context**: Check `jinja2_contexts` configuration
- **Template Errors**: Use `jinja2_debug = True` for debugging

## 📝 **Documentation Build Commands**

### **Standard Build**

```bash
# Full build
poetry run sphinx-build -b html docs/source docs/build/html

# Quick rebuild
poetry run sphinx-build -b html docs/source docs/build/html -q

# Clean build
poetry run sphinx-build -b html docs/source docs/build/html -E
```

### **Testing Specific Files**

```bash
# Test without AutoAPI (faster)
# Temporarily disable autoapi.extension in conf.py
poetry run sphinx-build -b html docs/source docs/build/html -q -E
```

## 🔧 **AutoAPI Configuration**

### **Enable/Disable**

```python
# Enable for full API docs
"autoapi.extension",

# Disable for faster testing
# "autoapi.extension",  # Temporarily disabled
```

### **Hooks Management**

```python
# When autoapi is enabled
app.connect("autoapi-skip-member", autoapi_skip_member)

# When autoapi is disabled
# app.connect("autoapi-skip-member", autoapi_skip_member)
```

## 🎯 **Agent Demo Files**

### **Files to Update** (11 total)

```
docs/source/agents/demos/
├── simple-demo.rst              ✅ Test template working
├── react-demo.rst               ⏳ Needs template conversion
├── baserag-demo.rst             ⏳ Needs template conversion
├── adaptiverag-demo.rst         ⏳ Needs template conversion
├── planandexecute-demo.rst      ⏳ Needs template conversion
├── debate-demo.rst              ⏳ Needs template conversion
├── personresearch-demo.rst      ⏳ Needs template conversion
├── summarizer-demo.rst          ⏳ Needs template conversion
├── reflection-demo.rst          ⏳ Needs template conversion
├── structuredoutput-demo.rst    ⏳ Needs template conversion
└── reactwithmemory-demo.rst     ⏳ Needs template conversion
```

### **Template Conversion Process**

1. **Identify agent type** (simple, react, rag, etc.)
2. **Add agent data** to `agent_demo_data.py`
3. **Convert RST file** to use `.. jinja::` directive
4. **Test build** with single file
5. **Verify rendering** in HTML output

## 📊 **Common File Patterns**

### **Agent Data Structure**

```python
"agent_id": {
    "agent_name": "AgentName",
    "agent_description": "Description text",
    "agent_icon": "🤖",
    "agent_type": "category",
    "agent_features": ["Feature1", "Feature2"],
    "agent_module_import": "haive.agents.module",
    "agent_class": "AgentClass",
    "agent_config": "config_parameters",
    "example_input": "Example input text",
    "agent_architecture_details": "Architecture description",
    "graph_data": {...},  # Visualization data
    "state_history": [...],  # State tracking
    "execution_trace": [...]  # Execution steps
}
```

### **JavaScript Dependencies**

```html
<!-- Missing visualizer scripts -->
<script>
  // AgentGraphVisualizer - needs implementation
  // StateHistoryVisualizer - needs implementation
  // ExecutionTraceVisualizer - needs implementation
</script>
```

## 🔍 **Debugging Tips**

### **Template Issues**

```bash
# Check if template is being processed
grep -A5 -B5 "agent_name" docs/build/html/agents/demos/file.html

# Check for raw template syntax
grep "{{" docs/build/html/agents/demos/file.html
```

### **Agent Data Issues**

```bash
# Test agent data loading
cd docs/source
poetry run python -c "from agent_demo_data import get_agent_context; print(get_agent_context('simple'))"
```

### **Build Issues**

```bash
# Check specific warnings
poetry run sphinx-build -b html docs/source docs/build/html -W --keep-going
```

## 🚀 **Performance Tips**

### **Fast Development Builds**

1. **Disable AutoAPI**: Comment out `autoapi.extension`
2. **Use incremental builds**: Skip `-E` flag
3. **Build specific pages**: Focus on single files
4. **Cache agent data**: Load once per build

### **Production Builds**

1. **Enable all extensions**: Include AutoAPI
2. **Clean build**: Use `-E` flag
3. **Check warnings**: Use `-W` flag
4. **Validate output**: Check HTML rendering

## 📁 **Key Files Reference**

### **Configuration**

- `docs/source/conf.py` - Main Sphinx configuration
- `docs/source/agent_demo_data.py` - Agent data for templates
- `pyproject.toml` - Dependencies

### **Templates**

- `docs/source/_templates/agent_demo_template.rst` - Template base
- `docs/source/agents/demos/simple-demo-test.rst` - Working example

### **Styling**

- `docs/source/_static/api-showcase.css` - API styling
- `docs/source/_static/showcase.css` - Agent demo styling

---

**Reference**: [MEM-009-DOCS-JINJA2-001] - Sphinx Jinja2 Template Processing
**Status**: ✅ **WORKING SOLUTION** - Template processing implemented and tested
