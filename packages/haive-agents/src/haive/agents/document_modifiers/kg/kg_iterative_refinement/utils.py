def replace_empty_placeholders(template: str) -> str:
    """Replace `{}` (empty placeholders) with `None`."""
    import re

    return re.sub(r"\{\s*\}", "None", template)
