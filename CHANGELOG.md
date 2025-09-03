## [unreleased]

### 🚜 Refactor

- _(tests)_ Move documentation test files from root to docs/tests directory for better organization

### 🚀 Features

- Add lazy loading and import fixing tasks to pyproject.toml
- Introduce universal dry-run wrapper for command execution
- Add examples gallery documentation
- Add AutoAPI debugging configuration and error handling
- Add comprehensive import fixing strategy documentation
- _(docs)_ Add graceful error handling for AutoAPI with organized logging
- Introduce universal dry-run and lazy loading management scripts
- Add syntax error catalog and detailed report files
- _(docs)_ Enhance Sphinx configuration for type hints and generics
- _(docs)_ Enhance docstring tools and coverage analysis
- _(docs)_ Add comprehensive docstring tools for formatting, generation, and validation
- _(docs)_ Add comprehensive documentation quality checking module
- _(docs)_ Add comprehensive documentation auditing module
- _(docs)_ Integrate automatic import diagnostics into sphinx configuration
- Introduce comprehensive dev-tools for automated Python code enhancement
- Add documentation testing and validation scripts
- _(memory)_ Add memory_reorganized module from backup branch
- Introduce comprehensive documentation error collection and analysis system
- _(docs)_ Docs update.
- _(docs)_ Add control for example execution in Sphinx builds
- _(docs)_ Add comprehensive analysis of documentation import issues
- _(docs)_ Enhance documentation build sessions with example control
- _(docs)_ Apply systematic fixes for documentation import errors
- _(docs)_ Implement additional fixes and enhancements for documentation imports
- _(docs)_ Enhance Sphinx configuration and import diagnostics
- _(docs)_ Reorganize Sphinx configuration and enhance documentation

### 🐛 Bug Fixes

- _(docs)_ Remove problematic Sphinx extensions without setup() function
- Correct relative imports in conf_modules - extensions now load correctly (76 total)
- _(docs)_ Improve sphinx configuration for generic class handling
- _(docs)_ Resolve import errors and sphinx configuration issues
- _(docs)_ Add additional missing modules to mock imports
- _(docs)_ Add more missing modules to mock imports for memory and multi-agent
- _(docs)_ Enhance Sphinx configuration for generic class handling
- _(docs)_ Remove incompatible sphinx-toolbox extensions due to ForwardRef issues
- _(docs)_ Improve handling of generic classes in Sphinx configuration
- _(docs)_ Remove unused custom getitem function from Sphinx configuration
- _(docs)_ Refine autoapi ignore patterns for problematic files
- Convert to relative imports in noxfiles package
- _(hyde)_ Partial fix for SequentialAgent import errors

### 🚜 Refactor

- Update type hints and clean up Sphinx configuration
- Remove dryrun_wrapper.py script
- Streamline command execution approach
- Update import fixing tasks in pyproject.toml
- _(docs)_ Streamline Sphinx configuration for generic class handling

### 📚 Documentation

- Overhaul Nox session documentation for Haive framework

### ⚙️ Miscellaneous Tasks

