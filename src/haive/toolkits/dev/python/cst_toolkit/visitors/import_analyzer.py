import libcst as cst
from collections import defaultdict

class ImportAnalyzer(cst.CSTVisitor):
    """Analyzes and detects issues in Python imports."""

    def __init__(self):
        super().__init__()
        self.imports = set()
        self.import_conflicts = defaultdict(set)
        self.unused_imports = set()
        self.used_identifiers = set()

    def visit_Import(self, node):
        """Track imported modules."""
        for alias in node.names:
            module_name = alias.name.value
            if alias.asname:
                self.import_conflicts[module_name].add(alias.asname.value)
            self.imports.add(module_name)
            self.unused_imports.add(module_name)

    def visit_ImportFrom(self, node):
        """Track `from module import x`."""
        if node.module:
            module_name = node.module.value
            for alias in node.names:
                imported_name = alias.name.value
                self.imports.add(module_name)
                self.import_conflicts[imported_name].add(module_name)
                self.unused_imports.add(imported_name)

    def visit_Name(self, node):
        """Detect used symbols in the script."""
        if node.value in self.unused_imports:
            self.unused_imports.discard(node.value)
        self.used_identifiers.add(node.value)

    def report_issues(self):
        """Generate a report on import issues."""
        print("📌 **Import Analysis Report**")
        print(f"✅ Used Imports: {self.imports}")
        print(f"🛑 Unused Imports: {self.unused_imports}")
        for import_name, conflicts in self.import_conflicts.items():
            if len(conflicts) > 1:
                print(f"⚠️ Conflict: {import_name} is imported from multiple sources: {conflicts}")

# Example Usage
def analyze_imports(filepath: str):
    with open(filepath, "r") as f:
        tree = cst.parse_module(f.read())

    analyzer = ImportAnalyzer()
    tree.visit(analyzer)
    analyzer.report_issues()

# analyze_imports("your_script.py")  # ✅ Detects unused, conflicting, and missing imports
