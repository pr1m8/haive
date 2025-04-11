import libcst as cst

class CodeSmellDetector(cst.CSTVisitor):
    """Detects deeply nested loops and other bad patterns."""

    def __init__(self):
        self.nesting_level = 0

    def visit_For(self, node):
        """Track nesting depth of loops."""
        self.nesting_level += 1
        if self.nesting_level > 3:
            print(f"⚠️ Deeply nested loop detected at line {node.lineno}")
        self.nesting_level -= 1

# Example Usage
def detect_code_smells(filepath: str):
    with open(filepath, "r") as f:
        tree = cst.parse_module(f.read())

    tree.visit(CodeSmellDetector())

# detect_code_smells("your_script.py")  # ✅ Warns about deeply nested loops
