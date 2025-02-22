#!/bin/bash
# Complete setup script for Sphinx documentation with mock modules

# Exit on error
set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Setting up documentation build environment...${NC}"

# Check if we're in the right directory
if [ ! -d "docs" ]; then
    echo -e "${RED}Please run this script from the project root directory!${NC}"
    exit 1
fi

# Create necessary directories
mkdir -p docs/_static
mkdir -p docs/_build
mkdir -p docs/_templates
mkdir -p docs/scripts
mkdir -p docs/mockups/haive/agents
mkdir -p docs/mockups/haive/flstaesr
mkdir -p docs/mockups/haive/core

# Create the mockup module generator script
cat > docs/scripts/create_module_mockups.py << 'EOL'
#!/usr/bin/env python
"""
Script to create mockup modules with docstrings for documentation.
"""
import os
import sys
import shutil
from pathlib import Path

# Define the mockup directory
MOCKUP_DIR = "docs/mockups"

# Define the structure and docstrings for the modules
MODULES = {
    "haive": {
        "docstring": """
        Haive: A Python framework for building and deploying AI agents.
        
        Haive provides tools, abstractions, and infrastructure for developing
        sophisticated AI agents that can reason, plan, and interact with their environment.
        """,
        "submodules": {
            "agents": {
                "docstring": """
                Agent implementations and frameworks.
                
                This module contains various agent implementations, from simple reactive
                agents to complex reasoning frameworks.
                """,
                "submodules": {
                    "summarizer": {
                        "docstring": """
                        A module for text summarization agents.
                        
                        These agents can process and summarize large amounts of text data.
                        """,
                        "submodules": {
                            "agent.py": """
                            Implementation of the summarizer agent.
                            
                            The SummarizerAgent takes in text and produces concise summaries
                            while preserving the key information.
                            
                            Classes:
                                SummarizerAgent: Main agent implementation for text summarization.
                            """,
                            "aug_llms.py": """
                            Augmented language models for summarization.
                            
                            Provides specialized extensions to base language models to improve
                            summarization capabilities.
                            
                            Classes:
                                SummaryAugmentedLLM: LLM with summarization-specific augmentations.
                            """,
                            "prompts.py": """
                            Prompts for summarization tasks.
                            
                            Contains templates and strategies for prompting language models
                            to perform effective summarization.
                            
                            Functions:
                                get_summary_prompt: Returns a prompt template for summarization.
                            """
                        }
                    },
                    "web_nav": {
                        "docstring": """
                        A module for web navigation agents.
                        
                        These agents can browse and interact with web content to extract information.
                        """,
                        "submodules": {
                            "agent.py": """
                            Implementation of the web navigation agent.
                            
                            The WebNavAgent can navigate websites and extract information.
                            
                            Classes:
                                WebNavAgent: Main agent implementation for web navigation.
                            """,
                            "state.py": """
                            State management for web navigation.
                            
                            Tracks the current state of a web navigation session.
                            
                            Classes:
                                BrowserState: Represents the state of a browser session.
                            """,
                            "tools.py": """
                            Tools for web interaction.
                            
                            Provides functionality for clicking, scrolling, typing, and other web-based actions.
                            
                            Classes:
                                WebTool: Base class for web interaction tools.
                                ClickTool: Tool for clicking elements on a page.
                                ScrollTool: Tool for scrolling a page.
                            """
                        }
                    },
                    "self_discover": {
                        "docstring": """
                        A module for self-discovering agents.
                        
                        These agents can autonomously explore and learn about their environment.
                        """,
                        "submodules": {
                            "agent.py": """
                            Implementation of the self-discovering agent.
                            
                            The SelfDiscoverAgent can explore and learn from its environment.
                            
                            Classes:
                                SelfDiscoverAgent: Main agent implementation for autonomous exploration.
                            """,
                            "aug_llms.py": """
                            Augmented language models for self-discovery.
                            
                            Provides extensions to base language models to facilitate 
                            autonomous exploration and learning.
                            
                            Classes:
                                ExplorationAugmentedLLM: LLM with exploration-specific augmentations.
                            """,
                            "state.py": """
                            State management for self-discovering agents.
                            
                            Tracks the agent's knowledge and exploration state.
                            
                            Classes:
                                ExplorationState: Represents the state of exploration.
                            """
                        }
                    },
                    "tot": {
                        "docstring": """
                        Tree of Thought agent implementation.
                        
                        Implements the Tree of Thought reasoning framework where multiple reasoning paths
                        are explored in parallel.
                        """,
                        "submodules": {
                            "agent.py": """
                            Implementation of the Tree of Thought agent.
                            
                            The ToTAgent explores multiple reasoning paths to solve complex problems.
                            
                            Classes:
                                ToTAgent: Main agent implementation for Tree of Thought reasoning.
                            """,
                            "state.py": """
                            State management for Tree of Thought agents.
                            
                            Tracks the multiple branches of reasoning being explored.
                            
                            Classes:
                                ThoughtTreeState: Represents the state of a thought tree.
                                ThoughtNode: A node in the thought tree.
                            """
                        }
                    },
                    "react_agent": {
                        "docstring": """
                        Reasoning and Acting agent implementation.
                        
                        Implements the ReAct framework where agents alternate between reasoning and acting.
                        """,
                        "submodules": {
                            "base.py": """
                            Base implementation of the ReAct agent.
                            
                            The ReActAgent alternates between reasoning and acting to solve tasks.
                            
                            Classes:
                                ReActAgent: Main agent implementation for ReAct framework.
                            """
                        }
                    }
                }
            },
            "flstaesr": {
                "docstring": """
                Flexible State and Search Representation.
                
                This module provides tools for representing and manipulating states
                and search spaces in agent-based systems.
                """,
                "submodules": {
                    "transform": {
                        "docstring": """
                        Tools for transforming data representations.
                        
                        Provides utilities for converting between different data formats and structures.
                        """,
                        "submodules": {
                            "base.py": """
                            Base transformation functionality.
                            
                            Defines the base interfaces and implementations for data transformations.
                            
                            Classes:
                                BaseTransformer: Abstract base class for all transformers.
                            """,
                            "inspect_experiment.py": """
                            Tools for inspecting and experimenting with transformations.
                            
                            Provides utilities for visualizing and analyzing transformation results.
                            
                            Functions:
                                inspect_transformer: Analyze the behavior of a transformer.
                            """
                        }
                    },
                    "annotate": {
                        "docstring": """
                        Tools for annotating data.
                        
                        Provides utilities for adding metadata and annotations to data.
                        """,
                        "submodules": {
                            "base.py": """
                            Base annotation functionality.
                            
                            Defines the base interfaces and implementations for data annotation.
                            
                            Classes:
                                BaseAnnotator: Abstract base class for all annotators.
                            """
                        }
                    }
                }
            },
            "core": {
                "docstring": """
                Core functionality for the Haive framework.
                
                Provides foundational tools and utilities used throughout the framework.
                """,
                "submodules": {
                    "utils.py": """
                    Utility functions and classes.
                    
                    Provides common utilities used across the Haive framework.
                    
                    Functions:
                        format_response: Format agent responses for display.
                        load_config: Load configuration from a file.
                    """,
                    "config.py": """
                    Configuration management.
                    
                    Provides tools for managing and accessing configuration settings.
                    
                    Classes:
                        Config: Central configuration management class.
                    """
                }
            }
        }
    }
}


