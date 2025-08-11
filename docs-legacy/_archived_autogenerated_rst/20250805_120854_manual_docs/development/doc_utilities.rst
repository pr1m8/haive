🛠️ Documentation Utilities



   <div class="feature-intro">
   <h1 class="gradient-text">Documentation Generation & Analysis</h1>
   <p>Comprehensive toolkit for analyzing, visualizing, and documenting all Haive agents across the ecosystem.</p>
   </div>

Overview



The Haive Documentation Utilities provide a powerful, unified system for:

- **🔍 Agent Analysis** - Discover and analyze all agent types automatically
- **🎨 Visualization** - Generate workflow diagrams and comparison charts
- **📚 Documentation** - Create comprehensive docs with cross-references
- **🧪 Example Validation** - Test and validate all example files

All tools work seamlessly with both **nox build system** and **command-line interface**.

Quick Start



.. note::


   Grid layout removed due to sphinx_design incompatibility.


   .. grid-item::



      **Using Nox (Recommended)**

.. code-block:: bash

         :class:``copy-button`
``

         # Complete workflow
         nox -s doc_utils_full

         # Individual components
         nox -s doc_utils_analyze     # Agent analysis
         nox -s doc_utils_visualize   # Visualizations
         nox -s doc_utils_generate    # Documentation

         .. grid-item::



         **Direct CLI Usage**

.. code-block:: bash

         :class`:``copy-button`
``

         # Agent analysis
         python doc_utils_runner.py analyze --report

         # Generate visualizations
         python doc_utils_runner.py visualize --compare

         # Run examples
         python doc_utils_runner.py run --discover

         Core Components



         .. grid:: 1 2 2 2


         .. grid-item-card:: 🔍 AgentAnalyzer

         :shadow: md

         **Comprehensive agent discovery and analysis**

         - Auto-detects 100+ agent types across packages
         - Identifies architectures (haive.agents, haive.core, haive.games)
         - Analyzes capabilities (visualization, tools, streaming)
         - Maps inheritance patterns and relationships

         .. grid-item-card:: 🧪 UniversalExampleRunner

         :shadow: md

         **Execute any example with monitoring**

         - Universal compatibility across all agent types
         - Streaming output with intelligent chunking
         - Timeout protection and error recovery
         - Automatic visualization generation

         .. grid-item-card:: 🎨 VisualizationManager

         :shadow: md

         **Universal agent visualization**

         - Multiple formats: PNG, SVG, HTML, Mermaid
         - Native visualization when available
         - Synthetic diagrams for any agent type
         - Comparison views across multiple agents

         .. grid-item-card:: 📚 DocumentationGenerator

         :shadow: md

         **Automated documentation creation**

         - Individual agent documentation
         - Project-wide docs with cross-references
         - Multiple formats: Markdown, RST, HTML
         - API documentation extraction

         Nox Integration



         The documentation utilities are fully integrated into the **nox build system** for seamless workflow integration:

         .. tabs::


         .. tab:: Quick Commands

.. code-block:: bash

         # Complete documentation utilities workflow
         nox -s doc_utils_full

         # Individual components
         nox -s doc_utils_analyze      # Agent analysis report
         nox -s doc_utils_examples     # Example validation
         nox -s doc_utils_visualize    # Generate visualizations
         nox -s doc_utils_generate     # Create documentation

         .. tab:: Output Structure

.. code-block:: text

         docs/build/
         ├── agent_analysis/
         │   └── agent_analysis_report.md
         ├── examples/
         │   └── example_validation_report.md
         ├── visualizations/
         │   ├── agent_comparison.html
         │   ├── simpleagent_workflow.png
         │   └── reactagent_workflow.png
         ├── generated_docs/
         │   ├── index.md
         │   ├── agent_comparison.md
         │   └── [agent_name]/
         └── doc_utils_summary.md

         .. tab:: Configuration

         Each nox session accepts environment variables for customization:

.. code-block:: bash

         # Customize timeouts and output
         TIMEOUT_SECONDS=120 nox -s doc_utils_examples
         MAX_OUTPUT_SIZE=50000000 nox -s doc_utils_examples

         Command-Line Interface



         For more granular control, use the CLI directly:

         .. tabs::


         .. tab:: Analysis Commands

.. code-block:: bash

         # Analyze all agents
         python doc_utils_runner.py analyze --report --output analysis.md

         # Analyze specific agent
         python doc_utils_runner.py analyze --agent-name SimpleAgent

         # Generate inheritance report
         python doc_utils_runner.py analyze --report --output inheritance.md

         .. tab:: Example Commands

.. code-block:: bash

         # Discover all examples
         python doc_utils_runner.py run --discover

         # Run specific example with monitoring
         python doc_utils_runner.py run --example-path path/to/example.py --visualize

         # Validate all examples (quick)
         python doc_utils_runner.py run --run-all --timeout 60 --max-concurrent 3

         .. tab:: Visualization Commands

.. code-block:: bash

         # Create agent comparison
         python doc_utils_runner.py visualize --compare --format html --theme dark

         # Visualize specific agent
         python doc_utils_runner.py visualize --agent-name ReactAgent --format png

         # Generate all visualizations
         python doc_utils_runner.py visualize --output ./visualizations/

         .. tab:: Documentation Commands

.. code-block:: bash

         # Generate project documentation
         python doc_utils_runner.py docs --format markdown --api-docs

         # Specific agent with full features
         python doc_utils_runner.py docs --agent-name SimpleAgent --style comprehensive

         # Minimal documentation
         python doc_utils_runner.py docs --style minimal --no-visualizations

         Programmatic API



         Use the utilities programmatically in your scripts:

         .. tabs::


         .. tab:: Agent Analysis

.. code-block:: python

    # Code example here

         from scripts.doc_utils import AgentAnalyzer

         # Discover all agents
         analyzer = AgentAnalyzer()
         agents = analyzer.discover_all_agents()

         print(f"Found {len(agents)} agents")

         # Get specific agent
         simple_agent = analyzer.get_agent_by_name("SimpleAgent")
         print(f"Architecture: {simple_agent.architecture}")
         print(f"Has visualization: {simple_agent.has_visualization}")

         # Generate analysis report
         report = analyzer.generate_analysis_report()
         with open("analysis_report.md", "w") as f:
             f.write(report)

         .. tab:: Example Execution

.. code-block:: python

    # Code example here

         import asyncio
         from scripts.doc_utils import UniversalExampleRunner, ExecutionConfig

         async def run_examples():
             runner = UniversalExampleRunner()

             # Discover examples
             examples = await runner.discover_all_examples()
             print(f"Found {len(examples)} examples")

             # Run specific example
             config = ExecutionConfig(
                 max_output_size=10_000_000,
                 stream_output=True,
                 enable_visualization=True
             )

             result = await runner.run_example(examples[0], config)
             print(f"Success: {result.success}")
             print(f"Time: {result.execution_time:.2f}s")

         asyncio.run(run_examples())

         .. tab:: Visualization Generation

.. code-block:: python

    # Code example here

         import asyncio
         from scripts.doc_utils import VisualizationManager, VisualizationConfig
         from pathlib import Path

         async def create_visualizations():
             viz_manager = VisualizationManager()

             # Get agent info
             analyzer = AgentAnalyzer()
             agents = analyzer.discover_all_agents()

             # Create visualization
             config = VisualizationConfig(
                 output_format="html",
                 theme="dark",
                 include_metadata=True
             )

             for agent in agents[:5]:  # First 5 agents
                 viz_path = Path(f"{agent.name.lower()}_viz.html")
                 result = await viz_manager.visualize_agent(agent, viz_path, config)

                 if result.success:
                     print(f"✅ {agent.name}: {result.output_path}")

         asyncio.run(create_visualizations())

         .. tab:: Documentation Generation

.. code-block:: python

    # Code example here

         import asyncio
         from scripts.doc_utils import DocumentationGenerator, DocumentationConfig
         from pathlib import Path

         async def generate_docs():
             doc_generator = DocumentationGenerator()

             # Configuration
             config = DocumentationConfig(
                 include_examples=True,
                 include_visualizations=True,
                 include_api_docs=True,
                 output_format="markdown",
                 template_style="comprehensive"
             )

             # Generate project-wide documentation
             output_dir = Path("./generated_documentation")
             result = await doc_generator.generate_project_documentation(
                 output_dir, config
             )

             if result.success:
                 print(f"Documentation generated:")
                 print(f"  Index: {result.index_file}")
                 print(f"  Files: {len(result.output_files)}")

         asyncio.run(generate_docs())

         Configuration Options




         .. tabs::


         .. tab:: ExecutionConfig

.. code-block:: python

    # Code example here

         from scripts.doc_utils import ExecutionConfig

         config = ExecutionConfig(
             max_output_size=10_000_000,    # 10MB max output
             chunk_size=1024,               # 1KB streaming chunks
             enable_visualization=True,      # Generate visualizations
             timeout_seconds=300,           # 5 minute timeout
             stream_output=True,            # Enable streaming
             save_full_output=True          # Save large outputs to file
         )

         .. tab:: VisualizationConfig

.. code-block:: python

    # Code example here

         from scripts.doc_utils import VisualizationConfig

         config = VisualizationConfig(
             output_format="html",          # png, svg, html, mermaid
             theme="dark",                  # default, dark, minimal
             include_metadata=True,         # Include agent metadata
             width=1200,                    # Image width
             height=800,                    # Image height
             dpi=300                        # Image DPI for PNG/SVG
         )

         .. tab:: DocumentationConfig

.. code-block:: python

    # Code example here

         from scripts.doc_utils import DocumentationConfig

         config = DocumentationConfig(
             include_examples=True,         # Include example files
             include_visualizations=True,   # Generate diagrams
             include_code_snippets=True,    # Add code examples
             include_api_docs=True,         # Extract API docs
             output_format="markdown",      # markdown, rst, html
             template_style="comprehensive", # minimal, standard, comprehensive
             generate_index=True,           # Create index files
             cross_reference=True           # Add cross-references
         )

         Supported Agent Types




         The system automatically handles all Haive agent architectures:

         .. grid:: 1 1 3 3


         .. grid-item-card:: haive.agents

         :shadow: sm

         **Mixin-based Architecture**

         - SimpleAgent, ReactAgent, MultiAgent
         - RAG agents, Memory agents
         - Planning agents, Document processing
         - Conversation agents

         .. grid-item-card:: haive.core.engine

         :shadow: sm

         **Protocol-based Architecture**

         - Registry-based agents
         - Configurable execution patterns
         - Engine-driven workflows

         .. grid-item-card:: haive.games

         :shadow: sm

         **Game-specific Agents**

         - Chess, Go, Poker agents
         - Board game strategies
         - Multi-player coordination
         - Tournament systems

         Output Examples



         .. tabs::


         .. tab:: Analysis Report

         The agent analysis generates comprehensive reports:

.. code-block:: markdown

         # Agent Analysis Report

         **Total Agents Found**: 127

         ## Architecture Distribution
         - haive.agents: 89 agents
         - haive.games: 32 agents
         - haive.core.engine: 6 agents

         ## Visualization Support
         - With visualization: 94
         - Without visualization: 33

         ## Execution Patterns
         - async: 78 agents
         - sync: 31 agents
         - both: 18 agents

         .. tab:: Visualization Output

         Multiple visualization formats are supported:

         <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin: 1rem 0;">

         <div>
         <h4>🖼️ Workflow Diagrams</h4>
         <ul>
         <li>PNG - High quality raster images</li>
         <li>SVG - Scalable vector graphics</li>
         <li>HTML - Interactive visualizations</li>
         <li>Mermaid - Diagram as code</li>
         </ul>
         </div>

         <div>
         <h4>📊 Comparison Views</h4>
         <ul>
         <li>Side-by-side agent comparison</li>
         <li>Capability matrix tables</li>
         <li>Architecture distribution charts</li>
         <li>Performance metrics</li>
         </ul>
         </div>

         </div>

         .. tab:: Documentation Structure

         Generated documentation follows a consistent structure:

.. code-block:: text

         generated_docs/
         ├── index.md                    # Project overview
         ├── agent_comparison.md         # Comparison table
         ├── architecture_overview.md    # Architecture guide
         └── [agent_name]/
             ├── [agent_name].md         # Main documentation
             ├── [agent_name]_examples.md # Example documentation
             ├── [agent_name]_api.md     # API reference
             └── [agent_name]_workflow.png # Visualization

         Performance & Scalability



         The documentation utilities are designed for performance:

         .. grid:: 1 2 2 2


         .. grid-item::



         <div class="metric-card">
         <span class="value">100+</span>
         <span class="label">Agents Analyzed</span>
         </div>

         .. grid-item::


         <div class="metric-card">
         <span class="value">&lt;30s</span>
         <span class="label">Full Analysis</span>
         </div>

         .. grid-item::


         <div class="metric-card">
         <span class="value">50+</span>
         <span class="label">Examples/Min</span>
         </div>

         .. grid-item::


         <div class="metric-card">
         <span class="value">10MB+</span>
         <span class="label">Output Handling</span>
         </div>

         **Key Performance Features:**

         - **Concurrent Execution** - Multiple examples run in parallel
         - **Streaming Output** - Prevents memory issues with large responses
         - **Intelligent Caching** - Repeated operations use cached results
         - **Timeout Protection** - Prevents hanging on problematic examples
         - **Graceful Degradation** - Works when optional dependencies are missing

         Troubleshooting



         .. dropdown:: Common Issues and Solutions

         :animate: fade-in-slide-down

         **Import Errors**

         Ensure you're running from the project root:


.. code-block:: bash

      cd /path/to/haive/backend/haive
      python doc_utils_runner.py analyze

      **Missing Dependencies**

      Some visualizations require optional packages:


.. code-block:: bash

      pip install graphviz matplotlib  # For advanced visualizations

      **Large Output Handling**

      The system automatically saves large outputs to files:


.. code-block:: text

      [OUTPUT TOO LARGE - Saved to: agent_output_1642789123.txt]

      **Timeout Issues**

      Increase timeout for slow examples:


.. code-block:: bash

      python doc_utils_runner.py run --timeout 600  # 10 minutes

      Integration with CI/CD



      Integrate documentation utilities into your CI/CD pipeline:

      .. tabs::


      .. tab:: GitHub Actions

.. code-block:: yaml

         name: Documentation Utilities
         on: [push, pull_request]

         jobs:
           doc-utilities:
             runs-on: ubuntu-latest
             steps:
               - uses: actions/checkout@v3

               - name: Setup Python
                 uses: actions/setup-python@v4
                 with:
                   python-version: '3.12'

               - name: Install dependencies
                 run: |
                   pip install poetry
                   poetry install --with docs

               - name: Run documentation utilities
                 run: nox -s doc_utils_full

               - name: Upload artifacts
                 uses: actions/upload-artifact@v3
                 with:
                   name: documentation-utilities
                   path: docs/build/

         .. tab:: GitLab CI

.. code-block:: yaml

         doc-utilities:
           stage: docs
           image: python:3.12
           before_script:
             - pip install poetry nox
             - poetry install --with docs
           script:
             - nox -s doc_utils_full
           artifacts:
             paths:
               - docs/build/
             expire_in: 30 days

         .. tab:: Pre-commit Hook

.. code-block:: yaml

         # .pre-commit-config.yaml
         repos:
           - repo: local
             hooks:
               - id: doc-utilities-check
                 name: Documentation utilities check
                 entry: nox -s doc_utils_analyze
                 language: system
                 pass_filenames: false
                 always_run: true

         Best Practices



         .. grid:: 1 1 2 2


         .. grid-item-card:: 🔄 Regular Updates

         :shadow: sm

         **Keep documentation current**

         - Run` ``nox -s` doc_utils_full`` weekly
         - Update visualizations after major changes
         - Validate examples before releases
         - Monitor agent discovery for new types

         .. grid-item-card:: 🎯 Targeted Analysis

         :shadow: sm

         **Focus on what matters**

         - Use` ``--agent-name`` for specific analysis
         - Generate visualizations for key agents
         - Validate critical examples first
         - Create focused documentation

         .. grid-item-card:: 📊 Performance Monitoring

         :shadow: sm

         **Track documentation health**

         - Monitor execution times
         - Check success rates
         - Review output sizes
         - Optimize slow components

         .. grid-item-card:: 🔧 Customization

         :shadow: sm

         **Adapt to your needs**

         - Configure timeouts appropriately
         - Choose visualization formats
         - Set documentation styles
         - Filter agent types

         Related Documentation



         - :doc`:`.`./development/index` - Development guide`

``
         - :doc`:`../api/index - API reference`

`
         - :doc`:`../agents/index - Agent documentation`

`
         - :doc`:`../examples/index - Example gallery`

`

         <style>
         .metric-card {
         background: var(--haive-surface);
         border: 1px solid var(--haive-border);
         border-radius: 8px;
         padding: 1.5rem;
         text-align: center;
         transition: transform 0.2s;
         }
         .metric-card:hover {
         transform: translateY(-2px);
         }
         .metric-card .value {
         display: block;
         font-size: 2rem;
         font-weight: bold;
         color: var(--haive-primary);
         margin-bottom: 0.5rem;
         }
         .metric-card .label {
         display: block;
         font-size: 0.875rem;
         color: var(--haive-text-muted);
         }
         .feature-intro {
         text-align: center;
         margin-bottom: 2rem;
         padding: 2rem;
         background: linear-gradient(135deg, var(--haive-primary-light), var(--haive-secondary-light));
         border-radius: 12px;
         }

         </style>

`
