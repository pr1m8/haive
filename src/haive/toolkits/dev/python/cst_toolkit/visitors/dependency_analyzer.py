import libcst as cst
from collections import defaultdict

class DependencyAnalyzer(cst.CSTVisitor):
    """Analyzes imports and tracks dependencies within a project."""
    
    def __init__(self):
        self.imports = defaultdict(set)

    def visit_Import(self, node):
        """Handle simple `import module` statements."""
        for alias in node.names:
            self.imports["current_file"].add(alias.name.value)

    def visit_ImportFrom(self, node):
        """Handle `from module import X` statements."""
        if node.module:
            self.imports["current_file"].add(node.module.value)

# Example Usage
def analyze_dependencies(filepath: str):
    with open(filepath, "r") as f:
        tree = cst.parse_module(f.read())

    analyzer = DependencyAnalyzer()
    tree.visit(analyzer)
    
    print(f"Dependencies in {filepath}: {analyzer.imports['current_file']}")

analyze_dependencies("/home/will/Projects/haive/backend/haive/src/haive/agents/simple/agent.py")  # ✅ Detects all imported modules