def create_directory_if_not_exists(directory):
    """Create a directory if it doesn't exist."""
    os.makedirs(directory, exist_ok=True)


def create_module_file(path, docstring):
    """Create a Python module file with the given docstring."""
    with open(path, 'w') as f:
        f.write(f'"""{docstring}"""\n\n')
        
        # Add mock classes or functions based on docstring content
        if "Classes:" in docstring:
            # Extract class names
            class_lines = [line.strip() for line in docstring.split('\n') 
                          if ':' in line and 'Classes:' not in line]
            for line in class_lines:
                class_name = line.split(':')[0].strip()
                f.write(f'\nclass {class_name}:\n    """\n    A mock class for documentation.\n    """\n    pass\n')
        
        if "Functions:" in docstring:
            # Extract function names
            func_lines = [line.strip() for line in docstring.split('\n') 
                         if ':' in line and 'Functions:' not in line]
            for line in func_lines:
                func_name = line.split(':')[0].strip()
                f.write(f'\ndef {func_name}():\n    """\n    A mock function for documentation.\n    """\n    pass\n')


def create_init_file(path, docstring, imports=None):
    """Create an __init__.py file with the given docstring and imports."""
    with open(path, 'w') as f:
        f.write(f'"""{docstring}"""\n\n')
        
        if imports:
            for imp in imports:
                if not imp.endswith('.py'):
                    f.write(f'from . import {imp}\n')
                else:
                    # Import from .py files directly
                    module_name = imp[:-3]  # Remove .py extension
                    f.write(f'from . import {module_name}\n')


