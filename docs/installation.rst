Installation
===========

.. contents:: On this page
   :local:
   :backlinks: none
   :depth: 1

Prerequisites
------------

Before installing Haive, ensure you have:

* Python 3.8 or newer
* pip or Poetry package manager

Standard Installation
-------------------

You can install Haive using pip:

.. code-block:: bash
   :caption: Install with pip
   :emphasize-lines: 1
   
   pip install haive

Poetry Installation
-----------------

If you're using Poetry:

.. code-block:: bash
   :caption: Install with Poetry
   :emphasize-lines: 1
   
   poetry add haive

Development Installation
----------------------

For development or contributing:

.. code-block:: bash
   :caption: Development installation
   
   # Clone the repository
   git clone https://github.com/yourusername/haive.git
   cd haive
   
   # Install with Poetry in development mode
   poetry install

   # Alternatively, with pip
   pip install -e .

Optional Dependencies
-------------------

Haive has several optional features that can be installed as extras:

.. list-table::
   :header-rows: 1
   :widths: 20 30 50

   * - Extra
     - Command
     - Description
   * - **all**
     - ``pip install haive[all]``
     - All optional dependencies
   * - **viz**
     - ``pip install haive[viz]``
     - Visualization tools
   * - **ml**
     - ``pip install haive[ml]``
     - Machine learning integrations

Verifying Installation
--------------------

After installation, you can verify that Haive was installed correctly:

.. code-block:: python
   
   import haive
   
   # Should print the installed version
   print(haive.__version__)

.. admonition:: Troubleshooting
   :class: warning
   
   If you encounter issues during installation, check the following:
   
   * Ensure you have the latest version of pip: ``pip install --upgrade pip``
   * If using Poetry, ensure you have a recent version: ``poetry --version``
   * Check for permissions issues if installing system-wide
   
   For more help, visit our :doc:`troubleshooting guide <troubleshooting>`.

Next Steps
---------

Now that you have Haive installed, check out the :doc:`Quick Start Guide <quickstart>` to begin using it.