- Clean up Sphinx configuration and update extension imports
- Update subproject commit reference for haive-mcp
- Update subproject commit references for haive-agents, haive-core, and haive-mcp
- Refactor noxfile.py for improved organization and clarity
- Update subproject commit references for haive-agents, haive-core, and haive-mcp
- Update subproject commit reference for haive-games
- Update haive-mcp submodule with Git LFS setup
- Refactor import and task paths in pyproject.toml
- Update subproject commit references for haive-core and haive-dataflow
- Add robots.txt for search engine indexing
- Update subproject commit references for haive-agents, haive-dataflow, haive-games, haive-mcp, haive-prebuilt, and haive-tools
- Update linting rules in trunk.yaml to include additional script files
- Update subproject commit references for haive-agents, haive-dataflow, and haive-prebuilt
- Update subproject commit references for haive-dataflow and haive-tools
- _(dependencies)_ Add sphinx-toolbox to development dependencies
- Update subproject commit references for haive-agents, haive-core, and haive-games
- _(docs)_ Update lint configuration to include additional documentation files
- Update subproject commit references for haive-agents and haive-core
- Update subproject commit reference for haive-tools
- Update submodule references after validator fixes
- Add validator fix scripts and documentation
- Add GitHub Action for handling submodules
- Streamline YAML configuration files
- Update Vale style configuration for consistency and docstring formatting
- Update docker-compose.yml for consistency and readability
- Enhance pre-commit configuration for improved YAML handling and formatting
- Enhance Sphinx command execution for improved verbosity and feedback
- Update dependencies and configuration for YAML handling
- Refine YAML configuration for improved readability and consistency
- Add comprehensive documentation build issue reports and checklists
- Remove deprecated documentation scripts and reports
- Remove deprecated dev-tools scripts for code enhancement
- Update .gitignore to exclude specific git fsck repair directory
- Update .gitignore to include recovery_catalog directory
- Update .gitignore to include pnpm-lock.yaml
- Refine pre-commit configuration for consistency and clarity
- Update monkeytype.ini to exclude virtual environment directory
- Update .gitignore to include archive directory
- Remove outdated deployment logs and backup manifests
- Remove outdated documentation and capture files
- Remove obsolete scripts and documentation files
- Remove outdated tournament result files and scripts
- Remove outdated stash files and enhance documentation structure
- Remove outdated documentation and testing scripts
- Remove outdated documentation reports and summary files
- Remove outdated documentation reports and summary files
- Remove obsolete scripts and files related to stash analysis and recovery
- Removed recovery catalog
- Update pyproject.toml with new dependencies and import rules
- Update noxfile.py to enhance documentation testing sessions
- Update dynamic_activation_example.py to improve import organization
- Enhance documentation and tool organization
- Add comprehensive documentation and error analysis files
- Update haive-agents subproject commit to latest version
- Update haive-agents subproject commit to latest version
- _(docs)_ Update conf.py to address import issues and enhance documentation build
- Update haive-agents subproject commit to latest version
- Update trunk.yaml configuration to enhance runtime and lint settings
- Refine trunk.yaml configuration for pre-commit hooks and output verbosity
- Update trunk.yaml to run pre-commit hooks on all staged files
- Refactor noxfiles for improved readability and consistency
- Update trunk.yaml to enhance pre-commit debugging and output management
- Refine trunk.yaml configuration for pre-commit hooks and output management
- Refine trunk.yaml configuration for pre-commit hooks and output management
- Refine trunk.yaml configuration for pre-commit hooks and output management
- Removed the auto update into actions/workflows from .pre-commit
- Update configuration files and add requirements update workflow
- Remove outdated JSON output files and backup scripts
- Enhance scripts with type hinting and formatting improvements
- Update .gitignore and pre-commit configuration
- Update .gitignore and trunk.yaml for linter configurations
- Add .gitignore for documentation files
- _(pyproject)_ Add sphinxcontrib-spelling and pyenchant dependencies
- Update subproject commits for haive-agents and haive-core
- Update .gitignore to include CLI tool log files
- Update subproject commits for haive packages

## [0.1.0] - 2025-07-31

### 🚀 Features

