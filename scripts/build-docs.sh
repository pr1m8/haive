#!/bin/bash
# This script helps build Sphinx documentation with mockup modules
# Create directory structure for custom templates
# Create directory structure for API docs
mkdir -p docs/api/agents
mkdir -p docs/api/flstaesr
mkdir -p docs/api/core

# Create main API index file
cat > docs/api/index.rst << 'EOL'
API Reference
============

.. toctree::
   :maxdepth: 2
   :caption: API Documentation:

   agents/index
   flstaesr/index
   core/index
EOL

# Create Agents index
cat > docs/api/agents/index.rst << 'EOL'
Agents
======

.. raw:: html

    <div class="feature-description">
        <p>The Agents module provides various agent implementations for different tasks and strategies.</p>
    </div>

.. toctree::
   :maxdepth: 2

   summarizer
   web_nav
   self_discover
   tot
   react_agent

.. admonition:: Developing New Agents
   :class: tip

   To create a new agent, follow the base agent interface and implement the required methods.
   See the :doc:`agent development guide <../../development/creating_agents>` for more information.
EOL

# Create FlStaeSR index
cat > docs/api/flstaesr/index.rst << 'EOL'
FlStaeSR: Flexible State and Search Representation
=================================================

.. raw:: html

    <div class="feature-description">
        <p>The FlStaeSR module provides flexible state and search representation tools.</p>
    </div>

.. toctree::
   :maxdepth: 2

   transform
   annotate
EOL

# Create Core index
cat > docs/api/core/index.rst << 'EOL'
Core
====

.. raw:: html

    <div class="feature-description">
        <p>The Core module provides foundational functionality for the Haive framework.</p>
    </div>

.. toctree::
   :maxdepth: 2

   utils
   config
EOL

# Create placeholder for agent modules
cat > docs/api/agents/summarizer.rst << 'EOL'
Summarizer Agent
==============

.. currentmodule:: haive.agents.summarizer

.. automodule:: haive.agents.summarizer
   :no-members:
   :no-inherited-members:

The Summarizer Agent helps create concise summaries of input text.

.. rubric:: Modules

.. autosummary::
   :toctree: generated
   
   agent
   aug_llms
   prompts

Agent
-----

.. automodule:: haive.agents.summarizer.agent
   :members:
   :undoc-members:
   :show-inheritance:

Augmented LLMs
-------------

.. automodule:: haive.agents.summarizer.aug_llms
   :members:
   :undoc-members:
   :show-inheritance:

Prompts
------

.. automodule:: haive.agents.summarizer.prompts
   :members:
   :undoc-members:
   :show-inheritance:
EOL

# Create placeholder for another agent
cat > docs/api/agents/web_nav.rst << 'EOL'
Web Navigation Agent
=================

.. currentmodule:: haive.agents.web_nav

.. automodule:: haive.agents.web_nav
   :no-members:
   :no-inherited-members:

The Web Navigation Agent helps navigate websites and retrieve information.

.. rubric:: Modules

.. autosummary::
   :toctree: generated
   
   agent
   state
   tools

Agent
-----

.. automodule:: haive.agents.web_nav.agent
   :members:
   :undoc-members:
   :show-inheritance:

State
-----

.. automodule:: haive.agents.web_nav.state
   :members:
   :undoc-members:
   :show-inheritance:

Tools
-----

.. automodule:: haive.agents.web_nav.tools
   :members:
   :undoc-members:
   :show-inheritance:
EOL

# Create placeholder for self_discover agent
cat > docs/api/agents/self_discover.rst << 'EOL'
Self-Discover Agent
=================

.. currentmodule:: haive.agents.self_discover

.. automodule:: haive.agents.self_discover
   :no-members:
   :no-inherited-members:

The Self-Discover Agent has capability for autonomous exploration and learning.

.. rubric:: Modules

.. autosummary::
   :toctree: generated
   
   agent
   aug_llms
   state

Agent
-----

.. automodule:: haive.agents.self_discover.agent
   :members:
   :undoc-members:
   :show-inheritance:

Augmented LLMs
-------------

.. automodule:: haive.agents.self_discover.aug_llms
   :members:
   :undoc-members:
   :show-inheritance:

State
-----

.. automodule:: haive.agents.self_discover.state
   :members:
   :undoc-members:
   :show-inheritance:
EOL

# Create placeholder for tot agent
cat > docs/api/agents/tot.rst << 'EOL'
Tree of Thought Agent
==================

.. currentmodule:: haive.agents.tot