def process_module(module_path, module_data, current_path=""):
    """Process a module and its submodules recursively."""
    if current_path:
        new_path = os.path.join(current_path, module_path)
    else:
        new_path = module_path
    
    # If this is a directory module
    if "submodules" in module_data:
        module_dir = os.path.join(MOCKUP_DIR, new_path)
        create_directory_if_not_exists(module_dir)
        
        # Create __init__.py
        init_path = os.path.join(module_dir, "__init__.py")
        submodule_names = list(module_data["submodules"].keys())
        create_init_file(init_path, module_data["docstring"], submodule_names)
        
        # Process submodules
        for submodule_name, submodule_data in module_data["submodules"].items():
            process_module(submodule_name, submodule_data, new_path)
    
    # If this is a Python file
    elif module_path.endswith('.py'):
        file_path = os.path.join(MOCKUP_DIR, new_path)
        create_module_file(file_path, module_data)


def main():
    """Main function to create all mockup modules."""
    # Clean up any existing mockup directory
    if os.path.exists(MOCKUP_DIR):
        shutil.rmtree(MOCKUP_DIR)
    
    # Create the mockup directory
    create_directory_if_not_exists(MOCKUP_DIR)
    
    # Process all modules
    for module_name, module_data in MODULES.items():
        process_module(module_name, module_data)
    
    print(f"Created mockup modules in {MOCKUP_DIR}")


if __name__ == "__main__":
    main()
EOL

# Make the script executable
chmod +x docs/scripts/create_module_mockups.py

# Create mockup modules
echo -e "${YELLOW}Creating mockup modules for documentation...${NC}"
python docs/scripts/create_module_mockups.py

# Create the optimized conf.py file
cat > docs/conf.py << 'EOL'
# Configuration file for the Sphinx documentation builder
import os
import sys
from datetime import datetime

# -- Path setup --------------------------------------------------------------
# Add mockups directory to the path so Sphinx can find the modules
sys.path.insert(0, os.path.abspath('./mockups'))

# Project information
project = 'Haive'
copyright = f'{datetime.now().year}, Your Name'
author = 'Your Name'
release = '0.1.0'

# -- General configuration ---------------------------------------------------
extensions = [
    # Core Sphinx extensions
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
    'sphinx.ext.autosectionlabel',
    'sphinx.ext.todo',
    'sphinx.ext.mathjax',
    
    # Third-party extensions
    'myst_parser',
    'sphinx_copybutton',
    'sphinx_design',
]

# -- Autodoc settings ----------------------------------------------
autodoc_typehints = 'both'
autodoc_typehints_format = 'short'
autodoc_member_order = 'groupwise'  # Group by type (methods, attributes, etc.)
autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'special-members': '__init__, __call__',
    'inherited-members': True,
    'show-inheritance': True,
    'member-order': 'groupwise',
}

# -- Napoleon settings (for Google and NumPy style docstrings) -----------
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = True
napoleon_use_ivar = True
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_preprocess_types = True
napoleon_attr_annotations = True

# -- MyST Parser settings (for Markdown support) ---------------------------
myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "dollarmath",
    "amsmath",
    "html_image",
    "html_admonition",
    "replacements",
    "smartquotes",
    "tasklist",
]
myst_heading_anchors = 3

# -- HTML output settings ---------------------------------------------------
html_theme = 'furo'  # Modern, clean theme
html_title = f"{project} Documentation"
html_short_title = project
html_static_path = ['_static']
html_css_files = ['custom.css']
html_js_files = ['custom.js']
html_favicon = '_static/favicon.ico'
html_logo = '_static/logo.png'
html_show_sourcelink = False
html_copy_source = False