- Reorganize documentation structure and clean up codebase
- Complete documentation build system setup
- Add enhanced tool management with validation routing
- Add structured output generalization for agents
- Add comprehensive documentation for games, engines, and models
- Simplify documentation CSS/JS and fix white-on-white text
- Add comprehensive MCP development session memory
- Transform games page to use beautiful showcase template
- Introduce debugging scripts for schema composition and engine tracking
- Add comprehensive documentation for memory structure and identified issues
- Add Sphinx configuration for Haive documentation
- Enhance Haive documentation with API reference and new architecture document
- Add API reference section to Haive tools documentation
- Update CLAUDE documentation and enhance API references
- _(docs)_ Improve build system with proper serve/autobuild separation
- _(tests)_ Add serialization tests for AugLLMConfig and address PydanticUndefined issues
- _(tests)_ Add test script for serialization issue resolution approaches
- _(tests)_ Add test script for serialization fix verification
- _(tests)_ Remove obsolete serialization test scripts
- _(docs)_ Add fast incremental build command for documentation
- _(debug)_ Add comprehensive debug scripts for prompt template conversion
- _(tests)_ Remove test script for engine node fix verification
- _(postgres)_ Implement PostgreSQL store tests and enhance documentation
- _(docs)_ Switch to PyData Sphinx theme and enhance documentation options
- _(agents)_ Implement agent-as-tool pattern in base Agent class
- _(docs)_ Enhance Sphinx configuration for improved documentation and GitHub integration
- _(examples)_ Add comprehensive multi-agent examples showcasing advanced patterns
- _(docs)_ Implement scripts to fix await issues and enhance documentation build
- _(docs)_ Comprehensive documentation issues audit and screenshot automation
- _(docs)_ Add JavaScript visualization file to HTML config
- _(types)_ Add 2,550+ type hints across all packages 🚀
- Massive type hint improvements across all packages
- Add comprehensive automation tools suite
- _(multi-agent)_ Implement Enhanced MultiAgent V3 with comprehensive features
- _(docs)_ Comprehensive documentation styling and structure overhaul
- _(docs)_ Comprehensive documentation styling and structure overhaul
- _(recovery)_ Complete submodule recovery and conflict resolution
- _(haive-core)_ Implement comprehensive lazy loading for import performance
- Comprehensive logging fixes and haive-agents documentation organization
- Add documentation utilities and scripts for agent analysis, visualization, and validation
- Enhance CLAUDE.md with agent examples and fix visualization script
- Add comprehensive fix strategy documentation and enhance validation scripts
- Add new documentation for ValidationNodeV2 and SimpleAgentV3 integration
- Add comprehensive Sphinx extensions installation script
- Add pre-commit config with hooks and CLI dependencies (bypassing hooks for now)
- Configure vale for Google-style docstrings and fix pre-commit errors
- Add comprehensive automated code fixing tools
- Introduce modular Sphinx configuration for enhanced documentation management
- _(trunk)_ Integrate custom pre-commit actions with Haive-specific validations
- _(trunk)_ Complete pre-commit integration with trunk actions
- _(trunk)_ Complete pre-commit integration with trunk actions
- _(trunk)_ Integrate custom pre-commit actions with Haive-specific validations
- _(trunk)_ Complete pre-commit integration with trunk actions
- _(trunk)_ Complete simplified trunk + pre-commit integration
- _(debug)_ Add scripts for syntax error checking and cataloging
- _(nox)_ Enhance documentation session imports in noxfile
- _(nox)_ Introduce environment utilities and phased documentation sessions

### 🐛 Bug Fixes

- Sync submodules to namespace-migration branch
- Replace broken autosummary with manual module documentation
- Remove discovered_readmes bloat and create missing page template
- Add exclusions for virtual environments and discovered_readmes
- Consolidate API documentation structure and apply showcase styling
- Improve MessageList serialization with proper BaseMessage checking and engine metadata preservation
- Replace ugly colors with beautiful purple theme and fix autodoc
- Fix white-on-white text issues in showcase
- Add nuclear text visibility fixes for showcase
- _(docs)_ Resolve toctree navigation duplication
- _(actions)_ Remove unnecessary blank lines in action YAML files
- _(docs)_ Resolve P0 AutoAPI infrastructure and apply design fixes
- Syntax errors in automation scripts and apply initial fixes
- Syntax errors in automation scripts and apply initial fixes
- Massive compilation error cleanup across all packages
- Update .gitmodules to reflect correct branches
- _(haive-core)_ Resolve 38 syntax errors
- _(haive-agents)_ Resolve 38 syntax errors
- _(haive-games)_ Resolve 4 syntax errors
- Update localhost URLs to new port in screenshot checking script
- Resolve circular imports and syntax errors in haive-agents
- Resolve additional import and syntax errors in haive-agents
- _(trunk)_ Override pre-push hook to check staged files only
- _(trunk)_ Enable proper trunk git hook actions

### 💼 Other

- Update haive-agents submodule ref to 5d585fec
- Move test files to proper locations and create AgentNodeV3 sequential test
- Remove test file

### 🚜 Refactor

- _(docs)_ Update Sphinx configuration for improved documentation generation
- Enhance memory management in documentation sessions
- Reorganize imports and enhance session listing in noxfile
- Overhaul Sphinx documentation configuration for modularity and efficiency
- Improve import organization across configuration files

### 📚 Documentation

- Add Claude memory documentation system
- Chess game already has comprehensive documentation
- Enhance Clue game models with comprehensive documentation
- Begin enhancing Mastermind game models documentation
- Add enhanced coding style guide with comprehensive Python examples
- Enhance CLAUDE.md with additional spacing for improved readability
- Add comprehensive improvements summary and test build
- Remove obsolete test build HTML file
- _(persistence)_ Add memory guide for Pydantic PostgreSQL serialization fix
- _(tools)_ Add comprehensive store memory system documentation
- _(store-tools)_ Add comprehensive integration documentation for store tools
- _(architecture)_ Add comprehensive guide for Enhanced Long-Term Memory Agent Architecture
- Add namespaced polyrepo structure and submodule safety to CLAUDE.md
- Fix alignment issues and add game streaming visualization
- Add comprehensive demo pages for all games and agents
- _(ci_cd)_ Update trunk + pre-commit integration guide to v5.0
- _(ci_cd)_ Add comprehensive guides for trunk and pre-commit integration
- Add comprehensive documentation for build issues and progress
- _(debugkit)_ Add comprehensive documentation for the Haive debugkit module

