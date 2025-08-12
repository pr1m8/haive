{#
    CLI Command Documentation Template
    
    Usage:
    {% include "cli-command.rst" %}
    
    Variables:
    - command: The command name 
    - description: Brief description
    - usage: Usage pattern
    - examples: List of example commands
    - options: List of command options
    - see_also: Related commands
#}

{{ command }}
{{ "=" * command|length }}

{{ description }}

Usage
-----

.. prompt:: bash

   $ {{ usage }}

{% if options %}
Options
-------

{% for option in options %}
``{{ option.name }}``
    {{ option.description }}
    {% if option.default %}**Default:** ``{{ option.default }}``{% endif %}

{% endfor %}
{% endif %}

{% if examples %}
Examples
--------

{% for example in examples %}
{{ example.title }}:

.. prompt:: bash

   {{ example.command }}

{% if example.output %}
Output:

.. code-block:: text

   {{ example.output }}
{% endif %}

{% if example.note %}
.. note::

   {{ example.note }}
{% endif %}

{% endfor %}
{% endif %}

{% if see_also %}
See Also
--------

{% for item in see_also %}
* :doc:`{{ item.link }}` - {{ item.description }}
{% endfor %}
{% endif %}