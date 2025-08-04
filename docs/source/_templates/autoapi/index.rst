API Reference
=============

This section contains auto-generated API reference documentation.

.. toctree::

   :maxdepth: 2
   :caption: Packages

   {% for page in pages|selectattr("is_top_level_object") %}
   {% if page.name in ['core', 'agents', 'tools', 'games', 'mcp', 'dataflow', 'prebuilt'] %}
   {{ page.include_path | fix_include_path }}
   {% endif %}
   {% endfor %}

.. note::


   This documentation is automatically generated from the source code using
   `sphinx-autoapi <https://github.com/readthedocs/sphinx-autoapi>`_.
