import os
from libcst import MetadataWrapper
import libcst as cst
class FunctionLoggingTransformer(cst.CSTTransformer):
    """Adds logging to function calls."""

    def __init__(self):
        super().__init__()

    def leave_FunctionDef(self, original_node: cst.FunctionDef, updated_node: cst.FunctionDef):
        """Inject logging at the start of every function."""
        log_statement = cst.parse_statement(f'print("Executing {original_node.name.value}")')

        new_body = [log_statement, *updated_node.body.body]
        return updated_node.with_changes(body=updated_node.body.with_changes(body=new_body))

def add_logging(filepath: str):
    """Inject logging into functions."""
    with open(filepath, "r") as f:
        tree = cst.parse_module(f.read())

    wrapper = MetadataWrapper(tree)
    modified_tree = wrapper.visit(FunctionLoggingTransformer())

    with open(filepath, "w") as f:
        f.write(modified_tree.code)

# add_logging("your_script.py")  # ✅ Add logging to all functions
