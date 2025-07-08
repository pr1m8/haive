Summarizer Agents
=================

Text summarization agents using different strategies.

Agents
------

.. autosummary::
   :toctree: generated
   :maxdepth: 1
   
   haive.agents.document_modifiers.summarizer.SummarizerAgent
   haive.agents.document_modifiers.summarizer.iterative_refinement.IterativeSummarizer

Map-Branch Summarizer
---------------------

The main summarizer uses a map-branch approach for processing large documents:

.. code-block:: python

   from haive.agents.document_modifiers.summarizer import SummarizerAgent
   
   summarizer = SummarizerAgent(
       name="map_branch_summarizer",
       engine=llm_engine,
       config=SummarizerConfig(
           chunk_size=1000,
           overlap=100,
           final_summary_max_tokens=500
       )
   )
   
   result = await summarizer.arun({
       "documents": documents,
       "query": "Summarize the key technical innovations"
   })

Features:
- Parallel chunk processing
- Context-aware summarization
- Configurable chunk sizes
- Query-focused summaries

Iterative Refinement Summarizer
-------------------------------

For high-quality summaries through iterative improvement:

.. code-block:: python

   from haive.agents.document_modifiers.summarizer.iterative_refinement import IterativeSummarizer
   
   summarizer = IterativeSummarizer(
       name="iterative_summarizer",
       engine=llm_engine,
       max_iterations=3
   )
   
   result = await summarizer.arun({
       "documents": documents,
       "refinement_criteria": ["clarity", "completeness", "conciseness"]
   })

Features:
- Multi-pass refinement
- Quality scoring
- Customizable criteria
- Progressive improvement