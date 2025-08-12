"""Configuration options for doq docstring generator.

This module shows how to configure doq for custom docstring generation.
"""

# Configuration options for doq can be set in multiple ways:
#
# 1. Via pyproject.toml:
#    [tool.doq]
#    template_path = "path/to/custom/templates"
#    formatter = "google"  # or "sphinx", "numpy"
#
# 2. Via setup.cfg:
#    [doq]
#    template_path = path/to/custom/templates
#    formatter = google
#
# 3. Via command line:
#    doq --formatter=google --template_path=templates/

# Example custom template configuration
DOQ_CONFIG = {
    "formatter": "google",  # 'sphinx', 'google', or 'numpy'
    "template_path": None,  # Path to custom Jinja2 templates
    "indent": 4,  # Number of spaces for indentation
}

# Example Google-style template for module docstrings
MODULE_TEMPLATE = '''"""{{ summary|capitalize }}.

{% if description %}
{{ description }}
{% endif %}

{% if examples %}
Examples:
    {{ examples|indent(4) }}
{% endif %}
"""'''

# Example Google-style template for __init__ methods
INIT_TEMPLATE = '''"""Initialize {{ class_name }} instance.

{% if args %}
Args:
{% for arg in args %}
    {{ arg.name }}{% if arg.type %} ({{ arg.type }}){% endif %}: {{ arg.description }}{% if arg.default %} (default: {{ arg.default }}){% endif %}.
{% endfor %}
{% endif %}

{% if raises %}
Raises:
{% for exc in raises %}
    {{ exc.type }}: {{ exc.description }}.
{% endfor %}
{% endif %}
"""'''

# Example function/method template
FUNCTION_TEMPLATE = '''"""{{ summary|capitalize }}.

{% if description %}
{{ description }}
{% endif %}

{% if args %}
Args:
{% for arg in args %}
    {{ arg.name }}{% if arg.type %} ({{ arg.type }}){% endif %}: {{ arg.description }}{% if arg.default %} (default: {{ arg.default }}){% endif %}.
{% endfor %}
{% endif %}

{% if returns %}
Returns:
    {% if returns.type %}{{ returns.type }}: {% endif %}{{ returns.description }}.
{% endif %}

{% if raises %}
Raises:
{% for exc in raises %}
    {{ exc.type }}: {{ exc.description }}.
{% endfor %}
{% endif %}

{% if examples %}
Examples:
    {{ examples|indent(4) }}
{% endif %}
"""'''