# Furo theme options
html_theme_options = {
    "sidebar_hide_name": False,
    "light_css_variables": {
        "color-brand-primary": "#3776ab",  # Python blue
        "color-brand-content": "#3776ab",
        "color-admonition-background": "#f8f9fb",
        "font-stack": "system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif",
        "font-stack--monospace": "SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', 'Courier New', monospace",
    },
    "dark_css_variables": {
        "color-brand-primary": "#5994ce",  # Lighter blue for dark mode
        "color-brand-content": "#5994ce",
    },
}

# -- Intersphinx mapping --------------------------------------------------
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
}

# -- Additional settings ---------------------------------------------------
todo_include_todos = True  # Include TODOs in documentation
pygments_style = "sphinx"  # Syntax highlighting style

# Mock imports to prevent import errors
autodoc_mock_imports = [
    'src',
    'langchain', 
    'langchain_community',
    'pydantic',
    'BaseModel'
]
EOL

# Create stylish custom.css
cat > docs/_static/custom.css << 'EOL'
/* Enhanced Custom CSS for Haive Documentation */

/* ------ GENERAL PAGE LAYOUT ------- */

/* Improved readability with better font rendering and line spacing */
body {
    text-rendering: optimizeLegibility !important;
    -webkit-font-smoothing: antialiased;
    line-height: 1.7;
    letter-spacing: 0.01em;
}

main {
    max-width: 1000px;
    margin: 0 auto;
}

/* ------ TYPOGRAPHY ------- */

/* Heading styles with improved spacing */
h1, h2, h3, h4, h5, h6 {
    margin-top: 1.5em;
    margin-bottom: 0.8em;
    font-weight: 600;
    line-height: 1.25;
}

h1 {
    font-size: 2.2em;
    position: relative;
    padding-bottom: 0.5em;
    margin-bottom: 1em;
}

h1:after {
    content: "";
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100px;
    height: 4px;
    background: var(--color-brand-primary);
    border-radius: 2px;
}

h2 {
    font-size: 1.7em;
    border-bottom: 1px solid var(--color-background-border);
    padding-bottom: 0.3em;
}

h3 {
    font-size: 1.4em;
    color: var(--color-brand-primary);
}

h4 {
    font-size: 1.2em;
    font-weight: 600;
}

/* Paragraph spacing */
p {
    margin-bottom: 1.2em;
}

/* ------ CODE BLOCKS AND SYNTAX HIGHLIGHTING ------- */

/* Code block styling */
div[class^="highlight-"] {
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    margin: 1.2em 0 1.8em 0;
    position: relative;
    overflow: hidden;
}

div[class^="highlight-"]::before {
    content: "";
    height: 4px;
    width: 100%;
    position: absolute;
    top: 0;
    left: 0;
    background: linear-gradient(to right, var(--color-brand-primary), rgba(55, 118, 171, 0.7));
}

pre {
    padding: 1.2em;
    line-height: 1.5;
    font-size: 0.95em;
    border-radius: 0 0 8px 8px;
    overflow-x: auto;
}

code {
    padding: 0.2em 0.4em;
    border-radius: 3px;
    font-size: 0.9em;
    background-color: var(--color-background-secondary);
}

/* ------ API DOCUMENTATION STYLING ------- */

/* Better API section headers */
.api-section {
    margin-top: 3em;
    padding-top: 1em;
    border-top: 1px solid var(--color-background-border);
}

/* Module headings */
.rubric {
    font-size: 1.3em;
    font-weight: 600;
    color: var(--color-brand-primary);
    margin: 1.5em 0 0.8em 0;
}

/* Class documentation */
dl.class, dl.function, dl.method, dl.attribute {
    background-color: var(--color-background-secondary);
    border-radius: 8px;
    padding: 1.5em;
    margin: 1.5em 0;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
    border-left: 4px solid var(--color-brand-primary);
}

dl.class > dt, dl.function > dt, dl.method > dt {
    font-family: var(--font-stack--monospace);
    font-weight: bold;
    background-color: rgba(0, 0, 0, 0.05);
    padding: 0.7em;
    margin: -1.5em -1.5em 1em -1.5em;
    border-radius: 8px 8px 0 0;
    border-bottom: 1px solid rgba(0, 0, 0, 0.1);
}

/* Function/method signature highlighting */
.sig-name {
    color: var(--color-brand-primary);
    font-weight: bold;
}

