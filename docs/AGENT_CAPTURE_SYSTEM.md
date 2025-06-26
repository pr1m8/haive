# Agent Capture & Documentation System

The Haive Agent Capture & Documentation System provides comprehensive tools for capturing agent execution flows, visualizing agent graphs, and generating interactive documentation with step-by-step replay capabilities.

## Features

- 🎯 **Live Agent Execution Capture** - Record real agent runs with full step-by-step traces
- 📊 **Graph Visualization** - Automatic generation of agent workflow diagrams  
- 🔍 **Interactive Replay** - Browse through execution steps with detailed content
- 📚 **Auto-Documentation** - Generate comprehensive documentation pages automatically
- 🎨 **Unified Interface** - Works with both `haive.agents.base.Agent` and `haive.core.engine.agent.Agent`

## Quick Start

### Basic Agent Capture

```python
from haive.core.utils.agent_capture import capture_agent_run

# Capture any agent execution
run = capture_agent_run(
    agent=my_agent,
    input_data={"question": "What is renewable energy?"},
    agent_name="MyAgent",
    capture_dir="docs/captures"
)

print(f"Captured {len(run.steps)} execution steps")
print(f"Duration: {run.duration:.2f}s")
print(f"Success: {run.is_successful}")
```

### Generate Documentation Page

```python
from haive.core.utils.doc_agent_showcase import create_agent_showcase_page

# Create a complete documentation page
page_path = create_agent_showcase_page(
    agent=my_agent,
    example_input={"task": "analyze climate data"},
    agent_name="ClimateAnalyzer",
    description="Agent specialized in climate data analysis",
    example_description="Analyzing global temperature trends"
)

print(f"Generated documentation: {page_path}")
```

### Use in Sphinx Documentation

Add the captured run to your RST documentation:

```rst
Climate Analysis Agent
======================

This agent specializes in climate data analysis and visualization.

.. agent-run-capture:: ../../captures/ClimateAnalyzer_abc123_20250101.json
   :show-graph:
   :show-logs:
   :paginated:
   :page-size: 10
```

## Architecture

### Agent Types Supported

The system works with both major Haive agent types:

1. **`haive.agents.base.Agent`** - Base agents with automatic graph building
2. **`haive.core.engine.agent.Agent`** - Core engine agents with rich features

### Capture Process

1. **Start Capture** - Initialize capture session with agent metadata
2. **Execute Agent** - Run agent with streaming or simple execution
3. **Record Steps** - Capture each execution step with content and timing
4. **Generate Graph** - Create visual representation of agent workflow
5. **Save Results** - Store complete capture data as JSON

### Documentation Generation

The system generates rich documentation including:

- **Execution Overview** - Metadata, duration, success status
- **Graph Visualization** - Agent workflow diagram
- **Step-by-Step Trace** - Detailed execution logs
- **Performance Metrics** - Step distribution and timing
- **Usage Examples** - Code snippets and configuration

## Components

### Core Modules

- **`haive.core.utils.agent_capture`** - Core capture functionality
- **`haive.core.utils.doc_agent_showcase`** - Documentation generation
- **`docs/source/_extensions/haive_sphinx_ext.py`** - Sphinx integration

### Data Models

- **`AgentRun`** - Complete execution capture
- **`ExecutionStep`** - Individual step in agent flow
- **`AgentCapture`** - Capture session manager

## Examples

### Demo Scripts

Run the included demo scripts to see the system in action:

```bash
# Demo with mock agents
python scripts/demo_agent_capture.py

# Demo with real Haive agents
python scripts/real_agent_capture_demo.py
```

### Batch Documentation

Document multiple agents at once:

```python
from haive.core.utils.doc_agent_showcase import batch_document_agents

agents_and_examples = [
    (simple_agent, {"query": "explain quantum computing"}),
    (react_agent, {"task": "research solar panels"}),
    (rag_agent, {"question": "climate change solutions"})
]

generated_files = batch_document_agents(agents_and_examples)
```

## Configuration

### Capture Settings

```python
capture = AgentCapture(capture_dir="docs/captures")

# Capture with custom metadata
run = capture.capture_streaming_execution(
    agent=agent,
    input_data=input_data,
    metadata={
        "experiment": "performance_test",
        "version": "1.2.0",
        "environment": "production"
    }
)
```

### Visualization Options

```python
# Universal graph visualization
graph_path = visualize_agent_graph(
    agent=agent,
    output_path="graphs/my_agent.png"
)
```

### Sphinx Directive Options

```rst
.. agent-run-capture:: path/to/capture.json
   :paginated:          # Enable pagination for long executions
   :page-size: 20       # Steps per page (default: 10)
   :show-graph:         # Display agent graph
   :show-logs:          # Show execution logs
   :show-metrics:       # Display performance metrics
```

## Integration

### With Nox Documentation

The system integrates seamlessly with the existing Nox documentation workflow:

```bash
# Build documentation with captured agent runs
poetry run nox -s docs

# Serve with live reload
poetry run nox -s docs-live

# Clean and rebuild
poetry run nox -s docs -- --clean
```

### With CI/CD

Capture agent runs in your CI pipeline:

```yaml
- name: Capture Agent Runs
  run: |
    python scripts/capture_agents_for_docs.py
    poetry run nox -s docs

- name: Deploy Documentation
  uses: peaceiris/actions-gh-pages@v3
  with:
    github_token: ${{ secrets.GITHUB_TOKEN }}
    publish_dir: ./docs/build/html
```

## Troubleshooting

### Common Issues

1. **Agent Import Errors**
   - Ensure all Haive packages are installed
   - Check Python path configuration

2. **Graph Visualization Failures**
   - Verify agent has `visualize_graph` method
   - Check output directory permissions

3. **Capture File Not Found**
   - Verify capture file paths in RST directives
   - Ensure files are relative to source directory

### Debug Mode

Enable debug logging to troubleshoot issues:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Run capture with debug info
run = capture_agent_run(agent, input_data, debug=True)
```

## Extending the System

### Custom Step Processing

Extend the capture system for custom step types:

```python
class CustomAgentCapture(AgentCapture):
    def _process_stream_update(self, update):
        # Custom processing logic
        if "custom_event" in update:
            self.current_run.add_step(
                step_type="custom",
                content=update["custom_event"]
            )
        super()._process_stream_update(update)
```

### Custom Documentation Templates

Create custom RST templates for specific agent types:

```python
class CustomDocumentationGenerator(AgentDocumentationGenerator):
    def _generate_rst_content(self, doc_data):
        # Custom RST generation
        return custom_template.format(**doc_data)
```

## Best Practices

1. **Naming Conventions** - Use descriptive agent names and capture directories
2. **Input Examples** - Provide realistic, representative example inputs
3. **Documentation** - Include clear descriptions and context
4. **Performance** - Consider pagination for agents with many steps
5. **Version Control** - Track capture files with your documentation

## Future Enhancements

- Real-time streaming visualization
- Agent performance comparison tools
- Interactive execution replay in browser
- Integration with agent testing frameworks
- Automated documentation generation in CI/CD

---

For more examples and advanced usage, see the demo scripts in the `scripts/` directory.