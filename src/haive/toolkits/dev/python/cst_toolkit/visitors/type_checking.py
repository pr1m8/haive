from typing import Dict
import libcst as cst

class TypeChecker(cst.CSTVisitor):
    """Checks for missing or incorrect type hints in functions."""

    def __init__(self):
        self.missing_annotations = []
        self.incorrect_annotations = []
        self.function_types: Dict[str, str] = {}

    def visit_FunctionDef(self, node):
        """Check if function has type hints."""
        function_name = node.name.value
        has_annotations = any(param.annotation for param in node.params.params)
        return_annotation = node.returns

        if not has_annotations:
            self.missing_annotations.append(function_name)

        if return_annotation and return_annotation.annotation and function_name in self.function_types:
            expected_type = self.function_types[function_name]
            actual_type = return_annotation.annotation.value
            if expected_type != actual_type:
                self.incorrect_annotations.append((function_name, expected_type, actual_type))

    def report_issues(self):
        """Print type checking report."""
        if self.missing_annotations:
            print(f"⚠️ Functions missing type hints: {self.missing_annotations}")
        if self.incorrect_annotations:
            for func, expected, actual in self.incorrect_annotations:
                print(f"❌ Incorrect return type in `{func}`: Expected {expected}, got {actual}")

# Example Usage
def check_types(filepath: str):
    with open(filepath, "r") as f:
        tree = cst.parse_module(f.read())

    checker = TypeChecker()
    tree.visit(checker)
    checker.report_issues()

# check_types("your_script.py")  # ✅ Detect missing type hints & incorrect return types
