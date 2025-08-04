Executable Documentation Examples
=================================

This page demonstrates the power of executable documentation using sphinx-exec-directive.

Basic Code Execution
--------------------

Here's a simple example that runs live:

.. code-block:: python

   # This code runs when building docs!
   import sys
   print(f"Python version: {sys.version}")
   print(f"Current directory: {os.getcwd()}")

   Haive Agent Example
   -------------------

   Let's create a simple agent (note: this requires proper API keys):

.. code-block:: python

   # Import Haive components
   from haive.agents.simple import SimpleAgent
   from haive.core.engine.aug_llm import AugLLMConfig
   
   # Create configuration
   config = AugLLMConfig(

       temperature=0.7,
       max_tokens=100

   )
   
   # Create agent
   agent = SimpleAgent(

       name="doc_example",
       engine=config

   )
   
   print(f"Agent created: {agent.name}")
   print(f"Agent type: {type(agent).__name__}")

   Terminal Commands
   -----------------

   Using sphinx-prompt for terminal examples:

   .. prompt:: bash $

   poetry run python -m haive.agents.simple
   poetry run pytest packages/haive-agents/tests/

   .. prompt:: python >>>

   from haive.agents import SimpleAgent
   agent = SimpleAgent(name="demo")
   agent.name

   Mathematical Computations
   -------------------------

   We can show computations with results:

.. code-block:: python

   import numpy as np
   
   # Create sample data
   data = np.random.randn(100)
   
   print(f"Mean: {np.mean(data):.4f}")
   print(f"Std Dev: {np.std(data):.4f}")
   print(f"Min: {np.min(data):.4f}")
   print(f"Max: {np.max(data):.4f}")

   Error Handling Example
   ----------------------

   Showing how errors are displayed:

.. code-block:: python

   try:

       # This will raise an error
       result = 1 / 0

   except ZeroDivisionError as e:

       print(f"Caught error: {e}")
       print("Error handling works!")

   Interactive Examples Gallery
   ----------------------------

   For more complex examples, see our :doc:`/auto_examples_agents/index` gallery.
