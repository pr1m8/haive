{% if not obj.display %}
:orphan:
{% endif %}

{# -------------------------------------------------------- #}
{#  Detect Class Type: Pydantic, Dataclass, Enum, or Flag  #}
{# -------------------------------------------------------- #}
{% set bases_string = obj.bases | join(" ") %}
{% set is_pydantic = "BaseModel" in bases_string or "BaseSettings" in bases_string %}
{% set is_dataclass = "@dataclass" in (obj.docstring or "") or "dataclass" in (obj.docstring or "") %}
{% set is_enum = "Enum" in bases_string %}
{% set is_flag = "Flag" in bases_string %}


{# ------------------------------ #}
{#  Graphviz Inheritance Diagram  #}
{# ------------------------------ #}
.. toggle:: Show Inheritance Diagram

   Inheritance diagram for {{ obj.name }}:

   .. graphviz::
      :align: center

      digraph inheritance_{{ obj.name | replace('.', '_') }} {
        node [shape=record];
        "{{ obj.name }}" [label="{{ obj.name }}"];
        {% for base in obj.bases %}
        "{{ base }}" -> "{{ obj.name }}";
        {% endfor %}
      }

{# ----------------------------- #}
{#        Pydantic Model        #}
{# ----------------------------- #}
{% if is_pydantic %}
.. autopydantic_model:: {{ obj.id }}
   :members:
   :undoc-members:
   :show-inheritance:
   :model-show-field-summary:
   :model-show-config-summary:
   :model-show-validator-members:
   :model-show-validator-summary:
   :model-show-json:
   :field-list-validators:
   :field-show-constraints:

{# ----------------------------- #}
{#         Dataclass             #}
{# ----------------------------- #}
{% elif is_dataclass %}
.. autoclass:: {{ obj.id }}
   :members:
   :undoc-members:
   :show-inheritance:

   .. note::

      **{{ obj.name }}** is a dataclass. Enhanced schema documentation will be available soon.

{# ----------------------------- #}
{#         Enum Classes         #}
{# ----------------------------- #}
{% elif is_enum or is_flag %}
.. autoclass:: {{ obj.id }}
   :members:
   :undoc-members:
   :show-inheritance:

   {% if is_flag %}
   .. note::

      **{{ obj.name }}** is a Flag Enum defined in ``{{ obj.module or obj.id.split('.')[:-1] | join('.') }}``.
   {% else %}
   .. note::

      **{{ obj.name }}** is an Enum defined in ``{{ obj.module or obj.id.split('.')[:-1] | join('.') }}``.
   {% endif %}

{# ----------------------------- #}
{#        Fallback Default      #}
{# ----------------------------- #}
{% else %}
.. autoclass:: {{ obj.id }}
   :members:
   :undoc-members:
   :show-inheritance:
{% endif %}
