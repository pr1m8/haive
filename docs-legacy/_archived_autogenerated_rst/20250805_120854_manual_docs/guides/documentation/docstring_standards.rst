Docstring Standards



Haive uses Google-style docstrings for all code documentation. This page outlines the standards and provides examples for each type of docstring.

Module Docstrings


----------------

Module docstrings should be placed at the top of the file and describe the module's purpose, functionality, and provide usage examples.

.. code-block:: python

    # Code example here

    """Module name and brief description.

    This module provides [functionality description].

    Example:
    >>> from haive.games.module_name import ClassName
    >>> instance = ClassName()
    >>> result = instance.method()

    Typical usage:
    - Step 1 description
    - Step 2 description



    Class Docstrings




    Class docstrings should describe the class's purpose, functionality, attributes, and provide usage examples.

.. code-block:: python

    # Code example here

    class ClassName:
    """Brief description of the class.

    Detailed description of the class's purpose and functionality.

    Attributes:
    attr1 (type): Description of attribute 1.
    attr2 (type): Description of attribute 2.

    Example:
    >>> instance = ClassName()
    >>> instance.method()



    Method/Function Docstrings




    Function docstrings should describe the function's purpose, parameters, return values, exceptions, and provide usage examples.

.. code-block:: python

    # Code example here

    def function_name(param1, param2=default):
    """Brief description of the function.

    Args:
    param1 (type): Description of parameter 1.
    param2 (type, optional): Description of parameter 2. Defaults to default.

    Returns:
    type: Description of the return value.

    Raises:
    Exception: Description of when this exception is raised.

    Example:
    >>> result = function_name("value", param2=42)



    Pydantic Models




    Pydantic models should have class docstrings and field descriptions.

.. code-block:: python

    # Code example here

    class ModelName(BaseModel):
    """Brief description of the model.

    Attributes:
    field1 (type): Description of field 1.
    field2 (type): Description of field 2.


        field1: type = Field(..., description="Description of field 1")
        field2: type = Field(default, description="Description of field 2")

    Game-Specific Docstrings




    For game modules, docstrings should include game-specific information:

.. code-block:: python

    # Code example here

    """Chess board game implementation.

    This module provides a complete implementation of Chess for the Haive
    games framework, including game state management, rules enforcement, move validation,
    and agent integration.

    Example:
    >>> from haive.games.chess import ChessAgent
    >>> agent = ChessAgent()
    >>> final_state = agent.run_game(visualize=True)

    Typical usage:
    - Create a game agent
    - Configure game parameters
    - Run a full game or analyze specific positions
    - Inspect game state and results



    Special Cases




    1. **Abstract Method*s**: Should include a description of what implementing classes should do.**

    2.*** *Propertie**s**: Should document the value being returned rather than parameters.

    3.*** *Private Method**s**: Should still be documented even though they're not part of the public API.

    Docstring Generation




    The ``add_docstrings`.py`` script in` the`` script``s`` directory can automatically generate appropriate docstrings for your code based on naming conventions and context.

.. code-block:: bash

    python scripts/add_docstrings.py --path` src/haive/games/chess``***`
`
`
