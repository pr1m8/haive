FLSTAESR Pipeline
===============

.. raw:: html

    <div class="module-header">
        <h1>📊 FLSTAESR Pipeline</h1>
        <p class="subtitle">Flexible State and Search Representation for document processing</p>
    </div>

Pipeline Stages
-------------

.. grid:: 2 2 2 3
    :gutter: 3
    :padding: 4
    :class-container: pipeline-grid

    .. grid-item-card:: Fetch
        :link: fetch/index
        :class-card: pipeline-card

        Retrieve documents from various sources.

    .. grid-item-card:: Load
        :link: load/index
        :class-card: pipeline-card

        Load and parse different document formats.

    .. grid-item-card:: Split
        :link: split/index
        :class-card: pipeline-card

        Intelligent document chunking strategies.

    .. grid-item-card:: Transform
        :link: transform/index
        :class-card: pipeline-card

        Document transformation and enhancement.

    .. grid-item-card:: Annotate
        :link: annotate/index
        :class-card: pipeline-card

        Add metadata and annotations.

    .. grid-item-card:: Store
        :link: store/index
        :class-card: pipeline-card

        Vector storage and retrieval.

Quick Start
----------

.. code-block:: python
    :caption: Basic Pipeline Usage
    :emphasize-lines: 4,7

    from haive.flstaesr import Pipeline
    from haive.flstaesr.load import PDFLoader
    from haive.flstaesr.transform import TextTransformer
    
    # Create pipeline
    pipeline = Pipeline([
        PDFLoader(),
        TextTransformer(),
        VectorStore()
    ])
    
    # Process documents
    results = pipeline.process("path/to/documents")

Components
---------

.. toctree::
   :maxdepth: 2
   :caption: Pipeline Stages
   :hidden:

   fetch/index
   load/index
   split/index
   transform/index
   annotate/index
   store/index

.. toctree::
   :maxdepth: 1
   :caption: Base Classes
   :hidden:

   base/pipeline
   base/component