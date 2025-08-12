"""Pydantic documentation configuration module.

This module contains configuration for documenting Pydantic models
with sphinxcontrib-autodoc-pydantic.
"""

# Pydantic extension
pydantic_extension = "sphinxcontrib.autodoc_pydantic"

# Pydantic model documentation settings
autodoc_pydantic_model_show_json = True
autodoc_pydantic_model_show_config_summary = True
autodoc_pydantic_model_show_validator_summary = True
autodoc_pydantic_model_show_field_summary = True
autodoc_pydantic_model_show_validator_members = True
autodoc_pydantic_model_undoc_members = False
autodoc_pydantic_model_hide_private = True
autodoc_pydantic_model_hide_reused_validator = True
autodoc_pydantic_model_hide_paramlist = False
autodoc_pydantic_model_show_config_member = True
autodoc_pydantic_model_show_dunder = False
autodoc_pydantic_model_signature_prefix = "pydantic model"

# Pydantic field documentation
autodoc_pydantic_field_list_validators = True
autodoc_pydantic_field_doc_policy = "both"
autodoc_pydantic_field_show_constraints = True
autodoc_pydantic_field_show_alias = True
autodoc_pydantic_field_show_default = True
autodoc_pydantic_field_show_required = True
autodoc_pydantic_field_swap_name_and_alias = False
autodoc_pydantic_field_signature_prefix = "field"

# Pydantic validator documentation
autodoc_pydantic_validator_signature_prefix = "validator"
autodoc_pydantic_validator_replace_signature = True

# Pydantic config documentation
autodoc_pydantic_config_signature_prefix = "config"

# BaseSettings documentation
autodoc_pydantic_settings_show_json = False
autodoc_pydantic_settings_show_config_summary = True
autodoc_pydantic_settings_show_field_summary = True
autodoc_pydantic_settings_show_validator_summary = True
autodoc_pydantic_settings_signature_prefix = "pydantic settings"

# Entity relationship diagrams
try:
    import erdantic

    autodoc_pydantic_model_erdantic_figure = True
    autodoc_pydantic_model_erdantic_figure_collapsed = False
except ImportError:
    autodoc_pydantic_model_erdantic_figure = False
    print("Warning: erdantic not installed, disabling ER diagrams")

# Custom CSS for Pydantic documentation
autodoc_pydantic_add_fallback_css_class = True
