import libcst as cst
from libcst import MetadataWrapper
class ImportConsolidator(cst.CSTTransformer):
    """Consolidates duplicate imports into a single statement."""

    def __init__(self):
        self.imports = {}

    def visit_Import(self, node):
        """Track module imports."""
        for alias in node.names:
            module_name = alias.name.value
            self.imports[module_name] = alias.asname.value if alias.asname else None

    def leave_Module(self, original_node, updated_node):
        """Remove duplicates and consolidate imports."""
        unique_imports = [
            cst.Import(names=[cst.ImportAlias(name=cst.Name(module), asname=self.imports[module])])
            for module in self.imports
        ]
        return updated_node.with_changes(body=[*unique_imports, *updated_node.body])

def clean_imports(filepath: str):
    """Merge duplicate imports."""
    with open(filepath, "r") as f:
        tree = cst.parse_module(f.read())

    wrapper = MetadataWrapper(tree)
    modified_tree = wrapper.visit(ImportConsolidator())

    with open(filepath, "w") as f:
        f.write(modified_tree.code)

# clean_imports("your_script.py")  # ✅ Deduplicate imports
