{{ fullname }}
{{ underline }}

.. currentmodule:: {{ module }}

.. autoclass:: {{ objname }}
   :members:
   :show-inheritance:
   :inherited-members:
   :special-members: __init__
   
.. agent-doc:: {{ fullname }}
   :show-example: true
   :show-visualization: true
   :show-config: true
   
.. rubric:: Related Resources

{% set module_path = module.replace('.', '/') %}
{% set example_file = module_path + '/example.py' %}
{% set config_file = module_path + '/config.py' %}

.. admonition:: Example Files
   :class: seealso
   
   - Example usage: ``{{ example_file }}``
   - Configuration: ``{{ config_file }}``
   
   Run the example:
   
   .. code-block:: bash

    python -m {{ module }}.example