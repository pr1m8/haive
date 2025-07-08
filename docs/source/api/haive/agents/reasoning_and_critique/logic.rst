Logic
=====

Logic-based reasoning and analysis agents with specialized engines.

Module path: ``haive.agents.reasoning_and_critique.logic``

Overview
--------

The logic module provides agents for formal reasoning, bias detection, and logical analysis:

- **Bias Detector**: Identifies cognitive biases in reasoning
- **Logical Reasoner**: Formal logic verification
- **Premise Extractor**: Extracts logical premises from text
- **Synthesis Agent**: Synthesizes logical conclusions
- **Uncertainty Analyzer**: Analyzes uncertainty in reasoning

Engines
-------

.. autosummary::
   :toctree: generated
   :maxdepth: 1
   
   haive.agents.reasoning_and_critique.logic.engines.bias_detector
   haive.agents.reasoning_and_critique.logic.engines.logical_reasoner
   haive.agents.reasoning_and_critique.logic.engines.premise_extractor
   haive.agents.reasoning_and_critique.logic.engines.synthesis_agent
   haive.agents.reasoning_and_critique.logic.engines.uncertainty_analyzer

Usage Example
-------------

.. code-block:: python

   from haive.agents.reasoning_and_critique.logic import LogicAgent
   from haive.agents.reasoning_and_critique.logic.engines import (
       BiasDetectorEngine,
       LogicalReasonerEngine
   )
   
   # Create logic agent with specialized engines
   logic_agent = LogicAgent(
       name="logic_analyzer",
       engines=[
           BiasDetectorEngine(),
           LogicalReasonerEngine()
       ]
   )
   
   # Analyze reasoning
   result = await logic_agent.arun({
       "text": "All birds can fly. Penguins are birds. Therefore, penguins can fly.",
       "analysis_type": "full"
   })

Features
--------

- **Multi-Engine Analysis**: Combines multiple logical analysis engines
- **Bias Detection**: Identifies common cognitive biases
- **Formal Logic**: Validates logical structures
- **Premise Extraction**: Extracts and validates premises
- **Uncertainty Quantification**: Measures reasoning confidence

Module Documentation
--------------------

.. automodule:: haive.agents.reasoning_and_critique.logic
   :members:
   :undoc-members:
   :show-inheritance: