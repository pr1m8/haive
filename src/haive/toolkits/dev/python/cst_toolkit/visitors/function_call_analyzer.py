from libcst import CSTVisitor, Name, Call
from collections import defaultdict
import libcst as cst
class FunctionCallAnalyzer(CSTVisitor):
    """Tracks function definitions and calls within a script."""
    
    def __init__(self):
        super().__init__()
        self.function_defs = set()
        self.function_calls = defaultdict(int)

    def visit_FunctionDef(self, node):
        """Track function definitions."""
        self.function_defs.add(node.name.value)

    def visit_Call(self, node: Call):
        """Track function calls."""
        if isinstance(node.func, Name):
            self.function_calls[node.func.value] += 1

    def report_unused_functions(self):
        """Find unused function definitions."""
        return [f for f in self.function_defs if self.function_calls[f] == 0]

# Example Usage
def analyze_function_calls(filepath: str):
    with open(filepath, "r") as f:
        tree = cst.parse_module(f.read())

    analyzer = FunctionCallAnalyzer()
    tree.visit(analyzer)
    
    print(f"Unused Functions: {analyzer.report_unused_functions()}")

# analyze_function_calls("your_script.py")  # ✅ Detect unused functions
