Installation
============

Requirements
------------

* Python 3.9 or higher*
* Poetry (recommended) or pip*
* Git*

Quick Install
-------------

Using Poetry (Recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    # Clone the repository
    git clone https://github.com/will-astley/haive.git
    cd haive/backend/haive

    # Install with Poetry
    poetry install

    # Activate the environment
    poetry shell

    Using pip
    ~~~~~~~~~

.. code-block:: bash

    # Clone and install
    git clone https://github.com/will-astley/haive.git
    cd haive/backend/haive
    pip install -e .

    Development Installation
    ------------------------

    For development work, install with all extras:

.. code-block:: bash

    # Install all development dependencies
    poetry install --all-extras

    # Install pre-commit hooks
    pre-commit install

    Package Selection
    -----------------

    You can install specific packages as needed:

.. code-block:: bash

    # Core framework only
    poetry install --only main

    # With agents
    poetry install --extras agents

    # With games
    poetry install --extras games

    # Everything
    poetry install --all-extras

    Configuration
    -------------

    Create a `.env` file in your project root:

.. code-block:: bash

    # LLM Configuration
    OPENAI_API_KEY=your_openai_key
    ANTHROPIC_API_KEY=your_anthropic_key

    # Optional: Custom settings
    HAIVE_LOG_LEVEL=INFO
    HAIVE_CACHE_DIR=~/.haive/cache

    Verification
    ------------

    Test your installation:

.. code-block:: python

    from haive.agents.simple import SimpleAgent
    from haive.core.engine import create_engine

    # Create a simple agent
    engine = create_engine("openai", model="gpt-4")
    agent = SimpleAgent(name="test", engine=engine)

    print("✅ Haive installed successfully!")

    Troubleshooting
    ---------------

    Common issues and solutions:

    **Import Errors**
    Ensure you're in the correct virtual environment and all packages are installed

    **Missing Dependencies**
    Run ``poetry install --all-extras`` to install all optional dependencies

    **API Key Issues**
    Verify your API keys are set correctly in your environment