.sig-prename {
    color: #777;
}

.sig-param {
    font-style: italic;
}

/* ------ ADMONITIONS (NOTES, WARNINGS, ETC.) ------- */

.admonition {
    border-radius: 8px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    margin: 1.5em 0;
    overflow: hidden;
}

.admonition p.admonition-title {
    font-weight: 600;
    margin: 0;
    padding: 0.8em 1em;
}

.admonition > .admonition-title {
    margin-top: 0 !important;
}

.admonition .admonition-title::before {
    margin-right: 0.5em;
}

.admonition > :not(.admonition-title) {
    margin-left: 1em;
    margin-right: 1em;
}

.admonition > :last-child {
    margin-bottom: 1em;
}

/* Specific admonition types */
.note, .seealso {
    border-left: 4px solid #3776ab;
}

.note .admonition-title, .seealso .admonition-title {
    background-color: rgba(55, 118, 171, 0.1);
    color: #3776ab;
}

.warning, .caution, .attention {
    border-left: 4px solid #ff9800;
}

.warning .admonition-title, .caution .admonition-title, .attention .admonition-title {
    background-color: rgba(255, 152, 0, 0.1);
    color: #e67e00;
}

.danger, .error {
    border-left: 4px solid #e53935;
}

.danger .admonition-title, .error .admonition-title {
    background-color: rgba(229, 57, 53, 0.1);
    color: #d32f2f;
}

.tip, .hint {
    border-left: 4px solid #4caf50;
}

.tip .admonition-title, .hint .admonition-title {
    background-color: rgba(76, 175, 80, 0.1);
    color: #388e3c;
}

/* ------ FEATURE DESCRIPTIONS ------- */

.feature-description {
    background-color: rgba(55, 118, 171, 0.05);
    border-radius: 8px;
    padding: 1.2em;
    margin-bottom: 2em;
    border-left: 4px solid var(--color-brand-primary);
}

.feature-description p {
    margin-bottom: 0;
    font-size: 1.1em;
    color: #555;
}
EOL

# Create a basic custom.js file
cat > docs/_static/custom.js << 'EOL'
// Custom JavaScript for Haive documentation

// Add copy buttons to code blocks
document.addEventListener('DOMContentLoaded', function() {
    const codeBlocks = document.querySelectorAll('pre');
    
    codeBlocks.forEach(function(codeBlock) {
        if (!codeBlock.querySelector('.copybutton')) {
            const button = document.createElement('button');
            button.className = 'copybutton';
            button.textContent = 'Copy';
            
            button.addEventListener('click', function() {
                const code = codeBlock.querySelector('code') ? 
                    codeBlock.querySelector('code').textContent :
                    codeBlock.textContent;
                
                navigator.clipboard.writeText(code.trim()).then(function() {
                    button.textContent = 'Copied!';
                    setTimeout(function() {
                        button.textContent = 'Copy';
                    }, 2000);
                }, function() {
                    button.textContent = 'Error!';
                });
            });
            
            codeBlock.appendChild(button);
        }
    });
});

// Add collapsible sections
document.addEventListener('DOMContentLoaded', function() {
    const collapsibleSections = document.querySelectorAll('.collapsible');
    
    collapsibleSections.forEach(function(section) {
        const header = section.querySelector('h2, h3, h4, h5, h6');
        if (header) {
            header.style.cursor = 'pointer';
            const content = document.createElement('div');
            content.className = 'collapsible-content';
            
            // Move all content after the header into the collapsible div
            let nextElement = header.nextElementSibling;
            while (nextElement) {
                const temp = nextElement.nextElementSibling;
                content.appendChild(nextElement);
                nextElement = temp;
            }
            
            section.appendChild(content);
            
            // Add click handler to toggle visibility
            header.addEventListener('click', function() {
                content.style.display = content.style.display === 'none' ? 'block' : 'none';
            });
        }
    });
});
EOL

# Create placeholder logo
echo -e "${YELLOW}Creating placeholder logo and favicon...${NC}"
convert -size 200x100 canvas:white -font Arial -pointsize 24 -fill black -gravity center -annotate 0 "Haive" docs/_static/logo.png 2>/dev/null || echo "ImageMagick not available, skipping logo creation"
convert -size 32x32 canvas:white -font Arial -pointsize 16 -fill black -gravity center -annotate 0 "H" docs/_static/favicon.ico 2>/dev/null || echo "ImageMagick not available, skipping favicon creation"

