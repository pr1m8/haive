import libcst as cst

class TestGenerator(cst.CSTVisitor):
    """Generates test cases from function signatures."""

    def __init__(self):
        self.tests = []

    def visit_FunctionDef(self, node):
        """Generate a basic test function based on function signature."""
        test_name = f"test_{node.name.value}"
        params = [param.name.value for param in node.params.params]
        test_body = f"    assert {node.name.value}({', '.join(params)}) is not None"

        self.tests.append(f"def {test_name}():\n    # TODO: Add assertions\n{test_body}\n")

    def generate_tests(self):
        """Prints generated test cases."""
        print("\n".join(self.tests))

# Example Usage
def generate_tests(filepath: str):
    with open(filepath, "r") as f:
        tree = cst.parse_module(f.read())

    generator = TestGenerator()
    tree.visit(generator)
    generator.generate_tests()

# generate_tests("your_script.py")  # ✅ Generate test cases
