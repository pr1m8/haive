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
