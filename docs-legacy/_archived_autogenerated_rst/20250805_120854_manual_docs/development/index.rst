🛠️ Development Guide



   <div class="dev-intro">
   <h1>Development & Contribution Guide</h1>
   <p>Everything you need to contribute to Haive, from setup to advanced tooling.</p>
   </div>

.. note::


   Grid layout removed due to sphinx_design incompatibility.


   .. grid-item-card:: 🚀 Getting Started

      :shadow: md

      **Development Environment Setup**

      Poetry, nox, pre-commit hooks, and IDE configuration for optimal development experience.

   .. grid-item-card:: 🛠️ Documentation Utilities

      :shadow: md

      **Advanced Documentation Tools**

      Analyze agents, generate visualizations, validate examples, and create comprehensive documentation.

   .. grid-item-card:: 🧪 Testing Guide

      :shadow: md

      **Testing Philosophy & Practices**

      No-mocks testing, real component validation, and comprehensive test coverage strategies.

   .. grid-item-card:: 📝 Contributing

      :shadow: md

      **Contribution Guidelines**

      Code standards, pull request process, and community guidelines for contributors.

Quick Commands



.. tabs::


   .. tab:: Documentation

.. code-block:: bash

         # Build documentation
         nox -s docs                    # Fast incremental build
         nox -s docs_full               # Full rebuild
         nox -s docs_autobuild          # Live reload server

         # Documentation utilities
         nox -s doc_utils_full          # Complete analysis & generation
         nox -s doc_utils_analyze       # Agent analysis report
         nox -s doc_utils_visualize     # Generate visualizations

         .. tab:: Testing

.. code-block:: bash

         # Run tests
         nox -s test                    # All tests
         poetry run pytest -v          # Verbose output
         poetry run pytest -k "test_simple"  # Specific tests

         # Quality checks
         nox -s lint                    # Code linting
         nox -s docs_quality            # Documentation quality

         .. tab:: Development