### 🧪 Testing

- Verify pre-commit hooks integration
- Verify simplified trunk + pre-commit integration
- Verify trunk pre-push only checks staged files

### ⚙️ Miscellaneous Tasks

- Ignore model cache
- Sync .gitignore to submodules and clean .pytest_cache
- Reorganize and update .gitignore to streamline ignored files and directories
- Expand .gitignore to include notebooks, logs, JSON dumps, and LangChain cache
- Update haive.code-workspace with enhanced settings and organization
- Update .gitignore for improved file management and clarity
- Comprehensive update to .gitignore for improved file management
- Update .gitignore to include additional directories for better file management
- Update .gitmodules to modify submodule configurations
- Update .gitmodules to refine submodule configurations
- Update haive.code-workspace for improved organization and clarity
- Update .gitignore and haive.code-workspace for improved organization and management
- Refactor haive.code-workspace for improved settings and clarity
- Update .gitignore and remove workspace files for improved organization
- Refactor code for improved readability and consistency
- Add DeepSource configuration for code analysis and formatting
- Remove deprecated diagnostic scripts for improved project cleanliness
- Update .gitignore to include project_docs directory
- Remove obsolete game result and loader metadata files
- _(dependencies)_ Update pyproject.toml and enhance documentation exclusion patterns
- _(scripts)_ Remove deprecated MCP Discovery Agent runner script
- _(cleanup)_ Remove obsolete debug scripts for agent and schema testing
- _(cleanup)_ Remove obsolete build artifacts and temporary files
- _(dependencies)_ Update linting tools and ignore documentation directory
- _(cleanup)_ Remove obsolete tournament result files
- _(cleanup)_ Remove obsolete test files for enhanced tool management
- _(gitattributes)_ Add tracking for release documentation archives
- _(docker)_ Clean up configuration files by removing unnecessary blank lines
- _(docs)_ Standardize string formatting in documentation examples
- _(gitattributes, gitignore)_ Update tracking for project_docs folder
- Clean up Git repository and documentation structure
- Update haive-agents submodule with enhanced patterns
- Update submodules with Enhanced MultiAgent V3 implementation
- Update linting configuration to allow package tests
- Update haive-agents submodule reference
- Update haive-core submodule reference for PostgreSQL fix
- Update haive-agents submodule reference for PostgreSQL test fixes
- Update haive-core submodule for PostgreSQL env var fix
- Update submodules for PostgreSQL and structured output fixes
- Update submodules for circular import fixes
- Update .clocignore to exclude test files
- Add sgfmill dependency to pyproject.toml
- Remove sphinx-docsearch dependency and add Safe Dev Dependencies Change Workflow documentation
- Update pyproject.toml with new dependencies and task configurations
- Update pyproject.toml for dependency versions and task configurations
- Update haive-tools submodule reference
- Update haive-mcp submodule with syntax error fixes
- Add .deepsource.toml
- Update .deepsource.toml
- Update Vale configuration for improved style checks
- Update pyproject.toml with new dependencies and linting configurations
- Update submodule references for haive-agents and haive-core
- Add lazy-log-formatter dependency and remove obsolete ubmodule status file
- Add sphinxtesters dependency for improved Sphinx testing
- Add pytest-doctestplus and sphinx-testing dependencies for enhanced testing
- _(pre-commit)_ Standardize hook names by removing quotes
- _(dependencies)_ Remove sphinx-webtools from pyproject.toml
- _(dependencies)_ Update pyproject.toml with new logging and debugging libraries
- _(haive-core)_ Update subproject commit reference
- Update subproject commit references for haive-agents, haive-core, and haive-tools
- Update subproject commit reference for haive-agents
- Update subproject commit reference for haive-agents
- Update subproject commit references for haive-agents and haive-core
- Update subproject commit reference for haive-core
- Update subproject commit reference for haive-core
- Update subproject commit reference for haive-core
- Update subproject commit reference for haive-agents
- Update subproject commit reference for haive-agents
- Update subproject commit references for haive-agents and haive-core
- Update subproject commit reference for haive-core
- Update subproject commit reference for haive-core
- Update subproject commit reference for haive-core