# Create a nicer index.rst file
cat > docs/index.rst << 'EOL'
Welcome to Haive
===============

.. raw:: html

   <div style="text-align:center; margin-bottom: 2em;">
     <p style="font-size: 1.2em; color: #555;">
       A powerful framework for building AI agents
     </p>
   </div>

.. grid:: 2

    .. grid-item-card:: Getting Started
        :link: installation
        :link-type: doc
        :class-card: sd-border-0

        Start building with Haive quickly.

    .. grid-item-card:: API Reference
        :link: api/index
        :link-type: doc
        :class-card: sd-border-0

        Explore the Haive API documentation.

Key Features
-----------

- **Flexible Agent Architecture**: Build agents with different reasoning strategies
- **State Management**: Track and manage agent state effectively
- **Tool Integration**: Easily connect agents to external tools and services
- **Extensible Design**: Create custom agents for your specific needs

.. code-block:: python
    :caption: Example: Creating a Simple Agent
    :linenos:

    from haive.agents import SummarizerAgent
    
    # Initialize the agent
    agent = SummarizerAgent()
    
    # Process input text
    result = agent.summarize("Your long text to summarize...")
    
    print(result)

.. toctree::
   :maxdepth: 2
   :caption: Contents:
   :hidden:

   installation
   usage
   api/index
   examples
   contributing
EOL

# Create a basic installation.rst file
cat > docs/installation.rst << 'EOL'
Installation
===========

You can install Haive using pip:

.. code-block:: bash

    pip install haive

Or with Poetry:

.. code-block:: bash

    poetry add haive

Development Installation
-----------------------

For development, clone the repository and install with Poetry:

.. code-block:: bash

    git clone https://github.com/yourusername/haive.git
    cd haive
    poetry install
EOL

# Create a usage.rst file
cat > docs/usage.rst << 'EOL'
Usage
=====

Basic Usage
----------

.. code-block:: python

    from haive.agents import ReActAgent
    from haive.core.config import Config
    
    # Create a configuration
    config = Config()
    config.set("model", "gpt-4")
    
    # Initialize an agent
    agent = ReActAgent(config)
    
    # Run the agent
    result = agent.run("Solve this math problem: If x + 2y = 15 and 2x - y = 5, what are x and y?")
    
    print(result)

Advanced Usage
-------------

.. code-block:: python

    from haive.agents.tot import ToTAgent
    from haive.core.utils import format_response
    
    # Initialize a Tree of Thought agent
    agent = ToTAgent(
        model="gpt-4",
        max_depth=3,
        beam_width=5
    )
    
    # Run the agent with a complex reasoning task
    result = agent.solve(
        "Design an algorithm to find the longest palindromic substring in a string."
    )
    
    # Format the result for display
    # Format the result for display
    formatted = format_response(result)
    
    print(formatted)
EOL

# Create a contributing.rst file
cat > docs/contributing.rst << 'EOL'
Contributing
===========

We welcome contributions to Haive! This document provides guidelines for contributing to the project.

Setting Up Development Environment
---------------------------------

1. Clone the repository:

   .. code-block:: bash

       git clone https://github.com/yourusername/haive.git
       cd haive

2. Install dependencies with Poetry:

   .. code-block:: bash

       poetry install

3. Install pre-commit hooks:

   .. code-block:: bash

       poetry run pre-commit install

Code Style
---------

We follow the Black code style. You can format your code with:

.. code-block:: bash

    poetry run black .

Testing
------

Run tests with pytest:

.. code-block:: bash

    poetry run pytest

Pull Request Process
-------------------

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests to ensure they pass
5. Submit a pull request
EOL

# Create an examples.rst file
cat > docs/examples.rst << 'EOL'
Examples
========

Basic Example: Summarization
---------------------------

