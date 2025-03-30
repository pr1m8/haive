import libcst as cst

class RenameTransformer(cst.CSTTransformer):
    """Renames functions, classes, and variables."""
    def __init__(self, rename_map):
        super().__init__()
        self.rename_map = rename_map  # {old_name: new_name}

    def leave_FunctionDef(self, original_node, updated_node):
        if original_node.name.value in self.rename_map:
            return updated_node.with_changes(name=cst.Name(self.rename_map[original_node.name.value]))
        return updated_node

    def leave_ClassDef(self, original_node, updated_node):
        if original_node.name.value in self.rename_map:
            return updated_node.with_changes(name=cst.Name(self.rename_map[original_node.name.value]))
        return updated_node

    def leave_Name(self, original_node, updated_node):
        if original_node.value in self.rename_map:
            return updated_node.with_changes(value=self.rename_map[original_node.value])
        return updated_node
