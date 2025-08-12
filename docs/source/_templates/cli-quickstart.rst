{#
    CLI Quick Start Guide Template
    
    Creates a comprehensive quick start guide for CLI tools
    
    Variables:
    - tool_name: Name of the CLI tool
    - install_cmd: Installation command
    - basic_usage: List of basic commands
    - advanced_usage: List of advanced commands
#}

{{ tool_name }} Quick Start
{{ "=" * (tool_name + " Quick Start")|length }}

Installation
------------

.. prompt:: bash

   $ {{ install_cmd }}

Basic Usage
-----------

{% for cmd in basic_usage %}
**{{ cmd.title }}**

.. prompt:: bash

   $ {{ cmd.command }}

{{ cmd.description }}

{% if cmd.example_output %}
.. code-block:: text

   {{ cmd.example_output }}
{% endif %}

{% endfor %}

Advanced Commands
-----------------

{% for cmd in advanced_usage %}
**{{ cmd.title }}**

.. prompt:: bash

   $ {{ cmd.command }}

{{ cmd.description }}

{% if cmd.options %}
Available options:

{% for opt in cmd.options %}
* ``{{ opt.flag }}`` - {{ opt.description }}
{% endfor %}
{% endif %}

{% endfor %}

Common Workflows
----------------

**Development Workflow:**

.. prompt:: bash

   $ poetry install --with docs
   $ poetry run sphinx-build -b html docs/source docs/build
   $ poetry run sphinx-autobuild docs/source docs/build

**Production Build:**

.. prompt:: bash

   $ poetry install --only main --only docs
   $ poetry run sphinx-build -b html -W docs/source docs/build