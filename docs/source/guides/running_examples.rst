Running Examples
================

Haive provides a comprehensive system for running and visualizing agent examples across all packages. This guide shows you how to use the Universal Example Runner system.

Quick Start
-----------

Run all examples with one command::

    # From project root
    python run_all_examples.py

    # With custom settings
    python run_all_examples.py --concurrent 5 --timeout 600

    # Only generate visualizations (faster)
    python run_all_examples.py --viz-only

Example Runner Features
-----------------------

The Universal Example Runner provides:

* **Automatic Discovery**: Finds all example files across packages
* **Streaming Output**: Real-time output display during execution
* **Visualization Generation**: Creates agent workflow diagrams
* **Error Handling**: Graceful handling of failed examples
* **Concurrent Execution**: Run multiple examples in parallel
* **Comprehensive Reports**: Detailed execution summaries

Architecture Support
--------------------

The runner supports all Haive agent architectures:

* **Simple Agents**: Basic conversational agents
* **ReAct Agents**: Reasoning and acting agents with tools
* **RAG Agents**: Retrieval-augmented generation agents
* **Planning Agents**: Multi-step planning agents
* **Game Agents**: Game-playing AI agents
* **Multi-Agent Systems**: Coordinated agent workflows

Usage Examples
--------------

Basic Usage
~~~~~~~~~~~

Run all examples with default settings::

    python run_all_examples.py

The runner will:

1. Discover all ``example.py`` files across packages
2. Display a list of found examples
3. Ask for confirmation before running
4. Execute examples with streaming output
5. Generate visualizations where possible
6. Create a comprehensive report

Advanced Options
~~~~~~~~~~~~~~~~

Customize execution with command-line options::

    # Run with more concurrent processes
    python run_all_examples.py --concurrent 8

    # Increase timeout for slow examples
    python run_all_examples.py --timeout 900

    # Only generate visualizations (skip execution)
    python run_all_examples.py --viz-only

    # Custom output directory
    python run_all_examples.py --output-dir my_results

Documentation Integration
-------------------------

For documentation generation, use the docs-specific runner::

    cd docs/
    python run_examples_for_docs.py

This will:

* Run key examples suitable for documentation
* Generate RST files for Sphinx Gallery
* Create visualization images in ``auto_examples/``
* Update the examples gallery index

The docs runner is optimized for:

* Shorter timeouts (suitable for CI/CD)
* Filtered example selection (most important only)
* Documentation-friendly output formatting
* Integration with Sphinx build system

Output Structure
----------------

The runner creates organized output:

.. code-block:: text

    example_outputs/
    ├── execution_report.md          # Summary report
    ├── full_output.txt             # Complete output log
    ├── agent_visualization_1.png   # Generated diagrams
    └── large_output_*.txt          # Individual large outputs

Example Discovery
-----------------

The system automatically discovers examples from:

* ``examples/`` directories in each package
* ``example.py`` files in agent modules
* Prebuilt agent examples
* Documentation examples
* Test examples (filtered appropriately)

Visualization Generation
------------------------

When examples include compatible agents, the runner:

1. Detects the agent type and architecture
2. Creates a minimal agent instance
3. Compiles the agent graph
4. Generates a workflow visualization PNG
5. Saves the diagram with a descriptive name

Supported visualizations:

* **Simple Agent Workflows**: Basic linear flows
* **ReAct Agent Graphs**: Complex reasoning loops
* **Multi-Agent Systems**: Agent interaction patterns
* **Tool Integration**: Tool usage patterns

Error Handling
--------------

The runner gracefully handles:

* **Import Errors**: Reports missing dependencies
* **Execution Timeouts**: Prevents hanging examples
* **Large Outputs**: Saves oversized outputs to files
* **Visualization Failures**: Continues without breaking
* **Concurrent Failures**: Isolates failed examples

Reporting
---------

The execution report includes:

* **Success/Failure Counts**: Overall statistics
* **Execution Times**: Performance metrics
* **Architecture Breakdown**: Agent type distribution
* **Error Details**: Specific failure information
* **Generated Files**: List of created visualizations

Integration with Build System
------------------------------

The example runner integrates with:

* **Nox Sessions**: Run via ``nox -s examples``
* **CI/CD Pipelines**: Automated example testing
* **Documentation Builds**: Gallery generation
* **Development Workflow**: Quick testing of changes

Nox Integration
~~~~~~~~~~~~~~~

Add to your development workflow::

    # Run examples during development
    nox -s examples

    # Run examples with docs generation
    nox -s examples_docs

Custom Example Scripts
----------------------

You can create custom runners for specific needs:

.. code-block:: python

    from scripts.doc_utils.example_runner import UniversalExampleRunner, ExecutionConfig

    async def run_my_examples():
        runner = UniversalExampleRunner()
        
        # Custom configuration
        config = ExecutionConfig(
            timeout_seconds=120,
            enable_visualization=True,
            max_output_size=1000000
        )
        
        # Discover specific examples
        examples = await runner.discover_all_examples()
        my_examples = [e for e in examples if "my_agent" in str(e)]
        
        # Run with custom settings
        results = await runner.run_multiple_examples(
            my_examples, config, max_concurrent=2
        )
        
        # Generate custom report
        report = runner.generate_example_report(results)
        print(report)

Troubleshooting
---------------

Common Issues
~~~~~~~~~~~~~

**Import Errors**
    Ensure all dependencies are installed: ``poetry install --all-extras``

**Timeout Issues**
    Increase timeout: ``--timeout 900`` (15 minutes)

**Memory Issues**
    Reduce concurrency: ``--concurrent 1``

**Missing Visualizations**
    Check that agents support the ``visualize_graph()`` method

Debug Mode
~~~~~~~~~~

Run with verbose logging::

    # Enable debug logging
    export PYTHONPATH=.
    python -m logging run_all_examples.py --verbose

Performance Tips
----------------

* Use ``--viz-only`` for quick visualization generation
* Adjust ``--concurrent`` based on your system capabilities
* Set appropriate ``--timeout`` values for complex examples
* Use the docs runner for CI/CD to run only essential examples

Best Practices
--------------

1. **Run regularly** during development to catch regressions
2. **Review reports** to understand example health
3. **Update examples** when agent APIs change
4. **Use visualizations** to document agent workflows
5. **Integrate with CI/CD** for automated testing

The Universal Example Runner makes it easy to maintain and showcase the rich ecosystem of Haive agent examples across all packages.