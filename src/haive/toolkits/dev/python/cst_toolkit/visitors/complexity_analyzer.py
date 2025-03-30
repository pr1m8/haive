from collections import defaultdict
import libcst as cst
class ComplexityAnalyzer(cst.CSTVisitor):
    """Analyzes cyclomatic complexity of functions."""

    def __init__(self):
        self.complexity = defaultdict(int)

    def visit_FunctionDef(self, node):
        """Track function definitions."""
        self.current_function = node.name.value
        self.complexity[self.current_function] = 1  # Start with 1

    def visit_If(self, node):
        """Increase complexity for conditional branches."""
        if self.current_function:
            self.complexity[self.current_function] += 1

    def visit_For(self, node):
        """Increase complexity for loops."""
        if self.current_function:
            self.complexity[self.current_function] += 1

    def visit_While(self, node):
        """Increase complexity for loops."""
        if self.current_function:
            self.complexity[self.current_function] += 1

    def report_complexity(self):
        """Print complexity report."""
        for func, score in self.complexity.items():
            print(f"🔍 {func} complexity score: {score}")

# Example Usage
def analyze_complexity(filepath: str):
    with open(filepath, "r") as f:
        tree = cst.parse_module(f.read())

    analyzer = ComplexityAnalyzer()
    tree.visit(analyzer)
    analyzer.report_complexity()
