import os
from libcst import MetadataWrapper
import libcst as cst
from libcst import Name, Call
class MultiFileRenameTransformer(cst.CSTTransformer):
    """Renames a function across multiple files."""
    
    def __init__(self, old_name: str, new_name: str):
        self.old_name = old_name
        self.new_name = new_name

    def leave_FunctionDef(self, original_node: cst.FunctionDef, updated_node: cst.FunctionDef):
        """Rename function definition."""
        if original_node.name.value == self.old_name:
            return updated_node.with_changes(name=cst.Name(value=self.new_name))
        return updated_node

    def leave_Call(self, original_node: Call, updated_node: Call):
        """Rename function calls."""
        if isinstance(original_node.func, Name) and original_node.func.value == self.old_name:
            return updated_node.with_changes(func=cst.Name(value=self.new_name))
        return updated_node

def rename_function_in_files(directory: str, old_name: str, new_name: str):
    """Renames a function across all `.py` files in a directory."""
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                with open(path, "r") as f:
                    tree = cst.parse_module(f.read())

                wrapper = MetadataWrapper(tree)
                modified_tree = wrapper.visit(MultiFileRenameTransformer(old_name, new_name))

                with open(path, "w") as f:
                    f.write(modified_tree.code)

# rename_function_in_files("src/", "old_func", "new_func")  # ✅ Rename function globally
