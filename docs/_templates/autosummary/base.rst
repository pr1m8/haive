{% extends "!autosummary/base.rst" %}

{# Add custom content to all autosummary pages #}

{% block document %}
{{ super() }}

.. note::
   
   This page was auto-generated from the source code. 
   For more examples and usage patterns, see the :doc:`/examples/index`.
{% endblock %}