.. automodule:: haive.agents.tot
   :no-members:
   :no-inherited-members:

The Tree of Thought (ToT) Agent implements reasoning by exploring multiple thought branches.

.. rubric:: Modules

.. autosummary::
   :toctree: generated
   
   agent
   state

Agent
-----

.. automodule:: haive.agents.tot.agent
   :members:
   :undoc-members:
   :show-inheritance:

State
-----

.. automodule:: haive.agents.tot.state
   :members:
   :undoc-members:
   :show-inheritance:
EOL

# Create placeholder for react agent
cat > docs/api/agents/react_agent.rst << 'EOL'
ReAct Agent
=========

.. currentmodule:: haive.agents.react_agent

.. automodule:: haive.agents.react_agent
   :no-members:
   :no-inherited-members:

The ReAct Agent implements the Reasoning and Acting framework.

.. rubric:: Modules

.. autosummary::
   :toctree: generated
   
   base

Base
----

.. automodule:: haive.agents.react_agent.base
   :members:
   :undoc-members:
   :show-inheritance:
EOL

# Create placeholder for transform module
cat > docs/api/flstaesr/transform.rst << 'EOL'
Transform
========

.. currentmodule:: haive.flstaesr.transform

.. automodule:: haive.flstaesr.transform
   :no-members:
   :no-inherited-members:

The Transform module provides tools for transforming data representations.

.. rubric:: Modules

.. autosummary::
   :toctree: generated
   
   base
   inspect_experiment

Base
----

.. automodule:: haive.flstaesr.transform.base
   :members:
   :undoc-members:
   :show-inheritance:

Inspection and Experimentation
----------------------------

.. automodule:: haive.flstaesr.transform.inspect_experiment
   :members:
   :undoc-members:
   :show-inheritance:
EOL

# Create placeholder for annotate module
cat > docs/api/flstaesr/annotate.rst << 'EOL'
Annotate
=======

.. currentmodule:: haive.flstaesr.annotate

.. automodule:: haive.flstaesr.annotate
   :no-members:
   :no-inherited-members:

The Annotate module provides tools for annotating data.

.. rubric:: Modules

.. autosummary::
   :toctree: generated
   
   base

Base
----

.. automodule:: haive.flstaesr.annotate.base
   :members:
   :undoc-members:
   :show-inheritance:
EOL

# Create placeholder for core modules
cat > docs/api/core/utils.rst << 'EOL'
Utilities
========

.. currentmodule:: haive.core.utils

.. automodule:: haive.core.utils
   :members:
   :undoc-members:
   :show-inheritance:

Utility functions and classes used throughout the Haive framework.
EOL

cat > docs/api/core/config.rst << 'EOL'
Configuration
===========

.. currentmodule:: haive.core.config

.. automodule:: haive.core.config
   :members:
   :undoc-members:
   :show-inheritance:

Configuration management tools and classes.
EOL

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

# Create mockup modules for documentation
echo -e "${YELLOW}Creating mockup modules for documentation...${NC}"
python docs/scripts/create_module_mockups.py

# Add mockup directory to Python path in conf.py
MOCKUP_DIR="$(pwd)/docs/mockups"
echo -e "${YELLOW}Using mockup modules from: ${MOCKUP_DIR}${NC}"

# Copy any existing CSS/JS files
if [ ! -f "docs/_static/custom.css" ]; then
    echo -e "${YELLOW}Creating placeholder custom.css file...${NC}"
    cat > docs/_static/custom.css << EOL
/* Custom styles for Haive documentation */
EOL
fi

if [ ! -f "docs/_static/custom.js" ]; then
    echo -e "${YELLOW}Creating placeholder custom.js file...${NC}"
    cat > docs/_static/custom.js << EOL
// Custom JavaScript for Haive documentation
EOL
fi

# Create placeholder images if needed
if [ ! -f "docs/_static/logo.png" ]; then
    echo -e "${YELLOW}Creating placeholder logo...${NC}"
    # Use a simple command to create a text-based placeholder image
    convert -size 200x100 canvas:white -font Arial -pointsize 24 -fill black -gravity center -annotate 0 "Haive" docs/_static/logo.png 2>/dev/null || echo "ImageMagick not available, skipping image creation"
fi

if [ ! -f "docs/_static/favicon.ico" ]; then
    echo -e "${YELLOW}Creating placeholder favicon...${NC}"
    convert -size 32x32 canvas:white -font Arial -pointsize 16 -fill black -gravity center -