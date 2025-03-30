import libcst as cst

class PrintToLoggingTransformer(cst.CSTTransformer):
    """Replaces print statements with logging."""

    def leave_Expr(self, original_node: cst.Expr, updated_node: cst.Expr):
        """Replace print calls with logging.info()."""
        if isinstance(original_node.value, cst.Call) and isinstance(original_node.value.func, cst.Name):
            if original_node.value.func.value == "print":
                return updated_node.with_changes(
                    value=cst.Call(func=cst.Name("logging.info"), args=original_node.value.args)
                )
        return updated_node

# Example Usage
def replace_print_with_logging(filepath: str):
    with open(filepath, "r") as f:
        tree = cst.parse_module(f.read())

    modified_tree = tree.visit(PrintToLoggingTransformer())

    with open(filepath, "w") as f:
        f.write(modified_tree.code)

# replace_print_with_logging("your_script.py")  # ✅ Auto-fixes `print()`
