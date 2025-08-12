.. _tags:

Documentation Tags
==================

This page provides an overview of all tags used throughout the documentation.
The sphinx-tags extension automatically generates tag pages when you build the documentation.

How Tags Work
-------------

Each page in the documentation can be tagged using the ``.. tags::`` directive at the top
of the file. When you build the documentation, sphinx-tags will:

1. Create individual tag pages in ``_tags/`` directory
2. Generate a tag index page showing all available tags
3. Add tag badges to each tagged page

Available Tags
--------------

The documentation uses the following tag categories:

- **api**: API documentation and reference materials
- **tutorial**: Step-by-step guides and tutorials
- **config**: Configuration and settings documentation
- **reference**: Reference documentation
- **security**: Security-related documentation
- **performance**: Performance optimization guides
- **ui**: User interface documentation

Using Tags
----------

To add tags to a page, include the following directive at the top of your ``.rst`` file:

.. code-block:: rst

   .. tags:: api, reference
   
   Your Page Title
   ===============
   
   Page content...

Or in Markdown files:

.. code-block:: markdown

   ```{tags} api, reference
   ```
   
   # Your Page Title
   
   Page content...