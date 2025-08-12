CLI Reference
=============

.. tags:: reference, api

This page provides automatically generated documentation for all command-line interfaces in PyAutoDoc.

Build Documentation Script
---------------------------

The enhanced documentation builder script with error reporting.

.. argparse::
   :module: scripts.build-docs
   :func: get_argument_parser
   :prog: build-docs.py

   The enhanced Sphinx documentation builder provides detailed error reporting and debugging capabilities. It parses sphinx-build output for warnings and errors, categorizes them, and displays them in a user-friendly format.

   Features:
   - Detailed error categorization and reporting
   - Line-by-line error context
   - Warning suppression options
   - Multiple output formats supported

Configuration Loader
---------------------

The configuration system testing and validation tool.

.. automodule:: docs.config.config_loader
   :members: main

Usage Examples
--------------

**Enhanced Documentation Build:**

.. prompt:: bash

   $ python scripts/build-docs.py

**Build with Custom Options:**

.. prompt:: bash

   $ python scripts/build-docs.py --builder html --source docs/source --build docs/build

**Quiet Mode:**

.. prompt:: bash

   $ python scripts/build-docs.py --quiet

**Test Configuration:**

.. prompt:: bash

   $ python docs/config/config_loader.py

**Shell Script Build:**

.. prompt:: bash

   $ chmod +x docs/build-docs.sh
   $ ./docs/build-docs.sh