.. code-block:: bash

         # Setup development environment
         poetry install --all-extras
         poetry run pre-commit install

         # Check code quality
         trunk check --all
         poetry run mypy packages/

         Development Workflow



         <div class="workflow-diagram">

         <div class="workflow-step">

         <div class="step-number">1</div>

         <div class="step-content">
         <h4>Setup</h4>
         <p>Clone, install dependencies, configure environment</p>
         </div>

         </div>

         <div class="workflow-arrow">→</div>

         <div class="workflow-step">

         <div class="step-number">2</div>

         <div class="step-content">
         <h4>Develop</h4>
         <p>Write code, create tests, update documentation</p>
         </div>

         </div>

         <div class="workflow-arrow">→</div>

         <div class="workflow-step">

         <div class="step-number">3</div>

         <div class="step-content">
         <h4>Validate</h4>
         <p>Run tests, check quality, generate docs</p>
         </div>

         </div>

         <div class="workflow-arrow">→</div>

         <div class="workflow-step">

         <div class="step-number">4</div>

         <div class="step-content">
         <h4>Submit</h4>
         <p>Create PR, review, merge</p>
         </div>

         </div>
         </div>

         Documentation Standards



         .. grid:: 1 1 3 3


         .. grid-item-card:: 📝 Code Documentation

         :shadow: sm

         **Google-style Docstrings**

         - All public functions documented
         - Type hints on all parameters
         - Examples for complex functions
         - Sphinx AutoAPI compatible

         .. grid-item-card:: 🎨 Visual Documentation

         :shadow: sm

         **Automated Visualizations**

         - Agent workflow diagrams
         - Architecture overviews
         - Comparison charts
         - Performance metrics

         .. grid-item-card:: 🧪 Living Documentation

         :shadow: sm

         **Example-Driven Docs**

         - Runnable code examples
         - Validated with real components
         - Auto-generated from analysis
         - Cross-referenced

         Quality Assurance



         Our development process ensures high code quality:

         .. list-table::


         :widths: 30 70
         :header-rows: 1

         * - Tool*

         - Purpose

         * - *Poetry**

         - Dependency management and virtual environments

         ** - *Nox**

         - Automated testing and documentation builds

         ** - *Pre-commit**

         - Git hooks for code quality checks

         ** - *Trunk**

         - Super-linter with auto-fixes

         ** - *Ruff**

         - Lightning-fast Python linting

         ** - *MyPy**

         - Static type checking

         ** - *Pytest**

         - Testing framework with real components

         Documentation Utilities Features



         The advanced documentation utilities provide:

         <div class="features-grid">

         <div class="feature">
         <span class="feature-icon">🔍</span>

         <div class="feature-content">
         <h4>Agent Discovery</h4>
         <p>Automatically finds and analyzes 100+ agent types across all packages</p>
         </div>

         </div>

         <div class="feature">
         <span class="feature-icon">🎨</span>

         <div class="feature-content">
         <h4>Universal Visualization</h4>
         <p>Creates workflow diagrams for any agent type, regardless of architecture</p>
         </div>

         </div>

         <div class="feature">
         <span class="feature-icon">🧪</span>

         <div class="feature-content">
         <h4>Example Validation</h4>
         <p>Tests all examples with streaming output and error handling</p>
         </div>

         </div>

         <div class="feature">
         <span class="feature-icon">📚</span>

         <div class="feature-content">
         <h4>Auto Documentation</h4>
         <p>Generates comprehensive docs with cross-references and API extraction</p>
         </div>

         </div>
         </div>

         Getting Help



         .. grid:: 1 1 2 2


         .. grid-item-card:: 💬 Community

         :shadow: sm

         **Join the Discussion**

         - GitHub Discussions for questions
         - Discord for real-time chat
         - Stack Overflow for technical issues
         - Community forums

         .. grid-item-card:: 🐛 Bug Reports

         :shadow: sm

         **Report Issues**

         - GitHub Issues for bugs
         - Include reproduction steps
         - Use issue templates
         - Provide system information

         .. toctree::


         :maxdepth: 2
         :hidden:

         setup
         doc_utilities
         testing
         contributing

         <style>
         .dev-intro {
         text-align: center;
         margin-bottom: 2rem;
         padding: 2rem;
         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
         color: white;
         border-radius: 12px;
         }
         .workflow-diagram {
         display: flex;
         align-items: center;
         justify-content: center;
         flex-wrap: wrap;
         gap: 1rem;
         margin: 2rem 0;
         padding: 2rem;
         background: var(--haive-surface);
         border-radius: 12px;
         }
         .workflow-step {
         display: flex;
         flex-direction: column;
         align-items: center;
         text-align: center;
         min-width: 150px;
         }
         .step-number {
         width: 40px;
         height: 40px;
         border-radius: 50%;
         background: var(--haive-primary);
         color: white;
         display: flex;
         align-items: center;
         justify-content: center;
         font-weight: bold;
         margin-bottom: 1rem;
         }
         .step-content h4 {
         margin: 0 0 0.5rem 0;
         color: var(--haive-text);
         }
         .step-content p {
         margin: 0;
         font-size: 0.875rem;
         color: var(--haive-text-muted);
         }
         .workflow-arrow {
         font-size: 1.5rem;
         color: var(--haive-text-muted);
         }
         .features-grid {
         display: grid;
         grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
         gap: 1.5rem;
         margin: 2rem 0;
         }
         .feature {
         display: flex;
         align-items: start;
         gap: 1rem;
         padding: 1.5rem;
         background: var(--haive-surface);
         border: 1px solid var(--haive-border);
         border-radius: 8px;
         }
         .feature-icon {
         font-size: 2rem;
         flex-shrink: 0;
         }
         .feature-content h4 {
         margin: 0 0 0.5rem 0;
         color: var(--haive-text);
         }
         .feature-content p {
         margin: 0;
         color: var(--haive-text-muted);
         font-size: 0.875rem;
         }

         </style>