.. code-block:: python

    from haive.agents.summarizer import SummarizerAgent
    
    text = """
    Machine learning (ML) is a field of inquiry devoted to understanding and building methods that 'learn', 
    that is, methods that leverage data to improve performance on some set of tasks. It is seen as a part 
    of artificial intelligence. Machine learning algorithms build a model based on sample data, known as 
    training data, in order to make predictions or decisions without being explicitly programmed to do so. 
    Machine learning algorithms are used in a wide variety of applications, such as in medicine, email 
    filtering, speech recognition, and computer vision, where it is difficult or unfeasible to develop 
    conventional algorithms to perform the needed tasks.
    """
    
    agent = SummarizerAgent()
    summary = agent.summarize(text)
    
    print(summary)
    # Output: Machine learning is a field that creates methods to learn from data and improve task 
    # performance without explicit programming. It's considered part of AI and is used in applications 
    # like medicine, email filtering, and computer vision.

Web Navigation Example
--------------------

.. code-block:: python

    from haive.agents.web_nav import WebNavAgent
    
    # Initialize the web navigation agent
    agent = WebNavAgent()
    
    # Navigate to a website and extract information
    results = agent.navigate(
        url="https://example.com",
        task="Find the contact information"
    )
    
    print(results)

Tree of Thought Reasoning
-----------------------

.. code-block:: python

    from haive.agents.tot import ToTAgent
    
    problem = "In how many ways can 8 people be seated at a round table?"
    
    # Initialize a Tree of Thought agent
    agent = ToTAgent(max_branches=3, max_depth=4)
    
    # Solve the problem
    solution = agent.solve(problem)
    
    print(solution)
EOL

# Create missing directories for API
mkdir -p docs/api/agents/generated
mkdir -p docs/api/flstaesr/generated
mkdir -p docs/api/core/generated

# Create developer documentation section
mkdir -p docs/development
cat > docs/development/creating_agents.rst << 'EOL'
Creating Custom Agents
====================

This guide explains how to create custom agents using the Haive framework.

Agent Interface
-------------

All agents should implement a common interface:

.. code-block:: python

    from haive.agents.base import BaseAgent
    
    class CustomAgent(BaseAgent):
        def __init__(self, config=None):
            super().__init__(config)
            # Additional initialization
        
        def run(self, input_data):
            """Main method to execute the agent's logic"""
            # Implement your agent's logic here
            return result

State Management
--------------

Agents typically need to manage state:

.. code-block:: python

    from haive.agents.base import BaseAgent
    from haive.core.state import State
    
    class CustomState(State):
        def __init__(self):
            self.history = []
            self.current_step = 0
            
        def update(self, new_info):
            self.history.append(new_info)
            self.current_step += 1
    
    class StatefulAgent(BaseAgent):
        def __init__(self, config=None):
            super().__init__(config)
            self.state = CustomState()
        
        def run(self, input_data):
            # Process using state
            self.state.update({"input": input_data})
            # More processing...
            return result

Testing Your Agent
----------------

Create comprehensive tests for your agent:

.. code-block:: python

    import pytest
    from haive.agents.custom import CustomAgent
    
    def test_custom_agent_basic():
        agent = CustomAgent()
        result = agent.run("test input")
        assert result is not None
        
    def test_custom_agent_complex_input():
        agent = CustomAgent()
        result = agent.run({"key": "value", "nested": {"data": 123}})
        assert "processed" in result
EOL

# Create build and clean script
cat > docs/make_docs.sh << 'EOL'
#!/bin/bash
# Script to build documentation

# Exit on error
set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Clean previous build
echo -e "${YELLOW}Cleaning previous build...${NC}"
rm -rf _build

# Create mockup modules
echo -e "${YELLOW}Creating mockup modules...${NC}"
python scripts/create_module_mockups.py

# Build HTML documentation
echo -e "${YELLOW}Building HTML documentation...${NC}"
sphinx-build -b html . _build/html

echo -e "${GREEN}Documentation built successfully! Open _build/html/index.html to view.${NC}"
EOL

# Make the script executable
chmod +x docs/make_docs.sh

# Final step: build the documentation
cd docs
echo -e "${YELLOW}Building initial documentation...${NC}"
poetry run sphinx-build -b html . _build/html

echo -e "${GREEN}Documentation setup complete!${NC}"
echo -e "${GREEN}Build the docs anytime by running:${NC}"
echo -e "  cd docs && ./make_docs.sh"
echo -e "${GREEN}View your documentation at:${NC}"
echo -e "  docs/_build/html/index.html"